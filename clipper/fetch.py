"""Download a YouTube/Twitch/Kick video or clip with yt-dlp (free). Returns local file path."""
import subprocess, sys

def fetch(url, outdir="downloads", max_height=1080):
    out = subprocess.run(
        ["yt-dlp", "-f", f"bv*[height<={max_height}]+ba/b[height<={max_height}]/b", "--merge-output-format", "mp4",
         "-o", f"{outdir}/%(id)s.%(ext)s", "--print", "after_move:filepath", "--no-simulate", url],
        capture_output=True, text=True)
    if out.returncode:
        sys.exit(out.stderr.strip()[-500:])
    return out.stdout.strip().splitlines()[-1]
