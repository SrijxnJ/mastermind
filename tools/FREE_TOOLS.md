# Free local editing tools

Free, open-source tools that run on the CPU. No API keys, no accounts, no usage limits. They replace paid apps and preset packs.
Rebuild them all in a fresh session with `tools/setup_free_tools.sh` (safe to run again). Installed 27 Oct 2026.

Each licence was checked before install: first the package metadata on PyPI, then the upstream `LICENSE` file (model licences come from Google's model-card PDFs).

| Tool | Version | Licence | Checked in | Where | Size on disk | Replaces | Wrapper |
|---|---|---|---|---|---|---|---|
| **auto-editor** (WyattBlue) | 29.3.1 | **Unlicense** (public domain) | PyPI `license_expression: Unlicense`; repo `LICENSE` | `.venv` (own venv; static binary ~41 MB) | ~65 MB | ReCut (paid silence remover) | `tools/autocut.sh` |
| **MediaPipe** (Google) | 1.1.1 | **Apache-2.0** | PyPI classifier; repo `LICENSE` | `.venv` | in the 1.1 GB venv | Paid "remove background" / CapCut Pro cut-out | `tools/text_behind.py` |
| MediaPipe `selfie_multiclass_256x256.tflite` (default model) | float32 "latest" (sha256 `c6748b12…`) | **Apache-2.0** | Model card PDF ("Licensed under Apache License, Version 2.0") | `~/sm-tools/models/vision/` | 16 MB | | `--model multiclass` |
| MediaPipe `selfie_segmenter.tflite` | float16 "latest" (sha256 `191ac952…`) | **Apache-2.0** | Model card PDF | same | 0.25 MB | | `--model selfie` |
| **rembg** (danielgatis) | 2.0.86 | **MIT** | PyPI classifier; repo `LICENSE.txt` | `.venv` | in the venv | | `--model u2netp` |
| rembg `u2netp.onnx` (U²-Net small) | sha256 `309c8469…` | **Apache-2.0** (U-2-Net repo `LICENSE`) | repo `LICENSE` | `~/sm-tools/models/vision/models/u2netp/` | 4.6 MB | | |
| **onnxruntime** (Microsoft, rembg's engine) | 1.31.1 | **MIT** | PyPI classifier | vision venv | | | |
| **OpenCV contrib** (guided-filter mask refinement) | 5.0.0.93 | **Apache-2.0** | PyPI classifier | vision venv | | | |
| numpy / Pillow | 2.4.6 / 13.0.0 | BSD-3-Clause (+0BSD/MIT/Zlib) / MIT-CMU | PyPI `license_expression` | vision venv | | Paid LUT/preset packs (with luts.py) | `tools/luts.py` |
| Anton, Instrument Serif (fonts) | from Google Fonts | **SIL OFL 1.1** | licence string embedded in each `.ttf` | `tools/fonts/` (committed, 0.3 MB) | | | text_behind default font |

Other packages pulled in by the vision venv (all permissive): absl-py, flatbuffers, protobuf, requests, tzdata (Apache-2.0); scipy, scikit-image, numba, llvmlite, pooch, networkx, imageio, tifffile, contourpy (BSD); PyMatting, attrs, jsonschema, sounddevice, fonttools (MIT); matplotlib (PSF-style); certifi (MPL-2.0); tqdm (MPL-2.0 AND MIT). Nothing GPL, nothing that phones home or meters usage.
`.venv` and `~/sm-tools/earshot` are separate (see `setup_audio_tools.sh`) and were not touched.

## 1. Silence / dead-air removal: `tools/autocut.sh`

```bash
tools/autocut.sh talk.mp4                 # -> talk_autocut.mp4, 0.15 s margin, 4 % loudness threshold
tools/autocut.sh talk.mp4 -l              # + talk_autocut.edits.csv (kept/cut ranges in seconds) + .v3 timeline
tools/autocut.sh talk.mp4 -x resolve      # + DaVinci Resolve .fcpxml (also premiere, final-cut-pro, shotcut, kdenlive)
tools/autocut.sh talk.mp4 -s 6            # speed silences up x6 instead of cutting them
tools/autocut.sh talk.mp4 -p              # stats only
```
Test (27 Oct 2026): 18.6 s of speech from the L10 reel, with 4 dead-air gaps added (1.8 + 2.2 + 1.5 + 2.5 = 8.0 s, frozen picture, pink-noise room tone at −50 dBFS).
**26.60 s → 18.77 s** (7.83 s removed, 29.4 %), 4 cuts, all on the inserted gaps, with no cut inside a sentence. Speed mode (`-s 6`) gave 26.53 → 20.07 s.
Render time was about 38 s on CPU for 27 s of 720p.

## 2. Text behind your head (L10): `tools/text_behind.py`

```bash
.venv/bin/python -I tools/text_behind.py IN.mp4 --text "75 KG" \
  --font tools/fonts/Anton-Regular.ttf --color "#FFD21F" --size 0.2 --x 0.5 --y 0.42 \
  --start 0.3 --end 3.3 --clip-start 4.0 --clip-end 7.5 -o OUT.mp4 [--mask-video MASK.mp4]
```
How it works: original frame → text layer (soft shadow, fade in/out) → the person cut out of the same frame on top.
The mask goes through confidence levels, a guided filter (edges snap to hair, hands and shoulders), motion-adaptive temporal smoothing (edges appear fast, fade slowly), a 1 px choke and a 1.5 px feather. The original audio is kept.
Other options: `--outline N` (hollow letters, like the L10 "EDIT" CTA), `--tracking`, `--rise`, `--opacity`, two lines with `\n`, `--model selfie|u2netp`.

Model comparison on the gym incline set (person reclined, arms overhead): **multiclass** gave a clean full-body silhouette (280 ms a frame).
**selfie** was 33 ms a frame but put false blobs in the background and gave blocky edges. **u2netp** caught only part of the body.
Use multiclass unless speed matters.
Speed: about 1 s a frame at 1080×1920 including the guided filter and encode, so a 3.5 s test takes about 100 s.
Temporal smoothing at 0.8 cut edge jitter by 19 % against no smoothing (second-difference metric 0.094 → 0.077) with no visible lag on the moving arms.

Limits: arms with heavy motion blur are only partly caught, so a letter can show faintly through a fast-moving forearm.
Objects the person holds (barbell, phone) count as background, so the text covers them.
It needs the subject's head or hands to actually cross the text area. Frame the shot with headroom (L06/L10).

## 3. Grade LUTs: `tools/luts.py` → `library/luts/`

`moody`, `gym-contrast`, `travel-warm`, `tech-clean` as 33-point `.cube` files, with before/after PNGs and import steps in `library/luts/README.md`.
Run `.venv/bin/python -I tools/luts.py [--compare NAME=IMAGE ...]`.
