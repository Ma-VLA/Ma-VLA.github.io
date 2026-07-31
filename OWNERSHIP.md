# 편집 소유권 규약 (Editing ownership)

이 사이트는 **서로 다른 머신의 세션이 각각 자기가 검증한 내용만** 올린다.
한쪽이 다른 쪽 근거를 고치면, 그 문장을 뒷받침하는 실측이 사라진 채 문장만 남는다.
그래서 HTML 안에 소유권 블록을 주석으로 표시한다.

## 마커 형식

```html
<!-- ═══ OWNER: TRAINING-SERVER (RTX A5000) · DO NOT EDIT ═══
     ... 설명 ...
═══ END OWNER: TRAINING-SERVER ═══ -->
```

`OWNER:` 와 `END OWNER:` 사이의 모든 것은 **그 소유자만 수정한다.**

## 소유자

| 소유자 | 머신 | 올릴 수 있는 것 |
|---|---|---|
| `TRAINING-SERVER` | RTX A5000 | 학습 config, 변환기·가드, 프롬프트 계약, ablation 근거, **A5000에서 잰 수치** |
| `JETSON` | AGX Orin 64GB | ROS2 노드 그래프, 수집 실측, executor timing, **온디바이스에서 잰 수치** |
| `SHARED` | — | 양쪽이 추가는 하되 구조는 바꾸지 않음 (예: `contents.html` 색인 항목) |

## 다른 소유자의 블록에 할 말이 있을 때

고치지 말고 **자기 소유 블록을 새로 만들어 옆에 붙인다.** 예를 들어 추론 지연은
현재 A5000 실측치만 있고 Jetson 측정치는 없다고 명시되어 있다. Jetson에서 재고 나면
그 문장을 덮어쓰지 말고 `OWNER: JETSON` 블록을 새로 열어 온디바이스 수치를 추가하면 된다.
두 수치가 나란히 있는 편이 정확하다 — 하나는 학습 서버, 하나는 로봇이다.

내용이 실제로 **틀렸다면** 고쳐도 된다. 다만 커밋 메시지에 어느 소유자의 블록을
왜 고쳤는지 쓴다.

## 현재 소유 현황

| 파일 | 소유 |
|---|---|
| `projects/e7-xarm6-policy.html` | 전체 `TRAINING-SERVER` |
| `technical/e6-policy-evolution.html` | `#training-diagnostics`, `#vision-lora-ablation` 블록만 `TRAINING-SERVER`. 나머지 기존 내용은 그대로 |
| `transitions/e6-to-xarm6.html` | embodiment 표 + `#stage-2b` 블록만 `TRAINING-SERVER` |
| `research.html` | Stage 2B 노드 + `#stage-2b` 블록만 `TRAINING-SERVER` |
| `index.html` | Stage 2B 노드만 `TRAINING-SERVER` |
| `contents.html` | `SHARED` — 페이지·섹션이 늘면 항목을 추가할 것 |
| `projects/quest3-xarm6.html` | `JETSON` (수집 인프라·실측) |
| `system/e6-vla-inference.html` | `JETSON` (ROS2 런타임) |

## 앵커

모든 `<section>`에 `id`가 있다. 딥링크와 `contents.html` 색인이 이걸 쓴다.
**id는 바꾸지 말 것** — 외부 링크와 색인이 동시에 깨진다. 섹션을 추가하면 id도 새로 붙인다.
