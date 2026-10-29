#!/usr/bin/env python3
"""text_behind.py - "text behind your head" (Brain L10) with free, local person segmentation.

Layers, bottom to top:  original frame  ->  text  ->  the person cut out of the same frame.
So the words sit behind you, in front of the background.

Segmentation (all CPU, all free):
  multiclass  MediaPipe selfie_multiclass_256x256 (Apache-2.0)  default, best silhouette (hair/body/clothes)
  selfie      MediaPipe selfie_segmenter (Apache-2.0)           ~10x faster, rougher, best for close-ups
  u2netp      rembg u2netp (MIT)                               general salient-object cut-out, weakest on bodies

Mask clean-up: confidence levels -> edge-aware guided filter (snaps to hair/shoulders) -> motion-adaptive
temporal smoothing (kills flicker, no ghosting on fast moves) -> 1 px choke -> gaussian feather.

Run it with the vision venv, isolated (-I):
  .venv/bin/python -I tools/text_behind.py IN.mp4 --text "75 KG" \
      --font tools/fonts/Anton-Regular.ttf --color "#FFFFFF" --size 0.17 --x 0.5 --y 0.40 \
      --start 0.3 --end 3.4 --clip-start 4.0 --clip-end 7.5 -o OUT.mp4

--size: font size in px (>1) or as a fraction of the video height (<=1).
--x/--y: centre of the text block as fractions of width/height.
--start/--end: when the text is on screen, in seconds of the OUTPUT (after --clip-start trimming).
The original audio is kept (trimmed to the same window).
"""
import argparse, json, os, subprocess, sys, time
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont, ImageFilter

MODELS = os.environ.get("VISION_MODELS", os.path.expanduser("~/sm-tools/models/vision"))
HERE = os.path.dirname(os.path.abspath(__file__))


# ---------------------------------------------------------------- video io
def probe(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height,r_frame_rate:stream_side_data=rotation:format=duration",
                          "-of", "json", path], capture_output=True, text=True, check=True).stdout
    d = json.loads(out); s = d["streams"][0]
    w, h = int(s["width"]), int(s["height"])
    rot = 0
    for sd in s.get("side_data_list", []) or []:
        if "rotation" in sd:
            rot = int(sd["rotation"])
    if abs(rot) % 180 == 90:
        w, h = h, w
    n, dd = s["r_frame_rate"].split("/")
    fps = float(n) / float(dd)
    has_audio = bool(json.loads(subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "json", path],
        capture_output=True, text=True).stdout or "{}").get("streams"))
    return w, h, fps, float(d["format"]["duration"]), has_audio


def trim_args(a):
    t = []
    if a.clip_start:
        t += ["-ss", f"{a.clip_start:.3f}"]
    if a.clip_end:
        t += ["-t", f"{a.clip_end - (a.clip_start or 0):.3f}"]
    return t


# ---------------------------------------------------------------- segmentation
class Segmenter:
    def __init__(self, kind, work_px):
        self.kind, self.work_px = kind, work_px
        if kind in ("multiclass", "selfie"):
            import mediapipe as mp
            from mediapipe.tasks.python import vision, BaseOptions
            self.mp = mp
            name = {"multiclass": "selfie_multiclass_256x256.tflite", "selfie": "selfie_segmenter.tflite"}[kind]
            path = os.path.join(MODELS, name)
            if not os.path.exists(path):
                sys.exit(f"model missing: {path} (run tools/setup_free_tools.sh)")
            self.seg = vision.ImageSegmenter.create_from_options(vision.ImageSegmenterOptions(
                base_options=BaseOptions(model_asset_path=path),
                output_confidence_masks=True, output_category_mask=False))
        elif kind == "u2netp":
            os.environ.setdefault("U2NET_HOME", MODELS)
            from rembg import new_session, remove
            self.session, self.remove = new_session("u2netp"), remove
        else:
            sys.exit(f"unknown model {kind}")

    def close(self):
        if hasattr(self, "seg"):
            self.seg.close(); del self.seg

    def __call__(self, rgb):
        h, w = rgb.shape[:2]
        sc = min(1.0, self.work_px / max(h, w))
        small = cv2.resize(rgb, (round(w * sc), round(h * sc)), interpolation=cv2.INTER_AREA) if sc < 1 else rgb
        if self.kind in ("multiclass", "selfie"):
            r = self.seg.segment(self.mp.Image(image_format=self.mp.ImageFormat.SRGB, data=np.ascontiguousarray(small)))
            masks = [m.numpy_view().copy() for m in r.confidence_masks]  # copy: buffers die with the result
            m = masks[0] if self.kind == "selfie" else 1.0 - masks[0]   # multiclass channel 0 = background
        else:
            m = np.asarray(self.remove(Image.fromarray(small), session=self.session, only_mask=True,
                                       post_process_mask=False), dtype=np.float32) / 255.0
        m = np.squeeze(m).astype(np.float32)
        return cv2.resize(m, (w, h), interpolation=cv2.INTER_LINEAR)


class MaskCleaner:
    """levels -> guided filter -> motion-adaptive EMA -> choke -> feather."""
    def __init__(self, a):
        self.lo, self.hi = a.mask_lo, a.mask_hi
        self.smooth, self.feather, self.choke, self.guided = a.smooth, a.feather, a.choke, a.guided
        self.prev = None

    def __call__(self, m, rgb):
        m = np.clip((m - self.lo) / max(1e-3, self.hi - self.lo), 0, 1).astype(np.float32)
        if self.guided > 0 and hasattr(cv2, "ximgproc"):
            g = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0
            m = np.clip(cv2.ximgproc.guidedFilter(g, m, self.guided, 1e-3), 0, 1)
        if self.prev is not None and self.smooth > 0:
            # strong smoothing where the mask barely changed (flicker), little where it moved a lot (real motion)
            diff = np.abs(m - self.prev)
            alpha = (1.0 - self.smooth) + diff * 2.5
            alpha = np.clip(alpha + 0.25 * (m > self.prev), 0, 1)  # appear fast (moving limbs), fade slower
            m = self.prev + alpha * (m - self.prev)
        self.prev = m
        out = m
        if self.choke > 0:
            k = 2 * self.choke + 1
            out = cv2.erode(out, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
        if self.feather > 0:
            out = cv2.GaussianBlur(out, (0, 0), self.feather)
        return out


# ---------------------------------------------------------------- text layer
def parse_color(c):
    c = c.strip().lstrip("#")
    if len(c) == 6:
        return tuple(int(c[i:i + 2], 16) for i in (0, 2, 4))
    sys.exit(f"colour must be #RRGGBB, got {c}")


def render_text(a, W, H):
    """Full-frame premultiplied RGB (float) + alpha (float), drawn once."""
    size = int(a.size * H) if a.size <= 1 else int(a.size)
    font = ImageFont.truetype(a.font, size)
    lines = a.text.replace("\\n", "\n").split("\n")
    track = a.tracking * size
    def line_w(s):
        return sum(font.getlength(ch) for ch in s) + track * max(0, len(s) - 1)
    asc, desc = font.getmetrics()
    lh = int((asc + desc) * a.line_height)
    block_h = lh * (len(lines) - 1) + asc + desc
    cx, cy = a.x * W, a.y * H
    pad = size  # room for shadow/stroke
    layer = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(layer)
    y0 = cy - block_h / 2
    for i, s in enumerate(lines):
        x = cx - line_w(s) / 2; y = y0 + i * lh
        for ch in s:
            if a.outline > 0:
                d.text((x, y), ch, font=font, fill=0, stroke_width=a.outline, stroke_fill=255)
            else:
                d.text((x, y), ch, font=font, fill=255)
            x += font.getlength(ch) + track
    text_a = np.asarray(layer, dtype=np.float32) / 255.0 * a.opacity
    col = np.array(parse_color(a.color), dtype=np.float32)
    rgb = text_a[..., None] * col
    alpha = text_a
    if a.shadow > 0:
        off = max(2, size // 40)
        sh = layer.filter(ImageFilter.GaussianBlur(max(2, size / 18)))
        sh = np.roll(np.asarray(sh, dtype=np.float32) / 255.0, (off, off), axis=(0, 1)) * a.shadow
        # shadow goes under the text: over-composite text onto black shadow
        alpha = text_a + sh * (1 - text_a)
        rgb = rgb  # shadow colour is black, so premultiplied rgb is unchanged
    ys, xs = np.nonzero(alpha > 0.002)
    if len(ys) == 0:
        sys.exit("text rendered empty - check font/size/position")
    bbox = (max(0, ys.min() - 2), min(H, ys.max() + 3), max(0, xs.min() - 2), min(W, xs.max() + 3))
    return rgb, alpha, bbox, size


def envelope(t, a):
    if t < a.start or t > a.end:
        return 0.0
    k = 1.0
    if a.fade > 0:
        k = min(k, (t - a.start) / a.fade, (a.end - t) / a.fade)
    return float(np.clip(k, 0, 1))


# ---------------------------------------------------------------- main
def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("input")
    p.add_argument("-o", "--output")
    p.add_argument("--text", required=True, help='use "\\n" for a second line')
    p.add_argument("--font", default=os.path.join(HERE, "fonts", "Anton-Regular.ttf"))
    p.add_argument("--color", default="#FFFFFF")
    p.add_argument("--size", type=float, default=0.16, help="px, or fraction of height if <= 1")
    p.add_argument("--x", type=float, default=0.5); p.add_argument("--y", type=float, default=0.33)
    p.add_argument("--start", type=float, default=0.0); p.add_argument("--end", type=float, default=1e9)
    p.add_argument("--fade", type=float, default=0.25, help="fade in/out seconds")
    p.add_argument("--rise", type=float, default=0.0, help="px the text drifts up while fading in")
    p.add_argument("--tracking", type=float, default=0.0, help="letter spacing as fraction of size")
    p.add_argument("--line-height", type=float, default=0.95)
    p.add_argument("--opacity", type=float, default=1.0)
    p.add_argument("--outline", type=int, default=0, help="px; >0 draws outlined (hollow) letters, L10 CTA style")
    p.add_argument("--shadow", type=float, default=0.35, help="soft drop-shadow opacity, 0 = off")
    p.add_argument("--clip-start", type=float, default=0.0); p.add_argument("--clip-end", type=float, default=0.0)
    p.add_argument("--model", default="multiclass", choices=["multiclass", "selfie", "u2netp"])
    p.add_argument("--work-px", type=int, default=960, help="long side the frame is shrunk to for segmentation")
    p.add_argument("--mask-lo", type=float, default=0.15); p.add_argument("--mask-hi", type=float, default=0.55)
    p.add_argument("--guided", type=int, default=6, help="guided-filter radius px (0 = off)")
    p.add_argument("--smooth", type=float, default=0.8, help="temporal smoothing 0..0.9 (0 = off)")
    p.add_argument("--choke", type=int, default=1, help="px the mask is shrunk before feathering")
    p.add_argument("--feather", type=float, default=1.5, help="gaussian sigma px on the mask edge")
    p.add_argument("--crf", type=int, default=17)
    p.add_argument("--mask-video", help="also write the cleaned mask as a grey MP4 (QA)")
    a = p.parse_args()

    W, H, fps, dur, has_audio = probe(a.input)
    out = a.output or os.path.splitext(a.input)[0] + "_textbehind.mp4"
    rgb_t, alpha_t, (y0, y1, x0, x1), px = render_text(a, W, H)
    rise_px = int(a.rise)
    if rise_px:
        y0 = max(0, y0 - rise_px)
    print(f"{W}x{H} @ {fps:.3f} fps, text '{a.text}' {px}px, model={a.model}", file=sys.stderr)

    dec = subprocess.Popen(["ffmpeg", "-v", "error", *trim_args(a), "-i", a.input, "-f", "rawvideo",
                            "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
    enc_cmd = ["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
               "-r", f"{fps}", "-i", "-"]
    if has_audio:
        enc_cmd += [*trim_args(a), "-i", a.input, "-map", "0:v", "-map", "1:a:0", "-c:a", "aac", "-b:a", "192k"]
    enc_cmd += ["-c:v", "libx264", "-preset", "medium", "-crf", str(a.crf), "-pix_fmt", "yuv420p",
                "-movflags", "+faststart", "-shortest", out]
    enc = subprocess.Popen(enc_cmd, stdin=subprocess.PIPE)
    menc = None
    if a.mask_video:
        menc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "gray", "-s", f"{W}x{H}",
                                 "-r", f"{fps}", "-i", "-", "-c:v", "libx264", "-crf", "20", "-pix_fmt", "yuv420p",
                                 a.mask_video], stdin=subprocess.PIPE)

    seg = Segmenter(a.model, a.work_px)
    clean = MaskCleaner(a)
    warm = a.start - 0.4  # start segmenting a little early so the temporal filter is settled
    fsize = W * H * 3; i = 0; t0 = time.time(); nseg = 0
    while True:
        buf = dec.stdout.read(fsize)
        if len(buf) < fsize:
            break
        t = i / fps; i += 1
        frame = np.frombuffer(buf, np.uint8).reshape(H, W, 3)
        k = envelope(t, a)
        m_full = None
        if t >= warm and t <= a.end + 0.05:
            m_full = clean(seg(frame), frame); nseg += 1
        if k <= 0 or m_full is None:
            enc.stdin.write(frame.tobytes())
            if menc: menc.stdin.write(((m_full if m_full is not None else np.zeros((H, W), np.float32)) * 255).astype(np.uint8).tobytes())
            continue
        shift = int(round(rise_px * (1 - k))) if rise_px else 0
        f = frame.astype(np.float32)
        sl = (slice(y0, y1), slice(x0, x1))
        ta = alpha_t[y0 + shift:y1 + shift, x0:x1] if shift else alpha_t[sl]
        tr = rgb_t[y0 + shift:y1 + shift, x0:x1] if shift else rgb_t[sl]
        hh = min(ta.shape[0], y1 - y0)
        reg = f[y0:y0 + hh, x0:x1]
        ta, tr = ta[:hh] * k, tr[:hh] * k
        with_text = tr + reg * (1 - ta[..., None])                  # text over background
        m = m_full[y0:y0 + hh, x0:x1][..., None]
        f[y0:y0 + hh, x0:x1] = reg * m + with_text * (1 - m)        # person back on top
        enc.stdin.write(np.clip(f + 0.5, 0, 255).astype(np.uint8).tobytes())
        if menc: menc.stdin.write((m_full * 255).astype(np.uint8).tobytes())
    dec.stdout.close(); dec.wait()
    enc.stdin.close(); enc.wait()
    if menc: menc.stdin.close(); menc.wait()
    seg.close()
    print(f"{i} frames ({nseg} segmented) in {time.time() - t0:.1f}s -> {out}", file=sys.stderr)


if __name__ == "__main__":
    main()
