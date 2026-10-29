---
name: mastermind
description: The creator's social-media Master Mind. Use whenever the user wants to ideate, plan, script, edit or critique a reel, Short, YouTube video, carousel or story, asks "what does the Brain say", wants options/routes/mockups for a style choice (captions, fonts, sound effects, transitions, grade, hook, CTA, pace), or wants to ingest a new lesson, run the trend researcher, or rebuild the map and wiki.
---

# Master Mind

The Brain lives in this repository. The creator's persona and rules are in `SYSTEM_PROMPT.md`; operating rules in `CLAUDE.md`.

## What's in it
| Layer | File |
|---|---|
| Ideas (atoms, one technique each, with sources and neural links) | `brain/data/atoms.json` + `brain/data/atoms_<id>.json` |
| Approaches: every style choice as a menu of options (good at / weak at / looks like / best for) | `brain/data/approaches.json` |
| Courses (long-form videos turned into chaptered learning material) | `brain/learn/*.json` |
| Lessons (raw notes per source) | `brain/lessons/*.md`, `brain/creators/*.md` |
| Idea lanes (per niche: ideas, storyboards, steps, needs) | `brain/ideas/<lane>.json` |
| Trends, viral studies and gaps (researcher) | `brain/research/` |
| Sounds, memes, transitions, LUTs, mixing | `library/` |
| Wiki (generated) | `wiki/index.md`, `wiki/approaches/`, `wiki/pathways/<format>.md`, `wiki/niches/` |
| Map (generated) | `mastermind/index.html` |

## Search before you answer
```bash
.venv/bin/python mastermind/query.py "<what you need>" -k 12
# --kind approach   → only style options;  --kind atom → only ideas;  --kind trend → only trends
```
Run 2–4 queries with different wording. Read `wiki/pathways/<format>.md` for the format in play and `wiki/approaches/<dimension>.md` for each style choice that matters.

## Ideating (routes, not verdicts)
Clashes are not problems to resolve. They are options. When ideating:
1. Name the format (reel30 / reel60 / reel90 / yt-short / yt-long / carousel / story) and niche.
2. Pick the 2–4 approach dimensions that matter most for this piece (hook type, caption style, SFX style, grade...).
3. Lay out routes: **Route A** (option X + option Y): what the reel looks like second by second, what it is good at, what it is weak at. Then **Route B**, and so on. Cite approaches as `[A:dimension/option]` and ideas as `[atom-id]`.
4. Don't pick for the creator unless asked; say which goal each route serves (reach, saves, shares, comments, trust, speed).
5. Offer a mockup: render the routes with HyperFrames (`.claude/skills/hyperframes`) or ffmpeg on the creator's own footage. Use real sounds from `library/` (CC0), never synthesized beeps.
6. Respect the face-check rule in `SYSTEM_PROMPT.md`.

## Adding knowledge
- New source → `brain/lessons/NN_slug.md` (lesson first, then production table), atoms in `brain/data/atoms_<id>.json`, new options folded into `approaches.json` (add a dimension or an option; never delete one), a line in `wiki/log.md`.
- Long-form video → a course in `brain/learn/` following `brain/learn/SCHEMA.md`.
- Rebuild after any change: `.venv/bin/python mastermind/build.py`.
