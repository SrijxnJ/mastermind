"""Merge featured picks + the full CC0 pool into one build list with catalog metadata.
Usage: python3 -I assemble.py SELECTION_JSON FULL_JUDGED_JSON OUT_JSON"""
import json, os, re, sys

SEL, FULL, OUT = sys.argv[1:4]

CAT = {  # use_when, pairs_with_transition (ids in transitions.json), niches
 "whoosh": ("Camera moves, whip pans, text/graphics sliding in. Peak the whoosh on the cut.", ["whip-pan", "zoom-in-transition", "object-mask-wipe", "slide-push", "spin", "light-leak"], ["travel", "tech", "gym", "gaming"]),
 "swoosh-fast": ("Fast flicks: captions popping across, UI swipes, quick pans, sword-like gestures.", ["whip-pan", "slide-push", "swipe-up-ui", "split-reveal"], ["tech", "gaming", "gym"]),
 "pop": ("Text, stickers, emojis, icons and lower thirds appearing (one pop per element).", ["swipe-up-ui", "iris-circle", "hand-cover"], ["tech", "travel", "gym", "gaming"]),
 "click-ui": ("Screen recordings, cursor clicks, toggles, menu choices, step counters.", ["swipe-up-ui", "counter-roll", "split-reveal"], ["tech", "gaming"]),
 "keyboard": ("Single key presses on keyboard close-ups, typing captions word by word, 'enter' on a reveal.", ["beat-sync-cut", "counter-roll"], ["tech", "gaming"]),
 "typing": ("Typing beds under keyboard B-roll, hacker/'I'm in' jokes, captions typed letter by letter.", ["j-cut", "l-cut"], ["tech", "gaming"]),
 "hit-impact": ("Zoom punches, text slams, punchlines, hard cuts, landing a jump.", ["zoom-punch", "camera-shake", "smash-cut", "freeze-frame"], ["gym", "gaming", "tech", "travel"]),
 "bass-drop-boom": ("Beat drops, big reveals, before/after, meme 'boom' moments (one per video).", ["zoom-punch", "camera-shake", "jump-through", "text-mask-reveal", "speed-ramp"], ["gym", "gaming", "tech", "travel"]),
 "riser": ("Build tension into a reveal or drop: cut exactly at the riser's end.", ["speed-ramp", "zoom-in-transition", "light-leak", "text-mask-reveal"], ["gym", "travel", "gaming", "tech"]),
 "downlifter": ("Energy falling away after a drop, 'fail' moments, scene endings, GTA-'wasted'-style slow-downs.", ["speed-ramp", "cross-dissolve", "freeze-frame"], ["gaming", "travel", "gym"]),
 "glitch": ("Glitch transitions, error jokes, RGB-split moments, tech/gaming cuts.", ["glitch", "pixelate"], ["tech", "gaming"]),
 "camera-shutter": ("Photo dumps, freeze frames, 'snapshot' stills, flash transitions.", ["photo-dump-shutter", "flash-white", "freeze-frame"], ["travel", "tech", "gym"]),
 "notification-ding": ("Fake notifications, DMs, checklist items, small reminders.", ["swipe-up-ui", "counter-roll"], ["tech", "travel", "gym", "gaming"]),
 "chime-success": ("Wins: PR completed, build boots, task done, checkmark appears.", ["counter-roll", "cross-dissolve", "freeze-frame"], ["gym", "tech", "travel", "gaming"]),
 "record-scratch": ("Freeze-frame 'yep, that's me', stopping the music for a twist.", ["freeze-frame", "smash-cut", "tape-stop-cut"], ["travel", "gym", "general"]),
 "rewind-tape-stop": ("Music stopping for a joke (tape stop) or going back in time (rewind).", ["vhs-rewind", "tape-stop-cut", "smash-cut"], ["general", "tech", "gym", "travel"]),
 "crowd-cheer-applause": ("Celebrating a PR, a win, a finished build (ironic for small wins).", ["freeze-frame", "speed-ramp"], ["gym", "gaming", "general"]),
 "gym": ("Plate and dumbbell clanks, barbell drops: lockout and rerack accents.", ["camera-shake", "zoom-punch", "beat-sync-cut", "speed-ramp"], ["gym"]),
 "gaming": ("Coins, power-ups and level-up jingles for gaming clips, counters and small wins.", ["counter-roll", "pixelate", "freeze-frame"], ["gaming", "tech", "gym"]),
 "cash-register": ("Price reveals, money saved/spent, budget totals.", ["counter-roll", "freeze-frame"], ["tech", "travel", "gym"]),
 "heartbeat": ("Tension before a max attempt, landing, price reveal; speed it up toward the moment.", ["speed-ramp", "rack-focus", "freeze-frame"], ["gym", "travel", "tech"]),
 "meme-cc0": ("Self-made CC0 versions of generic meme sounds (censor beep, sad trombone, rimshot).", ["freeze-frame", "smash-cut"], ["general", "gym", "tech", "gaming", "travel"]),
 "voice-announcer": ("Game-announcer voice lines (CC0): 'level up', 'mission failed', 'flawless victory', 'game over', countdowns.", ["freeze-frame", "smash-cut", "counter-roll"], ["gaming", "gym"]),
 "jingles": ("Short musical stings (sax, steel drum, pizzicato, hits) for intros, outros and punchlines.", ["cross-dissolve", "freeze-frame"], ["travel", "general"]),
 "foley": ("Everyday object sounds (doors, cloth, books, knives, pots, water) for B-roll realism.", ["match-cut", "object-mask-wipe"], ["travel", "tech", "general"]),
 "foley-footsteps": ("Footsteps on concrete, wood, grass, snow, carpet: walking B-roll, jump-through landings.", ["jump-through", "match-cut"], ["travel", "gym"]),
 "foley-cards-dice": ("Cards, poker chips and dice handling: board/card game content, 'deal' transitions.", ["slide-push"], ["gaming"]),
 "sci-fi": ("Lasers, engines, force fields, sci-fi doors: gaming edits and techy motion graphics.", ["glitch", "zoom-in-transition"], ["gaming", "tech"]),
 "ui-error": ("Error buzzes for wrong answers, failed attempts, fake error dialogs.", ["glitch", "smash-cut"], ["tech", "gaming"]),
 "ui-open-close": ("UI panels opening/closing, maximise/minimise, back/drop actions.", ["swipe-up-ui", "split-reveal"], ["tech"]),
 "misc": ("Uncategorised CC0 sounds: browse before use.", [], ["general"]),
}
GYM_SUB = [(r"metal_falling", "barbell/plate drop"), (r"clink|bing|bong|thud|impactMetal", "plate/dumbbell clank")]
GAMING_SUB = [(r"power_up|powerUp|power-up|Power%20Up", "power-up"), (r"coin", "8-bit coin"), (r"jingles_NES", "level-up / 8-bit jingle")]


def prefix(rel):
    if rel.startswith("kenney_"):
        return "kenney-" + rel.split("/")[0][7:].replace("-sounds", "").replace("-audio", "")
    if rel.startswith("oga/items/"):
        return "oga-" + rel.split("/")[2][:28]
    if rel.startswith("uisfx/"):
        return "uisfx-" + rel.split("/")[1]
    if rel.startswith("inhouse/"):
        return "inhouse"
    return "x"


def clean(name):
    name = name.replace("%20", "_")
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", name).strip("_")


def attribution(it):
    lic = it["licence"]
    if "BY" in lic:
        return f"\"{it['source_title']}\" by {it['author']} ({it['source_url']}), licensed CC BY 3.0. Credit in the caption."
    if it["author"].startswith("Srijan media library"):
        return "Not required (CC0, made in-house: library/tools/synth_inhouse.py)."
    return f"Not required (CC0). Courtesy credit: {it['author']}, {it['source_url']}"


sel = json.load(open(SEL))
full = json.load(open(FULL))
used_paths, used_names, out = set(), set(), []


def add(it, cat, featured, rank=None):
    base = clean(os.path.splitext(os.path.basename(it["rel"]))[0])
    name = f"{prefix(it['rel'])}-{base}.mp3"
    k = 2
    while (cat, name) in used_names:
        name = f"{prefix(it['rel'])}-{base}-{k}.mp3"
        k += 1
    used_names.add((cat, name))
    use, trans, niches = CAT.get(cat, CAT["misc"])
    sub = None
    for rx, label in (GYM_SUB if cat == "gym" else GAMING_SUB if cat == "gaming" else []):
        if re.search(rx, it["rel"]):
            sub = label
            break
    if "chalk" in it["rel"]:
        sub = "chalk clap"
    desc = it.get("source_title", "")
    e = {
        "id": f"{cat}/{os.path.splitext(name)[0]}",
        "staged": it["staged"], "category": cat, "file": name,
        "subtype": sub, "tier": "cc0", "featured": featured, "featured_rank": rank,
        "licence": it["licence"], "source_url": it["source_url"], "author": it["author"],
        "attribution": attribution(it), "source_file": os.path.basename(it["rel"]),
        "source_title": desc, "derived_from": it.get("derived_from") or None,
        "use_when": use + (f" ({sub})" if sub else ""), "pairs_with_transition": trans, "niches": niches,
        "z": it.get("z"), "verdict": it.get("verdict"), "sounds_most_like": it.get("sounds_most_like"),
        "check_summary": it.get("check_summary"),
        "trimmed_from_s": it.get("src_dur_s") if it.get("truncated") else None,
    }
    out.append(e)
    used_paths.add(it["path"])


ranks = {}
for it in sel:
    ranks[it["category"]] = ranks.get(it["category"], 0) + 1
    add(it, it["category"], True, ranks[it["category"]])
rej = 0
for cat, items in full.items():
    for it in items:
        if it["path"] in used_paths:
            continue
        codes = set(it.get("check_codes") or [])
        if "silent" in codes or "clipping" in codes and it.get("src_clip_runs", 0) > 2 or it.get("src_clip_runs", 0) > 5:
            rej += 1
            continue
        if it.get("staged_dur_s", 0) < 0.03:
            rej += 1
            continue
        add(it, cat, False)
json.dump(out, open(OUT, "w"), indent=1)
from collections import Counter
c = Counter(e["category"] for e in out)
print(len(out), "entries,", sum(e["featured"] for e in out), "featured,", rej, "rejected (clipped/silent/too short)")
print(dict(sorted(c.items())))
