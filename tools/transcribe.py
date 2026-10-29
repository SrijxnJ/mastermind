import os
import sys, json
from faster_whisper import WhisperModel
m = WhisperModel(sys.argv[2] if len(sys.argv)>2 else "small", device="cpu", compute_type="int8", download_root=os.path.expanduser("~/sm-tools/models/whisper"))
segs, info = m.transcribe(sys.argv[1], word_timestamps=True, vad_filter=True)
out=[]
for s in segs:
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text.strip()}")
    out.append({"start":s.start,"end":s.end,"text":s.text.strip(),"words":[{"w":w.word,"s":w.start,"e":w.end} for w in s.words]})
json.dump({"lang":info.language,"segments":out}, open(sys.argv[1]+".words.json","w"), indent=1)
