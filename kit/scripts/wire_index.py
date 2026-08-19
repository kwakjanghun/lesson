# -*- coding: utf-8 -*-
"""gen_scenes.py가 만든 slots.html을 index.html에 배선한다.

- 예시 씬 슬롯(el-s1 블록 + 주석 처리된 el-s2 블록)을 실제 슬롯들로 교체
- 루트 data-duration / const TOTAL 을 timing.json의 total로
- <!--AUDIO-SLOT--> 을 narration.mp3 오디오 태그로
"""
import json, os, re

ROOT = os.path.join(os.path.dirname(__file__), "..")
T = json.load(open(os.path.join(ROOT, "assets", "narration", "timing.json"), encoding="utf-8"))
TOTAL = T["total"]

slots = open(os.path.join(ROOT, "scripts", "slots.html"), encoding="utf-8").read()
p = os.path.join(ROOT, "index.html")
s = open(p, encoding="utf-8").read()

# 1) 예시 씬 슬롯 + 주석 블록을 실제 슬롯으로 교체
start = s.index('      <div\n        id="el-s1"')
end = s.index("      <div id=\"fade-out\"></div>")
s = s[:start] + slots + "\n" + s[end:]

# 2) 길이
s = re.sub(r'(id="root"[\s\S]*?data-duration=")[\d.]+(")', lambda m: m.group(1) + str(TOTAL) + m.group(2), s, count=1)
s = re.sub(r"const TOTAL = [\d.]+;", f"const TOTAL = {TOTAL};", s, count=1)

# 3) 오디오
audio = ('<audio\n        id="narration"\n        src="assets/narration.mp3"\n'
         '        data-start="0"\n        data-duration="%s"\n        data-volume="1"\n      ></audio>' % TOTAL)
s = s.replace("<!--AUDIO-SLOT-->", audio, 1)

open(p, "w", encoding="utf-8").write(s)
print("wired. TOTAL =", TOTAL)
print("scenes  =", len(T["scenes"]))
