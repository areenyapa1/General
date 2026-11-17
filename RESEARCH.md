# Research: what already works in clipping (Nov 2026)

## Money (Whop Content Rewards = main clipping marketplace)
- Median listed rate ~ $1 per 1,000 verified views (~700 live campaigns); typical $0.50-1.50, rare outliers higher.
- ~10% platform fee; paid only for approved clips + verified views; campaigns end when budget runs out.
- YouTube Shorts median slightly higher (~$1.4/1k) than TikTok/IG (~$1-1.2/1k).
- Math: 1M views/month ~ $1,000. Volume x hit-rate is the business -> automation matters.

## Paid tools (what they sell)
- Opus Clip: 0-100 virality score (hook + emotional peaks + trend fit), face-tracked reframe, animated captions.
- Klap: several clip options per video with scores, learns from which you pick.
- Vizard: cheaper, more clips per dollar, many caption languages.

## Open-source (free, MIT) we can borrow from
- OpenShorts (mutonby/openshorts): MediaPipe/YOLO face tracking reframe, blurred-bg mode, faster-whisper captions.
- AI-Youtube-Shorts-Generator, yt-short-clipper, OpenClip: LLM highlight detection, word-by-word captions.
- Postiz (open-source scheduler) publishes to TikTok/YT/IG/X - for Stage 3 auto-posting.

## What we adopted (done)
- 0-100 virality score with reasons (hook, hype, GTA 6 trend fit, audio spikes, length) in manifest.json.
- Audio loudness spikes as free "emotional peak" signal.
- Word-by-word highlighted captions (CapCut/Opus style) + hook title for first 3s.
- Blurred-background 9:16 (same as OpenShorts GENERAL mode).

## Next improvements (in order)
1. Facecam detection -> streamer face on top, gameplay below (GTA streams' best-performing layout).
2. Use YouTube/Twitch auto-captions when available (skip Whisper -> much faster/free-er).
3. Feedback loop: log views per clip, re-weight scoring toward winners (Klap-style learning).
4. Postiz/YouTube API auto-posting once clips prove they get views.
