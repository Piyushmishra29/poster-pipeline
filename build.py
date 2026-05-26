#!/usr/bin/env python3
"""Build Rockwall Fitness Price Card poster PDF.

Usage:
  python3 build.py              # render PDF + preview
  python3 build.py --regen-qr   # also regenerate assets/qr.png
"""
import subprocess, shutil, sys
from pathlib import Path
from weasyprint import HTML
import qrcode
from qrcode.constants import ERROR_CORRECT_H

HERE = Path(__file__).resolve().parent
HTML_IN = HERE / "poster.html"
PDF_OUT = HERE / "Rockwall-Price-Card-2026.pdf"
PREVIEW = HERE / "preview"
QR_PATH = HERE / "assets" / "qr.png"
QR_URL  = "https://rockwallfitness.in"

def make_qr():
    print(f"Generating QR -> {QR_PATH.name} ({QR_URL})")
    QR_PATH.parent.mkdir(parents=True, exist_ok=True)
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_H,
        box_size=12,
        border=2,
    )
    qr.add_data(QR_URL)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#050505", back_color="white")
    img.save(str(QR_PATH))
    print(f"  Wrote {QR_PATH.name} ({QR_PATH.stat().st_size/1024:.1f} KB)")

def build():
    print(f"Rendering {HTML_IN.name} -> {PDF_OUT.name}")
    HTML(filename=str(HTML_IN), base_url=str(HERE)).write_pdf(target=str(PDF_OUT))
    print(f"  Wrote {PDF_OUT.name} ({PDF_OUT.stat().st_size/1024:.0f} KB)")

def previews():
    if PREVIEW.exists(): shutil.rmtree(PREVIEW)
    PREVIEW.mkdir()
    subprocess.run(["pdftoppm", "-png", "-r", "200", str(PDF_OUT), str(PREVIEW/"page")], check=True)
    pages = len(list(PREVIEW.glob('page-*.png')))
    print(f"  {pages} preview page(s) at {PREVIEW.name}/")
    return pages

if __name__ == "__main__":
    regen = "--regen-qr" in sys.argv
    if regen or not QR_PATH.exists():
        make_qr()
    else:
        print(f"QR exists, skipping ({QR_PATH.name})")
    build()
    pages = previews()
    print(f"\nDone. PDF {PDF_OUT.stat().st_size/1024:.0f} KB, {pages} preview page(s).")
