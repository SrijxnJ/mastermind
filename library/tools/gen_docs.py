"""Generate memes.json/MEMES.md, transitions.json/TRANSITIONS.md from the source data + catalog.json.
Usage: python3 -I gen_docs.py LIBRARY_DIR MEMES_SRC_JSON TRANSITIONS_SRC_JSON"""
import json, os, re, sys

LIB, MSRC, TSRC = sys.argv[1:4]
cat = json.load(open(os.path.join(LIB, "catalog.json")))
cc0 = [e for e in cat if e["tier"] == "cc0"]


def featured(category, n=3, rx=None):
    xs = [e for e in cc0 if e["category"] == category and (rx is None or re.search(rx, e["file"]))]
    xs.sort(key=lambda e: (not e["featured"], e.get("featured_rank") or 999, e["file"]))
    return [e["file"] for e in xs[:n]]


# ------------------------------------------------------------------------------------------------ memes
# exact search terms for the licensed in-app libraries (Instagram Edits: Audio > Sound effects / Music; CapCut: Audio >
# Sound effects / Sounds). Availability varies by region and account type (Business accounts get a reduced music library).
SEARCH = {
 "vine-boom": ("vine boom", "vine boom"), "bruh": ("bruh", "bruh"), "metal-pipe": ("metal pipe", "metal pipe falling"),
 "emotional-damage": ("emotional damage", "emotional damage"), "windows-xp-error": ("windows error", "windows xp error"),
 "windows-xp-shutdown": ("windows shutdown", "windows xp shutdown"), "sad-violin": ("sad violin", "sad violin"),
 "record-scratch-freeze": ("record scratch", "record scratch"), "anime-wow": ("anime wow", "anime wow"),
 "phonk-gigachad": ("phonk", "gigachad phonk"), "aura-farming": ("aura", "aura edit phonk"),
 "stay-hard": ("stay hard goggins", "goggins stay hard"), "light-weight-baby": ("light weight baby", "yeah buddy light weight"),
 "goku-power-up": ("power up", "super saiyan power up"), "rocky-montage": ("Gonna Fly Now", "Eye of the Tiger"),
 "zyzz-hardstyle": ("zyzz hardstyle", "zyzz"), "nah-id-win": ("nah id win", "nah id win"), "let-him-cook": ("let him cook", "let him cook"),
 "gta-wasted": ("wasted", "gta wasted"), "minecraft-oof": ("oof", "minecraft oof"), "mario-coin": ("coin", "mario coin"),
 "level-up": ("level up", "level up"), "mlg-hitmarker": ("hitmarker", "mlg hitmarker"), "mission-failed": ("mission failed", "mission failed"),
 "among-us-emergency": ("among us", "emergency meeting"), "zelda-secret": ("secret discovered", "zelda secret"),
 "ps1-startup": ("playstation startup", "ps1 startup"), "curb-outro": ("curb your enthusiasm", "curb your enthusiasm"),
 "spongebob-time-card": ("a few moments later", "few moments later"), "taco-bell-bong": ("taco bell bong", "taco bell"),
 "fahhh": ("fahhh", "fahh"), "censor-beep": ("censor beep", "censor beep"), "oh-no": ("oh no oh no", "oh no oh no no no"),
 "coffin-dance": ("coffin dance", "astronomia"), "to-be-continued": ("to be continued", "to be continued"),
 "wilhelm-scream": ("wilhelm scream", "wilhelm scream"), "crickets": ("crickets", "crickets"), "rimshot": ("ba dum tss", "rimshot"),
 "sad-trombone": ("sad trombone", "sad trombone"), "airhorn": ("air horn", "mlg air horn"), "bonk": ("bonk", "bonk"),
 "boing": ("boing", "cartoon boing"), "dun-dun-dun": ("dun dun dun", "dramatic sound"), "law-and-order": ("law and order", "law and order"),
 "jeopardy-think": ("jeopardy", "jeopardy think music"), "wii-shop": ("wii shop", "wii shop channel"),
 "hello-darkness": ("hello darkness my old friend", "sound of silence"), "owen-wilson-wow": ("owen wilson wow", "wow owen wilson"),
 "rizz": ("rizz", "rizz sound effect"), "cat-laughing": ("cat laughing", "huh cat"), "yippee": ("yippee", "yippee"),
 "sheesh": ("sheesh", "sheesh"), "nani": ("nani", "omae wa mou shindeiru"), "directed-by": ("directed by robert b weide", "directed by robert b weide"),
 "dial-up": ("dial up", "dial up internet"), "im-in": ("hacker typing", "keyboard typing"), "mac-startup": ("startup sound", "mac startup"),
 "notification-ping": ("notification", "notification"), "cash-register": ("cash register", "ka ching"), "heartbeat-tension": ("heartbeat", "heartbeat"),
 "crowd-cheer": ("crowd cheer", "applause"), "airplane-chime": ("airplane chime", "seatbelt sign"), "suitcase-transition": ("stamp", "stamp"),
 "camera-shutter-snap": ("camera shutter", "camera shutter"), "rewind-tape": ("rewind", "vhs rewind"), "glitch-error": ("glitch", "glitch"),
 "chill-guy": ("chill guy", "chill guy"), "sigma-stare": ("sigma", "sigma bass boosted"),
 "flawless-victory": ("flawless victory", "flawless victory"), "combo-breaker": ("combo breaker", "combo breaker"),
}
# CC0 files in this library: (category, regex on file name or None, how close it is)
RECREATION = {
 "censor-beep": ("meme-cc0", r"censor", "recreation (a 1 kHz beep is the real thing)"),
 "sad-trombone": ("meme-cc0", r"trombone", "recreation (synthesized from scratch, same 4-note motif)"),
 "rimshot": ("meme-cc0", r"rimshot", "recreation (synthesized snare-snare-cymbal)"),
 "mission-failed": ("voice-announcer", r"mission_failed", "CC0 voice line 'Mission failed' (Kenney), not the CoD actor"),
 "flawless-victory": ("voice-announcer", r"flawless", "CC0 voice line 'Flawless victory' (Kenney fighter pack)"),
 "combo-breaker": ("voice-announcer", r"combo", "CC0 voice line 'Combo breaker' (Kenney fighter pack)"),
 "level-up": ("gaming", r"jingles_NES|power", "original CC0 chiptune level-up/power-up (+ voice 'level up' in voice-announcer)"),
 "mario-coin": ("gaming", r"coin", "original CC0 8-bit coins (not Nintendo's)"),
 "record-scratch-freeze": ("record-scratch", None, "CC0 scratch; record the VO line yourself"),
 "cash-register": ("cash-register", None, "CC0 equivalent"), "heartbeat-tension": ("heartbeat", None, "CC0 equivalent"),
 "crowd-cheer": ("crowd-cheer-applause", None, "CC0 equivalent"), "camera-shutter-snap": ("camera-shutter", None, "CC0 equivalent"),
 "rewind-tape": ("rewind-tape-stop", None, "CC0 equivalent (in-house tape stop / VHS rewind)"),
 "glitch-error": ("glitch", None, "CC0 equivalent"), "notification-ping": ("notification-ding", None, "CC0 equivalent (no Apple/WhatsApp tones)"),
 "airplane-chime": ("notification-ding", None, "similar-feel CC0 ding"), "im-in": ("typing", None, "CC0 typing bed; voice the line yourself"),
 "vine-boom": ("bass-drop-boom", None, "similar-feel substitute, NOT the vine boom sample"),
 "taco-bell-bong": ("bass-drop-boom", None, "similar-feel substitute"), "sigma-stare": ("bass-drop-boom", None, "similar-feel substitute"),
 "phonk-gigachad": ("bass-drop-boom", None, "boom for the drop only; the music must come from the app"),
 "metal-pipe": ("gym", r"clink|bing|bong|impactMetal", "similar-feel metal clank, NOT the meme sample"),
 "gta-wasted": ("downlifter", None, "substitute: downlifter + Kenney 'game over' announcer clip"),
 "windows-xp-shutdown": ("downlifter", None, "substitute"), "windows-xp-error": ("ui-error", None, "substitute error buzz"),
 "minecraft-oof": ("hit-impact", None, "substitute hit (no voice)"), "bonk": ("hit-impact", None, "similar-feel CC0 hit"),
 "dun-dun-dun": ("hit-impact", None, "build from 3 CC0 hits"), "law-and-order": ("gym", r"clink|bing|bong|impactMetal", "build from 2 metal clanks"),
 "nani": ("hit-impact", None, "hit for the zoom punch only"), "suitcase-transition": ("hit-impact", None, "CC0 thud"),
 "goku-power-up": ("riser", None, "riser substitute + your own yell"), "ps1-startup": ("riser", None, "substitute swell"),
 "mac-startup": ("chime-success", None, "substitute chime"), "zelda-secret": ("chime-success", None, "substitute chime"),
 "anime-wow": ("chime-success", None, "sparkle chime only (no voice)"), "yippee": ("chime-success", None, "chime only (no voice)"),
 "boing": ("pop", None, "pop substitute"), "airhorn": ("crowd-cheer-applause", None, "crowd substitute (no CC0 air horn passed QA)"),
 "light-weight-baby": ("crowd-cheer-applause", None, "crowd only; no voice"), "stay-hard": ("heartbeat", None, "heartbeat bed + your own VO"),
 "dial-up": ("glitch", None, "weak substitute"), "jeopardy-think": ("typing", None, "weak substitute (waiting bed)"),
 "mlg-hitmarker": ("click-ui", None, "click as hitmarker"), "aura-farming": ("pop", None, "pop for the '+aura' counter text only"),
}
memes = json.load(open(MSRC))
memes += [
 {"id": "flawless-victory", "name": "'Flawless victory' (Mortal Kombat announcer)", "group": "gaming",
  "sounds_like": "Deep announcer voice: 'Flawless victory.'", "meaning": "Total domination with zero damage: perfect set, perfect build, perfect trip.",
  "timing": "Line starts on the final frame of the win (last rep locked, last cable tied); freeze 30-45 frames under it.",
  "visual": "Freeze, desaturate the loser/background, gold text 'FLAWLESS VICTORY'.", "niches": ["gaming", "gym"],
  "in_app": "", "library_category": "voice-announcer", "risk": "The MK line is Warner Bros. IP: in-app only. The Kenney CC0 'flawless victory' voice line in this library is a legal stand-in."},
 {"id": "combo-breaker", "name": "'C-C-C-COMBO BREAKER' (Killer Instinct)", "group": "gaming",
  "sounds_like": "Hyped announcer stutter 'C-C-C-COMBO BREAKER!'", "meaning": "Someone interrupts your streak/flow (phone call mid-set, mom mid-game).",
  "timing": "On the frame of the interruption; 2-3 quick zoom punches on the stutter syllables (6 frames apart).",
  "visual": "Stutter zooms + shake, red flash.", "niches": ["gaming", "gym"], "in_app": "", "library_category": "voice-announcer",
  "risk": "Killer Instinct line is Microsoft/Rare IP: in-app only. Kenney CC0 'combo breaker' (no stutter) is in the library; stutter it yourself by repeating the first 80 ms 3 times."},
]
out = []
for m in memes:
    e = dict(m)
    e.pop("in_app", None)
    e.pop("library_category", None)
    edits, capcut = SEARCH.get(m["id"], (m["name"], m["name"]))
    e["edits_search"] = f"Instagram Edits > Audio > search \"{edits}\" (Sound effects tab for SFX, Music tab for songs)"
    e["capcut_search"] = f"CapCut > Audio > Sound effects (or Sounds) > search \"{capcut}\""
    rec = RECREATION.get(m["id"])
    if rec:
        c, rx, how = rec
        files = featured(c, 3, rx)
        e["cc0_in_library"] = {"category": c, "files": files, "closeness": how, "is_recreation": how.startswith("recreation") or "voice line" in how}
    else:
        e["cc0_in_library"] = None
    e["legal_route"] = "Use the in-app library (licensed for use inside the app) or the CC0 file listed; never rip from YouTube/TikTok/myinstants."
    out.append(e)
os.makedirs(os.path.join(LIB, "memes"), exist_ok=True)
json.dump(out, open(os.path.join(LIB, "memes", "memes.json"), "w"), indent=1, ensure_ascii=False)

groups = {}
for e in out:
    groups.setdefault(e["group"], []).append(e)
L = ["# Meme sounds and formats (2026 field guide)", "",
     f"{len(out)} meme sounds and formats in use in gym, tech/PC, gaming and travel reels. For each one: what it sounds like, what it means, the exact frame rule at **30 fps**, the visual pairing, the niche fit, **where to get it legally**, and the risks.",
     "", "**How to read this:**",
     "- **Edits / CapCut search** is the licensed route. Sounds in the in-app libraries are cleared for use *inside that app's export*. Search the exact term given. Availability changes by region and account type: Business accounts get a reduced music library, so switch to a Creator account for music memes.",
     "- **CC0 in library** marks a file in `library/sfx/` you can use anywhere. ✅ **recreation** means a CC0 version of the same thing (a censor beep, a sad-trombone motif, a CC0 announcer line). ≈ **substitute** means a similar-feel CC0 sound, not the meme itself. The audience will not read it as the meme.",
     "- Never download meme audio from YouTube/TikTok rippers, myinstants or soundboard sites. Those files are copyrighted recordings (films, games, TV, creators' voices).",
     "- Frame numbers are at 30 fps (1 frame = 33 ms). \"Lands on\" means the sound's transient (or peak) sits on that frame.",
     "- Trend status as of Oct 2026: classics (vine boom, bruh, metal pipe) are evergreen but overused. 'Fahhh' peaked on TikTok from Sept 2025 (Know Your Meme). Aura farming and phonk edits are still common but saturated. Check Instagram's trending audio (the ↗ arrow) or TikTok Creative Center before relying on any \"new\" sound.",
     "- Sources: Know Your Meme (fahh, aura, yara-yara phonk, sleep phonk entries); voxbooster/uppbeat/dubbingai 2026 meme-sound roundups (vendor lists, not usage data). See the bottom of this file.",
     "", "## Index", ""]
for g, es in groups.items():
    L.append(f"- **{g}**: " + ", ".join(f"[{e['name']}](#{e['id']})" for e in es))
for g, es in groups.items():
    L += ["", f"## {g.title()}", ""]
    for e in es:
        rec = e["cc0_in_library"]
        if rec:
            mark = "✅ recreation" if rec["is_recreation"] else "≈ substitute"
            recline = f"{mark}: `{rec['category']}` ({rec['closeness']}): " + ", ".join(f"`{f}`" for f in rec["files"])
        else:
            recline = "none (voice/music meme: use the in-app library or record your own take)"
        L += [f"<a id=\"{e['id']}\"></a>", f"### {e['name']}", "",
              f"- **Sounds like:** {e['sounds_like']}",
              f"- **Means:** {e['meaning']}",
              f"- **Timing (30 fps):** {e['timing']}",
              f"- **Visual pairing:** {e['visual']}",
              f"- **Niches:** {', '.join(e['niches'])}",
              f"- **Edits search:** `{SEARCH.get(e['id'], (e['name'],))[0]}`  ·  **CapCut search:** `{SEARCH.get(e['id'], (e['name'], e['name']))[1]}`",
              f"- **CC0 in library:** {recline}",
              f"- **Risk:** {e['risk']}", ""]
L += ["## Sources", "",
      "- Know Your Meme: \"Fahh\" (Taileons, TikTok spread from Sept 2025), \"Yara Yara Phonk\" (viral Apr-May 2026), \"Sleep Phonk\", aura-farming entries: https://knowyourmeme.com/memes/fahh",
      "- 2026 meme-sound roundups (commercial soundboards, treat as anecdotal): https://voxbooster.com/blog/meme-sound-effects, https://uppbeat.io/blog/sound-effects/meme-sound-effects, https://dubbingai.io/articles/en/collection/trending-tiktok-meme-sound-effects",
      "- Roblox 'oof' replacement (2022 licensing dispute): widely reported; the original is third-party IP.",
      "- Meme *images* (top-100 imgflip templates) live in `library/meme-images/` with notes in `memes/meme_images.json`.", ""]
open(os.path.join(LIB, "memes", "MEMES.md"), "w").write("\n".join(L))

# ------------------------------------------------------------------------------------------------ transitions
trs = json.load(open(TSRC))
tout = []
for t in trs:
    e = dict(t)
    e["sfx_files"] = {c: featured(c, 3) for c in t["sfx"]}
    tout.append(e)
os.makedirs(os.path.join(LIB, "transitions"), exist_ok=True)
json.dump(tout, open(os.path.join(LIB, "transitions", "transitions.json"), "w"), indent=1, ensure_ascii=False)
L = ["# Transitions playbook", "",
     f"{len(tout)} transitions for Srijan's reels. Each one lists what it is, when to use it, the paired SFX (with files from `library/sfx`), frame timing at **30 fps**, the easing curve, how to build it in CapCut, Instagram Edits and VN, how to film for it, and the ffmpeg / HyperFrames route.",
     "", "**Easing rules (Brain L03):** entrances **ease-out** (fast start, soft landing). Exits **ease-in** (accelerate away). UI elements get a **spring with 3-6 % overshoot**. Never linear, except opacity on a dissolve.",
     "**SFX rule:** a whoosh's *peak* goes on the cut frame, not its start. `catalog.json` gives each file's duration; for whooshes the peak is usually 40-60 % in. A hit's *transient* goes on frame 0 of the change.",
     "**HyperFrames:** names in backticks are registry blocks/components (`npx hyperframes add <name>`; see `.claude/skills/hyperframes-registry`).", "",
     "| # | Transition | Best for | SFX | Length (frames @30) |", "|---|---|---|---|---|"]
for i, t in enumerate(tout, 1):
    L.append(f"| {i} | [{t['name']}](#{t['id']}) | {t['when'].split('.')[0]} | {', '.join(t['sfx']) or 'none'} | {t['frames'].split('.')[0][:60]} |")
for t in tout:
    sfx = "; ".join(f"**{c}**: " + ", ".join(f"`{f}`" for f in fs) for c, fs in t["sfx_files"].items()) or "none (audio edit itself)"
    L += ["", f"<a id=\"{t['id']}\"></a>", f"## {t['name']}", "",
          f"**What:** {t['what']}", "", f"**When:** {t['when']}", "",
          f"| | |", "|---|---|",
          f"| Frames @30 fps | {t['frames']} |", f"| Easing | {t['easing']} |", f"| SFX timing | {t['sfx_timing']} |",
          f"| SFX files | {sfx} |", f"| CapCut | {t['capcut']} |", f"| Instagram Edits | {t['edits']} |", f"| VN | {t['vn']} |",
          f"| Filming (tripod/phone) | {t['filming']} |", f"| ffmpeg | `{t['ffmpeg']}` |", f"| HyperFrames | {t['hyperframes']} |"]
open(os.path.join(LIB, "transitions", "TRANSITIONS.md"), "w").write("\n".join(L) + "\n")
print(len(out), "memes;", len(tout), "transitions")
