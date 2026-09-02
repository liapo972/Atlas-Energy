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

HTTP_TIMEOUT = 20
WORKERS = 8
MAX_SECONDS = int(os.environ.get("MAX_SECONDS", "420"))
DEADLINE = time.time() + MAX_SECONDS


class Expired(Exception):
    pass


def left():
    return DEADLINE - time.time()


def http_get(url, headers=None):
    """Un seul essai, plus un second uniquement si le temps le permet."""
    for attempt in (0, 1):
        if left() < 5:
            raise Expired("butoir atteint")
        try:
            req = urllib.request.Request(url, headers=headers or {})
            with urllib.request.urlopen(req, timeout=min(HTTP_TIMEOUT, max(5, left()))) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and attempt == 0 and left() > 20:
                time.sleep(2)
                continue
            raise
        except Exception:
            if attempt == 0 and left() > 20:
                continue
            raise
    raise RuntimeError("echec")


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


def gie(base, country, day):
    q = urllib.parse.urlencode({"country": country, "from": day.isoformat(),
                                "to": day.isoformat(), "size": 10})
    raw = http_get(base + "?" + q, headers={"x-key": GIE_KEY})
    rows = (json.loads(raw) or {}).get("data") or []
    if not rows:
        raise RuntimeError("aucune donnee")
    return rows[0]


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


def main():
    day = date.today() - timedelta(days=1)
    metrics = {k: {} for k in ("price", "load", "storage", "netwd", "lng")}
    errors = []

    print("Journee visee :", day.isoformat(), flush=True)
    print("Butoir global :", MAX_SECONDS, "secondes", flush=True)

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

    out = {
        "generated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "day": day.isoformat(),
        "metrics": metrics,
        "errors": errors,
    }

    path = os.path.join(ROOT, "data", "prices.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print("\n--- Resultat ---", flush=True)
    for k, v in metrics.items():
        print("  %-8s %3d valeurs" % (k, len(v)))
    print("  duree     %ds" % int(MAX_SECONDS - max(0, left())))
    if errors:
        print("\n--- %d erreurs ---" % len(errors))
        for e in errors:
            print("  !", e)
    return 0


if __name__ == "__main__":
    sys.exit(main())
