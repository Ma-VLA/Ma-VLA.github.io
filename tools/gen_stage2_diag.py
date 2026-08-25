# -*- coding: utf-8 -*-
"""Stage 2 diagnosis figures (2026-08-21 ~ 08-25).

두 장이다.

  f_interventions.svg  네 개의 개입 중 무엇이 행동을 움직였나 — 홀드아웃 30 에피소드
  g_selectivity.svg    질의가 세 카드를 어떻게 흔드나 — 의미로 흔드나, 자리로 흔드나

값의 출처는 전부 `docs/stage2_mcp/GLYPH_GROUNDING_INVESTIGATION.md` (학습 repo) 의
§11.9 진단 v1 FREEZE 와 §11.11 selectivity 다. 두 장 모두 홀드아웃 30 에피소드,
에피소드마다 자기 세 목적지 평균으로 센터링한 잣대를 쓴다(통제 조건이 0 을 돌려준다).

색은 dataviz 검증기를 통과한 vz1/vz2/vz3 만 쓴다 — tools/README.md 참고.
"""
import pathlib

OUT = pathlib.Path(__file__).parent / 'figs'
OUT.mkdir(exist_ok=True)
def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def bi(en, ko): return f'data-en="{esc(en)}" data-ko="{esc(ko)}"'

# ══════════════ F. 무엇이 행동을 움직였나 ══════════════
# (라벨, 한국어, n_of_30, 검출됐나)  — R2 / R3 / R4 / R5
ROWS = [
    ("the whole sign view",   "간판 뷰 전체",     28, True,  "p = 4.3e-07"),
    ("only the printed words","인쇄된 글자만",     16, False, "not detected"),
    ("the category named",    "지시문의 카테고리", 15, False, "null"),
    ("the phase word",        "지시문의 phase 단어", 24, True, "cos +0.54"),
]
W, H, L, R = 1000, 250, 210, 215
PW = W - L - R
o = [f'<svg class="vz" viewBox="0 0 {W} {H}" role="img" xmlns="http://www.w3.org/2000/svg" '
     f'aria-label="Which interventions moved the arm along its own destination axis, out of thirty held-out episodes">']
o.append(f'<text class="vz-title" x="16" y="20" '
         f'{bi("Change one thing, and see if the arm turns","하나만 바꾸고 팔이 도는지 본다")}>'
         f'Change one thing, and see if the arm turns</text>')
o.append(f'<text class="vz-total" x="{W-16}" y="20" text-anchor="end" '
         f'{bi("30 held-out episodes","홀드아웃 30 에피소드")}>30 held-out episodes</text>')
TOP, ROW = 48, 40
# 우연 수준(15/30) 기준선
cx = L + PW * 15/30
o.append(f'<line class="vz-axis" x1="{cx:.1f}" y1="{TOP-6}" x2="{cx:.1f}" y2="{TOP+len(ROWS)*ROW-8}" '
         f'stroke-dasharray="3 3"/>')
o.append(f'<text class="vz-sub" x="{cx:.1f}" y="{TOP-12}" text-anchor="middle" '
         f'{bi("chance","우연")}>chance</text>')
for i,(en,ko,n,ok,note) in enumerate(ROWS):
    y = TOP + i*ROW
    o.append(f'<rect class="vz-track" x="{L}" y="{y}" width="{PW}" height="22" rx="4"/>')
    w = PW * n/30
    o.append(f'<rect class="vz-seg {"vz1" if ok else "vz2"}" x="{L}" y="{y}" width="{w:.1f}" height="22" rx="4">'
             f'<title>{esc(en)} · {n} of 30</title></rect>')
    o.append(f'<text class="vz-rowlbl" x="{L-12}" y="{y+16}" text-anchor="end" {bi(en,ko)}>{esc(en)}</text>')
    o.append(f'<text class="vz-val" x="{L+PW+10}" y="{y+16}">{n}/30</text>')
    o.append(f'<text class="vz-sub" x="{L+PW+64}" y="{y+16}" {bi(note,note)}>{esc(note)}</text>')
o.append(f'<text class="vz-note" x="16" y="{TOP+len(ROWS)*ROW+22}" '
         f'{bi("Read as a direction, not a size: the question is whether the action moves along that episode’s own destination axis. A size test on the same data cannot tell these four apart.","크기가 아니라 방향으로 읽습니다 — 행동이 그 에피소드 자신의 목적지 축을 따라 움직이는가를 묻습니다. 같은 데이터에 크기 검정을 걸면 이 넷이 구분되지 않습니다.")}>'
         f'Read as a direction, not a size — a size test cannot tell these four apart.</text>')
o.append('</svg>')
(OUT/'f_interventions.svg').write_text('\n'.join(o), encoding='utf-8')

# ══════════════ G. 질의가 세 카드를 어떻게 흔드나 ══════════════
# §11.11 selectivity, layer 14. 역할별(무슨 단어가 적혔나) vs 물리 위치별.
BY_ROLE = [("the card holding the named word","지목된 단어가 적힌 카드",0.22042),
           ("the card holding the other word","다른 단어가 적힌 카드",0.22615),
           ("the remaining card","나머지 카드",0.22819)]
BY_POS  = [("left","왼쪽",0.2200), ("centre","가운데",0.2314), ("right","오른쪽",0.2234)]
W, H, L, R = 1000, 318, 250, 120
PW = W - L - R
MAX = 0.24
o = [f'<svg class="vz" viewBox="0 0 {W} {H}" role="img" xmlns="http://www.w3.org/2000/svg" '
     f'aria-label="When the instruction names a different category, all three cards are disturbed alike; what separates them is position">']
o.append(f'<text class="vz-title" x="16" y="20" '
         f'{bi("Name a different category, and see which card reacts","다른 카테고리를 지목하고 어느 카드가 반응하는지 본다")}>'
         f'Name a different category, and see which card reacts</text>')
def group(o, top, rows, cls, head_en, head_ko):
    o.append(f'<text class="vz-lbl" x="16" y="{top-8}" {bi(head_en,head_ko)}>{esc(head_en)}</text>')
    for i,(en,ko,v) in enumerate(rows):
        y = top + i*30
        o.append(f'<rect class="vz-track" x="{L}" y="{y}" width="{PW}" height="20" rx="4"/>')
        w = PW * v/MAX
        o.append(f'<rect class="vz-seg {cls}" x="{L}" y="{y}" width="{w:.1f}" height="20" rx="4">'
                 f'<title>{esc(en)} · {v:.5f}</title></rect>')
        o.append(f'<text class="vz-rowlbl" x="{L-12}" y="{y+15}" text-anchor="end" {bi(en,ko)}>{esc(en)}</text>')
        o.append(f'<text class="vz-val" x="{L+w+10:.1f}" y="{y+15}">{v:.3f}</text>')
group(o, 66, BY_ROLE, "vz2", "by what is written on it", "무엇이 적혀 있나로 나누면")
group(o, 186, BY_POS, "vz1", "by where it sits", "어디에 놓였나로 나누면")
o.append(f'<text class="vz-note" x="16" y="290" '
         f'{bi("Same three cards, grouped two ways. Grouped by meaning they agree to three decimals; grouped by position the middle one moves most, in every arrangement. The query reaches the picture and moves it — by position, not by meaning.","같은 세 카드를 두 가지로 묶었습니다. 의미로 묶으면 소수점 셋째 자리까지 같고, 위치로 묶으면 어느 배치에서든 가운데가 가장 크게 움직입니다. 질의는 그림에 닿아 그것을 흔들되, 의미가 아니라 위치로 흔듭니다.")}>'
         f'Grouped by meaning they agree to three decimals; grouped by position the middle one moves most.</text>')
o.append(f'<text class="vz-sub" x="16" y="308" '
         f'{bi("Relative change in the sign view’s internal state at layer 14, 60 query pairs over 30 held-out episodes.","14층에서 간판 뷰 내부 상태의 상대 변화. 홀드아웃 30 에피소드에 질의 쌍 60개.")}>'
         f'Relative change at layer 14, 60 query pairs over 30 held-out episodes.</text>')
o.append('</svg>')
(OUT/'g_selectivity.svg').write_text('\n'.join(o), encoding='utf-8')
print("wrote f_interventions.svg, g_selectivity.svg")
