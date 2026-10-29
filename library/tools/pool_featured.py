"""Build the candidate pool (category -> files with licence metadata).
Usage: python3 -I pool.py DL_LIB UISFX_DIR OUT_JSON"""
import json, os, re, subprocess, sys

DL, UISFX, OUT = sys.argv[1:4]
KEN = {"casino-audio", "digital-audio", "impact-sounds", "interface-sounds", "music-jingles", "rpg-audio",
       "sci-fi-sounds", "ui-audio"}
oga = json.load(open(os.path.join(DL, "oga", "oga_items.json")))

# (category, regex on relative path) - first match wins per category, a file may serve several categories
RULES = [
    ("whoosh", r"swishes-sound-pack/.*swish-(1|2|3|4|5|6|7)\.wav$|air-whoosh/|erase-escape/"),
    ("swoosh-fast", r"swishes-sound-pack/.*swish-(8|9|10|11|12|13)\.wav$|3-melee-sounds/.*(sword|melee) sound"),
    ("pop", r"pop-sounds/|3-pop-sounds/pop\d|pop-effect-sounds/|bubbles-pop/|uisfx/(soft|rubber|organic)/(select|drop|snap)\.mp3"),
    ("click-ui", r"kenney_interface-sounds/.*/(click|select|tick)_|kenney_ui-audio/.*/(click|mouseclick)|qubodup-click|10-clicks-and-switches/.*click\.\d|uisfx/(minimal|studio|mechanical)/press\.mp3"),
    ("keyboard", r"keyboard-soundpack.*/keypress-0(0[1-9]|1\d)\.wav|uisfx/(mechanical|studio)/typing\.mp3"),
    ("typing", r"keyboard-soundpack.*/generated-00[3-6]|typing-soundeffect/|typewriter-sounds/.*typewriter[1-5]\.wav"),
    ("hit-impact", r"kenney_impact-sounds/.*/impact(Punch_heavy|Punch_medium|Wood_heavy|Soft_heavy|Generic_light)_00[0-2]|75-cc0.*bfh1_hit_(0[1-8])"),
    ("bass-drop-boom", r"kenney_sci-fi-sounds/.*/(lowFrequency_explosion|explosionCrunch_00[0-2])|muffled-distant-explosion/|synthesized-explosion/|explosions-4/|50-cc0-retro.*retro_explosion"),
    ("riser", r"level-up-power-up.*/unz/(Rise0\d|Upper01)\.aif$|kenney_digital-audio/.*/phaserUp[1-4]"),
    ("downlifter", r"level-up-power-up.*/unz/Downer01\.aif$|kenney_digital-audio/.*/(phaserDown|lowDown|highDown)"),
    ("glitch", r"kenney_interface-sounds/.*/glitch_|kenney_sci-fi-sounds/.*/computerNoise|kenney_digital-audio/.*/(zap\d|spaceTrash[1-3])|50-cc0-retro.*synth_misc_0[1-6]"),
    ("camera-shutter", r"camera/photo\.ogg"),
    ("notification-ding", r"kenney_interface-sounds/.*/(bong_|confirmation_00[0-2])|bell-dingschimes/|kalimba-two-notes/|alertnotification-sound/alert\.wav|uisfx/(glass|soft|studio|zen)/notification\.mp3"),
    ("chime-success", r"uisfx/(glass|dreamy|studio|soft|cinematic)/(success|complete|achievement)\.mp3|kenney_music-jingles/.*jingles_(STEEL|PIZZI|HIT)0[0-4]|magic-words-healing"),
    ("record-scratch", r"vinyl/vinylstart|scratch-vocal-sound/"),
    ("crowd-cheer-applause", r"applause-in-a-large-hall|well-done/.*\.flac$|crowd-shoutingspeaking|oooooooooooooo/"),
    ("gym", r"metal-impact-sounds/|kenney_impact-sounds/.*/impactMetal_heavy_00[0-3]|75-cc0.*bfh1_metal_(falling|hit)_0[1-3]|kenney_impact-sounds/.*/impactBell_heavy_000"),
    ("gaming", r"10-8bit-coin-sounds/.*/coin\d+\.wav$|12-coin-sound-effects/coin\.[1-6]\.|50-cc0-retro.*(retro_coin|power_up_0[1-6])|kenney_digital-audio/.*/powerUp([1-9]|1[0-2])\.|kenney_music-jingles/.*jingles_NES0[0-9]|new-thing-get/|oldschool-win.*round_end|power-up-level-up-beansjam/"),
    ("cash-register", r"coin-drop/coin_drop\.wav|purchasing-sound-effect/|kenney_rpg-audio/.*/handleCoins|kenney_casino-audio/.*/chips-(stack|collide)-[1-3]|80-cc0-rpg.*item_coins"),
    ("heartbeat", r"heartbeat-sounds/|heartbeat-single-sound/"),
]


def src_meta(rel):
    parts = rel.split("/")
    if parts[0].startswith("kenney_") and parts[0][7:] in KEN:
        pack = parts[0][7:]
        return {"licence": "CC0-1.0", "author": "Kenney (www.kenney.nl)",
                "source_url": f"https://kenney.nl/assets/{pack}", "source_title": f"Kenney {pack.replace('-', ' ').title()} pack"}
    if parts[0] == "oga":
        slug = parts[2]
        it = oga[slug]
        lic = "CC0-1.0" if all(l.strip() == "CC0" for l in it["licenses"]) else ",".join(it["licenses"])
        if slug == "well-done":  # file name says CCBY3: credit it to be safe
            lic = "CC0-1.0 / CC-BY-3.0 (file name says CC-BY 3.0; credit given)"
        return {"licence": lic, "author": it["author"], "source_url": it["url"], "source_title": it["title"]}
    if parts[0] == "uisfx":
        return {"licence": "CC0-1.0", "author": "Yuki Capital (uisfx 0.4.0)", "source_url": "https://github.com/romainsimon/uisfx",
                "source_title": "uisfx (vendored in .claude/skills/real-sfx/vendor)"}
    raise ValueError(rel)


files = []
for root, _, fs in os.walk(DL):
    for f in fs:
        if f.startswith("._") or "__MACOSX" in root:
            continue
        if f.lower().endswith((".wav", ".ogg", ".mp3", ".flac", ".aif", ".aiff")):
            full = os.path.join(root, f)
            files.append((os.path.relpath(full, DL), full))
for root, _, fs in os.walk(os.path.join(UISFX, "sounds")):
    for f in fs:
        if f.endswith(".mp3"):
            full = os.path.join(root, f)
            files.append(("uisfx/" + os.path.relpath(full, os.path.join(UISFX, "sounds")), full))

pool = {}
for cat, rx in RULES:
    r = re.compile(rx)
    for rel, full in sorted(files):
        if r.search(rel):
            if rel.startswith("oga/") and "/items/" not in rel:
                continue
            m = src_meta(rel)
            pool.setdefault(cat, []).append({"rel": rel, "path": full, **m})
for cat, lst in pool.items():
    print(cat, len(lst), file=sys.stderr)
json.dump(pool, open(OUT, "w"), indent=1)
