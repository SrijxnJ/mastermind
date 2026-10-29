#!/usr/bin/env bash
# Re-creates the free video-editing tools in a fresh cloud session (CPU only, no API keys, no usage limits).
# Safe to run again: venvs and models that already exist are reused; pip only fills in what's missing.
# Licences and versions: tools/FREE_TOOLS.md
#
#   $TOOLS/cut     auto-editor 29.3.1 (Unlicense)                     -> tools/autocut.sh       (~65 MB)
#   $TOOLS/vision  mediapipe 1.1.1 (Apache-2.0), rembg 2.0.86 (MIT),
#                  onnxruntime (MIT), opencv-contrib (Apache-2.0)      -> tools/text_behind.py
#                  numpy                                               -> tools/luts.py          (~1.1 GB incl. models)
#   models         MediaPipe selfie_segmenter (0.25 MB), selfie_multiclass_256x256 (16 MB), rembg u2netp (4.6 MB)
#
# Does not touch $TOOLS/media/.venv or $TOOLS/earshot (those belong to tools/setup_audio_tools.sh).
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TOOLS=${TOOLS:-~/sm-tools}
mkdir -p "$TOOLS"

# ---------------------------------------------------------------- auto-editor (silence / dead-air removal)
C="$TOOLS/cut"
[ -x "$C/bin/python" ] || python3 -m venv "$C"
"$C/bin/python" -m pip -q install --upgrade pip
# the wheel is a thin Python shim; on install it downloads the matching static binary from the
# project's GitHub release (github.com/WyattBlue/auto-editor/releases/29.3.1, ~41 MB)
"$C/bin/python" -m pip -q install "auto-editor==29.3.1"
echo "auto-editor $("$C/bin/auto-editor" --version) ready:  $SCRIPT_DIR/autocut.sh <video> [-m 0.15] [-l]"

# ---------------------------------------------------------------- person segmentation + LUT builder
V="$TOOLS/vision"
[ -x "$V/bin/python" ] || python3 -m venv "$V"
"$V/bin/python" -m pip -q install --upgrade pip
"$V/bin/python" -m pip -q install "mediapipe==1.1.1" "rembg[cpu]==2.0.86"
# (pulls onnxruntime, opencv-contrib-python, numpy, pillow, scipy, scikit-image, pymatting/numba)

M="$V/models"; mkdir -p "$M"
fetch(){ # url file sha256
  if [ -f "$M/$2" ] && echo "$3  $M/$2" | sha256sum -c --quiet - 2>/dev/null; then return; fi
  curl -sSfL -o "$M/$2.part" "$1"
  echo "$3  $M/$2.part" | sha256sum -c --quiet - || { echo "checksum mismatch for $2 (upstream changed?)" >&2; rm -f "$M/$2.part"; exit 1; }
  mv "$M/$2.part" "$M/$2"
}
fetch https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_segmenter/float16/latest/selfie_segmenter.tflite \
      selfie_segmenter.tflite 191ac9529ae506ee0beefa6b2c945a172dab9d07d1e802a290a4e4038226658b
fetch https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_multiclass_256x256/float32/latest/selfie_multiclass_256x256.tflite \
      selfie_multiclass_256x256.tflite c6748b1253a99067ef71f7e26ca71096cd449baefa8f101900ea23016507e0e0
# rembg fetches its own model on first use; do it now so renders work offline (lands in $M/models/u2netp/)
U2NET_HOME="$M" "$V/bin/python" -I -c "from rembg import new_session; new_session('u2netp')" 2>/dev/null
echo "309c8469258dda742793dce0ebea8e6dd393174f89934733ecc8b14c76f4ddd8  $M/models/u2netp/u2netp.onnx" | sha256sum -c --quiet - \
  || echo "warning: u2netp checksum differs from the one recorded in FREE_TOOLS.md" >&2

"$V/bin/python" -I -c "import mediapipe, rembg, onnxruntime, cv2, numpy; print('vision ok: mediapipe', mediapipe.__version__, '| onnxruntime', onnxruntime.__version__, '| opencv', cv2.__version__, '| guided filter', hasattr(cv2, 'ximgproc'))"
echo "text behind head:  $V/bin/python -I $SCRIPT_DIR/text_behind.py <video> --text '75 KG' --start 0.3 --end 3.3"
echo "grade LUTs:        $V/bin/python -I $SCRIPT_DIR/luts.py   (writes library/luts/*.cube)"

# fonts used by text_behind.py live in tools/fonts/ (SIL OFL 1.1), committed with the project - nothing to fetch
