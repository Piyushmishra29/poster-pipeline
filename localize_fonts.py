#!/usr/bin/env python3
"""One-time: download the Latin Google Fonts used by the posters into assets/fonts/
and emit assets/fonts.css with local @font-face rules, so WeasyPrint never hits the
network (which hangs on dozens of unicode-range subsets)."""
import re, urllib.request, pathlib

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
HERE = pathlib.Path(__file__).parent
FONTS = HERE / "assets" / "fonts"
FONTS.mkdir(parents=True, exist_ok=True)

CSS_URL = ("https://fonts.googleapis.com/css2?"
           "family=Anybody:wdth,wght@75..150,400..900&"
           "family=Inter+Tight:wght@400;500;700;800;900&display=swap")

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()

css = fetch(CSS_URL).decode("utf-8")

# Split into @font-face blocks, each preceded by a /* subset */ comment.
blocks = re.findall(r"/\*\s*([\w-]+)\s*\*/\s*(@font-face\s*\{.*?\})", css, re.S)
out = []
seen = 0
for subset, block in blocks:
    if subset != "latin":
        continue  # latin only — posters are uppercase Latin
    fam = re.search(r"font-family:\s*'([^']+)'", block).group(1)
    url = re.search(r"url\(([^)]+)\)", block).group(1)
    fn = f"{fam.replace(' ','')}-{seen}.woff2"
    (FONTS / fn).write_bytes(fetch(url))
    block = re.sub(r"url\([^)]+\)", f"url(fonts/{fn})", block)
    out.append(block)
    seen += 1
    print(f"  {fam} [{subset}] -> {fn}")

(HERE / "assets" / "fonts.css").write_text("\n".join(out) + "\n")
print(f"Wrote assets/fonts.css with {len(out)} face(s).")
