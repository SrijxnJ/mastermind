"""Srijan's voice tool: prepare his recordings, measure how he sounds, and speak new lines in his voice.

Runs locally on the Mac GPU (MPS) when available, else CPU, with Chatterbox Multilingual (MIT, Resemble AI). Every generated file carries
Chatterbox's inaudible Perth watermark, which marks it as AI-generated. Use it only for Srijan's own
voice, with his consent.

  V=~/sm-tools/voice/.venv/bin/python
  $V -I tools/voice.py prep  voice_note.m4a [more files…]          # → brain/voice/ref/ (clean WAVs + best reference clip)
  $V -I tools/voice.py analyze brain/voice/ref/clean_*.wav           # → brain/voice/profile.json + profile.md
  $V -I tools/voice.py say "Bro. Seventy kilo." --lang en --mood hype --out hook.wav
  $V -I tools/voice.py say "भाई आज leg day है" --lang hi --mood deadpan

Moods map to Chatterbox's two dials: exaggeration (energy) and cfg_weight (lower = faster, looser pacing).
Hindi lines read best in Devanagari; English words can stay in Latin script inside them.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
VOICE = ROOT / "brain" / "voice"
REF = VOICE / "ref"
OUT = VOICE / "out"
TRANSCRIBE = [str(ROOT.parent / ".venv" / "bin" / "python"), "-I", str(ROOT / "tools" / "transcribe.py")]
MOODS = {  # (exaggeration, cfg_weight, temperature)
    "calm": (0.35, 0.5, 0.7),
    "normal": (0.5, 0.5, 0.8),
    "deadpan": (0.25, 0.6, 0.6),
    "hype": (0.85, 0.3, 0.85),
    "whisper": (0.3, 0.55, 0.7),
}


def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *args], check=True)


def speech_spans(wav, min_len=2.0):
    """Non-silent spans (start, end) in seconds, from ffmpeg silencedetect."""
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(wav), "-af", "silencedetect=n=-38dB:d=0.35", "-f", "null", "-"],
                       capture_output=True, text=True)
    starts, ends = [], []
    for line in r.stderr.splitlines():
        if "silence_start" in line:
            starts.append(float(line.split("silence_start:")[1]))
        elif "silence_end" in line:
            ends.append(float(line.split("silence_end:")[1].split("|")[0]))
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(wav)],
                               capture_output=True, text=True).stdout or 0)
    spans, cur = [], 0.0
    for s, e in zip(starts, ends + [dur]):
        if s - cur >= min_len:
            spans.append((cur, s))
        cur = e
    if dur - cur >= min_len:
        spans.append((cur, dur))
    return spans, dur


def prep(files):
    REF.mkdir(parents=True, exist_ok=True)
    cleaned = []
    for i, f in enumerate(files, 1):
        out = REF / f"clean_{i:02d}.wav"
        # mono 24 kHz, rumble cut, gentle denoise, loudness to -20 LUFS (headroom for cloning)
        ffmpeg("-i", f, "-vn", "-ac", "1", "-ar", "24000",
               "-af", "highpass=f=70,afftdn=nf=-25,loudnorm=I=-20:TP=-2:LRA=11", str(out))
        cleaned.append(out)
        print(f"cleaned {f} → {out.name}")
    # best reference: the longest continuous speech span, trimmed to 8–15 s
    best = None
    for c in cleaned:
        spans, _ = speech_spans(c)
        for s, e in spans:
            length = min(e - s, 15.0)
            if length >= 6 and (best is None or length > best[3]):
                best = (c, s, s + length, length)
    if not best:
        sys.exit("No continuous speech of 6 s or more found. Record a longer, steadier take.")
    ffmpeg("-ss", f"{best[1]:.2f}", "-to", f"{best[2]:.2f}", "-i", str(best[0]), str(REF / "reference.wav"))
    print(f"reference.wav: {best[3]:.1f} s from {best[0].name} @ {best[1]:.1f}s")


def analyze(files):
    import librosa
    pitches, words, total_speech, total_dur, samples = [], 0, 0.0, 0.0, []
    for f in files:
        y, sr = librosa.load(f, sr=16000, mono=True)
        f0, voiced, _ = librosa.pyin(y, fmin=65, fmax=400, sr=sr, frame_length=1024)
        pitches.extend(f0[voiced & ~np.isnan(f0)].tolist())
        spans, dur = speech_spans(f, min_len=0.3)
        total_speech += sum(e - s for s, e in spans)
        total_dur += dur
        subprocess.run([*TRANSCRIBE, str(f), "small"], check=True, capture_output=True)
        wj = Path(str(f) + ".words.json")
        if not wj.exists():
            wj = Path(f).with_suffix(Path(f).suffix + ".words.json")
        if wj.exists():
            data = json.loads(wj.read_text())
            ws = data.get("words", data) if isinstance(data, dict) else data
            words += len(ws)
            samples.append(" ".join(w.get("word", "").strip() for w in ws)[:400])
    p = np.array(pitches)
    profile = {
        "files": [str(f) for f in files],
        "pitch_hz": {"median": round(float(np.median(p)), 1), "p10": round(float(np.percentile(p, 10)), 1),
                     "p90": round(float(np.percentile(p, 90)), 1)} if len(p) else None,
        "pitch_range_semitones": round(float(12 * np.log2(np.percentile(p, 90) / np.percentile(p, 10))), 1) if len(p) else None,
        "speech_ratio": round(total_speech / total_dur, 2) if total_dur else None,
        "words_per_minute": round(words / (total_speech / 60), 0) if total_speech else None,
        "transcript_samples": samples,
    }
    (VOICE / "profile.json").write_text(json.dumps(profile, ensure_ascii=False, indent=1))
    ph = profile["pitch_hz"] or {}
    (VOICE / "profile.md").write_text(
        "# Srijan's voice, measured\n\n"
        f"- Pitch: median {ph.get('median')} Hz, normal range {ph.get('p10')}–{ph.get('p90')} Hz ({profile['pitch_range_semitones']} semitones of movement)\n"
        f"- Pace: about {profile['words_per_minute']} words per minute of speech; talking {int((profile['speech_ratio'] or 0) * 100)}% of the time\n"
        "- Use the wpm for ig-reel's beats.py (`--wpm`) and for timing on-screen text.\n\n"
        "## What Whisper heard\n" + "\n".join(f"> {s}" for s in samples) + "\n")
    print(json.dumps({k: v for k, v in profile.items() if k != "transcript_samples"}, indent=1))


def load_model():
    import torch
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    # Mac GPU (Metal/MPS) when available, else CPU. Chatterbox's checkpoints were saved on CUDA,
    # so torch.load is patched to map them onto the chosen device.
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    _load = torch.load
    torch.load = lambda *a, **k: _load(*a, **{**k, "map_location": k.get("map_location") or torch.device(device)})
    torch.manual_seed(7)
    print(f"device: {device}")
    return ChatterboxMultilingualTTS.from_pretrained(device=device)


def synth(model, text, lang, mood, out, ref):
    import torchaudio as ta
    exag, cfg, temp = MOODS[mood]
    kw = {"audio_prompt_path": str(ref)} if ref and Path(ref).exists() else {}
    if not kw:
        print("note: no reference clip found, using Chatterbox's default voice")
    wav = model.generate(text, language_id=lang, exaggeration=exag, cfg_weight=cfg, temperature=temp, **kw)
    OUT.mkdir(parents=True, exist_ok=True)
    out = Path(out) if out else OUT / f"{mood}_{lang}_{abs(hash(text)) % 10**6}.wav"
    out.parent.mkdir(parents=True, exist_ok=True)
    ta.save(str(out), wav, model.sr)
    print(f"saved {out}  ({wav.shape[-1] / model.sr:.2f} s)")
    return wav.shape[-1] / model.sr


def say(text, lang, mood, out, ref):
    synth(load_model(), text, lang, mood, out, ref)


def batch(spec, ref):
    """spec: JSON list of {"text", "lang", "mood", "out", "ref"?}; one model load for all lines. Writes durations back."""
    lines = json.loads(Path(spec).read_text())
    model = load_model()
    for ln in lines:
        if ln.get("dur") and Path(ln["out"]).exists():
            continue  # already generated; delete "dur" (or the file) to redo a line
        ln["dur"] = synth(model, ln["text"], ln.get("lang", "en"), ln.get("mood", "normal"), ln["out"], ln.get("ref") or ref)
    Path(spec).write_text(json.dumps(lines, ensure_ascii=False, indent=1))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("prep"); p.add_argument("files", nargs="+")
    a = sub.add_parser("analyze"); a.add_argument("files", nargs="+")
    s = sub.add_parser("say"); s.add_argument("text"); s.add_argument("--lang", default="en", choices=["en", "hi"])
    s.add_argument("--mood", default="normal", choices=list(MOODS)); s.add_argument("--out")
    s.add_argument("--ref", default=str(REF / "reference.wav"))
    b = sub.add_parser("batch", help="generate many lines from a JSON spec with one model load")
    b.add_argument("spec"); b.add_argument("--ref", default=str(REF / "reference.wav"))
    args = ap.parse_args()
    if args.cmd == "prep":
        prep(args.files)
    elif args.cmd == "analyze":
        analyze(args.files)
    elif args.cmd == "batch":
        batch(args.spec, args.ref)
    else:
        say(args.text, args.lang, args.mood, args.out, args.ref)


if __name__ == "__main__":
    main()
