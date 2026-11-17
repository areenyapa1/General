"""ffmpeg render: 16:9 stream -> 9:16. Layout 'stack' = blurred bg + centered gameplay;
'fill' = center-crop. Burns captions (ASS) and an optional credit line."""
import os, subprocess, tempfile

def _ts(t):
    h, m = int(t // 3600), int(t % 3600 // 60)
    return f"{h}:{m:02d}:{t % 60:05.2f}"

def make_ass(words, clip_start, path, per_line=3):
    hdr = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\n\n[V4+ Styles]\n"
           "Format: Name,Fontname,Fontsize,PrimaryColour,OutlineColour,BorderStyle,Outline,Shadow,Alignment,MarginV\n"
           "Style: Default,DejaVu Sans,88,&H00FFFFFF,&H00000000,1,6,0,2,520\n\n[Events]\n"
           "Format: Layer,Start,End,Style,Text\n")
    lines = []
    for i in range(0, len(words), per_line):
        g = words[i:i + per_line]
        lines.append(f"Dialogue: 0,{_ts(g[0]['start'] - clip_start)},{_ts(g[-1]['end'] - clip_start)},Default,"
                     + " ".join(w["w"].upper() for w in g).replace("\n", " "))
    open(path, "w").write(hdr + "\n".join(lines) + "\n")

def render(src, start, end, out, words=None, layout="stack", credit=None):
    dur = end - start
    if layout == "fill":
        vf = "crop=ih*9/16:ih,scale=1080:1920"
    else:
        vf = ("split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30[bg];"
              "[b]scale=1080:-2[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2")
    tmp = None
    if words:
        tmp = tempfile.NamedTemporaryFile("w", suffix=".ass", delete=False).name
        make_ass([w for w in words if start <= w["start"] < end], start, tmp)
        vf += f",ass={tmp}"
    if credit:
        vf += (",drawtext=text='%s':fontcolor=white@0.8:fontsize=36:x=(w-text_w)/2:y=h-120" % credit.replace("'", ""))
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{start:.2f}", "-t", f"{dur:.2f}", "-i", src,
           "-vf", vf, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-c:a", "aac", "-b:a", "160k",
           "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    if tmp:
        os.unlink(tmp)
    return out
