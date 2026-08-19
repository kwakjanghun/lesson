# -*- coding: utf-8 -*-
"""씬 생성 공통 헬퍼 — 챕터별 gen_scenes.py가 import해서 쓴다.

    from scene_helpers import *   # win/local/seg_end/code_scene/steps_scene/full_code_scene ...

타이밍(win/local/seg_end)은 import 시점에 timing.json을 읽어 계산된다.
팔레트: CYAN/AMBER/PINK/GREEN/PURPLE/GOLD — 파일이 바뀔 때마다 acc= 로 바꾼다.
"""
import json, os, html

ROOT = os.path.join(os.path.dirname(__file__), "..")
T = json.load(open(os.path.join(ROOT, "assets", "narration", "timing.json"), encoding="utf-8"))
TOTAL = T["total"]
SC = {s["id"]: s for s in T["scenes"]}
ORDER = [s["id"] for s in T["scenes"]]
LEAD = 0.6

win = {}
for i, sid in enumerate(ORDER):
    start = 0.0 if i == 0 else round(SC[sid]["start"] - LEAD, 2)
    end = TOTAL if i == len(ORDER) - 1 else round(SC[ORDER[i + 1]]["start"] - LEAD, 2)
    win[sid] = (start, round(end - start, 2))

def local(sid, k):
    return round(SC[sid]["segs"][k]["start"] - win[sid][0], 2)

def seg_end(sid, k):
    g = SC[sid]["segs"][k]
    return round(g["start"] + g["dur"] - win[sid][0], 2)

NL = chr(10)
CYAN   = ("#4ce0d2", "76,224,210")
AMBER  = ("#ffb454", "255,180,84")
PINK   = ("#ff6ec7", "255,110,199")
GREEN  = ("#8aff80", "138,255,128")
PURPLE = ("#b28bff", "178,139,255")
GOLD   = ("#d4af37", "212,175,55")

def common_css(acc):
    a, rgb = acc
    return f"""
        @font-face {{
          font-family: "Pretendard";
          src: url("assets/fonts/PretendardVariable.woff2") format("woff2-variations");
          font-weight: 45 920;
          font-style: normal;
        }}
        #root {{ position: absolute; inset: 0; font-family: "Pretendard", sans-serif; color: #eaf0ff; }}
        #body {{ position: absolute; inset: 0; }}
        #head {{ position: absolute; left: 0; right: 0; top: 90px; text-align: center; opacity: 0; will-change: transform; }}
        #head .badge {{ display: inline-block; font-family: "JetBrains Mono", monospace; font-size: 30px; font-weight: 700;
          color: #0b1026; background: {a}; border-radius: 999px; padding: 8px 30px; margin-bottom: 18px; }}
        #head .name {{ display: block; font-size: 68px; font-weight: 900; letter-spacing: -0.03em; }}
        .codebox {{ position: absolute; left: 120px; top: 300px; width: 1000px; border-radius: 20px;
          border: 2px solid rgba(143,160,196,0.35); background: rgba(5,7,15,0.65); padding: 40px 0; opacity: 0; will-change: transform; }}
        .cl {{ display: block; font-family: "JetBrains Mono", monospace; font-size: 33px; line-height: 1.75;
          color: #eaf0ff; padding: 2px 46px; border-left: 8px solid rgba(0,0,0,0); white-space: pre; }}
        .cl i {{ font-style: normal; color: #8fa0c4; }}
        .cap {{ position: absolute; left: 1200px; top: 340px; width: 580px; border-radius: 20px;
          border: 2px solid rgba({rgb},0.5); background: rgba({rgb},0.06); padding: 36px 40px;
          font-size: 40px; font-weight: 700; line-height: 1.5; letter-spacing: -0.02em; opacity: 0; will-change: transform; }}
        .cap b {{ font-weight: 700; color: {a}; }}
"""

SHELL = """<!doctype html>
<html lang="ko">
  <head>
    <meta charset="UTF-8" />
  </head>
  <body>
    <template>
      <style>
%%CSS%%
      </style>

      <div id="root" data-composition-id="%%SID%%" data-width="1920" data-height="1080">
        <div id="body">
%%BODY%%
        </div>
      </div>

      <script>
        (function () {
          window.__timelines = window.__timelines || {};
          const tl = gsap.timeline({ paused: true });
%%JS%%
          window.__timelines["%%SID%%"] = tl;
        })();
      </script>
    </template>
  </body>
</html>
"""

ENTRY_JS = ('          tl.fromTo("#body", {x:150, opacity:0}, '
            '{x:0, opacity:1, duration:0.55, ease:"power3.out"}, 0);' + NL)

def write_scene(sid, css, body, js, first=False, acc=CYAN):
    entry = "" if first else ENTRY_JS
    out = (SHELL.replace("%%SID%%", sid).replace("%%CSS%%", common_css(acc) + css)
           .replace("%%BODY%%", body).replace("%%JS%%", entry + js))
    open(os.path.join(ROOT, "compositions", f"{sid}.html"), "w", encoding="utf-8").write(out)

def head_js(t=0.4):
    return (f'          tl.fromTo("#head", {{opacity:0, y:30}}, '
            f'{{opacity:1, y:0, duration:0.7, ease:"power3.out"}}, {t});' + NL)

def fade_js(sid, last=False):
    if last:
        return ""
    t = round(win[sid][1] - 0.45, 2)
    return (f'          tl.to("#body", {{x:-190, opacity:0, duration:0.45, '
            f'ease:"power3.in"}}, {t});' + NL)

def code_scene(sid, badge, title, lines, segs, first_seg_no_hl=False, acc=CYAN, font=33, top=300):
    a, rgb = acc
    css = f"""
        .codebox {{ top: {top}px; }}
        .cl {{ font-size: {font}px; }}
        .cap {{ top: {top + 40}px; }}
"""
    body = f"""          <div id="head">
            <span class="badge">{badge}</span>
            <span class="name">{title}</span>
          </div>
          <div class="codebox" id="code">
"""
    for i, ln in enumerate(lines):
        body += f'            <span class="cl" id="ln{i}">{ln}</span>' + NL
    body += "          </div>" + NL
    for k, (_, cap) in enumerate(segs):
        body += f'          <div class="cap" id="cap{k}">{cap}</div>' + NL

    js = head_js()
    js += '          tl.fromTo("#code", {opacity:0, y:40}, {opacity:1, y:0, duration:0.7, ease:"power3.out"}, 1.0);' + NL
    step = round(min(0.06, 0.5 / max(len(lines), 1)), 3)
    for i in range(len(lines)):
        js += (f'          tl.fromTo("#ln{i}", {{opacity:0, x:24}}, '
               f'{{opacity:1, x:0, duration:0.4, ease:"power4.out"}}, {round(1.15 + i * step, 2)});' + NL)
    prev = []
    for k, (idxs, _) in enumerate(segs):
        t = max(local(sid, k), 2.0)
        if k > 0:
            pt = round(t - 0.35, 2)
            js += (f'          tl.to("#cap{k-1}", {{opacity:0, y:-16, duration:0.35, '
                   f'ease:"power2.in"}}, {pt});' + NL)
            if prev and idxs != prev:
                sel = ",".join(f'"#ln{i}"' for i in prev)
                js += (f'          tl.to([{sel}], {{backgroundColor:"rgba(0,0,0,0)", '
                       f'borderLeftColor:"rgba(0,0,0,0)", duration:0.3}}, {pt});' + NL)
        if idxs and not (k == 0 and first_seg_no_hl):
            sel = ",".join(f'"#ln{i}"' for i in idxs)
            js += (f'          tl.to([{sel}], {{backgroundColor:"rgba({rgb},0.12)", '
                   f'borderLeftColor:"{a}", duration:0.35}}, {t});' + NL)
        js += (f'          tl.fromTo("#cap{k}", {{opacity:0, x:40}}, '
               f'{{opacity:1, x:0, duration:0.5, ease:"power3.out"}}, {round(t+0.15,2)});' + NL)
        if idxs:
            prev = idxs
    js += fade_js(sid)
    write_scene(sid, css, body, js, acc=acc)

def steps_scene(sid, badge, title, steps, acc=AMBER):
    """세그먼트 시각에 맞춰 단계 카드가 하나씩 등장하고, 지난 카드는 흐려진다."""
    a, rgb = acc
    n = len(steps)
    css = f"""
        #steps {{ position:absolute; left: 160px; right: 160px; top: 320px; }}
        .st {{ display:flex; align-items:flex-start; gap: 34px; border-radius: 20px;
          border: 2px solid rgba(143,160,196,0.3); background: rgba(234,240,255,0.03);
          padding: 30px 40px; margin-bottom: 26px; opacity: 0; will-change: transform; }}
        .st .no {{ flex: 0 0 auto; font-family:"JetBrains Mono", monospace; font-size: 40px; font-weight: 700;
          color: #0b1026; background: {a}; border-radius: 999px; width: 68px; height: 68px;
          display:flex; align-items:center; justify-content:center; }}
        .st .tx {{ flex: 1 1 auto; font-size: 40px; font-weight: 700; line-height: 1.45; letter-spacing:-0.02em; padding-top: 8px; }}
        .st .tx small {{ display:block; font-size: 32px; font-weight: 300; color:#8fa0c4; margin-top: 10px; }}
        .st b {{ color: {a}; }}
"""
    body = f"""          <div id="head">
            <span class="badge">{badge}</span>
            <span class="name">{title}</span>
          </div>
          <div id="steps">
"""
    for i, s in enumerate(steps):
        body += f'            <div class="st" id="st{i}"><span class="no">{i+1}</span><span class="tx">{s}</span></div>' + NL
    body += "          </div>" + NL

    js = head_js()
    for k in range(n):
        t = max(local(sid, k), 1.2)
        js += (f'          tl.fromTo("#st{k}", {{opacity:0, y:40}}, '
               f'{{opacity:1, y:0, duration:0.6, ease:"back.out(1.4)"}}, {t});' + NL)
        if k > 0:
            # 0.4까지 내리면 보조 텍스트 대비가 3:1 아래로 떨어진다 (check 경고)
            js += (f'          tl.to("#st{k-1}", {{opacity:0.62, duration:0.4}}, {t});' + NL)
    js += fade_js(sid)
    write_scene(sid, css, body, js, acc=acc)

def full_code_scene(sid, badge, title, lines, cap_html, acc=CYAN, font=26, top=250):
    a, rgb = acc
    line_h = round(font * 1.55 + 2, 1)
    css = f"""
        .codebox {{ top: {top}px; width: 1060px; padding: 30px 0; }}
        .cl {{ font-size: {font}px; line-height: 1.55; padding: 1px 40px; }}
        #scan {{ position: absolute; left: 120px; top: {top + 30}px; width: 1060px; height: {line_h}px; border-radius: 6px;
          background: rgba({rgb},0.10); border-left: 8px solid {a}; opacity: 0; will-change: transform; }}
        .cap {{ top: 320px; }}
"""
    body = f"""          <div id="head">
            <span class="badge">{badge}</span>
            <span class="name">{title}</span>
          </div>
          <div class="codebox" id="code">
"""
    for i, ln in enumerate(lines):
        body += f'            <span class="cl" id="ln{i}">{ln}</span>' + NL
    body += f"""          </div>
          <div id="scan" data-layout-allow-overlap></div>
          <div class="cap" id="cap0">{cap_html}</div>
"""
    n = len(lines)
    dur = win[sid][1]
    js = head_js()
    js += '          tl.fromTo("#code", {opacity:0, y:30}, {opacity:1, y:0, duration:0.5, ease:"power3.out"}, 0.8);' + NL
    step = round(min(0.06, 1.2 / max(n, 1)), 3)
    for i in range(n):
        js += (f'          tl.fromTo("#ln{i}", {{opacity:0, x:26}}, '
               f'{{opacity:1, x:0, duration:0.4, ease:"power4.out"}}, {round(1.0 + i * step, 2)});' + NL)
    scan_start = round(1.2 + n * step + 0.6, 2)
    scan_dur = round(max(dur - scan_start - 1.6, 2.0), 2)
    js += f'          tl.to("#scan", {{opacity:1, duration:0.3}}, {scan_start});' + NL
    js += (f'          tl.to("#scan", {{y: {round(line_h * (n - 1), 1)}, '
           f'duration: {scan_dur}, ease:"none"}}, {round(scan_start + 0.3, 2)});' + NL)
    js += f'          tl.to("#scan", {{opacity:0, duration:0.3}}, {round(scan_start + 0.3 + scan_dur, 2)});' + NL
    js += '          tl.fromTo("#cap0", {opacity:0, x:40}, {opacity:1, x:0, duration:0.5, ease:"power3.out"}, 2.4);' + NL
    js += fade_js(sid)
    write_scene(sid, css, body, js, acc=acc)

