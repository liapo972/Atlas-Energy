#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble index.html a partir des fragments de src/ et des metadonnees pays."""

import os
import sys
import json
import random

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "src")
sys.path.insert(0, SRC)

from countries_a import A
from countries_b import B
from countries_c import C

COUNTRIES = {}
COUNTRIES.update(A)
COUNTRIES.update(B)
COUNTRIES.update(C)

HEAD_PARTS = ["p1.html", "p2.html", "p3.html", "p4.html", "p5.html", "p6.html", "p7.html"]
BODY_PARTS = ["t_body.html", "t_js.html", "t_demo_news.html", "t_js2.html"]


ALSI_COUNTRIES = {"BE", "DE", "ES", "FI", "FR", "GB", "GR", "HR",
                  "IT", "LT", "NL", "PL", "PT", "SE"}


def demo_values():
    """Valeurs de repli, clairement identifiees comme fictives dans l'interface."""
    rnd = random.Random(20260901)
    out = {}
    for code, m in COUNTRIES.items():
        d = {
            "price": round(rnd.uniform(55, 130), 1),
            "load": round(rnd.uniform(35, 1450), 1),
        }
        if m.get("agsi"):
            d["storage"] = round(rnd.uniform(41, 82), 1)
            d["netwd"] = round(rnd.uniform(-260, 190), 1)
        if code in ALSI_COUNTRIES:
            d["lng"] = round(rnd.uniform(28, 79), 1)
        out[code] = d
    return out


def main():
    geo = json.load(open(os.path.join(ROOT, "data", "paths.json"), encoding="utf-8"))

    def read(parts):
        return "\n".join(
            open(os.path.join(SRC, p), encoding="utf-8").read() for p in parts
        )

    head = read(HEAD_PARTS)
    body = read(BODY_PARTS)

    html = (
        "<!doctype html>\n"
        '<html lang="fr">\n'
        "<head>\n"
        '<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
        '<meta name="description" content="Carte interactive des marches europeens '
        'de l\'electricite et du gaz, construite sur donnees ouvertes.">\n'
        "<style>html,body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n"
        + head +
        "\n</head>\n<body>\n"
        + body +
        "\n</body>\n</html>\n"
    )
    html = html.replace("__W__", str(geo["w"])).replace("__H__", str(geo["h"]))
    html = html.replace("__PATHS__", json.dumps(geo["paths"]))
    html = html.replace("__COUNTRIES__", json.dumps(COUNTRIES, ensure_ascii=False))
    html = html.replace("__DEMO__", json.dumps(demo_values()))

    left = [t for t in ("__W__", "__H__", "__PATHS__", "__COUNTRIES__", "__DEMO__")
            if t in html]
    if left:
        raise SystemExit("placeholders non remplaces: %s" % left)

    path = os.path.join(ROOT, "index.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

    print("index.html ecrit :", len(html), "octets")
    print("pays             :", len(COUNTRIES))
    return 0


if __name__ == "__main__":
    sys.exit(main())
