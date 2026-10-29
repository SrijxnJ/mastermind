# Transitions playbook

32 transitions for Srijan's reels. Each one lists what it is, when to use it, the paired SFX (with files from `library/sfx`), frame timing at **30 fps**, the easing curve, how to build it in CapCut, Instagram Edits and VN, how to film for it, and the ffmpeg / HyperFrames route.

**Easing rules (Brain L03):** entrances **ease-out** (fast start, soft landing). Exits **ease-in** (accelerate away). UI elements get a **spring with 3-6 % overshoot**. Never linear, except opacity on a dissolve.
**SFX rule:** a whoosh's *peak* goes on the cut frame, not its start. `catalog.json` gives each file's duration; for whooshes the peak is usually 40-60 % in. A hit's *transient* goes on frame 0 of the change.
**HyperFrames:** names in backticks are registry blocks/components (`npx hyperframes add <name>`; see `.claude/skills/hyperframes-registry`).

| # | Transition | Best for | SFX | Length (frames @30) |
|---|---|---|---|---|
| 1 | [Whip pan](#whip-pan) | Location changes in travel reels, gym-to-street, 'meanwhile' cuts | swoosh-fast, whoosh | Outgoing: last 4-6 frames whip; cut at the blur peak; incomi |
| 2 | [Zoom punch (punch-in)](#zoom-punch) | Talking heads (tech tips), punchlines, gym form cues ('KNEES OUT') | hit-impact, bass-drop-boom, pop | Zoom in over 2-3 frames, hold until the next sentence, snap  |
| 3 | [Match cut](#match-cut) | Travel transformations, gym 'day 1 vs day 300', tech setup evolution | whoosh, swoosh-fast | Hard cut (0 frames) |
| 4 | [Mask / object wipe (walk-past wipe)](#object-mask-wipe) | Travel (people/pillars passing), gym (plate or dumbbell passing the lens), tech (laptop lid closing) | whoosh, swoosh-fast | 8-15 frames as the object crosses |
| 5 | [J-cut](#j-cut) | Talking-head tech explainers, travel vlogs: hear the waves before you see the beach | none | Lead the audio 8-20 frames (0 |
| 6 | [L-cut](#l-cut) | B-roll over voice (tech: keep talking over screen recording; gym: coach voice over the set) | none | Hold outgoing audio 10-30 frames into clip B |
| 7 | [Speed ramp (velocity edit)](#speed-ramp) | Gym lifts (fast approach, slow-mo lockout), travel walks and drone shots, gaming clips; the phonk/velocity edit staple | whoosh, riser | Fast section 300-500% for 10-20 frames, ramp down over 6-10  |
| 8 | [Glitch transition](#glitch) | Tech reviews, gaming, 'system error' jokes | glitch | 4-8 frames total (2-4 each side of the cut) |
| 9 | [Flash / white dip](#flash-white) | Photo dumps, beat drops, before/after reveals, camera-shutter moments | camera-shutter, hit-impact | 1-2 frames of full white for a hard flash, or 4-6 frames fad |
| 10 | [Spin / rotation transition](#spin) | Fun travel montages, gaming highlights, outfit/gear changes | whoosh, swoosh-fast | 8-12 frames; cut at max rotational blur (frame 4-6) |
| 11 | [Light leak / lens burn](#light-leak) | Travel, sunset, nostalgic recaps, cinematic intros | whoosh, riser | 12-24 frames; leak peaks on the cut |
| 12 | [Camera shake / impact shake](#camera-shake) | Barbell drop, punchline, bass drop, memes (metal pipe, vine boom) | hit-impact, bass-drop-boom, gym | 4-8 frames, amplitude 8-20 px decaying to 0 (half each frame |
| 13 | [Hand / palm cover transition](#hand-cover) | Outfit/gym changes, before/after, travel 'teleport' | whoosh, pop | Cover over 6-10 frames, cut on the fully dark frame, uncover |
| 14 | [Jump-through / jump cut transition](#jump-through) | Travel destinations, gym outfit reveals, 'POV' trends | whoosh, bass-drop-boom | Cut at the jump apex (body blurred/closest); total motion 10 |
| 15 | [Rack focus](#rack-focus) | Tech product shots (focus from cable to GPU), travel details (flower -> landscape), gym (chalk bowl -> lifter) | whoosh | 15-30 frames for the pull; a cut can hide at the blurriest f |
| 16 | [Split reveal / split screen](#split-reveal) | Before/after (gym progress, desk setup), comparisons (GPU A vs B), travel 'expectation vs reality' | swoosh-fast, whoosh, click-ui | Split opens over 8-12 frames; panels hold; close over 6-8 |
| 17 | [Beat-synced cut](#beat-sync-cut) | Montages: gym day, travel recap, setup tour | none | Cut on the beat frame; at 120 BPM a beat = 15 frames at 30 f |
| 18 | [Smash cut](#smash-cut) | Comedy ('I'll just do one set' -> 3 hours later), expectation vs reality, hook openers | record-scratch, hit-impact | 0 frames |
| 19 | [Freeze frame + label](#freeze-frame) | 'That's me', gear callouts, meme punchlines, form-check pause in gym tutorials | record-scratch, camera-shutter, hit-impact | Hold 20-60 frames; text animates in over 6-8 frames |
| 20 | [Zoom-in / zoom-through transition](#zoom-in-transition) | Travel (zoom into window -> landscape), tech (zoom into screen -> UI), gaming (zoom into monitor -> gameplay) | whoosh, riser | 10-16 frames; cut at max zoom/blur (middle) |
| 21 | [Slide / push](#slide-push) | Lists ('3 things'), carousel-like tech comparisons, story chapters | swoosh-fast, whoosh | 8-12 frames |
| 22 | [Text mask reveal](#text-mask-reveal) | Travel destination titles ('BALI'), chapter cards, gym program names | whoosh, bass-drop-boom | Text in 8 frames, hold 15-30, scale-through 10-15 frames |
| 23 | [VHS rewind](#vhs-rewind) | 'Let's rewind', redo a fail, explain how it started | rewind-tape-stop | 15-45 frames of reversed footage at 3-6x |
| 24 | [Tape stop cut](#tape-stop-cut) | Comedy breaks, 'wait what?' moments, ending a montage | rewind-tape-stop, record-scratch | Slow-down 15-30 frames, then 6-12 frames of silence before t |
| 25 | [Morph cut / jump-cut smoothing](#morph-cut) | Tech talking heads with removed filler words | none | 6-10 frames |
| 26 | [Cross dissolve](#cross-dissolve) | Time passing, calm travel sequences, emotional endings | chime-success | 12-30 frames |
| 27 | [Blur transition](#blur-transition) | Dreamy travel, soft tech product shots, scene changes without energy | whoosh | 8-15 frames |
| 28 | [UI swipe / card swipe (phone screen)](#swipe-up-ui) | Tech/app reviews, 'notes app' storytelling, captions as UI cards | swoosh-fast, click-ui, pop | Slide 6-10 frames with a 2-4 frame overshoot settle |
| 29 | [Number counter / stat roll](#counter-roll) | Gym PR weights, PC benchmark FPS, travel budget totals | click-ui, gaming, chime-success, cash-register | 20-40 frames count, final value holds 30+ frames |
| 30 | [Photo-dump shutter sequence](#photo-dump-shutter) | Travel trips, gym 'month recap', setup builds | camera-shutter | 6-10 frames per photo; 1-frame white flash on entry |
| 31 | [Iris / circle reveal](#iris-circle) | Comedic endings ('That's all folks' feel), gaming, focus on a detail | pop, whoosh | 10-15 frames |
| 32 | [Pixelate transition](#pixelate) | Gaming content, retro/8-bit themes, tech | glitch, gaming | 8-12 frames |

<a id="whip-pan"></a>
## Whip pan

**What:** A very fast pan that smears the frame into motion blur; the cut hides inside the blur and the next clip continues the same direction.

**When:** Location changes in travel reels, gym-to-street, 'meanwhile' cuts. Any niche; best with energetic music.

| | |
|---|---|
| Frames @30 fps | Outgoing: last 4-6 frames whip; cut at the blur peak; incoming: first 4-6 frames still whipping, settling by frame 6-8. Total 8-12 frames. |
| Easing | Exit: ease-in (accelerate into the blur). Entry: ease-out (decelerate out of it). Never linear. |
| SFX timing | Whoosh PEAK on the cut frame (start the file ~0.15-0.3 s before the cut, depending on its peak time in catalog.json). |
| SFX files | **swoosh-fast**: `sfx/swoosh-fast/oga-3-melee-sounds-melee_sound.mp3`, `sfx/swoosh-fast/oga-swishes-sound-pack-swish-9.mp3`, `sfx/swoosh-fast/oga-3-melee-sounds-sword_sound.mp3`; **whoosh**: `sfx/whoosh/inhouse-whoosh_inhouse_big_dark.mp3`, `sfx/whoosh/inhouse-whoosh_inhouse_air_soft.mp3`, `sfx/whoosh/oga-swishes-sound-pack-swish-5.mp3` |
| CapCut | Split at the blur; Transitions > Camera > 'Whip pan' (or 'Pull in'), duration 0.3 s; or keyframe Position + Motion blur on 3 frames each side. |
| Instagram Edits | Instagram Edits: Transitions > 'Whip' / 'Swipe', 0.3 s; match direction to camera move. |
| VN | VN: Transition > 'Slide/Blur' and keyframe position; add Motion blur effect. |
| Filming (tripod/phone) | Phone on gimbal or handheld: end shot A with a fast pan right (wrist flick), start shot B with the same flick right. Shutter 1/60 s at 30 fps for real blur; avoid tripod (locked pans are too slow). |
| ffmpeg | `xfade=transition=hblur:duration=0.3 for a cheap version; real: crop+translate with expression and tmix=frames=5 for blur. e.g. [a][b]xfade=transition=smoothleft:duration=0.25:offset=T` |
| HyperFrames | Registry block `whip-pan` (shader transition); add it with `npx hyperframes add whip-pan`, mount between scenes, 0.3-0.4 s. |

<a id="zoom-punch"></a>
## Zoom punch (punch-in)

**What:** Instant digital zoom 100% -> 115-130% on a beat or a line to add emphasis without changing shot.

**When:** Talking heads (tech tips), punchlines, gym form cues ('KNEES OUT'). The default emphasis tool.

| | |
|---|---|
| Frames @30 fps | Zoom in over 2-3 frames, hold until the next sentence, snap back on a cut (0 frames) or over 4 frames. |
| Easing | Ease-out (fast start, soft land) or a spring with 3-5% overshoot for meme energy. |
| SFX timing | Hit transient on frame 0 of the zoom. |
| SFX files | **hit-impact**: `sfx/hit-impact/oga-thwack-sounds-thwack-07.mp3`, `sfx/hit-impact/oga-thwack-sounds-thwack-03.mp3`, `sfx/hit-impact/oga-75-cc0-breaking-falling-hit--bfh1_hit_08.mp3`; **bass-drop-boom**: `sfx/bass-drop-boom/kenney-sci-fi-lowFrequency_explosion_000.mp3`, `sfx/bass-drop-boom/oga-muffled-distant-explosion-NenadSimic_-_Muffled_Distant_Explosion.mp3`, `sfx/bass-drop-boom/kenney-sci-fi-lowFrequency_explosion_001.mp3`; **pop**: `sfx/pop/oga-pop-sounds-pop4.mp3`, `sfx/pop/oga-pop-sounds-pop8.mp3`, `sfx/pop/oga-pop-effect-sounds-p_2.mp3` |
| CapCut | Select clip > Animation > In > 'Zoom in' 0.1 s, or keyframe Scale 100% -> 120% across 3 frames; Graph: 'Ease out'. |
| Instagram Edits | Edits: Adjust > Zoom keyframes; or 'Zoom' effect in Effects. |
| VN | VN: Keyframe Scale, curve 'Ease Out'. |
| Filming (tripod/phone) | Shoot 4K (or 1080p with the subject centred, extra headroom) so 120-130% crop stays sharp. Tripod, locked off, eye-line at lens. |
| ffmpeg | `zoompan is slow; use scale+crop with an expression: crop=w=iw/Z:h=ih/Z where Z steps 1->1.2 at t0 (e.g. Z='if(gte(t,T0),1.2,1)'), then scale=1080:1920.` |
| HyperFrames | GSAP tween on the scene wrapper: gsap.fromTo(el,{scale:1},{scale:1.2,duration:0.08,ease:'power3.out'}). Component `camera-shake` for the accent. |

<a id="match-cut"></a>
## Match cut

**What:** Cut between two shots that share shape, motion or position (bar on shoulders -> backpack straps; mug -> fan; same hand pose in two cities).

**When:** Travel transformations, gym 'day 1 vs day 300', tech setup evolution. The most 'premium' looking transition.

| | |
|---|---|
| Frames @30 fps | Hard cut (0 frames). Align the matching object to the same pixels (use overlay/opacity 50% to line up). |
| Easing | None (cut). If the object moves, the motion speed must match across the cut. |
| SFX timing | Optional soft whoosh peaking on the cut; often better with no SFX and a music downbeat. |
| SFX files | **whoosh**: `sfx/whoosh/inhouse-whoosh_inhouse_big_dark.mp3`, `sfx/whoosh/inhouse-whoosh_inhouse_air_soft.mp3`, `sfx/whoosh/oga-swishes-sound-pack-swish-5.mp3`; **swoosh-fast**: `sfx/swoosh-fast/oga-3-melee-sounds-melee_sound.mp3`, `sfx/swoosh-fast/oga-swishes-sound-pack-swish-9.mp3`, `sfx/swoosh-fast/oga-3-melee-sounds-sword_sound.mp3` |
| CapCut | Overlay clip B over A at 50% opacity to align, then cut at the matching frame and reset opacity. |
| Instagram Edits | Edits: use 'Overlay' to line up, trim on the beat. |
| VN | VN: PiP at 50% opacity to align, then cut. |
| Filming (tripod/phone) | Tripod and a framing guide: mark subject position on the phone screen (tape/grid). Same lens, same height, same distance. Shoot B right after A or film with the grid overlay on. |
| ffmpeg | `Plain concat at the frame index; check alignment with blend=all_mode=difference.` |
| HyperFrames | Two scene clips back to back with data-start equal to the cut time; no block needed. |

<a id="object-mask-wipe"></a>
## Mask / object wipe (walk-past wipe)

**What:** Something (a person, pole, door, hand, dumbbell) crosses the lens; the next shot is revealed behind its edge.

**When:** Travel (people/pillars passing), gym (plate or dumbbell passing the lens), tech (laptop lid closing).

| | |
|---|---|
| Frames @30 fps | 8-15 frames as the object crosses. Cut at the frame the object fully covers the lens, or mask-track its edge. |
| Easing | Follows real motion; if you animate a mask, use ease-in-out. |
| SFX timing | Whoosh peak at full coverage frame. |
| SFX files | **whoosh**: `sfx/whoosh/inhouse-whoosh_inhouse_big_dark.mp3`, `sfx/whoosh/inhouse-whoosh_inhouse_air_soft.mp3`, `sfx/whoosh/oga-swishes-sound-pack-swish-5.mp3`; **swoosh-fast**: `sfx/swoosh-fast/oga-3-melee-sounds-melee_sound.mp3`, `sfx/swoosh-fast/oga-swishes-sound-pack-swish-9.mp3`, `sfx/swoosh-fast/oga-3-melee-sounds-sword_sound.mp3` |
| CapCut | Overlay clip A over B; Mask > Linear/Split; keyframe the mask edge to follow the object every 2 frames (or use 'Remove background' on A). |
| Instagram Edits | Edits: 'Cutout' on the moving object and layer B under it. |
| VN | VN: Mask (linear) with keyframes on the PiP layer. |
| Filming (tripod/phone) | Locked tripod. Have someone walk close past the lens (or swing a plate/towel across) at the end of A and the start of B, same direction. |
| ffmpeg | `Hard cut at the full-cover frame; for masked edges use alphamerge with a keyframed drawbox/geq mask.` |
| HyperFrames | CSS clip-path inset animation following the object edge; `transitions-cover` gallery has cover/uncover patterns. |

<a id="j-cut"></a>
## J-cut

**What:** Audio of the next clip starts before its picture ('J' shape on the timeline).

**When:** Talking-head tech explainers, travel vlogs: hear the waves before you see the beach. Smooths every hard cut.

| | |
|---|---|
| Frames @30 fps | Lead the audio 8-20 frames (0.27-0.67 s) before the picture cut. |
| Easing | Fade the incoming audio up over 4-6 frames. |
| SFX timing | None; the incoming ambience/voice is the sound. |
| SFX files | none (audio edit itself) |
| CapCut | Detach audio (Extract audio) from clip B, drag its start 10-15 frames earlier under clip A. |
| Instagram Edits | Edits: Detach audio, slide it earlier. |
| VN | VN: Extract audio, move it left. |
| Filming (tripod/phone) | Record 2-3 s of room tone/ambience before every take and after. Use a lav mic so audio is clean enough to lead. |
| ffmpeg | `Delay video vs audio: adelay on clip B's audio is negative -> instead start B's audio earlier with atrim/asetpts, then amix with A's tail; or acrossfade=d=0.4 with B's audio offset.` |
| HyperFrames | Place the audio element's data-start 0.3-0.6 s before the video's data-start. |

<a id="l-cut"></a>
## L-cut

**What:** Audio of the outgoing clip continues over the next clip's picture.

**When:** B-roll over voice (tech: keep talking over screen recording; gym: coach voice over the set).

| | |
|---|---|
| Frames @30 fps | Hold outgoing audio 10-30 frames into clip B. |
| Easing | Fade the trailing audio out over 6-10 frames if it doesn't end on a word. |
| SFX timing | None. |
| SFX files | none (audio edit itself) |
| CapCut | Extract audio from A and extend it past the cut. |
| Instagram Edits | Edits: Detach audio, extend. |
| VN | VN: Extract audio, extend right. |
| Filming (tripod/phone) | Shoot plenty of B-roll matching your script; leave 1 s of silence after lines. |
| ffmpeg | `Use the voice track as a separate input and overlay video segments on top (concat video, single continuous audio).` |
| HyperFrames | Voice audio as one continuous element; video scenes cut under it. |

<a id="speed-ramp"></a>
## Speed ramp (velocity edit)

**What:** Clip speeds up then slows (or vice versa) to land a moment on the beat in slow motion.

**When:** Gym lifts (fast approach, slow-mo lockout), travel walks and drone shots, gaming clips; the phonk/velocity edit staple.

| | |
|---|---|
| Frames @30 fps | Fast section 300-500% for 10-20 frames, ramp down over 6-10 frames to 25-50% for the hero moment, ramp back up over 6 frames. |
| Easing | Bezier speed curve: ease-in into slow-mo, ease-out out of it (CapCut 'Curve > Custom' or 'Montage'). |
| SFX timing | Whoosh peak on the moment speed drops; a sub hit on the first slow-mo frame. |
| SFX files | **whoosh**: `sfx/whoosh/inhouse-whoosh_inhouse_big_dark.mp3`, `sfx/whoosh/inhouse-whoosh_inhouse_air_soft.mp3`, `sfx/whoosh/oga-swishes-sound-pack-swish-5.mp3`; **riser**: `sfx/riser/inhouse-riser_inhouse_tonal_5s.mp3`, `sfx/riser/inhouse-riser_inhouse_noise_4s.mp3`, `sfx/riser/inhouse-riser_inhouse_noise_8s.mp3` |
| CapCut | Speed > Curve > 'Montage'/'Hero time' or Custom with 4 points; enable 'Smooth slow-mo' (optical flow). |
| Instagram Edits | Edits: Speed > Curve presets. |
| VN | VN: Speed > Curve with custom points. |
| Filming (tripod/phone) | Shoot 60 fps (or 120/240 for big slow-mo) at shutter 1/120+; keep the hero moment in the middle of the clip with 2 s before and after. |
| ffmpeg | `Split into segments with trim, setpts=PTS/4 (fast) and setpts=PTS*2 + minterpolate=fps=30 (slow), concat. Example: [0:v]trim=0:2,setpts=(PTS-STARTPTS)/4[a];[0:v]trim=2:3,setpts=(PTS-STARTPTS)*2[b];[a][b]concat=n=2:v=1` |
| HyperFrames | Pre-render the ramp with ffmpeg (HyperFrames plays footage at fixed rate), then mount the clip. |

<a id="glitch"></a>
## Glitch transition

**What:** RGB split, block displacement and stutter for a few frames at the cut.

**When:** Tech reviews, gaming, 'system error' jokes. Avoid in calm travel content.

| | |
|---|---|
| Frames @30 fps | 4-8 frames total (2-4 each side of the cut). Stutter: repeat 1-2 frames twice. |
| Easing | None (stepped/random) - that's the point. |
| SFX timing | Glitch sound spans the effect; the loudest burst on the cut frame. |
| SFX files | **glitch**: `sfx/glitch/inhouse-glitch_inhouse_stutter.mp3`, `sfx/glitch/inhouse-glitch_inhouse_data.mp3`, `sfx/glitch/inhouse-glitch_inhouse_zap.mp3` |
| CapCut | Transitions > Glitch > 'Glitch' or 'Signal'; or Effects > Basic > 'Glitch' 0.2 s across the cut. |
| Instagram Edits | Edits: Effects > 'Glitch'. |
| VN | VN: Effects > Glitch / RGB. |
| Filming (tripod/phone) | Nothing special; works best when both shots have contrast and edges. |
| ffmpeg | `Over the cut frames: rgbashift=rh=-12:bh=12, noise=alls=40:allf=t, and a stutter via select/loop; e.g. enable='between(t,T-0.07,T+0.07)' on rgbashift.` |
| HyperFrames | Registry block `glitch` (shader transition) or `chromatic-radial-split`; `transitions-distortion` gallery. |

<a id="flash-white"></a>
## Flash / white dip

**What:** Frame flashes to white (or a brightness spike) for 1-4 frames at the cut.

**When:** Photo dumps, beat drops, before/after reveals, camera-shutter moments.

| | |
|---|---|
| Frames @30 fps | 1-2 frames of full white for a hard flash, or 4-6 frames fading 100%->0 for a dip. |
| Easing | Exit of flash: ease-out (fast fade). Don't hold white more than 2 frames (photosensitivity, and it looks cheap). |
| SFX timing | Shutter or hit exactly on the white frame. |
| SFX files | **camera-shutter**: `sfx/camera-shutter/oga-camera-photo.mp3`, `sfx/camera-shutter/inhouse-shutter_inhouse_mech_a.mp3`, `sfx/camera-shutter/inhouse-shutter_inhouse_mech_b.mp3`; **hit-impact**: `sfx/hit-impact/oga-thwack-sounds-thwack-07.mp3`, `sfx/hit-impact/oga-thwack-sounds-thwack-03.mp3`, `sfx/hit-impact/oga-75-cc0-breaking-falling-hit--bfh1_hit_08.mp3` |
| CapCut | Transitions > Basic > 'Flash' 0.1-0.2 s, or insert a white Background clip of 2 frames. |
| Instagram Edits | Edits: Transitions > 'Flash'. |
| VN | VN: Transition 'Flash white'. |
| Filming (tripod/phone) | Nothing special; works best on high-contrast cuts. |
| ffmpeg | `xfade=transition=fadewhite:duration=0.13:offset=T or eq=brightness=0.6:enable='between(t,T,T+0.066)'.` |
| HyperFrames | Block `flash-through-white` or overlay `editorial-flash-overlay`. Use sparingly (the registry itself warns it is rarely a good neutral default). |

<a id="spin"></a>
## Spin / rotation transition

**What:** The frame rotates 90-360 degrees with blur into the next clip.

**When:** Fun travel montages, gaming highlights, outfit/gear changes. Overuse = 2016 vibe.

| | |
|---|---|
| Frames @30 fps | 8-12 frames; cut at max rotational blur (frame 4-6). |
| Easing | Ease-in out of A, ease-out into B; add motion blur. |
| SFX timing | Whoosh peak at the cut. |
| SFX files | **whoosh**: `sfx/whoosh/inhouse-whoosh_inhouse_big_dark.mp3`, `sfx/whoosh/inhouse-whoosh_inhouse_air_soft.mp3`, `sfx/whoosh/oga-swishes-sound-pack-swish-5.mp3`; **swoosh-fast**: `sfx/swoosh-fast/oga-3-melee-sounds-melee_sound.mp3`, `sfx/swoosh-fast/oga-swishes-sound-pack-swish-9.mp3`, `sfx/swoosh-fast/oga-3-melee-sounds-sword_sound.mp3` |
| CapCut | Transitions > Camera > 'Spin' / 'Rotate', 0.3 s; add Motion blur. |
| Instagram Edits | Edits: Transitions > 'Spin'. |
| VN | VN: Transition 'Rotate', or keyframe Rotation. |
| Filming (tripod/phone) | Rotate the phone (roll) at the end of A and start of B in the same direction, gimbal off. |
| ffmpeg | `rotate='if(lt(t,T),0,PI*2*min((t-T)/0.3,1))':ow=iw:oh=ih with tmix for blur; or xfade=transition=radial.` |
| HyperFrames | GSAP rotation tween on the scene container with filter:blur; `transitions-3d` gallery. |

<a id="light-leak"></a>
## Light leak / lens burn

**What:** Warm orange light flare washes over the cut, film style.

**When:** Travel, sunset, nostalgic recaps, cinematic intros. Not for tech tutorials.

| | |
|---|---|
| Frames @30 fps | 12-24 frames; leak peaks on the cut. |
| Easing | Ease-in-out opacity (sine). |
| SFX timing | Soft whoosh or reverse swell peaking on the cut. |
| SFX files | **whoosh**: `sfx/whoosh/inhouse-whoosh_inhouse_big_dark.mp3`, `sfx/whoosh/inhouse-whoosh_inhouse_air_soft.mp3`, `sfx/whoosh/oga-swishes-sound-pack-swish-5.mp3`; **riser**: `sfx/riser/inhouse-riser_inhouse_tonal_5s.mp3`, `sfx/riser/inhouse-riser_inhouse_noise_4s.mp3`, `sfx/riser/inhouse-riser_inhouse_noise_8s.mp3` |
| CapCut | Transitions > Light > 'Light leak' / Effects > 'Lens flare', 0.5-0.8 s. Or overlay a light-leak clip with blend 'Screen'. |
| Instagram Edits | Edits: Effects > 'Light leak'. |
| VN | VN: Overlay a light-leak video in 'Screen' blend. |
| Filming (tripod/phone) | Shoot real leaks: point the phone near the sun/lamp and pan slowly; save as overlays. |
| ffmpeg | `Overlay a leak clip with blend=all_mode=screen, or a gradient: geq to make an orange radial and fade it with fade=in/out.` |
| HyperFrames | Registry block `light-leak` (shader) or `transitions-light` gallery. |

<a id="camera-shake"></a>
## Camera shake / impact shake

**What:** Frame jitters for a few frames to sell an impact.

**When:** Barbell drop, punchline, bass drop, memes (metal pipe, vine boom).

| | |
|---|---|
| Frames @30 fps | 4-8 frames, amplitude 8-20 px decaying to 0 (half each frame). |
| Easing | Decaying (exponential) amplitude, random direction each frame. |
| SFX timing | Shake starts on the transient frame. |
| SFX files | **hit-impact**: `sfx/hit-impact/oga-thwack-sounds-thwack-07.mp3`, `sfx/hit-impact/oga-thwack-sounds-thwack-03.mp3`, `sfx/hit-impact/oga-75-cc0-breaking-falling-hit--bfh1_hit_08.mp3`; **bass-drop-boom**: `sfx/bass-drop-boom/kenney-sci-fi-lowFrequency_explosion_000.mp3`, `sfx/bass-drop-boom/oga-muffled-distant-explosion-NenadSimic_-_Muffled_Distant_Explosion.mp3`, `sfx/bass-drop-boom/kenney-sci-fi-lowFrequency_explosion_001.mp3`; **gym**: `sfx/gym/oga-75-cc0-breaking-falling-hit--bfh1_metal_falling_01.mp3`, `sfx/gym/oga-75-cc0-breaking-falling-hit--bfh1_metal_falling_02.mp3`, `sfx/gym/oga-75-cc0-breaking-falling-hit--bfh1_metal_falling_03.mp3` |
| CapCut | Effects > Basic > 'Shake' 0.2 s, or keyframe Position (+12,-8,+6,-3,0). |
| Instagram Edits | Edits: Effects > 'Shake'. |
| VN | VN: Effects > 'Shake'. |
| Filming (tripod/phone) | Shoot slightly wider so the shake doesn't show edges (or scale clip to 105%). |
| ffmpeg | `crop=iw-40:ih-40:x='20+15*sin(t*90)*exp(-(t-T)*12)*gte(t,T)':y='20+12*cos(t*77)*exp(-(t-T)*12)*gte(t,T)', then scale back.` |
| HyperFrames | Component `camera-shake` (camera moves). |

<a id="hand-cover"></a>
## Hand / palm cover transition

**What:** Hand (or object) moves over the lens to cover it; next clip starts with the hand moving away.

**When:** Outfit/gym changes, before/after, travel 'teleport'. Classic TikTok transition.

| | |
|---|---|
| Frames @30 fps | Cover over 6-10 frames, cut on the fully dark frame, uncover over 6-10 frames. |
| Easing | Natural motion; cut at the darkest frame. |
| SFX timing | Whoosh peak on the dark frame (or a pop when the new shot appears). |
| SFX files | **whoosh**: `sfx/whoosh/inhouse-whoosh_inhouse_big_dark.mp3`, `sfx/whoosh/inhouse-whoosh_inhouse_air_soft.mp3`, `sfx/whoosh/oga-swishes-sound-pack-swish-5.mp3`; **pop**: `sfx/pop/oga-pop-sounds-pop4.mp3`, `sfx/pop/oga-pop-sounds-pop8.mp3`, `sfx/pop/oga-pop-effect-sounds-p_2.mp3` |
| CapCut | Cut on the darkest frame; optionally add 'Blur' transition 0.1 s to hide differences. |
| Instagram Edits | Edits: trim on the darkest frame. |
| VN | VN: trim at the darkest frame. |
| Filming (tripod/phone) | Tripod, locked. End A: palm to the lens. Start B: palm on lens, then pull away. Keep the same hand and direction. |
| ffmpeg | `Cut at the darkest frame: find with signalstats YAVG minimum, then concat.` |
| HyperFrames | Plain cut between scenes at the computed frame. |

<a id="jump-through"></a>
## Jump-through / jump cut transition

**What:** You jump (or step) toward the camera and land in a new place/outfit.

**When:** Travel destinations, gym outfit reveals, 'POV' trends.

| | |
|---|---|
| Frames @30 fps | Cut at the jump apex (body blurred/closest); total motion 10-16 frames. |
| Easing | Follows real motion; add a 2-frame zoom punch on landing. |
| SFX timing | Whoosh rising into the apex; boom on landing frame. |
| SFX files | **whoosh**: `sfx/whoosh/inhouse-whoosh_inhouse_big_dark.mp3`, `sfx/whoosh/inhouse-whoosh_inhouse_air_soft.mp3`, `sfx/whoosh/oga-swishes-sound-pack-swish-5.mp3`; **bass-drop-boom**: `sfx/bass-drop-boom/kenney-sci-fi-lowFrequency_explosion_000.mp3`, `sfx/bass-drop-boom/oga-muffled-distant-explosion-NenadSimic_-_Muffled_Distant_Explosion.mp3`, `sfx/bass-drop-boom/kenney-sci-fi-lowFrequency_explosion_001.mp3` |
| CapCut | Cut at apex; add 'Pull in' transition 0.2 s. |
| Instagram Edits | Edits: Transitions > 'Zoom'. |
| VN | VN: cut at apex, 'Zoom' transition. |
| Filming (tripod/phone) | Same framing in both places (tripod height marked). Jump the same way both times; shoot 60 fps. |
| ffmpeg | `Concat at apex frame; add zoom punch on landing (see zoom-punch).` |
| HyperFrames | Cut + `cinematic-zoom` block for the blur. |

<a id="rack-focus"></a>
## Rack focus

**What:** Focus shifts from foreground to background (or vice versa) to redirect attention; can also hide a cut in the blur.

**When:** Tech product shots (focus from cable to GPU), travel details (flower -> landscape), gym (chalk bowl -> lifter).

| | |
|---|---|
| Frames @30 fps | 15-30 frames for the pull; a cut can hide at the blurriest frame. |
| Easing | Ease-in-out (sine). |
| SFX timing | Very soft air whoosh, peak at the blurriest frame, or no SFX. |
| SFX files | **whoosh**: `sfx/whoosh/inhouse-whoosh_inhouse_big_dark.mp3`, `sfx/whoosh/inhouse-whoosh_inhouse_air_soft.mp3`, `sfx/whoosh/oga-swishes-sound-pack-swish-5.mp3` |
| CapCut | Real rack focus is in camera; fake: keyframe 'Blur' effect 0->40->0 across the cut. |
| Instagram Edits | Edits: Effects > 'Blur' keyframes. |
| VN | VN: Blur keyframes. |
| Filming (tripod/phone) | iPhone Cinematic mode (tap to change focus) or Blackmagic Cam/manual focus app; tripod; foreground subject 20-40 cm from lens. |
| ffmpeg | `gblur=sigma='...'(no per-frame expression); use boxblur with enable segments, or split/overlay with xfade=transition=hblur.` |
| HyperFrames | CSS filter: blur() tween on the scene, `transitions-blur` gallery, component `blur-in`. |

<a id="split-reveal"></a>
## Split reveal / split screen

**What:** Frame splits (vertical/horizontal/diagonal) to reveal the next shot, or shows two shots side by side.

**When:** Before/after (gym progress, desk setup), comparisons (GPU A vs B), travel 'expectation vs reality'.

| | |
|---|---|
| Frames @30 fps | Split opens over 8-12 frames; panels hold; close over 6-8. |
| Easing | Ease-out on open with a 3% spring overshoot; ease-in on close. |
| SFX timing | Swoosh peak as panels reach position; click when each panel locks. |
| SFX files | **swoosh-fast**: `sfx/swoosh-fast/oga-3-melee-sounds-melee_sound.mp3`, `sfx/swoosh-fast/oga-swishes-sound-pack-swish-9.mp3`, `sfx/swoosh-fast/oga-3-melee-sounds-sword_sound.mp3`; **whoosh**: `sfx/whoosh/inhouse-whoosh_inhouse_big_dark.mp3`, `sfx/whoosh/inhouse-whoosh_inhouse_air_soft.mp3`, `sfx/whoosh/oga-swishes-sound-pack-swish-5.mp3`; **click-ui**: `sfx/click-ui/oga-10-clicks-and-switches-click.9.mp3`, `sfx/click-ui/oga-button-click-sound-effect-cc-qubodup-click2.mp3`, `sfx/click-ui/kenney-interface-tick_001.mp3` |
| CapCut | Overlay + Mask > Split/Linear; keyframe mask position. Or Template 'Split screen'. |
| Instagram Edits | Edits: Layout > split. |
| VN | VN: PiP + crop keyframes. |
| Filming (tripod/phone) | Same framing for both halves (tripod position marked), subject on one side of frame. |
| ffmpeg | `hstack/vstack for side-by-side; xfade=transition=vertopen / horzopen / diagtl for a reveal.` |
| HyperFrames | Component `before-after-wipe`; `transitions-push` gallery. |

<a id="beat-sync-cut"></a>
## Beat-synced cut

**What:** Cuts land exactly on beats (kick/snare) of the music.

**When:** Montages: gym day, travel recap, setup tour. The backbone of most reels.

| | |
|---|---|
| Frames @30 fps | Cut on the beat frame; at 120 BPM a beat = 15 frames at 30 fps, 140 BPM = 12.86 frames (alternate 13/13/13/12). |
| Easing | N/A (cuts). Move cuts 1 frame EARLY so the picture change reads with the transient (perception lag). |
| SFX timing | The music is the SFX; add an accent hit only on the drop. |
| SFX files | none (audio edit itself) |
| CapCut | Audio > Beat > Auto generate (or tap beats manually), clips snap to beat markers. |
| Instagram Edits | Edits: 'Beat sync' / auto-cut to music. |
| VN | VN: Music > Beat markers > Snap. |
| Filming (tripod/phone) | Shoot 2-3x more clips than beats; short actions that complete within 1-2 beats. |
| ffmpeg | `Get beat times (earshot timeline gives a beat grid, or aubio/librosa), then trim segments to those frame indexes and concat.` |
| HyperFrames | `npx hyperframes beats --json` gives hit times; set scene data-start to beat times; block `beat-freeze-cut`. |

<a id="smash-cut"></a>
## Smash cut

**What:** Abrupt cut from a loud/calm moment to the opposite with no transition, often to silence.

**When:** Comedy ('I'll just do one set' -> 3 hours later), expectation vs reality, hook openers.

| | |
|---|---|
| Frames @30 fps | 0 frames. Cut audio and picture on the same frame; silence 6-15 frames is powerful. |
| Easing | None. |
| SFX timing | Optional record scratch ending on the cut, or kill all audio. |
| SFX files | **record-scratch**: `sfx/record-scratch/inhouse-scratch_inhouse_baby.mp3`, `sfx/record-scratch/oga-scratch-vocal-sound-scroutch.mp3`, `sfx/record-scratch/inhouse-scratch_inhouse_baby_fast.mp3`; **hit-impact**: `sfx/hit-impact/oga-thwack-sounds-thwack-07.mp3`, `sfx/hit-impact/oga-thwack-sounds-thwack-03.mp3`, `sfx/hit-impact/oga-75-cc0-breaking-falling-hit--bfh1_hit_08.mp3` |
| CapCut | Split, delete; no transition. Cut music at the same frame. |
| Instagram Edits | Edits: Split. |
| VN | VN: Split. |
| Filming (tripod/phone) | Plan the contrast shot (quiet, static, deadpan face). |
| ffmpeg | `concat; ensure audio is cut at the same frame (afade=t=out:d=0.01 to avoid clicks).` |
| HyperFrames | Plain cut; audio element ends at the cut time. |

<a id="freeze-frame"></a>
## Freeze frame + label

**What:** Picture freezes for emphasis or to introduce a person/object with text.

**When:** 'That's me', gear callouts, meme punchlines, form-check pause in gym tutorials.

| | |
|---|---|
| Frames @30 fps | Hold 20-60 frames; text animates in over 6-8 frames. |
| Easing | Text: ease-out with spring overshoot (UI feel). |
| SFX timing | Scratch/shutter/hit on the freeze frame. |
| SFX files | **record-scratch**: `sfx/record-scratch/inhouse-scratch_inhouse_baby.mp3`, `sfx/record-scratch/oga-scratch-vocal-sound-scroutch.mp3`, `sfx/record-scratch/inhouse-scratch_inhouse_baby_fast.mp3`; **camera-shutter**: `sfx/camera-shutter/oga-camera-photo.mp3`, `sfx/camera-shutter/inhouse-shutter_inhouse_mech_a.mp3`, `sfx/camera-shutter/inhouse-shutter_inhouse_mech_b.mp3`; **hit-impact**: `sfx/hit-impact/oga-thwack-sounds-thwack-07.mp3`, `sfx/hit-impact/oga-thwack-sounds-thwack-03.mp3`, `sfx/hit-impact/oga-75-cc0-breaking-falling-hit--bfh1_hit_08.mp3` |
| CapCut | Edit > Freeze (creates a 3 s still), trim to length. |
| Instagram Edits | Edits: Freeze frame. |
| VN | VN: Freeze frame. |
| Filming (tripod/phone) | Make sure the freeze frame is sharp: shoot at 1/120+ shutter for moving subjects. |
| ffmpeg | `tpad=stop_mode=clone:stop_duration=1 on the segment, or loop=loop=30:size=1:start=N.` |
| HyperFrames | Block `beat-freeze-cut`; or a still image scene. |

<a id="zoom-in-transition"></a>
## Zoom-in / zoom-through transition

**What:** Zoom deep into a point of shot A (with blur) and emerge zoomed into shot B.

**When:** Travel (zoom into window -> landscape), tech (zoom into screen -> UI), gaming (zoom into monitor -> gameplay).

| | |
|---|---|
| Frames @30 fps | 10-16 frames; cut at max zoom/blur (middle). |
| Easing | Ease-in into the zoom, ease-out out of it. |
| SFX timing | Whoosh/riser peak on the cut. |
| SFX files | **whoosh**: `sfx/whoosh/inhouse-whoosh_inhouse_big_dark.mp3`, `sfx/whoosh/inhouse-whoosh_inhouse_air_soft.mp3`, `sfx/whoosh/oga-swishes-sound-pack-swish-5.mp3`; **riser**: `sfx/riser/inhouse-riser_inhouse_tonal_5s.mp3`, `sfx/riser/inhouse-riser_inhouse_noise_4s.mp3`, `sfx/riser/inhouse-riser_inhouse_noise_8s.mp3` |
| CapCut | Transitions > Camera > 'Pull in' / 'Zoom in' 0.3-0.5 s. |
| Instagram Edits | Edits: Transitions > 'Zoom'. |
| VN | VN: Transition 'Zoom'. |
| Filming (tripod/phone) | Frame a target point (screen, window, door) centred in A; start B centred on related content. |
| ffmpeg | `xfade=transition=zoomin:duration=0.4:offset=T (ffmpeg 6.1 has zoomin).` |
| HyperFrames | Block `cinematic-zoom`; component `parallax-zoom`. |

<a id="slide-push"></a>
## Slide / push

**What:** Shot B pushes shot A out of frame (left/right/up).

**When:** Lists ('3 things'), carousel-like tech comparisons, story chapters.

| | |
|---|---|
| Frames @30 fps | 8-12 frames. |
| Easing | Ease-in-out (cubic) or ease-out for a snappy UI feel. |
| SFX timing | Swoosh peak at mid-push. |
| SFX files | **swoosh-fast**: `sfx/swoosh-fast/oga-3-melee-sounds-melee_sound.mp3`, `sfx/swoosh-fast/oga-swishes-sound-pack-swish-9.mp3`, `sfx/swoosh-fast/oga-3-melee-sounds-sword_sound.mp3`; **whoosh**: `sfx/whoosh/inhouse-whoosh_inhouse_big_dark.mp3`, `sfx/whoosh/inhouse-whoosh_inhouse_air_soft.mp3`, `sfx/whoosh/oga-swishes-sound-pack-swish-5.mp3` |
| CapCut | Transitions > Slide > 'Push left'. |
| Instagram Edits | Edits: Transitions > 'Slide'. |
| VN | VN: Transition 'Push'. |
| Filming (tripod/phone) | Nothing special. |
| ffmpeg | `xfade=transition=slideleft (or smoothleft):duration=0.3:offset=T.` |
| HyperFrames | `transitions-push` gallery (CSS/GSAP). |

<a id="text-mask-reveal"></a>
## Text mask reveal

**What:** Big text acts as a window into the next shot, then scales up to fill the frame.

**When:** Travel destination titles ('BALI'), chapter cards, gym program names.

| | |
|---|---|
| Frames @30 fps | Text in 8 frames, hold 15-30, scale-through 10-15 frames. |
| Easing | Scale-through: ease-in (exponential) to feel like flying in. |
| SFX timing | Riser/whoosh into the scale-through, boom when the frame is fully open. |
| SFX files | **whoosh**: `sfx/whoosh/inhouse-whoosh_inhouse_big_dark.mp3`, `sfx/whoosh/inhouse-whoosh_inhouse_air_soft.mp3`, `sfx/whoosh/oga-swishes-sound-pack-swish-5.mp3`; **bass-drop-boom**: `sfx/bass-drop-boom/kenney-sci-fi-lowFrequency_explosion_000.mp3`, `sfx/bass-drop-boom/oga-muffled-distant-explosion-NenadSimic_-_Muffled_Distant_Explosion.mp3`, `sfx/bass-drop-boom/kenney-sci-fi-lowFrequency_explosion_001.mp3` |
| CapCut | Text > add text > use as Mask? CapCut: overlay video, Mask > 'Text' shape (or a text template 'video in text'), keyframe scale. |
| Instagram Edits | Edits: text with video fill template. |
| VN | VN: Text mask (Pro). |
| Filming (tripod/phone) | Shot B should be wide and bright so it reads through letters. |
| ffmpeg | `Render text as alpha with drawtext on a black canvas, alphamerge with clip B, scale with expression, overlay on A.` |
| HyperFrames | HTML text with background-clip:text over video, GSAP scale; kinetic type blocks in the registry. |

<a id="vhs-rewind"></a>
## VHS rewind

**What:** Footage plays backwards fast with scanlines and tracking noise to 'go back in time'.

**When:** 'Let's rewind', redo a fail, explain how it started.

| | |
|---|---|
| Frames @30 fps | 15-45 frames of reversed footage at 3-6x. |
| Easing | Speed ramps up over the first 6 frames. |
| SFX timing | Rewind sound spans it; a tape-stop/click at the end. |
| SFX files | **rewind-tape-stop**: `sfx/rewind-tape-stop/inhouse-tapestop_inhouse_hit.mp3`, `sfx/rewind-tape-stop/inhouse-tapestop_inhouse_sax.mp3`, `sfx/rewind-tape-stop/inhouse-rewind_inhouse_vhs.mp3` |
| CapCut | Reverse the clip, speed 4x, Effects > Retro > 'VHS'. |
| Instagram Edits | Edits: Reverse + speed + 'VHS' effect. |
| VN | VN: Reverse, Speed, VHS filter. |
| Filming (tripod/phone) | Normal footage; reversal works best on motion (walking, lifting). |
| ffmpeg | `reverse,setpts=PTS/4 on a trimmed segment, plus noise=alls=20:allf=t, eq=saturation=0.7, and a drawbox scanline overlay.` |
| HyperFrames | `transitions-other` (VHS) gallery; pre-reverse footage with ffmpeg. |

<a id="tape-stop-cut"></a>
## Tape stop cut

**What:** Music slows to a halt as the picture freezes or cuts to a contrasting scene.

**When:** Comedy breaks, 'wait what?' moments, ending a montage.

| | |
|---|---|
| Frames @30 fps | Slow-down 15-30 frames, then 6-12 frames of silence before the next beat. |
| Easing | Pitch/speed falls with ease-in (slow first, then drops). |
| SFX timing | Tape-stop starts 0.5-1 s before the freeze; ends on the freeze frame. |
| SFX files | **rewind-tape-stop**: `sfx/rewind-tape-stop/inhouse-tapestop_inhouse_hit.mp3`, `sfx/rewind-tape-stop/inhouse-tapestop_inhouse_sax.mp3`, `sfx/rewind-tape-stop/inhouse-rewind_inhouse_vhs.mp3`; **record-scratch**: `sfx/record-scratch/inhouse-scratch_inhouse_baby.mp3`, `sfx/record-scratch/oga-scratch-vocal-sound-scroutch.mp3`, `sfx/record-scratch/inhouse-scratch_inhouse_baby_fast.mp3` |
| CapCut | Use the library tape-stop file under a cut music track; or Audio > Speed curve on music. |
| Instagram Edits | Edits: audio speed ramp (if available) or library SFX. |
| VN | VN: audio speed keyframes. |
| Filming (tripod/phone) | Nothing special. |
| ffmpeg | `Library file overlapped with afade on the music; DIY: asetrate ramp isn't keyframeable - use the in-house synth.py tape stop (varispeed).` |
| HyperFrames | Place the tape-stop audio, kill the music element at the same time. |

<a id="morph-cut"></a>
## Morph cut / jump-cut smoothing

**What:** Smooths a jump cut in a talking head so the speaker seems continuous.

**When:** Tech talking heads with removed filler words.

| | |
|---|---|
| Frames @30 fps | 6-10 frames. |
| Easing | N/A (optical flow). |
| SFX timing | None. |
| SFX files | none (audio edit itself) |
| CapCut | CapCut desktop: Transitions > 'Morph' / 'Smooth' (or use zoom-punch alternation instead). |
| Instagram Edits | Edits: alternate 100%/115% zoom per cut instead. |
| VN | VN: none - alternate zoom levels. |
| Filming (tripod/phone) | Tripod, consistent position; keep hands still between sentences. |
| ffmpeg | `minterpolate across a short xfade; often better: alternate scale 100%/110% on every other jump cut.` |
| HyperFrames | Alternate scene scale between cuts. |

<a id="cross-dissolve"></a>
## Cross dissolve

**What:** Gradual blend between shots.

**When:** Time passing, calm travel sequences, emotional endings. Rare in fast reels.

| | |
|---|---|
| Frames @30 fps | 12-30 frames. |
| Easing | Linear opacity is acceptable; ease-in-out looks smoother. |
| SFX timing | Optional soft chime/ambience swell. |
| SFX files | **chime-success**: `sfx/chime-success/uisfx-glass-achievement.mp3`, `sfx/chime-success/uisfx-glass-success.mp3`, `sfx/chime-success/uisfx-studio-complete.mp3` |
| CapCut | Transitions > Basic > 'Mix', 0.5-1 s. |
| Instagram Edits | Edits: 'Dissolve'. |
| VN | VN: 'Dissolve'. |
| Filming (tripod/phone) | Nothing special; static shots dissolve best. |
| ffmpeg | `xfade=transition=fade:duration=0.6:offset=T; audio acrossfade=d=0.6.` |
| HyperFrames | `transitions-dissolve` gallery. |

<a id="blur-transition"></a>
## Blur transition

**What:** Shot A blurs out while B blurs in.

**When:** Dreamy travel, soft tech product shots, scene changes without energy.

| | |
|---|---|
| Frames @30 fps | 8-15 frames. |
| Easing | Ease-in-out. |
| SFX timing | Soft whoosh peak on the cut. |
| SFX files | **whoosh**: `sfx/whoosh/inhouse-whoosh_inhouse_big_dark.mp3`, `sfx/whoosh/inhouse-whoosh_inhouse_air_soft.mp3`, `sfx/whoosh/oga-swishes-sound-pack-swish-5.mp3` |
| CapCut | Transitions > Blur > 'Blur'. |
| Instagram Edits | Edits: 'Blur'. |
| VN | VN: 'Blur'. |
| Filming (tripod/phone) | Nothing special. |
| ffmpeg | `xfade=transition=hblur:duration=0.35:offset=T (or 'fadeblack' + boxblur).` |
| HyperFrames | `transitions-blur` gallery; component `blur-in`. |

<a id="swipe-up-ui"></a>
## UI swipe / card swipe (phone screen)

**What:** New scene slides up like a phone screen/app card with a spring.

**When:** Tech/app reviews, 'notes app' storytelling, captions as UI cards.

| | |
|---|---|
| Frames @30 fps | Slide 6-10 frames with a 2-4 frame overshoot settle. |
| Easing | Spring (overshoot 3-6%), as in iOS. |
| SFX timing | Click on touch frame, light swoosh during slide, pop on settle. |
| SFX files | **swoosh-fast**: `sfx/swoosh-fast/oga-3-melee-sounds-melee_sound.mp3`, `sfx/swoosh-fast/oga-swishes-sound-pack-swish-9.mp3`, `sfx/swoosh-fast/oga-3-melee-sounds-sword_sound.mp3`; **click-ui**: `sfx/click-ui/oga-10-clicks-and-switches-click.9.mp3`, `sfx/click-ui/oga-button-click-sound-effect-cc-qubodup-click2.mp3`, `sfx/click-ui/kenney-interface-tick_001.mp3`; **pop**: `sfx/pop/oga-pop-sounds-pop4.mp3`, `sfx/pop/oga-pop-sounds-pop8.mp3`, `sfx/pop/oga-pop-effect-sounds-p_2.mp3` |
| CapCut | Animation > In > 'Slide up' + keyframe overshoot; or Templates. |
| Instagram Edits | Edits: Animation 'Slide up'. |
| VN | VN: Keyframe position with overshoot. |
| Filming (tripod/phone) | Screen recordings at 60 fps; record your finger taps with a second camera if showing hands. |
| ffmpeg | `overlay with y expression: y='H-(H)*min(1,(t-T)/0.25)' (add overshoot with a damped sine).` |
| HyperFrames | GSAP with ease:'back.out(1.6)'; registry UI cards (`browser-device-stage`). |

<a id="counter-roll"></a>
## Number counter / stat roll

**What:** Numbers count up (weight, price, FPS) with ticks, landing on the final value.

**When:** Gym PR weights, PC benchmark FPS, travel budget totals.

| | |
|---|---|
| Frames @30 fps | 20-40 frames count, final value holds 30+ frames. |
| Easing | Ease-out (fast start, slow finish) so the final digits are readable. |
| SFX timing | Tick every 2-3 frames during count (slowing), chime/cash on the final value frame. |
| SFX files | **click-ui**: `sfx/click-ui/oga-10-clicks-and-switches-click.9.mp3`, `sfx/click-ui/oga-button-click-sound-effect-cc-qubodup-click2.mp3`, `sfx/click-ui/kenney-interface-tick_001.mp3`; **gaming**: `sfx/gaming/oga-50-cc0-retro-synth-sfx-power_up_01.mp3`, `sfx/gaming/oga-50-cc0-retro-synth-sfx-power_up_04.mp3`, `sfx/gaming/oga-10-8bit-coin-sounds-coin2.mp3`; **chime-success**: `sfx/chime-success/uisfx-glass-achievement.mp3`, `sfx/chime-success/uisfx-glass-success.mp3`, `sfx/chime-success/uisfx-studio-complete.mp3`; **cash-register**: `sfx/cash-register/inhouse-register_inhouse_chaching.mp3`, `sfx/cash-register/oga-purchasing-sound-effect-snd_purchase_0.mp3`, `sfx/cash-register/oga-80-cc0-rpg-sfx-item_coins_04.mp3` |
| CapCut | Text templates 'counter'; or keyframe multiple text layers. |
| Instagram Edits | Edits: text templates. |
| VN | VN: text keyframes. |
| Filming (tripod/phone) | Film the real display (bar, scale, FPS overlay) in focus as proof. |
| ffmpeg | `drawtext with text='%{eif\:min(225\,225*(t-T)/1)\:d}' style expression.` |
| HyperFrames | GSAP number tween (textContent snap), data-chart blocks. |

<a id="photo-dump-shutter"></a>
## Photo-dump shutter sequence

**What:** Rapid stills, each with a white flash and shutter, often on the beat.

**When:** Travel trips, gym 'month recap', setup builds.

| | |
|---|---|
| Frames @30 fps | 6-10 frames per photo; 1-frame white flash on entry. |
| Easing | Optional 102%->100% scale settle (ease-out) per photo. |
| SFX timing | Shutter on each photo's first frame. |
| SFX files | **camera-shutter**: `sfx/camera-shutter/oga-camera-photo.mp3`, `sfx/camera-shutter/inhouse-shutter_inhouse_mech_a.mp3`, `sfx/camera-shutter/inhouse-shutter_inhouse_mech_b.mp3` |
| CapCut | Import photos, 0.3 s each, Beat sync; Transition 'Flash' 0.1 s. |
| Instagram Edits | Edits: Photo template; 'Flash'. |
| VN | VN: photos 0.3 s + flash. |
| Filming (tripod/phone) | Shoot burst/Live Photos during the day. |
| ffmpeg | `Image concat demuxer with duration 0.3, then eq brightness flash on each boundary.` |
| HyperFrames | Image scenes with data-start on beats; `editorial-flash-overlay`. |

<a id="iris-circle"></a>
## Iris / circle reveal

**What:** Circle opens from (or closes to) a point, cartoon style.

**When:** Comedic endings ('That's all folks' feel), gaming, focus on a detail.

| | |
|---|---|
| Frames @30 fps | 10-15 frames. |
| Easing | Ease-in for close, ease-out for open. |
| SFX timing | Pop on full close; whoosh on open. |
| SFX files | **pop**: `sfx/pop/oga-pop-sounds-pop4.mp3`, `sfx/pop/oga-pop-sounds-pop8.mp3`, `sfx/pop/oga-pop-effect-sounds-p_2.mp3`; **whoosh**: `sfx/whoosh/inhouse-whoosh_inhouse_big_dark.mp3`, `sfx/whoosh/inhouse-whoosh_inhouse_air_soft.mp3`, `sfx/whoosh/oga-swishes-sound-pack-swish-5.mp3` |
| CapCut | Transitions > 'Circle' / Mask > Circle keyframes. |
| Instagram Edits | Edits: Mask circle. |
| VN | VN: Mask circle. |
| Filming (tripod/phone) | Leave the subject's face where the iris will close. |
| ffmpeg | `xfade=transition=circleclose / circleopen:duration=0.4:offset=T.` |
| HyperFrames | Block `sdf-iris`; `transitions-radial` gallery. |

<a id="pixelate"></a>
## Pixelate transition

**What:** Picture breaks into big pixels and resolves into the next clip.

**When:** Gaming content, retro/8-bit themes, tech.

| | |
|---|---|
| Frames @30 fps | 8-12 frames. |
| Easing | Stepped (pixel size halves each 2 frames). |
| SFX timing | 8-bit blip or glitch across the effect. |
| SFX files | **glitch**: `sfx/glitch/inhouse-glitch_inhouse_stutter.mp3`, `sfx/glitch/inhouse-glitch_inhouse_data.mp3`, `sfx/glitch/inhouse-glitch_inhouse_zap.mp3`; **gaming**: `sfx/gaming/oga-50-cc0-retro-synth-sfx-power_up_01.mp3`, `sfx/gaming/oga-50-cc0-retro-synth-sfx-power_up_04.mp3`, `sfx/gaming/oga-10-8bit-coin-sounds-coin2.mp3` |
| CapCut | Transitions > Glitch > 'Pixelate'/'Mosaic'. |
| Instagram Edits | Edits: 'Pixelate'. |
| VN | VN: 'Mosaic'. |
| Filming (tripod/phone) | Nothing special. |
| ffmpeg | `xfade=transition=pixelize:duration=0.35:offset=T.` |
| HyperFrames | Component `grid-pixelate-wipe`. |
