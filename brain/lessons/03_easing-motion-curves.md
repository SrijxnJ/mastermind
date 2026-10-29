# Lesson 03: Easing. Why animations look robotic, and the 3-rule fix

- **Source:** Srijan upload `Video-50003.mp4` (48.6 s, 720×1280). The end screen promotes the "Ugoki" motion course ("DM me UGOKI").
- **Studied:** 27 Oct 2026. Transcribed locally with faster-whisper; frames checked by eye.
- **Genre:** motion-design tutorial, faceless, all motion graphics

## The lesson (transcript, lightly trimmed)
> "Does your animation look robotic? The problem is its speed. Nothing in the real world moves at a constant speed.
> Look at its trail: every step is the same. It starts all at once, and it stops all at once.
> For everything that comes in: **ease out**. It arrives fast, then brakes for a long time, as if set down by a steady hand.
> For everything that leaves, the opposite: **ease in**. It starts slowly, then it gets away.
> And for the interface: **a spring**. It overshoots its target just a little, then settles back.
> Tell Claude in exactly these words, and your animation jumps to a whole new level."

**The exact prompt shown on screen (the reusable part):**
```
Entrances: ease out.
Exits: ease in.
Interface: spring, slight overshoot.
Nothing linear.
```

## How the video is made
| Area | What they do |
|---|---|
| Hook (0–2 s) | Question about a pain point ("Does your animation look robotic?") + a side-by-side: ROBOT vs PRO slider animation |
| Visual proof | Position-vs-time graphs with a dotted "trail": evenly spaced dots = linear; bunched dots = eased. The idea becomes something you can see |
| Captions | One word at a time, white bold sans; the key word sits in a **red highlight box** ("speed.", "out.", "brakes") |
| Palette | Near-black with a red glow, red as the only accent colour |
| Pacing | A new caption word every ~0.3–0.5 s; the graph animates continuously, with no cuts |
| CTA | Locked card "The full method → inside the Ugoki course", then "DM me UGOKI" typed into a DM box |

## What this means for us *(our take)*
- **Our own edits break this rule.** In the Khandala reel, the photo pans and push-ins in my ffmpeg build move at constant speed (linear). Fix: ease every pan/zoom (ease-out on entry moves, ease-in on exits). Edits/CapCut/VN keyframes have ease curves; in ffmpeg, use an eased expression instead of `t/d`.
- The rep-counter "pop" in the incline reel was already a fast-in, settle shape (close to a spring). Keep that.
- Word-by-word captions with one highlighted key word are a caption style we can reuse.

## Takeaways (added to the Brain)
- [Effects/Transitions] Entrances ease out · exits ease in · UI/text pops = spring with slight overshoot · **nothing linear**.
- [Editing] Paste the 4-line easing prompt whenever an AI builds motion graphics.
- [Text & fonts] Word-by-word captions with the key word in a coloured highlight box.
- [Content & hooks] "Robot vs Pro" side-by-side as the hook proof.
