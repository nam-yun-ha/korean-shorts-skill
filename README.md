# korean-shorts

**한국어 나레이션 음원 하나로 9:16 세로 쇼츠 모션그래픽을 만드는 Claude Code 스킬.**

mp3 를 넣으면 전사 → 자막 분할 → 장면 구성 → 모션 → 렌더까지 끝난 **1080×1920 · 30fps MP4** 가 나온다.
외부 영상 클립을 쓰지 않는다. 화면의 모든 것을 HTML/SVG 로 직접 그린다.

---

## 언제 쓰나

부동산 · 금융 · 정책 안내처럼 **수치와 조건이 많은 한국어 대본**에 맞다.

- 지원금 · 한도 · 소득 기준처럼 숫자가 여러 개 나올 때
- "둘 중 하나만" / "A였는데 B가 됐다" 같은 조건 · 변화를 설명할 때
- 매번 비슷한 톤으로 뽑아야 하는 채널을 운영할 때

**안 맞는 경우** — 실사 영상 편집, 인터뷰 컷 편집, 음악 중심 영상. 이 스킬은 그래픽을 그리는 쪽이다.

---

## 설치

```bash
git clone https://github.com/nam-yun-ha/korean-shorts-skill.git ~/.claude/skills/korean-shorts
```

Windows(PowerShell):

```powershell
git clone https://github.com/nam-yun-ha/korean-shorts-skill.git "$env:USERPROFILE\.claude\skills\korean-shorts"
```

Claude Code 를 다시 켜면 `/korean-shorts` 로 뜬다.

---

## 쓰는 법

```
[음원 파일 경로]
영상 만들어줘
```

또는 `/korean-shorts`.

중간에 **자막 분할과 장면 구성을 한 번 보여주고 확인을 받는다.** 거기서 틀리면 이후가 통째로 헛돌기 때문이다.

---

## 준비물

| 도구 | 확인 |
|---|---|
| Node.js 18+ | `node -v` |
| Python 3.8+ | `python -V` |
| ffmpeg · ffprobe | `ffmpeg -version` |
| HyperFrames CLI | 자동 (`npx hyperframes@0.8.14`) |

**폰트는 이 저장소에 없다.** 직접 받아서 프로젝트의 `fonts/` 에 넣는다 —
[Noto Sans KR](https://fonts.google.com/noto/specimen/Noto+Sans+KR) 의 **Medium · Bold · Black**, 확장자는 `.otf`,
파일명은 `NotoSansKR-Medium.otf` / `-Bold.otf` / `-Black.otf`.

---

## 들어 있는 것

```
SKILL.md                     설명서 — 10단계 절차 · 규칙 · 자주 틀리는 지점
reference/STYLE-RULES.md     효과 28종 + 발동조건표 + 프레임 단위 실측값
assets/scene-template.html   장면 뼈대 (무대 · 자막 · 안전선 · 레이어 순서)
assets/chargen.py            3D 클레이 캐릭터 생성기 (4포즈, 순수 SVG)
assets/build.py              템플릿 → index.html 빌드 + id 중복 검사
assets/hyperframes.json      프로젝트 설정
```

---

## 이 스킬의 핵심

레퍼런스 영상 4편을 **프레임 단위로 실측**해서 만들었다. "몇 초에 무엇이 터진다"가 아니라
**"말이 어떤 상태일 때 무엇을 건다"** 는 발동조건으로 정리했기 때문에, 처음 보는 대본에도 적용된다.

세 가지 원칙 위에 서 있다.

1. **고정하는 것은 셋뿐** — 상단 안전선 `y≥120` · 하단 안전선 `y≤1600` · 자막 기준선 `y=1560`.
   그 사이 1480px 는 매 장면 새로 짠다. *자막이 움직이면 못 읽고, 자막 말고 전부 고정하면 슬라이드쇼가 된다.*
2. **캐릭터는 제3의 층** — 무대 · 주석 · 캐릭터가 서로 다른 팔레트를 가진다.
   *같은 색이면 같은 층으로 읽힌다.*
3. **캐릭터의 동작 벡터가 정보를 겨눈다** — 도식의 대각 반대편에 둔다.
   *옆에 세우는 것만으로는 "함께 있는" 것이지 "맞물린" 것이 아니다.*

`SKILL.md` 에는 **`check` 가 통과시키는데도 화면에 안 나오는 함정 5가지**가 정리돼 있다.
전부 실제로 겪고 렌더 프레임을 봐야만 잡힌 것들이다.

---

## 라이선스

MIT — [LICENSE](LICENSE) 참조.

폰트 · 음원 · 영상 등 저작권 자산은 포함하지 않는다. 사용자가 직접 준비한다.
