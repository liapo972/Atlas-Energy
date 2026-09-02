#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Agrege des titres d'actualite et ecrit data/news.json.

Regle de droit respectee ici : on ne conserve que le TITRE, la SOURCE,
l'HORODATAGE et le LIEN vers l'article original. Jamais le corps du texte.
C'est l'usage pour lequel les editeurs publient des flux RSS.

Sources :
  - flux RSS/Atom cures (src/feeds.py)
  - GDELT DOC 2.0 (gratuit, sans cle) pour le fil monde et en socle par pays

Usage :
  python3 fetch_news.py            recupere et ecrit data/news.json
  python3 fetch_news.py --check    teste chaque flux et affiche un rapport
"""

import os
import re
import sys
import json
import time
import html
import urllib.request
import urllib.error
import urllib.parse
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone, timedelta

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "src"))

from feeds import FEEDS, GDELT_WORLD, GDELT_COUNTRY_TERMS, KEYWORDS
from countries_a import A
from countries_b import B
from countries_c import C

COUNTRIES = {}
COUNTRIES.update(A)
COUNTRIES.update(B)
COUNTRIES.update(C)

GDELT = "https://api.gdeltproject.org/api/v2/doc/doc"
UA = "atlas-marches-europe/1.0 (+github pages; contact via repo)"

MAX_PER_COUNTRY = 8
MAX_WORLD = 25
MAX_AGE_DAYS = 10


def http_get(url, retries=2, timeout=30):
    last = None
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": UA,
                "Accept": "application/rss+xml, application/atom+xml, application/xml, application/json;q=0.9, */*;q=0.8",
            })
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except Exception as exc:
            last = exc
            if attempt < retries:
                time.sleep(2 * (attempt + 1))
    raise last


def strip_ns(tag):
    return tag.split("}")[-1] if "}" in tag else tag


def clean(text):
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def parse_date(raw):
    if not raw:
        return None
    raw = raw.strip()
    try:
        d = parsedate_to_datetime(raw)
        if d.tzinfo is None:
            d = d.replace(tzinfo=timezone.utc)
        return d.astimezone(timezone.utc)
    except Exception:
        pass
    try:
        d = datetime.fromisoformat(raw.replace("Z", "+00:00"))
        if d.tzinfo is None:
            d = d.replace(tzinfo=timezone.utc)
        return d.astimezone(timezone.utc)
    except Exception:
        return None


def parse_feed(raw):
    """Retourne [(titre, lien, date)] pour RSS 2.0 comme pour Atom."""
    root = ET.fromstring(raw)
    items = []

    for el in root.iter():
        tag = strip_ns(el.tag)
        if tag not in ("item", "entry"):
            continue
        title = link = date = None
        for c in el:
            ct = strip_ns(c.tag)
            if ct == "title" and title is None:
                title = clean(c.text or "".join(c.itertext()))
            elif ct == "link":
                if c.text and c.text.strip():
                    link = c.text.strip()
                elif c.get("href") and c.get("rel", "alternate") == "alternate":
                    link = c.get("href")
            elif ct in ("pubDate", "published", "updated", "date") and date is None:
                date = parse_date(c.text)
        if title and link:
            items.append((title, link, date))
    return items


def gdelt(query, maxrecords=40, timespan="3d"):
    q = urllib.parse.urlencode({
        "query": query, "mode": "artlist", "format": "json",
        "maxrecords": maxrecords, "timespan": timespan, "sort": "datedesc",
    })
    raw = http_get(GDELT + "?" + q)
    try:
        payload = json.loads(raw.decode("utf-8", "replace"))
    except Exception:
        return []
    out = []
    for a in payload.get("articles") or []:
        title = clean(a.get("title"))
        url = a.get("url")
        if not title or not url:
            continue
        d = None
        seen = a.get("seendate") or ""
        try:
            d = datetime.strptime(seen, "%Y%m%dT%H%M%SZ").replace(tzinfo=timezone.utc)
        except Exception:
            pass
        out.append((title, url, d, a.get("domain") or "GDELT"))
    return out


def tag_countries(title, source_country):
    if source_country:
        return [source_country]
    hits = []
    low = title.lower()
    for code, words in KEYWORDS.items():
        for w in words:
            if w.lower() in low:
                hits.append(code)
                break
    return hits


def check_mode():
    print("Test des flux — %d sources\n" % len(FEEDS))
    ok = bad = 0
    for f in FEEDS:
        try:
            raw = http_get(f["url"], retries=0, timeout=20)
            items = parse_feed(raw)
            if items:
                print("  OK   %-28s %3d entrées" % (f["name"], len(items)))
                ok += 1
            else:
                print("  VIDE %-28s (répond mais aucune entrée exploitable)" % f["name"])
                bad += 1
        except Exception as exc:
            print("  MORT %-28s %s" % (f["name"], type(exc).__name__))
            bad += 1
    print("\n%d flux exploitables, %d à corriger ou retirer dans src/feeds.py" % (ok, bad))
    return 0 if ok else 1


def main():
    if "--check" in sys.argv:
        return check_mode()

    now = datetime.now(timezone.utc)
    floor = now - timedelta(days=MAX_AGE_DAYS)
    seen_links = set()
    items = []
    errors = []

    def add(title, link, date, source, theme, countries):
        if not link or link in seen_links:
            return
        if date and date < floor:
            return
        seen_links.add(link)
        items.append({
            "title": title[:240],
            "url": link,
            "source": source,
            "theme": theme,
            "date": (date or now).isoformat(timespec="seconds"),
            "countries": countries,
        })

    # 1. flux RSS/Atom cures
    for f in FEEDS:
        try:
            raw = http_get(f["url"])
            got = parse_feed(raw)
            if not got:
                errors.append("%s: repond mais aucune entree" % f["name"])
                continue
            for title, link, date in got[:15]:
                add(title, link, date, f["name"], f["theme"],
                    tag_countries(title, f.get("country")))
        except Exception as exc:
            errors.append("%s: %s" % (f["name"], type(exc).__name__))
        time.sleep(0.3)

    # 2. socle GDELT par pays
    for code, meta in COUNTRIES.items():
        name = meta["name"]["en"]
        query = '"%s" %s sourcelang:english' % (name, GDELT_COUNTRY_TERMS)
        try:
            for title, link, date, domain in gdelt(query, maxrecords=10):
                add(title, link, date, domain, "press", [code])
        except Exception as exc:
            errors.append("gdelt/%s: %s" % (code, type(exc).__name__))
        time.sleep(0.6)

    # 3. fil monde
    world = []
    try:
        for title, link, date, domain in gdelt(GDELT_WORLD, maxrecords=60):
            if link in seen_links:
                continue
            seen_links.add(link)
            world.append({
                "title": title[:240], "url": link, "source": domain,
                "theme": "press",
                "date": (date or now).isoformat(timespec="seconds"),
            })
    except Exception as exc:
        errors.append("gdelt/world: %s" % type(exc).__name__)

    # les communiques d'institutions et de banques centrales ouvrent le fil monde
    prio = [i for i in items if i["theme"] in ("policy", "grid") and not i["countries"]]
    prio.sort(key=lambda x: x["date"], reverse=True)
    world = prio[:8] + world
    world.sort(key=lambda x: x["date"], reverse=True)
    world = world[:MAX_WORLD]

    by_country = {}
    for it in items:
        for c in it["countries"]:
            by_country.setdefault(c, []).append(it)
    for c in by_country:
        by_country[c].sort(key=lambda x: x["date"], reverse=True)
        by_country[c] = by_country[c][:MAX_PER_COUNTRY]

    out = {
        "generated": now.isoformat(timespec="seconds"),
        "world": world,
        "countries": by_country,
        "errors": errors,
    }

    path = os.path.join(ROOT, "data", "news.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print("fil monde   :", len(world), "titres")
    print("pays servis :", len(by_country), "/", len(COUNTRIES))
    for e in errors:
        print("  !", e)
    return 0


if __name__ == "__main__":
    sys.exit(main())
