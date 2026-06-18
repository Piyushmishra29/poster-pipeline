#!/usr/bin/env python3
"""Render a standalone .svg to a .png via WeasyPrint + pdftoppm.
Usage: python3 render_svg.py sketch_name.svg
Output: sketch_name.png (square) in the same folder.
"""
import sys, subprocess, pathlib
from weasyprint import HTML

svg_path = pathlib.Path(sys.argv[1]).resolve()
svg = svg_path.read_text()

html = f"""<!DOCTYPE html><html><head><meta charset="utf-8"><style>
@page {{ size: 160mm 160mm; margin: 0; }}
* {{ margin: 0; padding: 0; }}
html, body {{ width: 160mm; height: 160mm; background: #FFFFFF; }}
svg {{ width: 160mm; height: 160mm; display: block; }}
</style></head><body>{svg}</body></html>"""

pdf_path = svg_path.with_suffix(".pdf")
HTML(string=html).write_pdf(str(pdf_path))
out_stem = str(svg_path.with_suffix(""))
subprocess.run(["pdftoppm", "-png", "-r", "150", "-singlefile", str(pdf_path), out_stem], check=True)
pdf_path.unlink(missing_ok=True)
print("wrote", out_stem + ".png")
