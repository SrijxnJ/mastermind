# Gaming: what is going viral (Indian creators)

Updated 2026-10-27 · 102 creators listed · 92 channels measured · 3,905 videos · machine-readable: [`gaming.json`](gaming.json) · full ranked swipe file: [`gaming_swipe.md`](gaming_swipe.md)

Ranked by **outlier multiple** (views / that channel's own median for that format). Above 3x is a signal. Hooks are video **titles** (YouTube), not spoken lines. Copy the formula, never the video; every row is attributed.

## Method
ig-viral outlier method on YouTube as the main corpus (Instagram had no usable public reel URLs from web search, see confidence). 102 Indian gaming creators listed (BGMI, Free Fire, Valorant, CS2, LoL, Hindi let's-play, co-op horror, clip editors, shorts-first meme channels; 3K to 53M subs). One paced yt-dlp --flat-playlist request per channel tab (Shorts; long-form for 26 channels), 2.5 to 3 s apart, no parallel requests, no login. 92 channels returned usable view counts (3,905 videos). Each video's outlier multiple = views / that channel's own median for that format (Shorts and long-form measured separately). Rows from channels with a median under 1,000 views are kept in the creator table but excluded from formula statistics (3,785 videos remain). Hook = the title (hook_source 'title'): YouTube's bot wall ('Sign in to confirm you're not a bot') blocked per-video metadata after 11 videos, so captions, upload dates and Short lengths were not fetched for the rest and we did not work around it. captured.tsv (587 rows: every >=3x video plus the two lowest per channel-format as the floor) was run through ig-viral/swipe.py -> brain/research/viral/gaming_swipe.md. Because swipe.py named only 56 of 587 hooks with the 26 ig-reel formulas, hooks (titles with hashtags stripped) were also classified with 13 gaming-specific G-formulas (regex, priority order G11 > G13 > G7 > G4 > G5 > G2 > G9 > G3 > G8 > G1 > G10 > G12, else G6 if 4 words or fewer) and compared top third vs bottom third by multiple, per format. Profiles: 15 small-to-mid creators closest to Srijan's lane scored against ig-profile/rubric.json from public channel pages and web-search snippets only; 5 rubric items (pinned, highlights, photo, recent activity, stories) are not observable without opening Instagram and are left null. Copy the formula, never the video: every row is attributed.

**Date range:** Last 40 uploads per channel (Shorts tab, plus the long-form tab for 26 channels), collected 27 Oct 2026. Flat listings carry no dates; the 11 outliers we could date run 2023-08-04 to 2026-08-27, and feed depth ranges from about 3 weeks (daily posters) to 2+ years (rare posters). Position in the feed (0 = newest) is used as the recency proxy.

## Top outliers
| # | Multiple | Views (median) | Creator | Hook (title) | Formula | Format | Date |
|---|---|---|---|---|---|---|---|
| 1 | 600.0x | 4,200,000 (7,000) | [@PHOENIXGAMINGTM](https://www.youtube.com/shorts/PeML371kghE) | Dragon Ball Super 🔥 | G13 Desi Pop-Culture Mashup | yt-short | 2023-08-04 |
| 2 | 302.3x | 1,300,000 (4,300) | [@THELEGENDSHREEMAAN](https://www.youtube.com/shorts/lF3oYdMjDxY) | Watchparty Funny moment🫂🤣 | G6 Cryptic Micro-Caption | yt-short | 2026-08-27 |
| 3 | 230.0x | 2,300,000 (10,000) | [@LUCIFER_DANGE](https://www.youtube.com/shorts/k4ypo-kQbaM) | Wait For End 🥵😂 | G7 Wait-For-It Payoff | yt-short | 2026-02-08 |
| 4 | 169.2x | 6,600,000 (39,000) | [@GodNixon](https://www.youtube.com/shorts/V6Q1RK4X5V0) | Tag Your Squad | G11 Viewer Task CTA | yt-short | 2026-07-17 |
| 5 | 160.3x | 19,000,000 (118,500) | [@Chimkandian](https://www.youtube.com/shorts/0CKAN4zG9Xs) | Shizuka Ne Yeh Kya Dikhaya / chimkandi | G13 Desi Pop-Culture Mashup | yt-short | 2024-04-09 |
| 6 | 158.6x | 4,600,000 (29,000) | [@OutlawIndia](https://www.youtube.com/shorts/F04ELGmdFC0) | GTA 5's Most Useless Stairs 💀 | - unclassified | yt-short | n/a |
| 7 | 138.5x | 5,400,000 (39,000) | [@GodNixon](https://www.youtube.com/shorts/ZVV9Galw724) | bro is gone 💀 | G6 Cryptic Micro-Caption | yt-short | 2026-08-05 |
| 8 | 88.0x | 49,000,000 (556,500) | [@Mythpatty](https://www.youtube.com/shorts/cQznMa_iPoM) | Can ACP play Among Us? | G9 Absurd Premise / Can X Do Y | yt-short | 2023-08-31 |
| 9 | 78.6x | 550,000 (7,000) | [@PHOENIXGAMINGTM](https://www.youtube.com/shorts/FEczPGaI9C8) | Super Ultra ProMax Camper 🤣 | G6 Cryptic Micro-Caption | yt-short | 2023-08-17 |
| 10 | 78.4x | 98,000 (1,250) | [@JerryVirus](https://www.youtube.com/watch?v=1eFtfWzb9dk) | यह गेम Horror कम, Funny ज़्यादा है / REPO Highlights | - unclassified | yt-long | 2025-12-07 |
| 11 | 72.2x | 14,000,000 (194,000) | [@DynamoGaming](https://www.youtube.com/shorts/cWv9mp1kN1k) | HOK x INDIA x UltraMan Collab 🤖🔥 | G13 Desi Pop-Culture Mashup | yt-short | n/a |
| 12 | 59.1x | 19,000,000 (321,500) | [@TwoSideGamersYT](https://www.youtube.com/shorts/8oJ5q4mLD0Q) | Free Fire New Character Ritikano🤣😂 Guess The Character Name -Garena Free Fire | G11 Viewer Task CTA | yt-short | n/a |
| 13 | 57.4x | 247,000 (4,300) | [@THELEGENDSHREEMAAN](https://www.youtube.com/shorts/aSIzeACgdTg) | Malik...Ek Fek Ke Maro Idhar Bhi...🤣 | - unclassified | yt-short | n/a |
| 14 | 57.1x | 5,200,000 (91,000) | [@ezio18rip](https://www.youtube.com/shorts/2pFmApDpgc8) | MY PAV ANTHEM x RRR x HIMLANDS | G13 Desi Pop-Culture Mashup | yt-short | n/a |
| 15 | 43.9x | 28,000,000 (638,000) | [@KaashPlays](https://www.youtube.com/shorts/tBRrWZpw1CE) | RCB fans this year 😢 | G13 Desi Pop-Culture Mashup | yt-short | n/a |
| 16 | 42.0x | 458,000 (10,900) | [@Electrobgmii](https://www.youtube.com/shorts/hf9LTyY9qiU) | Wait for Trolling 🤣😂 | G7 Wait-For-It Payoff | yt-short | n/a |
| 17 | 39.4x | 8,500,000 (216,000) | [@BeastBoyShub](https://www.youtube.com/shorts/JJ8j8oPtL-s) | BBS Tries Mimic Party (Pushing 30 Btw) | G9 Absurd Premise / Can X Do Y | yt-short | n/a |
| 18 | 36.4x | 6,000,000 (165,000) | [@NEYOOGAMINGYT](https://www.youtube.com/shorts/sWMmR4tJ17o) | Socha bahar ride pe jaake aata hoon 🥲 | - unclassified | yt-short | n/a |
| 19 | 30.4x | 2,100,000 (69,000) | [@HarshKhelraay](https://www.youtube.com/shorts/08op56-VlmI) | BEST MECCHA CHAMELEON SPOT 🤣 | G6 Cryptic Micro-Caption | yt-short | n/a |
| 20 | 28.1x | 7,300,000 (260,000) | [@ChapatiHindustaniGamer](https://www.youtube.com/shorts/9wA6obRlKDM) | How gamers solve problems | G3 Gamer-Life Relatable | yt-short | n/a |
| 21 | 27.7x | 1,900,000 (68,500) | [@AntaryamiGaming](https://www.youtube.com/shorts/T_9VK-0j1eI) | Emergency | G6 Cryptic Micro-Caption | yt-short | n/a |
| 22 | 26.1x | 47,000,000 (1,800,000) | [@NotGamerFleet](https://www.youtube.com/shorts/9BEXAKiAQBM) | @GamerFleet is Professional 🤣 | G8 Big-Name Crossover | yt-short | n/a |
| 23 | 25.9x | 672,000 (26,000) | [@HASHTAG._.GAMER._.1M](https://www.youtube.com/shorts/zxAhj6iYcRU) | School Wali Girl Ne Kaha "Teri Aukaat Kya Hai" 💔😭 Fir Dekho Kya Hua 😈 | G7 Wait-For-It Payoff | yt-short | n/a |
| 24 | 25.3x | 3,000,000 (118,500) | [@Chimkandian](https://www.youtube.com/shorts/WF_ZBZd3Evg) | Shinchan Ki Satakli 😱😢💀😂🤔🗡️ | G13 Desi Pop-Culture Mashup | yt-short | n/a |
| 25 | 24.3x | 34,000,000 (1,400,000) | [@GyanGaming](https://www.youtube.com/shorts/5SIy89r2bdY) | 18M Gyan Gaming | G6 Cryptic Micro-Caption | yt-short | n/a |

62 outliers in the JSON (top 40 capped at two per channel, plus the best >=3x video of every creator in Srijan's lane).

## Formulas (G-series, gaming-specific)
Top third vs bottom third by multiple, counted separately for Shorts and long-form (3,785 videos from channels with a median of 1,000+).

| ID | Formula | Top third (short / long) | Bottom third (short / long) | Note |
|---|---|---|---|---|
| G11 | Viewer Task CTA | 18 / 1 | 8 / 5 | Joint-best hit rate in Shorts with G13: 10 of 32 cleared 3x (31%). Short imperative that gives the viewer a job (tag, comment, guess). GodNixon 'Tag Your Squad' 169x. Hit rate >=3x: shorts 10/32, long 0/8. |
| G13 | Desi Pop-Culture Mashup | 21 / 11 | 10 / 11 | A cartoon, cricket, Bollywood or anime reference dropped into a game. 13 of 41 Shorts cleared 3x (32%), 21 in the top third vs 10 in the bottom, and it owns the extreme top (Dragon Ball 600x, Shizuka 160x, RRR 57x, RCB 44x). Recognition does the hook's work. Hit rate >=3x: shorts 13/41, long 1/29. |
| G8 | Big-Name Crossover | 42 / 31 | 33 / 33 | Another big creator's name or a collab in the title. 17% hit rate in Shorts; flat in long-form. Borrowed audience, needs access Srijan does not have yet. Hit rate >=3x: shorts 19/109, long 5/109. |
| G6 | Cryptic Micro-Caption | 278 / 26 | 238 / 19 | Two to four words, usually a reaction ('bro is gone', 'Emergency', 'game over'). Largest single bucket; slightly over-indexes up top (278 vs 238). Only works when the first frame is the payoff. Hit rate >=3x: shorts 96/770, long 4/63. |
| G5 | Skill Flex Number | 53 / 16 | 40 / 7 | A number or a skill claim (1v5, 999 IQ, clutch, ace). Mild over-index in Shorts (53 vs 41). Hit rate >=3x: shorts 19/141, long 1/34. |
| G4 | Rage / Troll / Expose | 32 / 35 | 30 / 14 | Rage, troll, expose, toxic, roast. The best long-form formula: 35 top vs 14 bottom, 18% hit rate (SauraXD 'Making Gamer Girls Cry', ytRish Mumbai-server toxicity, kevvv 'This Streamer Made Fun Of Me'). Neutral in Shorts. Hit rate >=3x: shorts 12/93, long 13/71. |
| G3 | Gamer-Life Relatable | 35 / 11 | 56 / 8 | 'How gamers...', 'When...', IRL. Under-indexes in Shorts (35 top vs 56 bottom) as a title, even though one of the biggest hits (Chapati 28x) is this shape. The shape is everywhere, so on its own it is noise. Hit rate >=3x: shorts 17/131, long 4/25. |
| G7 | Wait-For-It Payoff | 33 / 1 | 47 / 1 | 'Wait for end', 'phir dekho kya hua'. Under-indexes (33 vs 47). Overused by Free Fire skit channels. Hit rate >=3x: shorts 16/129, long 0/6. |
| G9 | Absurd Premise / Can X Do Y | 25 / 41 | 32 / 35 | 'Can X...', survive, escape, tries, challenge. Even in Shorts; dead in long-form (1 of 124 cleared 3x) because it is the default long-form title. Hit rate >=3x: shorts 11/84, long 1/124. |
| G2 | Desi Server / Lobby | 16 / 40 | 13 / 42 | India, Indian, Mumbai server, desi, random teammates. About baseline (14% in Shorts, 3% in long-form; it is the niche's default), but it is the title of almost every small Valorant/CS2 outlier (ytRish 14x, Lmaoo Noob 10x, Salty Boys 3.7x). Hit rate >=3x: shorts 6/44, long 4/132. |
| G1 | Friend Callout | 44 / 10 | 53 / 11 | A friend or teammate named in the title (@mention, dost, squad, bhai). Slightly under baseline (8% in Shorts, 44 top vs 53 bottom); works only when the friend is a known character (NotGamerFleet's @GamerFleet 26x). Hit rate >=3x: shorts 13/153, long 2/31. |
| G10 | News / Drop / Event | 41 / 8 | 45 / 9 | News, drops, events: GTA 6, PMWC/EWC/BGIS, bundles, updates. Baseline overall; small esports-news channels spike on fresh results (iFlicks 22x, Droid Plays 22-24x). Hit rate >=3x: shorts 17/135, long 0/26. |
| G12 | Series Label | 3 / 3 | 5 / 26 | Part / Episode / Day N. Never cleared 3x (0 of 47). Bottom-heavy in long-form (3 top vs 26 bottom). Series labels hold a base, they do not break out. Hit rate >=3x: shorts 0/11, long 0/36. |
| hooks.json-26 | The 26 ig-reel formulas | 16 | 24 | swipe.py named only 56 of 587 captured hooks with the 26 formulas (531 unclassified). Classified hooks sit more in the bottom third (24) than the top (16). Head To Head (#17, 'PUBG vs Free Fire') x5 and Verbatim Question (#16, 'Can ACP play Among Us?') x4 were the only repeats in the top third. Indian gaming titles are not written in the education/business hook grammar the 26 come from, which is why the G-series above exists. Median hook score top third 29 vs bottom 31: hookscore.py does not separate gaming titles. |

## Structure: what the top third shares
- Shorts break out, long-form holds: 12% of Shorts cleared 3x their channel median vs 5% of long videos (2,661 vs 1,124 videos).
- The title barely separates winners from losers in Shorts: median title length is 5 words in both the top and bottom third, and hookscore.py gives the top third 29 vs 31 for the bottom. In Shorts the first frame is the hook; the title is a caption. This data cannot see the first frame.
- What the top-third Shorts titles do have: a reaction in 4 words or fewer (14% hit rate vs 11%), Roman Hinglish (15% vs 12%), an @mention of a known person (16% vs 12%), one or two emoji with 💀 or 🤣. ALL-CAPS titles (9% vs 13%) and pipe-separated series titles (5% vs 13%) under-index.
- Long-form is the opposite: the top third is driven by conflict words (rage, troll, toxic, expose, roast: 18% hit rate) and the 'Part / Episode / Day N' label never broke out (0 of 36).
- Age effect: top-third Shorts sit deeper in the feed (median position 20 vs 15), so part of every multiple is time to accumulate views. Outliers among a channel's last five uploads (listed in viral_now) are the cleaner signal.
- Channel size: channels under 100K subs hit 3x on 9% of Shorts vs 13 to 14% for bigger channels, but the biggest multiples in the whole set come from small or mid channels (Half Skirmish 271x on a 354 median, THELEGENDSHREEMAAN 302x on 4,300, GodNixon 169x on 39,000).
- Known lengths (11 dated outliers): the big Shorts hits are 16 to 59 s, most 16 to 35 s (GodNixon 16 s and 35 s, THELEGENDSHREEMAAN 22 s, LUCIFER DANGE 25 s, PHOENIX 29 s). The long-form outlier (JerryVirus REPO highlights) is 12:47.
- CTA: the only CTA that shows up as a title pattern is the viewer task (tag your squad, comment, guess). It ties with G13 for the best hit rate in the set (31 to 32%). No other CTA is visible from titles.

## Unclassified, read by hand
Hooks the 26 ig-reel formulas could not name that look like formulas of their own.

- **"GTA 5's Most Useless Stairs 💀"** (The Outlaw (@OutlawIndia), 158.6x): Same channel repeats it: 'These GTA 5 Barrels Can Save Your Life 💀' 14.6x, 'Michael's Most Painful Moment in GTA 5 💀' 8.6x. A 'game-world oddity' formula: one weird object inside a famous game, superlative + skull. Not in hooks.json (The Superlative only matches at the start of the line).
- **"Socha bahar ride pe jaake aata hoon 🥲"** (Neyoo (@NEYOOGAMINGYT), 36.4x): First-person Hinglish inner monologue as the title. Same channel: 'Hum saale single he marenge 😭' 6.1x, '2 Crore ka nade recreate kar raha tha 😂' 8.5x; GodNixon 'iPhone 13 Todne Pe Surgery Kardi Guys 😂' 17.2x. Closest shape to Srijan's own voice. Candidate formula: Inner-Monologue Hinglish.
- **"Malik...Ek Fek Ke Maro Idhar Bhi...🤣"** (THE LEGEND SHREEMAAN (@THELEGENDSHREEMAAN), 57.4x): The friend's or streamer's own line, quoted verbatim, is the title ('"Not Your Type" Voicepack Reaction' 44.4x; JerryVirus 'Jerryyyy utarr naaa 😡' 6.1x). The gaming version of reading a comment out loud. Candidate formula: Verbatim Voice-Chat Quote.
- **"Gen Z Dad Be Like"** (GodNixon (@GodNixon), 9.9x): 'X be like' persona skit from a BGMI pro. Maps onto 'Corporate employee be like' for Srijan.
- **"Watchparty Funny moment🫂🤣"** (THE LEGEND SHREEMAAN (@THELEGENDSHREEMAAN), 302.3x (22 s, 27 Aug 2026)): A fan clip channel cutting a watch-party moment of two big streamers out-multiplied everything recent. The format is 'the reaction, not the game'.
- **"Dragon Ball Super 🔥"** (PHOENIX GAMING (@PHOENIXGAMINGTM), 600x (29 s, Aug 2023)): Single pop-culture name as the whole title over a BGMI clip. Old, but it is the purest example of G13: recognition carries the hook.
- **"Train Mein Mili 3 Cute Girls Ne Diya Number 😱 Phir Bot Account Se Kiya Aisa Prank"** (HASHTAG GAMER 1M (@HASHTAG._.GAMER._.1M), 22.7x): Long story-bait titles still work on faceless Free Fire skit channels. Not Srijan's audience; noted so it is not copied.

## Works
- Give the viewer a job in the title: 'Tag Your Squad' (GodNixon 169x, 35 s), comment/guess prompts. 10 of 32 such Shorts cleared 3x (31%), joint best with G13.
- Desi pop culture dropped into a game: Doraemon/Shinchan characters (Chimkandian 160x, 25x, 24x), RCB (Kaash Plays 44x), RRR (Ezio18rip 57x), Dragon Ball (PHOENIX 600x), Bigg Boss (Rakazone 14x). 13 of 41 such Shorts cleared 3x (32%, level with the viewer-task titles) and they own the extreme top.
- Social-deduction / hide-and-seek party games with friends: Mimic Party, Meccha Chameleon, Among Us. 'Mimic' titles have a median multiple of 2.0x (33% over 3x); BeastBoyShub 'BBS Tries Mimic Party (Pushing 30 Btw)' 39x, Harsh Khelraay 'BEST MECCHA CHAMELEON SPOT 🤣' 30x, MythPlays 'Can ACP play Among Us?' 88x.
- Conflict titles in long-form: troll/rage/toxic/expose/roast is the only formula that over-indexes in long videos (35 top vs 14 bottom, 18% hit rate). SauraXD 'Making Gamer Girls Cry in Valorant' 5.7x, kevvv 'This Streamer Made Fun Of Me. So I Destroyed Him.' 3.5x, ytRish three Mumbai-server toxicity videos at 12.9x to 14.1x.
- Indian-server chaos is the small PC-shooter channel's breakout: Half Skirmish 'Toxic Kids in Valorant India *FUNNY*' 271x, ytRish 14x, Lmaoo Noob 'Trolling Random Teammates In Valorant Mumbai Server 😹' 10x, Salty Boys 'Funniest 1V5 Clutch💀' 10x and 'Peak CS2 India Gameplay (Nothing Makes Sense) 💀' 3.7x (its newest video).
- Short reaction captions in Roman Hinglish with a 💀/🤣: 'bro is gone 💀' (GodNixon 138x, 16 s), 'game over 💀' 72x, 'Emergency' (Antaryami 28x), 'Malik ko pel dia' 22x.
- Clip channels around one streamer: fan editors out-multiply the source (THELEGENDSHREEMAAN 302x; Creator Studios 10x; ShreeMan Highlights runs on a stated 'one month after the stream' permission rule).
- A festival mini-vlog from a gamer: last Diwali Dynamo Gaming 'Diwali & Phatakey - Mini Vlog' 8.8x and Kaash Plays 'Happy Diwali 😭🧨' 7.8x.

## Doesn't work
- Topic alone. GTA 6 titles (111 videos) have a median multiple of 0.96x and 6% cleared 3x; R.E.P.O. 0.96x; Backrooms 0.86x; horror/scary/haunted words 0.95x with 3% over 3x. Everyone in the niche covers these, so the topic is the baseline, not the lift.
- Series labels: Part / Episode / Day N cleared 3x 0 times in 47 videos and sit in the bottom third of long-form (26 bottom vs 3 top). They keep a base audience; they never break out.
- 'Wait for end' / 'phir dekho kya hua' bait: 33 top vs 47 bottom in Shorts. Free Fire skit channels have worn it out.
- Generic 'How gamers... / When... / Every gamer...' titles: 35 top vs 56 bottom in Shorts. The relatable shape only works when the clip itself is specific (Chapati 'How gamers solve problems' 28x is the exception, not the rule).
- ALL-CAPS Shorts titles (9% vs 13%) and pipe-separated SEO titles on Shorts (5% vs 13%).
- Business-style hook grammar: the 26 ig-reel formulas named only 56 of 587 hooks, and the named ones sit more in the bottom third (24) than the top (16). hookscore.py does not separate gaming titles (29 top vs 31 bottom).
- Long-form for very small channels: Salty Boys' long-form median is 3,000 and JerryVirus' 1,250; their Shorts medians are 1,500 and 15,000. JerryVirus' 98K REPO highlights (78x) shows a long video can pop, but it took 40 uploads to find one.
- COD MW4 and LoL: zero Indian creators in the 92 channels titled a video about either in their last 40 uploads (3 old COD titles in total). There is no Indian evidence for these yet, only the global trend.

## Can work for Srijan
- CS2/Valorant 'Mumbai server' chaos Shorts with his friends' voice chat (G2 + G4). Why: it is the proven breakout route for small PC-shooter channels (Half Skirmish 271x, ytRish 14x, Lmaoo Noob 10x, Salty Boys 10x), it is footage Srijan already makes, and the Indian CS2 lane is nearly empty (Salty Boys 8K subs, No Pressure 283). Bleep the gaali.
- R.E.P.O. / Mimic-style co-op chaos with the same 3 to 4 friends, titled as a viewer task ('Tag the friend who...') (G11 on co-op footage). Why: G11 has a joint-best hit rate in the set (31%) and the tag turns the clip into a share inside friend groups like his own; co-op party games with friends are the hottest topic shape right now (Mimic 2.0x median).
- Desi pop-culture lines said in his own voice over his own clips: a monster becomes 'Shinchan ki mummy', Backrooms Level 0 becomes 'Pune PG ka corridor' (G13). Why: recognition is the biggest lift in the data (32% hit rate, 13 of 41, and the top of the table), and saying the reference himself avoids copyrighted clips and fits his Hinglish voice.
- First-person Hinglish inner-monologue captions about office-gamer life (candidate formula from the unclassified rows). Why: Neyoo 36x and GodNixon 17x show the 'socha ki...' shape works, and it is exactly how Srijan already talks (self-roast first, short verdict last). His 9-to-6 job is the angle nobody in this sample has.
- Micro-captions of 4 words or fewer with 💀 on a clip whose first frame is already the payoff (G6). Why: 14% hit rate and the biggest recent BGMI hits (GodNixon 'bro is gone 💀' 138x at 16 s); it only works if the edit starts on the moment, which suits his setup-to-payoff-under-20-s lane.
- 'Before GTA 6' as a joke line, not GTA 6 news. Why: GTA 6 titles are saturated (0.96x), but the meme form still lifts (Chapati 'iPhone 18 before GTA 6' 7.3x, Mythpat 'First Indian To Buy GTA 6' 4.1x). He has no console for launch day, so the joke is the only GTA 6 content he can make.
- A Diwali (8 Nov) 'gamer's Diwali' mini-vlog Short: rig, Sophie, patakhe, friends online. Why: both festival Shorts in the sample beat their channel by 7.8x to 8.8x last year, and it bridges his gaming and Pune/personality pillars.
- Later, not now: long-form compilations with a conflict title ('My friends sold me out 4 times in R.E.P.O.'). Why: G4 is the only long-form formula that over-indexes, but small channels' long-form medians are a fraction of their Shorts; build the Shorts base first.

## Viral right now
| What | Evidence | Until |
|---|---|---|
| Social-deduction / hide co-op party games (Mimic Party, Meccha Chameleon, Among Us revival) | BeastBoyShub 'BBS Tries Mimic Party' 39.4x; Harsh Khelraay 'BEST MECCHA CHAMELEON SPOT 🤣' 30.4x and 'Indian meme in Mimic party 😭😭' 5.7x (one of his last 4 uploads); Xyaa 'PERFECT CAMOUFLAGE #mecchachameleon' 4.6x; Live Insaan 'Mimic Party vs Ruchika and Harshit' 2.3x (5th newest). Undated, mid-to-recent feed positions. | Dec 2026 (estimate; party-game cycles run 2 to 3 months) |
| GTA 6 countdown and 'before GTA 6' jokes | Mythpat 'First Indian To Buy GTA 6 🤣🤣😎😎' 34M views, 4.1x (5th newest); MehulBest 'Don't Buy a PS5 Pro for GTA 6!' 5.6x (4th newest); Chapati Hindustani Gamer 'iPhone 18 before GTA 6' 7.3x. But 111 GTA 6 titles average 0.96x: the topic is saturated, the joke is not. Preload 12 Nov, launch 19 Nov (PS5/Xbox only). | 2026-11-30 |
| Indian mobile-esports result Shorts (PMWC 2026 / EWC, BGIS, PEL 2026, BGMI Survivor League) | Droid Plays' three newest Shorts at 22x to 24x ('Goldy Bhai Vs Owais Controversy!', 'Chinese Are Insane #pel2026', 'Oldest Player In BGIS Semifinals'); iFlicks 'WTF Shocking… GodLike in PMWC Finals' 22.4x. Survivor League (50 creators) runs to 17 Nov. | 2026-11-17 |
| BGMI squad meme Shorts with a micro-caption or a tag task | GodNixon 'Tag Your Squad' 169x (35 s, 17 Jul 2026), 'bro is gone 💀' 138x (16 s, 5 Aug 2026), 'game over 💀' 72x. | ongoing (3+ months running) |
| Streamer watch-party and voice-pack reaction clips by fan editors | THE LEGEND SHREEMAAN 'Watchparty Funny moment🫂🤣' 302x (22 s, 27 Aug 2026) and 'Reaction says it all...🫡' 4.9x (4th newest). | ongoing |
| Diwali gamer mini-vlogs | Last year: Dynamo Gaming 'Diwali & Phatakey - Mini Vlog' 8.8x, Kaash Plays 'Happy Diwali 😭🧨' 7.8x. Diwali is 8 Nov 2026. | 2026-11-10 |
| Halloween horror (running, but not lifting) | 8 Halloween titles, best 1.6x (Gaming Engineer 'Granny Halloween Update'); horror/scary words overall 0.95x. Granny 3/5 updates did better (Live Insaan 2.5x, BeastBoyShub 2.4x). | 2026-10-31 |
| COD MW4 launch memes (global only) | No Indian creator in the 92 channels posted MW4 in their last 40 uploads. The global trend is in brain/research/reports/2026-10-27.md (zanny 525K, nuke-cutscene backlash). No Indian evidence. | 2026-11-15 (global estimate) |

## Profile study (15 small-to-mid creators, ig-profile rubric)
Scored from public channel pages and web-search snippets only. Pinned three, highlights, photo, recency and stories are not observable without opening Instagram, so scores are out of the 60 observable points, scaled to 100.

| Handle | Score | Name | Bio (public) | Lesson |
|---|---|---|---|---|
| @SaltyBoys | 28 (17/60) | Salty Boys (IG: @salty_boys___, 13K followers, 74 posts per search snippet) | Hello, we are back! The Salty Boys are back! Atif, Sabarmati, and Forest are all back! | The cast is the product (three named friends in the bio, 'Feat. @SauraXD' is their best long video at 5.3x), but nothing in the name or bio says 'CS2 India funny', and the IG handle has stacked underscores. Closest account to Srijan's lane and the clearest warning: the friend group alone does not tell a stranger why to follow. |
| @SauraXD | 48 (29/60) | SauraXD | XD in my name is ironic, i am actually crying inside :( Subscribe for Daily Uploads. Business mail: ... | Self-roast bio line and titles that are a feeling, not a game ('Valorant Ranked Hits Differently At 3am' 6.0x). Personality is there; searched words are not. |
| @TheBrownVoid | 45 (27/60) | TheBrownVoid | Subscribe or else I'll take all your cookies and run away! Business Enquiry: ... | The most legible grid in the set: every long title ends '| Valorant Funny Moments India' with a starred keyword up front ('*WORST* Teammates in Valorant India😭'). Template titles build search; the joke bio does nothing. |
| @kevvvfps | 38 (23/60) | Kevvv FPS (IG name field: Kevin Solomon) | Hi I'm Kevvv. I love video games and if you do too, we're gonna have a blast together! | Only creator in the 15 with a searched word in the name ('FPS'). Shorts median 94K on 63K subs because titles are curiosity lines ('Bro Can't Stop Saying This One Word!' 10.6x). The IG name field wastes the slot on a real name. |
| @JerryVirus | 47 (28/60) | JerryVirus | Just here to have fun and build a great community! I play a variety of games. Mostly GTAV RP., but also BGMI (PUBG MOBILE), and other FPS ga | Devanagari-plus-English titles with a fixed '| REPO Highlights' tail gave the biggest long-form multiple in the lane (78x). Different handle on IG (@ig_jerryvirus) splits the brand. |
| @XyaaLive | 58 (35/60) | Xyaa | Hello! I am a variety gamer and streamer from India! You can watch more games that I play on my 2nd channel. Business queries: ... | Highest score: same handle on YouTube and IG, one link, a who-and-where bio line, and org affiliation as proof on IG. Her best Shorts are Hinglish lines spoken to camera ('Tum ek kaam karo, Gaming ki tayyari shuru kar do!' 4.9x). |
| @bhupeshyt | 33 (20/60) | Bhupesh | I edit videos for a living and play video games sometimes :D | Best identity line in the set for Srijan to learn from: a day job plus games, said plainly. Lowercase meme titles ('griefing level : professional'). Nothing else on the page (no link, no contact) converts it. |
| @defusedlive | 45 (27/60) | DEFUSED LIVE | PRO DEFUSED IN OTHER GAMES 😈 For Promotions & Enquiry: ... | Inside-joke bio, keyworded long titles ('...Horror video in Hindi'). Group-horror Minecraft with friends holds 145K long-form median; Shorts stall (14 in feed). |
| @HarshKhelraay | 43 (26/60) | Harsh Khelraay | Harsh Salunkhe AKA Harsh Khelraay. Good Valorant player known for Viper plays. Also Good at Photoshop and I do Thumbnail making streams. ... | A Valorant player whose biggest Short is a party game (Meccha Chameleon 30x). The bio names a specialism (Viper) and a quirk (shouting); the pun handle is memorable and sayable. |
| @SkRossi | 55 (33/60) | SkRossi | I'm SkRossi (Ganesh Gangadhar). On this channel, I do Valorant Livestreams and sometimes other games as well. I am a part of the Indian Espo | Clear what-and-why bio, but six links is a menu. His top Shorts are the human moments (reaction 11.8x, 'I can never get an Ace' 8.8x), not the tips. |
| @HydraFlick | 40 (24/60) | HydraFlick | Hi, I'm HydraFlick aka Rohan Ledwani, your fellow Indian content creator from Gujarat. ... I'm 27. Full-time Live Streamer/content creator.  | Age and city in the bio make him a person (Srijan's '26, Pune' does the same job). Grid is mixed tournament series, which flattens the Shorts median (22K). |
| @Meow16K | 52 (31/60) | Meow16K | I'm Saloni Pawar, you can call me Meow. I livestream first-person shooter games LIVE on this channel and play Valorant Professionally for Ri | Bio line one carries proof (pro team). Same handle everywhere. Her best Short is a Hinglish question to the viewer ('Game khelneka sahi waqt konsa hai dosto?' 8.3x), the G11 pattern again. |
| @Lmaoonoob | 55 (33/60) | Lmaoo Noob | I create fun and light-hearted Valorant trolling videos where I bait, confuse, and shock random teammates all for your entertainment. My goa | Best bio in the set at 630 subs: names the game, the behaviour and the victim. One repeated title template ('... Random Teammates In Valorant Mumbai Server 😹') gives a 10x hit. Proof that a tiny account can have a full-marks bio. |
| @ytRish | 40 (24/60) | RishYT | RishYT Official ⚡33. Games are Suppose to be Fun not Stressful. Valorant INDIA Content Creator ❤️ | Wasted first line, but the grid is one promise repeated (Mumbai-server toxicity) and three of those videos hit 13x to 14x on a 1,700 median. |
| @shreeman31 | 45 (27/60) | ShreeMan Highlights | Welcome to Shreeman Highlights! This is the ultimate fan-made channel dedicated to the legendary Shreeman Legend and his epic gaming moments | Clip editor done properly: says whose clips, what kind, and the permission rule. But near-identical titles ('REPO Funniest Moment 😂 | ShreeMan Legend' x many) blur the grid; the rival fan channel with varied quote-titles gets 300x. |

## Profile patterns
- 0 of 15 put a searched word in the display name (the IG name-field equivalent). Kevvv FPS and ShreeMan Highlights are the only two with any keyword. 'Srijan | CS2 & R.E.P.O. chaos' style name fields have no competition in this lane.
- The strongest bios name the game, the behaviour and the victim (Lmaoo Noob: 'bait, confuse, and shock random teammates') or carry proof (Meow16K: pro for Rising Esports; Xyaa: org affiliation on IG). Pure joke bios (TheBrownVoid, SauraXD, DEFUSED) give personality and no reason to follow.
- A day-job identity line is rare and memorable: Bhupesh 'I edit videos for a living and play video games sometimes'. Nobody in the 15 claims the office-gamer identity Srijan has.
- Age and city make a gamer a person: HydraFlick '27, Vadodara'. Srijan's '26, Pune' fits the same slot.
- Links are thin: only 5 of 15 descriptions carry a business email, only Xyaa points to a single destination (her second channel), and SkRossi lists six links (a menu).
- Handles drift across platforms in at least 3 of 15 (Salty Boys -> @salty_boys___, JerryVirus -> @ig_jerryvirus, Kevvv FPS -> @kevvv_fps). The accounts that keep one handle everywhere (Xyaa, Meow16K, Harsh Khelraay) score highest on that item.
- Friend-group channels sell the cast by name (Salty Boys' bio is three names; Live Insaan titles name Harshit and Ruchika; ShreeMan's fans title clips 'Why Always Tiwari?'). Named recurring friends are what titles can call out later.
- Legible grids come from one repeated title promise ('... | Valorant Funny Moments India', '... Mumbai Server 😹', '... | REPO Highlights'). Repetition helps search on long-form; on Shorts, identical titles blur (ShreeMan Highlights).
- Not observable without opening Instagram (left null in every breakdown): pinned three, highlights, profile photo, posting recency and story rings. Scores are out of the 60 observable points, scaled to 100.

## Your version (Srijan's hooks)
- **G11 Viewer Task CTA:** "Tag karo us dost ko jo R.E.P.O. mein hamesha sabse pehle marta hai."  
  Joint-best hit rate in the data (10 of 32 task-titled Shorts cleared 3x, 31%; GodNixon 'Tag Your Squad' 169x). His friend-group game nights supply the clip and the tag spreads it through groups like his own.
- **G2 Desi Server / Lobby (+ G4 Rage):** "Mumbai server pe maine bas 'hi' bola. Round 3 tak do log mujhe report kar chuke the."  
  Indian-server chaos is how small PC-shooter channels break out (Half Skirmish 271x, ytRish 14x, Lmaoo Noob 10x, Salty Boys 10x), and the CS2 India lane is nearly empty. Specific numbers, self-roast first, per his voice rules.
- **G13 Desi Pop-Culture Mashup:** "Backrooms Level 0 aur mera Pune wala PG. Spot the difference."  
  Recognition is the biggest lift (13 of 41 Shorts over 3x, 32%; Chimkandian 160x, Ezio18rip 57x, Kaash Plays 44x). He says the reference himself, so no copyrighted clip, and it ties gaming to his Pune pillar.
- **candidate: Inner-Monologue Hinglish Inner-Monologue Hinglish (from unclassified):** "Socha bas ek match khel ke so jaunga. Ab 3:40 baj gaye hain aur standup 9:30 ka hai."  
  Neyoo 'Socha bahar ride pe jaake aata hoon 🥲' 36x and GodNixon 17x use this exact shape; it is how Srijan already talks, and the office-gamer angle is unclaimed in the 15 profiles studied.
- **G6 Cryptic Micro-Caption:** "bro is gone 💀"  
  On-screen text only, over a clip that opens on a friend falling into a R.E.P.O. pit or getting one-tapped. GodNixon's 16 s 'bro is gone 💀' did 138x; it works only when the first frame is the payoff, which fits his under-20-s cut.
- **G5 Skill Flex Number:** "26 saal, 9 to 6 job, aur yeh 1v4 clutch. Raat ke 2 baje. 💀"  
  Salty Boys 'Funniest 1V5 Clutch💀' 10x on a 1,500 median; the corporate-guy contrast makes a normal clutch specific to him (Clutch or Choke franchise).

## Creator table
| Creator | Handle | Subs | Median views | Sampled | Top outlier |
|---|---|---|---|---|---|
| Phoenix Gaming | [@PHOENIXGAMINGTM](https://www.youtube.com/@PHOENIXGAMINGTM) | 59,600 | 7,000 | 40 | 600.0x "Dragon Ball Super 🔥" |
| The Legend Shreemaan (fan clips) | [@THELEGENDSHREEMAAN](https://www.youtube.com/@THELEGENDSHREEMAAN) | 3,670 | 4,300 | 40 | 302.3x "Watchparty Funny moment🫂🤣 #shreemanlegend #jonatha" |
| Half Skirmish | [@halfskirmish](https://www.youtube.com/@halfskirmish) | 1,230 | 354 | 40 | 270.8x "Toxic Kids in Valorant India *FUNNY*" |
| LUCIFER DANGE | [@LUCIFER_DANGE](https://www.youtube.com/@LUCIFER_DANGE) | 23,400 | 10,000 | 40 | 230.0x "Wait For End 🥵😂 #shorts #funny #freefirefunny #com" |
| GodNixon | [@GodNixon](https://www.youtube.com/@godnixon) | 1,440,000 | 39,000 | 40 | 169.2x "Tag Your Squad" |
| Chimkandian | [@Chimkandian](https://www.youtube.com/@Chimkandian) | 1,010,000 | 118,500 | 40 | 160.3x "Shizuka Ne Yeh Kya Dikhaya / chimkandi" |
| The Outlaw | [@OutlawIndia](https://www.youtube.com/@OutlawIndia) | 43,700 | 29,000 | 29 | 158.6x "GTA 5's Most Useless Stairs 💀" |
| MythPlays | [@Mythpatty](https://www.youtube.com/@Mythpatty) | 2,500,000 | 556,500 | 45 | 88.0x "Can ACP play Among Us?" |
| JerryVirus | [@JerryVirus](https://www.youtube.com/@JerryVirus) | 69,700 | 15,000 | 80 | 78.4x "यह गेम Horror कम, Funny ज़्यादा है / REPO Highligh" |
| Dynamo Gaming | [@DynamoGaming](https://www.youtube.com/@DynamoGaming) | 10,100,000 | 194,000 | 40 | 72.2x "HOK x INDIA x UltraMan Collab 🤖🔥" |
| Two Side Gamers | [@TwoSideGamersYT](https://www.youtube.com/@TwoSideGamersYT) | 12,900,000 | 321,500 | 40 | 59.1x "Free Fire New Character Ritikano🤣😂 Guess The Chara" |
| Ezio18rip | [@ezio18rip](https://www.youtube.com/@ezio18rip) | 1,880,000 | 91,000 | 80 | 57.1x "MY PAV ANTHEM x RRR x HIMLANDS #EZIO #ezio18rip #H" |
| Kaash Plays | [@KaashPlays](https://www.youtube.com/@KaashPlays) | 1,820,000 | 638,000 | 40 | 43.9x "RCB fans this year 😢 #viratkohli" |
| Electro ice-zard | [@Electrobgmii](https://www.youtube.com/@Electrobgmii) | 704,000 | 10,900 | 40 | 42.0x "Wait for Trolling 🤣😂 #shorts" |
| BeastBoyShub | [@BeastBoyShub](https://www.youtube.com/@BeastBoyShub) | 7,260,000 | 216,000 | 80 | 39.4x "BBS Tries Mimic Party (Pushing 30 Btw)" |
| Neyoo | [@NEYOOGAMINGYT](https://www.youtube.com/@NEYOOGAMINGYT) | 783,000 | 165,000 | 40 | 36.4x "Socha bahar ride pe jaake aata hoon 🥲" |
| Harsh Khelraay | [@HarshKhelraay](https://www.youtube.com/@HarshKhelraay) | 150,000 | 69,000 | 40 | 30.4x "BEST MECCHA CHAMELEON SPOT 🤣" |
| Chapati Hindustani Gamer | [@ChapatiHindustaniGamer](https://www.youtube.com/@ChapatiHindustaniGamer) | 8,770,000 | 260,000 | 40 | 28.1x "How gamers solve problems" |
| Antaryami Gaming | [@AntaryamiGaming](https://www.youtube.com/@AntaryamiGaming) | 4,020,000 | 68,500 | 40 | 27.7x "Emergency #comedy #funny" |
| NotGamerFleet | [@NotGamerFleet](https://www.youtube.com/@NotGamerFleet) | 4,870,000 | 1,800,000 | 80 | 26.1x "@GamerFleet is Professional 🤣 / #gamerfleet #short" |
| HASHTAG GAMER 1M | [@HASHTAG._.GAMER._.1M](https://www.youtube.com/@HASHTAG._.GAMER._.1M) | 811,000 | 26,000 | 40 | 25.9x "School Wali Girl Ne Kaha "Teri Aukaat Kya Hai" 💔😭 " |
| Gyan Gaming | [@GyanGaming](https://www.youtube.com/@GyanGaming) | 19,600,000 | 1,400,000 | 40 | 24.3x "18M Gyan Gaming #freefire" |
| Droid Plays | [@DroidPlays27](https://www.youtube.com/@DroidPlays27) | 2,290 | 1,000 | 40 | 24.0x "Goldy Bhai Vs Owais Controversy! #bgis #soul #bgmi" |
| iFlicks | [@iflickss](https://www.youtube.com/@iflickss) | 191,000 | 25,000 | 40 | 22.4x "WTF Shocking… GodLike in PMWC Finals…🥶 / EWC #GodL" |
| Gaming Engineer | [@GamingEngineerOfficial](https://www.youtube.com/@GamingEngineerOfficial) | 1,540,000 | 323,500 | 40 | 21.9x "Alert ⚠️:These Plugs are NOT for kids 🤣 #shorts #g" |
| Lokesh Gamer | [@LokeshGamer](https://www.youtube.com/@LOKESHGAMER) | 16,500,000 | 349,000 | 40 | 19.2x "Lokesh Gamer BMW M4 #shorts #shortsfeed #freefire" |
| Sooneeta | [@Sooneeta](https://www.youtube.com/@Sooneeta) | 11,100,000 | 635,500 | 40 | 17.3x "Destroying Ego of Random Teammate 😎 #shorts #freef" |
| Thugesh | [@Thugesh](https://www.youtube.com/@Thugesh) | 6,630,000 | 2,350,000 | 18 | 14.9x "Scammer Dost! 😂" |
| GoD camper gaming | [@GoD_camper_gaming](https://www.youtube.com/@GoD_camper_gaming) | 3,180 | 1,150 | 40 | 14.8x "Wait for 1vs4 ever￼￼ 💀…#ytshorts #shorts #bgmi #vi" |
| Sharkshe | [@Sharkshe](https://www.youtube.com/@SHARKSHE) | 581,000 | 110,500 | 40 | 14.5x "Budget Challenge 💸🖤🔝🦈 ft. @JONATHAN GAMING" |
| RishYT | [@ytRish](https://www.youtube.com/@ytRish) | 1,880 | 1,700 | 40 | 14.1x "VALORANT Agent Insta Lock Toxicity in Mumbai Serve" |
| Rakazone Gaming | [@RakaZoneGaming](https://www.youtube.com/@RakaZoneGaming) | 532,000 | 86,000 | 40 | 13.9x "Scout in Big Boss 😮 #shorts" |
| MortaL | [@MortaLyt](https://www.youtube.com/@MortaLyt) | 6,950,000 | 56,000 | 40 | 13.2x "MY GOBU ❤️🔥💣" |
| SkRossi | [@SkRossi](https://www.youtube.com/@SkRossi) | 167,000 | 25,500 | 30 | 11.8x "his reaction is priceless 😂 #valorant #shorts #val" |
| Dattrax Gaming | [@DattraxGaming](https://www.youtube.com/@DattraxGaming) | 3,400,000 | 111,500 | 40 | 11.7x "THE ULTIMATE GOLDEN CAR HEIST In GTA 5 Real Life!🔥" |
| Yessmartypie | [@Yessmartypie](https://www.youtube.com/@YesSmartyPie) | 6,910,000 | 866,500 | 40 | 11.5x "Most OP Clutch in Minecraft" |
| MehulBest | [@mehulbestYT](https://www.youtube.com/@mehulbestYT) | 2,430 | 1,350 | 40 | 11.1x "Ps5 back in stock🎉🎉 #ps5 #viral #shorts" |
| Kevvv FPS | [@kevvvfps](https://www.youtube.com/@kevvvfps) | 62,900 | 94,000 | 78 | 10.6x "Bro Can't Stop Saying This One Word!" |
| PANSHU LIVE | [@PANSHULive](https://www.youtube.com/@PANSHULive) | 35,000 | 2,350 | 40 | 10.6x "Legendry Action bundle 😈 #panshulive #freefire" |
| MLIMM Gaming | [@mlimm_gaming](https://www.youtube.com/@mlimm_gaming) | 77,500 | 10,500 | 40 | 10.5x "Prrra hai apna no4😂📈" |
| CarryMinati | [@CarryMinati](https://www.youtube.com/@CarryMinati) | 45,800,000 | 7,000,000 | 17 | 10.0x "Toh guys, naya vlog aane vaala hai taiyaar rehna 💀" |
| Creator Studios | [@creatorstudiosofficial](https://www.youtube.com/@creatorstudiosofficial) | 16,000 | 3,500 | 40 | 10.0x "Shreeman Legend Kaam25 Hogaya #shorts" |
| Salty Boys | [@SaltyBoys](https://www.youtube.com/@SaltyBoys) | 7,990 | 1,500 | 80 | 10.0x "Funniest 1V5 Clutch💀" |
| Lmaoo Noob | [@Lmaoonoob](https://www.youtube.com/@Lmaoonoob) | 630 | 1,700 | 40 | 10.0x "Trolling Random Teammates In Valorant Mumbai Serve" |
| Mythpat | [@Mythpat](https://www.youtube.com/@Mythpat) | 17,600,000 | 8,300,000 | 29 | 9.8x "when ACP plays AMONG US" |
| Payal Gaming | [@payalgaming](https://www.youtube.com/@PAYALGAMING) | 4,680,000 | 818,500 | 40 | 8.7x "Aur karo streamsnipe 🤣 #shortsfeed #payalgaming" |
| Snax Gaming | [@SnaxGaming](https://www.youtube.com/@SnaxGaming) | 2,670,000 | 452,000 | 40 | 8.4x "Age is just a number" |
| Meow16K | [@Meow16K](https://www.youtube.com/@Meow16k) | 62,100 | 4,200 | 40 | 8.3x "Game khelneka sahi waqt konsa hai dosto? 🙂‍↕️ #ind" |
| GamerFleet | [@GamerFleet](https://www.youtube.com/@GamerFleet) | 6,050,000 | 1,400,000 | 40 | 7.9x "FUNNIEST MEMES OF SOURAV JOSHI VLOGS😂" |
| 8bit Binks69 | [@8bitBinks69](https://www.youtube.com/@8bitBinks69) | 380,000 | 36,500 | 40 | 7.5x "The 3000$ Challenge 😱😱🤑💸💸" |
| AMIT FF 2.0 | [@amitff2.077](https://www.youtube.com/@amitff2.077) | 1,160,000 | 4,550,000 | 24 | 7.2x "Free Fire Ek Real Zindagi // Comedy Video / AMIT F" |
| Rite2Ace | [@Rite2Ace](https://www.youtube.com/@rite2ace) | 33,900 | 3,250 | 40 | 6.8x "Sometimes failure leads to success. You can't clut" |
| CarryisLive | [@CarryisLive](https://www.youtube.com/@CarryisLive) | 12,700,000 | 931,000 | 79 | 6.7x "THIS IS NOT A GAME 🤯" |
| ShreeMan Legend Live | [@shreemanlegendliveofficial](https://www.youtube.com/@shreemanlegendliveofficial) | 2,530,000 | 331,000 | 71 | 6.6x "Has Has ke Thakna Hai ? / Pura IGC Ek ZOO Me 😂" |
| NOOB NAWAB YT | [@noob_nawab_yt](https://www.youtube.com/@noob_nawab_yt) | 3,100 | 18,000 | 21 | 6.6x "Raju Kalakar #viralvideo #art #rajukalakar #virals" |
| Total Gaming | [@TotalGaming093](https://www.youtube.com/@TotalGaming093) | 45,900,000 | 16,000,000 | 40 | 6.2x "EASY 999 IQ MOMENT [SOLO VS SQUAD] / GARENA FREE F" |
| HydraFlick | [@HydraFlick](https://www.youtube.com/@HydraFlick) | 351,000 | 22,000 | 40 | 6.0x "Punish Opponents with IQ #shorts #valorant" |
| SauraXD | [@SauraXD](https://www.youtube.com/@SauraXD) | 244,000 | 317,000 | 40 | 6.0x "Valorant Ranked Hits Differently At 3am" |
| Tonde Gamer | [@TondeGamer](https://www.youtube.com/@TondeGamer) | 19,700,000 | 1,700,000 | 40 | 5.9x "Hecker hai Bhai Hecker 🧐" |
| TheBrownVoid | [@TheBrownVoid](https://www.youtube.com/@TheBrownVoid) | 46,800 | 8,050 | 80 | 5.8x "Me trying to lurk 😂😅 #brownvoid #valorant #valoran" |
| DARK KILLER FF | [@darkkiller_ff1](https://www.youtube.com/@darkkiller_ff1) | 26,500 | 7,800 | 40 | 5.8x "#nobatidao" |
| Bhupesh | [@bhupeshyt](https://www.youtube.com/@bhupeshyt) | 86,800 | 9,950 | 80 | 5.7x "GTA 5 BIKE RACES ARE CRAZY" |
| SenpaiVerse | [@SenpaiVersee](https://www.youtube.com/@SenpaiVersee) | 497,000 | 442,000 | 35 | 5.7x "Poppy Playtime Chapter 5 (FULL GAME)" |
| Dedtox | [@Dedtox](https://www.youtube.com/@Dedtox) | 93,400 | 8,850 | 40 | 5.2x "Aesteromorphs Edit" |
| Xyaa | [@XyaaLive](https://www.youtube.com/@XyaaLive) | 755,000 | 87,000 | 40 | 4.9x "Tum ek kaam karo, Gaming ki tayyari shuru kar do! " |
| DEFUSED LIVE | [@defusedlive](https://www.youtube.com/@defusedlive) | 332,000 | 69,500 | 52 | 4.9x "ALOO MAT KHAO #shorts" |
| Hitesh KS | [@HiteshKS](https://www.youtube.com/@HiteshKS) | 798,000 | 206,500 | 40 | 4.8x "😮 Top 3 MAGIC TRICKS 😮 / Hitesh KS" |
| Kronten Gaming | [@KrontenGaming](https://www.youtube.com/@KrontenGaming) | 2,000,000 | 144,500 | 22 | 4.7x "AKELA SAMAJKE AAGAYE THE MUJE MARNE 😂😂 PHIR AAGE K" |
| BerzereX | [@BERZEREX](https://www.youtube.com/@BERZEREX) | 239 | 574 | 40 | 4.7x "Multi Wither #minecraft #wither #fight #phonk" |
| Fun With SRB YT | [@funwithsrbyt](https://www.youtube.com/@funwithsrbyt) | 1,210,000 | 983,500 | 40 | 4.5x "Gajini Be Like Dhulpet Naku Dulekkuva 🤭😂// @funwit" |
| Mr STUD SUJEET | [@studsujeet](https://www.youtube.com/@studsujeet) | 27,700 | 1,100 | 40 | 4.3x "GTA 6 Launch Trailer Breakdown: Everything New YOU" |
| Jonathan Gaming | [@JONATHANGAMINGYT](https://www.youtube.com/@JONATHANGAMINGYT) | 7,970,000 | 1,000,000 | 9 | 4.1x "NO ONE CAN DEFEAT YOU, UNTIL YOU YOURSELF ACCEPT Y" |
| Scout | [@officialscoutop](https://www.youtube.com/@officialscoutop) | 5,210,000 | 609,500 | 40 | 3.9x "Gile-shikve khaane ke waqt yaad hi nahi aate. ❤️🍽️" |
| No Pressure | [@NoPressure_cs](https://www.youtube.com/@NoPressure_cs) | 283 | 375 | 40 | 3.7x "Minecraft Bedwars ! / #minecraftshorts #minecraft " |
| Your Zack | [@itsyourszack](https://www.youtube.com/@itsyourszack) | 232,000 | 379,500 | 34 | 3.7x "Kamla Ne Dil Tod Diya 😭💔/ Playing Horror Game " |
| ShreeMan Highlights | [@shreeman31](https://www.youtube.com/@shreeman31) | 8,080 | 11,000 | 40 | 3.6x "Why Always Tiwari? 😂 #shorts #shreemanlegend" |
| RON GAMING | [@RONGAMING72](https://www.youtube.com/@RONGAMING72) | 4,580,000 | 125,000 | 40 | 3.6x "MOMO Plays BGMI On PC For The First Time 😂😂 #short" |
| Toxic Rock Gaming | [@rock-live90](https://www.youtube.com/@rock-live90) | 370,000 | 218,000 | 21 | 3.6x "Wait For New Glitch 😂 #bgmi #bgmishorts" |
| SenpaiUnlimited | [@SenpaiUnlimited](https://www.youtube.com/@SenpaiUnlimited) | 1,980,000 | 691,500 | 52 | 3.5x "I Got Kitsune and Yeti from Gifts in Blox Fruits #" |
| Fury Gaming | [@furygamin9](https://www.youtube.com/@furygamin9) | 74,000 | 26,000 | 40 | 3.5x "GAME OVER 💀" |
| Ujjwal | [@UjjwalGamer](https://www.youtube.com/@UjjwalGamer) | 12,800,000 | 7,350,000 | 40 | 3.3x "MY FIRST DAY IN NEW GANGSTER CITY" |
| TLS WARRIOR | [@TLSWARRIOR](https://www.youtube.com/@TLSWARRIOR) | 5,580,000 | 2,500,000 | 40 | 3.0x "EK GAREEB V BADGE YOUTUBER 💀😂 FREEFIRE FUNNY MOMEN" |
| SlayyPop | [@SlayyPop](https://www.youtube.com/@SlayyPop) | 3,280,000 | 3,350,000 | 40 | 2.8x "Find The School Topper / Sach ya Scam / SlayyPop" |
| Hitesh KS Hindi Gaming | [@HiteshKSHindiGaming](https://www.youtube.com/@HiteshKSHindiGaming) | 2,530,000 | 7,000 | 40 | 2.7x "🦆 Batak ne Bachey ko Dara diyaa 😂 / UNTITLED GOOSE" |
| Techno Gamerz | [@TechnoGamerzOfficial](https://www.youtube.com/@TechnoGamerzOfficial) | 53,400,000 | 9,850,000 | 40 | 2.6x "I STARTED MY OWN CAR BUSINESS / GTA 5 GAMEPLAY #16" |
| Triggered Insaan | [@TriggeredInsaan](https://www.youtube.com/@triggeredinsaan) | 27,000,000 | 16,000,000 | 39 | 2.6x "Ruchika and I became Parents for 24 Hours" |
| omzhp | [@omzhp](https://www.youtube.com/@omzhp) | 4,930 | 5,750 | 40 | 2.6x "Heavy Breather Mic Troll in Valorant" |
| Slayy Point | [@SlayyPointOfficial](https://www.youtube.com/@SlayyPointOfficial) | 10,600,000 | 14,000,000 | 40 | 2.6x "Testing India's Most Expensive Luxury Train" |
| Live Insaan | [@LiveInsaan](https://www.youtube.com/@liveinsaan) | 15,700,000 | 3,350,000 | 40 | 2.5x "Granny 3 Hot Air Balloon Escape karliya" |
| Tru Gaming | [@TruGaming001](https://www.youtube.com/@TruGaming001) | 324,000 | 1,300 | 40 | 2.0x "I barely managed to escape." |
| ProBoiz 95 | [@ProBoiz95](https://www.youtube.com/@ProBoiz95) | 9,360,000 | 8,450,000 | 40 | 1.8x "Minecraft But Every Drop is a Gun!" |
| Anshu Bisht | [@AnshuBisht](https://www.youtube.com/@AnshuBisht) | 8,090,000 | 2,450,000 | 40 | 1.5x "100 days but TREASURE CHEST ARE SUPER OP Minecraft" |
| RG's Chillin | [@rgschillin5069](https://www.youtube.com/@rgschillin5069) | n/a | n/a | 0 | not measured: handle not found or tab returned no view counts (27 Oct 2026) |
| ClutchGod | [@clutchgod960](https://www.youtube.com/@clutchgod960) | n/a | n/a | 0 | not measured: handle not found or tab returned no view counts (27 Oct 2026) |
| Desi Gamers | [@DesiGamers](https://www.youtube.com/@DesiGamers) | n/a | n/a | 0 | not measured: handle not found or tab returned no view counts (27 Oct 2026) |
| N3haL | [@N3hal](https://www.youtube.com/@N3hal) | n/a | n/a | 0 | not measured: handle not found or tab returned no view counts (27 Oct 2026) |
| Rengoku Gaming | [@Rengoku_Gamingofficial](https://www.youtube.com/@Rengoku_Gamingofficial) | n/a | n/a | 0 | not measured: handle not found or tab returned no view counts (27 Oct 2026) |
| Rachitroo | [@Rachitroo](https://www.youtube.com/@Rachitroo) | n/a | n/a | 0 | not measured: handle not found or tab returned no view counts (27 Oct 2026) |
| Joker Ki Haveli | [@JokerKiHaveli](https://www.youtube.com/@JokerKiHaveli) | n/a | n/a | 0 | not measured: handle not found or tab returned no view counts (27 Oct 2026) |
| Rawknee | [@RawkneeGaming](https://www.youtube.com/@RawkneeGaming) | n/a | n/a | 0 | not measured: handle not found or tab returned no view counts (27 Oct 2026) |
| 8bit Goldy | [@8bitGoldy](https://www.youtube.com/@8bitGoldy) | n/a | n/a | 0 | not measured: handle not found or tab returned no view counts (27 Oct 2026) |
| Crazy Deep | [@CrazyDeep](https://www.youtube.com/@CrazyDeep) | n/a | n/a | 0 | not measured: handle not found or tab returned no view counts (27 Oct 2026) |

## Confidence
Medium on the shape findings, low on timing. 3,785 videos across 89 channels with medians of 1,000+ (3,905 across 92 in total) is a real sample for 'what over-indexes': G11 Viewer Task (10/32 over 3x), G13 Pop-Culture Mashup (13/41), G4 in long-form (13/71) and the Part/Episode null result (0/47) are findings; most other G-formulas sit within a few points of the 12% Shorts baseline and are not. Limits: (1) hooks are titles, not the spoken first line or the first frame; YouTube's bot wall stopped per-video fetches after 11 videos and captions were not attempted, so the visual hook (what actually decides a Short) is unmeasured. (2) Only 11 outliers are dated; 'viral now' leans on feed position and on brain/research/reports/2026-10-27.md, so treat the 'until' dates as estimates. (3) Multiples include an age effect (older videos had longer to grow). (4) Instagram: web search returned no public reel URLs for these creators (only profile pages, which we did not open), so the Instagram corpus is zero and profile scores use YouTube pages plus search snippets; 40 of 100 rubric points are unobservable. (5) G-formula matching is regex on Hinglish titles and will misfile some rows; 788 Shorts stayed unclassified. (6) Few accounts are within 10x of Srijan's size (928 IG followers); the closest are Salty Boys, Lmaoo Noob, RishYT, No Pressure, BerzereX, Half Skirmish.
