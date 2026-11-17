"""Transcription via faster-whisper (optional dependency). Output: list of segments."""
import json, sys

def transcribe(path, model="small", out=None):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        sys.exit("pip install faster-whisper  (or supply a transcript JSON with --transcript)")
    m = WhisperModel(model, compute_type="int8")
    segs, _ = m.transcribe(path, word_timestamps=True, vad_filter=True)
    data = [{"start": s.start, "end": s.end, "text": s.text.strip(),
             "words": [{"w": w.word.strip(), "start": w.start, "end": w.end} for w in (s.words or [])]}
            for s in segs]
    if out:
        json.dump(data, open(out, "w"), indent=1)
    return data
