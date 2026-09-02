#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Recupere les donnees ouvertes et ecrit data/prices.json.

Couche electricite (ENTSO-E Transparency Platform)
  price   documentType A44  prix day-ahead, moyenne baseload       EUR/MWh
  load    documentType A65  consommation realisee, energie du jour GWh

Couche gaz (GIE)
  storage AGSI+  taux de remplissage des stockages                 %
  netwd   AGSI+  soutirage net de la journee (negatif = injection) GWh
  lng     ALSI   taux de remplissage des terminaux GNL             %

Aucune donnee sous licence commerciale n'est collectee ici.

Le script est PARALLELISE et BORNE DANS LE TEMPS : il ne peut pas tourner
indefiniment. Passe le butoir, il ecrit ce qu'il a et sort proprement.

Variables d'environnement :
  ENTSOE_TOKEN  obligatoire pour la couche electricite
  GIE_KEY       obligatoire pour la couche gaz (AGSI+ et ALSI)
                AGSI_KEY est accepte comme alias historique
  MAX_SECONDS   butoir global, defaut 420
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from datetime import date, timedelta, datetime, timezone

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "src"))

from countries_a import A
from countries_b import B
from countries_c import C

COUNTRIES = {}
COUNTRIES.update(A)
COUNTRIES.update(B)
COUNTRIES.update(C)

ENTSOE_URL = "https://web-api.tp.entsoe.eu/api"
AGSI_URL = "https://agsi.gie.eu/api"
ALSI_URL = "https://alsi.gie.eu/api"

ALSI_COUNTRIES = {"BE", "DE", "ES", "FI", "FR", "GB", "GR", "HR",
                  "IT", "LT", "NL", "PL", "PT", "SE"}

TOKEN = os.environ.get("ENTSOE_TOKEN", "").strip()
GIE_KEY = (os.environ.get("GIE_KEY") or os.environ.get("AGSI_KEY") or "").strip()

HTTP_TIMEOUT = 15
WORKERS = 2

# Les deux API sont derriere une protection anti-bot qui rejette la signature
# par defaut d'urllib ("Python-urllib/3.x") : ENTSO-E repond alors 503 avec une
# page HTML, GIE renvoie un 403 Cloudflare "error code: 1010".
UA = "AtlasEnergy/1.0 (+https://github.com/liapo972/Atlas-Energy)"
BASE_HEADERS = {
    "User-Agent": UA,
    "Accept": "application/xml, text/xml, application/json;q=0.9, */*;q=0.8",
    "Accept-Language": "en",
}
MAX_SECONDS = int(os.environ.get("MAX_SECONDS", "420"))
DEADLINE = time.time() + MAX_SECONDS


class Expired(Exception):
    pass


def left():
    return DEADLINE - time.time()


BACKOFF = [2, 6, 15, 30]


def http_get(url, headers=None):
    """Reessaie avec attente croissante sur 429/5xx : l'API ENTSO-E rend
    beaucoup de 503 quand elle est sollicitee trop vite."""
    last = None
    for attempt in range(len(BACKOFF) + 1):
        if left() < 8:
            raise Expired("butoir atteint")
        try:
            h = dict(BASE_HEADERS)
            h.update(headers or {})
            req = urllib.request.Request(url, headers=h)
            with urllib.request.urlopen(req, timeout=min(HTTP_TIMEOUT, max(8, left()))) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            body = ""
            try:
                body = e.read(300).decode("utf-8", "replace").strip().replace("\n", " ")
            except Exception:
                pass
            last = RuntimeError("HTTP %s%s" % (e.code, (" — " + body[:160]) if body else ""))
            # Une page HTML ou un blocage anti-bot ne sont pas transitoires :
            # inutile de reessayer, on economise le budget de temps.
            low = body.lower()
            if "<!doctype html" in low or "<html" in low or "error code: 10" in low:
                raise last
            if e.code not in (429, 500, 502, 503, 504):
                raise last
        except Exception as e:
            last = RuntimeError("%s: %s" % (type(e).__name__, e))
        if attempt < len(BACKOFF):
            wait = BACKOFF[attempt]
            if left() < wait + 10:
                break
            time.sleep(wait)
    raise last or RuntimeError("echec")


def strip_ns(tag):
    return tag.split("}")[-1] if "}" in tag else tag


def entsoe(params):
    q = dict(params)
    q["securityToken"] = TOKEN
    raw = http_get(ENTSOE_URL + "?" + urllib.parse.urlencode(q))
    root = ET.fromstring(raw)
    if strip_ns(root.tag) == "Acknowledgement_MarketDocument":
        reason = " ".join(e.text or "" for e in root.iter()
                          if strip_ns(e.tag) == "text")
        raise RuntimeError((reason.strip() or "pas de donnees")[:160])
    return root


def window(day):
    return (day.strftime("%Y%m%d") + "0000",
            (day + timedelta(days=1)).strftime("%Y%m%d") + "0000")


def fetch_price(eic, day):
    start, end = window(day)
    root = entsoe({"documentType": "A44", "in_Domain": eic, "out_Domain": eic,
                   "periodStart": start, "periodEnd": end})
    vals, currency = [], "EUR"
    for el in root.iter():
        t = strip_ns(el.tag)
        if t == "currency_Unit.name" and el.text:
            currency = el.text.strip()
        if t == "Point":
            for c in el:
                if strip_ns(c.tag) == "price.amount" and c.text:
                    vals.append(float(c.text))
    if not vals:
        raise RuntimeError("aucun point de prix")
    return {"value": round(sum(vals) / len(vals), 2), "currency": currency}


def fetch_load(eic, day):
    start, end = window(day)
    root = entsoe({"documentType": "A65", "processType": "A16",
                   "outBiddingZone_Domain": eic,
                   "periodStart": start, "periodEnd": end})
    vals = []
    for el in root.iter():
        if strip_ns(el.tag) == "Point":
            for c in el:
                if strip_ns(c.tag) == "quantity" and c.text:
                    vals.append(float(c.text))
    if not vals:
        raise RuntimeError("aucun point de consommation")
    return {"value": round((sum(vals) / len(vals)) * 24 / 1000.0, 1)}


def gie(base, country, day, field="full"):
    """AGSI+/ALSI publient avec un decalage : on demande une fenetre de six
    jours et on retient la ligne la plus recente qui porte vraiment la valeur."""
    q = urllib.parse.urlencode({
        "country": country,
        "from": (day - timedelta(days=6)).isoformat(),
        "to": day.isoformat(),
        "size": 30})
    raw = http_get(base + "?" + q, headers={"x-key": GIE_KEY})
    rows = (json.loads(raw) or {}).get("data") or []
    if not rows:
        raise RuntimeError("aucune donnee sur la fenetre")
    for row in rows:                      # l'API renvoie du plus recent au plus ancien
        v = row.get(field)
        if v not in (None, "", "-", "N/A"):
            return row
    raise RuntimeError("fenetre sans valeur '%s'" % field)


def num(row, field):
    v = row.get(field)
    if v in (None, "", "-", "N/A"):
        raise RuntimeError("champ '%s' absent" % field)
    return float(v)


def run_jobs(jobs, label):
    """jobs = [(cle_metrique, code_pays, callable)] -> (resultats, erreurs)"""
    out, errors = {}, []
    if not jobs:
        return out, errors

    done = [0]

    def one(job):
        key, code, fn = job
        try:
            return key, code, fn(), None
        except Expired as e:
            return key, code, None, str(e)
        except Exception as e:
            return key, code, None, "%s: %s" % (type(e).__name__, e)

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        for key, code, value, err in pool.map(one, jobs):
            done[0] += 1
            if value is not None:
                out.setdefault(key, {})[code] = value
            elif err:
                errors.append("%s/%s: %s" % (key, code, err))
            if done[0] % 20 == 0:
                print("   ... %s %d/%d (%ds restantes)"
                      % (label, done[0], len(jobs), max(0, int(left()))), flush=True)
    return out, errors



class _Tee:
    """Duplique la sortie vers un fichier du depot, pour pouvoir relire le
    dernier run sans passer par l'interface GitHub."""

    def __init__(self, path):
        self.path = path
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.fh = open(path, "w", encoding="utf-8")
        self.stdout = sys.stdout

    def write(self, s):
        self.stdout.write(s)
        self.fh.write(s)

    def flush(self):
        self.stdout.flush()
        self.fh.flush()

def main():
    sys.stdout = _Tee(os.path.join(ROOT, "data", "last_run_data.txt"))
    day = date.today() - timedelta(days=1)
    metrics = {k: {} for k in ("price", "load", "storage", "netwd", "lng")}
    errors = []

    print("Journee visee :", day.isoformat(), flush=True)
    print("Butoir global :", MAX_SECONDS, "secondes", flush=True)
    print("Token ENTSO-E :", ("present (%d caracteres)" % len(TOKEN)) if TOKEN else "ABSENT", flush=True)
    print("Cle GIE       :", ("presente (%d caracteres)" % len(GIE_KEY)) if GIE_KEY else "ABSENTE", flush=True)

    # --- sonde : un seul appel de chaque API, verbeux ---
    if TOKEN:
        print("\nSonde ENTSO-E (France)...", flush=True)
        try:
            r = fetch_price("10YFR-RTE------C", day)
            print("  OK ->", r, flush=True)
        except Exception as e:
            print("  ECHEC ->", type(e).__name__, ":", e, flush=True)
    if GIE_KEY:
        print("Sonde GIE AGSI+ (France)...", flush=True)
        try:
            row = gie(AGSI_URL, "FR", day)
            print("  OK -> full =", row.get("full"), flush=True)
        except Exception as e:
            print("  ECHEC ->", type(e).__name__, ":", e, flush=True)
    print("", flush=True)

    jobs = []
    if TOKEN:
        for code, meta in COUNTRIES.items():
            eic = meta.get("eic")
            if not eic:
                continue
            jobs.append(("price", code, lambda e=eic: fetch_price(e, day)))
            jobs.append(("load", code, lambda e=eic: fetch_load(e, day)))
    else:
        errors.append("electricite: ENTSOE_TOKEN absent")

    if GIE_KEY:
        for code, meta in COUNTRIES.items():
            ag = meta.get("agsi")
            if ag:
                jobs.append(("gas", code, lambda a=ag: gie(AGSI_URL, a, day)))
            if code in ALSI_COUNTRIES:
                jobs.append(("lng", code, lambda c=code: gie(ALSI_URL, c, day)))
    else:
        errors.append("gaz: GIE_KEY absent")

    print("Requetes a lancer :", len(jobs), flush=True)
    res, errs = run_jobs(jobs, "requetes")
    errors.extend(errs)

    metrics["price"] = res.get("price", {})
    metrics["load"] = res.get("load", {})

    for code, row in (res.get("gas") or {}).items():
        try:
            metrics["storage"][code] = {"value": round(num(row, "full"), 1)}
        except Exception as e:
            errors.append("storage/%s: %s" % (code, e))
        try:
            metrics["netwd"][code] = {"value": round(num(row, "netWithdrawal"), 1)}
        except Exception as e:
            errors.append("netwd/%s: %s" % (code, e))

    for code, row in (res.get("lng") or {}).items():
        try:
            metrics["lng"][code] = {"value": round(num(row, "full"), 1)}
        except Exception as e:
            errors.append("lng/%s: %s" % (code, e))

    # Report des valeurs precedentes quand la collecte du jour a echoue :
    # mieux vaut une donnee datee qu'une carte vide. L'age est trace.
    path = os.path.join(ROOT, "data", "prices.json")
    carried = 0
    try:
        with open(path, encoding="utf-8") as f:
            old = json.load(f)
        old_day = old.get("day")
        for key, values in (old.get("metrics") or {}).items():
            for code, val in values.items():
                if code in metrics.get(key, {}):
                    continue
                keep = dict(val)
                keep["asof"] = val.get("asof") or old_day
                keep["stale"] = True
                metrics.setdefault(key, {})[code] = keep
                carried += 1
    except Exception:
        pass

    out = {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "day": day.isoformat(),
        "metrics": metrics,
        "carried": carried,
        "errors": errors,
    }

    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print("\n--- Resultat ---", flush=True)
    for k, v in metrics.items():
        fresh = sum(1 for x in v.values() if not x.get("stale"))
        print("  %-8s %3d valeurs (%d du jour, %d reportees)"
              % (k, len(v), fresh, len(v) - fresh))
    print("  duree     %ds" % int(MAX_SECONDS - max(0, left())))
    if errors:
        print("\n--- %d erreurs ---" % len(errors))
        for e in errors:
            print("  !", e)
    return 0


if __name__ == "__main__":
    sys.exit(main())
