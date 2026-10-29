# How this wiki works

This is an LLM-maintained wiki (the "LLM Wiki" pattern): raw sources stay untouched, an LLM distils them into one structured knowledge layer, and every readable page is generated from that layer. Nothing here is a plan for Srijan's content; it records what the sources teach and show.

## Layers
| Layer | Where | Who edits it |
|---|---|---|
| Raw sources | `brain/lessons/*.md`, `brain/creators/*.md`, `brain/research/reports/*.md`, `library/**` | Written once per source by an ingest; kept as evidence |
| Knowledge layer | `brain/data/atoms.json` (+ `brain/data/atoms_<id>.json` for later lessons) | The LLM, during ingest |
| Generated pages | `wiki/topics`, `wiki/pathways`, `wiki/niches`, `wiki/sources`, `wiki/clashes.md`, `wiki/index.md` | `mastermind/build.py` only. Never hand-edit |
| Map | `mastermind/index.html` (published as the Master Mind artifact) | `mastermind/build.py` only |

## The atom
One idea = one atom: `id`, `title` (≤8 words), `text`, `how`, `topic`, `stage`, `formats`, `niches`, `sources`, `clashes`, `evidence` (stated / observed / our-take / claim), `quote`.
- **Merge, don't duplicate.** If a new source repeats an existing idea, add its id to that atom's `sources`.
- **Disagreements become clashes** (`brain/CLASHES.md` and the `clashes` list), never silent overwrites.
- **Formats:** reel30 (≤30 s), reel60 (31–60 s), reel90 (60 s–3 min), yt-short, yt-long, carousel, story, podcast.
- **Stages** order every pathway: idea → script → film → edit → sound → graphics → publish → analyse → monetise → mindset.

## Neural links
`build.py` embeds every atom with a small sentence-embedding network (BAAI/bge-small-en-v1.5 via fastembed, on CPU) and wires each atom to its closest neighbours. Trends, memes and transitions are wired to their nearest atoms the same way. These links are the "Related" lines on every page and the synapses on the map.

## Operations
- **Ingest** a new source: write `brain/lessons/NN_slug.md` (lesson first, then production notes), add its atoms to `brain/data/atoms_<id>.json`, add clashes, append to `log.md`, then rebuild.
- **Research:** the researcher follows `brain/research/RESEARCHER.md` and updates `brain/research/trends.json`; rebuild afterwards.
- **Rebuild:** `.venv/bin/python mastermind/build.py` (needs `pip install fastembed numpy` in that venv; `tools/setup_audio_tools.sh` sets it up).
- **Lint** before each commit: every atom has valid enums, every source and clash id exists, no duplicate ids.
- **Query:** use the Ask tab on the Master Mind, or read `wiki/pathways/<format>.md` for a format, then its niche section.
