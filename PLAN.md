# GTA 6 Clipping Business Plan

Launch: Nov 19, 2026 (PS5/Xbox). Clip demand peaks in the first 2-3 weeks. Speed matters most.

## Revenue streams (run all three in parallel)
1. **Pay-per-view campaigns** - streamers/brands post clip bounties (Whop, Vyro, creator Discords).
   Typical $0.5-3 per 1k views; needs approval + consistent posting. Fastest cash.
2. **Own multi-platform clip channels** - TikTok, YouTube Shorts, IG Reels, X. Monetize via
   YT Partner / TikTok Creator Rewards (need eligibility), affiliate links, sponsorships.
3. **Service for streamers** - $200-1,500/mo retainers or per-clip fees. Highest ceiling, needs outreach.

## Rules that protect the business
- Only clip streamers who allow it (public clip policy, campaign terms, or written OK). Credit them.
- Add commentary/captions/edits - transformative content survives platform "unoriginal" filters.
- Never buy/bot views: campaigns audit and ban.
- Human review of every clip before posting (manifest.json status field).

## Week 1 checklist
- [ ] Create @handles on TikTok/YT/IG/X (same name), one niche: GTA 6 funny/chase/glitch moments.
- [ ] Join Whop + 3-5 streamer Discords; apply to every open GTA 6 campaign.
- [ ] DM 30 small/mid GTA streamers (500-5k viewers) offering free clips for 1 week -> convert to retainer.
- [ ] Run pipeline on VODs same day; post 3-5 clips/day/platform.
- [ ] Track views per clip in a sheet; double down on top formats.

## Pipeline
`python -m clipper.cli run VOD.mp4 --streamer NAME --top 8` -> ranked 9:16 captioned clips + manifest.json
(Whisper transcript -> heuristic/Claude moment scoring -> ffmpeg render). Set ANTHROPIC_API_KEY for AI ranking.
Higgsfield (AI video) can be added later for intros/b-roll; not needed for clipping itself.
