# tools/

Free, local, CPU-only helpers for the Brain. See also [FREE_TOOLS.md](FREE_TOOLS.md) for the editing tools (auto-cut, text behind head, LUTs).

## Reel X-ray and Reel Doctor

Two scripts that replace paid video breakdowns (vidIQ-style) and paid "virality predictors" (Higgsfield-style) with measurements we can check and rules we wrote down ourselves.

| | Reel X-ray (`xray.py`) | Reel Doctor (`doctor.py`) |
|---|---|---|
| Input | an Instagram / YouTube / TikTok URL, or a local video | a draft video (or URL) + `--format` + `--niche` |
| Does | measures the edit: cuts, overlays, text, faces, grade, motion, loudness, SFX, silences | runs the X-ray, then checks the draft against the Brain's rules, each citing its atom ids |
| Output | `xray.md` (production table like the lessons'), `xray.json`, sheets, timeline | `doctor.md` (Brain checklist score /100, pass / warn / fail per rule, measured value, why, fix), `doctor.json` |

The Doctor's number is a **Brain checklist score**: the share of the Brain's production rules the draft meets, weighted. It does **not** predict views or virality. Views depend on the idea, the audience and timing, and a rule can be broken on purpose.

### Commands

Always run them with the media venv and `-I` (isolated mode: nothing next to a downloaded video can be imported):

```bash
PY=.venv/bin/python

# X-ray a reel from its URL (downloads into a fresh <out>/source/ folder, saves yt-dlp metadata as source_info.json)
$PY -I tools/xray.py "https://www.instagram.com/p/DfAMeazmN77/" -o /tmp/xray_l10

# X-ray a local file; also label SFX moments with earshot (slower: earshot loads its models)
$PY -I tools/xray.py reel.mp4 -o out/ --listen

# Doctor a draft
$PY -I tools/doctor.py draft.mp4 --format reel30 --niche gym -o out/doctor_draft
```

`xray.py` options: `--listen` (earshot labels), `--whisper-model small|medium` (default `small`), `--lang en|hi`, `--transcript words.json` (reuse a `transcribe.py` transcript), `--meta info.json` (yt-dlp `-j` metadata for a local file; otherwise `<video>.info.json` or a `meta.json` next to the video is used if it is yt-dlp output), `--no-ocr`, `--no-faces`, `--text-fps 2`, `--cookies cookies.txt` (login-walled posts).

`doctor.py` options: `--format reel30|reel60|reel90|yt-short|yt-long` (guessed from length and aspect if left out), `--niche gym|tech|gaming|travel`, `--listen`, `--reuse-xray DIR` (score an existing X-ray without re-measuring), `--whisper-model`, `--lang`.

Speed on this 4-core container: an 85 s talking reel takes about 6 min (whisper `small` ~2.3 min, text/face sampling ~2 min, frames ~1 min); a 15–18 s silent edit about 45 s.

### Setup (fresh container)

1. `tools/setup_audio_tools.sh` (media venv: faster-whisper, yt-dlp, OpenCV contrib headless, numpy; earshot for `--listen`).
2. `tools/setup_xray.sh` adds matplotlib, MediaPipe (installed with `--no-deps` so it does not replace the headless OpenCV), the EGL/GLES system libraries MediaPipe needs, and four model files into `~/sm-tools/models/xray/`:

| Model | Used for | Licence (as listed by the source; not re-checked here) |
|---|---|---|
| OpenCV Zoo PP-OCRv3 DB text detector (2.4 MB) | where text is on screen | Apache-2.0 |
| OpenCV Zoo CRNN EN text recogniser (34 MB) | rough OCR (lowercase, no spaces) | Apache-2.0 |
| OpenCV Zoo YuNet face detector (0.2 MB) | face presence if MediaPipe is missing | MIT |
| MediaPipe face landmarker (3.7 MB) | eyes / mouth / head pose for the face check | Apache-2.0 |

Tesseract is not installed and not needed. If MediaPipe cannot load, the face check falls back to YuNet (presence only) and the Doctor marks it **manual**.

### What the X-ray measures

| Area | How | Notes |
|---|---|---|
| Meta | ffprobe + yt-dlp metadata | creator, caption, likes / comments / views when the platform exposes them, duration, size, fps, HDR |
| Transcript | faster-whisper (CPU int8, VAD, word timestamps) | words, first word time, words said in 0–3 s, wpm over active speech and over the whole video, pauses ≥ 0.5 s |
| Visual changes | ffmpeg scene score per frame (the number `select='gt(scene,X)'` uses) | events > 0.08 (frames within 0.2 s merged; the raw frame count is reported too, as Lesson 10 counted), hard changes > 0.25 |
| Full-frame vs overlay | 8×8 grid of frame differences at each event | full-frame = score ≥ 0.25, or ≥ 0.15 with ≥ 90% of the grid changed; the rest = overlay / partial (cards, captions entering, layout swaps) |
| Cut kinds | ORB feature match across each full-frame cut | punch-in / punch-out (same framing scaled), jump cut (same framing), new shot |
| Text on screen | DB text detector at 2 samples/s + rough CRNN OCR | "overlay" text = fixed on screen between samples (moving scene text such as signs or shoe stripes is ignored); caption-scale = ≥ 2.2% of the frame height; position bands and Reels UI zones (top 13%, bottom 18%, right rail) |
| Changes incl. text | scene events + caption / label / counter changes (OCR-debounced) | the cadence the Doctor scores |
| Faces | MediaPipe face landmarker blendshapes + head pose at 2 samples/s | flags eyes closed / half-closed, mouth open / wide, tongue, awkward angle; each flag gets a context (opening, closing, held still, animated still, in motion); crops in `faces_flagged.png` |
| Camera / motion | LK optical flow + RANSAC partial-affine fit per frame; Farneback flow energy | zoom / pan moves per shot; easing from the cumulative displacement vs a straight line (chord deviation ≤ 0.04 = constant speed / linear, ≥ 0.07 = eased, with ease-in / ease-out / in-out from the speed by thirds) |
| Grade | per frame | mean luma and saturation on the ffmpeg `signalstats` scale (YAVG, SATAVG) and full range, contrast (luma SD), blacks / whites, warmth (R−B), 6-colour k-means palette |
| Loudness | ffmpeg `ebur128=peak=true` | integrated LUFS, loudness range, true peak, momentary curve |
| Silences / dropouts | 100 ms windows ≥ 25 dB under the median (the Brain's dead-air measure) + ffmpeg `silencedetect` −40 dB / 0.25 s | |
| Music vs voice | voice level (word spans) vs the level in the pauses | "voice over a bed ~N dB under the voice", or no bed; pulse / BPM from onset autocorrelation |
| SFX / hits | spectral-flux onsets with ≥ 9 dB jump | transients outside speech are the SFX candidates; at each visual change: is there a transient within ±0.12 s, against the chance rate. With `--listen`, earshot's labels (pop, whoosh, hit …) are attached |
| Ending | first vs last frame correlation + colour histogram | loops to frame 1 / same scene / no loop; ends on black |

Files: `meta.json`, `transcript.json` + `transcript.txt`, `xray.json`, `xray.md`, `contact_sheet.png` (one frame per shot), `changes_sheet.png` (frame after each visual change), `timeline.png` (scene score, text, faces, loudness, transients, camera, grade), `faces_flagged.png`, `earshot_timeline.json` (with `--listen`).

### The Doctor's rules

Weights in brackets; pass = full, warn = half, fail = 0. Rules marked n/a (e.g. sound on a silent export), manual or info are left out of the score, and `doctor.md` says how many points were scored.

| Rule | Pass when | Brain atoms |
|---|---|---|
| Context in the first 2–3 s (15) | overlay text and / or the first word within ~1 s, every channel the video has within 3 s (yt-long: 5 s / 20 s) | `hook-context-first-words`, `hook-window-short-vs-long`, `hook-no-intro-payoff-first`, `hook-one-mississippi` |
| Something new every 1.2–2.5 s (15) | mean gap between changes (cuts, overlays, caption / label swaps) in range and no stretch over 4 s (yt-long 2.5–4.5 s, 8 s) | `edit-change-every-1-5-2-5s`, `edit-graphic-yap-overlay-2s`, `edit-trained-rhythm-break` (+ `edit-long-form-talking-pace`) |
| On-screen text / captions (10) | talking: caption-scale text during ≥ 60% of the speech; no voice: a hook text in the first 3 s and labels | `text-captions-on-yaps`, `hook-context-first-words`, `l10-plain-shadow-captions`, `text-word-by-word-highlight` |
| Text clear of the Reels UI (8) | ≤ 5% of caption samples touch the top 13%, bottom 18% or right rail | `text-safe-zone`, `growth-format-specs` |
| No dead air (8) | no gap > 0.7 s and < 2.5% dead 100 ms windows; a ~0.5 s dropout after the punchline is allowed | `edit-cut-breaths-no-dead-air`, `l10-dropout-after-punchline` |
| A sound on visual events (8) | ≥ 50% of visual changes have a transient and clearly above chance; with `--listen`, ≥ 40% have an earshot-labelled non-voice sound. Speech-heavy videos without `--listen` → manual | `sound-sfx-every-event`, `sound-sfx-meaning-map`, `sound-bass-hit-text-pop` |
| Loudness (8) | −15 to −13 LUFS integrated | `sound-loudness-minus-14` |
| True peak (4) | ≤ −1 dBTP | `sound-loudness-minus-14` |
| Music bed under the voice (4) | a bed in the pauses 6–18 dB under the voice | `sound-quiet-bed-throughout`, `sound-music-by-section` |
| Length (8) | reel30 7–35 s (vibe gym/travel reel without voice: 7–20 s), reel60 20–65, reel90 45–95, yt-short 10–60, yt-long ≥ 3 min | `edit-length-by-type`, `growth-format-specs` |
| Export spec (4) | 1080×1920, 30 (or 60) fps, SDR; yt-long 16:9 ≥ 1080p | `growth-format-specs` |
| Face check (6) | no flagged expression on the opening / closing frames, held stills or animated photos (flags while talking in motion are listed, not scored) | `edit-face-check` (SYSTEM_PROMPT face-check rule) |
| Eased moves, nothing linear (6) | no zoom / pan at constant speed | `fx-nothing-linear`, `fx-ease-out-entrances`, `fx-spring-ui`, `fx-khandala-linear-moves` |
| Ending (6) | loops to frame 1, or a CTA in the last 8 s, or a cut to black | `edit-loop-to-frame-1`, `growth-comment-keyword-cta`, `tr-cut-to-black-thud` |
| Punch-ins on a talking head (4, talking videos only) | ≥ 3 punch-ins / zoom moves a minute or camera shots ≤ 4 s | `fx-subtle-punch-in`, `fx-big-punch-in`, `edit-axial-jump-cuts` |
| Grade vs the niche look (info) | a reading of warmth / contrast / saturation against the niche recipe | `colour-gym-grade`, `colour-golden-hour-grade`, `colour-dark-matte-warm-key`, `l10-moody-grade-recipe`, `colour-neon-high-contrast` |

The Doctor reads atom titles and sources from `brain/data/atoms.json` and `atoms_L10.json` at run time and warns if a cited id is missing, so the citations stay honest when the Brain changes.

### Limits (read before trusting a number)

- **Not a predictor.** No model here has seen view counts. The score is a checklist.
- **SFX vs speech.** Without `--listen`, transients from hard consonants and drums look like SFX. The Doctor compares against the chance rate and marks the SFX rule manual on talking videos.
- **Overlay vs cut.** Full-frame vs overlay is a pixel heuristic; a punch-in combined with a card entering can land either side. The 0.25 threshold matches Lesson 10's method.
- **Text.** OCR is rough (lowercase, no spaces, ~2 samples/s). A sign in a locked-off shot counts as overlay text. Text changes have 0.5 s resolution.
- **Faces.** Blendshape thresholds are heuristics (blink ≥ 0.5, jawOpen ≥ 0.22). Talking frames are naturally mid-word; the rule only scores held, opening and closing frames. Small, profile or upside-down faces are often missed.
- **Motion.** The camera fit follows the dominant motion, which can be a big overlay. A smooth filmed pan at constant speed also reads as "linear".
- **Silent exports.** Sound rules are n/a; re-run on the final export with music.
