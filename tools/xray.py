#!/usr/bin/env python3
"""Reel X-ray: a free, local, CPU-only production breakdown of a reel / Short / video.

    .venv/bin/python -I tools/xray.py SOURCE [-o OUTDIR] [--listen]

SOURCE is an Instagram / YouTube / TikTok URL (downloaded with yt-dlp into a fresh folder, metadata saved like
`yt-dlp -j`) or a local video file. OUTDIR gets:

    meta.json          creator, caption, likes / comments / views (when the platform exposes them), duration, size, fps
    transcript.json    faster-whisper word timings (+ transcript.txt)
    xray.json          every measurement below, machine-readable (doctor.py reads this)
    xray.md            human summary with a production table like the Brain's lessons
    contact_sheet.png  one frame per shot;  changes_sheet.png  one frame per visual change
    timeline.png       scene score, text, faces, loudness, onsets, camera motion and grade over time
    faces_flagged.png  crops of frames whose expression fails the face check (when any)
    earshot_timeline.json  (only with --listen) earshot's labelled listening transcript

Nothing here predicts views. It measures what is on screen and in the mix so it can be compared with the Brain.
Run downloaded media with `python -I` (as above) so nothing next to the video can be imported.
"""
import argparse
import json
import math
import os
import re
import subprocess
import sys
import time

import numpy as np
import cv2

MODELS = os.environ.get('XRAY_MODELS', os.path.expanduser('~/sm-tools/models/xray'))
WHISPER_ROOT = os.environ.get('XRAY_WHISPER_ROOT', os.path.expanduser('~/sm-tools/models/whisper'))
EARSHOT_HOME = os.environ.get('EARSHOT_HOME', os.path.expanduser('~/sm-tools/earshot'))
EARSHOT_PY = os.path.join(EARSHOT_HOME, '.venv', 'bin', 'python')
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_B = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'

# thresholds (documented in tools/README.md)
SCENE_EVENT = 0.08      # ffmpeg scene score for "something changed on screen" (same as Lesson 10's method)
SCENE_HARD = 0.25       # ffmpeg scene score for a hard full-frame change (Lesson 10)
CELL_FULL = 0.90        # share of the 8x8 grid that changed for a sub-0.25 change to still count as full-frame
TEXT_MIN_H = 0.012      # a detected text box must be >= 1.2 % of the frame height
CAPTION_MIN_H = 0.022   # caption / title-scale text: >= 2.2 % of the frame height
SAFE_TOP, SAFE_BOTTOM, SAFE_RIGHT_X, SAFE_RIGHT_Y = 0.13, 0.82, 0.88, 0.50   # Reels UI zones (atom text-safe-zone)
DEAD_DB_BELOW_MEDIAN = 25.0   # atom edit-cut-breaths-no-dead-air: 100 ms windows 25 dB under the median


def log(*a):
    print('[xray]', *a, file=sys.stderr, flush=True)


def sh(cmd, check=True, text=True):
    r = subprocess.run(cmd, capture_output=True, text=text)
    if check and r.returncode != 0:
        raise RuntimeError(f'command failed ({r.returncode}): {" ".join(map(str, cmd))[:300]}\n{(r.stderr or "")[-1500:]}')
    return r


def r2(x, n=2):
    try:
        if x is None or (isinstance(x, float) and not math.isfinite(x)):
            return None
        return round(float(x), n)
    except Exception:
        return None


def fmt_t(t):
    if t is None:
        return '-'
    m, s = divmod(float(t), 60)
    return f'{int(m)}:{s:05.2f}'


# ----------------------------------------------------------------------------------------------- input / meta
def fresh_dir(base):
    d, n = base, 1
    while os.path.exists(d) and os.listdir(d):
        n += 1
        d = f'{base}_{n}'
    os.makedirs(d, exist_ok=True)
    return d


def download(url, outdir, cookies=None):
    import yt_dlp
    d = fresh_dir(os.path.join(outdir, 'source'))
    opts = {'outtmpl': os.path.join(d, '%(id)s.%(ext)s'), 'format': 'bv*+ba/b', 'merge_output_format': 'mp4',
            'quiet': True, 'noprogress': True, 'noplaylist': True}
    if cookies:
        opts['cookiefile'] = cookies
    log('downloading', url, '->', d)
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        info = ydl.sanitize_info(info)
    if info.get('_type') == 'playlist' and info.get('entries'):
        info = info['entries'][0]
    path = None
    for rd in info.get('requested_downloads') or []:
        path = rd.get('filepath') or path
    if not path or not os.path.exists(path):
        vids = [f for f in os.listdir(d) if f.lower().endswith(('.mp4', '.mkv', '.webm', '.mov'))]
        if not vids:
            raise RuntimeError('yt-dlp finished but no video file was found')
        path = os.path.join(d, vids[0])
    with open(os.path.join(outdir, 'source_info.json'), 'w') as fh:
        json.dump(info, fh, indent=1, default=str)
    return path, info


def find_local_info(video, meta_arg=None):
    cands = [meta_arg] if meta_arg else []
    base = os.path.splitext(video)[0]
    cands += [video + '.info.json', base + '.info.json', os.path.join(os.path.dirname(video), 'meta.json'),
              os.path.join(os.path.dirname(video), 'source_info.json')]
    for c in cands:
        if c and os.path.isfile(c):
            try:
                with open(c) as fh:
                    j = json.load(fh)
                if isinstance(j, dict) and ('extractor' in j or 'webpage_url' in j or 'uploader' in j):
                    return j, c
            except Exception:
                pass
    return None, None


def probe(video):
    j = json.loads(sh(['ffprobe', '-v', 'error', '-print_format', 'json', '-show_format', '-show_streams', video]).stdout)
    vs = next((s for s in j['streams'] if s.get('codec_type') == 'video' and not s.get('disposition', {}).get('attached_pic')), None)
    aus = next((s for s in j['streams'] if s.get('codec_type') == 'audio'), None)
    if vs is None:
        raise RuntimeError('no video stream')

    def rate(s):
        try:
            a, b = s.split('/')
            return float(a) / float(b) if float(b) else None
        except Exception:
            return None
    fps = rate(vs.get('avg_frame_rate') or '') or rate(vs.get('r_frame_rate') or '') or 30.0
    w, h = int(vs['width']), int(vs['height'])
    rot = 0
    for sd in vs.get('side_data_list') or []:
        if 'rotation' in sd:
            rot = int(float(sd['rotation']))
    rot = int(vs.get('tags', {}).get('rotate', rot))
    if abs(rot) % 180 == 90:
        w, h = h, w
    dur = float(j['format'].get('duration') or vs.get('duration') or 0)
    return {'width': w, 'height': h, 'fps': round(fps, 3), 'duration': round(dur, 3),
            'nb_frames': int(vs['nb_frames']) if str(vs.get('nb_frames', '')).isdigit() else None,
            'vcodec': vs.get('codec_name'), 'pix_fmt': vs.get('pix_fmt'), 'rotation': rot,
            'color_transfer': vs.get('color_transfer'),
            'has_audio': aus is not None, 'acodec': aus.get('codec_name') if aus else None,
            'audio_rate': int(aus['sample_rate']) if aus and aus.get('sample_rate') else None,
            'audio_channels': aus.get('channels') if aus else None,
            'bitrate_kbps': r2(float(j['format'].get('bit_rate', 0)) / 1000, 0),
            'size_mb': r2(float(j['format'].get('size', 0)) / 1e6, 2)}


def build_meta(video, pr, info, info_path, source):
    m = {'source': source, 'file': os.path.abspath(video)}
    if info:
        m.update({
            'creator': info.get('uploader') or info.get('channel') or info.get('creator'),
            'creator_id': info.get('uploader_id') or info.get('channel_id'),
            'title': info.get('title'), 'caption': info.get('description'),
            'likes': info.get('like_count'), 'comments': info.get('comment_count'),
            'views': info.get('view_count') if info.get('view_count') is not None else info.get('play_count'),
            'upload_date': info.get('upload_date'), 'timestamp': info.get('timestamp'),
            'url': info.get('webpage_url') or info.get('original_url'), 'platform': info.get('extractor_key') or info.get('extractor'),
            'tags': info.get('tags') or None, 'metadata_file': info_path,
        })
    m.update({'duration_s': pr['duration'], 'width': pr['width'], 'height': pr['height'], 'fps': pr['fps'],
              'aspect': f"{pr['width']}:{pr['height']}", 'vcodec': pr['vcodec'], 'has_audio': pr['has_audio'],
              'acodec': pr['acodec'], 'bitrate_kbps': pr['bitrate_kbps'], 'size_mb': pr['size_mb'],
              'hdr': pr.get('color_transfer') in ('smpte2084', 'arib-std-b67')})
    return m


# ----------------------------------------------------------------------------------------------- transcript
def transcribe(video, model_name='small', lang=None):
    from faster_whisper import WhisperModel
    log(f'transcribing with faster-whisper {model_name} (CPU int8)')
    m = WhisperModel(model_name, device='cpu', compute_type='int8', download_root=WHISPER_ROOT)
    segs, info = m.transcribe(video, word_timestamps=True, vad_filter=True, language=lang)
    out = []
    for s in segs:
        out.append({'start': r2(s.start, 3), 'end': r2(s.end, 3), 'text': s.text.strip(),
                    'words': [{'w': w.word.strip(), 's': r2(w.start, 3), 'e': r2(w.end, 3), 'p': r2(w.probability, 3)}
                              for w in (s.words or [])]})
    return {'lang': info.language, 'lang_prob': r2(info.language_probability, 3), 'model': model_name, 'segments': out}


def transcript_metrics(tr, dur):
    words = [w for s in tr['segments'] for w in s['words'] if w['w']]
    if not words:
        return {'n_words': 0}
    st = np.array([w['s'] for w in words])
    en = np.array([w['e'] for w in words])
    # active speech = union of word spans with gaps < 0.5 s bridged
    spans, cs, ce = [], st[0], en[0]
    for a, b in zip(st[1:], en[1:]):
        if a - ce < 0.5:
            ce = max(ce, b)
        else:
            spans.append((cs, ce))
            cs, ce = a, b
    spans.append((cs, ce))
    active = sum(b - a for a, b in spans)
    gaps = [(float(en[i]), float(st[i + 1] - en[i])) for i in range(len(words) - 1) if st[i + 1] - en[i] >= 0.5]
    first3 = ' '.join(w['w'] for w in words if w['s'] < 3.0)
    first_line = tr['segments'][0]['text'] if tr['segments'] else ''
    probs = [w['p'] for w in words if w.get('p') is not None]
    return {'n_words': len(words), 'first_word_s': r2(st[0]), 'last_word_s': r2(en[-1]),
            'speech_span_s': r2(en[-1] - st[0]), 'active_speech_s': r2(active),
            'speech_share': r2(active / dur if dur else 0, 3),
            'wpm_overall': r2(len(words) / dur * 60 if dur else 0, 0),
            'wpm_active': r2(len(words) / active * 60 if active > 0 else 0, 0),
            'first_3s_text': first3, 'first_line': first_line, 'mean_word_prob': r2(np.mean(probs) if probs else None, 3),
            'pauses_ge_0_5s': [{'t': r2(t), 'dur': r2(d)} for t, d in gaps],
            'spans': [[r2(a), r2(b)] for a, b in spans]}


# ----------------------------------------------------------------------------------------------- scene scores
def scene_scores(video):
    """per-frame ffmpeg scene score (the same number `select='gt(scene,X)'` thresholds)."""
    r = sh(['ffmpeg', '-hide_banner', '-nostats', '-loglevel', 'info', '-i', video, '-an',
            '-vf', "select='gte(scene,0)',metadata=print", '-f', 'null', '-'])
    ts, sc = [], []
    cur_t = None
    for line in r.stderr.splitlines():
        m = re.search(r'pts_time:([-\d.]+)', line)
        if m:
            cur_t = float(m.group(1))
            continue
        m = re.search(r'lavfi\.scene_score=([\d.]+)', line)
        if m and cur_t is not None:
            ts.append(cur_t)
            sc.append(float(m.group(1)))
            cur_t = None
    return np.array(ts), np.array(sc)


def cluster_events(ts, sc, thr, gap=0.2):
    idx = np.where(sc > thr)[0]
    ev = []
    for i in idx:
        if ev and ts[i] - ts[ev[-1]['last']] <= gap:
            e = ev[-1]
            e['last'] = i
            if sc[i] > e['score']:
                e['score'], e['i'] = float(sc[i]), int(i)
        else:
            ev.append({'i': int(i), 'first': int(i), 'last': int(i), 'score': float(sc[i])})
    for e in ev:
        e['t'] = float(ts[e['i']])
        e['span_s'] = float(ts[e['last']] - ts[e['first']])
    return ev


# ----------------------------------------------------------------------------------------------- frame pass
def analysis_size(w, h, long_side=480):
    s = long_side / max(w, h)
    return int(round(w * s / 2) * 2), int(round(h * s / 2) * 2)


def frame_pass(video, pr, want_idx):
    """one decode at ~480 px: grid differences, grade stats, camera motion (LK + partial affine), flow energy.
    want_idx: frame indices whose small frames to keep (sheets, punch-in checks)."""
    aw, ah = analysis_size(pr['width'], pr['height'])
    cmd = ['ffmpeg', '-v', 'error', '-i', video, '-an', '-vf', f'scale={aw}:{ah}', '-f', 'rawvideo', '-pix_fmt', 'bgr24', '-']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    fsz = aw * ah * 3
    G = 8
    cx, cy = aw / 2, ah / 2
    rows = []
    keep = {}
    want = set(want_idx)
    prev_g = prev_gb = prev_small = None
    i = 0
    while True:
        buf = p.stdout.read(fsz)
        if len(buf) < fsz:
            break
        f = np.frombuffer(buf, np.uint8).reshape(ah, aw, 3)
        g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        gb = cv2.GaussianBlur(g, (5, 5), 0)
        yuv = cv2.cvtColor(f, cv2.COLOR_BGR2YUV)
        u = yuv[..., 1].astype(np.float32) - 128
        v = yuv[..., 2].astype(np.float32) - 128
        hsv_s = cv2.cvtColor(f, cv2.COLOR_BGR2HSV)[..., 1]
        bm, gm, rm = f[..., 0].mean(), f[..., 1].mean(), f[..., 2].mean()
        row = {'Y': float(g.mean()), 'contrast': float(g.std()), 'p2': float(np.percentile(g, 2)),
               'p98': float(np.percentile(g, 98)), 'sat': float(np.sqrt(u * u + v * v).mean()),
               'hsv_s': float(hsv_s.mean()), 'warmth': float(rm - bm),
               'cellfrac': 0.0, 'diff': 0.0, 's': np.nan, 'tx': np.nan, 'ty': np.nan, 'rot': np.nan, 'inl': 0.0,
               'flow': np.nan}
        if prev_gb is not None:
            d = cv2.absdiff(gb, prev_gb).astype(np.float32)
            cells = cv2.resize(d, (G, G), interpolation=cv2.INTER_AREA)
            row['cellfrac'] = float((cells > 10).mean())
            row['diff'] = float(d.mean())
            pts = cv2.goodFeaturesToTrack(prev_g, 300, 0.01, 7)
            if pts is not None and len(pts) >= 15:
                nxt, st, _ = cv2.calcOpticalFlowPyrLK(prev_g, g, pts, None, winSize=(21, 21), maxLevel=3)
                ok = st.ravel() == 1
                if ok.sum() >= 12:
                    a0 = pts[ok].reshape(-1, 2) - (cx, cy)
                    a1 = nxt[ok].reshape(-1, 2) - (cx, cy)
                    M, inl = cv2.estimateAffinePartial2D(a0, a1, method=cv2.RANSAC, ransacReprojThreshold=1.5)
                    if M is not None:
                        row['s'] = float(math.hypot(M[0, 0], M[1, 0]))
                        row['rot'] = float(math.degrees(math.atan2(M[1, 0], M[0, 0])))
                        row['tx'], row['ty'] = float(M[0, 2]), float(M[1, 2])
                        row['inl'] = float(inl.mean()) if inl is not None else 0.0
            if i % 3 == 0:
                sm = cv2.resize(g, (aw // 2, ah // 2), interpolation=cv2.INTER_AREA)
                if prev_small is not None:
                    fl = cv2.calcOpticalFlowFarneback(prev_small, sm, None, 0.5, 2, 13, 2, 5, 1.1, 0)
                    row['flow'] = float(np.linalg.norm(fl, axis=2).mean() / (aw / 2) * 100)  # % of width per 3 frames
                prev_small = sm
        elif i == 0:
            prev_small = cv2.resize(g, (aw // 2, ah // 2), interpolation=cv2.INTER_AREA)
        if i in want:
            keep[i] = f.copy()
        rows.append(row)
        prev_g, prev_gb = g, gb
        i += 1
    p.wait()
    cols = {k: np.array([r[k] for r in rows], dtype=np.float64) for k in rows[0]} if rows else {}
    return cols, keep, (aw, ah)


# ----------------------------------------------------------------------------------------------- cuts, shots, moves
def classify_boundary(fa, fb):
    """compare the last frame before a cut with the first after: same framing scaled = punch-in / punch-out."""
    orb = cv2.ORB_create(800)
    ga, gb = cv2.cvtColor(fa, cv2.COLOR_BGR2GRAY), cv2.cvtColor(fb, cv2.COLOR_BGR2GRAY)
    ka, da = orb.detectAndCompute(ga, None)
    kb, db = orb.detectAndCompute(gb, None)
    if da is None or db is None or len(ka) < 20 or len(kb) < 20:
        return 'new shot', None
    mt = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True).match(da, db)
    if len(mt) < 20:
        return 'new shot', None
    h, w = ga.shape
    pa = np.float32([ka[m.queryIdx].pt for m in mt]) - (w / 2, h / 2)
    pb = np.float32([kb[m.trainIdx].pt for m in mt]) - (w / 2, h / 2)
    M, inl = cv2.estimateAffinePartial2D(pa, pb, method=cv2.RANSAC, ransacReprojThreshold=3.0)
    if M is None or inl is None or inl.sum() < 25 or inl.mean() < 0.3:
        return 'new shot', None
    s = math.hypot(M[0, 0], M[1, 0])
    if s > 1.04:
        return 'punch-in', s
    if s < 0.96:
        return 'punch-out', s
    return 'jump cut (same framing)', s


def smooth(x, k=5):
    x = np.asarray(x, float)
    if len(x) < k:
        return x
    pad = k // 2
    xp = np.pad(x, pad, mode='edge')
    med = np.array([np.median(xp[j:j + k]) for j in range(len(x))])
    return np.convolve(np.pad(med, 1, mode='edge'), np.ones(3) / 3, mode='valid')


def find_moves(cols, shots, fps, aw, ah):
    """continuous zooms / pans inside shots from the per-frame partial-affine fit; classify their speed curve."""
    moves = []
    n = len(cols['s'])
    for sh_ in shots:
        a, b = sh_['i0'] + 1, sh_['i1']   # skip the first frame (its motion is measured across the cut)
        if b - a < int(0.5 * fps):
            continue
        seg = slice(a, b)
        s = np.nan_to_num(cols['s'][seg], nan=1.0)
        tx = np.nan_to_num(cols['tx'][seg], nan=0.0)
        ty = np.nan_to_num(cols['ty'][seg], nan=0.0)
        zr = smooth(np.log(np.clip(s, 0.5, 2.0))) * fps          # log-zoom per second
        pxs = smooth(tx / aw) * fps                                # share of width per second
        pys = smooth(ty / ah) * fps
        for kind, sp, thr in (('zoom', zr, 0.03), ('pan-x', pxs, 0.04), ('pan-y', pys, 0.04)):
            mask = np.abs(sp) > thr
            j = 0
            L = len(sp)
            while j < L:
                if not mask[j]:
                    j += 1
                    continue
                sign = np.sign(sp[j])
                k = j
                gapc = 0
                while k + 1 < L and (mask[k + 1] and np.sign(sp[k + 1]) == sign or gapc < 2):
                    k += 1
                    if mask[k] and np.sign(sp[k]) == sign:
                        gapc = 0
                    else:
                        gapc += 1
                k -= gapc
                if (k - j + 1) / fps >= 0.4:
                    v = np.abs(sp[j:k + 1]) * (np.sign(sp[j:k + 1]) == sign)
                    vmax = np.percentile(v, 90)
                    # extend while the move is still going (catch slow ease-in / ease-out tails)
                    j0, k0 = j, k
                    while j0 > 0 and sp[j0 - 1] * sign > 0.15 * vmax:
                        j0 -= 1
                    while k0 + 1 < L and sp[k0 + 1] * sign > 0.15 * vmax:
                        k0 += 1
                    # speed-curve shape from the RAW per-frame motion (smoothing would invent ramps):
                    # cumulative displacement vs the straight chord. Linear motion = a straight line.
                    if kind == 'zoom':
                        raw = np.log(np.clip(np.nan_to_num(cols['s'][a + j0:a + k0 + 1], nan=1.0), 0.5, 2.0))
                    elif kind == 'pan-x':
                        raw = np.nan_to_num(cols['tx'][a + j0:a + k0 + 1]) / aw
                    else:
                        raw = np.nan_to_num(cols['ty'][a + j0:a + k0 + 1]) / ah
                    total = float(np.sum(raw))
                    nn = len(raw)
                    if abs(total) < 1e-9 or nn < 6:
                        j = k + 1
                        continue
                    pcum = np.cumsum(raw) / total
                    dev = float(np.max(np.abs(pcum - np.arange(1, nn + 1) / nn)))
                    spn = raw / (total / nn)
                    jit = float(np.std(spn - smooth(spn)))
                    th = [float(np.mean(x)) for x in np.array_split(spn, 3)]
                    if dev <= 0.04:
                        curve = 'linear (constant speed)'
                    elif jit > 0.6:
                        curve = 'irregular / handheld'
                    elif dev >= 0.07:
                        curve = 'eased (' + ('ease-in-out' if th[1] > max(th[0], th[2]) else 'ease-out' if th[0] > th[2] else 'ease-in') + ')'
                    else:
                        curve = 'near-linear'
                    t0 = (a + j0) / fps
                    moves.append({'kind': kind, 't0': r2(t0), 't1': r2((a + k0 + 1) / fps), 'dur': r2((k0 - j0 + 1) / fps),
                                  'total': r2((math.exp(total) - 1) * 100 if kind == 'zoom' else total * 100, 1),
                                  'unit': '% zoom' if kind == 'zoom' else ('% of width' if kind == 'pan-x' else '% of height'),
                                  'chord_dev': r2(dev, 3), 'jitter': r2(jit), 'speed_thirds': [r2(x) for x in th],
                                  'curve': curve, 'whole_shot': bool(j0 <= 1 and k0 >= L - 2), 'shot': sh_['n']})
                    k = max(k, k0)
                j = k + 1
    return moves


# ----------------------------------------------------------------------------------------------- sample pass
class TextModels:
    def __init__(self, ocr=True):
        self.det = self.rec = None
        p = os.path.join(MODELS, 'text_detection_en_ppocrv3_2023may.onnx')
        if os.path.exists(p):
            self.det = cv2.dnn.TextDetectionModel_DB(p)
            self.det.setBinaryThreshold(0.3).setPolygonThreshold(0.5).setMaxCandidates(200).setUnclipRatio(2.0)
        q = os.path.join(MODELS, 'text_recognition_CRNN_EN_2021sep.onnx')
        if ocr and os.path.exists(q):
            self.rec = cv2.dnn.TextRecognitionModel(q)
            self.rec.setDecodeType('CTC-greedy')
            self.rec.setVocabulary(list('0123456789abcdefghijklmnopqrstuvwxyz'))
            self.rec.setInputParams(1 / 127.5, (100, 32), (127.5, 127.5, 127.5))

    def detect(self, f):
        h, w = f.shape[:2]
        ih = 736
        iw = max(32, int(round(w * ih / h / 32)) * 32)
        self.det.setInputParams(1.0 / 255.0, (iw, ih), (122.67891434, 116.66876762, 104.00698793), True)
        boxes, conf = self.det.detect(f)
        out = []
        for b, c in zip(boxes, conf if len(conf) else [None] * len(boxes)):
            b = np.array(b, np.float32)
            x, y, bw, bh = cv2.boundingRect(b)
            rect = cv2.minAreaRect(b)
            th = min(rect[1]) / h
            if th < TEXT_MIN_H:
                continue
            txt = ''
            if self.rec is not None:
                txt = self._read(f, b)
            out.append({'x0': r2(max(0, x) / w, 3), 'y0': r2(max(0, y) / h, 3), 'x1': r2(min(w, x + bw) / w, 3),
                        'y1': r2(min(h, y + bh) / h, 3), 'h': r2(th, 4), 'conf': r2(c, 2) if c is not None else None,
                        'text': txt})
        return out

    def _read(self, f, poly):
        rect = cv2.minAreaRect(poly)
        (cx, cy), (rw, rh), ang = rect
        if rw < rh:
            rw, rh, ang = rh, rw, ang + 90
        M = cv2.getRotationMatrix2D((cx, cy), ang, 1.0)
        rot = cv2.warpAffine(f, M, (f.shape[1], f.shape[0]), flags=cv2.INTER_LINEAR)
        pad = rh * 0.12
        crop = cv2.getRectSubPix(rot, (int(rw + 2 * pad), int(rh + 2 * pad)), (cx, cy))
        if crop.size == 0:
            return ''
        g = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)
        # the CRNN reads ~ aspect 3:1; read long lines in overlapping chunks
        H, W = g.shape
        step = int(H * 3.2)
        parts = []
        x = 0
        while x < W:
            c = g[:, x:min(W, x + step)]
            if c.shape[1] >= H * 0.6:
                c3 = cv2.cvtColor(c, cv2.COLOR_GRAY2BGR)
                try:
                    parts.append(self.rec.recognize(cv2.resize(c3, (100, 32))))
                except Exception:
                    pass
            x += step
        return ''.join(parts)


class FaceModel:
    def __init__(self):
        self.kind = None
        self.err = None
        try:
            import mediapipe as mp
            from mediapipe.tasks.python import vision, BaseOptions
            p = os.path.join(MODELS, 'face_landmarker.task')
            if not os.path.exists(p):
                raise FileNotFoundError(p)
            self.mp = mp
            self.fl = vision.FaceLandmarker.create_from_options(vision.FaceLandmarkerOptions(
                base_options=BaseOptions(model_asset_path=p), output_face_blendshapes=True,
                output_facial_transformation_matrixes=True, num_faces=4,
                min_face_detection_confidence=0.5, min_face_presence_confidence=0.5))
            self.kind = 'mediapipe-face-landmarker'
        except Exception as e:
            self.err = f'{type(e).__name__}: {e}'
            p = os.path.join(MODELS, 'face_detection_yunet_2023mar.onnx')
            if os.path.exists(p):
                self.yn = cv2.FaceDetectorYN.create(p, '', (320, 320), 0.7)
                self.kind = 'opencv-yunet (presence only)'

    def detect(self, f):
        h, w = f.shape[:2]
        out = []
        if self.kind and self.kind.startswith('mediapipe'):
            res = self.fl.detect(self.mp.Image(image_format=self.mp.ImageFormat.SRGB, data=cv2.cvtColor(f, cv2.COLOR_BGR2RGB)))
            for k, lm in enumerate(res.face_landmarks):
                xs = [p.x for p in lm]
                ys = [p.y for p in lm]
                bs = {c.category_name: c.score for c in res.face_blendshapes[k]} if res.face_blendshapes else {}
                yaw = pitch = None
                if res.facial_transformation_matrixes:
                    R = np.array(res.facial_transformation_matrixes[k])[:3, :3]
                    yaw = math.degrees(math.atan2(-R[2, 0], math.hypot(R[2, 1], R[2, 2])))
                    pitch = math.degrees(math.atan2(R[2, 1], R[2, 2]))
                out.append({'x0': r2(min(xs), 3), 'y0': r2(min(ys), 3), 'x1': r2(max(xs), 3), 'y1': r2(max(ys), 3),
                            'size': r2(max(ys) - min(ys), 3),
                            'blinkL': r2(bs.get('eyeBlinkLeft'), 2), 'blinkR': r2(bs.get('eyeBlinkRight'), 2),
                            'jawOpen': r2(bs.get('jawOpen'), 2), 'tongueOut': r2(bs.get('tongueOut'), 2),
                            'smile': r2((bs.get('mouthSmileLeft', 0) + bs.get('mouthSmileRight', 0)) / 2, 2),
                            'yaw': r2(yaw, 1), 'pitch': r2(pitch, 1)})
        elif self.kind:
            self.yn.setInputSize((w, h))
            _, faces = self.yn.detect(f)
            for fc in faces if faces is not None else []:
                x, y, fw, fh = fc[:4]
                out.append({'x0': r2(x / w, 3), 'y0': r2(y / h, 3), 'x1': r2((x + fw) / w, 3), 'y1': r2((y + fh) / h, 3),
                            'size': r2(fh / h, 3)})
        return out


def face_flags(fc):
    """face-check heuristics on MediaPipe blendshapes (SYSTEM_PROMPT face-check rule). Advisory, not a verdict."""
    fl = []
    if fc.get('blinkL') is None:
        return fl
    b = min(fc['blinkL'], fc['blinkR'])
    if b >= 0.5:
        fl.append('eyes closed / mid-blink')
    elif b >= 0.35:
        fl.append('eyes half-closed')
    if (fc.get('jawOpen') or 0) >= 0.45:
        fl.append('mouth wide open')
    elif (fc.get('jawOpen') or 0) >= 0.22:
        fl.append('mouth open (mid-word?)')
    if (fc.get('tongueOut') or 0) >= 0.3:
        fl.append('tongue showing')
    if fc.get('yaw') is not None and (abs(fc['yaw']) > 40 or abs(fc['pitch'] or 0) > 30):
        fl.append('awkward angle')
    return fl


def sample_pass(video, pr, fps_s=2.0, ocr=True, faces=True):
    tm = TextModels(ocr=ocr)
    fm = FaceModel() if faces else None
    cap = cv2.VideoCapture(video)
    fps = pr['fps']
    dur = pr['duration']
    times = [0.1] + list(np.arange(0.5, dur, 1.0 / fps_s))
    want = sorted(set(min(int(round(t * fps)), int(dur * fps) - 1) for t in times))
    samples, palette_px, keep = [], [], {}
    wi = 0
    i = 0
    last_small = last_text = None
    while wi < len(want):
        ok = cap.grab()
        if not ok:
            break
        if i == want[wi]:
            ok, f = cap.retrieve()
            wi += 1
            if ok:
                t = i / fps
                small = cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (64, 114))
                rec = {'t': r2(t, 2)}
                if tm.det is not None:
                    if last_small is not None and cv2.absdiff(small, last_small).mean() < 1.2:
                        rec['text'] = last_text
                    else:
                        rec['text'] = tm.detect(f)
                        last_small, last_text = small, rec['text']
                if fm is not None and fm.kind:
                    rec['faces'] = fm.detect(f)
                    for fc in rec['faces']:
                        fc['flags'] = face_flags(fc)
                    if any(fc['flags'] for fc in rec['faces']):
                        keep[i] = f
                palette_px.append(cv2.resize(f, (36, 64), interpolation=cv2.INTER_AREA).reshape(-1, 3))
                samples.append(rec)
        i += 1
    cap.release()
    if fm is not None and fm.kind and fm.kind.startswith('mediapipe'):
        try:
            fm.fl.close()
        except Exception:
            pass
    info = {'text_model': 'opencv-zoo PP-OCRv3 DB detector' if tm.det is not None else None,
            'ocr': 'opencv-zoo CRNN EN (rough: lowercase, no spaces)' if tm.rec is not None else None,
            'face_model': fm.kind if fm else None, 'face_model_error': fm.err if fm else None,
            'sample_fps': fps_s}
    return samples, (np.concatenate(palette_px) if palette_px else None), keep, info


def palette(px, k=6):
    if px is None or len(px) < k:
        return []
    data = px.astype(np.float32)
    if len(data) > 60000:
        data = data[np.random.default_rng(0).choice(len(data), 60000, replace=False)]
    crit = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.5)
    cv2.setRNGSeed(1)
    _, lab, cen = cv2.kmeans(data, k, None, crit, 3, cv2.KMEANS_PP_CENTERS)
    cnt = np.bincount(lab.ravel(), minlength=k) / len(lab)
    order = np.argsort(-cnt)
    return [{'hex': '#%02x%02x%02x' % (int(cen[j][2]), int(cen[j][1]), int(cen[j][0])), 'share': r2(cnt[j], 3)} for j in order]


# ----------------------------------------------------------------------------------------------- audio
def decode_audio(video, sr=22050):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', video, '-vn', '-ac', '1', '-ar', str(sr), '-f', 'f32le', '-'],
                       capture_output=True)
    return np.frombuffer(r.stdout, np.float32).copy(), sr


def ebur128(video):
    r = sh(['ffmpeg', '-hide_banner', '-nostats', '-i', video, '-vn', '-filter_complex',
            'ebur128=peak=true:framelog=verbose', '-f', 'null', '-'], check=False)
    tt, mm, ss = [], [], []
    for line in r.stderr.splitlines():
        m = re.search(r't:\s*([\d.]+)\s+TARGET:.*?M:\s*([-\d.]+)\s+S:\s*([-\d.]+)', line)
        if m:
            tt.append(float(m.group(1)))
            mm.append(float(m.group(2)))
            ss.append(float(m.group(3)))
    summ = r.stderr[r.stderr.rfind('Summary:'):] if 'Summary:' in r.stderr else ''
    def grab(pat):
        m = re.search(pat, summ, re.S)
        return float(m.group(1)) if m else None
    return {'integrated_lufs': grab(r'I:\s*([-\d.]+) LUFS'), 'lra_lu': grab(r'LRA:\s*([-\d.]+) LU'),
            'true_peak_dbtp': grab(r'True peak:\s*Peak:\s*([-\d.]+) dBFS')}, np.array(tt), np.array(mm), np.array(ss)


def silencedetect(video, noise=-40, d=0.25):
    r = sh(['ffmpeg', '-hide_banner', '-nostats', '-i', video, '-vn', '-af', f'silencedetect=n={noise}dB:d={d}',
            '-f', 'null', '-'], check=False)
    out, st = [], None
    for line in r.stderr.splitlines():
        m = re.search(r'silence_start:\s*([-\d.]+)', line)
        if m:
            st = float(m.group(1))
        m = re.search(r'silence_end:\s*([-\d.]+)\s*\|\s*silence_duration:\s*([\d.]+)', line)
        if m:
            out.append({'start': r2(max(0, float(m.group(1)) - float(m.group(2)))), 'dur': r2(float(m.group(2)))})
            st = None
    if st is not None:
        out.append({'start': r2(st), 'dur': None, 'note': 'runs to the end'})
    return out


def onsets(x, sr):
    """spectral-flux onsets with a local prominence in dB. Returns times, strength, prominence, centroid."""
    n_fft, hop = 1024, 256
    if len(x) < n_fft * 4:
        return [], (np.zeros(0), np.zeros(0), np.zeros(0))
    win = np.hanning(n_fft).astype(np.float32)
    nfr = 1 + (len(x) - n_fft) // hop
    idx = np.arange(n_fft)[None, :] + hop * np.arange(nfr)[:, None]
    S = np.abs(np.fft.rfft(x[idx] * win, axis=1))
    L = np.log1p(100 * S)
    flux = np.maximum(0, np.diff(L, axis=0)).sum(axis=1)
    flux = np.concatenate([[0], flux])
    rms = np.sqrt((x[idx] ** 2).mean(axis=1)) + 1e-9
    db = 20 * np.log10(rms)
    freqs = np.fft.rfftfreq(n_fft, 1 / sr)
    cent = (S * freqs).sum(axis=1) / (S.sum(axis=1) + 1e-9)
    fr_t = (np.arange(nfr) * hop + n_fft / 2) / sr
    w = int(0.5 * sr / hop)
    med = np.array([np.median(flux[max(0, j - w):j + w + 1]) for j in range(nfr)])
    mad = np.median(np.abs(flux - np.median(flux))) + 1e-9
    thr = med + 2.5 * mad
    nb = int(0.05 * sr / hop)
    out = []
    last = -1e9
    for j in range(1, nfr - 1):
        if flux[j] > thr[j] and flux[j] == flux[max(0, j - nb):j + nb + 1].max() and fr_t[j] - last > 0.06:
            pre = db[max(0, j - int(0.15 * sr / hop)):max(1, j - 1)]
            post = db[j:j + max(1, int(0.03 * sr / hop))]
            prom = float(post.max() - np.percentile(pre, 20)) if len(pre) else 0.0
            out.append({'t': float(fr_t[j]), 'strength': float(flux[j] / (np.percentile(flux, 95) + 1e-9)),
                        'prom_db': prom, 'centroid_hz': float(cent[j]), 'level_db': float(post.max())})
            last = fr_t[j]
    return out, (fr_t, flux, db)


def window_levels(x, sr, win=0.1):
    n = int(win * sr)
    m = len(x) // n
    if m == 0:
        return np.array([]), np.array([])
    seg = x[:m * n].reshape(m, n)
    db = 10 * np.log10((seg ** 2).mean(axis=1) + 1e-12)
    return (np.arange(m) + 0.5) * win, db


def runs(mask, t, win):
    out, st = [], None
    for k, v in enumerate(mask):
        if v and st is None:
            st = k
        if (not v or k == len(mask) - 1) and st is not None:
            e = k + 1 if v else k
            out.append({'start': r2(t[st] - win / 2), 'dur': r2((e - st) * win)})
            st = None
    return out


def pulse(fr_t, flux):
    if len(flux) < 200:
        return None, 0.0
    env = flux - np.convolve(flux, np.ones(9) / 9, mode='same')
    env = np.maximum(env, 0)
    env = env - env.mean()
    ac = np.correlate(env, env, mode='full')[len(env) - 1:]
    ac = ac / (ac[0] + 1e-9)
    dt = fr_t[1] - fr_t[0]
    lo, hi = int(60 / 200 / dt), int(60 / 60 / dt)
    if hi >= len(ac):
        return None, 0.0
    k = lo + int(np.argmax(ac[lo:hi]))
    bpm = 60 / (k * dt)
    while bpm < 80:
        bpm *= 2
    while bpm > 170:
        bpm /= 2
    return round(bpm, 1), float(ac[k])


def audio_pass(video, pr, tr_metrics):
    x, sr = decode_audio(video)
    if len(x) == 0:
        return {'present': False}
    summary, tt, mm, ss = ebur128(video)
    sil = silencedetect(video)
    wt, wdb = window_levels(x, sr, 0.1)
    live = wdb[wdb > -80]
    med = float(np.median(live)) if len(live) else -80.0
    dead = (wdb < med - DEAD_DB_BELOW_MEDIAN) | (wdb < -60)
    dead_runs = [r for r in runs(dead, wt, 0.1)]
    ons, (fr_t, flux, fdb) = onsets(x, sr)
    # speech mask from the transcript
    spans = (tr_metrics or {}).get('spans') or []
    def in_speech(t, pad=0.0):
        return any(a - pad <= t <= b + pad for a, b in spans)
    sp_mask = np.array([in_speech(t) for t in wt]) if spans else np.zeros(len(wt), bool)
    speech_db = float(np.median(wdb[sp_mask])) if sp_mask.sum() >= 5 else None
    gap_mask = (~sp_mask) & (wdb > -70)
    if spans:  # only gaps inside the speaking part (outside it, music may be the whole show)
        gap_mask &= (wt > spans[0][0]) & (wt < spans[-1][1])
    bed_db = float(np.median(wdb[gap_mask])) if gap_mask.sum() >= 5 else None
    # transients: strong, prominent onsets (SFX, hits, drums, but also hard consonants in speech)
    strong = [o for o in ons if o['prom_db'] >= 9 and o['strength'] >= 0.8]
    for o in strong:
        o['in_speech'] = bool(in_speech(o['t'], 0.05)) if spans else False
    off_speech = [o for o in strong if not o['in_speech']]
    bpm, clarity = pulse(fr_t, flux)
    if speech_db is None:
        mix = 'no voice detected' + ('; music/sound only' if med > -45 else '; near-silent')
    elif bed_db is None or bed_db < -55 or (speech_db - bed_db) > 30:
        mix = 'voice with no audible bed in the pauses'
    else:
        mix = f'voice over a bed ~{speech_db - bed_db:.0f} dB under the voice'
    return {'present': True, **{k: r2(v, 1) for k, v in summary.items()},
            'median_window_db': r2(med, 1), 'mix': mix, 'speech_level_db': r2(speech_db, 1), 'bed_level_db': r2(bed_db, 1),
            'bed_under_voice_db': r2(speech_db - bed_db, 1) if speech_db is not None and bed_db is not None else None,
            'dead_window_pct': r2(100 * dead.mean(), 2), 'dead_runs': dead_runs,
            'longest_dead_s': r2(max([r['dur'] for r in dead_runs], default=0.0)),
            'silences_40db': sil, 'onset_count': len(ons), 'onsets_per_s': r2(len(ons) / pr['duration'], 2),
            'transients': [{k: r2(v, 2) if isinstance(v, float) else v for k, v in o.items()} for o in strong],
            'transients_per_s': r2(len(strong) / pr['duration'], 2),
            'sfx_candidates': [{k: r2(v, 2) if isinstance(v, float) else v for k, v in o.items()} for o in off_speech],
            'tempo_bpm': bpm if clarity >= 0.15 else None, 'pulse_clarity': r2(clarity, 2),
            '_series': {'ebur_t': tt, 'M': mm, 'S': ss, 'win_t': wt, 'win_db': wdb, 'flux_t': fr_t, 'flux': flux}}


def earshot_listen(video, outdir):
    out = os.path.join(outdir, 'earshot_timeline.json')
    if not os.path.exists(EARSHOT_PY):
        return None, f'earshot venv not found at {EARSHOT_PY}'
    code = ('import json,sys\nfrom earshot import api\n'
            'r=api.timeline(sys.argv[1], detail="normal")\n'
            'json.dump(r, open(sys.argv[2],"w"), indent=1, default=str)\n')
    env = dict(os.environ, EARSHOT_HOME=EARSHOT_HOME)
    log('earshot timeline (loads its models; can take minutes)...')
    r = subprocess.run([EARSHOT_PY, '-I', '-c', code, os.path.abspath(video), out], capture_output=True, text=True,
                       env=env, cwd=outdir, timeout=3600)
    if r.returncode != 0 or not os.path.exists(out):
        return None, (r.stderr or '')[-800:]
    with open(out) as fh:
        return json.load(fh), None


# ----------------------------------------------------------------------------------------------- pictures
def _font(sz, bold=False):
    from PIL import ImageFont
    try:
        return ImageFont.truetype(FONT_B if bold else FONT, sz)
    except Exception:
        return ImageFont.load_default()


def sheet(frames, labels, path, cols=None, title=None, tw=180):
    from PIL import Image, ImageDraw
    if not frames:
        return None
    n = len(frames)
    cols = cols or min(8, max(3, int(math.ceil(math.sqrt(n * 1.6)))))
    h0, w0 = frames[0].shape[:2]
    th = int(tw * h0 / w0)
    lab_h = 34
    top = 30 if title else 0
    rows = int(math.ceil(n / cols))
    im = Image.new('RGB', (cols * (tw + 6) + 6, top + rows * (th + lab_h + 6) + 6), (18, 18, 20))
    d = ImageDraw.Draw(im)
    if title:
        d.text((8, 6), title, fill=(235, 235, 235), font=_font(16, True))
    for k, (f, lab) in enumerate(zip(frames, labels)):
        r_, c_ = divmod(k, cols)
        x, y = 6 + c_ * (tw + 6), top + 6 + r_ * (th + lab_h + 6)
        im.paste(Image.fromarray(cv2.cvtColor(cv2.resize(f, (tw, th), interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2RGB)), (x, y))
        for li, line in enumerate(lab.split('\n')[:2]):
            d.text((x + 2, y + th + 2 + li * 15), line, fill=(220, 220, 220) if li == 0 else (160, 160, 160), font=_font(12, li == 0))
    im.save(path)
    return path


def timeline_png(path, X):
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    dur = X['meta']['duration_s']
    rows = 5
    fig, ax = plt.subplots(rows, 1, figsize=(16, 10), sharex=True, gridspec_kw={'hspace': 0.35})
    c = X['cuts']
    a0 = ax[0]
    a0.plot(c['_t'], c['_scene'], lw=0.6, color='#555')
    a0.axhline(SCENE_EVENT, color='#e9a', lw=0.6, ls='--')
    a0.axhline(SCENE_HARD, color='#c33', lw=0.6, ls='--')
    for e in c['events']:
        a0.axvline(e['t'], color='#c33' if e['type'] == 'full-frame' else '#e90', lw=0.8, alpha=0.7)
    a0.set_ylabel('scene\nscore')
    a0.set_title('visual changes (red = full-frame, orange = overlay / partial), dashed = 0.08 / 0.25 thresholds', fontsize=9, loc='left')
    a1 = ax[1]
    ts = [s['t'] for s in X['samples']]
    if X['text']['available']:
        a1.step(ts, [1 if any(b['h'] >= CAPTION_MIN_H and b.get('static') for b in (s.get('text') or [])) else 0 for s in X['samples']], where='post', color='#28a', label='caption-scale overlay text')
        a1.step(ts, [0.5 if (s.get('text') or []) else 0 for s in X['samples']], where='post', color='#8bd', label='any text')
    if X['faces']['model']:
        a1.scatter(ts, [-0.25 if s.get('faces') else np.nan for s in X['samples']], s=6, color='#4a4', label='face')
        fl = [(s['t']) for s in X['samples'] if any(f.get('flags') for f in s.get('faces') or [])]
        a1.scatter(fl, [-0.25] * len(fl), s=18, color='#d22', marker='x', label='face flagged')
    a1.set_ylim(-0.5, 1.2)
    a1.legend(fontsize=7, loc='upper right', ncol=4)
    a1.set_ylabel('text /\nfaces')
    a2 = ax[2]
    au = X['audio']
    if au.get('present'):
        s_ = au['_series']
        a2.plot(s_['win_t'], s_['win_db'], lw=0.5, color='#999', label='100 ms level dBFS')
        if len(s_['ebur_t']):
            a2.plot(s_['ebur_t'], s_['M'], lw=0.8, color='#36c', label='momentary LUFS')
        for o in au['sfx_candidates']:
            a2.axvline(o['t'], color='#e50', lw=0.7, alpha=0.8)
        for r in au['dead_runs']:
            a2.axvspan(r['start'], r['start'] + r['dur'], color='#f99', alpha=0.4)
        for sp in (X['transcript'].get('metrics') or {}).get('spans') or []:
            a2.axvspan(sp[0], sp[1], ymin=0.95, ymax=1.0, color='#4a4', alpha=0.8)
        a2.set_ylim(-70, 0)
        a2.legend(fontsize=7, loc='lower right')
        a2.set_title('audio: green bar = speech, orange lines = SFX/hit candidates, red = dead air', fontsize=9, loc='left')
    else:
        a2.text(0.5, 0.5, 'no audio stream (silent export)', ha='center', va='center', transform=a2.transAxes)
    a2.set_ylabel('dB')
    a3 = ax[3]
    m = X['motion']
    a3.plot(m['_t'], m['_zoom_rate'], lw=0.6, color='#a3c', label='zoom %/s')
    a3.plot(m['_t'], m['_pan_rate'], lw=0.6, color='#3a9', label='pan % width/s')
    for mv in m['moves']:
        a3.axvspan(mv['t0'], mv['t1'], color='#f55' if mv['curve'].startswith('linear') else '#ddd', alpha=0.35)
    a3.set_ylim(-60, 60)
    a3.legend(fontsize=7, loc='upper right')
    a3.set_ylabel('camera')
    a3.set_title('camera motion (shaded = detected move; red = constant speed / linear)', fontsize=9, loc='left')
    a4 = ax[4]
    g = X['colour']
    a4.plot(g['_t'], g['_Y'], lw=0.8, color='#333', label='mean luma')
    a4.plot(g['_t'], g['_contrast'], lw=0.8, color='#888', label='contrast (luma sd)')
    a4.plot(g['_t'], np.array(g['_sat']) * 3, lw=0.8, color='#d70', label='saturation x3')
    a4.legend(fontsize=7, loc='upper right')
    a4.set_ylabel('grade')
    a4.set_xlabel('seconds')
    a4.set_xlim(0, dur)
    fig.suptitle(f"Reel X-ray timeline: {os.path.basename(X['meta']['file'])}", fontsize=11)
    fig.savefig(path, dpi=90, bbox_inches='tight')
    plt.close(fig)
    return path


# ----------------------------------------------------------------------------------------------- main run
def run(source, outdir, listen_req=False, whisper_model='small', meta_path=None, ocr=True, faces=True, text_fps=2.0,
        cookies=None, lang=None, transcript_path=None):
    t_start = time.time()
    os.makedirs(outdir, exist_ok=True)
    timing = {}
    if re.match(r'^https?://', source):
        video, info = download(source, outdir, cookies)
        info_path = os.path.join(outdir, 'source_info.json')
    else:
        video = source
        if not os.path.isfile(video):
            raise FileNotFoundError(video)
        info, info_path = find_local_info(video, meta_path)
    pr = probe(video)
    meta = build_meta(video, pr, info, info_path, source)
    with open(os.path.join(outdir, 'meta.json'), 'w') as fh:
        json.dump(meta, fh, indent=1, default=str)
    dur, fps = pr['duration'], pr['fps']
    log(f"{os.path.basename(video)}: {dur:.1f} s {pr['width']}x{pr['height']} {fps} fps, audio={pr['has_audio']}")

    # transcript
    t0 = time.time()
    tr, trm = None, None
    if transcript_path:
        with open(transcript_path) as fh:
            tr = json.load(fh)
        for s in tr['segments']:   # accept transcribe.py's format too
            for w in s['words']:
                w.setdefault('p', None)
    elif pr['has_audio']:
        try:
            tr = transcribe(video, whisper_model, lang)
        except Exception as e:
            log('transcription failed:', e)
    if tr:
        trm = transcript_metrics(tr, dur)
        with open(os.path.join(outdir, 'transcript.json'), 'w') as fh:
            json.dump(tr, fh, indent=1)
        with open(os.path.join(outdir, 'transcript.txt'), 'w') as fh:
            for s in tr['segments']:
                fh.write(f"[{fmt_t(s['start'])}-{fmt_t(s['end'])}] {s['text']}\n")
    timing['transcript_s'] = r2(time.time() - t0, 1)

    # scene scores and events
    t0 = time.time()
    log('scene scores (ffmpeg)')
    sts, ssc = scene_scores(video)
    ev = cluster_events(sts, ssc, SCENE_EVENT)
    timing['scenes_s'] = r2(time.time() - t0, 1)

    # frames we want to keep: around every event + mid-frames, chosen after we know the shots; keep generously
    want = set()
    for e in ev:
        want.update({max(0, e['first'] - 1), e['i'], min(len(sts) - 1, e['last'] + 2)})
    nfr_est = len(sts) if len(sts) else int(dur * fps)
    want.update(range(0, nfr_est, max(1, int(fps / 2))))   # every 0.5 s, for mid-shot frames
    want.update({max(0, nfr_est - 1), max(0, nfr_est - 2), max(0, nfr_est - 3)})
    t0 = time.time()
    log('frame pass (grade, grid diffs, camera motion)')
    cols, keep, (aw, ah) = frame_pass(video, pr, want)
    nfr = len(cols['Y'])
    ftimes = sts if len(sts) == nfr else np.arange(nfr) / fps
    timing['frames_s'] = r2(time.time() - t0, 1)

    # ending: does the last frame loop back to the first? does it end on black?
    def _sig(f):
        g_ = cv2.GaussianBlur(cv2.resize(cv2.cvtColor(f, cv2.COLOR_BGR2GRAY), (36, 64), interpolation=cv2.INTER_AREA), (3, 3), 0)
        return g_.astype(np.float32)
    last_i = max([k for k in keep if k >= nfr - 3], default=None)
    ending = {}
    if 0 in keep and last_i is not None:
        a_, b_ = _sig(keep[0]), _sig(keep[last_i])
        ncc = float(((a_ - a_.mean()) * (b_ - b_.mean())).mean() / (a_.std() * b_.std() + 1e-6))
        ha = cv2.calcHist([cv2.cvtColor(keep[0], cv2.COLOR_BGR2HSV)], [0, 1], None, [18, 8], [0, 180, 0, 256])
        hb = cv2.calcHist([cv2.cvtColor(keep[last_i], cv2.COLOR_BGR2HSV)], [0, 1], None, [18, 8], [0, 180, 0, 256])
        hc = float(cv2.compareHist(cv2.normalize(ha, ha), cv2.normalize(hb, hb), cv2.HISTCMP_CORREL))
        ending = {'first_last_ncc': r2(ncc, 3), 'first_last_hist_corr': r2(hc, 3),
                  'loops_to_first_frame': bool(ncc >= 0.8 and hc >= 0.8),
                  'similar_scene': bool(ncc >= 0.6 and hc >= 0.5),
                  'ends_on_black': bool(float(keep[last_i].mean()) < 12), 'starts_on_black': bool(float(keep[0].mean()) < 12)}

    # classify events: full-frame vs overlay / partial
    for e in ev:
        cf = float(np.max(cols['cellfrac'][e['first']:e['last'] + 1])) if nfr else 0
        e['cellfrac'] = r2(cf, 2)
        e['type'] = 'full-frame' if e['score'] >= SCENE_HARD or (cf >= CELL_FULL and e['score'] >= 0.15) else 'overlay / partial'
        e['hard'] = e['score'] >= SCENE_HARD
    boundaries = [e for e in ev if e['hard'] or e['type'] == 'full-frame']
    shots, prev_i = [], 0
    for k, e in enumerate(boundaries + [None]):
        i1 = e['first'] if e else nfr
        if i1 - prev_i >= 2 or e is None:
            shots.append({'n': len(shots) + 1, 'i0': prev_i, 'i1': i1, 't0': r2(ftimes[prev_i] if prev_i < nfr else dur),
                          't1': r2(ftimes[i1] if i1 < nfr else dur)})
        if e:
            prev_i = e['first']
    for s_ in shots:
        s_['dur'] = r2(s_['t1'] - s_['t0'])
        seg = slice(s_['i0'], max(s_['i0'] + 1, s_['i1']))
        s_['Y'] = r2(np.mean(cols['Y'][seg]), 1)
        s_['sat'] = r2(np.mean(cols['sat'][seg]), 1)
        s_['contrast'] = r2(np.mean(cols['contrast'][seg]), 1)
        s_['flow'] = r2(np.nanmean(cols['flow'][seg]) if np.isfinite(cols['flow'][seg]).any() else 0, 2)
        s_['events_inside'] = sum(1 for e in ev if s_['i0'] < e['i'] < s_['i1'])
    # boundary kinds (punch-in / jump cut / new shot)
    for e in boundaries:
        fa, fb = keep.get(max(0, e['first'] - 1)), keep.get(min(nfr - 1, e['last'] + 2))
        if fa is not None and fb is not None:
            e['cut_kind'], sc_ = classify_boundary(fa, fb)
            e['cut_scale'] = r2(sc_, 3)
    # visual-change cadence
    et = [e['t'] for e in ev]
    marks = [0.0] + et + [dur]
    gaps = np.diff(marks)
    gi = int(np.argmax(gaps)) if len(gaps) else 0
    n_full = sum(1 for e in ev if e['type'] == 'full-frame')
    cuts = {'scene_threshold_event': SCENE_EVENT, 'scene_threshold_hard': SCENE_HARD,
            'raw_frames_over_event': int((ssc > SCENE_EVENT).sum()), 'raw_frames_over_hard': int((ssc > SCENE_HARD).sum()),
            'n_events': len(ev), 'n_full_frame': n_full, 'n_overlay': len(ev) - n_full,
            'n_hard': sum(1 for e in ev if e['hard']),
            'hard_times': [r2(e['t']) for e in ev if e['hard']],
            'changes_per_s': r2(len(ev) / dur, 3) if dur else None,
            'mean_change_interval_s': r2(dur / (len(ev) + 1), 2) if dur else None,
            'median_change_interval_s': r2(np.median(gaps), 2) if len(gaps) else None,
            'longest_gap_s': r2(gaps[gi], 2) if len(gaps) else None,
            'longest_gap_at': [r2(marks[gi]), r2(marks[gi + 1])] if len(gaps) else None,
            'gaps_over_3s': [[r2(marks[k]), r2(gaps[k])] for k in range(len(gaps)) if gaps[k] > 3.0],
            'n_shots': len(shots), 'avg_shot_s': r2(np.mean([s_['dur'] for s_ in shots]), 2) if shots else None,
            'punch_ins': [r2(e['t']) for e in boundaries if e.get('cut_kind') == 'punch-in'],
            'events': [{'t': r2(e['t']), 'score': r2(e['score'], 3), 'span_s': r2(e['span_s']), 'cellfrac': e['cellfrac'],
                        'type': e['type'], 'hard': e['hard'], 'cut_kind': e.get('cut_kind'), 'cut_scale': e.get('cut_scale')} for e in ev],
            'shots': [{k: v for k, v in s_.items() if k not in ('i0', 'i1')} for s_ in shots],
            '_t': ftimes, '_scene': ssc if len(ssc) == nfr else np.interp(ftimes, sts, ssc) if len(sts) else np.zeros(nfr)}

    # camera moves and easing
    moves = find_moves(cols, shots, fps, aw, ah)
    zr = np.nan_to_num(np.log(np.clip(np.nan_to_num(cols['s'], nan=1.0), 0.5, 2))) * fps * 100
    pan = np.nan_to_num(cols['tx'], nan=0.0) / aw * fps * 100
    for e in boundaries:   # don't plot the cut frames as motion
        zr[e['first']:e['last'] + 1] = 0
        pan[e['first']:e['last'] + 1] = 0
    motion = {'moves': moves, 'n_moves': len(moves),
              'n_linear': sum(1 for m in moves if m['curve'].startswith('linear')),
              'n_eased': sum(1 for m in moves if m['curve'].startswith('eased')),
              'n_near_linear': sum(1 for m in moves if m['curve'] == 'near-linear'),
              'mean_flow_pct_width': r2(np.nanmean(cols['flow']), 2) if np.isfinite(cols['flow']).any() else None,
              'per_shot_flow': [{'shot': s_['n'], 't0': s_['t0'], 'flow': s_['flow']} for s_ in shots],
              'camera_still_share': r2(float(np.mean((np.abs(smooth(zr)) < 1.5) & (np.abs(smooth(pan)) < 2))), 3),
              '_t': ftimes, '_zoom_rate': smooth(zr), '_pan_rate': smooth(pan)}

    # colour
    colour = {'yavg_signalstats': r2(16 + np.mean(cols['Y']) * 219 / 255, 1),
              'satavg_signalstats': r2(np.mean(cols['sat']) * 224 / 255, 2),
              'mean_luma': r2(np.mean(cols['Y']), 1), 'luma_p10_p90': [r2(np.percentile(cols['Y'], 10), 1), r2(np.percentile(cols['Y'], 90), 1)],
              'contrast_sd': r2(np.mean(cols['contrast']), 1), 'black_p2': r2(np.median(cols['p2']), 1),
              'white_p98': r2(np.median(cols['p98']), 1), 'satavg': r2(np.mean(cols['sat']), 2),
              'hsv_sat': r2(np.mean(cols['hsv_s']), 1), 'warmth_r_minus_b': r2(np.mean(cols['warmth']), 1),
              '_t': ftimes, '_Y': cols['Y'], '_contrast': cols['contrast'], '_sat': cols['sat']}
    per_s = []
    for sec in range(int(math.ceil(dur))):
        m_ = (ftimes >= sec) & (ftimes < sec + 1)
        if m_.any():
            per_s.append({'t': sec, 'Y': r2(cols['Y'][m_].mean(), 1), 'sat': r2(cols['sat'][m_].mean(), 1),
                          'contrast': r2(cols['contrast'][m_].mean(), 1), 'warmth': r2(cols['warmth'][m_].mean(), 1)})
    colour['per_second'] = per_s

    # text / faces / palette
    t0 = time.time()
    log('sample pass (text regions, OCR, faces, palette)')
    samples, px, face_keep, sinfo = sample_pass(video, pr, text_fps, ocr, faces)
    colour['palette'] = palette(px)
    timing['samples_s'] = r2(time.time() - t0, 1)
    text = {'available': sinfo['text_model'] is not None, 'model': sinfo['text_model'], 'ocr': sinfo['ocr']}
    if text['available'] and samples:
        # overlay text stays put on screen while the picture moves; scene text (signs, shoe stripes) moves with it.
        # a box is 'static' if the previous or next sample has a box in the same screen band and position.
        def _match(b, o):
            yo = max(0, min(b['y1'], o['y1']) - max(b['y0'], o['y0'])) / max(1e-6, min(b['y1'] - b['y0'], o['y1'] - o['y0']))
            same_x = abs((b['x0'] + b['x1']) / 2 - (o['x0'] + o['x1']) / 2) <= 0.1 or abs(b['x0'] - o['x0']) <= 0.04
            return yo >= 0.6 and same_x and 0.6 <= b['h'] / max(1e-6, o['h']) <= 1.6
        for k_, s in enumerate(samples):
            nb = (samples[k_ - 1]['text'] if k_ > 0 else []) + (samples[k_ + 1]['text'] if k_ + 1 < len(samples) else [])
            for b in s['text']:
                b['static'] = any(_match(b, o) for o in nb)
        anyt = np.array([bool(s['text']) for s in samples])
        ovt = np.array([any(b['static'] for b in s['text']) for s in samples])
        capt = np.array([any(b['h'] >= CAPTION_MIN_H and b['static'] for b in s['text']) for s in samples])
        st_ = np.array([s['t'] for s in samples])
        intr = []
        for s in samples:
            for b in s['text']:
                if b['h'] < CAPTION_MIN_H or not b['static']:
                    continue
                z = []
                if b['y1'] > SAFE_BOTTOM:
                    z.append('bottom')
                if b['y0'] < SAFE_TOP:
                    z.append('top')
                if b['x1'] > SAFE_RIGHT_X and b['y1'] > SAFE_RIGHT_Y:
                    z.append('right rail')
                if z:
                    intr.append({'t': s['t'], 'zones': z, 'box': [b['x0'], b['y0'], b['x1'], b['y1']], 'text': b['text']})
        cy = [((b['y0'] + b['y1']) / 2) for s in samples for b in s['text'] if b['h'] >= CAPTION_MIN_H and b['static']]
        spans = (trm or {}).get('spans') or []
        sp_s = [s for s, t in zip(capt, st_) if any(a <= t <= b for a, b in spans)]
        text.update({'any_share': r2(anyt.mean(), 3), 'caption_share': r2(capt.mean(), 3),
                     'caption_share_during_speech': r2(np.mean(sp_s), 3) if sp_s else None,
                     'first_text_s': r2(st_[anyt][0]) if anyt.any() else None,
                     'overlay_share': r2(ovt.mean(), 3), 'first_overlay_text_s': r2(st_[ovt][0]) if ovt.any() else None,
                     'n_scene_text_boxes': sum(1 for s in samples for b in s['text'] if not b['static']),
                     'first_caption_s': r2(st_[capt][0]) if capt.any() else None,
                     'text_in_first_1s': bool(ovt[st_ <= 1.0].any()), 'text_in_first_3s': bool(ovt[st_ <= 3.0].any()),
                     'first_3s_ocr': [b['text'] for s in samples if s['t'] <= 3.0 for b in s['text'] if b['text'] and b['static']][:12],
                     'caption_centre_y_median': r2(np.median(cy), 3) if cy else None,
                     'band_share': {'top_13pct': r2(np.mean([c < SAFE_TOP for c in cy]), 3) if cy else None,
                                    'middle': r2(np.mean([SAFE_TOP <= c <= SAFE_BOTTOM for c in cy]), 3) if cy else None,
                                    'bottom_18pct': r2(np.mean([c > SAFE_BOTTOM for c in cy]), 3) if cy else None},
                     'safe_zone_intrusions': intr, 'n_samples': len(samples),
                     'n_samples_intruding': len({i['t'] for i in intr})})
    # text changes (a new label / caption / counter is a visual change too: atom edit-change-every-1-5-2-5s)
    tchg = []
    if text['available'] and samples:
        import difflib

        def capb(s_):
            return sorted([b for b in (s_.get('text') or []) if b['h'] >= CAPTION_MIN_H and b.get('static')], key=lambda b: (round(b['y0'], 2), b['x0']))

        def iou(a, b):
            ix = max(0, min(a['x1'], b['x1']) - max(a['x0'], b['x0']))
            iy = max(0, min(a['y1'], b['y1']) - max(a['y0'], b['y0']))
            u = (a['x1'] - a['x0']) * (a['y1'] - a['y0']) + (b['x1'] - b['x0']) * (b['y1'] - b['y0']) - ix * iy
            return ix * iy / u if u > 0 else 0

        def similar(x, y):
            if not x or not y:
                return True   # no OCR: compare geometry only
            thr = 0.7 if min(len(x), len(y)) <= 4 else 0.6
            return difflib.SequenceMatcher(None, x, y).ratio() >= thr

        def same(A, B):
            return len(A) == len(B) and all(iou(a_, b_) >= 0.5 and similar(a_['text'], b_['text']) for a_, b_ in zip(A, B))
        # compare with the last STABLE text state; a new state must hold for the next sample too (OCR flicker filter)
        ref = None
        for k_, c_ in enumerate(samples):
            A = capb(c_)
            if ref is None:
                ref = A
                continue
            if same(A, ref):
                continue
            nxt = capb(samples[k_ + 1]) if k_ + 1 < len(samples) else None
            if nxt is None or same(A, nxt) or (len(A) != len(ref) and len(A) == len(nxt) and
                                               all(iou(a_, b_) >= 0.5 for a_, b_ in zip(A, nxt))):
                tchg.append(c_['t'])
                ref = A
        text['text_change_times'] = tchg
        text['n_text_changes'] = len(tchg)
    comb = sorted(set(et) | {t for t in tchg if all(abs(t - e) > 0.35 for e in et)})
    cm = [0.0] + comb + [dur]
    cg = np.diff(cm)
    cgi = int(np.argmax(cg)) if len(cg) else 0
    cuts['combined'] = {'n': len(comb), 'times': [r2(t) for t in comb],
                        'mean_interval_s': r2(dur / (len(comb) + 1), 2) if dur else None,
                        'median_interval_s': r2(np.median(cg), 2) if len(cg) else None,
                        'longest_gap_s': r2(cg[cgi], 2) if len(cg) else None,
                        'longest_gap_at': [r2(cm[cgi]), r2(cm[cgi + 1])] if len(cg) else None,
                        'gaps_over_3s': [[r2(cm[k]), r2(cg[k])] for k in range(len(cg)) if cg[k] > 3.0],
                        'note': 'scene-score events plus caption / label changes found by the text detector (0.5 s resolution)'}
    fcs = {'model': sinfo['face_model'], 'model_error': sinfo['face_model_error']}
    if sinfo['face_model'] and samples:
        with_f = [s for s in samples if s.get('faces')]
        flagged = [{'t': s['t'], 'flags': sorted({fl for f in s['faces'] for fl in f.get('flags', [])}),
                    'faces': [{k: f.get(k) for k in ('size', 'blinkL', 'blinkR', 'jawOpen', 'tongueOut', 'yaw', 'pitch', 'smile')} for f in s['faces'] if f.get('flags')]}
                   for s in samples if any(f.get('flags') for f in s.get('faces') or [])]
        for f_ in flagged:
            t = f_['t']
            m_ = (ftimes >= t - 0.3) & (ftimes <= t + 0.3)
            still = bool(m_.any() and np.max(cols['diff'][m_]) < 0.25)   # a true freeze / photo: almost no pixel change
            in_move = any(mv['t0'] <= t <= mv['t1'] and mv['curve'] != 'irregular / handheld' for mv in moves)
            f_['context'] = ('opening frame' if t <= 1.0 else 'closing frame' if t >= dur - 1.0 else
                             'held / still frame' if still else 'animated still (pan/zoom)' if in_move else 'in motion')
        fcs.update({'face_share': r2(len(with_f) / len(samples), 3),
                    'median_face_size': r2(np.median([f['size'] for s in with_f for f in s['faces']]), 3) if with_f else None,
                    'n_flagged_samples': len(flagged), 'flagged': flagged,
                    'blendshapes': sinfo['face_model'].startswith('mediapipe')})
        if face_keep:
            crops, labs = [], []
            for i, f in sorted(face_keep.items())[:40]:
                t = i / fps
                srec = next((s for s in samples if abs(s['t'] - t) < 0.02), None)
                for fc in (srec or {}).get('faces', []):
                    if not fc.get('flags'):
                        continue
                    H, W = f.shape[:2]
                    x0, y0, x1, y1 = fc['x0'] * W, fc['y0'] * H, fc['x1'] * W, fc['y1'] * H
                    pw, ph = (x1 - x0) * 0.4, (y1 - y0) * 0.4
                    c = f[int(max(0, y0 - ph)):int(min(H, y1 + ph)), int(max(0, x0 - pw)):int(min(W, x1 + pw))]
                    if c.size:
                        crops.append(cv2.resize(c, (180, int(180 * c.shape[0] / max(1, c.shape[1])))) if c.shape[1] else c)
                        labs.append(f"{fmt_t(t)}\n{', '.join(fc['flags'])}"[:60])
            if crops:
                hh = max(x.shape[0] for x in crops)
                crops = [cv2.copyMakeBorder(x, 0, hh - x.shape[0], 0, 0, cv2.BORDER_CONSTANT) for x in crops]
                sheet(crops, labs, os.path.join(outdir, 'faces_flagged.png'), title='Face check: flagged frames (advisory, confirm by eye)')
                fcs['sheet'] = 'faces_flagged.png'

    # audio
    t0 = time.time()
    if pr['has_audio']:
        log('audio (ebur128, silences, onsets, mix)')
        audio = audio_pass(video, pr, trm)
    else:
        audio = {'present': False}
    timing['audio_s'] = r2(time.time() - t0, 1)
    # SFX on visual events
    if audio.get('present'):
        sx = [o['t'] for o in audio['transients']]
        hit = [e for e in cuts['events'] if any(abs(e['t'] - s) <= 0.12 for s in sx)]
        audio['visual_events_with_transient'] = [e['t'] for e in hit]
        audio['visual_event_sfx_share'] = r2(len(hit) / len(cuts['events']), 3) if cuts['events'] else None
        # how often a random +-0.12 s window would contain a transient anyway (speech and drums make many)
        audio['visual_event_sfx_chance'] = r2(1 - math.exp(-audio['transients_per_s'] * 0.24), 3)
        early = [d for d in audio['dead_runs'] + [{'start': s['start'], 'dur': s['dur']} for s in audio['silences_40db'] if s.get('dur')]]
        audio['dropouts'] = sorted({(d['start'], d['dur']) for d in early if d['dur'] and 0.2 <= d['dur'] <= 0.8 and 0.5 < d['start'] < dur - 0.5})
    listen = {'ran': False, 'requested': bool(listen_req)}
    es = None
    if listen.get('requested') and audio.get('present'):
        t0 = time.time()
        es, err = earshot_listen(video, outdir)
        timing['earshot_s'] = r2(time.time() - t0, 1)
        if es:
            lab = [e for e in es.get('events', []) if e.get('label')]
            listen.update({'ran': True, 'summary': es.get('summary'), 'labelled_events': [
                {'t': r2(e['t']), 'label': e['label'], 'kind': e.get('kind'), 'prom_db': r2(e.get('prominence_db'), 1)} for e in lab],
                'sections': [{'start': s_['start'], 'end': s_['end'],
                              'genre': [g['tag'] for g in s_.get('music_genre', [])[:2]],
                              'mood': [g['tag'] for g in s_.get('music_mood', [])[:1]]} for s_ in es.get('sections', [])]})
            for o in audio['sfx_candidates'] + audio['transients']:
                near = min(lab, key=lambda e: abs(e['t'] - o['t']), default=None)
                if near is not None and abs(near['t'] - o['t']) <= 0.15:
                    o['earshot'] = f"{near['label']} ({near.get('kind')})"
        else:
            listen['error'] = err

    X = {'tool': 'Reel X-ray', 'version': 1, 'meta': meta, 'probe': pr,
         'transcript': {'available': tr is not None, 'lang': tr.get('lang') if tr else None, 'metrics': trm},
         'cuts': cuts, 'ending': ending, 'motion': motion, 'colour': colour, 'text': text, 'faces': fcs, 'audio': audio,
         'listen': listen, 'samples': samples, 'timing': timing}

    # pictures
    log('contact sheets and timeline')
    frames, labs = [], []
    for s_ in shots[:64]:
        mid = (s_['i0'] + s_['i1']) // 2
        k = min(keep, key=lambda j: abs(j - mid)) if keep else None
        if k is not None:
            frames.append(keep[k])
            labs.append(f"#{s_['n']} {fmt_t(s_['t0'])}\n{s_['dur']:.1f}s  Y{s_['Y']:.0f} sat{s_['sat']:.0f}")
    sheet(frames, labs, os.path.join(outdir, 'contact_sheet.png'), title=f'One frame per shot ({len(shots)} shots)')
    frames, labs = [], []
    for e in ev[:72]:
        k = min(nfr - 1, e['last'] + 2)
        if k in keep:
            frames.append(keep[k])
            labs.append(f"{fmt_t(e['t'])} {'CUT' if e['type'] == 'full-frame' else 'overlay'}\nscore {e['score']:.2f} grid {e['cellfrac']:.2f}")
    sheet(frames, labs, os.path.join(outdir, 'changes_sheet.png'), title=f'Frame after each visual change ({len(ev)} events at scene > {SCENE_EVENT})')
    try:
        timeline_png(os.path.join(outdir, 'timeline.png'), X)
    except Exception as e:
        log('timeline.png failed:', e)
    timing['total_s'] = r2(time.time() - t_start, 1)

    clean = strip_private(X)
    with open(os.path.join(outdir, 'xray.json'), 'w') as fh:
        json.dump(clean, fh, indent=1, default=_json_default)
    with open(os.path.join(outdir, 'xray.md'), 'w') as fh:
        fh.write(render_md(clean, outdir))
    log(f'done in {timing["total_s"]} s -> {outdir}')
    return clean


def _json_default(o):
    if isinstance(o, np.ndarray):
        return o.tolist()
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.bool_,)):
        return bool(o)
    return str(o)


def strip_private(o):
    if isinstance(o, dict):
        return {k: strip_private(v) for k, v in o.items() if not k.startswith('_')}
    if isinstance(o, list):
        return [strip_private(v) for v in o]
    if isinstance(o, tuple):
        return [strip_private(v) for v in o]
    return o


# ----------------------------------------------------------------------------------------------- markdown
def render_md(X, outdir):
    m, c, mo, g, tx, fc, au, tr = X['meta'], X['cuts'], X['motion'], X['colour'], X['text'], X['faces'], X['audio'], X['transcript']
    tm = tr.get('metrics') or {}
    L = []
    name = m.get('title') or os.path.basename(m['file'])
    L.append(f'# Reel X-ray: {name}\n')
    L.append(f"- **Source:** {m.get('url') or m['source']}")
    if m.get('creator'):
        L.append(f"- **Creator:** {m['creator']} (@{m.get('creator_id') or '?'}) · posted {m.get('upload_date') or '?'}")
    if m.get('likes') is not None or m.get('comments') is not None or m.get('views') is not None:
        L.append(f"- **Stats at download:** {m.get('likes')} likes · {m.get('comments')} comments · views {m.get('views') if m.get('views') is not None else 'not exposed'}")
    if m.get('caption'):
        cap = m['caption'].replace('\n', ' ')
        L.append(f"- **Caption:** {cap[:280]}{'…' if len(cap) > 280 else ''}")
    L.append(f"- **File:** {m['duration_s']:.1f} s · {m['width']}×{m['height']} · {m['fps']} fps · audio: {'yes (' + str(m['acodec']) + ')' if m['has_audio'] else 'none (silent export)'}")
    L.append(f"- **Method:** ffmpeg scene score (events > {c['scene_threshold_event']}, hard > {c['scene_threshold_hard']}) + 8×8 grid difference; "
             f"LK optical flow + partial-affine camera fit; {tx.get('model') or 'no text model'}{' + ' + tx['ocr'] if tx.get('ocr') else ''}; "
             f"{fc.get('model') or 'no face model'}; faster-whisper {X['transcript'].get('lang') or ''}; ffmpeg ebur128 / silencedetect; spectral-flux onsets"
             f"{'; earshot timeline' if X['listen'].get('ran') else ''}. Not a virality prediction.\n")

    L.append('## Production (measured)\n')
    L.append('| Area | Measured |')
    L.append('|---|---|')
    if tm.get('n_words'):
        L.append(f"| Length & pace | {m['duration_s']:.1f} s. {tm['n_words']} words; speech {tm['active_speech_s']:.0f} s ({100 * tm['speech_share']:.0f}% of the runtime) → **~{tm['wpm_active']:.0f} wpm** while talking ({tm['wpm_overall']:.0f} wpm over the whole video). First word at {tm['first_word_s']:.2f} s |")
    else:
        L.append(f"| Length & pace | {m['duration_s']:.1f} s. No speech detected |")
    hook = []
    if tm.get('n_words'):
        hook.append(f"said in 0–3 s: “{tm['first_3s_text']}”")
    if tx.get('available'):
        hook.append(f"on-screen overlay text {'from ' + str(tx['first_overlay_text_s']) + ' s' if tx.get('first_overlay_text_s') is not None else 'none'}"
                    + (f" (OCR guess: {', '.join(tx['first_3s_ocr'][:5])})" if tx.get('first_3s_ocr') else ''))
    first_ev = c['events'][0]['t'] if c['events'] else None
    hook.append(f"first visual change at {first_ev if first_ev is not None else '-'} s")
    L.append(f"| Hook (0–3 s) | {'; '.join(hook)} |")
    L.append(f"| Visual changes | **{c['n_events']} events** (scene > {c['scene_threshold_event']}, frames within 0.2 s merged) = **one every ~{c['mean_change_interval_s']} s**; counted per frame: {c['raw_frames_over_event']} frames = one every {m['duration_s'] / max(1, c['raw_frames_over_event']):.1f} s "
             f"(median gap {c['median_change_interval_s']} s; longest {c['longest_gap_s']} s at {c['longest_gap_at'][0] if c['longest_gap_at'] else '-'} s). "
             f"{c['n_full_frame']} full-frame changes vs {c['n_overlay']} overlay/partial; {c['n_hard']} hard (> {c['scene_threshold_hard']}): "
             f"{', '.join(str(t) for t in c['hard_times'][:14])}{' …' if len(c['hard_times']) > 14 else ''} |")
    cb = c.get('combined') or {}
    if cb:
        L.append(f"| Changes incl. text | {cb['n']} changes when caption / label swaps count too ({tx.get('n_text_changes', 0)} text changes) = **one every ~{cb['mean_interval_s']} s**; "
                 f"longest stretch with nothing new {cb['longest_gap_s']} s ({cb['longest_gap_at'][0]}–{cb['longest_gap_at'][1]} s) |")
    kinds = {}
    for e in c['events']:
        if e.get('cut_kind'):
            kinds[e['cut_kind']] = kinds.get(e['cut_kind'], 0) + 1
    L.append(f"| Shots & cuts | {c['n_shots']} shots, average **{c['avg_shot_s']} s**. Cut kinds: {', '.join(f'{v}× {k}' for k, v in kinds.items()) or 'none'}"
             f"{'; punch-ins at ' + ', '.join(map(str, c['punch_ins'])) + ' s' if c['punch_ins'] else ''} |")
    mv = mo['moves']
    mvs = '; '.join(f"{x['kind']} {x['total']:+.0f}{x['unit'].split()[0]} {x['t0']}–{x['t1']} s ({x['curve']})" for x in mv[:8])
    L.append(f"| Camera / motion | Mean optical-flow motion {mo['mean_flow_pct_width']}% of width per 3 frames; camera still {100 * (mo['camera_still_share'] or 0):.0f}% of the time. "
             f"{len(mv)} sustained zoom/pan moves ({mo['n_linear']} linear, {mo['n_eased']} eased){': ' + mvs if mv else ''}{' …' if len(mv) > 8 else ''} |")
    if tx.get('available'):
        bs = tx.get('band_share') or {}
        L.append(f"| On-screen text | Text in {100 * tx['any_share']:.0f}% of samples (overlay-like, fixed on screen: {100 * tx['overlay_share']:.0f}%; {tx['n_scene_text_boxes']} moving scene-text boxes ignored), caption-scale overlay text in {100 * tx['caption_share']:.0f}%"
                 f"{' (' + str(round(100 * tx['caption_share_during_speech'])) + '% while speaking)' if tx.get('caption_share_during_speech') is not None else ''}. "
                 f"Caption-scale text centred at {100 * tx['caption_centre_y_median']:.0f}% height (median)" if tx.get('caption_centre_y_median') is not None else
                 f"| On-screen text | Text in {100 * tx['any_share']:.0f}% of samples; no caption-scale overlay text")
        L[-1] += (f"; bands top/middle/bottom {bs.get('top_13pct')}/{bs.get('middle')}/{bs.get('bottom_18pct')}. "
                  f"Safe-zone intrusions in {tx['n_samples_intruding']} of {tx['n_samples']} samples |")
    else:
        L.append('| On-screen text | text model not available |')
    if fc.get('model'):
        L.append(f"| Faces | Face in {100 * (fc.get('face_share') or 0):.0f}% of samples (median face height {fc.get('median_face_size')} of frame). "
                 f"{fc.get('n_flagged_samples', 0)} samples flagged by the face check{' (eyes / mouth / angle from MediaPipe blendshapes)' if fc.get('blendshapes') else ' (presence only)'} |")
    pal = ' '.join(f"`{p['hex']}` {100 * p['share']:.0f}%" for p in g.get('palette', []))
    L.append(f"| Grade | ffmpeg-signalstats scale: **YAVG {g['yavg_signalstats']}**, **SATAVG {g['satavg_signalstats']}**. Full-range: mean luma {g['mean_luma']} / 255 (p10–p90 {g['luma_p10_p90'][0]}–{g['luma_p10_p90'][1]}), contrast (luma SD) {g['contrast_sd']}, "
             f"blacks p2 {g['black_p2']} / whites p98 {g['white_p98']}, HSV saturation {g['hsv_sat']}, warmth R−B {g['warmth_r_minus_b']:+} |")
    L.append(f"| Palette | {pal} |")
    en = X.get('ending') or {}
    if en:
        L.append(f"| Ending | last frame vs first: correlation {en['first_last_ncc']}, colour match {en['first_last_hist_corr']} → "
                 f"{'**loops to frame 1**' if en['loops_to_first_frame'] else 'same scene, not the same frame' if en.get('similar_scene') else 'does not loop'}; {'ends on black' if en['ends_on_black'] else 'does not end on black'} |")
    if au.get('present'):
        L.append(f"| Audio level | Integrated **{au['integrated_lufs']} LUFS**, loudness range **{au['lra_lu']} LU**, true peak **{au['true_peak_dbtp']} dBTP** |")
        L.append(f"| Music / voice | {au['mix']}"
                 f"{' (voice ' + str(au['speech_level_db']) + ' dBFS, pauses ' + str(au['bed_level_db']) + ' dBFS)' if au.get('bed_level_db') is not None and au.get('speech_level_db') is not None else ''}. "
                 f"{'Steady pulse ~' + str(au['tempo_bpm']) + ' BPM' if au.get('tempo_bpm') else 'No steady beat grid'} (pulse clarity {au['pulse_clarity']}) |")
        sfx = au['sfx_candidates']
        sfx_s = ', '.join(f"{o['t']:.2f}" + (f" ({o['earshot']})" if o.get('earshot') else '') for o in sfx[:24])
        L.append(f"| SFX / hits | {len(au['transients'])} strong transients (≥ 9 dB jump; {au['transients_per_s']}/s, speech consonants included). "
                 f"Outside speech (likely SFX / music hits): {len(sfx)}{': ' + sfx_s if sfx else ''}{' …' if len(sfx) > 24 else ''}. "
                 f"{len(au['visual_events_with_transient'])} of {c['n_events']} visual changes have a transient within ±0.12 s "
                 f"({100 * (au['visual_event_sfx_share'] or 0):.0f}% vs ~{100 * au['visual_event_sfx_chance']:.0f}% by chance) |")
        dr = ', '.join(f"{d['start']:.2f} s ({d['dur']:.1f} s)" for d in au['dead_runs'][:10])
        L.append(f"| Silences / dropouts | Dead air (100 ms windows ≥ {DEAD_DB_BELOW_MEDIAN:.0f} dB under the median): {au['dead_window_pct']}% of windows, longest {au['longest_dead_s']} s"
                 f"{': ' + dr if dr else ''}. ffmpeg silencedetect (−40 dB, ≥ 0.25 s): "
                 f"{', '.join(str(s['start']) + ' s (' + str(s['dur']) + ' s)' for s in au['silences_40db'][:8]) or 'none'} |")
    else:
        L.append('| Audio | **No audio stream**: a silent export (music / SFX would be added in-app) |')
    if X['listen'].get('ran'):
        L.append(f"| earshot | {X['listen']['summary'][:600]} |")
    elif X['listen'].get('error'):
        L.append(f"| earshot | failed: {X['listen']['error'][:200]} |")
    L.append('')

    if tm.get('n_words'):
        L.append('## Hook transcript (first 3 s)\n')
        L.append(f"> {tm['first_3s_text']}\n")
        L.append(f"First line: “{tm['first_line']}”. Full transcript: `transcript.txt`.\n")
    L.append('## Visual change list\n')
    L.append('| t (s) | type | score | grid changed | cut kind |')
    L.append('|---|---|---|---|---|')
    for e in c['events'][:80]:
        L.append(f"| {e['t']} | {e['type']} | {e['score']} | {e['cellfrac']} | {e.get('cut_kind') or ''}{(' ×' + str(e['cut_scale'])) if e.get('cut_scale') else ''} |")
    L.append('')
    L.append('## Shots\n')
    L.append('| # | start | length | changes inside | mean luma | sat | flow |')
    L.append('|---|---|---|---|---|---|---|')
    for s_ in c['shots'][:80]:
        L.append(f"| {s_['n']} | {fmt_t(s_['t0'])} | {s_['dur']} s | {s_['events_inside']} | {s_['Y']} | {s_['sat']} | {s_['flow']} |")
    L.append('')
    if mo['moves']:
        L.append('## Camera moves and easing\n')
        L.append('| t (s) | move | total | chord deviation | speed by thirds | curve |')
        L.append('|---|---|---|---|---|---|')
        for x in mo['moves'][:40]:
            L.append(f"| {x['t0']}–{x['t1']} | {x['kind']}{' (whole shot)' if x['whole_shot'] else ''} | {x['total']:+} {x['unit']} | {x['chord_dev']} | {' / '.join(str(v) for v in x['speed_thirds'])} | {x['curve']} |")
        L.append('')
    if tx.get('available') and tx.get('safe_zone_intrusions'):
        L.append('## Text in the Reels UI zones\n')
        for i in tx['safe_zone_intrusions'][:20]:
            L.append(f"- {i['t']} s: {', '.join(i['zones'])} (box x {i['box'][0]}–{i['box'][2]}, y {i['box'][1]}–{i['box'][3]}) “{i['text']}”")
        L.append('')
    if fc.get('flagged'):
        L.append('## Face check (advisory)\n')
        for f in fc['flagged'][:25]:
            L.append(f"- {f['t']} s ({f.get('context')}): {', '.join(f['flags'])}")
        L.append('')
    if X['listen'].get('ran'):
        L.append('## earshot labels\n')
        for e in X['listen']['labelled_events'][:40]:
            L.append(f"- {e['t']} s: {e['label']} ({e['kind']})")
        L.append('')
    L.append('## Files\n')
    for f in ('meta.json', 'transcript.txt', 'xray.json', 'contact_sheet.png', 'changes_sheet.png', 'timeline.png', 'faces_flagged.png', 'earshot_timeline.json'):
        if os.path.exists(os.path.join(outdir, f)):
            L.append(f'- `{f}`')
    L.append(f"\nTiming: {X['timing']}")
    return '\n'.join(L) + '\n'


def main(argv=None):
    ap = argparse.ArgumentParser(description='Reel X-ray: measure a reel / video locally (no paid APIs).')
    ap.add_argument('source', help='video file or URL (Instagram / YouTube / TikTok via yt-dlp)')
    ap.add_argument('-o', '--out', help='output folder (default: ./xray_<name>)')
    ap.add_argument('--listen', action='store_true', help='also run earshot timeline to label SFX moments (slow: loads models)')
    ap.add_argument('--whisper-model', default='small', help='faster-whisper model (default small)')
    ap.add_argument('--lang', default=None, help='force transcript language, e.g. en or hi')
    ap.add_argument('--transcript', help='reuse an existing words.json (transcribe.py format) instead of transcribing')
    ap.add_argument('--meta', help='yt-dlp -j json for a local file (else <video>.info.json / meta.json next to it)')
    ap.add_argument('--no-ocr', action='store_true', help='detect text regions but skip reading them')
    ap.add_argument('--no-faces', action='store_true')
    ap.add_argument('--text-fps', type=float, default=2.0, help='samples per second for text / faces (default 2)')
    ap.add_argument('--cookies', help='cookies.txt for yt-dlp (private / login-walled posts)')
    a = ap.parse_args(argv)
    name = re.sub(r'[^A-Za-z0-9_-]+', '_', os.path.splitext(os.path.basename(a.source.rstrip('/')))[0])[:40] or 'video'
    out = a.out or os.path.join(os.getcwd(), f'xray_{name}')
    X = run(a.source, out, listen_req=a.listen, whisper_model=a.whisper_model, meta_path=a.meta, ocr=not a.no_ocr,
            faces=not a.no_faces, text_fps=a.text_fps, cookies=a.cookies, lang=a.lang, transcript_path=a.transcript)
    print(os.path.join(out, 'xray.md'))
    return X


if __name__ == '__main__':
    main()
