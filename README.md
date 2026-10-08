# Plantation Finance Plan — Initiative Board

Public GitHub Pages copy of The Plantation PV's A/R, A/P, Controller & CFO initiative board.

- **Source of truth:** the "Plantation Finance Board" Claude artifact, which Calvin updates in Claude alongside the Word Finance Plan.
- **Daily sync (7 AM ET):** a Claude scheduled task reads the current artifact, runs `scripts/sync.py`, and commits `index.html` here only when the board changed.
- **Manual sync:** `python3 scripts/sync.py <artifact index.html> index.html`

The page carries a `noindex` tag so search engines don't list it, but anyone with the URL can view it.
