# -*- coding: utf-8 -*-
"""Stage 2 선택기 진단 그림 한 장 (2026-09-09).

  h_frozen.svg  단어를 바꾸면 고르는 간판도 따라 바뀌는가 — 굳은 답이 냈을 값과 나란히

왜 이 그림인가: 이 페이지에서 글로만 읽으면 제일 안 와닿는 것이 **"굳은 답 기준선"** 이다.
간판이 셋이고 분야가 셋이며 분야마다 정답 간판이 다르므로, 답이 완전히 굳어 있어도 셋 중
하나에서는 저절로 맞는다. 그 기준선을 안 그리면 기준선의 29/58 을 "절반은 따라간다"로
읽게 되고 진단이 반대로 간다.

값의 출처는 `docs/stage2_mcp/E7_FULL_AUDIT_20260827.md` §37.3 · §37.4 (학습 repo).
전부 JAX · 학습서버 실측이고 변환기를 거치지 않았다.

색은 dataviz 검증기를 통과한 vz1/vz2 만 쓴다 — tools/README.md 참고.
"""
import pathlib

OUT = pathlib.Path(__file__).parent / 'figs'
OUT.mkdir(exist_ok=True)
def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def bi(en, ko): return f'data-en="{esc(en)}" data-ko="{esc(ko)}"'

# (영문 라벨, 한국어 라벨, 실측, 굳은 답이었다면, 분모, 처치군인가)
ROWS = [
    ("Baseline · held-out",  "기준선 · 시험용",  29,  28,  58, False),
    ("Baseline · training",  "기준선 · 학습",     0,   0, 168, False),
    ("Repaired · held-out",  "처치 후 · 시험용", 54,  19,  58, True),
    ("Repaired · training",  "처치 후 · 학습",   90,   0, 168, True),
]

W, H, L, R = 1000, 300, 232, 210
PW = W - L - R
TOP, ROW = 74, 44

o = [f'<svg class="vz" viewBox="0 0 {W} {H}" role="img" xmlns="http://www.w3.org/2000/svg" '
     f'aria-label="How often the chosen sign follows the swapped word, printed beside what a frozen answer would give">']
o.append(f'<text class="vz-title" x="16" y="20" '
         f'{bi("Swap the word, and see if the chosen sign follows","단어를 바꾸고 고르는 간판이 따라오는지 본다")}>'
         f'Swap the word, and see if the chosen sign follows</text>')
o.append(f'<text class="vz-sub" x="16" y="40" '
         f'{bi("A part that always answers the same thing is still right on one of the three signs — that is the hollow marker, not zero.","늘 같은 답만 내는 부품도 세 간판 중 하나에서는 저절로 맞습니다 — 그 값이 빈 표식이고, 0 이 아닙니다.")}>'
         f'A part that never moves is still right on one sign in three — that is the hollow marker.</text>')

for i,(en,ko,got,frozen,n,treat) in enumerate(ROWS):
    y = TOP + i*ROW
    o.append(f'<rect class="vz-track" x="{L}" y="{y}" width="{PW}" height="22" rx="4"/>')
    w = PW * got/n
    o.append(f'<rect class="vz-seg {"vz1" if treat else "vz2"}" x="{L}" y="{y}" width="{w:.1f}" height="22" rx="4">'
             f'<title>{esc(en)} · {got} of {n}</title></rect>')
    # 굳은 답이었다면 — 속 빈 표식. 막대와 같은 축 위에 놓아야 눈으로 바로 견줘진다.
    fx = L + PW * frozen/n
    o.append(f'<line class="vz-axis" x1="{fx:.1f}" y1="{y-5}" x2="{fx:.1f}" y2="{y+27}" stroke-dasharray="3 3"/>')
    o.append(f'<circle class="vz-axis" cx="{fx:.1f}" cy="{y+11}" r="5" fill="none"/>')
    o.append(f'<text class="vz-rowlbl" x="{L-12}" y="{y+16}" text-anchor="end" {bi(en,ko)}>{esc(en)}</text>')
    o.append(f'<text class="vz-val" x="{L+PW+12}" y="{y+16}">{got}/{n}</text>')
    o.append(f'<text class="vz-sub" x="{L+PW+78}" y="{y+16}" '
             f'{bi(f"frozen {frozen}", f"굳은 답 {frozen}")}>frozen {frozen}</text>')

o.append(f'<text class="vz-note" x="16" y="{TOP+len(ROWS)*ROW+22}" '
         f'{bi("The two baseline rows sit on their own marker: the answer did not move at all. After the repair the bar clears the marker on both sets — the word is now being read. It is still read only for the pairings of sign arrangement and category that training contained.","기준선 두 행은 자기 표식 위에 그대로 앉아 있습니다 — 답이 전혀 움직이지 않았습니다. 처치 후에는 두 집합 모두 막대가 표식을 넘어섭니다. 단어를 읽고 있다는 뜻입니다. 다만 학습에 들어 있던 간판 배치와 분야의 짝에 한해서입니다.")}>'
         f'The baseline rows sit on their own marker — the answer did not move at all.</text>')
o.append(f'<text class="vz-sub" x="16" y="{TOP+len(ROWS)*ROW+42}" '
         f'{bi("Held-out episodes, 29 of them, contribute two swaps each; training episodes, 84, contribute two each. Measured in JAX on the training server.","시험용 에피소드 29개가 각각 두 번씩, 학습 에피소드 84개가 각각 두 번씩 기여합니다. 학습서버의 JAX 실측입니다.")}>'
         f'29 held-out and 84 training episodes, two swaps each. Measured in JAX.</text>')
o.append('</svg>')
(OUT/'h_frozen.svg').write_text('\n'.join(o), encoding='utf-8')
print("wrote", OUT/'h_frozen.svg')
