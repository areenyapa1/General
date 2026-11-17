"""Pick clip-worthy moments. Heuristic scoring by default; optional Claude re-rank."""
import json, os, re

HYPE = re.compile(r"\b(no way|what the|bro|oh my god|omg|insane|crazy|clip (that|it)|"
                  r"let'?s go|holy|wait|are you serious|got me|dead|ruined|rockstar|gta|"
                  r"wasted|busted|wanted|helicopter|heist|chase|cop|police|funniest)\b", re.I)

def _score(text, dur, loudness=0.0):
    s = len(HYPE.findall(text)) * 2.0
    s += text.count("!") * 0.5 + text.count("?") * 0.3
    s += loudness
    if dur < 12 or dur > 75:        # shorts sweet spot 15-60s
        s -= 3
    return s

def candidates(segments, min_len=18, max_len=55, loudness=None):
    """Slide a window over transcript segments; return scored windows (no overlap)."""
    wins = []
    for i, a in enumerate(segments):
        txt, end = a["text"], a["end"]
        for b in segments[i:]:
            end, txt = b["end"], (txt + " " + b["text"]) if b is not a else a["text"]
            dur = end - a["start"]
            if dur >= min_len:
                ld = (loudness or {}).get(int(a["start"] // 5), 0.0)
                wins.append({"start": a["start"], "end": end, "text": txt, "score": _score(txt, dur, ld)})
            if dur >= max_len:
                break
    wins.sort(key=lambda w: -w["score"])
    picked = []
    for w in wins:
        if all(w["end"] <= p["start"] or w["start"] >= p["end"] for p in picked):
            picked.append(w)
    return picked

def rerank_with_claude(cands, top=10, model="claude-sonnet-5-5"):
    """Ask Claude for a hook title + viral score per candidate. Needs ANTHROPIC_API_KEY."""
    if not os.environ.get("ANTHROPIC_API_KEY"):
        return cands[:top]
    import anthropic
    client = anthropic.Anthropic()
    pool = cands[:top * 3]
    prompt = ("You pick viral short-form clips from GTA 6 streams. For each numbered candidate return JSON "
              "list [{\"i\":n,\"score\":0-10,\"title\":\"<=8 word hook\"}]. Prefer self-contained, funny, "
              "shocking, or skillful moments. JSON only.\n\n" +
              "\n".join(f"{i}: {c['text'][:400]}" for i, c in enumerate(pool)))
    r = client.messages.create(model=model, max_tokens=2000, messages=[{"role": "user", "content": prompt}])
    try:
        ranks = json.loads(r.content[0].text)
    except Exception:
        return cands[:top]
    for x in ranks:
        pool[x["i"]].update(score=x["score"], title=x.get("title", ""))
    return sorted(pool, key=lambda c: -c["score"])[:top]
