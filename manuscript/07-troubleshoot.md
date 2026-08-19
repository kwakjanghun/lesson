# 7. 자주 막히는 곳 & 해결

> 전부 **이 자료를 만들면서 실제로 겪은 것**입니다. 순서는 "자주 겪는 순".
> 여기 없는 문제는 → 에러를 그대로 클로드에게 (부록 A-15).

| # | 증상 | 원인 | 해결 |
|---|---|---|---|
| 1 | `npx hyperframes …` 가 아무 말 없이 끝나거나 멈춤 (exit 127 / 0xC0000409) | **경로에 한글**이 있음 (바탕화면, 다운로드, "보강영상" 폴더 등) | 작업을 `C:\hyper\〈영문〉` 으로. 원본 PDF·영상은 한글 폴더에 있어도 됨 — HyperFrames 프로젝트 폴더만 영문이면 됨. `hyperframes init` 도 같은 이유로 죽으니 init 대신 **킷을 복사**해서 시작 |
| 2 | 설치했는데 `node`/`python`/`ffmpeg` 를 "찾을 수 없습니다" | 설치 전에 연 PowerShell 창은 새 프로그램을 모름 | PowerShell 창 **전부 닫고 새로 열기**. 그래도 안 되면 재시작. Python은 설치 때 "Add to PATH" 체크를 빠뜨렸을 가능성 → 재설치 |
| 3 | `check` 는 통과했는데 렌더 영상에 **빈 화면** 구간 | check는 레이아웃·문법만 봄. 요소가 안 나타나는 건 못 잡음 | 렌더 전 반드시 `npx hyperframes snapshot --at 5,30,60,…` 으로 컨택트 시트를 **눈으로** 확인. 렌더 후에도 `ffmpeg -ss 30 -i out.mp4 -frames:v 1 check.png` 한 장 |
| 4 | check에서 `content_overlap … 텍스트 두 블록이 겹침` | 진짜 겹침이거나, CSS가 깨져 모든 요소가 좌상단에 쌓임 | 스냅샷을 보면 바로 구분됨. 이 자료 예시에선 CSS 중괄호 오타(`{{`)였음 → 클로드에게 "스냅샷 보고 원인 찾아 고쳐 줘". 의도한 겹침이면 `data-layout-allow-overlap` |
| 5 | 유튜브 `/watch` 가 **403 Forbidden / 429** | 2026년 유튜브가 yt-dlp에 JS 런타임·PO 토큰을 요구. 날에 따라 막힘 | `winget install DenoLand.Deno` + `pip install -U yt-dlp` 후 재시도. 그래도 막히면 영상을 파일로 받아 로컬 경로로 watch. (2026-08-19에는 deno를 깔아도 403 → 로컬 파일로 진행했음) |
| 6 | Qwen3-TTS: `CUDA error: device-side assert … input[0] != 0` | **RTX 20xx(Turing)에서 float16** 사용 → 숫자 범위 초과로 NaN | `dtype=bfloat16` (0.6B는 float32). 공식 예제의 fp16을 그대로 쓰면 안 됨 |
| 7 | Qwen3-TTS: `flash_attention_2 … not supported` | FlashAttention2는 RTX 30xx(Ampere) 이상 전용 | `attn_implementation="sdpa"` |
| 8 | Qwen3-TTS가 15분 넘게 GPU를 잡고 안 끝남 | `do_sample=False`(greedy) → 문장 끝(EOS)을 못 찾고 max_new_tokens까지 생성 | greedy 금지, `temperature=0.3` |
| 9 | 내 목소리가 **안 닮음 / 세그먼트마다 음색이 흔들림** | (a) 0.6B 모델 (b) temperature 0.9 기본값 (c) ref_text 불일치 | (a) 1.7B로 (b) 0.3으로 (c) 녹음과 텍스트를 글자 단위로 맞추기. `ref_text` 가 없으면 x-vector 모드로 떨어져 품질 급락 |
| 10 | TTS가 평소보다 2~3배 느림 | 렌더(크롬 5개, CPU)와 동시에 돌림 | 렌더 끝나고 TTS, 또는 TTS 끝나고 렌더 |
| 11 | Kaggle 커널 로그에 `Temporary failure in name resolution` / `Network is unreachable` | **휴대폰 인증** 안 된 계정은 커널 인터넷이 막힘 | kaggle.com/settings → Phone Verification. 명령어 탓이 아님 |
| 12 | Kaggle `no GPU` | 주간 30시간 한도 소진 또는 machine_shape 설정 | `check.py` 가 남은 시간을 보여 줌. 다음 주 월요일 리셋 |
| 13 | 인트로와 본편을 붙였더니 소리가 안 나거나 화면이 깨짐 | 두 영상의 해상도·fps·오디오 샘플레이트가 다름 | ffmpeg concat 때 `fps=30, format=yuv420p, aformat=48000:stereo` 로 맞추기 (클로드에게 "규격 맞춰서 붙여 줘") |
| 14 | 렌더 시작 시 "Chrome Headless Shell 없음" | 최초 1회 설치 필요 | `npx hyperframes browser ensure` (약 115MB) |
| 15 | 클로드가 PDF를 못 읽음 / `pdftoppm` 없음 | PDF 이미지 렌더 도구 없음 | 텍스트 추출은 `pip install pymupdf` 로 충분. PDF 그림이 꼭 필요하면 "PDF 3쪽을 이미지로 저장해 줘"(fitz) |
| 16 | `.ps1` 스크립트가 한글 깨지며 실행 안 됨 | Windows PowerShell 5.1은 BOM 없는 .ps1을 CP949로 읽음 | 파일을 **UTF-8 with BOM** 으로 저장 (킷 CLAUDE.md 8번에 복구 명령) |
| 17 | `git push` 에서 로그인 창이 안 뜨거나 거부 | 깃허브 자격 증명 미설정 | 윈도우 "자격 증명 관리자"에서 github 항목 삭제 후 다시 push → 브라우저 로그인. 또는 `winget install GitHub.cli` → `gh auth login` |
| 18 | 클로드가 "이 작업은 허용이 필요합니다"만 반복 | 권한 수동 모드 | 내용 확인 후 허용. 반복 작업이면 "편집 자동 수락" |

## 막혔을 때의 순서

1. 에러 **전문**을 복사 (빨간 글씨 위아래 10줄 포함)
2. 클로드에게: "방금 명령이 실패했어. 에러를 읽고 원인 한 줄 + 고치는 명령을 알려줘. 나는 복사·붙여넣기만 할 수 있어."
3. 클로드가 고친 뒤 **같은 명령을 다시** 실행
4. 세 번 실패하면 위 표에서 증상으로 찾기 → 그래도 안 되면 {{REPO_URL}}/issues 에 남겨 주세요
