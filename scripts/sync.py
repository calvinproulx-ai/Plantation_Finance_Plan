#!/usr/bin/env python3
"""Build index.html for GitHub Pages from the published Plantation Finance Board artifact.

Usage: python3 scripts/sync.py <artifact_index.html> [output=index.html]

The artifact service may wrap the page in an extra skeleton; this keeps only the
board's own <!DOCTYPE html> document, adds a noindex tag and a "last synced" stamp.
Exits 0 and prints CHANGED or UNCHANGED (ignoring the synced stamp).
"""
import re, sys, datetime, pathlib
try:
    from zoneinfo import ZoneInfo
    now = datetime.datetime.now(ZoneInfo("America/New_York"))
except Exception:
    now = datetime.datetime.utcnow()

src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
out = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "index.html")

inner = src
# take the LAST doctype document if the wrapper put the board inside another skeleton
docs = [x.start() for x in re.finditer(r"<!DOCTYPE html>", src, re.I)]
if len(docs) > 1:
    start = docs[-1]
    end = src.find("</html>", start)
    inner = src[start:end + len("</html>")]

assert "Plantation Finance Board" in inner, "unexpected artifact content"
assert inner.count('class="card"') >= 10, "too few initiative cards — refusing to publish"

inner = re.sub(r'<meta name="robots"[^>]*>\s*', "", inner)
head_add = '<meta name="robots" content="noindex, nofollow">'
if 'name="viewport"' not in inner:
    head_add += '\n<meta name="viewport" content="width=device-width, initial-scale=1">'
inner = inner.replace("<head>", "<head>\n" + head_add, 1)
inner = re.sub(r'\s*<div class="synced">.*?</div>', "", inner, flags=re.S)
stamp = now.strftime("%b %-d, %Y %-I:%M %p ET")
inner = inner.replace("</footer>", f'</footer>\n  <div class="synced" style="margin-top:8px;font-size:11px;color:var(--ink-faint);font-family:monospace">Synced from the Claude artifact {stamp}</div>', 1)

def strip(s): return re.sub(r'<div class="synced".*?</div>', "", s, flags=re.S)
old = out.read_text(encoding="utf-8") if out.exists() else ""
changed = strip(old) != strip(inner)
if changed or not old:
    out.write_text(inner, encoding="utf-8")
print("CHANGED" if changed else "UNCHANGED")
