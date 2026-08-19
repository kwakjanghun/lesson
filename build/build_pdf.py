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

parts = []
toc = []
for i, (fn, title) in enumerate(CHAPTERS):
    path = os.path.join(MS, fn)
    if not os.path.exists(path):
        print("missing", fn); continue
    md = open(path, encoding="utf-8").read()
    md = preprocess(md, MS)
    body = markdown.markdown(md, extensions=["tables", "fenced_code", "sane_lists", "toc"])
    body = body.replace("<!--QR-->", QR_HTML)
    # 각 장의 첫 h1에 id 부여
    anchor = f"ch{i}"
    body = re.sub(r"<h1>", f'<h1 id="{anchor}">', body, count=1)
    parts.append(f'<section class="chapter" id="sec-{anchor}">{body}</section>')
    toc.append(f'<li><a href="#{anchor}">{H.escape(title)}</a></li>')

CSS = open(os.path.join(ROOT, "build", "style.css"), encoding="utf-8").read()
cover = f"""
<section class="cover">
  <div class="cover-kicker">AI 디지털 도구 나눔 자료</div>
  <h1 class="cover-title">{H.escape(TITLE)}</h1>
  <div class="cover-sub">{H.escape(SUB)}</div>
  <div class="cover-sub2">{H.escape(SUB2)}</div>
  <div class="cover-tags"><span>클로드 코드</span><span>watch · 보기</span><span>HyperFrames · 만들기</span><span>Qwen3-TTS · 말하기</span></div>
  <div class="cover-author">{H.escape(AUTHOR)}</div>
  <div class="cover-repo">{H.escape(REPO_TXT)}</div>
</section>
<section class="toc">
  <h1>차례</h1>
  <ol>{''.join(toc)}</ol>
  <p class="toc-note">회색 상자는 복사해서 붙여넣는 것입니다. <code>PS&gt;</code> 는 PowerShell, 말풍선은 클로드 코드 채팅창. 캡처 아래 "이 화면이 나오면 성공"까지 확인하고 다음으로 갑니다.</p>
</section>
"""
html_doc = f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8"/>
<title>{H.escape(TITLE)}</title>
<style>{CSS}</style>
</head><body>
{cover}
{''.join(parts)}
</body></html>"""
html_path = os.path.join(OUT, "guide.html")
open(html_path, "w", encoding="utf-8").write(html_doc)
print("html:", html_path, f"{os.path.getsize(html_path)/1e6:.1f} MB")

if args.no_pdf:
    sys.exit(0)

EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
pdf_path = os.path.join(OUT, args.out)
cmd = [EDGE, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
       "--run-all-compositor-stages-before-draw", "--virtual-time-budget=20000",
       f"--print-to-pdf={pdf_path}", "file:///" + html_path.replace("\\", "/")]
subprocess.run(cmd, check=True, capture_output=True)
import fitz
d = fitz.open(pdf_path)
print("pdf:", pdf_path, "pages:", len(d), f"{os.path.getsize(pdf_path)/1e6:.1f} MB")
