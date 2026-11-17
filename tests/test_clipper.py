from clipper.select import candidates
from clipper.render import make_ass

SEGS = [{"start": i * 6.0, "end": i * 6.0 + 5, "text": t, "words": []} for i, t in enumerate(
    ["just chilling", "wait no way the GTA 6 trailer easter egg is insane!", "okay moving on",
     "so anyway", "walking", "driving", "idle talk", "more idle"])]

def test_hype_window_ranks_first():
    c = candidates(SEGS)
    assert "easter egg" in c[0]["text"]

def test_no_overlap():
    c = candidates(SEGS)
    for a in c:
        for b in c:
            if a is not b:
                assert a["end"] <= b["start"] or a["start"] >= b["end"]

def test_ass_written(tmp_path):
    p = tmp_path / "x.ass"
    make_ass([{"w": "hi", "start": 10, "end": 10.5}, {"w": "there", "start": 10.5, "end": 11}], 9.0, str(p))
    t = p.read_text()
    assert "HI" in t and "THERE" in t and "0:00:01.00" in t

def test_virality_and_reasons():
    c = candidates(SEGS)[0]
    assert 0 < c["virality"] <= 100 and "strong hook" in c["why"]

def test_word_highlight_and_hook(tmp_path):
    p = tmp_path / "y.ass"
    make_ass([{"w": "no", "start": 1, "end": 1.3}, {"w": "way", "start": 1.3, "end": 1.6}], 0, str(p), hook="Wait for it")
    t = p.read_text()
    assert t.count("Dialogue: 0,") == 2 and "\\c&H00E6FF&" in t and "WAIT FOR IT" in t
