#!/usr/bin/env bash
# Re-creates what Reel X-ray (xray.py) and Reel Doctor (doctor.py) need in a fresh cloud container.
# Free, local, CPU-only. Assumes the media venv from setup_audio_tools.sh (faster-whisper, yt-dlp, OpenCV, numpy).
set -euo pipefail
TOOLS=${TOOLS:-~/sm-tools}
M=$TOOLS/media
PIP="$M/.venv/bin/pip"
# matplotlib draws timeline.png; mediapipe (Apache-2.0) gives the face check its eye / mouth readings.
# mediapipe goes in with --no-deps: its own deps would pull the non-headless OpenCV over the headless one.
"$PIP" -q install matplotlib
"$PIP" -q install --no-deps mediapipe absl-py
# MediaPipe's native library needs EGL / GLES even on CPU
if ! ldconfig -p | grep -q libEGL.so.1; then apt-get install -y --no-install-recommends libegl1 libgles2; fi
# model files (all free): OpenCV zoo text detector + CRNN reader + YuNet face detector, MediaPipe face landmarker
D=$M/models/xray; mkdir -p "$D"; cd "$D"
Z=https://media.githubusercontent.com/media/opencv/opencv_zoo/main/models
[ -s text_detection_en_ppocrv3_2023may.onnx ] || curl -sSL -o text_detection_en_ppocrv3_2023may.onnx $Z/text_detection_ppocr/text_detection_en_ppocrv3_2023may.onnx
[ -s text_recognition_CRNN_EN_2021sep.onnx ] || curl -sSL -o text_recognition_CRNN_EN_2021sep.onnx $Z/text_recognition_crnn/text_recognition_CRNN_EN_2021sep.onnx
[ -s face_detection_yunet_2023mar.onnx ] || curl -sSL -o face_detection_yunet_2023mar.onnx $Z/face_detection_yunet/face_detection_yunet_2023mar.onnx
[ -s face_landmarker.task ] || curl -sSL -o face_landmarker.task https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task
ls -la "$D"
echo "xray ready: $M/.venv/bin/python -I tools/xray.py <video|url>   doctor: $M/.venv/bin/python -I tools/doctor.py <draft>"
