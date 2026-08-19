# -*- coding: utf-8 -*-
"""통합과학2 Ⅲ-1 화학 변화 ① 산화와 환원 — 개념 씬 10개 + index 슬롯 생성.
timing.json(실측 TTS 타이밍)을 읽어 세그먼트 시각에 요소가 등장한다."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from scene_helpers import *  # win/local/seg_end/write_scene/head_js/fade_js/palettes/ROOT/ORDER/TOTAL

def head(badge, title):
    return f"""          <div id="head">
            <span class="badge">{badge}</span>
            <span class="name">{title}</span>
          </div>
"""

def app(sel, t, y=36, d=0.6, ease="back.out(1.4)"):
    return (f'          tl.fromTo("{sel}", {{opacity:0, y:{y}}}, '
            f'{{opacity:1, y:0, duration:{d}, ease:"{ease}"}}, {t});' + NL)

def dim(sel, t, to=0.55):
    return f'          tl.to("{sel}", {{opacity:{to}, duration:0.4}}, {t});' + NL

CARD = """
        .card { position:absolute; border-radius: 24px; border: 2px solid rgba(143,160,196,0.3);
          background: rgba(234,240,255,0.03); padding: 34px 40px; opacity: 0; will-change: transform; }
        .card h3 { font-size: 46px; font-weight: 900; letter-spacing:-0.03em; margin-bottom: 14px; }
        .card p { font-size: 34px; font-weight: 300; line-height: 1.5; color:#eaf0ff; }
        .card .eq { font-family:"JetBrains Mono", monospace; font-size: 34px; font-weight: 700; color:#eaf0ff;
          margin: 14px 0 10px; white-space: nowrap; }
        .card .tag { display:inline-block; font-size: 28px; font-weight: 700; border-radius: 999px; padding: 4px 18px; margin-right: 10px; margin-top: 6px; }
        .ox { color:#0b1026; background:#ff6ec7; }
        .rd { color:#0b1026; background:#4ce0d2; }
        .lbl { position:absolute; font-size: 30px; font-weight: 300; color:#8fa0c4; opacity:0; }
"""

# ─────────────────────────── s01 타이틀 ───────────────────────────
sid = "s01"
css = """
        #kicker { position:absolute; left:0; right:0; top: 300px; text-align:center; font-size: 40px; font-weight: 300; color:#8fa0c4; opacity:0; letter-spacing: 0.02em; }
        #title { position:absolute; left:0; right:0; top: 380px; text-align:center; font-size: 170px; font-weight: 900; letter-spacing:-0.04em; color:#4ce0d2; opacity:0; will-change: transform; }
        #sub { position:absolute; left:0; right:0; top: 620px; text-align:center; font-size: 52px; font-weight: 700; color:#eaf0ff; opacity:0; }
        #ring { position:absolute; left: 860px; top: 760px; width: 200px; height: 200px; opacity:0; }
        #ring svg { width:200px; height:200px; display:block; }
        #ring .orb { fill:#d4af37; }
        #ring .el { fill:#ff6ec7; }
        #ring .path { fill:none; stroke: rgba(143,160,196,0.5); stroke-width: 3; }
"""
body = """          <div id="kicker">통합과학 2 · Ⅲ. 변화와 다양성 · 1. 화학 변화</div>
          <div id="title">산화와 환원</div>
          <div id="sub">산소의 이동, 그리고 전자의 이동</div>
          <div id="ring">
            <svg viewBox="0 0 200 200">
              <circle class="path" cx="100" cy="100" r="80" />
              <circle class="orb" cx="100" cy="100" r="26" />
              <g id="orbit"><circle class="el" cx="180" cy="100" r="11" /></g>
            </svg>
          </div>
"""
js = app("#kicker", 0.5, y=20)
js += app("#title", 1.2, y=50, d=0.9, ease="power3.out")
js += app("#sub", 2.4, y=24)
js += app("#ring", 3.2, y=20)
dur = win[sid][1]
js += (f'          tl.to("#orbit", {{rotation: 360 * {max(1, int(dur // 4))}, svgOrigin:"100 100", duration:{round(dur,2)}, ease:"none"}}, 0);' + NL)
js += fade_js(sid)
write_scene(sid, css, body, js, first=True)

# ─────────────────────────── s02 산소 이동 정의 ───────────────────────────
sid = "s02"
css = CARD + """
        #ox { left: 160px; top: 330px; width: 700px; height: 330px; }
        #rd { left: 1060px; top: 330px; width: 700px; height: 330px; }
        #atom { position:absolute; left: 1330px; top: 560px; width: 110px; height: 110px; border-radius: 50%;
          background:#d4af37; color:#0b1026; font-weight: 900; font-size: 60px; display:flex; align-items:center; justify-content:center; opacity:0; will-change: transform; }
        #arrow { position:absolute; left: 700px; top: 585px; width: 520px; height: 60px; opacity:0; }
        #arrow svg { width:520px; height:60px; display:block; }
        #arrow path { fill:none; stroke:#d4af37; stroke-width:6; stroke-dasharray: 560; stroke-dashoffset: 560; }
        #arrow polygon { fill:#d4af37; }
        #sim { position:absolute; left:0; right:0; top: 760px; text-align:center; font-size: 64px; font-weight: 900; letter-spacing:-0.03em; color:#4ce0d2; opacity:0; will-change: transform; }
        #sim small { display:block; font-size: 34px; font-weight: 300; color:#8fa0c4; margin-top: 14px; letter-spacing: 0; }
"""
body = head("산소의 이동", "산화와 환원이란?") + """          <div class="card" id="ox"><h3 style="color:#ff6ec7">산화 <span style="font-weight:300;font-size:30px;color:#8fa0c4">Oxidation</span></h3><p>물질이 <b style="color:#ff6ec7">산소를 얻는</b> 반응</p></div>
          <div class="card" id="rd"><h3 style="color:#4ce0d2">환원 <span style="font-weight:300;font-size:30px;color:#8fa0c4">Reduction</span></h3><p>물질이 <b style="color:#4ce0d2">산소를 잃는</b> 반응</p></div>
          <div id="atom" data-layout-allow-overlap>O</div>
          <div id="arrow" data-layout-allow-overlap><svg viewBox="0 0 520 60"><path d="M500 30 L30 30" /><polygon points="40,14 8,30 40,46" /></svg></div>
          <div id="sim">산화와 환원은 항상 <u>동시에</u> 일어난다<small>한 물질이 산소를 잃으면(환원), 다른 물질이 그 산소를 얻는다(산화) — 동시성</small></div>
"""
t1, t2 = local(sid, 0), local(sid, 1)
js = head_js()
js += app("#ox", t1 + 0.8)
js += app("#rd", t1 + 2.6)
js += app("#atom", t2 + 0.2, y=0, d=0.4)
js += f'          tl.to("#arrow", {{opacity:1, duration:0.2}}, {t2 + 0.6});' + NL
js += f'          tl.to("#arrow path", {{strokeDashoffset: 0, duration: 1.2, ease:"power2.inOut"}}, {t2 + 0.6});' + NL
js += f'          tl.to("#atom", {{x: -880, duration: 1.6, ease:"power2.inOut"}}, {t2 + 0.8});' + NL
js += app("#sim", t2 + 3.2, y=30)
js += fade_js(sid)
write_scene(sid, css, body, js)

# ─────────────────────────── s03 역사를 바꾼 산화 환원 ───────────────────────────
sid = "s03"
css = CARD + """
        .card { left: 160px; width: 1600px; height: 190px; padding: 26px 40px; }
        .card h3 { display:inline-block; margin-right: 30px; vertical-align: middle; }
        .card .eq { display:inline-block; vertical-align: middle; font-size: 30px; margin: 0 24px 0 0; }
        .card .tags { display:inline-block; vertical-align: middle; }
        #c0 { top: 300px; } #c1 { top: 520px; } #c2 { top: 740px; }
"""
body = head("역사를 바꾼 반응", "자연과 인류를 바꾼 산화 환원") + """          <div class="card" id="c0"><h3 style="color:#d4af37">① 광합성</h3><span class="eq">물 + 이산화 탄소 → 포도당 + 산소</span><span class="tags"><span class="tag rd">이산화 탄소 환원</span><span class="tag ox">물 산화</span></span><p>엽록체에서 빛 에너지를 이용해 만든다</p></div>
          <div class="card" id="c1"><h3 style="color:#d4af37">② 화석 연료의 연소</h3><span class="eq">메테인 + 산소 → 이산화 탄소 + 물 + 에너지</span><span class="tags"><span class="tag ox">메테인 산화</span><span class="tag rd">산소 환원</span></span><p>산업과 교통의 에너지 — 인류의 삶이 풍요로워졌다</p></div>
          <div class="card" id="c2"><h3 style="color:#d4af37">③ 철의 제련</h3><span class="eq">산화 철(Ⅲ) + 일산화 탄소 → 철 + 이산화 탄소</span><span class="tags"><span class="tag rd">산화 철 환원</span><span class="tag ox">일산화 탄소 산화</span></span><p>철광석에서 순수한 철을 얻어 기구·건축물에 이용</p></div>
"""
js = head_js()
for k in range(3):
    t = local(sid, k) + 0.6
    js += app(f"#c{k}", t)
    if k > 0:
        js += dim(f"#c{k-1}", t, 0.6)
js += fade_js(sid)
write_scene(sid, css, body, js, acc=GOLD)

# ─────────────────────────── s04 실험 ───────────────────────────
sid = "s04"
css = CARD + """
        #exp { left: 160px; top: 300px; width: 820px; height: 620px; }
        #tube { position:absolute; left: 60px; top: 120px; width: 140px; height: 330px; border: 4px solid rgba(234,240,255,0.6); border-top:none; border-radius: 0 0 70px 70px; overflow:hidden; }
        #powder { position:absolute; left:0; right:0; bottom:0; height: 110px; background:#1b1b22; }
        #powder2 { position:absolute; left:0; right:0; bottom:0; height: 110px; background:#c24a2a; opacity:0; }
        #lime { position:absolute; left: 300px; top: 200px; width: 150px; height: 250px; border: 4px solid rgba(234,240,255,0.6); border-top:none; border-radius: 0 0 20px 20px; overflow:hidden; }
        #limew { position:absolute; left:0; right:0; bottom:0; height: 120px; background: rgba(140,190,255,0.25); }
        #limew2 { position:absolute; left:0; right:0; bottom:0; height: 120px; background: rgba(234,240,255,0.85); opacity:0; }
        .bub { position:absolute; width: 18px; height: 18px; border-radius:50%; border: 2px solid #eaf0ff; opacity:0; }
        #elab { position:absolute; left: 500px; top: 150px; width: 290px; font-size: 32px; font-weight:300; line-height:1.5; color:#eaf0ff; opacity:0; }
        #elab b { color:#4ce0d2; font-weight:700; }
        #sum { position:absolute; left: 40px; right: 40px; bottom: 30px; font-size: 34px; font-weight: 700; line-height: 1.45; opacity:0; }
        #cu { left: 1040px; top: 300px; width: 720px; height: 620px; }
        #cu .row { display:flex; align-items:center; gap: 22px; margin-top: 22px; opacity:0; }
        #cu .sq { width: 72px; height: 72px; border-radius: 14px; flex: 0 0 auto; }
        #cu .row p { font-size: 31px; }
"""
body = head("실험으로 확인", "산화 구리(Ⅱ)와 탄소 · 구리판 가열") + """          <div class="card" id="exp"><h3>산화 구리(Ⅱ) + 탄소 가열</h3>
            <div id="tube"><div id="powder"></div><div id="powder2"></div></div>
            <div id="lime"><div id="limew"></div><div id="limew2"></div>
              <span class="bub" style="left:40px;bottom:20px"></span><span class="bub" style="left:80px;bottom:50px"></span><span class="bub" style="left:55px;bottom:85px"></span></div>
            <div id="elab">석회수가 <b>뿌옇게</b> → 이산화 탄소 발생<br/><br/>시험관 속 <b style="color:#ff8a65">붉은색</b> 물질 → 구리</div>
            <div id="sum"><span style="color:#4ce0d2">산화 구리(Ⅱ)</span> 산소 잃음 → 구리 (환원)<br/><span style="color:#ff6ec7">탄소</span> 산소 얻음 → 이산화 탄소 (산화)</div>
          </div>
          <div class="card" id="cu"><h3>구리판 가열</h3>
            <div class="row" id="r0"><span class="sq" style="background:#1b1b22"></span><p><b style="color:#ff6ec7">겉불꽃</b> — 산소 충분, 온도 높음<br/>구리 + 산소 → 산화 구리(Ⅱ) <b>검게</b>, 질량 <b>증가</b></p></div>
            <div class="row" id="r1"><span class="sq" style="background:#c24a2a"></span><p><b style="color:#4ce0d2">속불꽃</b> — 불완전 연소, 일산화 탄소 발생<br/>산화 구리(Ⅱ) → 구리 <b>붉게</b>, 질량 <b>감소</b></p></div>
          </div>
"""
t0, t1, t2 = local(sid, 0), local(sid, 1), local(sid, 2)
js = head_js()
js += app("#exp", t0 + 0.5)
js += f'          tl.to("#limew2", {{opacity:1, duration:1.4}}, {t0 + 6});' + NL
for i in range(3):
    js += (f'          tl.fromTo("#lime .bub:nth-of-type({i+1})", {{opacity:0, y:0}}, {{opacity:0.9, y:-60, duration:1.2, ease:"power1.out", immediateRender:false}}, {t0 + 5.5 + i*0.5});' + NL)
js += f'          tl.to("#powder2", {{opacity:1, duration:1.4}}, {t0 + 8.5});' + NL
js += app("#elab", t0 + 9.5, y=20)
js += app("#sum", t1 + 0.3, y=20)
js += app("#cu", t2 + 0.4)
js += app("#r0", t2 + 1.2, y=20)
js += app("#r1", t2 + 8.0, y=20)
js += fade_js(sid)
write_scene(sid, css, body, js, acc=AMBER)

# ─────────────────────────── s05 전자 이동 ───────────────────────────
sid = "s05"
css = CARD + """
        #d0 { left: 160px; top: 300px; width: 700px; height: 220px; }
        #d1 { left: 1060px; top: 300px; width: 700px; height: 220px; }
        #stage { position:absolute; left: 0; right:0; top: 580px; height: 360px; opacity:0; }
        .atom { position:absolute; top: 40px; width: 220px; height: 220px; border-radius:50%; display:flex; align-items:center; justify-content:center; flex-direction:column; font-weight:900; font-size: 64px; letter-spacing:-0.03em; will-change: transform; }
        .atom small { font-size: 30px; font-weight: 300; margin-top: 6px; }
        #zn { left: 420px; background: rgba(255,110,199,0.15); border: 4px solid #ff6ec7; color:#ff6ec7; }
        #cu { left: 1280px; background: rgba(76,224,210,0.15); border: 4px solid #4ce0d2; color:#4ce0d2; }
        .e { position:absolute; top: 120px; width: 54px; height: 54px; border-radius:50%; background:#d4af37; color:#0b1026; font-weight:900; font-size: 28px; display:flex; align-items:center; justify-content:center; opacity:0; will-change: transform; }
        #e1 { left: 640px; } #e2 { left: 640px; top: 190px; }
        #eq { position:absolute; left:0; right:0; top: 300px; text-align:center; font-family:"JetBrains Mono", monospace; font-size: 38px; font-weight:700; color:#eaf0ff; opacity:0; }
        #eq span { margin: 0 40px; }
        #same { position:absolute; left:0; right:0; top: 830px; text-align:center; font-size: 44px; font-weight: 700; color:#d4af37; opacity:0; }
"""
body = head("전자의 이동", "전자로 다시 정의하는 산화와 환원") + """          <div class="card" id="d0"><h3 style="color:#ff6ec7">산화</h3><p>물질이 <b style="color:#ff6ec7">전자를 잃는</b> 반응</p></div>
          <div class="card" id="d1"><h3 style="color:#4ce0d2">환원</h3><p>물질이 <b style="color:#4ce0d2">전자를 얻는</b> 반응</p></div>
          <div id="stage">
            <div class="atom" id="zn">Zn<small>아연</small></div>
            <div class="atom" id="cu">Cu²⁺<small>구리 이온</small></div>
            <div class="e" id="e1" data-layout-allow-overlap>e⁻</div><div class="e" id="e2" data-layout-allow-overlap>e⁻</div>
            <div id="eq"><span style="color:#ff6ec7">Zn → Zn²⁺ + 2e⁻</span><span style="color:#4ce0d2">Cu²⁺ + 2e⁻ → Cu</span></div>
          </div>
          <div id="same">잃은 전자 수 = 얻은 전자 수 (2개 = 2개)</div>
"""
t0, t1 = local(sid, 0), local(sid, 1)
js = head_js()
js += app("#d0", t0 + 0.6)
js += app("#d1", t0 + 2.6)
js += app("#stage", t1 + 0.3, y=20)
js += f'          tl.set("#e1, #e2", {{opacity:0}}, 0);' + NL
js += (f'          tl.fromTo("#e1", {{opacity:1, x:0}}, {{opacity:1, x: 640, duration:1.4, ease:"power2.inOut", immediateRender:false}}, {t1 + 3.0});' + NL)
js += (f'          tl.fromTo("#e2", {{opacity:1, x:0}}, {{opacity:1, x: 640, duration:1.4, ease:"power2.inOut", immediateRender:false}}, {t1 + 3.4});' + NL)
js += f'          tl.to("#zn", {{scale:0.88, duration:0.6}}, {t1 + 3.6});' + NL
js += f'          tl.to("#cu", {{scale:1.1, duration:0.6}}, {t1 + 4.2});' + NL
js += app("#eq", t1 + 5.0, y=16)
js += app("#same", t1 + 8.5, y=16)
js += fade_js(sid)
write_scene(sid, css, body, js, acc=PINK)

# ─────────────────────────── s06 금속과 금속 염 수용액 ───────────────────────────
sid = "s06"
css = CARD + """
        .col { top: 290px; width: 760px; height: 660px; padding: 28px 36px; }
        #a { left: 160px; } #b { left: 1000px; }
        .beaker { position:absolute; right: 40px; top: 110px; width: 150px; height: 200px; border: 4px solid rgba(234,240,255,0.6); border-top:none; border-radius: 0 0 18px 18px; overflow:hidden; }
        .liq { position:absolute; left:0; right:0; bottom:0; height: 150px; }
        .rows { position:absolute; left: 36px; top: 120px; width: 500px; }
        .rows p { font-size: 31px; line-height: 1.4; margin-bottom: 14px; opacity:0; }
        .rows b { font-weight: 700; }
        .bottom { position:absolute; left: 36px; right: 36px; bottom: 30px; font-size: 32px; font-weight: 700; line-height:1.45; opacity:0; }
"""
body = head("금속 + 금속 염 수용액", "반응성이 큰 금속이 산화된다") + """          <div class="card col" id="a"><h3>황산 구리(Ⅱ) 수용액 + 아연</h3>
            <div class="beaker"><div class="liq" id="liqa" style="background: rgba(70,140,255,0.75)"></div></div>
            <div class="rows"><p id="a0"><span class="tag ox">산화</span> 아연 Zn → Zn²⁺ (녹아 들어감)</p><p id="a1"><span class="tag rd">환원</span> 구리 이온 Cu²⁺ → Cu (석출)</p><p id="a2">푸른색이 <b style="color:#4ce0d2">옅어진다</b> — 구리 이온 수 감소</p></div>
            <div class="bottom" id="a3">전체 이온 수 <span style="color:#d4af37">일정</span> (Zn²⁺ 1개 생성 ↔ Cu²⁺ 1개 감소)<br/>반응성: Zn &gt; Cu</div>
          </div>
          <div class="card col" id="b"><h3>질산 은 수용액 + 구리</h3>
            <div class="beaker"><div class="liq" id="liqb" style="background: rgba(70,140,255,0.12)"></div></div>
            <div class="rows"><p id="b0"><span class="tag ox">산화</span> 구리 Cu → Cu²⁺</p><p id="b1"><span class="tag rd">환원</span> 은 이온 Ag⁺ → Ag (석출)</p><p id="b2">푸른색이 <b style="color:#4ce0d2">진해진다</b> — 구리 이온 수 증가</p></div>
            <div class="bottom" id="b3">전체 이온 수 <span style="color:#d4af37">감소</span> (Cu²⁺ 1개 생성 ↔ Ag⁺ 2개 감소)<br/>반응성: Cu &gt; Ag</div>
          </div>
"""
t0, t1, t2 = local(sid, 0), local(sid, 1), local(sid, 2)
js = head_js()
js += app("#a", t0 + 0.4)
js += app("#a0", t0 + 3.5, y=16); js += app("#a1", t0 + 9.0, y=16); js += app("#a2", t0 + 15.5, y=16)
js += f'          tl.to("#liqa", {{backgroundColor:"rgba(70,140,255,0.25)", duration:3.0}}, {t0 + 15.5});' + NL
js += app("#a3", t1 + 0.5, y=16)
js += app("#b", t2 + 0.3)
js += app("#b0", t2 + 3.0, y=16); js += app("#b1", t2 + 5.5, y=16); js += app("#b2", t2 + 8.5, y=16)
js += f'          tl.to("#liqb", {{backgroundColor:"rgba(70,140,255,0.75)", duration:3.0}}, {t2 + 8.5});' + NL
js += app("#b3", t2 + 11.5, y=16)
js += fade_js(sid)
write_scene(sid, css, body, js)

# ─────────────────────────── s07 묽은 염산 · 비금속 · 산소=전자 ───────────────────────────
sid = "s07"
css = CARD + """
        .card { left: 160px; width: 1600px; padding: 26px 40px; }
        #k0 { top: 290px; height: 230px; } #k1 { top: 545px; height: 180px; } #k2 { top: 750px; height: 180px; }
        .card .eq { font-size: 32px; }
        .ok { color:#4ce0d2; } .no { color:#ff6ec7; }
"""
body = head("여러 가지 산화 환원", "묽은 염산 · 비금속 · 산소 이동도 전자 이동") + """          <div class="card" id="k0"><h3>① 금속 + 묽은 염산</h3><div class="eq">Mg + 2H⁺ → Mg²⁺ + H₂↑ &nbsp; <span class="tag ox">Mg 산화</span><span class="tag rd">H⁺ 환원</span></div><p>반응성 금속 &gt; 수소일 때만 반응 — <b class="ok">Mg, Zn ○</b> &nbsp; <b class="no">Cu, Ag ×</b> &nbsp;(수용액 양이온 수·금속판 질량 감소)</p></div>
          <div class="card" id="k1"><h3>② 금속 + 비금속</h3><p>Na + Cl, &nbsp;Mg + O₂ — 금속은 전자를 잃고 <b style="color:#ff6ec7">양이온</b>, 비금속은 전자를 얻고 <b style="color:#4ce0d2">음이온</b> → 이온 결합</p></div>
          <div class="card" id="k2"><h3>③ 산소의 이동 = 전자의 이동</h3><p>산소를 얻는 산화 = 전자를 <b style="color:#ff6ec7">잃는</b> 것 &nbsp;/&nbsp; 산소를 잃는 환원 = 전자를 <b style="color:#4ce0d2">얻는</b> 것 &nbsp;(Mg → Mg²⁺, O → O²⁻)</p></div>
"""
js = head_js()
for k in range(3):
    t = local(sid, k) + 0.6
    js += app(f"#k{k}", t)
    if k > 0:
        js += dim(f"#k{k-1}", t, 0.6)
js += fade_js(sid)
write_scene(sid, css, body, js, acc=GREEN)

# ─────────────────────────── s08 일상 속 산화 환원 ───────────────────────────
sid = "s08"
css = CARD + """
        .g { width: 500px; height: 250px; padding: 28px 34px; }
        .g h3 { font-size: 40px; }
        .g p { font-size: 29px; }
        #g0 { left: 160px; top: 300px; } #g1 { left: 710px; top: 300px; } #g2 { left: 1260px; top: 300px; }
        #g3 { left: 160px; top: 600px; } #g4 { left: 710px; top: 600px; } #g5 { left: 1260px; top: 600px; }
"""
items = [("사과의 갈변", "깎은 부분이 공기 중에서 산화되어 갈색으로"),
         ("반딧불이의 빛", "몸속 루시페린이 산화될 때 불빛"),
         ("일회용 손난로", "철가루가 산화되며 열 발생"),
         ("불꽃놀이", "화약이 산화되며 높은 열 → 금속 불꽃색"),
         ("머리카락 염색", "과산화 수소가 멜라닌 색소를 산화(탈색)"),
         ("섬유 표백", "표백제의 산화 환원 반응으로 옷이 하얗게")]
body = head("일상생활 속", "우리 곁의 산화 환원 반응")
for i, (h, p) in enumerate(items):
    body += f'          <div class="card g" id="g{i}"><h3 style="color:#d4af37">{h}</h3><p>{p}</p></div>' + NL
t0, t1 = local(sid, 0), local(sid, 1)
js = head_js()
for i in range(3):
    js += app(f"#g{i}", t0 + 2.5 + i * 3.2)
for i in range(3, 6):
    js += app(f"#g{i}", t1 + 0.8 + (i - 3) * 3.4)
js += fade_js(sid)
write_scene(sid, css, body, js, acc=GOLD)

# ─────────────────────────── s09 시험 포인트 ───────────────────────────
sid = "s09"
css = """
        #steps { position:absolute; left: 160px; right: 160px; top: 300px; }
        .st { display:flex; align-items:flex-start; gap: 30px; border-radius: 20px; border: 2px solid rgba(143,160,196,0.3);
          background: rgba(234,240,255,0.03); padding: 24px 36px; margin-bottom: 20px; opacity: 0; will-change: transform; }
        .st .no { flex:0 0 auto; font-family:"JetBrains Mono", monospace; font-size: 36px; font-weight:700; color:#0b1026; background:#d4af37;
          border-radius: 999px; width: 62px; height: 62px; display:flex; align-items:center; justify-content:center; }
        .st .tx { flex:1 1 auto; font-size: 35px; font-weight: 700; line-height: 1.4; letter-spacing:-0.02em; padding-top: 8px; }
        .st b { color:#4ce0d2; }
"""
pts = ["산화 = 산소를 <b>얻거나</b> 전자를 <b>잃는</b> 것 / 환원 = 산소를 <b>잃거나</b> 전자를 <b>얻는</b> 것",
       "산화와 환원은 항상 <b>동시에</b> — 잃은 전자 수 = 얻은 전자 수",
       "금속 염 수용액: <b>산화된 쪽이 반응성 큰 금속</b> · 이온 수 변화 · 수용액 색 변화를 함께 묻는다",
       "광합성 · 연소 · 제련에서 <b>무엇이 산화되고 무엇이 환원되는지</b> 구분"]
body = head("시험 포인트", "이것만은 꼭!") + '          <div id="steps">' + NL
for i, p in enumerate(pts):
    body += f'            <div class="st" id="st{i}"><span class="no">{i+1}</span><span class="tx">{p}</span></div>' + NL
body += "          </div>" + NL
t0, t1 = local(sid, 0), local(sid, 1)
js = head_js()
js += app("#st0", t0 + 1.0); js += app("#st1", t0 + 8.5)
js += app("#st2", t1 + 0.5); js += app("#st3", t1 + 9.0)
js += fade_js(sid)
write_scene(sid, css, body, js, acc=GOLD)

# ─────────────────────────── s10 마무리 ───────────────────────────
sid = "s10"
css = """
        #big { position:absolute; left:0; right:0; top: 380px; text-align:center; font-size: 96px; font-weight: 900; letter-spacing:-0.04em; line-height:1.2; opacity:0; will-change: transform; }
        #big em { font-style:normal; color:#4ce0d2; }
        #sub { position:absolute; left:0; right:0; top: 660px; text-align:center; font-size: 40px; font-weight: 300; color:#8fa0c4; opacity:0; }
"""
body = """          <div id="big">산소의 이동, <em>전자의 이동</em><br/>두 눈으로 보는 산화와 환원</div>
          <div id="sub">다음 시간 — 산과 염기, 그리고 중화 반응 · 수고했어요!</div>
"""
js = app("#big", 0.6, y=40, d=0.8, ease="power3.out")
js += app("#sub", 6.5, y=24)
write_scene(sid, css, body, js)

# ─────────────────────────── index 슬롯 ───────────────────────────
slots = ""
for sid in ORDER:
    st, du = win[sid]
    slots += f"""      <div
        id="el-{sid}"
        data-composition-id="{sid}"
        data-composition-src="compositions/{sid}.html"
        data-start="{st}"
        data-duration="{du}"
        data-track-index="1"
        data-width="1920"
        data-height="1080"
      ></div>
"""
open(os.path.join(ROOT, "scripts", "slots.html"), "w", encoding="utf-8").write(slots)
print("scenes written:", ORDER, "TOTAL", TOTAL)
