"""Stage (trim) every candidate, then let earshot judge it. Writes STAGE/judged.json.
Usage: EARSHOT_HOME=... <earshot venv python> -I judge.py POOL_JSON SYNTH_DIR STAGE_DIR"""
import json, os, subprocess, sys, glob
import numpy as np
import soundfile as sf

POOL, SYNTH, STAGE = sys.argv[1:4]
SR = 44100
LONG = {"riser", "downlifter", "crowd-cheer-applause", "heartbeat", "typing", "foley", "sci-fi"}
NORANK = len(sys.argv) > 4 and sys.argv[4] == "norank"
SKIP = set(json.load(open(sys.argv[5]))) if len(sys.argv) > 5 else set()
QUERY = {
    "whoosh": "a whoosh of air passing by", "swoosh-fast": "a fast swoosh swish",
    "pop": "a short bubble pop", "click-ui": "a mouse click, user interface button click",
    "keyboard": "a single mechanical keyboard key press", "typing": "typing on a keyboard",
    "hit-impact": "a punch hit impact", "bass-drop-boom": "a deep bass boom",
    "riser": "a rising sweep riser building tension", "downlifter": "a falling sweep, downlifter",
    "glitch": "a digital glitch", "camera-shutter": "a camera shutter click",
    "notification-ding": "a notification ding", "chime-success": "a bright success chime",
    "record-scratch": "a vinyl record scratch", "rewind-tape-stop": "a tape stop, music slowing down",
    "crowd-cheer-applause": "a crowd applauding and cheering", "gym": "heavy metal weights clanking in a gym",
    "gaming": "an 8-bit video game coin or power-up sound", "cash-register": "a cash register cha-ching with coins",
    "heartbeat": "a heartbeat",
}


def load(path):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32).reshape(-1, 2).astype(np.float64)


def stage(x, cat):
    mono = np.abs(x).max(1)
    pk = mono.max()
    if pk <= 0:
        return None, {}
    info = {"src_peak_db": round(20 * np.log10(pk), 2), "src_dur_s": round(len(x) / SR, 3)}
    # clipping in the source: runs of >=3 samples at the max magnitude near full scale
    near = mono >= 0.999 * pk
    runs = np.sum(near[2:] & near[1:-1] & near[:-2])
    info["src_clip_runs"] = int(runs) if pk > 0.98 else 0
    # 10 ms envelope
    w = int(0.01 * SR)
    nfr = len(mono) // w
    env = np.array([mono[i * w:(i + 1) * w].max() for i in range(nfr)]) + 1e-12
    env_db = 20 * np.log10(env / pk)
    above = np.where(env_db > -45)[0]
    if not len(above):
        return None, info
    s, e = above[0] * w, min(len(x), (above[-1] + 1) * w + int(0.05 * SR))
    s = max(0, s - int(0.004 * SR))
    maxlen = int((10.0 if cat in LONG else 4.0) * SR)
    y = x[s:e]
    truncated = False
    if len(y) > maxlen:
        truncated = True
        if cat == "riser":  # keep the build into the loudest moment
            pk_i = int(np.argmax(np.abs(y).max(1)))
            end = min(len(y), pk_i + int(0.3 * SR))
            y = y[max(0, end - maxlen):end]
        else:
            y = y[:maxlen]
    y = y.copy()
    fi = int(0.003 * SR)
    y[:fi] *= np.linspace(0, 1, fi)[:, None]
    fo = int((0.25 if truncated else 0.02) * SR)
    fo = min(fo, len(y) // 3)
    y[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
    # noise floor: quietest 10% of 20 ms windows during the first 90% (relative to peak), only meaningful for long files
    w2 = int(0.02 * SR)
    seg = np.abs(y).max(1)
    frames = np.array([np.sqrt(np.mean(seg[i:i + w2] ** 2)) for i in range(0, max(1, len(seg) - w2), w2)]) + 1e-12
    info["floor_db_re_peak"] = round(float(20 * np.log10(np.percentile(frames, 10) / pk)), 1)
    info["truncated"] = truncated
    return y, info


pool = json.load(open(POOL))
syn = json.load(open(os.path.join(SYNTH, "synth_meta.json")))
for p, m in syn.items():
    pool.setdefault(m["category"], []).append({
        "rel": "inhouse/" + m["category"] + "/" + os.path.basename(p), "path": p, "licence": "CC0-1.0",
        "author": "Srijan media library (in-house DSP" + (", from CC0 Kenney recordings" if m["sources"] else "") + ")",
        "source_url": "in-house: library/tools/synth.py", "source_title": m["description"],
        "derived_from": [os.path.basename(s) for s in m["sources"]]})

from earshot import api  # noqa: E402

out = {}
for cat, items in pool.items():
    os.makedirs(os.path.join(STAGE, cat), exist_ok=True)
    staged = []
    for i, it in enumerate(items):
        if it["path"] in SKIP:
            continue
        try:
            x = load(it["path"])
        except Exception as e:
            print("load fail", it["rel"], e, file=sys.stderr)
            continue
        y, info = stage(x, cat)
        if y is None:
            continue
        sp = os.path.join(STAGE, cat, f"{i:04d}.wav")
        sf.write(sp, y.astype(np.float32), SR, subtype="PCM_24")
        it2 = dict(it, staged=sp, staged_dur_s=round(len(y) / SR, 3), **info)
        try:
            chk = api.sfx_check(sp)
        except Exception as e:  # noqa
            chk = {"ok": None, "summary": f"check failed: {e}", "warnings": []}
        it2["check_ok"] = chk.get("ok")
        it2["check_summary"] = chk.get("summary")
        it2["check_codes"] = [w["code"] for w in chk.get("warnings", [])]
        staged.append(it2)
    if not staged:
        continue
    if NORANK or cat not in QUERY:
        out[cat] = staged
        print(cat, len(staged), file=sys.stderr, flush=True)
        continue
    r = api.rank([s["staged"] for s in staged], QUERY[cat])
    by = {x["path"]: x for x in r["results"]}
    for s in staged:
        rr = by.get(s["staged"]) or by.get(os.path.abspath(s["staged"]))
        if rr:
            s["z"], s["verdict"], s["sounds_most_like"] = rr["z"], rr["verdict"], rr["sounds_most_like"]
    staged.sort(key=lambda s: -s.get("z", -99))
    out[cat] = staged
    print(cat, len(staged), "| best:", ", ".join(f"{os.path.basename(s['rel'])}({s.get('z')},{s.get('verdict')})" for s in staged[:5]),
          file=sys.stderr, flush=True)
json.dump(out, open(os.path.join(STAGE, "judged.json"), "w"), indent=1)
