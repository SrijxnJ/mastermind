#!/usr/bin/env python3
"""luts.py - build the Brain's grade recipes as 33-point .cube LUTs (free replacement for paid preset packs).

Writes library/luts/<name>.cube. The files import into CapCut, VN, DaVinci Resolve,
Premiere/Lightroom, and run in ffmpeg:  ffmpeg -i in.mp4 -vf lut3d=library/luts/moody.cube out.mp4

Optional before/after PNGs (the AFTER half is rendered by ffmpeg's lut3d from the .cube itself, so the
picture also proves the file loads):
  .venv/bin/python -I tools/luts.py --compare moody=photo.jpg gym-contrast=frame.png ...

Recipes (source in brackets). All values act on display-referred Rec.709 (phone footage, SDR), 0..1:
  moody         [L10] curves: highlights -35 (white 1.0 -> 0.86, upper mids pulled down), blacks +12 lifted
                (0 -> 12/255), saturation -15 %. The L10 soft vignette (-40) is NOT in the LUT (a LUT can't
                know pixel position): add it in the app, or ffmpeg  vignette=angle=PI/5
  gym-contrast  [SP gym grade + L07 deep blacks, C32 resolved per pillar] deep blacks (crushed toe), punchy
                S-curve, slight teal shadows / orange highlights, a touch cooler overall, saturation x1.05
  travel-warm   [L06 + SP golden hour + KH Khandala grade] warm golden mids, shadows lifted a little,
                highlights pulled to keep the sun's disc, highlights slightly desaturated, mids sat +8 %
  tech-clean    [our take for the tech/PC pillar] neutral mids, cool highlights, clean black point,
                gentle contrast for crisp edges, saturation x0.97 (keeps RGB/UI colours honest)
"""
import argparse, os, subprocess, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.normpath(os.path.join(HERE, "..", "library", "luts"))
FONT = os.path.join(HERE, "fonts", "Anton-Regular.ttf")
N = 33
LUMA = np.array([0.2126, 0.7152, 0.0722])


# ------------------------------------------------------------------ helpers
def curve(points):
    """Monotone cubic (Fritsch-Carlson) through (x, y) points -> vectorised f(x)."""
    xs, ys = map(np.asarray, zip(*points))
    d = np.diff(ys) / np.diff(xs)
    m = np.concatenate([[d[0]], (d[:-1] + d[1:]) / 2, [d[-1]]])
    for k in range(len(d)):
        if d[k] == 0:
            m[k] = m[k + 1] = 0
        else:
            a, b = m[k] / d[k], m[k + 1] / d[k]
            s = a * a + b * b
            if s > 9:
                t = 3 / np.sqrt(s); m[k] = t * a * d[k]; m[k + 1] = t * b * d[k]
    def f(x):
        x = np.clip(x, xs[0], xs[-1])
        i = np.clip(np.searchsorted(xs, x, side="right") - 1, 0, len(xs) - 2)
        h = xs[i + 1] - xs[i]; t = (x - xs[i]) / h
        h00 = 2 * t**3 - 3 * t**2 + 1; h10 = t**3 - 2 * t**2 + t
        h01 = -2 * t**3 + 3 * t**2; h11 = t**3 - t**2
        return h00 * ys[i] + h10 * h * m[i] + h01 * ys[i + 1] + h11 * h * m[i + 1]
    return f


def luma(rgb):
    return rgb @ LUMA


def saturate(rgb, s):
    """s: scalar or per-pixel array; scales chroma around Rec.709 luma."""
    y = luma(rgb)[..., None]
    s = np.asarray(s)[..., None] if np.ndim(s) else s
    return y + (rgb - y) * s


def smoothstep(a, b, x):
    t = np.clip((x - a) / (b - a), 0, 1)
    return t * t * (3 - 2 * t)


def tone(rgb, lo=None, mid=None, hi=None):
    """Lift/gamma/gain-style colour balance weighted by luminance (like ffmpeg colorbalance rs/rm/rh)."""
    y = luma(rgb)[..., None]
    ws = 1 - smoothstep(0.0, 0.45, y)
    wh = smoothstep(0.55, 1.0, y)
    wm = 1 - ws - wh
    out = rgb.copy()
    for w, v in ((ws, lo), (wm, mid), (wh, hi)):
        if v is not None:
            out = out + w * np.asarray(v)
    return out


# ------------------------------------------------------------------ recipes
def moody(rgb):
    c = curve([(0, 12 / 255), (0.25, 0.262), (0.5, 0.478), (0.75, 0.668), (1.0, 0.86)])
    return saturate(c(rgb), 0.85)


def gym_contrast(rgb):
    c = curve([(0, 0.0), (0.05, 0.018), (0.25, 0.215), (0.5, 0.5), (0.75, 0.795), (1.0, 0.985)])
    out = c(rgb)
    out = tone(out, lo=(-0.012, 0.006, 0.020), mid=(-0.004, 0.0, 0.006), hi=(0.022, 0.006, -0.018))
    return saturate(out, 1.05)


def travel_warm(rgb):
    c = curve([(0, 0.022), (0.25, 0.265), (0.5, 0.52), (0.78, 0.79), (1.0, 0.965)])
    out = tone(c(rgb), lo=(0.006, 0.0, -0.006), mid=(0.05, 0.022, -0.04), hi=(0.016, 0.006, -0.016))
    y = luma(np.clip(out, 0, 1))
    s = 1.08 - 0.30 * smoothstep(0.62, 1.0, y)      # richer mids, highlights slightly desaturated
    return saturate(out, s)


def tech_clean(rgb):
    c = curve([(0, 0.0), (0.04, 0.03), (0.25, 0.235), (0.5, 0.5), (0.75, 0.77), (1.0, 1.0)])
    out = tone(c(rgb), mid=(-0.002, 0.0, 0.004), hi=(-0.014, 0.0, 0.018))
    return saturate(out, 0.97)


RECIPES = {"moody": moody, "gym-contrast": gym_contrast, "travel-warm": travel_warm, "tech-clean": tech_clean}
TITLES = {"moody": "Moody (L10: highlights -35, blacks +12, sat -15%)",
          "gym-contrast": "Gym contrast (deep blacks, punchy, slight teal-orange)",
          "travel-warm": "Travel warm (L06 golden mids, soft highlights)",
          "tech-clean": "Tech clean (neutral, cool highlights, crisp)"}


# ------------------------------------------------------------------ io
def write_cube(name, fn, path):
    g = np.linspace(0, 1, N)
    b, gg, r = np.meshgrid(g, g, g, indexing="ij")          # .cube order: red changes fastest
    rgb = np.stack([r, gg, b], axis=-1).reshape(-1, 3)
    out = np.clip(fn(rgb), 0, 1)
    with open(path, "w") as f:
        f.write(f'TITLE "{TITLES[name]}"\n')
        f.write(f"LUT_3D_SIZE {N}\nDOMAIN_MIN 0.0 0.0 0.0\nDOMAIN_MAX 1.0 1.0 1.0\n")
        for v in out:
            f.write(f"{v[0]:.6f} {v[1]:.6f} {v[2]:.6f}\n")
    ident = np.abs(out - rgb).mean()
    print(f"{path}  ({N}^3 = {N**3} entries, mean shift from identity {ident:.4f})")


def compare(name, img, cube, out_png, height=720):
    """Before | after side by side; the after half is ffmpeg lut3d applied with the .cube."""
    lab = ("drawtext=fontfile='{f}':text='{t}':fontsize={s}:fontcolor=white:x=24:y=24:"
           "box=1:boxcolor=black@0.45:boxborderw=12")
    s = height // 26
    fc = (f"[0:v]scale=-2:{height},split[a][b];"
          f"[a]{lab.format(f=FONT, t='BEFORE', s=s)}[l];"
          f"[b]lut3d=file='{cube}',{lab.format(f=FONT, t='AFTER - ' + name, s=s)}[r];"
          f"[l][r]hstack=2,drawbox=x=iw/2-2:y=0:w=4:h=ih:color=white@0.9:t=fill")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", img, "-filter_complex", fc, "-frames:v", "1", out_png],
                   check=True)
    print(f"{out_png}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default=OUT_DIR)
    ap.add_argument("--only", nargs="*", choices=list(RECIPES))
    ap.add_argument("--compare", nargs="*", default=[], metavar="NAME=IMAGE",
                    help="write <out>/<name>_before_after.png from this still (jpg/png, or a video frame you extracted)")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    for name in a.only or RECIPES:
        write_cube(name, RECIPES[name], os.path.join(a.out, f"{name}.cube"))
    for item in a.compare:
        name, img = item.split("=", 1)
        if name not in RECIPES:
            sys.exit(f"unknown LUT {name}")
        compare(name, img, os.path.join(a.out, f"{name}.cube"), os.path.join(a.out, f"{name}_before_after.png"))


if __name__ == "__main__":
    main()
