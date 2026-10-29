"""Normalise + encode the selected SFX into library/sfx and write library/catalog.json.

Input: the build list made by assemble.py (one item per sound: 'staged' trimmed wav, 'category', 'file' name,
licence/author/source fields, use_when, pairs_with_transition, niches, earshot results).

Per file:
  1. loudnorm pass 1 (EBU R128) on the staged, trimmed wav (sounds < 0.4 s are measured padded to one 400 ms block)
  2. target = min(-16 LUFS, the loudness at which true peak reaches -1.5 dBTP)  -> loudnorm stays in *linear* mode
  3. loudnorm pass 2 (linear=true, measured values), aresample 44.1 kHz, trim padding, MP3 128 kbps CBR (libmp3lame)
  4. re-measure the MP3 (ebur128 peak=true); if true peak > -1.0 dBTP, turn down and re-encode
Usage: python3 -I build_library.py SELECTION_JSON LIBRARY_DIR
"""
import json, os, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor

SEL, LIB = sys.argv[1:3]
TARGET_I, TP_PRE, TP_MAX = -16.0, -1.5, -1.0


def run(args):
    return subprocess.run(args, capture_output=True, text=True)


def dur(path):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path]).stdout.strip())


def loudnorm_measure(path, d):
    pad = "highpass=f=20," + (f"apad=whole_dur={max(0.45, d)}," if d < 0.45 else "")
    r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af",
             f"{pad}loudnorm=I={TARGET_I}:TP={TP_PRE}:LRA=20:print_format=json", "-f", "null", "-"])
    js = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
    return {k: float(js[k]) for k in ("input_i", "input_tp", "input_lra", "input_thresh", "target_offset")}


def ebur(path, d):
    pad = f"apad=whole_dur={max(0.45, d)}," if d < 0.45 else ""
    r = run(["ffmpeg", "-hide_banner", "-nostats", "-i", path, "-af", f"{pad}ebur128=peak=true", "-f", "null", "-"])
    s = r.stderr[r.stderr.rindex("Summary:"):]
    i = float(re.search(r"I:\s+(-?[\d.]+|-inf) LUFS", s).group(1))
    tp = float(re.search(r"Peak:\s+(-?[\d.]+|-inf) dBFS", s).group(1))
    return i, tp


def encode(src, dst, m, target, d, extra_gain_db=0.0):
    pad = "highpass=f=20," + (f"apad=whole_dur={max(0.45, d)}," if d < 0.45 else "")
    ln = (f"loudnorm=I={target:.2f}:TP={TP_PRE}:LRA=20:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:linear=true:print_format=json")
    af = f"{pad}{ln},aresample=44100,atrim=0:{d:.4f},volume={extra_gain_db}dB"
    r = run(["ffmpeg", "-hide_banner", "-nostats", "-y", "-i", src, "-af", af, "-ac", "2", "-c:a", "libmp3lame",
             "-b:a", "128k", "-map_metadata", "-1", dst])
    js = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
    return js.get("normalization_type")


sel = json.load(open(SEL))


def build(it):
    src = it["staged"]
    d = dur(src)
    m = loudnorm_measure(src, d)
    peak_limited_i = m["input_i"] + (TP_PRE - m["input_tp"])  # loudness at which the true peak hits TP_PRE
    target = max(min(TARGET_I, peak_limited_i), -40.0)
    out_dir = os.path.join(LIB, "sfx", it["category"])
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, it["file"])
    gain, ntype = 0.0, None
    for _ in range(4):
        ntype = encode(src, dst, m, target, d, gain)
        i, tp = ebur(dst, dur(dst))
        if tp <= TP_MAX:
            break
        gain -= (tp - TP_MAX) + 0.3
    e = {
        "id": it["id"], "file": os.path.relpath(dst, LIB).replace(os.sep, "/"), "category": it["category"],
        "subtype": it.get("subtype"), "tier": it["tier"], "featured": it["featured"], "featured_rank": it.get("featured_rank"),
        "duration_s": round(dur(dst), 3), "lufs": round(i, 1), "peak_db": round(tp, 1),
        "licence": it["licence"], "source_url": it["source_url"], "author": it["author"], "attribution": it["attribution"],
        "use_when": it["use_when"], "pairs_with_transition": it["pairs_with_transition"], "niches": it["niches"],
        "source_file": it.get("source_file"), "source_title": it.get("source_title"), "derived_from": it.get("derived_from"),
        "trimmed_from_s": it.get("trimmed_from_s"),
        "normalisation": ("loudnorm 2-pass linear, " + ("-16 LUFS target" if target >= TARGET_I - 0.05 else
                          f"peak-limited to {target:.1f} LUFS (true-peak ceiling)") +
                          (f", {gain:.1f} dB extra trim after MP3" if gain else "") + f" [{ntype}]"),
        "earshot": {"query_z": it.get("z"), "verdict": it.get("verdict"), "sounds_most_like": it.get("sounds_most_like"),
                    "audit": it.get("check_summary")},
    }
    return e


with ThreadPoolExecutor(max_workers=int(os.environ.get("JOBS", "4"))) as ex:
    catalog = list(ex.map(build, sel))
catalog.sort(key=lambda e: (e["category"], not e["featured"], e.get("featured_rank") or 999, e["file"]))
json.dump(catalog, open(os.path.join(LIB, "catalog.json"), "w"), indent=1, ensure_ascii=False)
print(len(catalog), "sounds;", sum(e["peak_db"] > -1.0 for e in catalog), "over -1 dBTP", file=sys.stderr)
