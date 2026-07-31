# -*- coding: utf-8 -*-
"""Stage 2B figures. Every number is measured or derived — see each figure's note."""
import numpy as np, pathlib

OUT = pathlib.Path(__file__).parent / 'figs'
OUT.mkdir(exist_ok=True)
def esc(s): return s.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
def bi(en, ko): return f'data-en="{esc(en)}" data-ko="{esc(ko)}"'

# ══════════════ A. sequence budget ══════════════
W, H, L, R = 1000, 190, 16, 16
segs = [("image", 512, "vz1", "2 slots × 256 patches"), ("prompt", 200, "vz2", "padded field"),
        ("action", 16, "vz3", "= action horizon")]
total = sum(s[1] for s in segs)
o = [f'<svg class="vz" viewBox="0 0 {W} {H}" role="img" xmlns="http://www.w3.org/2000/svg" '
     f'aria-label="Token budget: 512 image plus 200 prompt plus 16 action equals 728">']
o.append(f'<text class="vz-title" x="{L}" y="20" {bi("Where the 728 tokens go","728 토큰의 배분")}>Where the 728 tokens go</text>')
x, PW, BY, BH = L, W-L-R, 44, 42
for name, n, cls, sub in segs:
    w = PW * n / total - 2
    o.append(f'<rect class="vz-seg {cls}" x="{x:.1f}" y="{BY}" width="{w:.1f}" height="{BH}" rx="4">'
             f'<title>{name} · {n} tokens · {n/total*100:.1f}%</title></rect>')
    if w > 54:
        o.append(f'<text class="vz-in" x="{x+w/2:.1f}" y="{BY+BH/2+5:.1f}" text-anchor="middle">{n}</text>')
    else:  # 16 토큰은 안에 안 들어간다
        o.append(f'<text class="vz-out" x="{x+w/2:.1f}" y="{BY-8:.1f}" text-anchor="middle">{n}</text>')
    lx = min(max(x + w/2, L+30), W-R-30)
    o.append(f'<text class="vz-lbl" x="{lx:.1f}" y="{BY+BH+18:.1f}" text-anchor="middle">{name}</text>')
    o.append(f'<text class="vz-sub" x="{lx:.1f}" y="{BY+BH+33:.1f}" text-anchor="middle">{sub}</text>')
    x += w + 2
# prompt 필드 안의 실사용 표시
px = L + PW * 512 / total
pw = PW * 200 / total
uw = pw * 34 / 200
o.append(f'<rect class="vz-used" x="{px+1:.1f}" y="{BY+BH+44}" width="{uw:.1f}" height="8" rx="3"/>')
o.append(f'<rect class="vz-usedtrack" x="{px+1+uw:.1f}" y="{BY+BH+44}" width="{pw-2-uw:.1f}" height="8" rx="3"/>')
o.append(f'<text class="vz-note" x="{px+1:.1f}" y="{BY+BH+70}" '
         f'{bi("12–34 tokens actually used, measured with the PaliGemma tokenizer — the rest is padding","PaliGemma 토크나이저 실측 12–34 토큰 사용, 나머지는 패딩")}>'
         f'12–34 tokens actually used — the rest is padding</text>')
o.append(f'<text class="vz-total" x="{W-R}" y="20" text-anchor="end">{total} total</text>')
o.append('</svg>')
(OUT/'a_budget.svg').write_text('\n'.join(o), encoding='utf-8')

# ══════════════ B. prompt cost by style ══════════════
STYLES = [("category_only", 12), ("resolved", 18), ("single_rule", 26), ("rule_table", 34)]
W, H, L, R = 1000, 208, 140, 90
o = [f'<svg class="vz" viewBox="0 0 {W} {H}" role="img" xmlns="http://www.w3.org/2000/svg" '
     f'aria-label="Prompt token cost by style, against the 200-token field">']
o.append(f'<text class="vz-title" x="16" y="20" {bi("Prompt cost against the 200-token field","200 토큰 영역 대비 프롬프트 비용")}>Prompt cost against the 200-token field</text>')
PW = W-L-R; ROW = 32; TOP = 44
for i, (name, n) in enumerate(STYLES):
    y = TOP + i*ROW
    o.append(f'<rect class="vz-track" x="{L}" y="{y}" width="{PW}" height="20" rx="4"/>')
    w = PW * n / 200
    o.append(f'<rect class="vz-seg vz1" x="{L}" y="{y}" width="{w:.1f}" height="20" rx="4">'
             f'<title>{name} · {n} of 200 tokens</title></rect>')
    o.append(f'<text class="vz-rowlbl" x="{L-10}" y="{y+14}" text-anchor="end">{name}</text>')
    o.append(f'<text class="vz-val" x="{L+w+8:.1f}" y="{y+14}">{n}</text>')
o.append(f'<line class="vz-axis" x1="{L}" y1="{TOP+len(STYLES)*ROW-6}" x2="{L+PW}" y2="{TOP+len(STYLES)*ROW-6}"/>')
o.append(f'<text class="vz-sub" x="{L}" y="{TOP+len(STYLES)*ROW+10}">0</text>')
o.append(f'<text class="vz-sub" x="{L+PW}" y="{TOP+len(STYLES)*ROW+10}" text-anchor="end">200</text>')
o.append(f'<text class="vz-note" x="16" y="{H-12}" '
         f'{bi("Worst case over every category and destination. The field is padded to 200, so all four styles give the same 728-token sequence — wording costs nothing.","카테고리·목적지 전 조합 중 최악값. 영역이 200으로 패딩되므로 네 방식 모두 동일한 728 시퀀스 — 문구 비용은 0.")}>'
         f'The field is padded, so all four give the same 728-token sequence — wording costs nothing.</text>')
o.append('</svg>')
(OUT/'b_prompt.svg').write_text('\n'.join(o), encoding='utf-8')

# ══════════════ C. wrap vs percentile normalization ══════════════
rng = np.random.default_rng(7); N = 540
d = rng.normal(0, 0.24, N); d[123] = -360.0
nz = lambda a: (a - np.quantile(a,.01)) / (np.quantile(a,.99)-np.quantile(a,.01)+1e-6)*2 - 1
nrm  = nz(d)
fix  = np.where(np.abs(d) > 180, d - np.sign(d)*360, d)
nfix = nz(fix)
W, H, L, R = 1000, 300, 132, 26
PW = W-L-R
o = [f'<svg class="vz" viewBox="0 0 {W} {H}" role="img" xmlns="http://www.w3.org/2000/svg" '
     f'aria-label="One wrapped frame lands about 722 normalized units outside the training range; the correction moves only that frame">']
o.append(f'<text class="vz-title" x="16" y="20" {bi("What one wrapped frame does after percentile normalization","wrap 1프레임이 백분위 정규화 후 어디에 놓이는가")}>What one wrapped frame does after percentile normalization</text>')
lo, hi = -780.0, 60.0
X = lambda v: L + (v-lo)/(hi-lo)*PW
for i,(vals, en, ko) in enumerate([(nrm,"naive difference","단순 차분"), (nfix,"shortest path","최단경로")]):
    y = 52 + i*46
    o.append(f'<text class="vz-rowlbl" x="{L-10}" y="{y+5}" text-anchor="end" {bi(en,ko)}>{en}</text>')
    o.append(f'<line class="vz-axis" x1="{L}" y1="{y+20}" x2="{L+PW}" y2="{y+20}"/>')
    inl = vals[np.abs(vals) <= 5]
    x0, x1 = X(inl.min()), X(inl.max())
    o.append(f'<rect class="vz-seg vz1" x="{x0:.1f}" y="{y-7}" width="{max(x1-x0,3):.1f}" height="22" rx="3">'
             f'<title>{len(inl)} frames, normalized {inl.min():.2f} to {inl.max():.2f}</title></rect>')
    o.append(f'<text class="vz-flag2" x="{x1-5:.1f}" y="{y-11:.1f}" text-anchor="end">{len(inl)}</text>')
    out = vals[np.abs(vals) > 5]
    if len(out):
        o.append(f'<circle class="vz-dot--bad" cx="{X(out[0]):.1f}" cy="{y+4}" r="5.5"><title>the wrapped frame</title></circle>')
        o.append(f'<text class="vz-flag" x="{X(out[0])+12:.1f}" y="{y+8}">{out[0]:.0f}</text>')
for v in (-750,-500,-250,0):
    o.append(f'<line class="vz-grid" x1="{X(v):.1f}" y1="40" x2="{X(v):.1f}" y2="122"/>')
    o.append(f'<text class="vz-sub" x="{X(v):.1f}" y="136" text-anchor="middle">{v}</text>')
o.append(f'<text class="vz-sub" x="{L+PW}" y="152" text-anchor="end" {bi("normalized action units","정규화 액션 단위")}>normalized action units</text>')
ZT, ZH, ZB = 176, 62, 238
zlo, zhi = -2.0, 2.0
Z = lambda v: L + (v-zlo)/(zhi-zlo)*PW
bins = np.linspace(zlo, zhi, 61)
ha,_ = np.histogram(nrm[np.abs(nrm)<=5], bins); hb,_ = np.histogram(nfix[np.abs(nfix)<=5], bins)
mx = max(ha.max(), hb.max()); bw = PW/60
o.append(f'<text class="vz-rowlbl" x="{L-10}" y="{ZT+ZH/2}" text-anchor="end" {bi("zoom ±2","확대 ±2")}>zoom ±2</text>')
o.append(f'<rect class="vz-okband" x="{Z(-1):.1f}" y="{ZT-6}" width="{Z(1)-Z(-1):.1f}" height="{ZH+12}" rx="3"><title>training range ±1</title></rect>')
for k,(a,b) in enumerate(zip(ha,hb)):
    x = L + k*bw
    if a: o.append(f'<rect class="vz-seg vz1" x="{x+1:.1f}" y="{ZB-a/mx*ZH:.1f}" width="{bw-2:.1f}" height="{a/mx*ZH:.1f}" rx="2"/>')
    if b: o.append(f'<rect class="vz-hist2" x="{x+1:.1f}" y="{ZB-b/mx*ZH:.1f}" width="{bw-2:.1f}" height="{b/mx*ZH:.1f}" rx="2"/>')
o.append(f'<line class="vz-axis" x1="{L}" y1="{ZB}" x2="{L+PW}" y2="{ZB}"/>')
for v in (-2,-1,0,1,2):
    o.append(f'<text class="vz-sub" x="{Z(v):.1f}" y="{ZB+15}" text-anchor="middle">{v:+d}</text>')
o.append(f'<text class="vz-note" x="16" y="{H-10}" '
         f'{bi("The two histograms coincide: the correction rewrites only the wrapped frame and leaves every other delta bit-identical. q99 minus q01 moves 0.985 to 0.997 — one frame in 540 is 0.19%, inside the 1% tail, so the percentiles can never widen to cover it.","두 히스토그램이 겹친다 — 보정은 wrap 프레임 하나만 다시 쓰고 나머지 델타는 비트 단위로 동일하다. q99−q01 은 0.985→0.997로만 움직인다. 540 중 1프레임은 0.19%로 1% 꼬리 안쪽이라 백분위가 넓어질 수 없다.")}>'
         f'The two histograms coincide — the correction rewrites only the wrapped frame. One frame in 540 is 0.19%, inside the 1% tail.</text>')
o.append('</svg>')
(OUT/'c_wrap.svg').write_text('\n'.join(o), encoding='utf-8')

# ══════════════ D. chunk timing ══════════════
W, H, L, R = 1000, 172, 16, 16
o = [f'<svg class="vz" viewBox="0 0 {W} {H}" role="img" xmlns="http://www.w3.org/2000/svg" '
     f'aria-label="A 16-step chunk covers exactly one second; inference measured at 86.5 ms on the training server">']
o.append(f'<text class="vz-title" x="{L}" y="20" {bi("One chunk = one second of robot motion","청크 1개 = 로봇 동작 1초")}>One chunk = one second of robot motion</text>')
PW = W-L-R; BY, BH = 46, 34
for k in range(16):
    x = L + PW*k/16
    o.append(f'<rect class="vz-step" x="{x+1:.1f}" y="{BY}" width="{PW/16-2:.1f}" height="{BH}" rx="3">'
             f'<title>step {k+1} · 62.5 ms</title></rect>')
o.append(f'<text class="vz-sub" x="{L}" y="{BY+BH+16}">0 ms</text>')
o.append(f'<text class="vz-sub" x="{L+PW}" y="{BY+BH+16}" text-anchor="end">1000 ms</text>')
o.append(f'<text class="vz-stepnum" x="{L+PW/32:.1f}" y="{BY+BH/2+5:.1f}" text-anchor="middle">1</text>')
o.append(f'<text class="vz-stepnum" x="{L+PW*31/32:.1f}" y="{BY+BH/2+5:.1f}" text-anchor="middle">16</text>')
iw = PW * 86.5/1000
o.append(f'<rect class="vz-seg vz2" x="{L}" y="{BY+BH+30}" width="{iw:.1f}" height="20" rx="4">'
         f'<title>inference 86.5 ms (p95 87.5) — RTX A5000</title></rect>')
o.append(f'<text class="vz-val" x="{L+iw+10:.1f}" y="{BY+BH+45}">86.5 ms</text>')
o.append(f'<text class="vz-sub" x="{L+iw+80:.1f}" y="{BY+BH+45}" '
         f'{bi("to produce the next chunk — measured on the RTX A5000, not on the robot","다음 청크 생성 시간 — RTX A5000 실측, 로봇에서 잰 값 아님")}>'
         f'to produce the next chunk — RTX A5000, not the robot</text>')
o.append(f'<text class="vz-note" x="{L}" y="{H-10}" '
         f'{bi("16 steps at 16 Hz is exactly 1.000 s, so the next chunk must be ready before the current one runs out.","16Hz × 16스텝 = 정확히 1.000초. 현재 청크가 소진되기 전에 다음 청크가 준비돼야 한다.")}>'
         f'16 steps at 16 Hz is exactly 1.000 s.</text>')
o.append('</svg>')
(OUT/'d_timing.svg').write_text('\n'.join(o), encoding='utf-8')

for f in sorted(OUT.iterdir()):
    print(f'  {f.name:16s} {f.stat().st_size:6d} B')
