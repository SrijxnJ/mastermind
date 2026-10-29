"""OpenGameArt CC0 sound search. Usage: python3 -I oga.py OUTDIR "kw1" "kw2" ...
Writes OUTDIR/oga_items.json (merged) with per-item licence(s), author, files. Only items whose every licence is CC0."""
import json, os, re, subprocess, sys, time, html, urllib.parse

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
DB = os.path.join(OUT, "oga_items.json")
items = json.load(open(DB)) if os.path.exists(DB) else {}


def get(url):
    r = subprocess.run(["curl", "-sS", "-m", "60", "-A", "Mozilla/5.0 srijan-sfx-library", url],
                       capture_output=True, text=True)
    return r.stdout


for kw in sys.argv[2:]:
    q = urllib.parse.urlencode({"keys": kw, "field_art_type_tid[]": "13", "field_art_licenses_tid[]": "4",
                                "sort_by": "count", "sort_order": "DESC", "items_per_page": "24"})
    page = get("https://opengameart.org/art-search-advanced?" + q)
    links = []
    for m in re.finditer(r'<div class="field-item even"><a href="/content/([^"]+)">([^<]+)</a>', page):
        links.append((m.group(1), html.unescape(m.group(2))))
    if not links:
        for m in re.finditer(r'href="/content/([a-z0-9-]+)">([^<]+)</a>', page):
            if m.group(1) not in ("faq",) and "art-challenge" not in m.group(1):
                links.append((m.group(1), html.unescape(m.group(2))))
    print(kw, len(links), file=sys.stderr)
    for slug, title in links[:12]:
        if slug in items:
            items[slug].setdefault("kw", []).append(kw)
            continue
        p = get("https://opengameart.org/content/" + slug)
        lic = re.findall(r"license-name'>([^<]+)<", p)
        files = re.findall(r'href="(https://opengameart.org/sites/default/files/[^"]+\.(?:wav|ogg|mp3|flac|zip))"', p)
        author = re.findall(r'field-name-author-submitter.*?<a href="/users/[^"]+">([^<]+)</a>', p, re.S)
        sub = re.findall(r'<a href="/users/([^"]+)"', p)
        attrib = re.findall(r'field-name-field-art-attribution.*?<div class="field-item even">(.*?)</div>', p, re.S)
        items[slug] = {"slug": slug, "title": title, "url": "https://opengameart.org/content/" + slug,
                       "licenses": lic, "files": sorted(set(files)), "author": author[0] if author else (sub[0] if sub else None),
                       "attribution_note": re.sub("<[^>]+>", "", attrib[0]).strip()[:300] if attrib else "",
                       "kw": [kw]}
        time.sleep(0.5)
    json.dump(items, open(DB, "w"), indent=1)
ok = {k: v for k, v in items.items() if v["licenses"] and all(l.strip() == "CC0" for l in v["licenses"])}
print(len(items), "items,", len(ok), "CC0-only", file=sys.stderr)
for k, v in ok.items():
    print(f"{','.join(v['kw'])}\t{k}\t{v['author']}\t{len(v['files'])} files\t{v['title']}")
