# HANDOFF — Rockwall Fitness / poster-pipeline

_Last updated: 2026-05-29 · Branch: `main` · Repo: https://github.com/Piyushmishra29/poster-pipeline_

## What this repo is
HTML + CSS → **print-ready PDF** pipeline (WeasyPrint) for Rockwall Fitness, a young/loud gym in Krishnanagar, Bangalore. One `build.py` renders everything; each git branch is a distinct poster project (this is the seed/main).

```bash
pip3 install weasyprint qrcode[pil] Pillow      # deps (once)
python3 build.py <file.html>                     # render any artifact
```
Output naming: `poster.html`→price card · `poster_v*`→variants · `sticker_*`→`Rockwall-Sticker-*` · `brand-kit`→`Rockwall-Brand-Kit-2026`.

## OFFICIAL BRAND PALETTE (client-confirmed 2026-05-27 — use everywhere)
| Role | Name | HEX | RGB |
|---|---|---|---|
| Primary | Acid Lime | **#D1DD27** | 209/221/39 |
| Base | Ink Navy | **#171921** | 23/25/33 |
| Text | White | **#FFFFFF** | 255/255/255 |
| Secondary 01 | Steel Grey | **#898989** | 137/137/137 |
| Secondary 02 | Fog Grey | **#B3B3B3** | 179/179/179 |

- **No red / coral / cyan / grape / amber.** Client rejected a rainbow secondary. Energy = lime + bold type, not colour variety.
- **Logo is NOT changing** (billboards/LEDs depend on it). Two-tone: ROCK=lime, WALL=white, FITNESS=lime → needs dark grounds. Source: `assets/logo.png` (from rockwallfitness.in).
- Fonts: **Anybody** (variable, display, wdth 150), **Inter Tight** (body), **JetBrains Mono** (labels/folios).

## Deliverables (all rendered + committed)
| Artifact | Source | PDF |
|---|---|---|
| **Brand Guidelines** (27pp, A4, agency editorial system, official palette) | `brand-kit.html` | `Rockwall-Brand-Kit-2026.pdf` |
| Price card v3 (A3, 2-sided: front + STUDENT EDITION back) — **the ship pick** | `poster_v3.html` | `Rockwall-Price-Card-2026-v3.pdf` |
| Price card variants v1/v2a/v2b/v2c (explorations) | `poster*.html` | `Rockwall-Price-Card-2026*.pdf` |
| 3 student die-cut stickers (DEADLIFT>DEADLINE, ROCKWALL plate, CGPA↓GAINS↑) | `sticker_*.html` | `Rockwall-Sticker-*.pdf` |

Web previews for README/sharing: `docs/brand-kit-web/` (27) and `docs/previews-web/` (posters).

## Brand-kit structure (27pp)
Cover · Index · **§01 Identity** (manifesto, logo primary/lockups/clear-space/misuse) · **§02 Colour** (core, two greys, usage) · **§03 Type** (display, body/mono) · **§04 Elements** (motifs, patterns, icons, photography) · **§05 In Use** (voice, poster, social, merch, signage) · Back cover. Full-bleed section dividers between each.
Motifs (p17) all derive from the identity: THE LINK (logo notch), STRETCH (glitch seam), POLY-CUT, DIAMOND, KNURL, HALFTONE.

## WeasyPrint gotchas (bit us repeatedly — see also memory)
- `inset:` shorthand **dropped** → use explicit top/right/bottom/left.
- CSS does **not** cascade into inline SVG → put fill/stroke as presentation attributes (or on a `<g>`).
- `clip-path: polygon()` unreliable → prefer `border-radius` / `transform: skew`.
- Multi-stop gradients: use explicit hex + 4-stop syntax (double-position stops flaky).
- `dpi=300` rasterises gradient backgrounds → huge files. Brand kit renders **lightweight** in `build.py` (the `if stem=="brand-kit"` branch); posters/stickers keep the print-grade branch (A3+bleed+crop+PDF/A-3b).
- Re-encode progressive JPEGs to baseline (`progressive=False`).

## OPEN / NEXT
1. **Consistency decision (pending user):** posters v1–v3 + stickers still use the OLD neon lime `#CFFF3C` on pure black `#050505`. Brand kit is on the official `#D1DD27` / `#171921`. Decide whether to roll the official palette across posters + stickers.
2. Possible follow-ups raised but not built: kiss-cut sticker sheet (single A4), more stickers (6 AM CLUB, BOOKS DOWN), social story/square crops, README gallery for the brand kit.
3. If updating posters to official palette: swap `#CFFF3C`→`#D1DD27` and `#050505`→`#171921` in `poster*.html`, re-render, re-commit.

## Push status
All work committed and pushed to `origin/main` (HEAD = motifs rebuild). Pushes use `git -c credential.helper='!gh auth git-credential' push` (gh CLI auth as Piyushmishra29).
