#!/usr/bin/env bash
# Re-creates the audio tools in a fresh cloud session.
# The Claude skills themselves live in .claude/skills (committed), so they load automatically.
# What doesn't survive a new container is earshot's Python environment and models; this script rebuilds them.
#   - earshot (MIT, github.com/Leonxlnx/earshot): CPU audio "ears", ~1.1 GB of models on first fetch
#   - Real SFX (.claude/skills/real-sfx) only needs python3 + ffmpeg, which the container already has
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TOOLS=${TOOLS:-~/sm-tools}
mkdir -p "$TOOLS"
if [ ! -d "$TOOLS/earshot/.git" ]; then
  GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/Leonxlnx/earshot "$TOOLS/earshot"
fi
cd "$TOOLS/earshot"
[ -d .venv ] || python3 -m venv .venv
.venv/bin/python -m pip -q install torch --index-url https://download.pytorch.org/whl/cpu
.venv/bin/python -m pip -q install -e ".[mcp,llm,dev]"
export EARSHOT_HOME="$TOOLS/earshot"
.venv/bin/python -m earshot doctor --fetch
.venv/bin/python -m earshot doctor
echo "earshot ready:  EARSHOT_HOME=$TOOLS/earshot $TOOLS/earshot/.venv/bin/python -m earshot <command>"

# Media helpers: faster-whisper (word-level transcripts), yt-dlp (downloads), OpenCV contrib (CSRT tracker), fastembed (Master Mind neural links)
M=${TOOLS}/media
mkdir -p "$M"; [ -d "$M/.venv" ] || python3 -m venv "$M/.venv"
"$M/.venv/bin/pip" -q install faster-whisper "yt-dlp[default]" opencv-contrib-python-headless fastembed numpy
# yt-dlp needs a JavaScript runtime to solve YouTube's challenges; Node is preinstalled, so enable it.
mkdir -p "$HOME/.config/yt-dlp" && echo "--js-runtimes node" > "$HOME/.config/yt-dlp/config"
cp "$SCRIPT_DIR/transcribe.py" "$M/transcribe.py"
echo "media tools ready: $M/.venv/bin/python -I $M/transcribe.py <video> [small|medium]"

# Instagram agent skills read their voice file from ~/.claude/instagram/; the master copy lives in the Brain.
mkdir -p "$HOME/.claude/instagram" && cp "$SCRIPT_DIR/../brain/voice/ig-voice.md" "$HOME/.claude/instagram/voice.md"
