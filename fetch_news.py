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
from concurrent.futures import ThreadPoolExecutor
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

WORKERS = 8
HTTP_TIMEOUT = 15
MAX_SECONDS = int(os.environ.get("MAX_SECONDS", "420"))
DEADLINE = time.time() + MAX_SECONDS


class Expired(Exception):
    pass


def left():
    return DEADLINE - time.time()


def http_get(url, retries=1, timeout=None):
    timeout = timeout or HTTP_TIMEOUT
    last = None
    for attempt in range(retries + 1):
        if left() < 5:
            raise Expired("butoir atteint")
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": UA,
                "Accept": "application/rss+xml, application/atom+xml, application/xml, application/json;q=0.9, */*;q=0.8",
            })
            with urllib.request.urlopen(req, timeout=min(timeout, max(5, left()))) as r:
                return r.read()
        except Exception as exc:
            last = exc
            if attempt >= retries or left() < 20:
                break
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


HREF_RE = re.compile(r'''href=["\']([^"\']+)["\']''')
URL_RE = re.compile(r"https?://[^\s\"'<>]+")


def sanitize_link(raw, base):
    """Remet d'aplomb un lien de flux RSS.

    Certains flux publient n'importe quoi dans <link> : ACER y met carrement
    un fragment de HTML (<a href="/news/...">), d'autres publient un chemin
    relatif. On extrait l'URL reelle puis on la resout contre l'adresse du
    flux, et on ecrase les doubles barres qui trainent (la BCE en produit)."""
    if not raw:
        return None
    raw = html.unescape(raw.strip())

    if "href=" in raw:
        m = HREF_RE.search(raw)
        if m:
            raw = m.group(1)
    elif not raw.startswith(("http://", "https://")):
        m = URL_RE.search(raw)
        if m:
            raw = m.group(0)

    raw = raw.strip().strip('"\'<>')
    if not raw:
        return None

    url = urllib.parse.urljoin(base, raw)
    parts = urllib.parse.urlsplit(url)
    if parts.scheme not in ("http", "https") or not parts.netloc:
        return None
    path = re.sub(r"/{2,}", "/", parts.path)
    return urllib.parse.urlunsplit(
        (parts.scheme, parts.netloc, path, parts.query, parts.fragment))


def parse_feed(raw, base=""):
    """Retourne [(titre, lien, date)] pour RSS 2.0 comme pour Atom."""
    root = ET.fromstring(raw)
    items = []

    for el in root.iter():
        tag = strip_ns(el.tag)
        if tag not in ("item", "entry"):
            continue
        title = link = guid = date = None
        for c in el:
            ct = strip_ns(c.tag)
            if ct == "title" and title is None:
                title = clean(c.text or "".join(c.itertext()))
            elif ct == "link":
                if c.get("href") and c.get("rel", "alternate") == "alternate":
                    link = link or c.get("href")
                elif c.text and c.text.strip():
                    link = link or c.text
            elif ct == "guid" and c.text:
                guid = c.text
            elif ct in ("pubDate", "published", "updated", "date") and date is None:
                date = parse_date(c.text)

        url = sanitize_link(link, base) or sanitize_link(guid, base)
        if title and url:
            items.append((title, url, date))
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
            raw = http_get(f["urls"][0], retries=0)
            items = parse_feed(raw, f["urls"][0])
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
    sys.stdout = _Tee(os.path.join(ROOT, "data", "last_run_news.txt"))
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

    # 1. flux RSS/Atom cures, en parallele.
    #    Chaque source propose plusieurs URL candidates : on garde la premiere
    #    qui repond ET se parse. Le resultat est journalise pour pouvoir
    #    figer la bonne URL dans src/feeds.py.
    feed_status = {}

    def do_feed(f):
        tried = []
        for url in f["urls"]:
            try:
                got = parse_feed(http_get(url), url)
                if got:
                    return f, got, None, url
                tried.append("%s -> vide" % url)
            except Exception as exc:
                tried.append("%s -> %s" % (url, type(exc).__name__))
        return f, None, " | ".join(tried), None

    print("Flux RSS :", len(FEEDS), "sources", flush=True)
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        for f, got, err, url in pool.map(do_feed, FEEDS):
            if got:
                feed_status[f["name"]] = {"ok": True, "url": url, "items": len(got)}
                print("  OK   %-24s %s" % (f["name"], url), flush=True)
                for title, link, date in got[:15]:
                    add(title, link, date, f["name"], f["theme"],
                        tag_countries(title, f.get("country")))
            else:
                feed_status[f["name"]] = {"ok": False, "tried": err}
                errors.append("%s: %s" % (f["name"], err))
                print("  MORT %-24s %s" % (f["name"], err), flush=True)

    # 2. socle GDELT par pays, en parallele
    def do_country(item):
        code, meta = item
        query = '"%s" %s sourcelang:english' % (meta["name"]["en"], GDELT_COUNTRY_TERMS)
        try:
            return code, gdelt(query, maxrecords=10), None
        except Exception as exc:
            return code, None, "gdelt/%s: %s" % (code, type(exc).__name__)

    print("Requetes GDELT pays :", len(COUNTRIES), flush=True)
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        for code, rows, err in pool.map(do_country, list(COUNTRIES.items())):
            if err:
                errors.append(err)
                continue
            for title, link, date, domain in rows:
                add(title, link, date, domain, "press", [code])

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
        "feed_status": feed_status,
        "errors": errors,
    }

    path = os.path.join(ROOT, "data", "news.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)

    print("\n--- Resultat ---")
    print("  fil monde   :", len(world), "titres")
    print("  pays servis :", len(by_country), "/", len(COUNTRIES))
    print("  duree       : %ds" % int(MAX_SECONDS - max(0, left())))
    if errors:
        print("\n--- %d avertissements ---" % len(errors))
        for e in errors:
            print("  !", e)
    return 0


if __name__ == "__main__":
    sys.exit(main())
