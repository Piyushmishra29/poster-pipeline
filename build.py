#!/usr/bin/env python3
"""Build Rockwall Fitness Price Card poster PDF.

Usage:
  python3 build.py                    # render poster.html -> Rockwall-Price-Card-2026.pdf
  python3 build.py poster_v2a.html    # render any variant by filename
  python3 build.py --regen-qr         # also regenerate assets/qr.png
"""
import subprocess, shutil, sys
from pathlib import Path
from weasyprint import HTML
import qrcode
from qrcode.constants import ERROR_CORRECT_H

HERE = Path(__file__).resolve().parent
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

def pdf_name(html_path: Path) -> Path:
    stem = html_path.stem
    if stem == "brand-kit":
        return HERE / "Rockwall-Brand-Kit-2026.pdf"
    if stem.startswith("sticker_"):
        name = stem.replace("sticker_", "")
        return HERE / f"Rockwall-Sticker-{name.title()}.pdf"
    if stem == "poster":
        return HERE / "Rockwall-Price-Card-2026.pdf"
    suffix = stem.replace("poster_", "")
    return HERE / f"Rockwall-Price-Card-2026-{suffix}.pdf"

def preview_dir(html_path: Path) -> Path:
    stem = html_path.stem
    if stem == "brand-kit":
        return HERE / "preview-brand-kit"
    if stem.startswith("sticker_"):
        return HERE / f"preview-{stem.replace('_', '-')}"
    if stem == "poster":
        return HERE / "preview"
    suffix = stem.replace("poster_", "")
    return HERE / f"preview-{suffix}"

def build(html_path: Path) -> Path:
    pdf = pdf_name(html_path)
    # Brand kit + stickers render lightweight — they're small/reference docs and
    # the print-grade dpi=300 rasterises gradient/SVG content into huge PDFs.
    if html_path.stem == "brand-kit" or html_path.stem.startswith("sticker_"):
        kind = "reference doc" if html_path.stem == "brand-kit" else "sticker"
        print(f"Rendering {html_path.name} -> {pdf.name}  [{kind}: lightweight]")
        HTML(filename=str(html_path), base_url=str(HERE)).write_pdf(
            target=str(pdf),
            jpeg_quality=90,
            uncompressed_pdf=False,
        )
    else:
        print(f"Rendering {html_path.name} -> {pdf.name}  [print: bleed + crop marks + PDF/A]")
        HTML(filename=str(html_path), base_url=str(HERE)).write_pdf(
            target=str(pdf),
            dpi=300,
            jpeg_quality=95,
            full_fonts=True,
            uncompressed_pdf=False,
            pdf_variant="pdf/a-3b",
            pdf_identifier=b"rockwall-2026-print",
        )
    print(f"  Wrote {pdf.name} ({pdf.stat().st_size/1024:.0f} KB)")
    return pdf

def previews(html_path: Path, pdf: Path) -> int:
    p = preview_dir(html_path)
    if p.exists(): shutil.rmtree(p)
    p.mkdir()
    subprocess.run(["pdftoppm", "-png", "-r", "200", str(pdf), str(p/"page")], check=True)
    pages = len(list(p.glob('page-*.png')))
    print(f"  {pages} preview page(s) at {p.name}/")
    return pages

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    html_name = args[0] if args else "poster.html"
    html_path = HERE / html_name
    if not html_path.exists():
        raise SystemExit(f"Not found: {html_path}")

    regen = "--regen-qr" in flags
    if regen or not QR_PATH.exists():
        make_qr()
    else:
        print(f"QR exists, skipping ({QR_PATH.name})")
    pdf = build(html_path)
    pages = previews(html_path, pdf)
    print(f"\nDone. {pdf.name} {pdf.stat().st_size/1024:.0f} KB, {pages} preview page(s).")
