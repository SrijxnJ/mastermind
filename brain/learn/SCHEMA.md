# Learn module schema

One JSON file per source: `brain/learn/<SOURCE_ID>.json` (L01–L10, R1). The Master Mind renders each as a visual, in-depth course page. Write for Srijan: he should be able to learn the whole video from the page without watching it. Depth over brevity, plain words, concrete examples, his niches (gym, tech/PC, gaming) used in examples where it helps (mark those as "applied").

```json
{
  "id": "L05",
  "title": "Personal brand full course",
  "creator": "Caleb Ralston",
  "url": "https://…",
  "length": "6 h 22 min",
  "kind": "youtube | ig-reel | upload | creator",
  "one_liner": "the single most important idea, ≤20 words",
  "why_it_matters": "2–3 sentences: why a creator like Srijan should care",
  "big_idea": {"statement": "the thesis in one bold sentence", "support": ["3–5 short reasons"]},
  "map": [{"chapter": "…", "time": "0:00–24:10", "gist": "≤15 words"}],
  "chapters": [{
    "title": "…", "time": "1:02:10", "summary": "3–6 sentences",
    "blocks": [ BLOCK, … ]
  }],
  "production": [{"area": "Hook | Pacing | Sound | Type | Grade | Camera | …", "detail": "…"}],
  "takeaways": [{"text": "…", "atom": "existing atom id or empty"}],
  "glossary": [{"term": "…", "def": "…"}],
  "quiz": [{"q": "…", "a": "…"}],
  "try_it": [{"title": "…", "steps": ["…"], "niche": "gym|tech|gaming|any"}]
}
```

## Blocks (pick the one that fits the idea; vary them)
| type | fields | renders as |
|---|---|---|
| `framework` | `style`: steps \| cycle \| funnel \| pyramid \| ladder \| matrix \| timeline \| equation \| venn; `title`; `items`: [{`label`, `text`}]; `caption` | a diagram (steps = numbered flow; cycle = loop; funnel = narrowing layers top→bottom; pyramid = bottom→top layers, items listed base first; ladder = abstract→concrete rungs; matrix = 2×2, exactly 4 items, plus `axes`: {`x`, `y`}; timeline = dated sequence; equation = items joined by + and the last item is the result; venn = 2–3 overlapping sets) |
| `quote` | `text` (verbatim), `who`, `time` | big pull quote |
| `stat` | `value` ("70/20/10", "15 s", "3:1"), `label`, `note`, `evidence`: stated \| claim \| observed | big number tile |
| `compare` | `title`, `left`: {`title`, `items`}, `right`: {`title`, `items`} | side-by-side (do vs don't, before vs after, A vs B) |
| `example` | `title`, `before`, `after`, `why` | rewrite card |
| `checklist` | `title`, `items` | tick list |
| `callout` | `tone`: tip \| warn \| myth \| applied, `text` | coloured note |
| `story` | `title`, `text` | anecdote the speaker told |

Rules: quotes are verbatim from the transcript; numbers and income claims carry `evidence`; every chapter has 2–6 blocks; at least one `framework` per chapter where the content has structure; 8–20 chapters for long videos (3–6 h), 3–6 for short reels. Validate the JSON (json.load) and that `matrix` has 4 items and `atom` ids exist in `brain/data/atoms.json` or `brain/data/atoms_L10.json`.
