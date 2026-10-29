# Srijan's media library

Sound effects, meme notes, transitions and a mixing guide for short-form reels (gym, tech/PC, gaming, travel), edited in
Instagram Edits, CapCut and VN, or with ffmpeg + HyperFrames. Every file in `sfx/` has a clean licence: **CC0**,
or **CC BY** with the credit written down in `catalog.json`.

## Index

| Path | What |
|---|---|
| [`catalog.json`](catalog.json) | One entry per sound (2151): id, file, category, subtype, tier, featured, duration_s, lufs, peak_db, licence, source_url, author, attribution, use_when, pairs_with_transition, niches, earshot verdict |
| `sfx/<category>/` | 2151 trimmed, loudness-normalised MP3s (128 kbps, 44.1 kHz) in 30 categories (39M) |
| [`memes/MEMES.md`](memes/MEMES.md), `memes/memes.json` | 70 meme sounds/formats: meaning, frame timing, visual pairing, Edits + CapCut search terms, CC0 recreation if one exists, risk |
| `meme-images/`, `memes/meme_images.json` | Top 100 imgflip meme templates + usage notes (12M) |
| [`transitions/TRANSITIONS.md`](transitions/TRANSITIONS.md), `transitions/transitions.json` | 32 transitions: when, paired SFX files, frames at 30 fps, easing, CapCut/Edits/VN steps, filming, ffmpeg/HyperFrames |
| [`mixing/MIXING.md`](mixing/MIXING.md) | Levels (L06: lo-fi bed −22 to −24 dB under voice), ducking, iPhone voice chain, loudness targets, gym beat-sync, ffmpeg recipes, earshot QA checklist |
| `raw/kenney/<pack>/` | Untouched Kenney CC0 packs for digging (10 packs, 18M) |
| `raw/opengameart_sources.json` | Index of the 166 CC0-only OpenGameArt items used (URL, author, title). The raw files themselves were not kept (482 MB; dropped to save disk); re-download from the URLs |
| [`local-only/`](local-only/LICENCE-NOTE.md) | Tier for Mixkit / Sonniss files, which are free to use in videos but may NOT be redistributed. Empty: both sites block this container (see the note) |
| `tools/` | The pipeline that built all of this: OpenGameArt search, in-house DSP (`synth_inhouse.py`), staging + earshot judging, selection, normalise/encode (`build_library.py`), doc generators |

## How to pick a sound fast

1. Open the category folder. Files with `"featured": true` in `catalog.json` are the earshot-ranked top picks (listed below). The rest are the full CC0 packs, sorted into the same categories.
2. Every file is pre-normalised. Short clicks/pops sit lower because they hit the −1 dBTP ceiling first. Turn sounds **down** in the editor, never up (see MIXING.md §1 for starting levels).
3. MP3 adds ~26 ms of encoder delay at the start (under 1 frame at 30 fps). For frame-exact work in ffmpeg, use the `raw/kenney/` original, or re-download the OpenGameArt source (URL in `catalog.json`).

## Counts

**Total:** 2151 sounds, 94 featured. **Tiers:** cc0: 2151. **Sources:** OpenGameArt: 1382, Kenney: 734, in-house: 27, uisfx: 8.

| Category | Featured | All | Featured files (best first) |
|---|---|---|---|
| `whoosh` | 5 | 15 | inhouse-whoosh_inhouse_big_dark.mp3, inhouse-whoosh_inhouse_air_soft.mp3, oga-swishes-sound-pack-swish-5.mp3, oga-swishes-sound-pack-swish-4.mp3, inhouse-whoosh_inhouse_bright_pass.mp3 |
| `swoosh-fast` | 5 | 42 | oga-3-melee-sounds-melee_sound.mp3, oga-swishes-sound-pack-swish-9.mp3, oga-3-melee-sounds-sword_sound.mp3, oga-swishes-sound-pack-swish-8.mp3, inhouse-swoosh_inhouse_flick.mp3 |
| `pop` | 5 | 41 | oga-pop-sounds-pop4.mp3, oga-pop-sounds-pop8.mp3, oga-pop-effect-sounds-p_2.mp3, oga-bubbles-pop-pop.mp3, oga-pop-effect-sounds-p_4.mp3 |
| `click-ui` | 5 | 221 | oga-10-clicks-and-switches-click.9.mp3, oga-button-click-sound-effect-cc-qubodup-click2.mp3, kenney-interface-tick_001.mp3, oga-button-click-sound-effect-cc-qubodup-hover1.mp3, kenney-ui-click4.mp3 |
| `keyboard` | 4 | 15 | oga-keyboard-soundpack-1-typing--keypress-017.mp3, oga-keyboard-soundpack-1-typing--keypress-001.mp3, oga-keyboard-soundpack-1-typing--keypress-005.mp3, uisfx-studio-typing.mp3 |
| `typing` | 4 | 26 | oga-keyboard-soundpack-1-typing--generated-003_slow.mp3, oga-keyboard-soundpack-1-typing--generated-004_medium.mp3, oga-typing-soundeffect-typing_0.mp3, oga-typewriter-sounds-typewriter4.mp3 |
| `hit-impact` | 6 | 228 | oga-thwack-sounds-thwack-07.mp3, oga-thwack-sounds-thwack-03.mp3, oga-75-cc0-breaking-falling-hit--bfh1_hit_08.mp3, oga-75-cc0-breaking-falling-hit--bfh1_hit_06.mp3, kenney-impact-impactPunch_medium_000.mp3, kenney-impact-impactPunch_heavy_001.mp3 |
| `bass-drop-boom` | 5 | 59 | kenney-sci-fi-lowFrequency_explosion_000.mp3, oga-muffled-distant-explosion-NenadSimic_-_Muffled_Distant_Explosion.mp3, kenney-sci-fi-lowFrequency_explosion_001.mp3, inhouse-subdrop_inhouse_long.mp3, inhouse-subdrop_inhouse_short.mp3 |
| `riser` | 4 | 4 | inhouse-riser_inhouse_tonal_5s.mp3, inhouse-riser_inhouse_noise_4s.mp3, inhouse-riser_inhouse_noise_8s.mp3, inhouse-riser_inhouse_shepard_6s.mp3 |
| `downlifter` | 3 | 5 | inhouse-downlifter_inhouse_air_5s.mp3, inhouse-downlifter_inhouse_noise_3s.mp3, inhouse-downlifter_inhouse_tonal_3s.mp3 |
| `glitch` | 4 | 7 | inhouse-glitch_inhouse_stutter.mp3, inhouse-glitch_inhouse_data.mp3, inhouse-glitch_inhouse_zap.mp3, kenney-sci-fi-computerNoise_002.mp3 |
| `camera-shutter` | 3 | 6 | oga-camera-photo.mp3, inhouse-shutter_inhouse_mech_a.mp3, inhouse-shutter_inhouse_mech_b.mp3 |
| `notification-ding` | 5 | 38 | oga-alertnotification-sound-alert.mp3, uisfx-studio-notification.mp3, kenney-interface-confirmation_001.mp3, uisfx-glass-notification.mp3, kenney-interface-confirmation_002.mp3 |
| `chime-success` | 5 | 42 | uisfx-glass-achievement.mp3, uisfx-glass-success.mp3, uisfx-studio-complete.mp3, uisfx-dreamy-achievement.mp3, uisfx-glass-complete.mp3 |
| `record-scratch` | 3 | 5 | inhouse-scratch_inhouse_baby.mp3, oga-scratch-vocal-sound-scroutch.mp3, inhouse-scratch_inhouse_baby_fast.mp3 |
| `rewind-tape-stop` | 3 | 3 | inhouse-tapestop_inhouse_hit.mp3, inhouse-tapestop_inhouse_sax.mp3, inhouse-rewind_inhouse_vhs.mp3 |
| `crowd-cheer-applause` | 3 | 8 | oga-applause-in-a-large-hall-or--applause-clapping-church-crowd-immersive.mp3, oga-well-done-Well_Done_CCBY3.mp3, oga-oooooooooooooo-oooooooooo.mp3 |
| `gym` | 6 | 30 | oga-75-cc0-breaking-falling-hit--bfh1_metal_falling_01.mp3, oga-75-cc0-breaking-falling-hit--bfh1_metal_falling_02.mp3, oga-75-cc0-breaking-falling-hit--bfh1_metal_falling_03.mp3, oga-metal-impact-sounds-clink2.mp3, oga-metal-impact-sounds-bing1.mp3, oga-metal-impact-sounds-clink1_0.mp3 |
| `gaming` | 6 | 411 | oga-50-cc0-retro-synth-sfx-power_up_01.mp3, oga-50-cc0-retro-synth-sfx-power_up_04.mp3, oga-10-8bit-coin-sounds-coin2.mp3, oga-10-8bit-coin-sounds-coin3.mp3, kenney-music-jingles-jingles_NES05.mp3, kenney-music-jingles-jingles_NES00.mp3 |
| `cash-register` | 4 | 72 | inhouse-register_inhouse_chaching.mp3, oga-purchasing-sound-effect-snd_purchase_0.mp3, oga-80-cc0-rpg-sfx-item_coins_04.mp3, oga-80-cc0-rpg-sfx-item_coins_02.mp3 |
| `heartbeat` | 3 | 7 | oga-heartbeat-sounds-heartbeat_fast_reverb.mp3, oga-heartbeat-sounds-heartbeat_slow_reverb.mp3, oga-heartbeat-sounds-heartbeat_fast_0.mp3 |
| `meme-cc0` | 3 | 3 | inhouse-censor_beep_1khz.mp3, inhouse-sad_trombone_inhouse.mp3, inhouse-rimshot_badumtss_inhouse.mp3 |
| `foley` | 0 | 269 |  |
| `foley-cards-dice` | 0 | 35 |  |
| `foley-footsteps` | 0 | 54 |  |
| `jingles` | 0 | 68 |  |
| `sci-fi` | 0 | 178 |  |
| `ui-error` | 0 | 8 |  |
| `ui-open-close` | 0 | 39 |  |
| `voice-announcer` | 0 | 212 |  |

## Licence policy

- **Allowed in `sfx/` and `raw/`:** CC0 / public domain, or CC BY with the attribution recorded (`attribution` field; put it in the caption when you use the sound).
- **Licences in this library:** CC0-1.0: 2150 files; CC0-1.0 / CC-BY-3.0 (file name says CC-BY 3.0; credit given): 1 files.
- **Sources used:** Kenney.nl audio packs (CC0); OpenGameArt items whose every listed licence is CC0. One item, qubodup's "Well Done", is listed CC0 but its file name says CC BY 3.0, so it is credited as CC BY to be safe. uisfx (CC0 audio, vendored in `.claude/skills/real-sfx/vendor`). In-house sounds made with numpy/scipy DSP, from scratch or from CC0 Kenney recordings, are dedicated CC0 (`tools/synth_inhouse.py`).
- **Never committed:** Mixkit, Pixabay, Zapsplat, myinstants, BBC Sound Effects (non-commercial only), anything ripped from games, films, TV or other creators. Meme audio is reached through the **Instagram Edits / CapCut in-app libraries** (search terms in MEMES.md). Mixkit and Sonniss files may only ever live in `local-only/`.
- **Meme images** (`meme-images/`) are third-party templates. Use them only for commentary or parody with your own caption; never in ads.
- **Blocked from this container (2026-10-27):** Openverse API (504 timeouts), the Freesound CDN, Pixabay, BigSoundBank and GIPHY (403), Wikimedia Commons (429 rate limit), Mixkit (Cloudflare challenge), Sonniss (403).

## Existing tools and how they relate

- **earshot** (`~/sm-tools/earshot`, MIT): used to judge every featured pick (`api.rank` against a text description, CLAP z-score + verdict) and to audit every file (`sfx check`: clipping, clicks, DC, cut tails, comb ring). Its 252-sound bank is code-synthesised and renders on demand (`earshot sfx render whoosh_fast/crisp -o w.wav`, `earshot kit`). It is MIT-licensed code, not CC0 audio, so renders are **referenced, not committed**. Good bank ids: `whoosh_fast/*`, `riser/*`, `downlifter/*`, `cut_hit/*`, `shutter/*`, `glitch/*`, `notify/*`, `typing_key/*`.
- **real-sfx** skill (`.claude/skills/real-sfx`): its vendored **uisfx** pack (936 MP3s = 78 UI cues × 12 styles, audio CC0) is usable. The featured chime/notification/keyboard picks come from it. To have real-sfx place sounds from this library, register it: `python scripts/setup.py add-library srijan library/sfx --tier main --index`. That works because `catalog.json` gives each file its type.
- **real-sound** skill: the process for full soundtracks (cue list, licence checks, mixer, QA). Use it with this library as the source.

## Rebuild

```bash
S=<scratch dir>; L=library   # then: python3 -I $L/tools/fix_categories.py $L
python3 -I $L/tools/oga_search.py $S/dl/oga whoosh pop ...              # OpenGameArt CC0 index + files
$EARSHOT_VENV/python -I $L/tools/synth_inhouse.py $S/dl $S/synth        # in-house CC0 sounds
$EARSHOT_VENV/python -I $L/tools/stage_and_judge.py POOL.json $S/synth $S/stage   # trim + earshot rank/audit
python3 -I $L/tools/select_featured.py sel.json $S/stage/judged.json ...   # featured picks
python3 -I $L/tools/assemble.py sel.json full_judged.json build.json && python3 -I $L/tools/build_library.py build.json $L
python3 -I $L/tools/gen_docs.py $L $L/tools/data/memes_src.json $L/tools/data/transitions_src.json && python3 -I $L/tools/gen_readme.py $L
```
