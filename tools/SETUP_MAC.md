# Setting up on Srijan's Mac

Install only what a task needs, when it first needs it.

## Base (needed for the Brain search and the Master Mind page)
```bash
brew install python ffmpeg            # Homebrew: https://brew.sh
cd ~/Documents/social-media-manager-srijan
python3 -m venv .venv && source .venv/bin/activate
pip install fastembed numpy pillow
python mastermind/build.py   # rebuilds index.html + wiki
```
Open `mastermind/index.html` in Chrome.

## Add when needed
| For | Install |
|---|---|
| Transcribing reels / voice notes | `pip install faster-whisper "yt-dlp[default]"` |
| Reel X-ray + Doctor | `pip install opencv-contrib-python-headless mediapipe matplotlib` |
| Silence cutting | `pip install auto-editor` |
| Text behind head | `pip install mediapipe rembg onnxruntime` |
| Voice in Srijan's voice | `pip install chatterbox-tts` (Apple Silicon: uses the Mac's GPU via MPS) |
| Motion graphics | `npx -y hyperframes@latest` (needs Node) |

The Linux setup scripts in this folder (`setup_*.sh`) were for the old cloud machine; on the Mac use the table above. Paths like `~/sm-tools/...` inside older scripts point to the cloud machine; replace with this folder's `.venv`.

## Installed (2026-10-28, Srijan's MacBook Air M1, macOS 26.6.2)

Run everything from `~/Documents/social-media-manager-srijan` (the project root). Brew lives in `/opt/homebrew`; put it on PATH once with `echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile`.

| What | Where | Versions |
|---|---|---|
| Homebrew 7.0.11 | `/opt/homebrew` | python@3.11 (3.11.18), ffmpeg 9.0.2, node 26.12.1, git |
| Main Python env (Brain, Master Mind, xray, doctor, text_behind, luts, transcribe, autocut) | `.venv/` (python 3.11) | fastembed 0.9.1, numpy 2.4.6, pillow 13.0.0, faster-whisper 1.2.1, yt-dlp 2026.10.26, opencv-contrib-python-headless 5.0.0.93, mediapipe 1.2.0, matplotlib 3.11.2, librosa 0.11.0, auto-editor 29.3.1, rembg 2.0.86, onnxruntime 1.31.1 |
| earshot (audio listening) | `~/sm-tools/earshot/` (git clone) + `~/sm-tools/earshot/.venv` | earshot 0.4.0, torch 2.14.1; run with `EARSHOT_HOME=~/sm-tools/earshot ~/sm-tools/earshot/.venv/bin/python -m earshot …`; models fetched by `earshot doctor --fetch` |
| Chatterbox voice (Srijan's voice only) | `~/sm-tools/voice/.venv` (python 3.11) | chatterbox-tts 0.1.7, torch 2.6.0, setuptools<81 (resemble-perth needs `pkg_resources`), uses the Mac GPU (MPS); `tools/voice.py` picks mps automatically; model weights cached in `~/.cache/huggingface` |
| HyperFrames 0.8.212 | not installed, run via `npx -y hyperframes@latest …` (uses brew node) | `doctor` passes: ffmpeg, ffprobe, Chrome; optional whisper-cpp / Kokoro / MusicGen / Docker not installed |
| real-sfx library | `.claude/skills/real-sfx/config.json` → library `main` = `library/sfx` (2,147 sounds, indexed in `library_index.json`) | run its scripts with `/usr/bin/python3` or `.venv/bin/python` |
| Model folders (created lazily) | `~/sm-tools/models/whisper`, `~/sm-tools/models/xray`, `~/sm-tools/models/vision` | faster-whisper, X-ray and rembg/MediaPipe models download here on first use |
| Motion-prompt collection (awesome-opus5-5-videos, MIT) | `library/motion-prompts/` (703 prompts + `data/videos.json` + `search.py`) | reference only, no install; refresh by re-cloning to `~/sm-tools/incoming/` and rsyncing |
| yt-dlp config | `~/.config/yt-dlp/config` | `--js-runtimes node` |
| ig-* skill inputs | `~/.claude/instagram/voice.md`, `~/.claude/instagram/swipe.md` | copies of `brain/voice/ig-voice.md` and `brain/research/viral/swipe_all.md`; re-copy after editing the originals |

Not installed on purpose: Docker, whisper-cpp, Kokoro, MusicGen (HyperFrames optional extras), vidIQ.
| Public export | `tools/export_public.py` → `github/mastermind/` (allowlist + scrub + rebuild + `docs/index.html` for GitHub Pages); overrides in `tools/public/` | rerun before every push |
