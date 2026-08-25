# -*- coding: utf-8 -*-
"""Push regenerated SVGs back into the pages that carry them.

The figures live inline in the HTML rather than as image files, so they inherit
the site's theme tokens and stay crisp. That means regenerating an SVG is only
half the job — this does the other half.

    python3 tools/gen_lineage.py && python3 tools/gen_e7figs.py
    python3 tools/embed.py

Matching is by the SVG's aria-label prefix, so a figure can move around inside a
page without breaking the link between generator and destination.
"""

from __future__ import annotations

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
FIGS = pathlib.Path(__file__).resolve().parent / "figs"

# svg file -> (page, first words of that svg's aria-label)
TARGETS = [
    ("lineage.svg", "technical/e6-policy-evolution.html", "E6 v1-v26"),
    ("e6_norm.svg", "technical/e6-policy-evolution.html", "E6 joint j5 spans"),
    ("perdim.svg", "technical/e6-policy-evolution.html", "Per-dimension training loss"),
    ("a_budget.svg", "projects/e7-xarm6-policy.html", "Token budget"),
    ("b_prompt.svg", "projects/e7-xarm6-policy.html", "Prompt token cost"),
    ("c_wrap.svg", "projects/e7-xarm6-policy.html", "One wrapped frame"),
    ("d_timing.svg", "projects/e7-xarm6-policy.html", "A 16-step chunk"),
    ("f_interventions.svg", "projects/e7-stage2-log.html", "Which interventions moved the arm"),
    ("g_selectivity.svg", "projects/e7-stage2-log.html", "When the instruction names a different"),
]


def main() -> int:
    changed, failed = 0, 0
    for name, page_rel, label in TARGETS:
        svg_path, page_path = FIGS / name, ROOT / page_rel
        if not svg_path.is_file():
            print(f"  MISSING  {name} — run the generator first")
            failed += 1
            continue

        new = svg_path.read_text(encoding="utf-8").strip()
        page = page_path.read_text(encoding="utf-8")

        # Find the one <svg> whose aria-label starts with this figure's label.
        hits = [
            m for m in re.finditer(r"<svg\b.*?</svg>", page, re.S)
            if re.search(rf'aria-label="{re.escape(label)}', m.group(0))
        ]
        if len(hits) != 1:
            print(f"  {'NO MATCH' if not hits else 'AMBIGUOUS'}  {name} in {page_rel} "
                  f"(aria-label starting {label!r}: {len(hits)} found)")
            failed += 1
            continue

        if hits[0].group(0).strip() == new:
            print(f"  unchanged  {name}")
            continue

        page_path.write_text(page[: hits[0].start()] + new + page[hits[0].end():], encoding="utf-8")
        print(f"  updated    {name} -> {page_rel}")
        changed += 1

    print(f"\n{changed} updated, {failed} failed")
    if not failed:
        print("Check the result before committing — this rewrites published pages:\n"
              "  git diff --stat")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
