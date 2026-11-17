"""Loudness spikes (screams, laughs, explosions) per 5s window - a free 'emotion' signal like Opus Clip uses."""
import array, math, subprocess

def loudness_map(path, window=5, rate=8000):
    """Return {window_index: bonus 0..3} for windows that are much louder than the stream's average."""
    p = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-i", path, "-vn", "-ac", "1", "-ar", str(rate),
                          "-f", "s16le", "-"], stdout=subprocess.PIPE)
    chunk = rate * window * 2
    rms = []
    while True:
        b = p.stdout.read(chunk)
        if not b:
            break
        a = array.array("h", b[: len(b) // 2 * 2])
        rms.append(math.sqrt(sum(x * x for x in a) / max(len(a), 1)))
    p.wait()
    if len(rms) < 2:
        return {}
    mean = sum(rms) / len(rms)
    sd = math.sqrt(sum((r - mean) ** 2 for r in rms) / len(rms)) or 1
    return {i: round(min(3.0, (r - mean) / sd), 2) for i, r in enumerate(rms) if r > mean + sd}
