# poster-pipeline

A small HTML + CSS → PDF build pipeline for **print-ready A3 posters**, designed for client work at SMARK8ING / Daily Mark8ing. Renders WeasyPrint, exports A3 with 3 mm bleed + crop marks + sRGB at PDF/A-3b quality.

Each git branch is a separate poster project. The `main` branch ships the first one — a price-card for **Rockwall Fitness, Bangalore** — as a working example.

---

## What's inside

| File | Purpose |
|---|---|
| `build.py` | WeasyPrint render + `pdftoppm` preview + QR generator. Takes any `poster_*.html` filename. |
| `poster.html` (v1) | First version. Neon-glitch lime/black, sticker-cluster hero. |
| `poster_v2a.html` | Maximalist editorial variant. Magenta spark, sticker collage, agit headline. |
| `poster_v2b.html` | Brutalist monospace variant. CAD-grid, real pricing table, athlete hero band. **Heaviest brand departure.** |
| `poster_v2c.html` | Cyberpunk HUD variant. Signal bars, modular price modules, scanline atmosphere. |
| `poster_v3.html` | **Synthesis pick** — athlete-led hero + clean prices + one CTA + STUDENT EDITION back page. |
| `assets/` | Logo, gym photos, QR, processed hero image. |
| `assets/gym-photos/` | 89 raw photos pulled from `rockwallfitness.in`. |
| `Rockwall-Price-Card-2026-*.pdf` | Rendered outputs, ready for press. |
| `preview-*/page-N.png` | Eyeball-able PNG renders per page. |

---

## Render

```bash
# Install deps once
pip3 install weasyprint qrcode[pil] Pillow

# Render any variant
python3 build.py poster_v3.html

# First run (or after editing the QR target URL)
python3 build.py poster_v3.html --regen-qr
```

Output: a new `Rockwall-Price-Card-2026-<variant>.pdf` and `preview-<variant>/page-N.png` for review.

---

## Print export spec

Everything `build.py` emits is configured for press:

- **Page size:** 297 × 420 mm (A3)
- **Bleed:** 3 mm all sides → final PDF is **303 × 426 mm**
- **Crop marks:** auto-emitted by WeasyPrint (`marks: crop cross`)
- **Background bleed:** `@page { background: #050505; }` so the dark fill covers the bleed area — no white edge after trim
- **Colour:** sRGB (don't convert to CMYK before sending — printer's RIP handles it)
- **Images:** JPEG q95, no chroma subsampling, baseline
- **Hero photo:** Lanczos-upscaled to 3200×2134 + unsharp mask + slight contrast boost (~270 DPI effective at hero band size)
- **PDF variant:** PDF/A-3b (archival print-safe)

Send the PDF straight to the printer. Tell them: A3, 3 mm bleed, trim to marks.

---

## Per-project convention (this repo)

Following the pattern across Piyush's repos: **each branch is a distinct poster project.** The root README on each branch is project-specific.

- `main` — example seed: Rockwall Fitness 2026 price card
- future branches — one per client / poster series

To start a new poster project:

```bash
git checkout -b clientname-poster
# clear assets/, swap in new content, rewrite poster.html
# update this README to describe the new project
python3 build.py poster.html
git add . && git commit -m "Seed clientname poster"
```

The build pipeline (`build.py`, the `@page` rules in HTML, the WeasyPrint quirks documented below) carry over to every branch.

---

## WeasyPrint gotchas (learned the hard way)

These CSS properties are **silently dropped** by WeasyPrint — don't use them and expect rendering to work:

- `inset:` shorthand → use explicit `top/right/bottom/left`
- `display: contents` → flatten the HTML instead
- `mix-blend-mode` → use opacity layers + filters instead
- `backdrop-filter` → unsupported
- `filter: drop-shadow()` → unsupported (use `box-shadow` or SVG `<feDropShadow>`)
- `text-shadow` → unsupported

These ARE supported and work as expected:

- `filter: grayscale() contrast() brightness()` on images
- `clip-path: polygon(...)`
- `linear-gradient`, `radial-gradient`, `repeating-linear-gradient`
- `transform: scale/rotate/translate` (mm units OK)
- `font-variation-settings: "wdth" 150` on variable fonts
- `@page { size, margin, bleed, marks, background }`

If an image doesn't appear → check whether its container has zero dimensions due to dropped `inset:` shorthand. That bit me twice.

---

## Credits

- Concept + iteration: Piyush Mishra (SMARK8ING)
- Build pipeline + execution help: Claude (Anthropic)
- Photography: Rockwall Fitness in-house
- Fonts: Anybody, Inter Tight, JetBrains Mono, Archivo Black, Departure Mono, Bricolage Grotesque (Google Fonts, OFL)

---

*Branch: `main` · Project: Rockwall Fitness 2026 Price Card · Last updated: 2026-05-27*
