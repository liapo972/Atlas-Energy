#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Recupere les donnees ouvertes et ecrit data/prices.json.

Couche electricite (ENTSO-E Transparency Platform)
  price   documentType A44  prix day-ahead, moyenne baseload      EUR/MWh
  load    documentType A65  consommation realisee, energie du jour GWh

Couche gaz (GIE)
  storage AGSI+  taux de remplissage des stockages                %
  netwd   AGSI+  soutirage net de la journee (negatif = injection) GWh
  lng     ALSI   taux de remplissage des terminaux GNL             %

Aucune donnee sous licence commerciale n'est collectee ici.

Variables d'environnement :
  ENTSOE_TOKEN  obligatoire pour la couche electricite
  GIE_KEY       obligatoire pour la couche gaz (vaut pour AGSI+ et ALSI)
                AGSI_KEY est accepte comme alias historique
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET
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

# Pays disposant de terminaux GNL suivis par ALSI.
ALSI_COUNTRIES = {"BE", "DE", "ES", "FI", "FR", "GB", "GR", "HR",
                  "IT", "LT", "NL", "PL", "PT", "SE"}

TOKEN = os.environ.get("ENTSOE_TOKEN", "").strip()
GIE_KEY = (os.environ.get("GIE_KEY") or os.environ.get("AGSI_KEY") or "").strip()


def http_get(url, headers=None, retries=3):
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=headers or {})
            with urllib.request.urlopen(req, timeout=45) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and attempt < retries - 1:
                time.sleep(3 * (attempt + 1))
                continue
            raise
        except Exception:
            if attempt < retries - 1:
                time.sleep(3 * (attempt + 1))
                continue
            raise


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
        raise RuntimeError(reason.strip() or "pas de donnees")
    return root


def window(day):
    return (day.strftime("%Y%m%d") + "0000",
            (day + timedelta(days=1)).strftime("%Y%m%d") + "0000")


def fetch_price(eic, day):
    """Moyenne baseload des prix day-ahead."""
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
    """Energie consommee sur la journee, a partir de la puissance moyenne."""
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
    mean_mw = sum(vals) / len(vals)
    return {"value": round(mean_mw * 24 / 1000.0, 1)}


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


def main():
    day = date.today() - timedelta(days=1)
    metrics = {k: {} for k in ("price", "load", "storage", "netwd", "lng")}
    errors = []

    if TOKEN:
        for code, meta in COUNTRIES.items():
            eic = meta.get("eic")
            if not eic:
                continue
            for key, fn in (("price", fetch_price), ("load", fetch_load)):
                try:
                    metrics[key][code] = fn(eic, day)
                except Exception as exc:
                    errors.append("%s/%s: %s" % (key, code, exc))
                time.sleep(0.4)
    else:
        errors.append("electricite: ENTSOE_TOKEN absent, couche non mise a jour")

    if GIE_KEY:
        for code, meta in COUNTRIES.items():
            ag = meta.get("agsi")
            if ag:
                try:
                    row = gie(AGSI_URL, ag, day)
                    metrics["storage"][code] = {"value": round(num(row, "full"), 1)}
                    try:
                        metrics["netwd"][code] = {
                            "value": round(num(row, "netWithdrawal"), 1)}
                    except Exception as exc:
                        errors.append("netwd/%s: %s" % (code, exc))
                except Exception as exc:
                    errors.append("storage/%s: %s" % (code, exc))
                time.sleep(0.4)
            if code in ALSI_COUNTRIES:
                try:
                    row = gie(ALSI_URL, code, day)
                    metrics["lng"][code] = {"value": round(num(row, "full"), 1)}
                except Exception as exc:
                    errors.append("lng/%s: %s" % (code, exc))
                time.sleep(0.4)
    else:
        errors.append("gaz: GIE_KEY absent, couche non mise a jour")

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

    print("jour :", out["day"])
    for k, v in metrics.items():
        print("  %-8s %3d valeurs" % (k, len(v)))
    for e in errors:
        print("  !", e)
    return 0


if __name__ == "__main__":
    sys.exit(main())
