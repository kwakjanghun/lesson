# 마무리

## 오늘 한 것

```
설치 (2장)  →  보기 watch (3장)  →  만들기 HyperFrames (4장)  →  영상 한 편 (5장)  →  내 목소리 (6장)
```

한 번 깔아 두면, 다음부터는 **"PDF 주고 30분"** 입니다. 대본은 교과서에서, 화면은 클로드가, 목소리는 선생님이.

## 이 자료의 모든 것은 여기에

- **저장소**: {{REPO_URL}}
  - `guide/` 이 PDF · `manuscript/` 원고 · `kit/` 화학변화 예제 킷(바로 실행됨) · `captures/` 실제 화면 · `manuscript/prompts.md` 복붙 프롬프트
- **완성 영상**: {{VIDEO_URL}}
  - 기본 목소리(edge-tts) 판 / 내 목소리(Qwen3) 판 / 인트로

{{QR_REPO}}

## 다음에 해 볼 것

1. 나머지 소단원(산·염기·중화 / 물질 변화와 에너지) — 같은 PDF, 같은 프롬프트, 범위만 바꿔서
2. 자막 — "embedded-captions 스킬로 자막 넣어 줘"
3. 학생용 짧은 버전 — "시험 포인트 장면만 1분 숏폼으로 9:16"
4. 실험 영상 끼워 넣기 — 직접 찍은 mp4를 장면 사이에 (킷의 `assets/video/` 방식)

## 문의

곽장훈 · 숭신고등학교 · kwakja@ssgh.hs.kr
저장소 Issues 에 남겨 주셔도 됩니다. 막힌 화면을 캡처해서 보내 주시면 같이 봅니다.

---

# 부록 B. 실제 제작 사례 — ESP32 코드해설 영상 14편

같은 파이프라인으로 만든 「사물인터넷과 센서 제어」(2학년) 코드해설 영상입니다. 2026-08-14~15 이틀 동안 아래 14편(총 83분)을 제작했고, 그중 8편은 **하루 만에 대본 → 내 목소리 → 렌더 → 납품**했습니다.

| 챕터 | 길이 | 챕터 | 길이 |
|---|---|---|---|
| 02 개발환경과 첫 프로젝트 | 5:22 | 11 아날로그 입력 | 7:01 |
| 03 LED 기초 | 7:02 | 12 소리 센서 | 6:47 |
| 04 RGB LED | 6:42 | 13 온습도 센서 | 5:15 |
| 05 소리 | 5:00 | 14 초음파 거리 측정 | 5:18 |
| 06 디스플레이 | 5:21 | 15 스마트 주차 시스템 | 5:31 |
| 07 LCD와 서보모터 | 7:06 | 16 적외선 리모컨 | 5:20 |
| 08 버튼 입력 | 6:36 | | |
| 09 게임 만들기 | 4:50 | | |

코드 영상은 "코드 한 줄 한 줄 하이라이트 + 설명" 형식이라 장면 생성기(`gen_scenes.py`)가 다릅니다. 그 킷은 개인 스킬 `allinone` 으로 만들어 두었고, 이 자료의 개념 영상 킷(`lesson/kit`)과 **대본·음성·렌더 파이프라인은 같습니다**. 즉 과목이 무엇이든 "대본 → 음성 실측 → 장면 → 검사 → 렌더"만 지키면 됩니다.

---

# 부록 C. 출처·라이선스

| 항목 | 출처 / 라이선스 |
|---|---|
| HyperFrames | HeyGen, Apache 2.0 — https://github.com/heygen-com/hyperframes |
| HyperFrames 한국어 스타터 킷 | philosophyAIEDU/260731eduhyper (필로소피 AI 교육) — https://github.com/philosophyAIEDU/260731eduhyper. 유튜브 「HyperFrames로 수업 자료 만드는 방법」 https://www.youtube.com/watch?v=HGLhfRkfANA |
| watch 스킬 | bradautomates/claude-video, MIT |
| `npx skills` | Vercel skills CLI, https://skills.sh |
| Qwen3-TTS | Alibaba Qwen, Apache 2.0 — Qwen/Qwen3-TTS-12Hz-1.7B-Base |
| edge-tts | Microsoft Edge 읽기 음성 (개인·교육용 무료), `ko-KR-InJoonNeural` |
| Pretendard 글꼴 | SIL OFL 1.1 / JetBrains Mono, OFL |
| kaggle-tts 스킬 | 곽장훈 자체 제작. 방식 참고: 방구석컴퍼니 유튜브(aTtnuVokUNk) |
| 2·3·4장 단계 카드 그림 | 곽장훈 자체 제작 「교사용_설치안내영상.mp4」에서 watch 스킬로 추출 (`captures/yt/SOURCES.md`) |
| 설치 사이트 화면 | nodejs.org, claude.ai/download (2026-08-19 캡처) |
| 교과 내용 | 「통합과학2 Ⅲ. 변화와 다양성 — 1. 화학 변화 (교사용)」 학습지, 숭신고 |
| 이 자료 | 곽장훈(숭신고), 2026-08. 자유롭게 복제·수정·배포 가능 (CC BY 4.0). 영상·원고의 교과 내용은 교과서 저작권을 따릅니다 |
