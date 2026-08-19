# 클로드 코드 × HyperFrames로 수업 영상 자동 제작하기 — 내 목소리 나레이션까지

> 설치부터 완성까지, 아무것도 몰라도 따라 하는 가이드 · 곽장훈(숭신고) · 2026. 8.
> AI 디지털 도구 나눔 자료

**PDF 수업 자료 한 장 → 내 목소리로 설명하는 6분 모션그래픽 수업 영상.** 편집 프로그램·코딩 지식·비용 없이, 복사·붙여넣기로.

| | |
|---|---|
| 📄 **가이드 PDF** | [`guide/클로드코드_HyperFrames_수업영상제작_가이드.pdf`](guide/) |
| 🎬 **완성 영상** | [Releases](../../releases) — 통합과학2 「화학 변화 ① 산화와 환원」 (기본 목소리 / 내 목소리 / 인트로) |
| 🧰 **예제 킷** | [`kit/`](kit/) — 바로 `npx hyperframes check` 되는 화학변화 프로젝트 (대본·장면·스크립트) |
| 📋 **복붙 프롬프트** | [`manuscript/prompts.md`](manuscript/prompts.md) |
| 🖼 **실제 화면** | [`captures/`](captures/) |

## 3줄 빠른 시작

```powershell
mkdir C:\hyper; cd C:\hyper
npx skills add heygen-com/hyperframes --agent claude-code -y --copy
git clone https://github.com/kwakjanghun/lesson.git; cd lesson\kit; npx hyperframes check
```
그다음 Claude 데스크탑 → 코드 탭 → `C:\hyper\lesson` 열고 `manuscript/prompts.md` 의 **A-9** 프롬프트를 붙여넣으면 됩니다. (Node.js·Python·ffmpeg 설치는 가이드 2장)

## 세 도구, 세 동사

| 도구 | 동사 | 하는 일 |
|---|---|---|
| 클로드 코드 | 일꾼 | 내 PC에서 파일 읽기·프로그램 실행·결과 만들기 |
| watch 스킬 | **보기** | 유튜브·수업 영상을 클로드가 보고 정리 |
| HyperFrames | **만들기** | 대본 타이밍에 맞춘 모션그래픽 영상 렌더 |
| Qwen3-TTS | **말하기** | 12초 녹음으로 내 목소리 나레이션 (로컬 GPU 또는 Kaggle 무료 GPU) |

## 폴더

```
guide/        완성 PDF, guide.html
manuscript/   장별 원고(00~08), prompts.md
kit/          화학변화 예제 HyperFrames 프로젝트 (CLAUDE.md, frame.md, scripts/, compositions/, index.html)
captures/     설치·제작 과정 실제 화면 (yt/SOURCES.md 에 출처)
build/        build_pdf.py, style.css — md → HTML → PDF(Edge headless)
```

## 라이선스

자료·원고: CC BY 4.0 (곽장훈). HyperFrames Apache 2.0 · 스타터 킷 philosophyAIEDU/260731eduhyper · watch MIT · Qwen3-TTS Apache 2.0 · Pretendard OFL. 교과 내용은 교과서 저작권을 따릅니다.
