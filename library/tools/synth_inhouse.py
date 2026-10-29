"""In-house CC0 sound design (numpy/scipy DSP, some from CC0 Kenney recordings).
Usage: <earshot venv python> -I synth.py DL_LIB OUTDIR
Writes OUTDIR/<category>/<name>.wav and OUTDIR/synth_meta.json"""
import json, os, subprocess, sys
import numpy as np
from scipy import signal

DL, OUT = sys.argv[1], sys.argv[2]
SR = 44100
rng = np.random.default_rng(20261027)
meta = {}


def load(path):
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                       capture_output=True, check=True)
    return np.frombuffer(r.stdout, np.float32).astype(np.float64)


def find(pattern):
    import glob
    g = sorted(glob.glob(os.path.join(DL, "**", pattern), recursive=True))
    if not g:
        raise FileNotFoundError(pattern)
    return g[0]


def save(cat, name, y, desc, sources=None, stereo_width=0.0):
    # mono on purpose: a delayed-copy stereo widener comb-filters (earshot flagged "ring") and phone speakers are mono
    stereo_width = 0.0
    y = np.asarray(y, np.float64)
    if y.ndim == 1:
        if stereo_width > 0:
            d = int(0.011 * SR)
            r = np.concatenate([np.zeros(d), y[:-d]])
            l = y
            y = np.stack([l * (1 - stereo_width * 0.3) + r * stereo_width * 0.3, r * (1 - stereo_width * 0.3) + l * stereo_width * 0.3], 1)
        else:
            y = np.stack([y, y], 1)
    # fades against clicks
    n = len(y)
    fi, fo = min(int(0.002 * SR), n // 4), min(int(0.03 * SR), n // 4)
    y[:fi] *= np.linspace(0, 1, fi)[:, None]
    y[-fo:] *= np.linspace(1, 0, fo)[:, None]
    y = y - y.mean(0)
    y = y / (np.abs(y).max() + 1e-9) * 0.89
    os.makedirs(os.path.join(OUT, cat), exist_ok=True)
    p = os.path.join(OUT, cat, name + ".wav")
    import soundfile as sf
    sf.write(p, y.astype(np.float32), SR, subtype="PCM_24")
    meta[p] = {"category": cat, "name": name, "description": desc, "sources": sources or []}


def noise(n, color="pink"):
    w = rng.standard_normal(n)
    if color == "white":
        return w
    f = np.fft.rfftfreq(n, 1 / SR)
    s = np.fft.rfft(w)
    s[1:] /= np.sqrt(f[1:]) if color == "pink" else f[1:]
    s[0] = 0
    x = np.fft.irfft(s, n)
    return x / np.abs(x).max()


def sweep_bp(x, fc, q=1.2, block=256):
    """time-varying 2nd-order bandpass: fc array per sample (block-wise coefficients, state carried)"""
    y = np.zeros_like(x)
    zi = np.zeros(2)
    for i in range(0, len(x), block):
        c = float(np.clip(fc[min(i + block // 2, len(fc) - 1)], 40, SR * 0.45))
        b, a = signal.iirpeak(c, q, fs=SR) if False else signal.butter(2, [c / (1 + 0.5 / q), c * (1 + 0.5 / q)], "bandpass", fs=SR, output="ba")[:2]
        if zi.shape[0] != max(len(a), len(b)) - 1:
            zi = np.zeros(max(len(a), len(b)) - 1)
        y[i:i + block], zi = signal.lfilter(b, a, x[i:i + block], zi=zi)
    return y


def sweep_lp(x, fc, block=256):
    y = np.zeros_like(x)
    zi = np.zeros(2)
    for i in range(0, len(x), block):
        c = float(np.clip(fc[min(i + block // 2, len(fc) - 1)], 30, SR * 0.45))
        b, a = signal.butter(2, c, "lowpass", fs=SR)
        y[i:i + block], zi = signal.lfilter(b, a, x[i:i + block], zi=zi)
    return y


def env_ar(n, peak_frac, a_pow=2.0, r_pow=2.5):
    t = np.linspace(0, 1, n)
    k = max(1, int(peak_frac * n))
    e = np.empty(n)
    e[:k] = (t[:k] / t[k - 1]) ** a_pow if k > 1 else 1
    e[k:] = (1 - (t[k:] - t[k - 1]) / (1 - t[k - 1])) ** r_pow
    return e


def reverb(x, t60=1.2, mix=0.25):
    n = int(t60 * SR)
    ir = rng.standard_normal(n) * np.exp(-6.9 * np.arange(n) / n)
    ir = sweep_lp(ir, np.linspace(6000, 1500, n))
    wet = signal.fftconvolve(x, ir)[: len(x) + n]
    wet = np.pad(wet, (0, len(x) + n - len(wet)))
    wet /= np.abs(wet).max() + 1e-9
    dry = np.concatenate([x, np.zeros(n)])
    dry /= np.abs(dry).max() + 1e-9
    return dry * (1 - mix) + wet * mix


def varispeed(x, rate):
    """read x with per-sample playback rate (can go negative); returns output with len(rate)"""
    pos = np.cumsum(rate)
    pos = np.clip(pos, 0, len(x) - 2)
    i = pos.astype(int)
    f = pos - i
    return x[i] * (1 - f) + x[i + 1] * f


# ---------------------------------------------------------------- whooshes (noise through a moving band)
for name, dur, f0, f1, f2, pk, q, color in [
    ("whoosh_inhouse_air_soft", 0.9, 350, 1800, 500, 0.55, 1.0, "pink"),
    ("whoosh_inhouse_big_dark", 1.4, 180, 900, 250, 0.6, 0.8, "brown"),
    ("whoosh_inhouse_bright_pass", 0.7, 800, 4200, 1200, 0.5, 1.4, "pink"),
]:
    n = int(dur * SR)
    t = np.linspace(0, 1, n)
    k = int(pk * n)
    fc = np.concatenate([np.geomspace(f0, f1, k), np.geomspace(f1, f2, n - k)])
    x = sweep_bp(noise(n, color), fc, q) * env_ar(n, pk, 2.2, 1.8)
    save("whoosh", name, x, f"In-house whoosh: {color} noise through a band sweeping {f0}->{f1}->{f2} Hz, peak at {pk*dur:.2f} s",
         stereo_width=0.8)

for name, dur, f0, f1, pk in [("swoosh_inhouse_flick", 0.32, 1500, 6000, 0.45), ("swoosh_inhouse_snap", 0.25, 900, 5000, 0.5)]:
    n = int(dur * SR)
    k = int(pk * n)
    fc = np.concatenate([np.geomspace(f0, f1, k), np.geomspace(f1, f0, n - k)])
    x = sweep_bp(noise(n, "pink"), fc, 1.5) * env_ar(n, pk, 3, 2.5)
    save("swoosh-fast", name, x, f"In-house fast swoosh: pink noise band {f0}->{f1} Hz in {dur} s", stereo_width=0.6)

# ---------------------------------------------------------------- risers
for name, dur in [("riser_inhouse_noise_4s", 4.0), ("riser_inhouse_noise_8s", 8.0)]:
    n = int(dur * SR)
    t = np.linspace(0, 1, n)
    fc = np.geomspace(250, 9000, n)
    x = sweep_bp(noise(n, "pink"), fc, 1.1) * (t ** 2.2)
    x[-int(0.04 * SR):] *= np.linspace(1, 0, int(0.04 * SR))
    save("riser", name, x, f"In-house noise riser {dur:.0f} s: pink noise band 250->9000 Hz, swell to a hard stop (cut lands on the end)",
         stereo_width=1.0)

for name, dur in [("riser_inhouse_tonal_5s", 5.0)]:
    n = int(dur * SR)
    t = np.linspace(0, 1, n)
    f = 110 * 2 ** (t * 2.0)  # two octaves up
    ph = 2 * np.pi * np.cumsum(f) / SR
    saw = sum(np.sin(k * ph) / k for k in range(1, 12))
    saw2 = sum(np.sin(k * ph * 1.006) / k for k in range(1, 12))
    x = sweep_lp(saw + saw2, np.geomspace(300, 7000, n)) * (t ** 1.8)
    x += 0.35 * sweep_bp(noise(n), np.geomspace(500, 10000, n), 1.0) * t ** 3
    x[-int(0.04 * SR):] *= np.linspace(1, 0, int(0.04 * SR))
    save("riser", name, x, "In-house tonal riser 5 s: detuned saw A2->A4 opening a low-pass, plus noise air", stereo_width=1.0)

# shepard riser (endless rise feel), 6 s
n = int(6 * SR)
t = np.arange(n) / SR
x = np.zeros(n)
for k in range(6):
    pos = (k / 6 + t / 6 * 1.0) % 1.0
    f = 55 * 2 ** (pos * 6)
    ph = 2 * np.pi * np.cumsum(f) / SR
    w = np.sin(np.pi * pos) ** 2
    x += w * np.sin(ph)
x *= np.linspace(0.15, 1, n) ** 1.5
x[-int(0.04 * SR):] *= np.linspace(1, 0, int(0.04 * SR))
save("riser", "riser_inhouse_shepard_6s", x, "In-house Shepard-tone riser 6 s (endless-rise illusion)", stereo_width=0.8)

# ---------------------------------------------------------------- downlifters
for name, dur, color in [("downlifter_inhouse_noise_3s", 3.0, "pink"), ("downlifter_inhouse_air_5s", 5.0, "pink")]:
    n = int(dur * SR)
    t = np.linspace(0, 1, n)
    x = sweep_bp(noise(n, color), np.geomspace(8000, 150, n), 1.0) * (1 - t) ** 1.6
    x[: int(0.01 * SR)] *= np.linspace(0, 1, int(0.01 * SR))
    save("downlifter", name, x, f"In-house downlifter {dur:.0f} s: noise band 8 kHz->150 Hz, decaying", stereo_width=1.0)
n = int(3.5 * SR)
t = np.linspace(0, 1, n)
f = 440 * 2 ** (-t * 3)
ph = 2 * np.pi * np.cumsum(f) / SR
x = sweep_lp(sum(np.sin(k * ph) / k for k in range(1, 10)), np.geomspace(6000, 200, n)) * (1 - t) ** 1.3
x += 0.3 * sweep_bp(noise(n), np.geomspace(9000, 300, n), 1.0) * (1 - t) ** 2
save("downlifter", "downlifter_inhouse_tonal_3s", x, "In-house tonal downlifter 3.5 s: saw A4 falling 3 octaves through a closing low-pass", stereo_width=0.8)

# ---------------------------------------------------------------- sub drops and booms
for name, dur, f0, f1, drive in [("subdrop_inhouse_long", 2.5, 140, 32, 1.5), ("subdrop_inhouse_short", 1.3, 160, 40, 2.0)]:
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = f1 + (f0 - f1) * np.exp(-t / (dur * 0.18))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / (dur * 0.45))
    x = np.tanh(drive * x) / np.tanh(drive)
    click = sweep_lp(noise(int(0.02 * SR), "white"), np.full(int(0.02 * SR), 3000.0)) * np.linspace(1, 0, int(0.02 * SR)) * 0.4
    x[: len(click)] += click
    x *= np.minimum(1, (n - np.arange(n)) / (0.35 * n)) ** 2  # fade the last 35 % so the tail is not cut
    save("bass-drop-boom", name, x, f"In-house sub drop: sine {f0}->{f1} Hz glide with soft saturation and a short click ({dur} s)")
n = int(0.6 * SR)
t = np.arange(n) / SR
body = np.sin(2 * np.pi * np.cumsum(55 + 90 * np.exp(-t / 0.05)) / SR) * np.exp(-t / 0.25)
crack = sweep_lp(noise(n, "white"), np.geomspace(6000, 300, n)) * np.exp(-t / 0.04)
x = np.tanh(1.8 * (body + 0.5 * crack))
x = reverb(x, 2.5, 0.35)
save("bass-drop-boom", "boom_inhouse_cinematic", x, "In-house cinematic boom: pitched sub thump + noise crack into a 2.5 s dark tail (vine-boom-like feel, not the meme sample)")

# ---------------------------------------------------------------- tape stop / rewind (from CC0 Kenney jingles)
for name, pat, stop_s in [("tapestop_inhouse_sax", "jingles_SAX03.ogg", 0.9), ("tapestop_inhouse_8bit", "jingles_NES03.ogg", 0.7),
                          ("tapestop_inhouse_hit", "jingles_HIT02.ogg", 1.2)]:
    src = find(pat)
    x = load(src)
    lead = min(len(x) - int(stop_s * SR) - 10, int(0.8 * SR))
    lead = max(lead, int(0.3 * SR))
    ns = int(stop_s * SR)
    rate = np.concatenate([np.ones(lead), np.linspace(1, 0, ns) ** 1.6])
    y = varispeed(x, rate)
    y = signal.lfilter(*signal.butter(2, 35, "highpass", fs=SR), y)  # the stopping tape drifts to DC
    m = len(y)
    y *= np.minimum(1, (m - np.arange(m)) / (0.45 * ns)) ** 1.5  # level falls with the pitch, as on a real deck
    save("rewind-tape-stop", name, y, f"In-house tape stop: Kenney CC0 jingle, playback rate ramped 1->0 over {stop_s} s",
         sources=[src])
for name, pat in [("rewind_inhouse_vhs", "jingles_PIZZI04.ogg"), ("rewind_inhouse_fast", "jingles_STEEL05.ogg")]:
    src = find(pat)
    x = load(src)
    n = int(1.6 * SR)
    t = np.arange(n) / SR
    rate = -(1 + 2.5 * np.clip(t / 0.4, 0, 1)) * (1 + 0.08 * np.sin(2 * np.pi * 7 * t))
    start = len(x) - 2
    pos = start + np.cumsum(rate)
    pos = np.mod(pos, len(x) - 2)
    i = pos.astype(int)
    fr = pos - i
    y = x[i] * (1 - fr) + x[i + 1] * fr
    y = sweep_bp(y, np.full(n, 2200.0), 0.5) + 0.04 * noise(n, "white")
    y *= np.minimum(1, t / 0.05) * np.minimum(1, (t[-1] - t) / 0.15)
    save("rewind-tape-stop", name, y, "In-house VHS rewind: CC0 Kenney jingle played backwards at 1-3.5x with flutter, band-limited + tape hiss",
         sources=[src])

# ---------------------------------------------------------------- record scratches (vinyl-style position modulation)
for name, pat, kind in [("scratch_inhouse_stop", "jingles_SAX07.ogg", "stop"), ("scratch_inhouse_baby", "jingles_HIT05.ogg", "baby"),
                        ("scratch_inhouse_double", "jingles_PIZZI02.ogg", "double")]:
    src = find(pat)
    x = load(src)
    if kind == "stop":
        n = int(1.4 * SR)
        t = np.arange(n) / SR
        rate = np.where(t < 0.55, 1.0, np.where(t < 0.62, 1 - 30 * (t - 0.55), np.where(t < 0.80, -1.6, 0.0)))
        rate = signal.savgol_filter(rate, 301, 2)
    elif kind == "baby":
        n = int(1.0 * SR)
        t = np.arange(n) / SR
        rate = np.where(t < 0.25, 1.0, 2.2 * np.sin(2 * np.pi * 4.0 * (t - 0.25)))
    else:
        n = int(1.2 * SR)
        t = np.arange(n) / SR
        rate = np.where(t < 0.35, 1.0, 2.6 * np.sign(np.sin(2 * np.pi * 5.0 * (t - 0.35))) * np.minimum(1, (1.2 - t) * 4))
        rate = signal.savgol_filter(rate, 201, 2)
    pos = int(0.2 * SR) + np.cumsum(rate)
    pos = np.clip(pos, 0, len(x) - 2)
    i = pos.astype(int)
    fr = pos - i
    y = x[i] * (1 - fr) + x[i + 1] * fr
    y += 0.02 * sweep_bp(noise(n, "white"), np.full(n, 3000.0), 0.7) * np.abs(rate)  # stylus noise
    save("record-scratch", name, y, f"In-house record scratch ({kind}): a CC0 Kenney jingle read with a moving vinyl position", sources=[src])

# ---------------------------------------------------------------- camera shutters (designed two-stage clicks)
for name, gap, body_hz, dec in [("shutter_inhouse_dslr", 0.075, 2600, 0.012), ("shutter_inhouse_mirrorless", 0.045, 3800, 0.008),
                                ("shutter_inhouse_film", 0.11, 1900, 0.018)]:
    n = int(0.35 * SR)
    y = np.zeros(n)
    for k, (t0, amp) in enumerate([(0.0, 1.0), (gap, 0.8)]):
        m = int(0.06 * SR)
        tt = np.arange(m) / SR
        burst = noise(m, "white") * np.exp(-tt / (dec * 0.4))
        ring = np.sin(2 * np.pi * body_hz * (1 + 0.15 * k) * tt) * np.exp(-tt / dec)
        thud = np.sin(2 * np.pi * 180 * tt) * np.exp(-tt / 0.01)
        s = 0.6 * sweep_bp(burst, np.full(m, 4500.0), 0.7) + 0.5 * ring + 0.35 * thud
        i0 = int(t0 * SR)
        y[i0:i0 + m] += amp * s
    y = reverb(y, 0.25, 0.12)
    save("camera-shutter", name, y, f"In-house camera shutter: two mechanical transients {gap*1000:.0f} ms apart, body ring {body_hz} Hz")

# ---------------------------------------------------------------- cash register "cha-ching" (CC0 Kenney coins + synthesized bell)
coins = load(find("handleCoins.ogg"))
for name, bell_f, coins_at in [("register_inhouse_chaching", 2093.0, 0.16), ("register_inhouse_bell_drawer", 1568.0, 0.25)]:
    n = int(1.6 * SR)
    t = np.arange(n) / SR
    drawer = sweep_bp(noise(n, "pink"), np.geomspace(700, 2200, n), 1.2) * np.where(t < 0.18, (t / 0.18) ** 2, np.exp(-(t - 0.18) / 0.02))
    clunk = np.sin(2 * np.pi * 140 * t) * np.exp(-np.maximum(t - 0.18, 0) / 0.03) * (t >= 0.18)
    bell = np.zeros(n)
    tb = np.maximum(t - 0.05, 0)
    for ratio, a, d in [(1.0, 1.0, 0.9), (2.76, 0.5, 0.45), (5.4, 0.25, 0.2), (8.93, 0.12, 0.1)]:
        bell += a * np.sin(2 * np.pi * bell_f * ratio * tb) * np.exp(-tb / d) * (t >= 0.05)
    y = 0.35 * drawer + 0.6 * clunk + 0.55 * bell
    i0 = int(coins_at * SR)
    c = coins[: n - i0]
    y[i0:i0 + len(c)] += 0.9 * c / (np.abs(c).max() + 1e-9)
    save("cash-register", name, y, "In-house cha-ching: synthesized register bell + drawer slide + Kenney CC0 coin handling",
         sources=[find("handleCoins.ogg")], stereo_width=0.4)

# ---------------------------------------------------------------- chalk clap (gym)
for name, n_layers, puff in [("chalkclap_inhouse_single", 3, 0.5), ("chalkclap_inhouse_dusty", 4, 0.9)]:
    n = int(0.9 * SR)
    t = np.arange(n) / SR
    y = np.zeros(n)
    for k in range(n_layers):
        t0 = 0.008 * k + rng.uniform(0, 0.003)
        i0 = int(t0 * SR)
        m = int(0.12 * SR)
        tt = np.arange(m) / SR
        b = sweep_bp(noise(m, "white"), np.full(m, rng.uniform(1000, 1600)), 0.9) * np.exp(-tt / 0.012)
        y[i0:i0 + m] += b * (1 - 0.15 * k)
    y += 0.25 * sweep_bp(noise(n, "white"), np.full(n, 1200.0), 0.8) * np.exp(-t / 0.05)  # palm body
    y += puff * 0.12 * sweep_lp(noise(n, "pink"), np.full(n, 4000.0)) * np.where(t > 0.02, np.exp(-(t - 0.02) / 0.25), 0) * np.minimum(1, t / 0.06)
    y = reverb(y, 0.5, 0.15)
    save("gym", name, y, "In-house chalk clap: layered hand-clap transients + a soft chalk-dust puff", stereo_width=0.5)

json.dump(meta, open(os.path.join(OUT, "synth_meta.json"), "w"), indent=1)
print(len(meta), "sounds written")


# ================================================================ extras (added after the first earshot pass)
# more baby/chirp scratches (the 'baby' style read as a record scratch; the 'stop' style did not)
for name, pat, f_osc, depth in [("scratch_inhouse_baby_fast", "jingles_SAX10.ogg", 6.0, 2.6), ("scratch_inhouse_chirp", "jingles_STEEL08.ogg", 5.0, 3.0)]:
    src = find(pat)
    x = load(src)
    n = int(0.9 * SR)
    t = np.arange(n) / SR
    rate = np.where(t < 0.15, 1.0, depth * np.sin(2 * np.pi * f_osc * (t - 0.15)))
    pos = np.clip(int(0.25 * SR) + np.cumsum(rate), 0, len(x) - 2)
    i = pos.astype(int)
    fr = pos - i
    y = x[i] * (1 - fr) + x[i + 1] * fr
    y += 0.02 * sweep_bp(noise(n, "white"), np.full(n, 3000.0), 0.7) * np.abs(rate)
    save("record-scratch", name, y, f"In-house record scratch (baby scratch {f_osc:.0f} Hz): a CC0 Kenney jingle read with an oscillating vinyl position", sources=[src])

# camera shutters v2: layered CC0 Kenney mechanical clicks + noise bursts (v1 pure-synth shutters failed earshot)
def _onset(x):
    k = int(np.argmax(np.abs(x) > 0.05 * np.abs(x).max()))
    x = x[max(0, k - 40):]
    return x / np.abs(x).max()
def _nb(ms, lo, hi, dec):
    m = int(ms / 1000 * SR)
    tt = np.arange(m) / SR
    b, a = signal.butter(2, [lo, hi], "bandpass", fs=SR)
    return signal.lfilter(b, a, rng.standard_normal(m)) * np.exp(-tt / dec)
def _mk(parts, dur=0.4):
    y = np.zeros(int(dur * SR))
    for x, t0, g in parts:
        i0 = int(t0 * SR)
        m = min(len(x), len(y) - i0)
        y[i0:i0 + m] += g * x[:m]
    return y
_mc = _onset(load(find("metalClick.ogg")))
_sw2 = _onset(load(find("switch2.ogg")))
_sw4 = _onset(load(find("switch4.ogg")))
save("camera-shutter", "shutter_inhouse_mech_a", _mk([(_mc, 0, 0.9), (_nb(30, 2000, 12000, 0.004), 0.0, 0.8),
     (_mc[::-1][-int(0.06 * SR):], 0.05, 0.4), (_sw4, 0.065, 0.8)]),
     "In-house camera shutter: Kenney CC0 metal click + switch click 65 ms apart with a bright noise burst",
     sources=[find("metalClick.ogg"), find("switch4.ogg")])
save("camera-shutter", "shutter_inhouse_mech_b", _mk([(_mc, 0, 1.0), (_nb(50, 800, 8000, 0.008), 0.0, 0.7), (_sw2, 0.055, 0.7)]),
     "In-house camera shutter: Kenney CC0 metal click + switch click 55 ms apart with a noise slap",
     sources=[find("metalClick.ogg"), find("switch2.ogg")])

# glitches v2: buffer-repeat stutter + bit-crush of CC0 Kenney sci-fi/digital recordings (the raw ones are 20 ms ticks or 5 s beds)
def _crush(x, bits, hold):
    q = 2 ** (bits - 1)
    y = np.round(x * q) / q
    return np.repeat(y[::hold], hold)[: len(x)]
for name, pat, seed_off, seq in [
        ("glitch_inhouse_stutter", "computerNoise_002.ogg", 0.40, [(0.045, 4), (0.02, 3), (0.09, 1), (0.012, 6)]),
        ("glitch_inhouse_data", "computerNoise_003.ogg", 1.10, [(0.03, 2), (0.06, 2), (0.015, 8), (0.05, 1)]),
        ("glitch_inhouse_zap", "zap1.ogg", 0.05, [(0.025, 3), (0.04, 2), (0.01, 10), (0.08, 1)])]:
    src = find(pat)
    x = load(src)
    x = x / (np.abs(x).max() + 1e-9)
    pos = int(seed_off * SR)
    out = []
    for k, (slice_s, reps) in enumerate(seq):
        m = int(slice_s * SR)
        seg = x[pos:pos + m].copy()
        if len(seg) < m:
            seg = np.pad(seg, (0, m - len(seg)))
        seg *= np.minimum(1, np.minimum(np.arange(m), m - np.arange(m)) / 32)  # 0.7 ms edges, no hard clicks
        seg = _crush(seg, bits=[4, 6, 3, 8][k % 4], hold=[3, 1, 6, 2][k % 4])
        out.extend([seg] * reps)
        pos += int(rng.uniform(0.05, 0.4) * SR)
    y = np.concatenate(out)
    y = signal.lfilter(*signal.butter(2, 60, "highpass", fs=SR), y)
    save("glitch", name, y, "In-house glitch: buffer-repeat stutter + bit-crush/sample-hold of a CC0 Kenney sci-fi recording", sources=[src])

# meme-style CC0 recreations (generic motifs, made from scratch: not the copyrighted recordings)
n = int(0.6 * SR); t = np.arange(n) / SR
save("meme-cc0", "censor_beep_1khz", np.sin(2 * np.pi * 1000 * t) * np.minimum(1, np.minimum(t, t[-1] - t) / 0.004),
     "In-house censor beep: 1 kHz sine, 0.6 s (trim to the word)")
def _brass(f0, dur, bend=0.0, wah=True):
    m = int(dur * SR); tt = np.arange(m) / SR
    f = f0 * 2 ** ((bend * tt / dur) / 12) * (1 + 0.012 * np.sin(2 * np.pi * 5.5 * tt) * np.clip(tt / 0.3, 0, 1))
    ph = 2 * np.pi * np.cumsum(f) / SR
    x = sum(np.sin(k * ph) / k ** 0.9 for k in range(1, 18))
    cut = 600 + 2200 * (0.5 + 0.5 * np.sin(2 * np.pi * (1.6 if wah else 0) * tt - np.pi / 2)) if wah else np.full(m, 2500.0)
    x = sweep_lp(x, cut)
    env = np.minimum(1, tt / 0.04) * np.minimum(1, (dur - tt) / 0.08)
    return x * env
seq = [(_brass(233.08, 0.45), 0.0), (_brass(220.0, 0.45), 0.5), (_brass(207.65, 0.45), 1.0), (_brass(196.0, 1.6, bend=-1.0), 1.5)]
y = np.zeros(int(3.3 * SR))
for x, t0 in seq:
    i0 = int(t0 * SR); y[i0:i0 + len(x)] += x
save("meme-cc0", "sad_trombone_inhouse", reverb(y, 0.8, 0.12), "In-house sad trombone ('wah wah wah waaah'): synthesized muted-brass line Bb3-A3-Ab3-G3, made from scratch")
def _snare(dur=0.25):
    m = int(dur * SR); tt = np.arange(m) / SR
    body = np.sin(2 * np.pi * 190 * tt) * np.exp(-tt / 0.03)
    sn = sweep_bp(rng.standard_normal(m), np.full(m, 3500.0), 0.6) * np.exp(-tt / 0.06)
    return 0.6 * body + sn
def _cymbal(dur=1.8):
    m = int(dur * SR); tt = np.arange(m) / SR
    x = rng.standard_normal(m)
    x = signal.lfilter(*signal.butter(2, 5000, "highpass", fs=SR), x)
    ring = sum(np.sin(2 * np.pi * f * tt) for f in (3720, 5210, 6880, 8930)) * 0.05
    return (x + ring) * np.exp(-tt / 0.45) * np.minimum(1, tt / 0.002)
y = np.zeros(int(2.2 * SR))
for x, t0, g in [(_snare(), 0.0, 0.8), (_snare(), 0.16, 0.9), (_cymbal(), 0.40, 0.8), (_snare(0.3), 0.40, 0.7)]:
    i0 = int(t0 * SR); y[i0:i0 + len(x)] += g * x
save("meme-cc0", "rimshot_badumtss_inhouse", reverb(y, 0.6, 0.1), "In-house 'ba-dum-tss' rimshot: two synthesized snare hits + cymbal crash")
n = int(2.0 * SR); t = np.arange(n) / SR
gate = np.zeros(n)
for a, b in [(0.0, 0.22), (0.3, 0.52), (0.6, 1.6)]:
    gate += ((t >= a) & (t < b)) * np.minimum(1, np.minimum(t - a, b - t) / 0.01).clip(0, 1)
horn = sum(np.sign(np.sin(2 * np.pi * f * t)) * 0.3 + sum(np.sin(2 * np.pi * k * f * t) / k for k in range(1, 10)) for f in (466.16, 587.33, 698.46))
horn = np.tanh(1.5 * sweep_lp(horn, np.full(n, 3500.0)))
save("meme-cc0", "airhorn_inhouse", horn * gate, "In-house air horn: 3 blasts of a distorted Bb-major horn chord (synthesized)")
json.dump(meta, open(os.path.join(OUT, "synth_meta.json"), "w"), indent=1)
