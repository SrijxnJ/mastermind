# Lesson 10: Storyboard first, then let Claude edit (a pause-and-play teardown)

- **Source:** https://www.instagram.com/p/DfAMeazmN77/ (84.9 s, 720×1280, 30 fps)
- **Creator:** Chanyoung Ryu "Chandler" (@chandlerintelligence). He breaks down **another creator's reel** (a man in an A's cap and patterned cardigan, not named on screen). Chandler says that creator sells the workflow for $97.
- **Stats at download (27 Oct 2026, about 4 h after posting at 15:37 UTC):** 53 likes, **63 comments** (more comments than likes; all 15 comments yt-dlp returned are just "Edit"). Views not exposed. Posted 27 Oct 2026.
- **Caption (summary):** "Giving away EVERY WORKFLOW in this vid (for free). Comment "EDIT" and I'll send it to you, with the exact styling I used." It restates the storyboard step, Whisper timing, the person cutout + Remotion, the FFmpeg grades, and "For transitions I skipped the recursive zoom and went with a whip pan. It looks cleaner." Tags: #claude #claudecode #aivideoediting #videoediting #remotion.
- **Studied:** 27 Oct 2026. Method: yt-dlp download + `-j` metadata; faster-whisper `small` word-level transcript (351 words); 85 frames at 1 fps + scene-change frames (ffmpeg `select=gt(scene,0.08)`: 41 events) read as contact sheets, plus full-res crops of the storyboard, prompt bars and grade panel; frame strips around each transition; ffmpeg `ebur128` / `volumedetect` / `silencedetect` / `signalstats`; earshot `timeline` (normal detail). No vidIQ.
- **Genre:** tech / AI-editing tutorial, talking head at a desk + overlays.

## The lesson

### 1. The format: a "pause-and-play breakdown" of a paid creator's reel
Chandler's own planning doc names the format: **"Format: Pause-and-play breakdown"** (doc "Chandler Intelligence / 020 · Claude Edited This", status "In edit"). The other creator's reel plays **with its own audio** in a rounded card top-right. When it reaches an effect, Chandler freezes it, shrinks it to a thumbnail beside his head, and says how to make that effect with Claude. Then the source plays again.
- The source plays 10 times, **19.9 s of the 84.9 s (23%)**. Its lines carry the story: "No CapCut, no Edits app." [0:12] · "One sentence and the whole video is edited. Watch." [0:22] · "And I know nothing about video editing." [0:36].
- **The hook is borrowed, then undercut.** The source's strongest line plays first: "I didn't edit a single second of this video. Claude did." [0:00–0:02]. Chandler then says: **"This guy's selling this for 97 bucks. I'm giving it away for free."** [0:03–0:05] (a $97 checkout card pops on the source card at about 0:04).

### 2. The key step: storyboard before anything is edited (or shot)
The source creator's line sets it up: "My [workflow] is a little different because before rendering, it gives me a complete storyboard, so I can see what Claude is thinking before it creates my video." [1:08–1:14]. *(Whisper heard "my rate"; the word is unclear.)*

Chandler: **"Okay, so this part is critical. Before Claude edits anything, have it write a storyboard, so that you both agree on what the video looks like first. I always do this before I shoot."** [1:14–1:22]

Two storyboards are shown on screen:
| Whose | Columns / fields (read from frames) | Example row |
|---|---|---|
| **Chandler's** (Notion-style doc, white card overlay, 1:17–1:22) | `#` · `Freeze` (the second where he pauses the source) · `Chandler says` · `On screen` | 1 · 2.4 · "For the text behind your head, tell Claude to cut you out with a person segmentation model…" · "Checkerboard, words behind head". Rows continue: 4.8 Whisper repo card · 8.0 prompt bar types · 11.4 "Warm on, slider takes it off" · 15.3 magazine prompt · 16.9 real timeline · 22.6 zoom prompt, punch-in · 25.0 grade panel · 28.7 yt-dlp repo card |
| **The source creator's** (dark green terminal-style card "claude-editing / storyboard · v2 · 24 beats", 1:12–1:14) | beat number · in/out timecode · duration · shot ("Talking head, wide") · the spoken line in serif italic · a direction bullet · **EMPHASIS** · **GOLD** · **SCORE** | 01 · 0:00.0–0:02.8 · 2.8 s · "I didn't edit a single second of this video. Claude did." · "Hook over the first shot from frame 0" · EMPHASIS: "Claude did (gold serif), CapCut (struck through)" · GOLD: "second" · SCORE: **"drop 1 on 'Claude did.'"**; another beat: "tape stop under the scratch 0:28.3 · drop 2 on 'storyboard'" |

The caption describes the table: "every line I say, what's on screen, and which tool makes it. I fix the plan, then Claude builds the edit from it."

### 3. The recipes, effect by effect (his words)
| [time] | Effect in the source | How Chandler says to make it |
|---|---|---|
| [0:06–0:12] | Text behind your head | "Tell Claude to cut you out with a person's segmentation model, then put the words behind you using Remotion." (He shows a checkerboard cut-out of himself, then "Chandler Intelligence" behind his head.) |
| [0:14–0:21] | Word-timed captions | "Use Whisper to get the timing of every word and Remotion to put them on screen. **I'd lose the green box though. Plain text with shadow looks way cleaner.**" |
| [0:24–0:26] | Prompt-bar UI ("make it more aesthetic") | "Ask Claude to draw these for you as vector graphics." |
| [0:26–0:31] | "The whole thing warms up" + before/after slider | "FFmpeg for the color change and Remotion again for the slider effect." |
| [0:31–0:36] | Magazine-cover title ("CLAUDE" masthead behind the head) | "I don't know what the heck this is supposed to be, but here's how you create it." The prompt types on: "Make this a magazine cover: CLAUDE masthead behind my head, cover…" |
| [0:37–0:42] | Editor-timeline graphic | **"You could create a mock-up of your editor timeline, but a real screenshot would look much better."** (He shows a mock-up, then a real NLE timeline screenshot.) |
| [0:43–0:49] | Recursive zoom | **"These zooms are a bit too much in my opinion, but give this prompt to Claude and it'll create it for you."** Prompt: "On the word "this", shrink the shot into a picture of itself, 3 levels deep, then push through it with a spin and blur." |
| [0:48–0:58] | "Make it moody and the colors go dark" | "Personally, I'd go with something like this… This is just FFmpeg again. **Curves to pull the highlights down and lift the blacks. Saturation down 15%. Then a soft vignette.**" On-screen grade panel: Highlights −35, Blacks +12, Saturation −15, Vignette −40 |
| [0:59–1:08] | 3×3 wall of reels | Prompt: "Shrink my shot into the centre tile of a 3x3 grid, then pop 8 of these reels in around it, one per frame." Plus "YouTube DLP [yt-dlp] to download the reels. It's a free tool that grabs videos from Instagram, TikTok, YouTube, pretty much anywhere." |
| caption | Transitions | "I skipped the recursive zoom and went with a whip pan. It looks cleaner." |

**CTA:** "Comment edit for everything I explain in this video." [1:22–1:24], with "EDIT" as large outlined letters **behind his head** (the same cut-out effect, reused for the CTA keyword).

## Production (editing, sound, animation, captions)
| Area | Measured / observed |
|---|---|
| Length & pace | 84.9 s. Chandler speaks 250 words in about 65 s (**~231 wpm**, fast); the source's 101 words fill the other 19.9 s |
| Visual changes | 41 scene-change events (threshold 0.08) = **one every ~2.1 s**. Only 6 are full-frame hard changes at threshold 0.25 (9.3, 12.0, 33.3, 36.3, 62.5, 82.2 s); the rest are overlays entering, leaving or resizing |
| Camera layer | One locked-off desk camera (laptop in the foreground, warm practical lamp, dark office). About 8 framing changes across the reel: wide, a tighter punch-in, a second angle with a podcast mic in frame (from ~58.8 s), a tight closing shot (82.2 s). Camera shots average roughly 10 s; the overlays carry the pace |
| Layout | Him centred, lower 60%. The source reel sits in a **rounded-corner card**: top-right at about half the width while it plays, shrunk to a small thumbnail (~13% of the width) beside his head while he talks. Info cards (GitHub repo card, FFmpeg logo card, prompt bar, grade panel, storyboard doc) sit top-centre above his head |
| Hook text (0–2.5 s only) | "HOW TO **ACTUALLY** EDIT VIDEOS / USING CLAUDE": condensed bold uppercase (Bebas/Oswald-like), white on black boxes, "ACTUALLY" in lime green |
| Captions | White bold sans (SF Pro/Inter-like), **soft drop shadow, no box**, 1–3 words, centred at ~61% height (just above the laptop edge). A coral box highlights "every word" once [0:16], while he talks about word timing. This matches his "lose the green box" advice |
| Text behind head | "Text behind your head" (light geometric sans, white), "Chandler Intelligence" (two-tone: olive-yellow + white), CTA "EDIT" (huge, outlined, low-opacity grey). Each sits behind his cut-out silhouette |
| Prompt bars | Dark rounded bar, white sans, **typewriter type-on**, orange square send arrow (Claude-app look). 5 prompts shown in full |
| Proof cards | GitHub cards (openai/whisper, yt-dlp/yt-dlp with star/fork counts) appear **on the word**; FFmpeg logo card on "FFmpeg"; grade panel whose slider numbers change as he says each step (Highlights −35 → Blacks +12 → Saturation −15 → Vignette −40). At 56 s, his own footage's measured saturation drops from ~8 to ~4.5 (SATAVG): **each effect is applied to him while he names it** |
| 3×3 wall | His shot shrinks into the centre tile (about 0.25 s, 61.0–61.3 s) and the reels pop in; the grid then stays as the thumbnail |
| Transitions | **Whip/blur cut** at 49.6–49.8 s (about 5 frames of horizontal motion blur into a new framing, whoosh + hit at 49.75/49.85 s). The source card itself blurs at 24.3–24.5 s. No recursive zoom used on his own footage |
| Grade | Low-key moody: mean luma 63–72 / 255 (about 25–28%), very low saturation (SATAVG ~7–9), warm tungsten practicals, blacks not crushed (YMIN 7–12). The grade he recommends is the one he wears |
| Audio level | Integrated **−14.1 LUFS**, loudness range **2.3 LU** (heavily compressed). No silence ≥0.25 s below −40 dB except one deliberate dropout |
| Music | Continuous bed under the voice: earshot tags funk with vocal chops at 0–12 s and 72–85 s (drum-heavier), a lighter "corporate" bed in the middle (tags are weak hints). In voice gaps the bed measures about −23 to −26 dB mean vs −16.8 dB for the whole mix, so it sits **~7–10 dB under the voice** |
| SFX moments | **0.5 s near-silence (−42 LUFS) at 2.50 s, right after "Claude did."** (the source storyboard's "drop 1 on 'Claude did.'"). Pops: 5.87 ($97 card / "free"), 13.92, 22.14, 39.86 (timeline mock-up), 61.44 (3×3 wall), 76.94 (storyboard doc). Hit: 42.12 (real screenshot). Whooshes: 37.76, 49.75 (whip), 68.82 (source card expands). About 10 SFX across 41 visual events: **not** one per event. Some of these may be inside the source reel's audio |
| Voice | Close mic, dry, compressed. The source's audio plays at full level when its card is big |
| CTA | Spoken + "EDIT" behind the head; caption repeats "Comment "EDIT"" |

## Tools, repos and skills named
| Tool | What it does here | Licence / status | Brain status |
|---|---|---|---|
| **Remotion** (remotion.dev, github.com/remotion-dev/remotion) | React-based code-to-video: places captions, words behind the head, the slider reveal, prompt bars, the magazine cover, the 3×3 wall | **Remotion License** (source-available, not OSI open source): free for individuals, for-profit companies with up to 3 employees and non-profits, even for commercial videos; larger companies need a paid company licence (checked on its LICENSE.md, 27 Oct 2026) | **New: PARKED candidate.** Overlaps HyperFrames (P11, Apache-2.0, skills already stored). Not installed |
| **Person segmentation model** (not named in the reel) | Cuts him out of each frame so text can sit behind him | Depends on the model: e.g. MediaPipe selfie segmentation (Apache-2.0) or rembg (MIT) | **New: PARKED candidate.** Not installed |
| Whisper | Word timings for captions, labels and repo cards | MIT | Have it (faster-whisper, P8) |
| FFmpeg | Warm look, moody grade (curves, saturation, vignette) | LGPL/GPL | Have it |
| yt-dlp | Downloads the reels for the 3×3 wall | Unlicense | Have it (P9) |
| Notion-style doc | Holds his storyboard table | n/a | Process idea, not a tool |

## Unique vs already in the Brain
| New in L10 | Already in the Brain (overlap) |
|---|---|
| **Storyboard-first**: Claude writes the full beat table (line / on screen / tool / freeze time) and you approve it before any edit, and even before shooting | L08 "scripting & storyboarding" is named only as one of six pillars, with no method; L04 reference-driven editing; L09 many rewrites |
| **SCORE + EMPHASIS columns in the storyboard**: music drops, tape stops and gold-word emphasis planned per beat | L07 music changes by section (but not planned per line) |
| **Pause-and-play teardown** of another creator's reel as a format | L04 / R1 reference-driven study (for us, not as content) |
| **Undercut hook**: play the rival's best line, then "he sells this for $97, I'm giving it away free" | L05 "give the real thing"; L04 "that's why they sell courses"; L02 price-strike effects (R1) |
| **Text behind your head** (segmentation cut-out) for titles, brand name and the CTA keyword | L06 frame low with headroom for graphics |
| **Plain white captions with a soft shadow, no box** ("way cleaner") | L03/R1 word-by-word with a highlight box; L04 caption bar (clash, see C29) |
| **Apply each effect to yourself while you name it** (proof by demonstration) | L07/R1 proof inserts |
| **Real screenshot > AI mock-up** for UI and timeline graphics | R1/L07 "show proof on screen" |
| **Moody grade recipe**: highlights −35, blacks +12 (lifted), saturation −15%, soft vignette; animated grade panel | KH Khandala ffmpeg grade; SP gym grade (cool, contrasty); L07 deep blacks (clash, see C32) |
| **Whip pan over recursive zoom** (the Brain's Transitions section is still empty) | trends.json lists "swipe/whip" as a gap |
| **Tool card on the exact word** (repo / logo card timed by Whisper) | L02 GitHub star counters; L04 repo table |
| **0.5 s music dropout right after the punchline**, then the beat returns | L07 riser + sub-boom at chapter edges |
| Prompt bar typed on screen as a graphic; ask Claude to draw UI as **vector graphics** | L04 prompt shown as a step |
| Data point: 63 comments vs 53 likes after ~4 h with a comment-keyword CTA | L01/L02 comment CTA (C1) |

## Possible clashes (not resolved)
- **C29 (new): Caption style.** L10: "I'd lose the green box though. Plain text with shadow looks way cleaner." vs cheat sheet: word-by-word captions with the key word in a coloured highlight box (L03, R1) and L04's uppercase caption bar. *(He still uses one coral box once.)*
- **C30 (new): Plan every line vs just start.** L10: storyboard the whole video and agree on it before editing, "I always do this before I shoot." vs L06 "the key to the yap is you just do it" + ReCut unscripted pauses, and L08 Briar "say something crazy and get into it". Related to C13/C21 (polish vs speed).
- **C31 (new): Breaking down someone else's reel.** L10 plays another creator's reel with its audio for 23% of the runtime and builds the post around it. vs the Brain's originality rule (atom `growth-originality`, SP: no near-duplicates/reposts) and research notes that YouTube (1 Oct rule) and Instagram down-rank low-effort reuse of others' clips. *(Commentary with demos on your own footage may count as transformative. Not decided.)*
- **C32 (new): Grade blacks.** L10's moody grade **lifts** the blacks and cuts saturation 15% (soft, filmic) vs L07 "high contrast, deep blacks, neon accents" and SP gym grade "higher contrast". *(Possibly genre-specific: moody desk/tech vs gym. Not decided.)*
- **Extends C1 / C11 (teaser vs give all):** "I'm giving it away for free" and the reel does explain every step, yet "Comment EDIT… with the exact styling I used" holds back the exact styling for the DM. Evidence for the comment side of C1: 63 comments vs 53 likes, all visible comments are "Edit".
- **Extends C8 / C22 (AI's role):** "I didn't edit a single second of this video. Claude did." is the strongest "AI does the whole edit" claim in the Brain, but both creators keep human taste calls (storyboard approval, "too much", "looks cleaner").

## Takeaways (added to the Brain)
- [Process] Storyboard first: before Claude edits (or before you shoot), have it write the whole video as a table (# / time / what I say / on screen / which tool / sound cue), fix the plan, then build from it. [L10]
- [Sound] Put the music in the storyboard: a SCORE line per beat ("drop on 'Claude did.'", "tape stop under the scratch") and an EMPHASIS line (which word goes gold or gets struck through). [L10]
- [Sound] A ~0.5 s music dropout right after the hook punchline, then the beat comes back. [L10]
- [Content & hooks] Pause-and-play breakdown: play a popular (or paid) reel in a card, freeze at each effect, explain how to make it, then play on. [L10]
- [Content & hooks] Undercut hook: play the rival's best line, then "He's selling this for $97. I'm giving it away for free." [L10]
- [Effects] Text behind your head: a person-segmentation cut-out with the text layer between background and you; reuse it for the CTA keyword. [L10]
- [Effects] Prove each technique by applying it to your own shot as you name it (grade sliders move, your saturation drops, you shrink into the 3×3 grid). [L10]
- [Text & fonts] Captions as plain white bold sans with a soft shadow and no box, 1–3 words, just above the lower third (clashes with highlight boxes, C29). [L10]
- [Text & fonts] Show the real prompt typing into a chat-style bar; tool/repo cards appear on the exact word (Whisper timing). A real screenshot beats an AI mock-up. [L10]
- [Colour] Moody grade: curves pull highlights down (−35), lift blacks (+12), saturation −15%, soft vignette (−40); reveal a look with a before/after slider. [L10]
- [Transitions] Whip pan (about 5 frames of motion blur + whoosh/hit) instead of a recursive picture-in-picture zoom, which "is a bit too much". [L10]
