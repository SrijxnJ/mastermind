"""Pick the final SFX per category from the earshot-judged pools. Writes selection.json + prints a table.
Usage: python3 -I select.py OUT_JSON judged1.json [judged2.json ...]   (later files' in-house entries replace earlier)"""
import json, os, re, sys

OUT = sys.argv[1]
merged = {}
for f in sys.argv[2:]:
    d = json.load(open(f))
    for cat, items in d.items():
        cur = merged.setdefault(cat, [])
        names = {os.path.basename(x["rel"]) for x in items if x["rel"].startswith("inhouse/")}
        cur[:] = [x for x in cur if not (x["rel"].startswith("inhouse/") and os.path.basename(x["rel"]) in names)]
        cur.extend(items)
# the first pass judged in-house sounds rendered with a comb-filtering stereo widener: drop those, keep the mono re-render
N = {"gaming": 6, "gym": 6, "click-ui": 5, "pop": 5, "keyboard": 4, "typing": 4, "hit-impact": 6, "whoosh": 6,
     "swoosh-fast": 5, "notification-ding": 5, "chime-success": 5, "bass-drop-boom": 5, "riser": 4, "downlifter": 4,
     "glitch": 4, "camera-shutter": 3, "record-scratch": 3, "rewind-tape-stop": 3, "crowd-cheer-applause": 3,
     "cash-register": 4, "heartbeat": 3, "meme-cc0": 3}
HARD = {"clipping", "clicks", "silent"}
# categories where the CLAP vocabulary has no good word: accept lower verdicts (documented in the catalog)
LENIENT = {"rewind-tape-stop", "cash-register", "glitch", "notification-ding", "gym", "crowd-cheer-applause"}
EXCLUDE = re.compile(r"kenney_interface-sounds/Audio/glitch_00|chalkclap_inhouse|shutter_inhouse_(dslr|mirrorless|film)|scratch_inhouse_(stop|double)|"
                     r"rewind_inhouse_fast|tapestop_inhouse_8bit|register_inhouse_bell_drawer|crowd_shouting")


def key(it):
    rel = it["rel"]
    if rel.startswith("uisfx/"):
        return "uisfx:" + os.path.basename(rel)
    if rel.startswith("kenney_"):
        return re.sub(r"[_-]?\d+\.\w+$", "", rel)
    if rel.startswith("inhouse/"):
        return rel
    return it["source_url"]


sel = []
for cat, items in merged.items():
    items = sorted(items, key=lambda s: -(s.get("z") or -99))
    ok = []
    for s in items:
        if EXCLUDE.search(s["rel"]):
            continue
        hard = HARD - ({"clicks"} if cat in ("glitch", "heartbeat") else set())  # clicks are the design of a glitch
        if set(s.get("check_codes") or []) & hard or s.get("src_clip_runs", 0) > 2:
            continue
        v = s.get("verdict")
        if v == "no match" and cat not in LENIENT:
            continue
        if v in ("weak", "no match") and cat not in LENIENT and len(ok) >= 3:
            continue
        ok.append(s)
    picked, per = [], {}
    if cat == "gaming":  # coins, power-ups and level-up jingles, two each
        groups = [r"power_up", r"coin\d", r"jingles_NES0[05]"]
        for g in groups:
            picked += [s for s in ok if re.search(g, s["rel"])][:2]
    elif cat == "gym":  # make sure each gym sub-type is present
        groups = [r"metal_falling", r"clink|impactMetal_heavy|bing|bong|thud"]
        for g in groups:
            for s in ok:
                if re.search(g, s["rel"]) and s not in picked and sum(bool(re.search(g, p["rel"])) for p in picked) < 3:
                    picked.append(s)
        picked = picked[:N[cat]]
    else:
        for s in ok:
            k = key(s)
            cap = 3 if cat in ("keyboard", "heartbeat", "crowd-cheer-applause") else 2
            if per.get(k, 0) >= cap:
                continue
            per[k] = per.get(k, 0) + 1
            picked.append(s)
            if len(picked) >= N.get(cat, 4):
                break
    for i, s in enumerate(picked, 1):
        s["category"] = cat
        s["file"] = f"{cat}_{i:02d}.mp3"
        sel.append(s)
    print(f"== {cat}: {len(picked)} of {len(items)}")
    for s in picked:
        print(f"   {s['file']:28} z{str(s.get('z')):>5} {str(s.get('verdict'))[:6]:6} {s['staged_dur_s']:>6}s {','.join(s.get('check_codes') or [])[:20]:20} {s['rel'][-55:]}")
json.dump(sel, open(OUT, "w"), indent=1)
print(len(sel), "selected")
