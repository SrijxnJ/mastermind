#!/usr/bin/env bash
# autocut.sh - remove silences / dead air from a talking clip (free replacement for the paid ReCut app).
# Engine: auto-editor (Unlicense, github.com/WyattBlue/auto-editor), installed by tools/setup_free_tools.sh
# into its own venv at $TOOLS/cut. CPU only, fully local.
#
# Usage:
#   autocut.sh INPUT [options]
#     -o, --output FILE      output video (default: INPUT_autocut.mp4 next to the input)
#     -m, --margin SEC       padding kept around speech, seconds (default 0.15). Raise to 0.25-0.3 for a calmer cut,
#                            lower to 0.08 for a "jump-cut every breath" Shorts pace.
#     -t, --threshold N      loudness threshold 0-1 (default 0.04 = 4%). Raise (0.06-0.08) for noisy rooms/gyms,
#                            lower (0.02) for quiet voices.
#     -s, --silent-speed X   instead of cutting silences, play them X times faster (e.g. 6). Default: cut.
#     -l, --list             also write an edit list: INPUT_autocut.edits.csv (kept/cut ranges in seconds)
#                            + INPUT_autocut.v3 (auto-editor JSON timeline; re-render with: auto-editor X.v3)
#     -x, --xml TYPE         also write an NLE timeline: premiere | resolve | final-cut-pro | shotcut | kdenlive
#     -p, --preview          print stats only (before/after length, number of cuts), write nothing
#
# Examples:
#   tools/autocut.sh talk.mp4                         # talk_autocut.mp4, 0.15 s margin
#   tools/autocut.sh talk.mp4 -m 0.25 -t 0.06 -l      # calmer cut, noisy room, plus edit list
#   tools/autocut.sh talk.mp4 -x resolve              # also a DaVinci Resolve timeline to fine-tune by hand
set -euo pipefail

TOOLS=${TOOLS:-~/sm-tools}
AE="$TOOLS/cut/bin/auto-editor"
if [ ! -x "$AE" ]; then
  echo "auto-editor not found at $AE - run tools/setup_free_tools.sh first" >&2; exit 1
fi

usage(){ sed -n '2,22p' "$0" | sed 's/^# \{0,1\}//'; exit "${1:-0}"; }
[ $# -ge 1 ] || usage 1
case "$1" in -h|--help) usage 0;; esac

IN=$1; shift
[ -f "$IN" ] || { echo "no such file: $IN" >&2; exit 1; }
IN_ABS=$(readlink -f "$IN")
BASE="${IN_ABS%.*}"
OUT="${BASE}_autocut.mp4"
MARGIN=0.15; THRESH=0.04; SPEED=""; LIST=0; XML=""; PREVIEW=0

while [ $# -gt 0 ]; do
  case "$1" in
    -o|--output) OUT=$2; shift 2;;
    -m|--margin) MARGIN=$2; shift 2;;
    -t|--threshold) THRESH=$2; shift 2;;
    -s|--silent-speed) SPEED=$2; shift 2;;
    -l|--list) LIST=1; shift;;
    -x|--xml) XML=$2; shift 2;;
    -p|--preview) PREVIEW=1; shift;;
    -h|--help) usage 0;;
    *) echo "unknown option: $1" >&2; usage 1;;
  esac
done

OUT_ABS=$(readlink -f "$OUT")
OBASE="${OUT_ABS%.*}"
COMMON=(--edit "audio:threshold=${THRESH}" --margin "${MARGIN}s" --no-open --progress none)
[ -n "$SPEED" ] && COMMON+=(--when-silent "speed:${SPEED}")

dur(){ ffprobe -v error -show_entries format=duration -of csv=p=0 "$1"; }

if [ "$PREVIEW" = 1 ]; then
  "$AE" "$IN_ABS" "${COMMON[@]}" --stats
  exit 0
fi

"$AE" "$IN_ABS" "${COMMON[@]}" -o "$OUT_ABS"

if [ "$LIST" = 1 ]; then
  "$AE" "$IN_ABS" "${COMMON[@]}" --export v3 -o "${OBASE}.v3"
  "$AE" "$IN_ABS" "${COMMON[@]}" --export v1 -o "${OBASE}.v1"
  # v1 = [start_frame, end_frame, speed] chunks at the v3 timebase -> readable CSV in seconds
  python3 -I - "${OBASE}.v1" "${OBASE}.v3" "${OBASE}.edits.csv" <<'PY'
import json, sys
from fractions import Fraction
v1 = json.load(open(sys.argv[1])); v3 = json.load(open(sys.argv[2]))
tb = Fraction(v3.get("timebase", "30/1"))
rows, out_t = [], Fraction(0)
for a, b, sp in v1["chunks"]:
    s, e = Fraction(a) / tb, Fraction(b) / tb
    if sp >= 99999:
        act, od = "cut", Fraction(0)
    elif sp == 1:
        act, od = "keep", e - s
    else:
        act, od = f"speed x{sp:g}", (e - s) / Fraction(sp).limit_denominator(1000)
    rows.append((act, float(s), float(e), float(e - s), float(out_t), float(out_t + od)))
    out_t += od
with open(sys.argv[3], "w") as f:
    f.write("action,src_start_s,src_end_s,src_dur_s,out_start_s,out_end_s\n")
    for r in rows:
        f.write("%s,%.3f,%.3f,%.3f,%.3f,%.3f\n" % r)
PY
  rm -f "${OBASE}.v1"
  echo "edit list: ${OBASE}.edits.csv  (auto-editor timeline: ${OBASE}.v3)"
fi

if [ -n "$XML" ]; then
  case "$XML" in
    premiere) EXT=xml;; resolve|final-cut-pro) EXT=fcpxml;; shotcut) EXT=mlt;; kdenlive) EXT=kdenlive;;
    *) echo "unknown --xml type: $XML" >&2; exit 1;;
  esac
  "$AE" "$IN_ABS" "${COMMON[@]}" --export "$XML" -o "${OBASE}_${XML}.${EXT}"
  echo "timeline: ${OBASE}_${XML}.${EXT}"
fi

B=$(dur "$IN_ABS"); A=$(dur "$OUT_ABS")
python3 -I -c "b,a=$B,$A; print(f'before {b:.2f}s -> after {a:.2f}s  (removed {b-a:.2f}s, {100*(b-a)/b:.1f}%)')"
echo "output: $OUT_ABS"
