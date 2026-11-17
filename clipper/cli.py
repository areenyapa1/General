"""Usage:
  python -m clipper.cli run VIDEO_OR_URL --streamer NAME [--transcript t.json] [--top 8] [--layout stack|fill] [--out clips/]
Writes clips + manifest.json (title, source credit, timestamps) for your review queue."""
import argparse, json, os
from .transcribe import transcribe
from .select import candidates, rerank_with_claude
from .render import render
from .fetch import fetch

def run(a):
    if a.video.startswith('http'):
        a.video = fetch(a.video)
    segs = json.load(open(a.transcript)) if a.transcript else transcribe(a.video, out=a.video + ".transcript.json")
    picks = rerank_with_claude(candidates(segs), top=a.top)
    words = [w for s in segs for w in s.get("words", [])]
    os.makedirs(a.out, exist_ok=True)
    manifest = []
    for n, c in enumerate(picks, 1):
        f = os.path.join(a.out, f"{a.streamer}_{n:02d}.mp4")
        render(a.video, c["start"], c["end"], f, words=words, layout=a.layout,
               credit=f"via @{a.streamer}" if a.streamer else None)
        manifest.append({"file": f, "start": c["start"], "end": c["end"], "score": c["score"],
                         "title": c.get("title") or c["text"][:60], "source": a.streamer, "status": "review"})
    json.dump(manifest, open(os.path.join(a.out, "manifest.json"), "w"), indent=1)
    print(f"{len(manifest)} clips -> {a.out}/manifest.json")

def main():
    p = argparse.ArgumentParser(); sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run"); r.add_argument("video"); r.add_argument("--streamer", default="")
    r.add_argument("--transcript"); r.add_argument("--top", type=int, default=8)
    r.add_argument("--layout", default="stack"); r.add_argument("--out", default="clips")
    r.set_defaults(fn=run)
    a = p.parse_args(); a.fn(a)

if __name__ == "__main__":
    main()
