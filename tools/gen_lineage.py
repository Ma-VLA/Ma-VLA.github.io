# -*- coding: utf-8 -*-
"""E6 v1-v26 decision lineage figure. All values from src/openpi/training/config.py."""
import pathlib

OUT = pathlib.Path(__file__).parent / 'figs' / 'lineage.svg'

DATASETS = [  # (label, first_version, last_version)
    ("random_v1", 1, 1), ("orange_v2", 2, 5), ("orange_v6", 6, 7), ("orange_v8", 8, 9),
    ("orange_v10", 10, 12), ("orange_v13", 13, 13), ("orange_v14", 14, 15), ("orange_v16", 16, 26),
]
LORA = {v: (22, 26) for v in range(1, 17)}
LORA.update({17: (14, 25), 18: (0, 25), 19: (14, 18), 20: (19, 25), 21: (0, 8),
             22: (9, 17), 23: (18, 26), 24: (0, 26), 25: (15, 19), 26: (22, 25)})

W, H = 1000, 300
L, R = 96, 16                      # 왼쪽은 "Late 18–26"/"SigLIP layer" 라벨이 들어갈 폭
PLOT_W = W - L - R
SLOT = PLOT_W / 26
BAND_Y, BAND_H = 46, 26            # dataset lineage band
PB_TOP, PB_BOT = 108, 240          # layer-span panel
LAYER_MAX = 26

def x_of(v):        return L + (v - 1) * SLOT          # left edge of version v
def x_mid(v):       return x_of(v) + SLOT / 2
def y_of(layer):    return PB_BOT - layer * (PB_BOT - PB_TOP) / LAYER_MAX

o = []
a = o.append
a(f'<svg class="lineage" viewBox="0 0 {W} {H}" role="img" xmlns="http://www.w3.org/2000/svg" '
  f'aria-label="E6 v1-v26: dataset lineage above, SigLIP vision-LoRA layer range below">')

# ── SigLIP band guides (Early / Mid / Late) ──
for lo, hi, name in [(0, 8, "Early 0–8"), (9, 17, "Mid 9–17"), (18, 26, "Late 18–26")]:
    yt, yb = y_of(hi), y_of(lo)
    a(f'<rect class="ln-band" x="{L}" y="{yt:.1f}" width="{PLOT_W}" height="{yb-yt:.1f}"/>')
    a(f'<text class="ln-band-lbl" x="{L-8}" y="{(yt+yb)/2+3.5:.1f}" text-anchor="end">{name}</text>')

# ── phase divider between v16 and v17 ──
xd = x_of(17)
a(f'<line class="ln-divide" x1="{xd:.1f}" y1="22" x2="{xd:.1f}" y2="{PB_BOT+6}"/>')
a(f'<text class="ln-phase" x="{(L+xd)/2:.1f}" y="14" text-anchor="middle" '
  f'data-en="Phase 1 — the dataset moves, the config does not" '
  f'data-ko="1단계 — 데이터셋이 바뀌고, 설정은 고정">Phase 1 — the dataset moves, the config does not</text>')
a(f'<text class="ln-phase" x="{(xd+W-R)/2:.1f}" y="14" text-anchor="middle" '
  f'data-en="Phase 2 — the dataset is frozen, the range is swept" '
  f'data-ko="2단계 — 데이터셋이 고정되고, 범위를 훑음">Phase 2 — the dataset is frozen, the range is swept</text>')

# ── dataset lineage band ──
a(f'<text class="ln-axis" x="{L-8}" y="{BAND_Y+BAND_H/2+3.5}" text-anchor="end" '
  f'data-en="Dataset" data-ko="데이터셋">Dataset</text>')
for i, (name, v0, v1) in enumerate(DATASETS):
    x0 = x_of(v0) + 1                       # 2px surface gap between segments
    w = (v1 - v0 + 1) * SLOT - 2
    a(f'<rect class="ln-ds ln-ds{i%2}" x="{x0:.1f}" y="{BAND_Y}" width="{w:.1f}" height="{BAND_H}" rx="4"/>')
    if w >= 62:
        a(f'<text class="ln-ds-lbl" x="{x0+w/2:.1f}" y="{BAND_Y+BAND_H/2+3.5}" text-anchor="middle">{name}</text>')
    else:                                    # too narrow to hold text — offset with a leader
        xm = x0 + w / 2
        anchor, tx = ("middle", xm) if v0 > 1 else ("start", x0)
        a(f'<line class="ln-leader" x1="{xm:.1f}" y1="{BAND_Y-3}" x2="{xm:.1f}" y2="{BAND_Y-11}"/>')
        a(f'<text class="ln-ds-lbl ln-ds-lbl--out" x="{tx:.1f}" y="{BAND_Y-15}" text-anchor="{anchor}">{name}</text>')

# ── vision-LoRA layer spans ──
a(f'<text class="ln-axis" x="{L-8}" y="{PB_TOP+4}" text-anchor="end" '
  f'data-en="SigLIP layer" data-ko="SigLIP 레이어">SigLIP layer</text>')
BAR_W = SLOT * 0.58
for v in range(1, 27):
    lo, hi = LORA[v]
    xm, yt, yb = x_mid(v), y_of(hi), y_of(lo)
    cls = "ln-span ln-span--best" if v == 23 else "ln-span"
    a(f'<rect class="{cls}" x="{xm-BAR_W/2:.1f}" y="{yt:.1f}" width="{BAR_W:.1f}" '
      f'height="{max(yb-yt,3):.1f}" rx="4"><title>v{v} · SigLIP {lo}–{hi}</title></rect>')
a(f'<text class="ln-best-lbl" x="{x_mid(23):.1f}" y="{y_of(26)-9:.1f}" text-anchor="middle">v23 · 18–26</text>')

# ── version axis ──
for v in range(1, 27):
    if v in (1, 5, 10, 16, 20, 23, 26):
        a(f'<text class="ln-tick" x="{x_mid(v):.1f}" y="{PB_BOT+19}" text-anchor="middle">v{v}</text>')
a(f'<line class="ln-baseline" x1="{L}" y1="{PB_BOT+1}" x2="{W-R}" y2="{PB_BOT+1}"/>')
a(f'<text class="ln-axis" x="{L}" y="{H-10}" data-en="Policy version" data-ko="정책 버전">Policy version</text>')
a('</svg>')

OUT.write_text('\n'.join(o), encoding='utf-8')
print('\n'.join(o)[:400])
print(f'\n… {len(o)} elements')
