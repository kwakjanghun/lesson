# 부록 A. 복붙용 프롬프트·명령 모음

> 이 페이지의 회색 상자는 **그대로 복사해서 붙여넣는** 것입니다.
> `PS>` 로 시작하는 줄은 **PowerShell 창**에, 말풍선 상자는 **클로드 코드 채팅창**에 넣습니다.
> 선생님 상황에 맞게 바꿔야 하는 부분은 `〈 〉` 로 표시했습니다.

---

## A-1. 설치 확인 (PowerShell)

```
PS> node -v
PS> python --version
PS> ffmpeg -version
PS> git --version
```
네 줄 모두 버전 숫자가 나오면 준비 끝. "찾을 수 없습니다"가 나오는 항목만 2장으로 돌아가 설치합니다.

## A-2. 작업 폴더 만들기 (PowerShell)

```
PS> mkdir C:\hyper
```
영문 폴더가 중요합니다. 바탕화면·다운로드·한글 이름 폴더에서는 영상 도구가 조용히 멈춥니다.

## A-3. 클로드 코드에서 첫 대화 (채팅창)

```
안녕! 지금 열려 있는 폴더 경로를 알려주고, 이 컴퓨터에 node, python, ffmpeg, git이 설치돼 있는지 확인해 줘.
없는 게 있으면 어떻게 설치하는지 알려줘.
```

## A-4. watch 스킬 설치 (PowerShell, C:\hyper 에서)

```
PS> cd C:\hyper
PS> npx skills add bradautomates/claude-video --agent claude-code --skill watch -y --copy
```
유튜브 영상을 받으려면 deno도 한 번 설치합니다 (2026년 기준 유튜브 정책 때문에 필요):
```
PS> winget install --id DenoLand.Deno -e
PS> pip install -U yt-dlp
```

## A-5. watch 써 보기 (채팅창)

```
/watch C:\hyper\〈영상파일〉.mp4  이 영상이 어떤 내용인지 단계별로 요약해 줘. 화면에 나온 명령어가 있으면 적어 줘.
```
유튜브 주소도 됩니다:
```
/watch https://www.youtube.com/watch?v=〈영상ID〉  이 수업 영상의 구성(도입·전개·정리)과 핵심 개념을 정리해 줘.
```

## A-6. HyperFrames 설치 (PowerShell, C:\hyper 에서)

```
PS> cd C:\hyper
PS> npx skills add heygen-com/hyperframes --agent claude-code -y --copy
PS> git clone https://github.com/kwakjanghun/lesson.git
PS> cd lesson\kit
PS> npx hyperframes check
```
`Check passed` 가 나오면 성공. 처음엔 `npx hyperframes` 가 패키지를 내려받느라 1~2분 걸립니다.

## A-7. 첫 렌더 (PowerShell)

```
PS> npx hyperframes render -o test.mp4
```
`Render complete` 와 함께 `test.mp4` 가 생기면 영상 제작 환경이 완성된 것입니다.

## A-8. 나레이션 도구 설치 (PowerShell)

```
PS> pip install edge-tts mutagen pymupdf
```

## A-9. 수업 영상 만들기 — 기본 프롬프트 (채팅창, `C:\hyper\lesson` 폴더를 연 상태)

```
이 폴더는 수업 영상 제작 킷이야. kit/ 폴더의 구조(scripts/make_narration.py, scripts/gen_scenes.py, scripts/wire_index.py, compositions/, index.html)를 먼저 읽어 줘.

내 수업 자료는 〈C:\hyper\source\수업자료.pdf〉 야. 이 PDF를 읽고 아래 조건으로 학습 영상을 만들어 줘.
- 대상: 〈고1 통합과학〉, 길이 5~7분
- 장면 8~10개, 장면마다 나레이션 3~5문장 (학생에게 말하는 존댓말 수업 톤)
- 내용·용어·수치는 반드시 PDF에서 가져올 것 (지어내지 않기)
- 마지막에 '시험 포인트' 장면 1개 포함
- 작업은 C:\hyper\〈영문이름〉 폴더에서 (한글 경로 금지)

순서: ① 대본(SCENES) 작성 → ② make_narration.py로 음성 생성 → ③ gen_scenes.py로 장면 만들기 → ④ npx hyperframes check 통과 → ⑤ 스냅샷으로 눈 확인 → ⑥ 렌더 → ⑦ 완성 mp4 경로 알려주기.
대본을 다 쓰면 렌더 전에 한 번 보여 줘.
```

## A-10. 인트로 붙이기 (채팅창)

```
완성된 본편 앞에 〈C:\hyper\source\인트로.mp4〉 를 붙여서 final.mp4 로 만들어 줘. 해상도 1920x1080, 30fps, 오디오 48kHz로 맞춰서.
```

## A-11. 목소리 바꾸기 — 기본 목소리 (채팅창)

```
나레이션 목소리를 여성(ko-KR-SunHiNeural)으로 바꿔서 다시 만들어 줘.
```

## A-12. 내 목소리 레퍼런스 준비 (PowerShell, GPU PC)

```
PS> cd C:\ai\qwen3tts
PS> python prep_ref.py 〈C:\hyper\source\내목소리.m4a〉 ref\myvoice_clean.wav
```
그리고 `ref\myvoice.txt` 에 **녹음에서 실제로 읽은 문장**을 그대로 적어 둡니다.

## A-13. 내 목소리로 나레이션 교체 (채팅창, GPU PC)

```
같은 대본으로 나레이션을 내 목소리(Qwen3-TTS, C:\ai\qwen3tts\tts.py)로 다시 만들어 줘.
scripts/make_narration_myvoice.py 를 쓰고, 끝나면 gen_scenes.py → wire_index.py → check → 렌더까지 이어서 해 줘.
```

## A-14. 내 목소리 — Kaggle 무료 GPU (PowerShell)

```
PS> pip install -U kaggle
PS> kaggle auth login
```
(브라우저가 열리면 Approve → 코드 붙여넣기. **이 로그인은 선생님이 직접** 합니다.)
```
PS> python ~\.claude\skills\kaggle-tts\scripts\check.py
PS> python ~\.claude\skills\kaggle-tts\scripts\prep_ref.py C:\ai\qwen3tts\ref\myvoice_clean.wav --no-clean --text C:\ai\qwen3tts\ref\myvoice.txt
PS> python ~\.claude\skills\kaggle-tts\scripts\run_batch.py 〈대본.txt〉 --name 〈이름〉
```

## A-15. 문제 생겼을 때 (채팅창)

```
방금 명령이 실패했어. 에러 메시지를 그대로 읽고, 원인을 한 줄로 말해 준 다음, 고치는 명령을 알려줘. 내가 할 수 있는 건 복사·붙여넣기뿐이야.
```
