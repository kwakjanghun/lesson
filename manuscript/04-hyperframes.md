# 4. HyperFrames 설치 — 영상 제작 엔진과 예제 킷

> **목표**: HyperFrames 스킬을 설치하고, 예제 킷을 받아 `check` 통과 → 첫 렌더(`test.mp4`)까지.
> 걸리는 시간 15분.

## 4-1. HyperFrames가 뭔가요

- 오픈소스(Apache 2.0) 영상 제작 도구. **웹페이지(HTML)를 1초에 30장씩 스크린샷 찍어 영상으로** 만듭니다.
- 웹페이지 안에 "몇 초에 무엇이 어떻게 움직인다"가 코드로 적혀 있고, **그 코드를 쓰는 게 클로드가 가장 잘하는 일**입니다.
- 그래서 After Effects에서 키프레임을 찍는 대신, 클로드에게 말로 시키면 됩니다.

결과물은 유튜브에서 흔히 보는 "개념 설명 모션그래픽" 스타일 — 어두운 배경, 또렷한 글자, 나레이션에 맞춰 등장하는 도형·표·반응식.

## 4-2. 스킬 설치 (부록 A-6)

```
PS> cd C:\hyper
PS> npx skills add heygen-com/hyperframes --agent claude-code -y --copy
```

![HyperFrames 설치 명령 — 한 줄이면 끝](../captures/yt/04-01-hyperframes-cmd.jpg)

**이 화면이 나오면 성공**: 스킬 26개가 `✓ … (copied)` 로 쭉 설치되고 `Done!`. (실제 기록: `captures/04-01-npx-skills-add.txt`)

> 스킬 26개가 뭐냐면 — hyperframes(본체), hyperframes-core/animation/audio(규칙서), motion-graphics, faceless-explainer(설명 영상), embedded-captions(자막) … 클로드가 상황에 맞는 것을 알아서 골라 읽습니다. 선생님이 외울 필요 없습니다.

## 4-3. 예제 킷 받기

이 자료의 깃허브 저장소가 곧 **예제 킷**입니다. 5장의 화학변화 영상이 통째로 들어 있어서, 클로드가 "이렇게 만들면 되는구나"를 보고 따라 합니다.

```
PS> cd C:\hyper
PS> git clone https://github.com/kwakjanghun/lesson.git
PS> cd lesson\kit
PS> npx hyperframes check
```

**이 화면이 나오면 성공**:
```
◆  Checking kit
Lint      0 error(s)
Runtime   ◇ 0 errors, 0 warnings
Layout    ◇ 0 issues
Contrast  ◇ 53/53 text checks pass WCAG AA
◇  Check passed
```
처음 실행은 `npx` 가 hyperframes 패키지(0.8.x)를 내려받느라 1~2분 걸립니다. 두 번째부터는 몇 초.

![킷 첫 check 통과 화면](../captures/04-02-kit-check.txt)

### 킷 안에 뭐가 있나

| 파일/폴더 | 역할 | 선생님이 만질 일 |
|---|---|---|
| `CLAUDE.md` | 클로드가 읽는 **규칙서** (한글 경로 금지, 씬 작성 규칙, 검증 방법) | 없음 |
| `frame.md` | **디자인 시스템** (배경색 #0B1026, 강조색, 글꼴 크기) — 톤을 바꾸고 싶으면 이것만 | 가끔 |
| `scripts/make_narration.py` | 대본(SCENES) → 음성(edge-tts) + 타이밍 | 클로드가 대본 부분만 교체 |
| `scripts/make_narration_myvoice.py` | 같은 것, **내 목소리(Qwen3)** 판 | 6장 |
| `scripts/gen_scenes.py` | 타이밍에 맞춰 장면 HTML 10개 생성 | 클로드가 새 영상마다 새로 씀 |
| `scripts/wire_index.py` | 장면·음성을 `index.html`에 배선 | 없음 |
| `compositions/s01~s10.html` | 화학변화 예제의 장면 10개 | 참고용 |
| `script_chem_redox.md` | 예제 대본 전문 (사람이 읽는 용) | 참고용 |
| `source_text.md` | 예제의 PDF 추출 텍스트 | 참고용 |

## 4-4. 첫 렌더 (부록 A-7)

킷 안에서 12초짜리 예제 한 번 돌려 봅니다:
```
PS> npx hyperframes render -o test.mp4
```
**이 화면이 나오면 성공**:
```
  █████████████████████████  100%  Render complete
◇  C:\hyper\lesson\kit\test.mp4
   2.3 MB · 12.0s video · rendered in 19.9s
```
(실제 기록: `captures/04-03-first-render.txt`)

![첫 렌더 결과 프레임](../captures/04-03-first-render.png)

> 처음 렌더에서 "Chrome Headless Shell이 없다"고 하면 `npx hyperframes browser ensure` 한 번 (약 115MB, 최초 1회).
> 렌더 시간은 대략 **영상 길이의 1.3~1.5배**입니다. 6분 영상 → 8~9분.

## 4-5. 여기까지 오면

설치는 전부 끝났습니다. 이제부터는 **클로드에게 말로 시키는 것**만 남았습니다 — 5장.
