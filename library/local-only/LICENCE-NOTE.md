# local-only/: NEVER share, upload or commit these files

Files in this folder are **licensed for use inside our videos only**. Their licences **forbid redistribution** of the raw
sound files. Don't push them to GitHub, put them in a shared Drive folder, send them to anyone, or bundle them into a
template or pack. A `.gitignore` here blocks everything except these notes.

| Folder | Source | Licence in short | Credit |
|---|---|---|---|
| `mixkit/` | mixkit.co sound effects | Mixkit Sound Effects Free License: free to use in commercial and personal videos, no attribution needed; **you may not redistribute or resell the sounds on their own** | Not required |
| `sonniss/` | Sonniss "GDC Game Audio Bundle" (sonniss.com/gameaudiogdc) | Royalty-free, commercial use allowed, no attribution; **no redistribution of the sound files** (see the licence PDF inside each bundle) | Not required |

**Status (2026-10-27): both folders are EMPTY.** From this cloud container, mixkit.co serves a Cloudflare bot challenge
(HTTP 429 `cf-mitigated: challenge`) and sonniss.com returns HTTP 403. Getting past those checks would be circumventing
the sites' bot protection, so nothing was downloaded. To fill them, on your own computer:

1. **Mixkit:** open https://mixkit.co/free-sound-effects/ (whoosh, transition, impact, pop, click, crowd, cash, game
   categories), click *Download* on the ones you like, and drop the `.wav` files into `mixkit/<category>/`.
2. **Sonniss:** download one GDC bundle part from https://sonniss.com/gameaudiogdc (each year's bundle is 20-30 GB in
   parts; take the parts that hold whooshes/transitions, impacts, UI, foley and crowd, ~2 GB max), unzip into
   `sonniss/<publisher>/`, and keep the licence PDF next to it.
3. Run `library/tools/build_library.py` style processing yourself or ask Claude to "catalogue local-only".
   Entries then appear in `catalog.json` with `"tier": "local-only"`.

Rule of thumb: anything in `library/sfx/` (tier `cc0`) may be shared; anything in `local-only/` may only be *heard in a
finished video*.
