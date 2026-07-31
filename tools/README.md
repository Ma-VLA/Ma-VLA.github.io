# tools — 그림 생성기

사이트의 그림은 **PNG가 아니라 HTML 안에 인라인된 SVG**다. 그래야 라이트/다크 테마
토큰을 그대로 물려받고, 확대해도 안 깨지고, 언어 토글이 그림 안의 글자에도 걸린다.
대신 값이 바뀌면 손으로 SVG를 고쳐야 하는데 — 그러지 말라고 이 폴더가 있다.

GitHub Pages는 `tools/`를 서빙하지 않는다. 사이트에는 영향 없다.

## 쓰는 법

```bash
python3 tools/gen_lineage.py     # E6 결정 계보  → tools/figs/lineage.svg
python3 tools/gen_e7figs.py      # Stage 2B 4장  → tools/figs/*.svg
python3 tools/embed.py           # 위 결과를 해당 페이지에 밀어넣기
git diff --stat                  # 뭐가 바뀌었는지 반드시 확인하고
```

`embed.py`는 SVG의 `aria-label` 앞부분으로 대상을 찾는다. 그림이 페이지 안에서
자리를 옮겨도 연결이 안 끊긴다. 대신 **`aria-label`을 바꾸면 연결이 끊기니**
바꿀 거면 `embed.py`의 `TARGETS` 도 같이 고칠 것.

## 그림 5장과 그 값의 출처

| 파일 | 페이지 | 값의 출처 |
|---|---|---|
| `lineage.svg` | `technical/e6-policy-evolution.html#decision-lineage` | `src/openpi/training/config.py` 의 v1~v26 블록에서 직접 추출한 데이터셋명·LoRA 레이어 범위 |
| `a_budget.svg` | `projects/e7-xarm6-policy.html#prompt-contract` | E7 config 의 `image_keys`/`max_token_len`/`action_horizon` + `So400m/14` 에서 나오는 슬롯당 256 패치 |
| `b_prompt.svg` | 〃 | PaliGemma 토크나이저 직접 인코딩 (전 카테고리·목적지 최악값, BOS·개행 포함) |
| `c_wrap.svg` | `…#dataset-integrity-guards` | openpi 가 적용하는 백분위 정규화에서 유도. 기록된 std 15.5 를 15.478 로 재현 |
| `d_timing.svg` | `…#measured-on-the-training-server` | 청크 길이는 산술값, 86.5ms 는 **RTX A5000 실측** (로봇 아님 — 본문에 명시돼 있음) |

## 색을 바꾸려면

마크 색은 눈으로 고른 게 아니라 접근성 검증기를 통과시킨 값이다.

- 사이트 teal 은 이 명도에서 **채도 0.1 을 못 넘어 회색으로 읽힌다** → 데이터 마크에 쓰지 말 것
- 결과(성공/실패)를 빨강–노랑–초록으로 칠하지 말 것 → protan/deutan 에서 ΔE 3~6 으로 붕괴한다.
  결과는 같은 페이지의 F2 가 이미 담당한다
- `vz1/vz2/vz3` 은 all-pairs 검증을 두 모드 모두 통과한 3슬롯이다.
  라이트 모드 aqua 는 대비가 3:1 미만이라 **직접 라벨로 완화**하고 있으니 라벨을 지우지 말 것

바꿀 거면 dataviz 검증기를 사이트 표면(`#ffffff` / `#171e1b`)에 대고 두 모드 모두
통과시킨 값만 쓸 것.

## 확인용 PNG 렌더

SSH 환경이라 브라우저가 없다. SVG 는 CSS 클래스로 칠해지므로 그냥 렌더하면
전부 검게 나온다 — 속성을 인라인해서 렌더해야 한다. `cairosvg` 필요.

렌더 결과는 `/home/billy/26kp/` 에 둔다 (GUI 없는 환경의 관례).
