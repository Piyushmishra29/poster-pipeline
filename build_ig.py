#!/usr/bin/env python3
"""Render the IG social layouts to exact-pixel PNGs (no bleed, no crop marks).

Pages are sized in CSS px (1080xH). At 96 dpi, 1 CSS px == 1 device px, so
pdftoppm -r 96 yields exactly 1080xH pixels — pixel-perfect Instagram assets.

Usage:
  python3 build_ig.py            # render both post + story
  python3 build_ig.py post       # just the 4:5 feed post
  python3 build_ig.py story      # just the 9:16 story
"""
import subprocess, sys
from pathlib import Path
from weasyprint import HTML

HERE = Path(__file__).resolve().parent

TARGETS = {
    "post":  ("dance_ig_post.html",  "Rockwall-Dance-IG-Post-1080x1350.png"),
    "story": ("dance_ig_story.html", "Rockwall-Dance-IG-Story-1080x1920.png"),
}

def render(key):
    html_name, png_name = TARGETS[key]
    html_path = HERE / html_name
    pdf_tmp = HERE / f".{key}_ig_tmp.pdf"
    out_png = HERE / png_name
    print(f"Rendering {html_name} -> {png_name}")
    HTML(filename=str(html_path), base_url=str(HERE)).write_pdf(target=str(pdf_tmp))
    # -singlefile drops the page suffix so we get exactly <name>.png
    stem = str(out_png.with_suffix(""))
    subprocess.run(["pdftoppm", "-png", "-r", "96", "-singlefile", str(pdf_tmp), stem], check=True)
    pdf_tmp.unlink(missing_ok=True)
    # report dims
    dims = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(out_png)],
                          capture_output=True, text=True).stdout
    w = h = "?"
    for line in dims.splitlines():
        if "pixelWidth" in line:  w = line.split(":")[-1].strip()
        if "pixelHeight" in line: h = line.split(":")[-1].strip()
    print(f"  Wrote {png_name}  {w}x{h}  ({out_png.stat().st_size/1024:.0f} KB)")

if __name__ == "__main__":
    keys = sys.argv[1:] or ["post", "story"]
    for k in keys:
        if k not in TARGETS:
            raise SystemExit(f"Unknown target '{k}'. Use: post | story")
        render(k)
    print("\nDone.")
