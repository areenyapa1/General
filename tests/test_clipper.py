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
    assert "HI THERE" in p.read_text() and "0:00:01.00" in p.read_text()
