# -*- coding: utf-8 -*-
"""manuscript/*.md → guide/guide.html → guide/*.pdf (Edge headless)

사용:  python build/build_pdf.py [--repo URL] [--video URL] [--out 파일명.pdf]
플레이스홀더: {{REPO_URL}} {{VIDEO_URL}} {{QR_REPO}}
  - URL이 주어지면 치환 + QR 생성, 없으면 "[깃허브 링크 예정]" 으로 표시
특수 규칙: ![alt](…/파일.txt) 는 이미지가 아니라 터미널 캡처(텍스트)로 <pre> 박스에 넣는다.
"""
import os, re, sys, io, base64, argparse, subprocess, shutil, html as H
import markdown

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MS = os.path.join(ROOT, "manuscript")
OUT = os.path.join(ROOT, "guide")
os.makedirs(OUT, exist_ok=True)

ap = argparse.ArgumentParser()
ap.add_argument("--repo", default="")
ap.add_argument("--video", default="")
ap.add_argument("--out", default="draft.pdf")
ap.add_argument("--no-pdf", action="store_true")
ap.add_argument("--style", default="")
ap.add_argument("--only", type=int, default=0, help="앞 N개 장만 (목업용)")
args = ap.parse_args()

TITLE = "클로드 코드 × HyperFrames로 수업 영상 자동 제작하기"
SUB = "— 내 목소리 나레이션까지 —"
SUB2 = "설치부터 완성까지, 아무것도 몰라도 따라 하는 가이드"
AUTHOR = "곽장훈 · 숭신고등학교 · 2026. 8."
SUBJECT_LINE = "AI 디지털 도구 나눔 자료 · 주제: 클로드 코드 × HyperFrames로 수업 영상 자동 제작하기 — 내 목소리 나레이션까지"

CHAPTERS = [
    ("00-intro.md", "0. 이 자료로 무엇이 되는가"),
    ("01-prepare.md", "1. 준비물"),
    ("02-install-claude.md", "2. 클로드 코드 설치"),
    ("03-watch.md", "3. watch 스킬 — 보기"),
    ("04-hyperframes.md", "4. HyperFrames 설치 — 만들기"),
    ("05-make-video.md", "5. 영상 제작 실습"),
    ("06-voice.md", "6. 내 목소리 입히기 — 말하기"),
    ("07-troubleshoot.md", "7. 자주 막히는 곳 & 해결"),
    ("08-closing.md", "마무리 · 부록 B · 부록 C"),
    ("prompts.md", "부록 A. 복붙용 프롬프트·명령 모음"),
]

def data_uri(path):
    ext = os.path.splitext(path)[1].lower()
    mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg"}[ext[1:]]
    return f"data:{mime};base64," + base64.b64encode(open(path, "rb").read()).decode()

def qr_uri(url):
    import qrcode
    img = qrcode.make(url, box_size=6, border=2)
    b = io.BytesIO(); img.save(b, format="PNG")
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()

repo = args.repo or ""
video = args.video or ""
REPO_TXT = repo if repo else "[깃허브 링크 — 업로드 후 삽입]"
VIDEO_TXT = video if video else "[완성 영상 링크(깃허브 Releases) — 업로드 후 삽입]"
QR_HTML = (f'<div class="qr"><img src="{qr_uri(repo)}" alt="QR"/><div>{H.escape(repo)}</div></div>' if repo
           else '<div class="qr qr-pending">QR 코드 자리<br/>(저장소 업로드 후 삽입)</div>')

def preprocess(md, base):
    # 플레이스홀더
    md = md.replace("{{REPO_URL}}", REPO_TXT).replace("{{VIDEO_URL}}", VIDEO_TXT)
    md = md.replace("{{QR_REPO}}", "\n\n<!--QR-->\n\n")
    # 텍스트 캡처 → pre
    def txt_sub(m):
        alt, rel = m.group(1), m.group(2)
        p = os.path.normpath(os.path.join(base, rel))
        body = open(p, encoding="utf-8", errors="replace").read().rstrip()
        return f'\n\n<div class="term"><div class="term-cap">{H.escape(alt)}</div><pre>{H.escape(body)}</pre></div>\n\n'
    md = re.sub(r'!\[([^\]]*)\]\(([^)]+\.txt)\)', txt_sub, md)
    # 이미지 → data URI + figure
    def img_sub(m):
        alt, rel = m.group(1), m.group(2)
        p = os.path.normpath(os.path.join(base, rel))
        if not os.path.exists(p):
            return f'\n\n<div class="missing">[그림 없음: {H.escape(rel)}]</div>\n\n'
        return f'\n\n<figure><img src="{data_uri(p)}" alt="{H.escape(alt)}"/><figcaption>{H.escape(alt)}</figcaption></figure>\n\n'
    md = re.sub(r'!\[([^\]]*)\]\(([^)]+\.(?:png|jpg|jpeg))\)', img_sub, md)
    return md

FONT_URI = "data:font/woff2;base64," + base64.b64encode(open(os.path.join(ROOT,"kit","assets","fonts","PretendardVariable.woff2"),"rb").read()).decode()

def postprocess(body):
    # 코드 블록 분류: PS 창 / 채팅 말풍선 / 실행 결과 / 중립 코드
    def pre_sub(m):
        inner = m.group(1); raw = H.unescape(re.sub(r"<[^>]+>", "", inner))
        if "PS>" in raw or raw.lstrip().startswith("$ "):
            kind = "ps"; label = "Windows PowerShell"
        elif any(k in raw for k in ["[watch]", "[tts]", "[kaggle-tts]", "◇", "█", "TOTAL", "made s", "Check", "Render", "Lint", "Installed", "mean_volume", "s01 ", "✓", "rendered in", "Capturing"]):
            kind = "out"; label = "실행 결과"
        elif '("s0' in raw or raw.lstrip().startswith(("{", "[", "<", "node ", "v2")) or "\n" not in raw.strip() and len(raw) < 40:
            kind = "code"; label = ""
        else:
            kind = "chat"; label = "클로드 코드 채팅창에 붙여넣기"
        if kind == "ps":
            return f'<div class="ps"><div class="bar"><i></i><i></i><i></i><span>{label}</span></div><pre>{inner}</pre></div>'
        if kind == "out":
            return f'<div class="out"><div class="bar"><span>{label}</span></div><pre>{inner}</pre></div>'
        if kind == "chat":
            return f'<div class="chat"><div class="who"><b>C</b><span>{label}</span><em>복사 → 붙여넣기 → Enter</em></div><pre>{inner}</pre></div>'
        return f'<pre class="code">{inner}</pre>'
    body = re.sub(r"<pre><code>(.*?)</code></pre>", pre_sub, body, flags=re.S)
    # 성공 콜아웃
    body = re.sub(r"<p><strong>이 화면이 나오면 성공</strong>", '<p class="ok"><strong>이 화면이 나오면 성공</strong>', body)
    # 인용 종류
    body = re.sub(r"<blockquote>\s*<p>(⚠|💡)", lambda m: f'<blockquote class="{ "warn" if m.group(1)=="⚠" else "tip" }"><p>{m.group(1)}', body)
    body = re.sub(r"<blockquote>\s*<p><strong>목표</strong>", '<blockquote class="goal"><p><strong>목표</strong>', body)
    return body

parts = []
toc = []
for i, (fn, title) in enumerate(CHAPTERS[:args.only] if args.only else CHAPTERS):
    path = os.path.join(MS, fn)
    if not os.path.exists(path):
        print("missing", fn); continue
    md = open(path, encoding="utf-8").read()
    md = preprocess(md, MS)
    body = markdown.markdown(md, extensions=["tables", "fenced_code", "sane_lists", "toc"])
    body = body.replace("<!--QR-->", QR_HTML)
    # 각 장의 첫 h1에 id 부여
    anchor = f"ch{i}"
    def h1sub(m):
        t = m.group(1); num, _, rest = t.partition(". ")
        if not rest or not num[:1].isdigit(): num, rest = "", t
        title, _, lead = rest.partition(" — ")
        lead_html = f'<div class="ch-lead">{lead}</div>' if lead else ""
        num_html = f'<div class="ch-num">{num}</div>' if num else ""
        return f'<div class="ch-open">{num_html}<h1 id="{anchor}">{title}</h1>{lead_html}</div>'
    body = re.sub(r"<h1[^>]*>(.*?)</h1>", h1sub, body, count=1)
    body = postprocess(body)
    parts.append(f'<section class="chapter" id="sec-{anchor}">{body}</section>')
    num, _, rest = title.partition(". ")
    if not rest: num, rest = "", title
    toc.append(f'<li><a href="#{anchor}"><span class="n">{H.escape(num)}</span><span class="t">{H.escape(rest)}</span></a></li>')

CSS = open(os.path.join(ROOT, "build", f"style-{args.style}.css" if args.style else "style.css"), encoding="utf-8").read()
CSS = '@font-face{font-family:"Pretendard";src:url(' + FONT_URI + ') format("woff2-variations");font-weight:45 920;}' + chr(10) + CSS
HERO = data_uri(os.path.join(ROOT, "captures", "05-07-still-title.png"))
HERO2 = data_uri(os.path.join(ROOT, "captures", "05-07-still-metal.png"))
cover = f"""
<section class="cover">
  <div class="cv-top">
    <div class="cv-kicker"><span>AI 디지털 도구 나눔 자료</span><span>2026 · 숭신고등학교</span></div>
    <h1 class="cv-title">클로드 코드 <span class="x">×</span> HyperFrames로<br/>수업 영상 <em>자동 제작</em>하기</h1>
    <div class="cv-sub">내 목소리 나레이션까지</div>
    <p class="cv-desc">{H.escape(SUB2)}. PDF 수업 자료 한 장을 넣으면, 선생님 목소리로 설명하는 6분짜리 모션그래픽 수업 영상이 나옵니다. 편집 프로그램도 코딩도 비용도 없이 — 복사·붙여넣기로.</p>
  </div>
  <div class="cv-hero"><img src="{HERO}" alt=""/><div class="cv-hero-cap">예시 결과물 · 통합과학2 「화학 변화 ① 산화와 환원」 6분 · 내 목소리</div></div>
  <div class="cv-flow">
    <div class="st"><b>01</b><span>PDF 한 장</span></div><i>→</i>
    <div class="st"><b>02</b><span>클로드가 대본·장면</span></div><i>→</i>
    <div class="st"><b>03</b><span>HyperFrames 렌더</span></div><i>→</i>
    <div class="st"><b>04</b><span>내 목소리 12초</span></div>
  </div>
  <div class="cv-foot">
    <div class="cv-verbs"><span><b>보기</b> watch</span><span><b>만들기</b> HyperFrames</span><span><b>말하기</b> Qwen3-TTS</span></div>
    <div class="cv-author">{H.escape(AUTHOR)}<br/><small>{H.escape(REPO_TXT)}</small></div>
  </div>
</section>
<section class="toc">
  <div class="toc-head"><div class="toc-kicker">CONTENTS</div><h1>차례</h1></div>
  <ol>{''.join(toc)}</ol>
  <div class="toc-side"><img src="{HERO2}" alt=""/></div>
  <p class="toc-note"><b>읽는 법</b> — 검은 창(Windows PowerShell)은 파워셸에, 말풍선(C)은 클로드 코드 채팅창에 붙여넣습니다. 초록 체크 "이 화면이 나오면 성공"까지 확인하고 다음으로. 막히면 7장.</p>
</section>
"""
toc_html = cover[cover.index('<section class="toc">'):]
cover_only = cover[:cover.index('<section class="toc">')]
html_doc = f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"/>
<title>{H.escape(TITLE)}</title>
<style>{CSS}</style>
</head><body>
{toc_html}
{''.join(parts)}
</body></html>"""
cover_doc = f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"/><title>cover</title>
<style>{CSS}
@page {{ size: A4; margin: 0; }}
.cover {{ margin: 0 !important; height: 297mm !important; width: 210mm !important; page-break-after: auto !important; }}
</style></head><body>{cover_only}</body></html>"""
cover_path = os.path.join(OUT, f"cover{'-'+args.style if args.style else ''}.html")
open(cover_path, "w", encoding="utf-8").write(cover_doc)
html_path = os.path.join(OUT, f"guide{'-'+args.style if args.style else ''}.html")
open(html_path, "w", encoding="utf-8").write(html_doc)
print("html:", html_path, f"{os.path.getsize(html_path)/1e6:.1f} MB")

if args.no_pdf:
    sys.exit(0)

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
pdf_path = os.path.join(OUT, args.out)
cmd = [EDGE, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
       "--run-all-compositor-stages-before-draw", "--virtual-time-budget=20000",
       f"--print-to-pdf={pdf_path}", "file:///" + html_path.replace("\\", "/")]
body_pdf = pdf_path + ".body.pdf"; cover_pdf = pdf_path + ".cover.pdf"
cmd[-2] = f"--print-to-pdf={body_pdf}"
subprocess.run(cmd, check=True, capture_output=True)
cmd2 = list(cmd); cmd2[-2] = f"--print-to-pdf={cover_pdf}"; cmd2[-1] = "file:///" + cover_path.replace("\\", "/")
subprocess.run(cmd2, check=True, capture_output=True)
import fitz
d = fitz.open(cover_pdf); d2 = fitz.open(body_pdf); d.insert_pdf(d2); d.save(pdf_path); d.close(); d2.close()
os.remove(body_pdf); os.remove(cover_pdf)
d = fitz.open(pdf_path)
print("pdf:", pdf_path, "pages:", len(d), f"{os.path.getsize(pdf_path)/1e6:.1f} MB")
