# -*- coding: utf-8 -*-
"""Where the E6 training loss actually goes, by action dimension.

Measured on the representative v23 checkpoint with scripts/perdim_loss.py in
the training repo: 6 batches of 8, horizon 16, bfloat16. The script replicates
compute_loss and stops before the mean over the action dimension.
"""
import pathlib

OUT = pathlib.Path(__file__).parent / 'figs' / 'perdim.svg'

REAL = [("j1", 0.03603), ("j2", 0.07115), ("j3", 0.08259), ("j4", 0.09796),
        ("j5", 0.13174), ("j6", 0.04359), ("gripper", 0.04960)]
PAD_MEAN, PAD_SUM, REAL_SUM = 0.00019, 0.00478, 0.51266
HL = "j5"

def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def bi(en, ko): return f'data-en="{esc(en)}" data-ko="{esc(ko)}"'

W, H, L, R = 1000, 320, 92, 152
PW = W - L - R
TOP, ROWH, BARH = 56, 25, 16
mx = max(v for _, v in REAL)

o = [f'<svg class="vz" viewBox="0 0 {W} {H}" role="img" xmlns="http://www.w3.org/2000/svg" '
     f'aria-label="Per-dimension training loss on the representative checkpoint: j5 is the largest single share and the 25 padding dimensions are under one percent">']
o.append(f'<text class="vz-title" x="16" y="20" '
         f'{bi("Where the training loss goes, dimension by dimension","학습 loss가 차원별로 어디로 가는가")}>'
         f'Where the training loss goes, dimension by dimension</text>')
o.append(f'<text class="vz-sub" x="16" y="38" '
         f'{bi("mean squared error per dimension · v23 checkpoint · 6 batches of 8 · horizon 16","차원별 평균제곱오차 · v23 체크포인트 · 6배치×8 · horizon 16")}>'
         f'mean squared error per dimension · v23 checkpoint · 6 batches of 8</text>')

for i, (name, v) in enumerate(REAL):
    y = TOP + i*ROWH
    hl = name == HL
    w = PW * v / mx
    o.append(f'<text class="{"vz-val" if hl else "vz-rowlbl"}" x="{L-10}" y="{y+12}" text-anchor="end">{name}</text>')
    o.append(f'<rect class="vz-track" x="{L}" y="{y}" width="{PW:.1f}" height="{BARH}" rx="3"/>')
    o.append(f'<rect class="vz-seg vz1{"" if hl else " vz-dim"}" x="{L}" y="{y}" width="{w:.1f}" height="{BARH}" rx="3">'
             f'<title>{name} · {v:.5f} · {v/REAL_SUM*100:.1f}% of the real-dimension loss</title></rect>')
    if w > PW - 56:   # 막대가 트랙을 거의 채우면 밖에 둘 자리가 없다
        o.append(f'<text class="vz-in" x="{L+w-8:.1f}" y="{y+12}" text-anchor="end">{v:.5f}</text>')
    else:
        o.append(f'<text class="{"vz-val" if hl else "vz-sub"}" x="{L+w+8:.1f}" y="{y+12}">{v:.5f}</text>')
    o.append(f'<text class="{"vz-flag" if hl else "vz-sub"}" x="{W-R+62}" y="{y+12}" text-anchor="end">{v/REAL_SUM*100:.1f}%</text>')

o.append(f'<text class="vz-sub" x="{W-R+62}" y="{TOP-8}" text-anchor="end" '
         f'{bi("share of real-dim loss","실제 차원 loss 중 비중")}>share of real-dim loss</text>')

# the 25 padding dimensions, on the same scale
yp = TOP + len(REAL)*ROWH + 14
o.append(f'<line class="vz-grid" x1="{L-46}" y1="{yp-7}" x2="{W-R+62}" y2="{yp-7}"/>')
w = max(PW * PAD_MEAN / mx, 1.5)
o.append(f'<text class="vz-rowlbl" x="{L-10}" y="{yp+12}" text-anchor="end" '
         f'{bi("25 pad","패딩 25")}>25 pad</text>')
o.append(f'<rect class="vz-track" x="{L}" y="{yp}" width="{PW:.1f}" height="{BARH}" rx="3"/>')
o.append(f'<rect class="vz-seg vz2" x="{L}" y="{yp}" width="{w:.1f}" height="{BARH}" rx="3">'
         f'<title>25 padding dimensions · mean {PAD_MEAN:.5f} each · {PAD_SUM:.5f} in total</title></rect>')
o.append(f'<text class="vz-sub" x="{L+w+8:.1f}" y="{yp+12}">{PAD_MEAN:.5f} each</text>')
o.append(f'<text class="vz-flag" x="{W-R+62}" y="{yp+12}" text-anchor="end">0.92% of all</text>')

o.append(f'<text class="vz-note" x="16" y="{H-30}" '
         f'{bi("The action space is 32 wide and the robot has 7 dimensions. The 25 padding dimensions carry 0.92% of the reported loss — the real dimensions average 383 times more — so the padding is close to free and replacing the head with a native 7-dimensional one has almost nothing to recover.","액션 공간은 32차원이고 로봇은 7차원이다. 패딩 25차원이 보고된 loss의 0.92%를 차지하고 실제 차원은 평균 383배 크다 — 즉 패딩은 사실상 공짜이고, 헤드를 native 7차원으로 교체해도 되찾을 게 거의 없다.")}>'
         f'The 25 padding dimensions carry 0.92% of the loss; the real dimensions average 383× more.</text>')
o.append(f'<text class="vz-note" x="16" y="{H-12}" '
         f'{bi("j5 is the largest single share at 25.7%, and it is the joint the arm holds mechanically fixed — the normalizer divides it by a range 13.4 times narrower than the other joints.","j5가 25.7%로 단독 최대인데, 이 관절은 팔이 기계적으로 고정하고 있는 관절이다 — 정규화가 다른 관절보다 13.4배 좁은 범위로 나눈다.")}>'
         f'j5 is the largest single share at 25.7% — and it is the joint held mechanically fixed.</text>')
o.append('</svg>')
OUT.write_text('\n'.join(o), encoding='utf-8')
print('wrote', OUT.name, OUT.stat().st_size, 'B')
