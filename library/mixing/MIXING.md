# Mixing guide for Srijan's reels

Practical levels, ducking, voice cleanup, loudness targets, gym beat-sync, ffmpeg recipes and an earshot QA pass.
It applies to Instagram Edits, CapCut and VN on the phone, and to our ffmpeg/HyperFrames pipeline.

---

## 1. The level ladder (what sits where)

Use the voice as the anchor and set everything else relative to it. The numbers below are **short-term loudness (LUFS-S)**
while that element is playing. Our Brain rule from L06 (Oren, *Art of Yapping*): **the lo-fi/chill-hop bed sits at about
−22 to −24 dB under the voice**, i.e. around −22 to −24 LUFS while the voice runs at about −14 to −16 LUFS, which is
8-10 LU of separation. ([brain/lessons/06_oren-art-of-yapping.md](../../brain/lessons/06_oren-art-of-yapping.md); see also L01:
"one quiet music bed plus an SFX for every visual event", and L07: riser + sub-boom at chapter edges.)

| Element | Target while playing | Relative to voice | Notes |
|---|---|---|---|
| Voice (VO / talking head) | −14 to −16 LUFS-S, peaks ≤ −3 dBFS before the limiter | 0 (anchor) | Compressed and de-essed (section 3) |
| Music bed under voice | **−22 to −24 LUFS-S** [L06] | −8 to −10 LU | Duck with sidechain, or set it there and leave it |
| Music with no voice (montage, drop) | −14 to −15 LUFS-S | music becomes the anchor | Bring it up over 6-10 frames when the voice stops |
| UI one-shots (click, pop, ding) | −20 to −24 LUFS-M (momentary) | −6 to −10 LU | Felt more than heard; they must not mask consonants |
| Whooshes / swooshes | −18 to −22 LUFS-M | −4 to −8 LU | Peak on the cut (find the loudest moment with `earshot timeline` or by eye on the waveform) |
| Impacts, booms, sub drops | −14 to −18 LUFS-M, peak ≤ −1 dBTP after master | −0 to −4 LU | Sub content (< 60 Hz) disappears on phone speakers: layer a mid-range hit too |
| Risers | ramp from −30 to −18 LUFS-M | ends −4 LU under voice | Cut them dead on the downbeat/cut |
| Ambience (crowd, room tone, city) | −28 to −32 LUFS-S | −14 LU+ | Continuity glue; fade 10 frames in/out |
| Meme stings (vine boom, bruh...) | about voice level, once | 0 to −3 LU | Pause the voice for it; never stack two |

**Our library files are pre-normalised** (`catalog.json` → `lufs`, `peak_db`): one-shots to **−16 LUFS-I** (two-pass loudnorm, linear) or to a **−1.5 dBTP** pre-encode ceiling (all files measure ≤ −1 dBTP after MP3), whichever comes first (short clicks and pops hit the ceiling first, so they measure quieter than −16). So when you drop
one into the timeline, turn it **down**, never up:

| Category | Starting fader on a library file | Approx. CapCut / Edits volume (linear %) |
|---|---|---|
| click-ui, keyboard, typing, pop | −8 to −12 dB | 25-40 % |
| notification-ding, chime-success, gaming | −6 to −10 dB | 30-50 % |
| whoosh, swoosh-fast | −6 to −10 dB | 30-50 % |
| hit-impact, bass-drop-boom, gym | −2 to −6 dB | 50-80 % |
| riser, downlifter, rewind/tape-stop, glitch | −6 to −10 dB | 30-50 % |
| crowd-cheer-applause, heartbeat | −10 to −16 dB | 15-30 % |

(dB to linear: −6 dB ≈ 50 %, −10 dB ≈ 32 %, −12 dB ≈ 25 %, −20 dB = 10 %. Phone editors label volume in percent, CapCut desktop in dB.)

**Density rule.** One sound per visual event (L01/L02), but at most **one foreground SFX every ~0.5 s** under speech. If two
events are closer than 8 frames, keep the more important one, or turn the second down 6 dB.

---

## 2. Ducking (sidechain) so the voice always wins

- **Phone editors:** CapCut has *Audio > Volume > "Ducking"* (applies to the music track while voice plays); in Edits/VN,
  split the music at sentence boundaries and drop the segments under speech by 8-10 dB with 4-6 frame fades.
  Ducking that is set by hand per sentence sounds better than automatic ducking, which pumps.
- **ffmpeg:** `sidechaincompress` with the voice as the key (recipe 6.3). Settings that sound natural on music beds: threshold
  0.03-0.05, ratio 6-10, attack 20 ms, release 250-400 ms. Fast release pumps on every word, which is wrong for a lo-fi bed
  and fine for a phonk edit.
- **Duck amount:** −6 to −10 dB of gain reduction under talking, back to full level within 0.3-0.5 s of the voice stopping.
- **SFX are never ducked**: place them at their own level.

---

## 3. iPhone voice cleanup chain (in this order)

| Step | Why | ffmpeg filter | Phone-app equivalent |
|---|---|---|---|
| 1. High-pass 80-100 Hz | Removes handling rumble, AC, traffic | `highpass=f=90` | CapCut *Voice enhance*; Edits *Enhance voice* |
| 2. Noise reduction (light) | Hiss/room noise from the iPhone mic | `afftdn=nr=10:nf=-40` (≤ 12 dB, or speech goes underwater) | CapCut *Reduce noise* |
| 3. Mud cut −2 to −4 dB at 200-350 Hz | iPhone close-mic boominess | `equalizer=f=250:t=q:w=1.2:g=-3` | EQ preset "Voice" |
| 4. Presence +1.5 to +3 dB at 3-5 kHz | Intelligibility on phone speakers | `equalizer=f=4000:t=q:w=1:g=2` | — |
| 5. Compressor 3:1 | Even level word to word | `acompressor=threshold=-20dB:ratio=3:attack=5:release=120:makeup=3` | — |
| 6. De-ess (5-8 kHz) | Sibilance gets harsh after compression and AAC encoding | `deesser=i=0.4:m=0.5:f=0.5` | — |
| 7. Loudness | Final voice around −16 LUFS before the mix | `loudnorm` (recipe 6.1) | — |

Recording beats repair: lav/Røde plug-in mic (L06 gear list), phone 20-30 cm from the mouth, soft room (curtains, bed), and
**3 s of room tone** before each take (useful for noise prints and J/L-cuts).

---

## 4. Loudness targets for the export (and where the numbers come from)

| Platform | Integrated target | True peak | Status |
|---|---|---|---|
| **YouTube (long + Shorts)** | **−14 LUFS** | −1 dBTP | **Observed, not published.** YouTube turns loud uploads down to ~−14 LUFS and never turns quiet ones up. You can read the offset in *Stats for nerds → "content loudness"* (positive = YouTube turns you down). Sources: productionadvice.co.uk/stats-for-nerds; forasoft.com "LUFS targets per platform 2026". No source we found treats Shorts separately; they are assumed to share YouTube's normalisation |
| **Instagram Reels / Facebook** | **−14 LUFS (aim −14 to −16)** | −1 dBTP (−1.5 safer for AAC) | **No published Meta spec.** Every number online is an estimate; observed behaviour clusters around −14 LUFS (forasoft 2026; filmandflow "ultimate LUFS guide"; opus.pro loudness normalizer list) |
| **TikTok** | −14 LUFS (estimate) | −1 dBTP | No published spec (same sources) |
| **Spotify (reference only)** | −14 LUFS | −1 dBTP (−2 recommended on upload) | **Official**: Spotify for Artists, "Loudness normalization on Spotify" |

**What we do:** master every reel to **−14 LUFS integrated, −1.5 dBTP, LRA ≤ 9 LU**. That is loud enough not to sound
quiet next to other reels in the feed, and it leaves headroom for the AAC transcode, which raises peaks by 0.5-1 dB.
Mixes that are much louder (−9 to −10 LUFS) only get turned down on YouTube, and on Instagram they lose punch to the limiter.

When Srijan adds the song **inside Instagram Edits** after our export, the app mixes it on top. Then export our voice + SFX
stem at about **−16 LUFS**, so the song added in the app has room, and set the in-app music slider to roughly 15-25 %.

---

## 5. Music-to-rep beat sync for gym clips

1. **Measure the reps.** Note the frame of each lockout (top of a squat, arms straight on a press). Rep interval
   `r` = average frames between lockouts / 30 (seconds).
2. **Pick the tempo.** One rep per bar: `BPM = 240 / r` (a 2.8 s rep gives 86 BPM). One rep per two beats: `BPM = 120 / r`.
   Phonk and drift tracks are mostly 120-150 BPM, so they suit **half-bar reps** (r = 0.8-1.0 s, for fast sets) or
   **one rep per 2 bars** with slow eccentrics.
3. **Fix the footage, not the song.** Speed the clip by up to ±8 % (`setpts=PTS/1.06`) so `r` fits the grid. Changing music
   speed is audible; changing a lift's speed by 6 % is not.
4. **Anchor the first lockout on a downbeat** (beat 1 of a bar). Every later lockout then lands on a beat. Put the
   **drop** of the song on the **top set's lockout**, with a zoom punch, shake and boom (see TRANSITIONS: speed-ramp, camera-shake).
5. **Cut on beats, move cuts 1 frame early** (the eye lags the ear). At 30 fps: 120 BPM = 15 frames/beat, 128 = 14.06,
   140 = 12.86 (alternate 13/13/13/12), 150 = 12.
6. **Beat grid tools:** `earshot timeline song.mp3` (beat grid + sections), `npx hyperframes beats --json` (hit times for
   HyperFrames scenes), CapCut *Beat > Auto generate*.
7. Rep-count SFX: a soft click or 8-bit coin on each lockout at −12 dB; a chime-success or crowd cheer on the last rep.

---

## 6. ffmpeg recipes

### 6.1 Two-pass loudnorm (linear, measured)
```bash
# pass 1: measure
ffmpeg -hide_banner -i mix.wav -af loudnorm=I=-14:TP=-1.5:LRA=9:print_format=json -f null - 2> ln.txt
# read input_i, input_tp, input_lra, input_thresh, target_offset from the JSON at the end of ln.txt, then pass 2:
ffmpeg -i mix.wav -af "loudnorm=I=-14:TP=-1.5:LRA=9:measured_I=-19.3:measured_TP=-3.1:measured_LRA=6.2:measured_thresh=-29.8:offset=0.4:linear=true,aresample=48000" -c:a aac -b:a 256k mix_master.m4a
```
If `normalization_type` in the pass-2 JSON says *dynamic*, the true-peak ceiling could not be held linearly. Lower `I` by 1 LU,
or put `alimiter=limit=0.84` before loudnorm. Always end with `aresample` (loudnorm works at 192 kHz internally).

### 6.2 Voice chain (iPhone)
```bash
ffmpeg -i voice.m4a -af "highpass=f=90,afftdn=nr=10:nf=-40,equalizer=f=250:t=q:w=1.2:g=-3,equalizer=f=4000:t=q:w=1:g=2,acompressor=threshold=-20dB:ratio=3:attack=5:release=120:makeup=3,deesser=i=0.4:m=0.5:f=0.5" voice_clean.wav
```

### 6.3 Duck the music under the voice (sidechain)
```bash
ffmpeg -i music.mp3 -i voice_clean.wav -filter_complex \
"[1:a]asplit=2[vkey][vmix];[0:a]volume=-6dB[m];[m][vkey]sidechaincompress=threshold=0.04:ratio=8:attack=20:release=300:makeup=1[mduck];[mduck][vmix]amix=inputs=2:duration=longest:normalize=0[out]" \
-map "[out]" mix.wav
```

### 6.4 Place SFX on exact frames (frame N at 30 fps → N/30 s → ms)
```bash
# whoosh peaking on the cut at frame 96 (3.200 s). inhouse-whoosh_inhouse_big_dark.mp3 peaks 0.84 s in
# (built with its peak at 60 % of 1.4 s), so start it at 3.200 - 0.840 = 2.360 s
ffmpeg -i mix.wav -i library/sfx/whoosh/inhouse-whoosh_inhouse_big_dark.mp3 -filter_complex \
"[1:a]adelay=2360|2360,volume=-8dB[w];[0:a][w]amix=inputs=2:duration=first:normalize=0" mix_sfx.wav
```
Use `normalize=0` in `amix`, otherwise every input is turned down by 1/N.

### 6.5 Fades, trims, cleanup
```bash
ffmpeg -i in.wav -af "atrim=0:3.5,afade=t=in:d=0.005,afade=t=out:st=3.2:d=0.3" out.wav   # trim + click-free fades
ffmpeg -i in.wav -af "silenceremove=start_periods=1:start_threshold=-50dB" out.wav          # strip leading silence
ffmpeg -i in.wav -af "highpass=f=30,lowpass=f=16000" out.wav                                  # rumble/ultrasonic cleanup
ffmpeg -i in.wav -af ebur128=peak=true -f null -                                              # measure I, LRA, true peak
```

### 6.6 Mux the final audio onto the edit
```bash
ffmpeg -i edit.mp4 -i mix_master.m4a -map 0:v -map 1:a -c:v copy -c:a copy -shortest final.mp4
```

### 6.7 Library maintenance
`library/tools/build_library.py` holds the exact trim, normalise and encode code used for `library/sfx`
(two-pass `loudnorm` with `linear=true`, −16 LUFS or the −1 dBTP ceiling, MP3 128 kbps, final true peak re-measured).

---

## 7. earshot QA checklist (before posting)

earshot is installed at `~/sm-tools/earshot` (`source .venv/bin/activate; export EARSHOT_HOME=~/sm-tools/earshot`).
`measure`, `sfx` and `kit` load no models (fast). The other commands load models in 20-40 s per call, so for many files use one
Python process (`from earshot import api`) or `earshot mcp`.

- [ ] `earshot measure final.mp4`: integrated **−14 ±1 LUFS**, true peak **≤ −1 dBTP**, LRA ≤ 9 LU.
- [ ] `earshot timeline final.mp4 --video final.mp4`: every SFX event lands within **±1 frame (33 ms)** of its cut/text
      pop; no SFX louder than the voice except the single meme/impact moment; no silent holes > 1.5 s unless they are a deliberate beat.
- [ ] `earshot sheet final.mp4 -o qa.png`: look at the loudness lane. The bed should sit in a flat band 8-10 LU under the voice.
- [ ] `earshot sfx check file.wav` on any new or edited sound: no clipping, no clicks, no cut tails, no DC.
- [ ] `earshot match file.mp3 "a fast air whoosh" --alts "wind" "a sword swing"` when unsure a sound reads as intended.
- [ ] `earshot critique final.mp4` (launch-film scorecard): use only as a hint. Its profile is product launch films, not reels.
- [ ] Mono check: `ffmpeg -i final.mp4 -af "pan=mono|c0=0.5*c0+0.5*c1" mono.wav` and listen: phone speakers are mono, so
      wide stereo whooshes must not vanish.
- [ ] Phone-speaker check: listen once on the iPhone speaker at 50 % volume. Can you understand every word? Is any SFX painful?
- [ ] Licence check: every sound comes from `library/` (CC0/CC-BY, credits in `catalog.json`) or from the in-app library.
      Nothing ripped. Any CC-BY credit goes into the caption.
