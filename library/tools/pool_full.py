"""Full CC0 pool: every Kenney pack file + every CC0-only OpenGameArt file, one category each.
Usage: python3 -I pool_full.py DL_LIB OUT_JSON"""
import json, os, re, sys

DL, OUT = sys.argv[1:3]
oga = json.load(open(os.path.join(DL, "oga", "oga_items.json")))
AUD = (".wav", ".ogg", ".mp3", ".flac", ".aif", ".aiff", ".oga")
CAP = 30  # processed files per OpenGameArt item (the rest stays in raw/)
SKIP_ITEMS = re.compile(r"glitch-music|ringtone|music|song|theme|loop-pack|soundtrack", re.I)


def kenney_cat(pack, name):
    n = name.lower()
    if pack.startswith("voiceover"):
        return "voice-announcer"
    if pack == "music-jingles":
        return "gaming" if "nes" in n else "jingles"
    if pack == "impact-sounds":
        if n.startswith("footstep"):
            return "foley-footsteps"
        if "impactmetal" in n:
            return "gym"
        return "hit-impact"
    if pack == "interface-sounds":
        if re.match(r"(click|select|tick|switch|toggle|scroll|pluck)", n):
            return "click-ui"
        if re.match(r"(confirmation|bong|question|glass)", n):
            return "notification-ding"
        if n.startswith("error"):
            return "ui-error"
        if n.startswith("glitch"):
            return "glitch"
        return "ui-open-close"
    if pack == "ui-audio":
        return "click-ui"
    if pack == "digital-audio":
        if re.match(r"(laser|phaser|zap1|zap2|spacetrash)", n):
            return "sci-fi"
        if re.match(r"(highdown|lowdown)", n):
            return "downlifter"
        return "gaming"
    if pack == "rpg-audio":
        if n.startswith("handlecoins"):
            return "cash-register"
        if n.startswith("footstep"):
            return "foley-footsteps"
        return "foley"
    if pack == "sci-fi-sounds":
        if re.match(r"(lowfrequency_explosion|explosioncrunch)", n):
            return "bass-drop-boom"
        if n.startswith("computernoise"):
            return "glitch"
        return "sci-fi"
    if pack == "casino-audio":
        return "cash-register" if n.startswith("chip") else "foley-cards-dice"
    return "misc"


RULES = [  # applied to "<item slug> <file name>" for OpenGameArt files
    ("voice-announcer", r"voice|announcer|game-voice"),
    ("camera-shutter", r"camera|photo|shutter"),
    ("record-scratch", r"scratch|vinyl"),
    ("heartbeat", r"heart"),
    ("crowd-cheer-applause", r"applause|crowd|cheer|clap|well-done|oooo"),
    ("typing", r"typing|typewriter|generated-0"),
    ("keyboard", r"keypress|keyboard"),
    ("gaming", r"8bit|8-bit|retro|nes-sounds|chip|power.?up|level|coin\d|pickup|jump|blip|bleep|new-thing|round_end|death\.wav|win-and-die|ping-pong"),
    ("cash-register", r"coin|gold|money|purchas|cash|sack"),
    ("pop", r"pop|bubble|balloon"),
    ("click-ui", r"click|button|switch|hover|select|menu|interface|gui|ui-|ui_|beep"),
    ("swoosh-fast", r"swish|sword|melee|swing"),
    ("whoosh", r"whoosh|woosh|swoosh|erase"),
    ("riser", r"rise\d|upper|riser"),
    ("downlifter", r"downer"),
    ("glitch", r"glitch|static|computer"),
    ("bass-drop-boom", r"explos|boom|blast|bomb"),
    ("gym", r"metal_falling|metal-impact|clink|clang|anvil"),
    ("hit-impact", r"hit|punch|impact|thud|thwack|smack|slap|break|falling|crash|wood|stone"),
    ("notification-ding", r"bell|ding|chime|notif|alert|kalimba"),
    ("chime-success", r"success|victory|fanfare|jingle|magic|heal|spell"),
    ("sci-fi", r"laser|sci|space|engine|zap|phaser|electric|shot"),
    ("foley-footsteps", r"foot|step"),
    ("foley", r"door|cloth|book|glass|water|splash|fire|creak|squish|lock|item|misc|wind|slime|creature"),
]

pool = {}
seen = set()
for top in sorted(os.listdir(DL)):
    p = os.path.join(DL, top)
    if top.startswith("kenney_") and os.path.isdir(p):
        pack = top[len("kenney_"):]
        for root, _, fs in os.walk(p):
            for f in sorted(fs):
                if not f.lower().endswith(AUD) or f.startswith("Preview") or f.startswith("._"):
                    continue
                full = os.path.join(root, f)
                cat = kenney_cat(pack, f)
                pool.setdefault(cat, []).append({
                    "rel": os.path.relpath(full, DL), "path": full, "licence": "CC0-1.0", "author": "Kenney (www.kenney.nl)",
                    "source_url": f"https://kenney.nl/assets/{pack}", "source_title": f"Kenney {pack.replace('-', ' ').title()} pack",
                    "pack": "kenney/" + pack})
items_dir = os.path.join(DL, "oga", "items")
for slug in sorted(os.listdir(items_dir)):
    it = oga.get(slug)
    if not it or not it["licenses"] or not all(l.strip() == "CC0" for l in it["licenses"]):
        continue
    if SKIP_ITEMS.search(slug) or (it.get("author") or "").lower() == "kenney":
        continue  # Kenney re-uploads on OGA duplicate the kenney.nl originals we already have
    files = []
    for root, _, fs in os.walk(os.path.join(items_dir, slug)):
        if "__MACOSX" in root:
            continue
        for f in fs:
            if f.lower().endswith(AUD) and not f.startswith("._"):
                files.append(os.path.join(root, f))
    # prefer one format per base name (wav > flac > ogg > mp3)
    best = {}
    rank = {".wav": 0, ".flac": 1, ".aif": 1, ".aiff": 1, ".ogg": 2, ".oga": 2, ".mp3": 3}
    for f in files:
        b, e = os.path.splitext(os.path.basename(f))
        k = (os.path.dirname(f).replace("/Vorbis", "").replace("/PCM", "").replace("/OGG", "").replace("/WAV", ""), b.lower())
        if k not in best or rank[e.lower()] < rank[os.path.splitext(best[k])[1].lower()]:
            best[k] = f
    taken = 0
    for f in sorted(best.values()):
        key = (slug + " " + os.path.basename(f)).lower()
        cat = next((c for c, rx in RULES if re.search(rx, key)), "misc")
        if cat == "misc" or taken >= CAP:
            continue  # unsorted or beyond the per-item cap: kept in library/raw/opengameart only
        taken += 1
        pool.setdefault(cat, []).append({
            "rel": os.path.relpath(f, DL), "path": f, "licence": "CC0-1.0", "author": it["author"],
            "source_url": it["url"], "source_title": it["title"], "pack": "opengameart/" + slug})
for c in sorted(pool):
    print(c, len(pool[c]), file=sys.stderr)
print("total", sum(len(v) for v in pool.values()), file=sys.stderr)
json.dump(pool, open(OUT, "w"), indent=1)
