# Standing brief: Trend Researcher

This brief lets any future run repeat the trend scan the same way. **Cadence: weekly** (Monday is best: ViralMint's Shorts tracker refreshes on Mondays). The first run was 27 Oct 2026.

## 1. Role and rules

- You report what is going viral **now** in Srijan's niches. **Findings only: no content plans, scripts or recommendations for Srijan.** Interpretation is allowed only when marked *(our take)*.
- **Cite every claim with a source URL and a date** (the post date, plus the date you accessed it).
- **Label every number:**
  - **(tracker):** a third-party tracker number (ViralMint, vidiq.com public stats pages, Modash, CreatorDB).
  - **(yt-dlp):** read from the post's own metadata.
  - **(unverified):** a single blog or aggregator source, or a TikTok search snippet.
  - Never round a number up, and never invent one. If a number is missing, say "not given".
- Prefer **concrete posts** (creator, URL, views or likes, date, length) over generic "trend" blogs. Mark blogs written by companies that sell a tool as vendor sources.
- Flag anything that is **expiring** (seasonal, event-bound) or **saturated**.
- **Do not use the vidIQ MCP tools.** The public vidiq.com stats web pages are fine to read with WebFetch.
- **Do not get around bot checks.** YouTube downloads are blocked here, and so are TikTok via yt-dlp and Instagram profile listing. Use only single-reel yt-dlp metadata.
- **Never git commit or push.** Just write the files.

## 2. Scope

- **Niches:** gym/fitness, tech/PC/gadgets, gaming (PC, console, Indian mobile), plus travel and cross-niche general formats that a gym/tech creator could adapt.
- **Platforms:** Instagram Reels, YouTube Shorts, TikTok, YouTube long-form.
- **Geography:** India and Hinglish first wherever possible, then global.
- **Window:** the last 4 to 8 weeks before the run date.
- **Length buckets:**
  - `reel30`: 30 s or less.
  - `reel60`: 31 to 60 s.
  - `reel90`: 60 s to 3 min.
  - `yt-short`
  - `yt-long`
- **Srijan context:**
  - Account: @srijan_jaiswall, based in Pune.
  - Gear and apps: iPhone 15 and a tripod; edits in Edits, CapCut and VN.
  - Language: English or Hinglish.
  - Pillars: gym (main), travel, plus extras (PC rig, dog).
  - Where to read more: `../../SYSTEM_PROMPT.md` and `../README.md`.

## 3. Sources and queries that worked (27 Oct 2026)

Use them in this order. Each item says what it gives you.

1. **ViralMint YouTube trending (best hard data, daily):**
   - Pages:
     - `https://viralmint.net/trends/youtube-trending-science-and-technology/`
     - `.../youtube-trending-gaming/`
     - `.../youtube-trending-in/` (India)
     - `.../youtube-trending-howto-and-style/`
     - `.../youtube-shorts-tracker/` (weekly Shorts breakouts, with a length, speech and breakout-multiple summary)
   - WebFetch prompt: "Snapshot date, then list all trending videos with channel, title, views, likes, short or not."
2. **vidiq.com public channel stats:** `https://vidiq.com/youtube-stats/channel/@<handle>/`. Gives the latest video, its date, views (often "in the first N hours"), top videos and 28-day views.
   - These handles worked: `@mrwhosetheboss`, `@techburner`, `@TrakinTech`, `@JeffNippard`, `@WillTennyson`, `@JesseJamesWest`, `@FitTuber`, `@TechnoGamerzOfficial`, `@TotalGaming093`.
   - These returned 404: `@shox_workout`, `@CarterPCs`.
3. **Lightreel weekly Instagram report:** `https://lightreel.ai/blogs/whats-trending-on-instagram`. Gives formats, hook formulas, a category section (fitness, tech/AI) and reel IDs. Treat its FAQ numbers as unsourced.
4. **Later Reels trends (dated weekly with audio links):** `https://later.com/blog/instagram-reels-trends/`.
5. **Audio lists:**
   - Buffer: `https://buffer.com/resources/trending-audio-instagram/`.
   - SocialBee: `https://socialbee.com/blog/trending-instagram-songs-this-week/`. It tags gym and travel audios.
   - ZOPE (Hindi Reels songs): `https://zopedigital.in/instagram-trending-songs`.
   - Revid (TikTok sounds, daily): `https://www.revid.ai/viral-tiktok-songs`.
6. **TikTok roundups** (TikTok itself can't be fetched; its discover pages return an empty shell):
   - NewEngen: `https://newengen.com/insights/tiktok-trends/` and `.../instagram-trends/`.
   - Ramdam: `https://www.ramd.am/blog/trends-tiktok`.
   - Sozee: `https://www.sozee.ai/resources/current-tiktok-trends/`. Gives trend stages and saturation.
   - **WebSearch with `allowed_domains: ["tiktok.com"]`** returns discover-page snippets that carry likes and update dates. Use these queries: `gym trend october 2026`, `pc setup trend 2026 viral`, `gaming meme sound trend october 2026`. Mark the results unverified.
7. **Memes:**
   - Know Your Meme. Search for "Know Your Meme trending memes <month year>" and fetch the trend pages, which include TikTok URLs and view counts.
   - NapoleonCat: `https://napoleoncat.com/blog/trending-memes/`.
8. **Instagram reel metadata:**
   ```
   .venv/bin/yt-dlp --skip-download -j https://www.instagram.com/reel/<ID>/
   ```
   - Read these fields: `channel`, `like_count`, `comment_count`, `upload_date` and `description`.
   - Views come back as null. TikTok URLs fail with an impersonation error.
9. **News for niche events.** Search each of these:
   - "<new device> review / durability"
   - "<game> launch players reaction"
   - "GTA 6 release"
   - "RAM prices <month year>"
   - "Flipkart sale <month year>"
   - "BGMI / Free Fire India <month year>"
   - "Instagram Edits app new features <month year>"
   - "YouTube Shorts update <month year>"
10. **Indian creator lists:** Modash, e.g. `https://www.modash.io/find-influencers/india/fitness`. Gives average reel plays and engagement.
11. **Brain creator studies:** for example `../creators/rahulmhinduja.md`, which has measured Indian tech reels.

**Low yield (skip or use last):**
- Generic "trend 2026" blogs with no dates.
- Pippit/CapCut template pages.
- SEO pages about Indian mobile games.
- Searches with several creators joined by OR (they don't match; search one creator at a time).

## 4. Steps

1. **Read context:**
   - `../README.md` (the Brain).
   - `../CLASHES.md` and `../PARKED.md`.
   - The previous report in `reports/` and `trends.json`, so you can mark what is new, rising or fading.
   - `ls .claude/skills`.
   - `ls library`.
2. **Scan:** run the sources in section 3, niche by niche. Aim for at least 3 concrete examples per niche, including at least one from India.
3. **Pull metadata:** run yt-dlp on every Instagram reel you cite.
4. **Fill each trend's fields** (see section 5).
5. **Run the gap check** (section 6).
6. **Write the outputs** (section 5) and validate the JSON:
   ```
   python3 -c "import json; json.load(open('trends.json'))"
   ```
   Also check that niche values, length-bucket values, need statuses and heat values match the allowed lists in section 5.
7. **Re-check `library/` at the end of the run.** It may be built at the same time as your run; update the need statuses if it has appeared.

## 5. Output format

**`reports/YYYY-MM-DD.md`** has these sections:
1. Headlines (5 bullets).
2. Trends by niche: one table each for gym, tech, gaming and general, with the columns Trend / Platform / Length / Heat / Best example, plus short notes.
3. Trending audio and meme sounds, by niche, with lifespan rules.
4. Capability gap: what we have, the top 10 missing items (ranked by how many trends they block), and the partial items.
5. Knowledge the Brain is missing entirely.
6. Calendar of upcoming events.
7. Sources: most useful, also used, and weak or blocked.

**`trends.json`:** overwrite it each run, keeping `first_seen` from earlier runs for any trend that continues.

```json
{"updated":"YYYY-MM-DD","trends":[{"id":"kebab-case","name":"…","niche":"gym|tech|gaming|travel|general",
 "platforms":["instagram","tiktok","yt-short","yt-long"],"formats":["reel30","reel60","reel90","yt-short","yt-long"],
 "what":"…","hook":"…","edit":"…","sound":"…",
 "examples":[{"url":"…","creator":"…","views":"… (tracker|yt-dlp|unverified)","date":"YYYY-MM-DD"}],
 "needs":[{"item":"…","status":"have|partial|missing","note":"…"}],
 "heat":1,"first_seen":"YYYY-MM-DD"}],
 "trending_audio":[{"name":"…","niche":"…","use":"…","source":"url (+date)"}],
 "brain_gaps":[{"topic":"…","why":"…"}]}
```

**Heat scale:**

| Heat | Meaning |
|---|---|
| 5 | Peaking now and still rising, or an event window opening within about 3 weeks |
| 4 | Strong, with fresh examples in the last 2 weeks |
| 3 | Active but mid-cycle, or the evidence is mostly unverified |
| 2 | Past its peak |
| 1 | Expiring or dead |

Extra top-level keys such as `window` and `notes` are allowed.

## 6. How to do the gap check

For each trend, list what an **original** version would need. Use these categories:
- skills and knowledge
- assets (SFX, music, templates, fonts, LUTs)
- sounds
- gear
- people
- access (devices, games, events)
- techniques

Mark each need with one status:

| Status | Meaning |
|---|---|
| **have** | It is in the Brain README or the System Prompt, or a skill does it today, or the gear is known to exist |
| **partial** | Possible, but with no written recipe; or it depends on unknown gear; or it can only be done in-app at post time (trending audio) |
| **missing** | Not available anywhere |

**Check each need against:**
- `../README.md`, especially the cheat-sheet sections. Transitions and Colour were still empty on 27 Oct.
- `../../SYSTEM_PROMPT.md`: gear list, gym module, playbook.
- `.claude/skills`:
  - `real-sfx`: check whether `config.json` still has `"libraries": []` (UI cues only).
  - `real-sound`
  - `earshot`
  - `hyperframes`, `hyperframes-cli` and `hyperframes-registry` (runnable; about 450 blocks)
  - `media-use`
- `.venv`: faster-whisper, yt-dlp, OpenCV.
- `library/`: sounds, memes, transitions. It did not exist on 27 Oct.
- `../PARKED.md`: parked tools, such as comment-to-DM.

**Then:**
- Rank the missing items by how many trends they block.
- List **Brain gaps**: topics the Brain does not cover at all, each with a one-line reason tied to a current trend.

## 7. Watch-list for the next run (from the 27 Oct run)

- **GTA 6:** preload 12 Nov, launch 19 Nov. Expect reaction and first-hour content.
- **LoL Worlds final:** 14 Nov.
- **BGMI Survivor League:** ends 17 Nov.
- **Diwali sales:** from 28 Oct; Black Friday on 27 Nov.
- **iPhone Duo:** the crease and crack stories are still developing (Consumer Reports).
- **MW4:** TTK and SBMM patches.
- **Peptides and stimulant content:** has it peaked?
- **Great Lock In:** runs to 31 Dec.
- **"Symphony" and the Charli XCX glitch audio:** both were rising.
- **Instagram Edits:** "Sync Video Effects to Music" was still a test.
- **`library/`:** did it appear, and what does it hold?
