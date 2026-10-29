#!/usr/bin/env python3
"""Reel Doctor: run the Reel X-ray on a draft and score it against explicit rules from the Brain.

    .venv/bin/python -I tools/doctor.py DRAFT.mp4 [--format reel30|reel60|reel90|yt-short|yt-long]
                                                              [--niche gym|tech|gaming|travel] [-o OUTDIR] [--listen]

Writes OUTDIR/doctor.md and OUTDIR/doctor.json (plus the X-ray in OUTDIR/xray/). Each rule cites the Brain atom ids
(brain/data/atoms.json, atoms_L10.json) it comes from, shows the measured value, the target, why it matters and the
concrete fix. The total is a **Brain checklist score**: how many of the Brain's production rules the draft meets.
It is not a prediction of views or virality, and a rule can be broken on purpose.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)   # -I drops the script folder from sys.path; xray.py lives next to this file
import xray  # noqa: E402

BRAIN = os.path.join(os.path.dirname(HERE), 'brain', 'data')
SCORE = {'pass': 1.0, 'warn': 0.5, 'fail': 0.0}

FORMATS = {
    # length: (pass lo, pass hi, warn lo, warn hi) seconds; cadence: target seconds between visual changes
    'reel30': {'len': (7, 35, 5, 45), 'vertical': True, 'cadence': (1.2, 2.5), 'hook_s': 3.0, 'loop': True},
    'reel60': {'len': (20, 65, 12, 80), 'vertical': True, 'cadence': (1.2, 2.5), 'hook_s': 3.0, 'loop': False},
    'reel90': {'len': (45, 95, 30, 120), 'vertical': True, 'cadence': (1.2, 2.5), 'hook_s': 3.0, 'loop': False},
    'yt-short': {'len': (10, 60, 7, 180), 'vertical': True, 'cadence': (1.2, 2.5), 'hook_s': 3.0, 'loop': True},
    'yt-long': {'len': (180, 3600, 60, 7200), 'vertical': False, 'cadence': (2.5, 4.5), 'hook_s': 20.0, 'loop': False},
}
VIBE_NICHES = ('gym', 'travel')
CTA_WORDS = re.compile(r'\b(comment|follow|save|share|send|subscribe|link|dm|bio|tag)\b', re.I)


def load_atoms():
    atoms = {}
    for fn in ('atoms.json', 'atoms_L10.json'):
        p = os.path.join(BRAIN, fn)
        if os.path.exists(p):
            with open(p) as fh:
                for a in json.load(fh).get('atoms', []):
                    atoms[a['id']] = a
    return atoms


ATOMS = load_atoms()


def cite(*ids):
    out = []
    for i in ids:
        a = ATOMS.get(i)
        if a is None:
            print(f'[doctor] warning: atom {i} not found in the Brain', file=sys.stderr)
            out.append({'id': i, 'title': '(missing from atoms.json)', 'sources': []})
        else:
            out.append({'id': i, 'title': a['title'], 'sources': a.get('sources', [])})
    return out


def R(rid, title, weight, status, measured, target, why, atoms, fix, note=None):
    return {'id': rid, 'title': title, 'weight': weight, 'status': status, 'measured': measured, 'target': target,
            'why': why, 'atoms': cite(*atoms), 'fix': fix, 'note': note}


def guess_format(X):
    d = X['meta']['duration_s']
    if X['meta']['width'] > X['meta']['height']:
        return 'yt-long'
    return 'reel30' if d <= 35 else 'reel60' if d <= 65 else 'reel90'


def transcript_words(xdir):
    p = os.path.join(xdir, 'transcript.json')
    if not os.path.exists(p):
        return []
    with open(p) as fh:
        tr = json.load(fh)
    return [w for s in tr['segments'] for w in s['words'] if w.get('w')]


# ------------------------------------------------------------------------------------------------- rules
def rules(X, fmt, niche, xdir):
    F = FORMATS[fmt]
    m, c, tx, au, tm = X['meta'], X['cuts'], X['text'], X['audio'], (X['transcript'].get('metrics') or {})
    dur = m['duration_s']
    has_audio = au.get('present', False)
    has_speech = bool(tm.get('n_words')) and (tm.get('mean_word_prob') or 1) >= 0.45 and (tm.get('speech_share') or 0) >= 0.15
    out = []

    # 1. hook / context early ------------------------------------------------------------------------------
    early, win = (1.0, F['hook_s']) if fmt != 'yt-long' else (5.0, F['hook_s'])
    fw = tm.get('first_word_s') if has_speech else None
    ft = tx.get('first_overlay_text_s') if tx.get('available') else None
    ch_early = [n for n, t in (('speech', fw), ('on-screen text', ft)) if t is not None and t <= early]
    ch_win = [n for n, t in (('speech', fw), ('on-screen text', ft)) if t is not None and t <= win]
    expected = 2 if has_speech else 1
    meas = (f"first word {fw:.2f} s" if fw is not None else 'no speech') + '; ' + \
           (f"first on-screen text {ft:.2f} s" if ft is not None else 'no on-screen text') + \
           (f"; said in 0–3 s: “{tm.get('first_3s_text', '')}”" if has_speech else '') + \
           (f"; OCR guess: {', '.join(tx.get('first_3s_ocr', [])[:3])}" if tx.get('first_3s_ocr') else '')
    if not has_audio:
        meas += ' (silent export: the voice channel is not in this file)'
    if ch_early and len(ch_win) >= expected:
        st = 'pass'
    elif ch_win:
        st = 'warn'
    else:
        st = 'fail'
    out.append(R('hook-context', 'Context in the first 2–3 s', 15, st, meas,
                 f"topic said AND written within ~{early:.0f} s (all channels within {win:.0f} s)",
                 'The first words are the context; the creator claims delaying it even to the back half of the first sentence sharply raises skip rate. Short form gives 2–3 s; a line not understood in ~2 s fails.',
                 ['hook-context-first-words', 'hook-window-short-vs-long', 'hook-no-intro-payoff-first', 'hook-one-mississippi'],
                 'Open on the strongest frame with a hook text of 8 words or fewer on screen from frame 1 (Edits/CapCut: text layer at 0:00), and say the same topic in the first words. No greeting, no logo.'
                 if st != 'pass' else ('Keep it: the topic is on screen and in the audio from the start.' if has_speech else
                                       'Keep it: the topic is written from the first second. If you add a voiceover, say it in the first words too.')))

    # 2. visual change cadence -----------------------------------------------------------------------------
    cb = c.get('combined') or {}
    lo, hi = F['cadence']
    mi, lg = cb.get('mean_interval_s'), cb.get('longest_gap_s')
    lg_lim = 4.0 if fmt != 'yt-long' else 8.0
    if mi is None:
        st = 'warn'
    elif lo * 0.65 <= mi <= hi and lg <= lg_lim:
        st = 'pass'
    elif mi <= hi + 1.0 and lg <= lg_lim * 1.6:
        st = 'warn'
    else:
        st = 'fail'
    if mi is not None and mi < lo * 0.65:
        st = 'warn'
    gaps = ', '.join(f"{g[0]:.1f}–{g[0] + g[1]:.1f} s" for g in cb.get('gaps_over_3s', [])[:6])
    out.append(R('visual-change', f'Something new on screen every {lo}–{hi} s', 15, st,
                 f"{cb.get('n')} changes (cuts, overlays, caption/label swaps) = one every {mi} s; longest stretch with nothing new {lg} s"
                 f"{' (' + gaps + ')' if gaps else ''}. Scene-only: {c['n_events']} events, {c['n_hard']} hard cuts, avg shot {c['avg_shot_s']} s",
                 f"one change every {lo}–{hi} s; no stretch over {lg_lim:.0f} s" + ('' if fmt != 'yt-long' else ' (long-form talking shots 2.5–4.5 s)'),
                 'A cut, layout swap, label, card or animation every 1.5–2.5 s keeps the eye moving (L01/L02; Rahul ~1.2–2 s; L10 ~2.1 s mostly from overlays, only 6 full-frame cuts in 85 s).',
                 ['edit-change-every-1-5-2-5s', 'edit-graphic-yap-overlay-2s'] + (['edit-long-form-talking-pace'] if fmt == 'yt-long' else []) + ['edit-trained-rhythm-break'],
                 (f"Add a change inside each long stretch ({gaps or 'see timeline.png'}): a cut on motion, a 105–110% punch-in on the key word, a label/counter or a card. "
                  'Breaking the rhythm once for the big moment is fine (train it, then break it).') if st != 'pass' else
                 'Keep the rhythm; break it once on purpose for the payoff.' if mi is None or mi >= lo * 0.65 else
                 'Very fast: check every change can be read (One Mississippi).'))

    # 3. on-screen text / captions ----------------------------------------------------------------------------
    if not tx.get('available'):
        out.append(R('on-screen-text', 'On-screen text / captions present', 10, 'manual', 'text detector not available', '', '',
                     ['text-captions-on-yaps'], 'Check by eye.'))
    else:
        if has_speech:
            share = tx.get('caption_share_during_speech') or 0
            st = 'pass' if share >= 0.6 else 'warn' if share >= 0.3 else 'fail'
            meas = f"caption-scale text on screen during {100 * share:.0f}% of the speech ({100 * tx['any_share']:.0f}% of samples have any text)"
            tgt = 'captions on ≥ 60% of the talking'
            fix = ('Add word-timed captions (1–3 words, white bold sans with a soft shadow, just above the lower third; transcript.json has the word timings).'
                   if st != 'pass' else 'Keep the captions; pick one style and stay consistent (box vs no box is an open clash, C29).')
        else:
            share = tx.get('caption_share') or 0
            st = 'pass' if tx.get('text_in_first_3s') and share >= 0.2 else 'warn'
            meas = f"overlay text in {100 * tx['overlay_share']:.0f}% of samples (caption-scale {100 * share:.0f}%), first at {tx.get('first_overlay_text_s')} s"
            tgt = 'a hook text in the first 3 s, labels where they add meaning'
            fix = ('Add a short hook line in the first second and a label / counter where something changes.' if st != 'pass'
                   else 'Keep it: hook text from the start, labels carry the story.')
        out.append(R('on-screen-text', 'On-screen text / captions present', 10, st, meas, tgt,
                     'Captions and a title on talk-to-camera videos are "really important" for almost everybody; the context should also be written, not only said.',
                     ['text-captions-on-yaps', 'hook-context-first-words', 'l10-plain-shadow-captions', 'text-word-by-word-highlight'], fix,
                     note='Only text that stays fixed on screen between samples counts (moving signs and logos are ignored); a static sign in a locked-off shot can still count. OCR guesses in xray.md.'))

    # 4. safe zones ---------------------------------------------------------------------------------------
    if F['vertical'] and tx.get('available'):
        n_cap = sum(1 for s in X['samples'] if any(b['h'] >= xray.CAPTION_MIN_H and b.get('static') for b in (s.get('text') or [])))
        n_in = tx.get('n_samples_intruding', 0)
        share = n_in / n_cap if n_cap else 0
        st = 'pass' if share <= 0.05 else 'warn' if share <= 0.2 else 'fail'
        zones = {}
        for i in tx.get('safe_zone_intrusions', []):
            for z in i['zones']:
                zones.setdefault(z, []).append(i['t'])
        zs = '; '.join(f"{z}: {len(ts)}× (e.g. {', '.join(str(t) for t in ts[:4])} s)" for z, ts in zones.items())
        out.append(R('safe-zones', 'Text clear of the Reels UI', 8, st,
                     f"{n_in} of {n_cap} samples with caption-scale text touch a UI zone{': ' + zs if zs else ''}",
                     f"caption-scale text between {100 * xray.SAFE_TOP:.0f}% and {100 * xray.SAFE_BOTTOM:.0f}% of the height and off the right rail (x > {100 * xray.SAFE_RIGHT_X:.0f}% in the lower half)",
                     'Reels are 9:16 1080×1920: the top ~250 px, the bottom ~350 px (caption, username, audio) and the right-side buttons cover text.',
                     ['text-safe-zone', 'growth-format-specs'],
                     'Move those text layers toward the middle band (about 13–82% height) and left of the right ~12%.' if st != 'pass' else 'Keep it.',
                     note='Only text fixed on screen counts; a sign in a locked-off shot can still trigger it. Ignore intrusions that are part of the footage.'))
    elif not F['vertical']:
        out.append(R('safe-zones', 'Text clear of the Reels UI', 8, 'n/a', 'long-form 16:9', '', '', ['text-safe-zone'], ''))

    # 5. dead air ------------------------------------------------------------------------------------------
    silent_note = 'Silent export: music and SFX are added in-app (pick a low-use track). Re-run the Doctor on the final export with sound.'
    if not has_audio:
        out.append(R('dead-air', 'No dead air (except an intentional dropout)', 8, 'n/a', 'no audio stream', 'no silence > ~0.7 s', '',
                     ['edit-cut-breaths-no-dead-air', 'sound-low-use-count-track'], silent_note))
    else:
        runs = [r for r in au['dead_runs'] if r['dur'] > 0.7]
        lg = au['longest_dead_s']
        pct = au['dead_window_pct']
        st = 'pass' if lg <= 0.7 and pct <= 2.5 else 'warn' if lg <= 1.2 and pct <= 6 else 'fail'
        drops = [r for r in au['dead_runs'] if 0.2 <= r['dur'] <= 0.7]
        out.append(R('dead-air', 'No dead air (except an intentional dropout)', 8, st,
                     f"longest gap {lg} s; {pct}% of 100 ms windows ≥ 25 dB under the median"
                     f"{'; gaps > 0.7 s at ' + ', '.join(str(r['start']) for r in runs[:6]) + ' s' if runs else ''}"
                     f"{'; short dropouts (fine if on purpose) at ' + ', '.join(str(r['start']) for r in drops[:5]) + ' s' if drops else ''}",
                     'no gap > 0.7 s; < 2.5% dead windows (Rahul); one ~0.5 s dropout after the punchline is a tool',
                     'Jump cuts remove breaths; Rahul\'s reels have under 2.5% dead windows. A deliberate ~0.5 s music dropout right after the hook punchline (L10) is the exception.',
                     ['edit-cut-breaths-no-dead-air', 'l10-dropout-after-punchline'],
                     ('Cut the pauses on the word timestamps (transcript.json) or run silence removal; keep the bed running under pauses.' if st != 'pass'
                      else 'Keep it.')))

    # 6. SFX on visual events --------------------------------------------------------------------------------
    if not has_audio:
        out.append(R('sfx-on-events', 'A sound on visual events', 8, 'n/a', 'no audio stream', '', '',
                     ['sound-sfx-every-event', 'sound-low-use-count-track'], silent_note))
    else:
        L_ = X.get('listen') or {}
        evs = [e['t'] for e in c['events']]
        if L_.get('ran'):
            lab = [e for e in L_['labelled_events'] if e.get('kind') not in ('VOICE', None)]
            hit = [t for t in evs if any(abs(t - e['t']) <= 0.15 for e in lab)]
            share = len(hit) / len(evs) if evs else 0
            st = 'pass' if share >= 0.4 else 'warn' if share >= 0.15 else 'fail'
            meas = f"earshot labels a non-voice sound within ±0.15 s of {len(hit)} of {len(evs)} visual changes ({100 * share:.0f}%)"
        else:
            share, ch = au.get('visual_event_sfx_share') or 0, au.get('visual_event_sfx_chance') or 0
            meas = (f"{len(au.get('visual_events_with_transient', []))} of {len(evs)} visual changes have a strong transient within ±0.12 s "
                    f"({100 * share:.0f}%; ~{100 * ch:.0f}% would happen by chance at this transient rate)")
            if share >= 0.5 and share >= ch + 0.2:
                st = 'pass'
            elif share >= ch + 0.1:
                st = 'warn'
            elif has_speech or (au.get('transients_per_s') or 0) > 1.0:
                st = 'manual'
                meas += '. Speech / drums make too many transients to tell SFX apart; run with --listen or check by ear'
            else:
                st = 'fail'
        out.append(R('sfx-on-events', 'A sound on visual events', 8, st, meas,
                     'a whoosh / pop / hit on most visual events (L01) — or deliberately few, as L10 (~10 SFX on 41 events)',
                     'An edit without SFX feels like a "silent movie": whoosh = move, pop = text in, chime = success, thud = impact.',
                     ['sound-sfx-every-event', 'sound-sfx-meaning-map', 'sound-bass-hit-text-pop'],
                     'Place SFX on the change times listed in xray.md (Real SFX skill or Edits → Sound effects): whoosh on moves, pop on text, hit on the payoff.'
                     if st != 'pass' else 'Keep it.'))

    # 7-8. loudness and true peak -----------------------------------------------------------------------------
    if not has_audio:
        out.append(R('loudness', 'Loudness near −14 LUFS', 8, 'n/a', 'no audio stream', '−14 LUFS ±1', '', ['sound-loudness-minus-14'], silent_note))
        out.append(R('true-peak', 'True peak ≤ −1 dBTP', 4, 'n/a', 'no audio stream', '≤ −1 dBTP', '', ['sound-loudness-minus-14'], silent_note))
    else:
        I_, tp, lra = au.get('integrated_lufs'), au.get('true_peak_dbtp'), au.get('lra_lu')
        st = 'fail' if I_ is None else 'pass' if -15 <= I_ <= -13 else 'warn' if -16.5 <= I_ <= -11.5 else 'fail'
        out.append(R('loudness', 'Loudness near −14 LUFS', 8, st, f"integrated {I_} LUFS, loudness range {lra} LU",
                     '−14 LUFS ±1 (range ~2–5 LU, heavily compressed)',
                     'All 12 measured Rahul reels sit at −14 LUFS with a 2.2–4.8 LU range; L10 measures −14.1 LUFS / 2.3 LU.',
                     ['sound-loudness-minus-14'],
                     'ffmpeg two-pass loudnorm=I=-14:TP=-1:LRA=4, then re-check with ebur128.' if st != 'pass' else 'Keep it.'))
        st = 'fail' if tp is None else 'pass' if tp <= -1.0 else 'warn' if tp <= 0.0 else 'fail'
        out.append(R('true-peak', 'True peak ≤ −1 dBTP', 4, st, f"true peak {tp} dBTP", '≤ −1 dBTP on the master',
                     'Headroom so the platform\'s re-encode does not clip (a decoded lossy file can read a little hotter than its master).',
                     ['sound-loudness-minus-14'], 'Limit at −1 dBTP (loudnorm TP=-1 or a true-peak limiter) before export.' if st != 'pass' else 'Keep it.'))

    # 9. music bed under the voice --------------------------------------------------------------------------
    if has_audio and has_speech:
        bu = au.get('bed_under_voice_db')
        if bu is None or au.get('bed_level_db') is None or au['bed_level_db'] < -55:
            st, meas = 'warn', 'no audible bed in the voice pauses'
        else:
            st = 'pass' if 6 <= bu <= 18 else 'warn'
            meas = f"bed in the pauses ~{bu} dB under the voice ({au['bed_level_db']} vs {au['speech_level_db']} dBFS)"
        out.append(R('music-bed', 'Quiet music bed under the voice', 4, st, meas, 'a bed running throughout, ~6–18 dB under the voice',
                     'A low bed under the whole video (Oren ~−22 to −24 dB; L10 ~7–10 dB under the voice) glues the cuts and hides breaths.',
                     ['sound-quiet-bed-throughout', 'sound-music-by-section'],
                     ('Add a low bed and duck it under the voice (CapCut: music volume low; ffmpeg sidechaincompress).' if 'no audible' in meas else
                      'Bed is too loud against the voice: pull it down / duck it.' if bu is not None and bu < 6 else
                      'Bed is barely audible: bring it up a few dB.') if st != 'pass' else 'Keep it.'))

    # 10. length -------------------------------------------------------------------------------------------
    plo, phi, wlo, whi = F['len']
    vibe = niche in VIBE_NICHES and fmt in ('reel30', 'yt-short') and not has_speech
    if vibe:
        plo, phi = 7, 20
    st = 'pass' if plo <= dur <= phi else 'warn' if wlo <= dur <= whi else 'fail'
    out.append(R('length', f'Length fits {fmt}', 8, st, f"{dur:.1f} s",
                 f"{plo}–{phi} s" + (' (vibe reel: 7–15 s ideal for completion and loops)' if vibe else ''),
                 '7–15 s for pure vibe reels (completion + loops), 20–60 s for tutorials/vlogs with value, under 3 min to stay eligible for non-follower recommendation.',
                 ['edit-length-by-type', 'growth-format-specs'],
                 ('Trim toward the target: cut the weakest beat, keep the payoff.' if dur > phi else 'Too short for this format: add a beat or pick a shorter format.')
                 if st != 'pass' else 'Keep it.'))

    # 11. export spec ------------------------------------------------------------------------------------------
    w, h, fps = m['width'], m['height'], m['fps']
    if F['vertical']:
        ok_size = (w, h) == (1080, 1920)
        ok_ratio = abs(w / h - 9 / 16) < 0.01
        st = 'pass' if ok_size and fps in (30, 60) or (ok_size and abs(fps - 30) < 0.1) else 'warn' if ok_ratio else 'fail'
        tgt = '1080×1920 (9:16), 30 fps (60 for slow-mo sources), SDR'
    else:
        st = 'pass' if abs(w / h - 16 / 9) < 0.01 and h >= 1080 else 'warn'
        tgt = '16:9, ≥ 1080p'
    if m.get('hdr'):
        st = 'warn' if st == 'pass' else st
    out.append(R('spec', 'Export spec', 4, st, f"{w}×{h}, {fps} fps{', HDR' if m.get('hdr') else ''}", tgt,
                 'Reels are delivered at 1080×1920 30 fps; HDR off unless the phone\'s HDR upload looks right.',
                 ['growth-format-specs'], 'ffmpeg: scale=1080:1920, -r 30, libx264 -crf 18 -pix_fmt yuv420p, SDR.' if st != 'pass' else 'Keep it.'))

    # 12. face check ------------------------------------------------------------------------------------------
    fc = X['faces']
    if not fc.get('model') or not fc.get('blendshapes'):
        out.append(R('face-check', 'Face check (eyes, mouth, angle)', 6, 'manual',
                     f"face model: {fc.get('model') or 'none'}{' (' + fc['model_error'][:120] + ')' if fc.get('model_error') else ''}",
                     'no frame with eyes mid-blink, mouth open / mid-word, tongue or an awkward angle where the face is held',
                     'Hard rule from Srijan\'s feedback: never use frames where the mouth is open or mid-word, the eyes are mid-blink or the angle is awkward.',
                     ['edit-face-check'], 'Scrub every held frame, the opening and closing frames and the cover by eye.'))
    elif not fc.get('face_share'):
        out.append(R('face-check', 'Face check (eyes, mouth, angle)', 6, 'pass', 'no face detected in any sample (2 per second)', '',
                     'Hard rule from Srijan\'s feedback (SYSTEM_PROMPT face check).', ['edit-face-check'],
                     'Nothing to check automatically; if a face is in frame but small or turned away, check the cover by eye.'))
    else:
        fl = fc.get('flagged', [])
        key = [f for f in fl if f.get('context') in ('opening frame', 'closing frame', 'held / still frame', 'animated still (pan/zoom)')]
        moving = [f for f in fl if f not in key]
        st = 'pass' if not key else 'warn' if len(key) <= 3 else 'fail'
        ks = '; '.join(f"{f['t']} s {f['context']}: {', '.join(f['flags'])}" for f in key[:6])
        out.append(R('face-check', 'Face check (eyes, mouth, angle)', 6, st,
                     f"face in {100 * fc['face_share']:.0f}% of samples; {len(key)} flagged where the face is held or opens/closes the video"
                     f"{' (' + ks + ')' if ks else ''}; {len(moving)} flagged mid-motion (normal while talking)",
                     'no flagged expression on opening / closing / held frames or the cover',
                     'Hard rule from Srijan\'s feedback: never use frames where the mouth is open or mid-word, the eyes are mid-blink or half-closed, the tongue shows or the angle is awkward.',
                     ['edit-face-check'],
                     ('Swap or trim those frames (see faces_flagged.png); for the cover pick a clear smile, a confident neutral look or a candid look-away with the mouth closed.'
                      if st != 'pass' else 'Keep it; still pick the cover frame by eye.'),
                     note='MediaPipe blendshapes (eyeBlink, jawOpen, tongueOut) and head pose; advisory, confirm by eye.'))

    # 13. easing ---------------------------------------------------------------------------------------------
    mv = X['motion']['moves']
    lin = [x for x in mv if x['curve'].startswith('linear')]
    near = [x for x in mv if x['curve'] == 'near-linear']
    bad = len(lin) + 0.5 * len(near)
    st = 'pass' if bad < 1 else 'warn' if bad <= 2 and len(lin) < max(2, len(mv) / 2) else 'fail'
    ls = '; '.join(f"{x['kind']} {x['t0']}–{x['t1']} s ({x['total']:+.0f}{x['unit'].split()[0]})" for x in (lin + near)[:6])
    out.append(R('easing', 'Eased moves, nothing linear', 6, st,
                 f"{len(mv)} sustained zoom/pan moves: {len(lin)} constant-speed, {len(near)} near-linear, {X['motion']['n_eased']} eased"
                 f"{' (' + ls + ')' if ls else ''}",
                 'every keyframed zoom / pan / slide eases (entrances ease out, exits ease in, UI springs)',
                 'Nothing in the real world moves at constant speed; linear motion starts and stops all at once and looks robotic. Our Khandala pans and push-ins were linear.',
                 ['fx-nothing-linear', 'fx-ease-out-entrances', 'fx-spring-ui', 'fx-khandala-linear-moves'],
                 ('Re-keyframe those moves with an ease (CapCut: keyframe → Graphs → ease out; ffmpeg zoompan/crop: replace t/d with 1-pow(1-t/d,3)).'
                  if st != 'pass' else 'Keep it.'),
                 note='Measured on the whole picture: a smooth filmed pan at constant speed also reads as linear.'))

    # 14. ending / loop -----------------------------------------------------------------------------------------
    en = X.get('ending') or {}
    words = transcript_words(xdir) if has_speech else []
    tail = ' '.join(w['w'] for w in words if w['s'] >= dur - 8)
    cta = bool(CTA_WORDS.search(tail))
    tail_ocr = ' '.join(b['text'] for s in X['samples'] if s['t'] >= dur - 4 for b in (s.get('text') or []))
    cta_txt = bool(re.search(r'comment|follow|save|share|send|link', tail_ocr))
    loop = en.get('loops_to_first_frame')
    black = en.get('ends_on_black')
    if loop or cta or cta_txt or black:
        st = 'pass'
    else:
        st = 'warn'
    meas = (f"last frame vs first: correlation {en.get('first_last_ncc')}, colour {en.get('first_last_hist_corr')} → {'loops' if loop else 'same scene, not the same frame' if en.get('similar_scene') else 'no loop'}; "
            f"{'ends on black' if black else 'no cut to black'}; CTA {'spoken' if cta else 'not spoken'} in the last 8 s"
            f"{', CTA-like text on screen' if cta_txt else ''}")
    out.append(R('ending', 'Ending: loop, CTA or a hard out', 6, st, meas,
                 'loop back to frame 1 (vibe reels / Shorts), or a clear CTA, or a thud + cut to black',
                 'Loopable edits win on watch time (Khandala ends on the sun and feet); a comment-keyword CTA drives comments; the L08 teaser ends on a thud and a hard cut to black.',
                 ['edit-loop-to-frame-1', 'growth-comment-keyword-cta', 'tr-cut-to-black-thud'],
                 (('The last frame is the same scene as the first but not the same framing: match it exactly (same crop and position) so the loop is seamless'
                   if en.get('similar_scene') else 'End on a frame that matches the first shot so the reel loops') + (' (preferred for this format)' if F['loop'] else '') +
                  ', or close with one CTA ("Comment KEYWORD…" / "send this to…").') if st != 'pass' else 'Keep it.'))

    # 15. punch-ins on talking heads ----------------------------------------------------------------------------
    if has_speech and (fc.get('face_share') or 0) >= 0.5:
        n_pi = len(c.get('punch_ins', [])) + sum(1 for x in mv if x['kind'] == 'zoom' and x['total'] > 3)
        per_min = n_pi / dur * 60
        st = 'pass' if per_min >= 3 or c['avg_shot_s'] <= 4 else 'warn'
        out.append(R('punch-ins', 'Punch-ins / jump cuts on the talking head', 4, st,
                     f"{n_pi} punch-ins or zoom moves ({per_min:.1f}/min); average camera shot {c['avg_shot_s']} s",
                     '105–110% punch-ins on key phrases, bigger 1.15–1.3× on punchlines; axial jump cuts every 3–6 words',
                     'Talking heads hold attention with digital punch-ins on emphasis words and new sections.',
                     ['fx-subtle-punch-in', 'fx-big-punch-in', 'edit-axial-jump-cuts'],
                     'Split on key phrases and scale the segment to 105–110% (1.15–1.3× on the punchline).' if st != 'pass' else 'Keep it.'))

    # 16. grade (info) -------------------------------------------------------------------------------------------
    g = X['colour']
    gid = {'gym': ['colour-gym-grade'], 'travel': ['colour-golden-hour-grade'], 'tech': ['colour-dark-matte-warm-key', 'l10-moody-grade-recipe'],
           'gaming': ['colour-neon-high-contrast']}.get(niche or '', [])
    if gid:
        notes = []
        if niche == 'gym':
            notes.append('cool/neutral' if g['warmth_r_minus_b'] <= 5 else f"warm (R−B {g['warmth_r_minus_b']:+}) — the gym grade is cooler or neutral")
            notes.append('contrasty' if g['contrast_sd'] >= 55 else f"flat-ish (luma SD {g['contrast_sd']}) — the gym grade has higher contrast")
        elif niche == 'travel':
            notes.append('warm' if g['warmth_r_minus_b'] > 5 else f"neutral/cool (R−B {g['warmth_r_minus_b']:+}) — golden hour wants warm mids")
        elif niche == 'tech':
            notes.append('low-key' if g['mean_luma'] < 90 else 'bright')
        elif niche == 'gaming':
            notes.append('saturated' if g['satavg_signalstats'] >= 15 else 'muted — the neon look wants saturated accents')
        out.append(R('grade', f'Grade vs the {niche} look', 0, 'info',
                     f"YAVG {g['yavg_signalstats']}, contrast SD {g['contrast_sd']}, SATAVG {g['satavg_signalstats']}, warmth R−B {g['warmth_r_minus_b']:+} → {', '.join(notes)}",
                     ATOMS.get(gid[0], {}).get('text', '')[:160], 'Each niche has a grade recipe in the Brain; this is a reading, not a score.', gid,
                     ATOMS.get(gid[0], {}).get('how') or 'See the atom recipe.'))
    return out


def score(rs):
    sc = [r for r in rs if r['status'] in SCORE and r['weight'] > 0]
    tw = sum(r['weight'] for r in sc)
    return round(100 * sum(r['weight'] * SCORE[r['status']] for r in sc) / tw) if tw else None, tw


ICON = {'pass': 'PASS', 'warn': 'WARN', 'fail': 'FAIL', 'manual': 'MANUAL', 'n/a': 'n/a', 'info': 'info'}


def render(D, X):
    m = X['meta']
    L = [f"# Reel Doctor: {os.path.basename(m['file'])}\n"]
    L.append(f"**Brain checklist score: {D['score']}/100** · format `{D['format']}`{' (guessed)' if D['format_guessed'] else ''} · niche `{D['niche'] or '-'}` · "
             f"{m['duration_s']:.1f} s {m['width']}×{m['height']} {'with audio' if m['has_audio'] else 'silent export'}\n")
    L.append('> This scores the draft against explicit production rules in the Brain (each cites its atom ids). '
             'It is **not** a virality prediction: views depend on the idea, the audience and timing, and a rule can be broken on purpose.\n')
    cnt = {}
    for r in D['rules']:
        cnt[r['status']] = cnt.get(r['status'], 0) + 1
    L.append('Results: ' + ' · '.join(f"{v} {k}" for k, v in sorted(cnt.items(), key=lambda kv: ['pass', 'warn', 'fail', 'manual', 'n/a', 'info'].index(kv[0]))) +
             f" (scored over {D['scored_weight']} of {sum(r['weight'] for r in D['rules'])} rule points; n/a, manual and info rules are not scored)\n")
    fixes = sorted([r for r in D['rules'] if r['status'] in ('fail', 'warn', 'manual')],
                   key=lambda r: (['fail', 'warn', 'manual'].index(r['status']), -r['weight']))
    if fixes:
        L.append('## Fix first\n')
        for k, r in enumerate(fixes[:8], 1):
            L.append(f"{k}. **{r['title']}** ({ICON[r['status']]}): {r['fix']}")
        L.append('')
    L.append('## Checklist\n')
    L.append('| Rule | Result | Measured | Target | Brain atoms |')
    L.append('|---|---|---|---|---|')
    for r in D['rules']:
        at = ', '.join(f"`{a['id']}`" for a in r['atoms'])
        L.append(f"| {r['title']} (w{r['weight']}) | **{ICON[r['status']]}** | {r['measured']} | {r['target']} | {at} |")
    L.append('')
    L.append('## Why each rule matters, and the fix\n')
    for r in D['rules']:
        L.append(f"### {r['title']}: {ICON[r['status']]}\n")
        L.append(f"- **Measured:** {r['measured']}")
        if r['target']:
            L.append(f"- **Target:** {r['target']}")
        if r['why']:
            L.append(f"- **Why:** {r['why']}")
        L.append('- **Brain:** ' + '; '.join(f"`{a['id']}` {a['title']} [{', '.join(a['sources'])}]" for a in r['atoms']))
        if r['fix']:
            L.append(f"- **Fix:** {r['fix']}")
        if r.get('note'):
            L.append(f"- *Note:* {r['note']}")
        L.append('')
    L.append('## Evidence\n')
    L.append(f"X-ray: `{os.path.relpath(D['xray_dir'], D['out_dir'])}/xray.md` (production table), `timeline.png`, `contact_sheet.png`, `changes_sheet.png`"
             + (', `faces_flagged.png`' if os.path.exists(os.path.join(D['xray_dir'], 'faces_flagged.png')) else '') + '.')
    return '\n'.join(L) + '\n'


def main(argv=None):
    ap = argparse.ArgumentParser(description='Reel Doctor: Brain checklist score for a draft (not a virality prediction).')
    ap.add_argument('draft', help='draft video file (or URL)')
    ap.add_argument('--format', choices=sorted(FORMATS), help='target format (default: guessed from length and aspect)')
    ap.add_argument('--niche', choices=['gym', 'tech', 'gaming', 'travel'])
    ap.add_argument('-o', '--out', help='output folder (default ./doctor_<name>)')
    ap.add_argument('--listen', action='store_true', help='run earshot to label SFX (slower)')
    ap.add_argument('--reuse-xray', help='use an existing X-ray folder (xray.json) instead of re-running it')
    ap.add_argument('--whisper-model', default='small')
    ap.add_argument('--lang')
    a = ap.parse_args(argv)
    name = re.sub(r'[^A-Za-z0-9_-]+', '_', os.path.splitext(os.path.basename(a.draft.rstrip('/')))[0])[:40] or 'draft'
    out = a.out or os.path.join(os.getcwd(), f'doctor_{name}')
    os.makedirs(out, exist_ok=True)
    if a.reuse_xray:
        xdir = a.reuse_xray
        with open(os.path.join(xdir, 'xray.json')) as fh:
            X = json.load(fh)
    else:
        xdir = os.path.join(out, 'xray')
        X = xray.run(a.draft, xdir, listen_req=a.listen, whisper_model=a.whisper_model, lang=a.lang)
    fmt = a.format or guess_format(X)
    rs = rules(X, fmt, a.niche, xdir)
    sc, tw = score(rs)
    D = {'tool': 'Reel Doctor', 'score': sc, 'score_label': 'Brain checklist score (not a virality prediction)',
         'format': fmt, 'format_guessed': a.format is None, 'niche': a.niche, 'scored_weight': tw,
         'video': X['meta']['file'], 'xray_dir': os.path.abspath(xdir), 'out_dir': os.path.abspath(out), 'rules': rs}
    with open(os.path.join(out, 'doctor.json'), 'w') as fh:
        json.dump(D, fh, indent=1, ensure_ascii=False)
    with open(os.path.join(out, 'doctor.md'), 'w') as fh:
        fh.write(render(D, X))
    print(f"Brain checklist score {sc}/100 ({fmt}{', ' + a.niche if a.niche else ''}) -> {os.path.join(out, 'doctor.md')}")
    return D


if __name__ == '__main__':
    main()
