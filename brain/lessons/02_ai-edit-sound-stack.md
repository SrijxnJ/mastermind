# Lesson 02: Sound for AI-made edits (Openverse, Real SFX, earshot)

- **Source:** https://www.instagram.com/p/De9yxpuIG6X/ (42 s)
- **Studied:** 27 Oct 2026, with an AI scene breakdown (vidIQ). Every tool below was checked on its own website or repo on the same day.
- **Genre:** tech / creator-tools explainer, talking head + motion graphics

## The lesson
**The problem it names:** "Why do your Claude edits look pro but sound like a silent movie?" An AI editing agent can't *hear*, so it skips sound or fakes it with synthetic beeps.

**The fix: a three-part sound stack**
1. **Source library: Openverse.** A free library of millions of openly licensed sounds that can be searched with no API key.
2. **Placement: Real SFX (Claude Code skill).** Finds every moment in an edit that needs a sound and places a real recording on that exact frame. Honest limit: it ships only 78 UI sounds, which is why you pair it with a library.
3. **Ears: earshot (open source).** Lets the agent listen: it scores an edit against pro launch films and generates its own whooshes in code.

## Verified facts (checked 27 Oct 2026)
| Tool | What it really is | Cost / licence | Notes |
|---|---|---|---|
| **Openverse** (`api.openverse.org`) | Search API over CC-licensed audio (mostly from Freesound) | Free, no key needed. Each sound has its own licence | Our test search for "whoosh" returned 240 results, e.g. "Deep Whoosh #1" (CC0). **Use CC0 for Instagram.** CC-BY sounds need credit in the caption |
| **Real SFX** (clipwing.pro/skills/real-sfx; source github.com/Clipwing/skills) | Claude Code skill: detects moments, places real SFX from *your* sound folder, ducks them under voice, outputs MP4 + SFX WAV + report | Free; its 78 bundled UI sounds are CC0 | Needs Python 3.9+ and ffmpeg (we have both) |
| **earshot** (github.com/Leonxlnx/earshot) | CPU audio-analysis CLI + MCP server + 2 Claude skills (`earshot`, `real-sound`) | MIT code; models Apache-2.0 / BSD-3. About 3.0k stars | Downloads about 1.1 GB of models on first run; Python 3.10+. Commands include `critique` (launch-film scorecard), `timeline` (second-by-second listening log), `forge` (make whooshes in code), `sfx` (252-sound bank). Optional Gemini upload only with explicit flags and a key |

## How the video itself is made
| Area | What they do |
|---|---|
| Hook (0–3 s) | Pain question plus contrast text: "Looks pro. Sounds like this: 🔇" |
| Structure | Problem, then 3 numbered tools (1/3, 2/3, 3/3 badges), then summary card, then CTA. 42 s total |
| Pacing | A visual change every 1.5–2.5 s: badges, slide-in cards, number counters |
| Text | Serif italic for emphasis words (*pro*, *honest*) + clean sans for body, with yellow/orange keyword highlights |
| Effects | Animated number counters (5,220,123 sounds; GitHub stars ticking up), frosted UI cards, spring/bounce slide-ins |
| Sound | Pop / click / whoosh / snap on **every** visual change |
| Trust move | "The honest part: it only ships 78 sounds." Admitting a limit makes the rest believable |
| CTA | "Comment SOUND and I'll send you all three links" + animated comment badge |

## What this means for us *(our take)*
- This is exactly the gap in **our** pipeline. I edit Srijan's reels with ffmpeg and can measure audio (loudness, levels) but can't judge how it sounds. Our Khandala and incline edits went out **silent**, with music added later in Edits.
- With Openverse (CC0 only) + Real SFX-style placement + earshot critique, I could add **pops on text, whooshes on cuts, and a thud on the final lockout** myself, then have earshot check the mix and sync before Srijan adds the song.
- The **number counter** effect (counting up to "75 KG") and **"1/3, 2/3, 3/3" badges** are effects we can reuse for gym and travel list content.
- The **"honest part"** line is a strong scripting move for Srijan's comeback content ("not heavy for everyone").

## Takeaways (added to the Brain)
- [Sound] An edit without SFX feels like a "silent movie": put a sound on every visual event.
- [Sound] Free sound source: Openverse, filtered to CC0 for Instagram.
- [Effects] Number counters and n/3 progress badges hold attention in list videos.
- [Content & hooks] Contrast hook: "Looks X. Sounds/feels like Y."
- [Content & hooks] State an honest limitation to build trust.
- [Text & fonts] Serif italic for emphasis + sans for body (same pairing as our Khandala reel).
