# Rockwall Fitness — Brand Sketches

A cast of cute mascot doodles for Rockwall Fitness, built with the
[gattyworks/brand-illustrations](https://github.com/gattyworks/brand-illustrations)
framework methodology, adapted to the Rockwall brand.

## Style DNA (Rockwall adaptation)
- Minimalist flat geometric vector doodles.
- VERY THICK monoweight **black `#000000`** outlines (stroke ~14, round joins/caps).
- Flat **white `#FFFFFF`** fills. No gradients, shadows, or 3D.
- **Exactly ONE accent** per sketch: Rockwall lime **`#CFFF3C`**.
- Faces: solid black dot eyes + simple U-smile. Tiny U-shaped limbs.
- Square 1:1, generous padding, centered.

## The cast

| File | Name | Reads as | Lime moment | Metaphor / use |
|---|---|---|---|---|
| `sketch_boulder.*` | **Boulder** | a strong rock giving a thumbs-up | moss/chalk patch | the "Rockwall" namesake, strength, foundation |
| `sketch_dumbbell.*` | **Rep** | a dumbbell with a face | the two end plates | lifting, reps, training |
| `sketch_kettlebell.*` | **Swing** | a kettlebell | band across the bell | conditioning, cardio |
| `sketch_shaker.*` | **Fuel** | a half-full shaker bottle | the drink level | the cafe / fuel-bar, recovery |
| `sketch_stopwatch.*` | **Tick** | a stopwatch | the top button | timed classes, the "30 SECONDS" biometric desk |

## Rendering
Each sketch is a standalone `.svg`. To re-render a PNG:

```bash
python3 render_svg.py sketch_boulder.svg   # -> sketch_boulder.png
```

(`render_svg.py` wraps the SVG in HTML, renders with WeasyPrint, and rasterises
with `pdftoppm` — same toolchain as the poster pipeline.)
