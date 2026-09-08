#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Teste tous les liens sortants de la carte et ecrit data/link_status.txt.

Les URL des fiches pays ont ete ecrites a la main : elles vieillissent, les
sites se reorganisent, les pages disparaissent. Plutot que de decouvrir les
liens morts un par un en cliquant, ce script les teste tous et sort un
rapport trie, a lancer depuis l'onglet Actions quand le besoin s'en fait
sentir.

Usage : python3 check_links.py
"""

import os
import sys
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "src"))

from countries_a import A
from countries_b import B
from countries_c import C

COUNTRIES = {}
COUNTRIES.update(A)
COUNTRIES.update(B)
COUNTRIES.update(C)

# Liens communs, affiches sur chaque fiche pays.
FIXED = [
    ("*", "EEX — Market Data Hub", "https://www.eex.com/en/market-data/market-data-hub"),
    ("*", "ENTSO-E Transparency", "https://transparency.entsoe.eu/"),
    ("*", "GIE AGSI+", "https://agsi.gie.eu/"),
    ("*", "GIE ALSI", "https://alsi.gie.eu/"),
]

UA = "AtlasEnergy-linkcheck/1.0 (+https://github.com/liapo972/Atlas-Energy)"
TIMEOUT = 20
WORKERS = 6


def probe(url):
    """HEAD d'abord ; certains sites le refusent, on retombe sur un GET."""
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers={
                "User-Agent": UA,
                "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
                "Accept-Language": "en,fr;q=0.9",
            })
            with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
                return r.status, r.geturl()
        except urllib.error.HTTPError as e:
            if method == "HEAD" and e.code in (403, 405, 501):
                continue
            return e.code, None
        except Exception as e:
            if method == "HEAD":
                continue
            return None, type(e).__name__
    return None, "echec"


def main():
    targets = []
    for code, meta in sorted(COUNTRIES.items()):
        for label, url, _note in meta.get("tso", []):
            targets.append((code, label, url))
    targets.extend(FIXED)

    print("Test de %d liens\n" % len(targets), flush=True)

    def one(t):
        code, label, url = t
        status, extra = probe(url)
        return code, label, url, status, extra

    ok, redir, dead = [], [], []
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        for code, label, url, status, extra in pool.map(one, targets):
            line = "%-3s %-34s %s" % (code, label[:34], url)
            if status and 200 <= status < 300:
                if extra and extra.rstrip("/") != url.rstrip("/"):
                    redir.append(line + "\n        -> redirige vers " + extra)
                else:
                    ok.append(line)
            elif status:
                dead.append("[%s] %s" % (status, line))
            else:
                dead.append("[%s] %s" % (extra, line))

    out = []
    out.append("%d liens testes : %d OK, %d redirections, %d a corriger"
               % (len(targets), len(ok), len(redir), len(dead)))
    if dead:
        out.append("\n=== A CORRIGER ===")
        out.extend(sorted(dead))
    if redir:
        out.append("\n=== REDIRECTIONS (a figer sur la cible) ===")
        out.extend(sorted(redir))
    out.append("\n=== OK ===")
    out.extend(sorted(ok))

    report = "\n".join(out)
    print(report)
    path = os.path.join(ROOT, "data", "link_status.txt")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(report + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
