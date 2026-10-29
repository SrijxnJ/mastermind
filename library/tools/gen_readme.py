"""Write library/README.md from catalog.json and the folders. Usage: python3 -I gen_readme.py LIBRARY_DIR"""
import json, os, subprocess, sys
from collections import Counter, defaultdict

LIB = sys.argv[1]
cat = json.load(open(os.path.join(LIB, "catalog.json")))
memes = json.load(open(os.path.join(LIB, "memes", "memes.json")))
imgs = json.load(open(os.path.join(LIB, "memes", "meme_images.json")))
trs = json.load(open(os.path.join(LIB, "transitions", "transitions.json")))


def du(p):
    return subprocess.run(["du", "-sh", os.path.join(LIB, p)], capture_output=True, text=True).stdout.split()[0]


by = defaultdict(list)
for e in cat:
    by[e["category"]].append(e)
lic = Counter(e["licence"] for e in cat)
tiers = Counter(e["tier"] for e in cat)
src = Counter(("Kenney" if "kenney.nl" in e["source_url"] else "OpenGameArt" if "opengameart" in e["source_url"]
               else "uisfx" if "uisfx" in e["source_url"] else "in-house") for e in cat)
raw_k = sorted(os.listdir(os.path.join(LIB, "raw", "kenney")))
raw_o = json.load(open(os.path.join(LIB, "raw", "opengameart_sources.json")))
CORE = ["whoosh", "swoosh-fast", "pop", "click-ui", "keyboard", "typing", "hit-impact", "bass-drop-boom", "riser", "downlifter",
        "glitch", "camera-shutter", "notification-ding", "chime-success", "record-scratch", "rewind-tape-stop",
        "crowd-cheer-applause", "gym", "gaming", "cash-register", "heartbeat", "meme-cc0"]
EXTRA = sorted(set(by) - set(CORE))

L = ["# Srijan's media library", "",
     "Sound effects, meme notes, transitions and a mixing guide for short-form reels (gym, tech/PC, gaming, travel), edited in",
     "Instagram Edits, CapCut and VN, or with ffmpeg + HyperFrames. Every file in `sfx/` has a clean licence: **CC0**,",
     "or **CC BY** with the credit written down in `catalog.json`.", "",
     "## Index", "",
     "| Path | What |", "|---|---|",
     f"| [`catalog.json`](catalog.json) | One entry per sound ({len(cat)}): id, file, category, subtype, tier, featured, duration_s, lufs, peak_db, licence, source_url, author, attribution, use_when, pairs_with_transition, niches, earshot verdict |",
     f"| `sfx/<category>/` | {len(cat)} trimmed, loudness-normalised MP3s (128 kbps, 44.1 kHz) in {len(by)} categories ({du('sfx')}) |",
     f"| [`memes/MEMES.md`](memes/MEMES.md), `memes/memes.json` | {len(memes)} meme sounds/formats: meaning, frame timing, visual pairing, Edits + CapCut search terms, CC0 recreation if one exists, risk |",
     f"| `meme-images/`, `memes/meme_images.json` | Top {len(imgs)} imgflip meme templates + usage notes ({du('meme-images')}) |",
     f"| [`transitions/TRANSITIONS.md`](transitions/TRANSITIONS.md), `transitions/transitions.json` | {len(trs)} transitions: when, paired SFX files, frames at 30 fps, easing, CapCut/Edits/VN steps, filming, ffmpeg/HyperFrames |",
     "| [`mixing/MIXING.md`](mixing/MIXING.md) | Levels (L06: lo-fi bed −22 to −24 dB under voice), ducking, iPhone voice chain, loudness targets, gym beat-sync, ffmpeg recipes, earshot QA checklist |",
     f"| `raw/kenney/<pack>/` | Untouched Kenney CC0 packs for digging ({len(raw_k)} packs, {du('raw/kenney')}) |",
     f"| `raw/opengameart_sources.json` | Index of the {len(raw_o)} CC0-only OpenGameArt items used (URL, author, title). The raw files themselves were not kept (482 MB; dropped to save disk); re-download from the URLs |",
     "| [`local-only/`](local-only/LICENCE-NOTE.md) | Tier for Mixkit / Sonniss files, which are free to use in videos but may NOT be redistributed. Empty: both sites block this container (see the note) |",
     "| `tools/` | The pipeline that built all of this: OpenGameArt search, in-house DSP (`synth_inhouse.py`), staging + earshot judging, selection, normalise/encode (`build_library.py`), doc generators |",
     "", "## How to pick a sound fast", "",
     "1. Open the category folder. Files with `\"featured\": true` in `catalog.json` are the earshot-ranked top picks (listed below). The rest are the full CC0 packs, sorted into the same categories.",
     "2. Every file is pre-normalised. Short clicks/pops sit lower because they hit the −1 dBTP ceiling first. Turn sounds **down** in the editor, never up (see MIXING.md §1 for starting levels).",
     "3. MP3 adds ~26 ms of encoder delay at the start (under 1 frame at 30 fps). For frame-exact work in ffmpeg, use the `raw/kenney/` original, or re-download the OpenGameArt source (URL in `catalog.json`).",
     "", "## Counts", "",
     f"**Total:** {len(cat)} sounds, {sum(e['featured'] for e in cat)} featured. **Tiers:** " + ", ".join(f"{k}: {v}" for k, v in tiers.items()) +
     ". **Sources:** " + ", ".join(f"{k}: {v}" for k, v in src.most_common()) + ".", "",
     "| Category | Featured | All | Featured files (best first) |", "|---|---|---|---|"]
for c in CORE + EXTRA:
    es = by.get(c, [])
    f = sorted([e for e in es if e["featured"]], key=lambda e: e["featured_rank"] or 99)
    L.append(f"| `{c}` | {len(f)} | {len(es)} | " + ", ".join(os.path.basename(e["file"]) for e in f) + " |")
L += ["", "## Licence policy", "",
      "- **Allowed in `sfx/` and `raw/`:** CC0 / public domain, or CC BY with the attribution recorded (`attribution` field; put it in the caption when you use the sound).",
      "- **Licences in this library:** " + "; ".join(f"{k}: {v} files" for k, v in lic.most_common()) + ".",
      "- **Sources used:** Kenney.nl audio packs (CC0); OpenGameArt items whose every listed licence is CC0. One item, qubodup's \"Well Done\", is listed CC0 but its file name says CC BY 3.0, so it is credited as CC BY to be safe. uisfx (CC0 audio, vendored in `.claude/skills/real-sfx/vendor`). In-house sounds made with numpy/scipy DSP, from scratch or from CC0 Kenney recordings, are dedicated CC0 (`tools/synth_inhouse.py`).",
      "- **Never committed:** Mixkit, Pixabay, Zapsplat, myinstants, BBC Sound Effects (non-commercial only), anything ripped from games, films, TV or other creators. Meme audio is reached through the **Instagram Edits / CapCut in-app libraries** (search terms in MEMES.md). Mixkit and Sonniss files may only ever live in `local-only/`.",
      "- **Meme images** (`meme-images/`) are third-party templates. Use them only for commentary or parody with your own caption; never in ads.",
      "- **Blocked from this container (2026-10-27):** Openverse API (504 timeouts), the Freesound CDN, Pixabay, BigSoundBank and GIPHY (403), Wikimedia Commons (429 rate limit), Mixkit (Cloudflare challenge), Sonniss (403).",
      "", "## Existing tools and how they relate", "",
      "- **earshot** (`~/sm-tools/earshot`, MIT): used to judge every featured pick (`api.rank` against a text description, CLAP z-score + verdict) and to audit every file (`sfx check`: clipping, clicks, DC, cut tails, comb ring). Its 252-sound bank is code-synthesised and renders on demand (`earshot sfx render whoosh_fast/crisp -o w.wav`, `earshot kit`). It is MIT-licensed code, not CC0 audio, so renders are **referenced, not committed**. Good bank ids: `whoosh_fast/*`, `riser/*`, `downlifter/*`, `cut_hit/*`, `shutter/*`, `glitch/*`, `notify/*`, `typing_key/*`.",
      "- **real-sfx** skill (`.claude/skills/real-sfx`): its vendored **uisfx** pack (936 MP3s = 78 UI cues × 12 styles, audio CC0) is usable. The featured chime/notification/keyboard picks come from it. To have real-sfx place sounds from this library, register it: `python scripts/setup.py add-library srijan library/sfx --tier main --index`. That works because `catalog.json` gives each file its type.",
      "- **real-sound** skill: the process for full soundtracks (cue list, licence checks, mixer, QA). Use it with this library as the source.",
      "", "## Rebuild", "",
      "```bash",
      "S=<scratch dir>; L=library   # then: python3 -I $L/tools/fix_categories.py $L",
      "python3 -I $L/tools/oga_search.py $S/dl/oga whoosh pop ...              # OpenGameArt CC0 index + files",
      "$EARSHOT_VENV/python -I $L/tools/synth_inhouse.py $S/dl $S/synth        # in-house CC0 sounds",
      "$EARSHOT_VENV/python -I $L/tools/stage_and_judge.py POOL.json $S/synth $S/stage   # trim + earshot rank/audit",
      "python3 -I $L/tools/select_featured.py sel.json $S/stage/judged.json ...   # featured picks",
      "python3 -I $L/tools/assemble.py sel.json full_judged.json build.json && python3 -I $L/tools/build_library.py build.json $L",
      "python3 -I $L/tools/gen_docs.py $L $L/tools/data/memes_src.json $L/tools/data/transitions_src.json && python3 -I $L/tools/gen_readme.py $L",
      "```", ""]
open(os.path.join(LIB, "README.md"), "w").write("\n".join(L))
print("README written")
