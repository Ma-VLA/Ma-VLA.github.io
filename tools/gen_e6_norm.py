# -*- coding: utf-8 -*-
"""E6 j5: a mechanically fixed joint meeting a percentile normalizer.

Every value is read from the v16 norm_stats that trained the representative
policy — assets/pi05_e6_v16_lora/Kyle-Riss/dobot_e6_pick_place_orange_v16/.
"""
import pathlib

OUT = pathlib.Path(__file__).parent / 'figs' / 'e6_norm.svg'

# (label, state q99-q01 in degrees, action delta q99-q01 in deg/frame)
ROWS = [("j1", 35.6602, 3.2852), ("j2", 42.7667, 2.6339), ("j3", 72.1240, 4.2894),
        ("j4", 54.2895, 3.5747), ("j5",  2.0420, 0.2448), ("j6", 35.6687, 3.2927)]
HL = "j5"

def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def bi(en, ko): return f'data-en="{esc(en)}" data-ko="{esc(ko)}"'

W, H = 1000, 268
LBL, GAP, R = 54, 58, 20
PANEL = (W - LBL - GAP - R) / 2
TOP, ROWH, BARH = 74, 26, 15

o = [f'<svg class="vz" viewBox="0 0 {W} {H}" role="img" xmlns="http://www.w3.org/2000/svg" '
     f'aria-label="E6 joint j5 spans two degrees across the dataset, so its per-frame delta range is one thirteenth of the other joints">']
o.append(f'<text class="vz-title" x="16" y="20" '
         f'{bi("A joint that does not move, divided by how little it moves","움직이지 않는 관절을, 움직이지 않는 만큼으로 나누기")}>'
         f'A joint that does not move, divided by how little it moves</text>')

heads = [(LBL, PANEL, max(r[1] for r in ROWS),
          "Joint span across the dataset", "데이터셋 전체 관절 가동 폭", "degrees", 1),
         (LBL + PANEL + GAP, PANEL, max(r[2] for r in ROWS),
          "Per-frame delta range — the divisor", "프레임당 델타 범위 — 나누는 값", "deg / frame", 2)]

for x0, pw, mx, en, ko, unit, col in heads:
    o.append(f'<text class="vz-lbl" x="{x0}" y="{TOP-24}" {bi(en, ko)}>{en}</text>')
    o.append(f'<text class="vz-sub" x="{x0}" y="{TOP-10}">{unit}</text>')
    for i, row in enumerate(ROWS):
        v, y = row[col], TOP + i*ROWH
        w = pw * v / mx
        hl = row[0] == HL
        o.append(f'<rect class="vz-track" x="{x0}" y="{y}" width="{pw:.1f}" height="{BARH}" rx="3"/>')
        o.append(f'<rect class="vz-seg vz1{"" if hl else " vz-dim"}" x="{x0}" y="{y}" '
                 f'width="{max(w,1.5):.1f}" height="{BARH}" rx="3">'
                 f'<title>{row[0]} · {v:.4g} {unit}</title></rect>')
        # 막대가 패널을 거의 채우면 라벨을 안으로 넣는다 — 밖에 두면 잘린다
        if w > pw - 42:
            o.append(f'<text class="vz-in" x="{x0+w-7:.1f}" y="{y+11.5}" text-anchor="end">{v:.4g}</text>')
        else:
            o.append(f'<text class="{"vz-val" if hl else "vz-sub"}" x="{x0+max(w,1.5)+7:.1f}" y="{y+11.5}">{v:.4g}</text>')

for i, row in enumerate(ROWS):
    y = TOP + i*ROWH
    cls = "vz-val" if row[0] == HL else "vz-rowlbl"
    o.append(f'<text class="{cls}" x="{LBL-10}" y="{y+11.5}" text-anchor="end">{row[0]}</text>')

y5 = TOP + 4*ROWH
o.append(f'<text class="vz-flag" x="{W-R}" y="{y5+11.5}" text-anchor="end">13.4x narrower</text>')
o.append(f'<text class="vz-note" x="16" y="{H-30}" '
         f'{bi("j5 is held near −88° by the arm geometry: it spans 2.0° across the whole dataset while the others span 35–72°. Its per-frame delta range is 0.245 against a median of 3.29.","j5는 팔 구조상 −88° 부근에 고정된다 — 전체 데이터셋에서 2.0°만 움직이는 동안 다른 관절은 35–72° 움직인다. 프레임당 델타 범위는 0.245로 중앙값 3.29 대비 13.4배 좁다.")}>'
         f'j5 is held near −88° by the arm geometry — 2.0° across the whole dataset against 35–72° for the others.</text>')
o.append(f'<text class="vz-note" x="16" y="{H-12}" '
         f'{bi("This model normalizes by the percentile range, not by standard deviation, so that 0.245 is the divisor: whatever jitter remains in a joint that barely moves is stretched to fill the same ±1 the working joints get.","이 모델은 표준편차가 아니라 백분위 범위로 정규화하므로 0.245가 나누는 값이 된다 — 거의 안 움직이는 관절에 남은 지터가 실제로 일하는 관절과 똑같은 ±1로 펴진다.")}>'
         f'The divisor is that 0.245 — jitter in a barely-moving joint is stretched to the same ±1 the working joints get.</text>')
o.append('</svg>')
OUT.write_text('\n'.join(o), encoding='utf-8')
print('wrote', OUT.name, OUT.stat().st_size, 'B')
