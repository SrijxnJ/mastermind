# Lesson 04: The "1-prompt edit with Claude" workflow

- **Source:** Srijan upload `Video-60622.mp4` (85 s, 720×1280). Talking head on top, red whiteboard-style step board below.
- **Studied:** 27 Oct 2026. Transcribed locally with faster-whisper; the tools table was read from frames.
- **Genre:** creator-tools tutorial

## The workflow (as the creator describes it)
1. Install Claude Code; open the **Code** tab, choose **Local**, open a new folder (his is called "my boss editor").
2. **Copy these GitHub repositories** (shown as a table):

| Tool | Role in the workflow (his words) | Repo |
|---|---|---|
| FFmpeg | Every cut, crop, mix, mute and render | github.com/FFmpeg/FFmpeg |
| faster-whisper | Word-level transcription, which every cut is placed against | github.com/SYSTRAN/faster-whisper |
| Whisper | OpenAI's speech model; faster-whisper is a faster runtime for it | github.com/openai/whisper |
| yt-dlp | Downloading the YouTube source | github.com/yt-dlp/yt-dlp |
| OpenCV (+ contrib) | Following whoever is talking in the vertical crop (the CSRT tracker is in contrib) | github.com/opencv/opencv (+ opencv_contrib) |
| Puppeteer | Drives headless Chrome to render the HTML captions and titles to video, and took the GitHub screenshots | github.com/puppeteer/puppeteer |
| HyperFrames (HeyGen) | Agent-built motion graphics from HTML | github.com/heygen-com/hyperframes |

3. **Prompt:** "You are my short form editor. Here are all the GitHub links to help you do your job."
4. **Find an edit you like** and send the link: "I like the style of this reel. Can we duplicate this style and use it for a video of mine?"
5. **Shoot your video**, then give Claude the file path ("here's my video"). It edits it in the reference's style, with no timeline editor involved.
6. **Review & voice to edit:** give feedback in plain words.
7. **Bonus: turn it into a skill:** "Hey, turn this into a skill." Next time it's one prompt.

Closing line: "I know it is a lot, but that's also probably why they're selling their courses."

## How the video is made
| Area | What they do |
|---|---|
| Hook | "You've probably seen these videos lately where people are editing with Claude or ChatGPT. Let me show you how." Plus a trust line: **"No DM for resources, everything you need is right here."** It's an anti-CTA that stands out against everyone else's comment-to-DM CTA |
| Layout | Top: talking head with headphones (home office); bottom: a **red board** with handwritten-style numbered steps that zoom/pan to each step and screenshot |
| Captions | Uppercase bold white caption bar between the two halves, 3–4 words at a time |
| Save bait | "I'll leave it here for a second so you can take a picture" = a screenshot/save moment |
| Ending | Pulls back to the whole board (the full map in one frame), which drives saves |

## Comparison with what we already do *(our take)*
We already run most of this stack in our sessions: FFmpeg ✅, OpenCV ✅, Python ✅, Claude Code skills ✅. New from this lesson:
- **faster-whisper** gives word-level timestamps, which means real word-by-word captions and cutting on words. Now installed.
- **yt-dlp** downloads reference videos (YouTube reliably; Instagram is often blocked). Now installed.
- **OpenCV CSRT tracker** automatically follows a person in a 9:16 crop, e.g. when reframing a landscape gym clip. Now installed.
- **HyperFrames** makes agent-built motion graphics from HTML (captions, counters, list cards). Its skills are stored; running its CLI was blocked by the safety check (see PARKED).
- **The big idea:** "turn this into a skill." Once Srijan's editing style is stable, package it as our own reusable skill (parked).

## Takeaways (added to the Brain)
- [Growth] Anti-CTA "no DM needed, it's all here" builds trust and saves; the comment-keyword CTA builds comments. *(Clash with L01/L02 → see CLASHES.md)*
- [Editing] Reference-driven editing: send the reel whose style you want, then your raw footage.
- [Content & hooks] "You've probably seen X lately… let me show you how": a trend-riding hook.
- [Text & fonts] Uppercase caption bar between split-screen halves.
- [Growth] Screenshot moment ("take a picture") + full-map ending = save bait.
