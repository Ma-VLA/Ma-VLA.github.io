# -*- coding: utf-8 -*-
"""확인용 PNG 렌더 — SSH 환경에 브라우저가 없어서 눈으로 보려면 이게 필요하다.

SVG 는 사이트의 CSS 클래스로 칠해진다. 그냥 렌더하면 클래스가 안 붙어 **전부 검게** 나오므로,
`style.css` 의 토큰을 읽어 속성으로 인라인한 뒤 렌더한다.

  python3 tools/render_png.py h_frozen.svg          # 라이트·다크 두 장

⚠️ 색 값은 여기 손으로 적지 않고 `style.css` 에서 읽는다 — 두 곳에 적으면 갈라진다.
결과는 /home/billy/26kp/ 에 둔다 (GUI 없는 환경의 관례).
"""
import re, sys, pathlib
import cairosvg

ROOT = pathlib.Path(__file__).resolve().parent.parent
CSS = (ROOT / "style.css").read_text()

def tokens(dark: bool) -> dict:
    """`.vz` 블록과 :root 에서 필요한 토큰만 뽑는다. 다크는 뒤에 오는 정의가 이긴다."""
    out = {}
    for name in ("vz1","vz2","vz3","vz-track","vz-band","text","muted","line","surface"):
        hits = re.findall(rf"--{re.escape(name)}:\s*([#\w().,%\s-]+?);", CSS)
        if not hits:
            raise SystemExit(f"🔴 style.css 에서 --{name} 을 못 찾았다")
        # 라이트 = 첫 정의, 다크 = 두 번째가 있으면 그것
        out[name] = (hits[1] if dark and len(hits) > 1 else hits[0]).strip()
    return out

FILL = {"vz1":"vz1","vz2":"vz2","vz3":"vz3","vz-track":"vz-track","vz-usedtrack":"vz-track",
        "vz-step":"vz-track","vz-okband":"vz-band","vz-used":"vz2","vz-title":"text",
        "vz-rowlbl":"text","vz-lbl":"text","vz-val":"text","vz-out":"text",
        "vz-sub":"muted","vz-note":"muted","vz-total":"muted","vz-flag2":"muted",
        "vz-flag":"vz2","vz-stepnum":"muted"}
STROKE = {"vz-axis":"line","vz-grid":"line","vz-hist2":"vz2"}
SIZE = {"vz-title":13,"vz-total":12,"vz-lbl":11.5,"vz-rowlbl":11.5,"vz-sub":10.5,
        "vz-note":11,"vz-val":11,"vz-out":11,"vz-stepnum":11,"vz-flag":12,"vz-flag2":10.5}
BOLD = {"vz-title","vz-val","vz-out","vz-flag","vz-stepnum"}

def inline(svg: str, T: dict) -> str:
    def rep(m):
        classes = m.group(1).split()
        a = []
        for c in classes:
            if c in FILL:  a.append(f'fill="{T[FILL[c]]}"')
            if c in STROKE: a.append(f'stroke="{T[STROKE[c]]}"')
            if c in SIZE:  a.append(f'font-size="{SIZE[c]}"')
            if c in BOLD:  a.append('font-weight="700"')
        # `fill="none"` 같이 원소가 직접 준 속성이 이기도록 앞에 놓는다
        return (" ".join(a) + " " if a else "") + m.group(0)
    return re.sub(r'class="([^"]+)"', rep, svg)

def main() -> int:
    if len(sys.argv) < 2:
        raise SystemExit("쓰기: python3 tools/render_png.py <figs 안의 파일명>")
    src = ROOT / "tools/figs" / sys.argv[1]
    svg = src.read_text()
    for dark in (False, True):
        T = tokens(dark)
        s = inline(svg, T)
        # 🔴 배경은 <rect> 로 깐다. cairosvg 는 style="background:" 를 무시해서
        #    다크 렌더가 흰 바탕에 밝은 글자로 나온다 -- 확인이 안 되는 그림이 된다.
        vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', s)
        if not vb:
            raise SystemExit("🔴 viewBox 를 못 읽었다 — 배경을 깔 크기를 모른다")
        s = re.sub(r"(<svg[^>]*>)",
                   rf'\1<rect x="0" y="0" width="{vb.group(1)}" height="{vb.group(2)}" '
                   rf'fill="{T["surface"]}"/>', s, count=1)
        out = pathlib.Path("/home/billy/26kp") / f"{src.stem}_{'dark' if dark else 'light'}.png"
        cairosvg.svg2png(bytestring=s.encode(), write_to=str(out), scale=2.0)
        print("wrote", out)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
