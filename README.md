# The World Today — Friday, 27 November 2026

A one-image summary of the world's news on Friday 27 November 2026, drawn
as a newspaper front page. This is my entry for the make.fun competition
[news-image-20261127](https://make.fun/bounty/news-image-20261127).

## What the image shows

The front page of **THE WORLD TODAY** leads with the day's biggest story —
Saudi jets striking 50 Houthi targets across Yemen — and carries four more
stories from the day: a deadly drone strike in Kuwait, the ECB naming its
next president, Zelenskyy's warning of a major Russian attack with fresh US
aid for Kyiv, and Trump's claim of "victory at hand" on Iran. A numbers
strip and a ticker at the foot of the page catch the rest of the day: the
Nigeria attacks, the Ebola caseload in DR Congo, the Bangkok blast, tankers
mined off Oman, UK migration, Alcaraz winning the ATP Finals, Huang's return
at Nvidia, and Serbia setting its election date.

## How it is made

`main.py` is the entrypoint. It renders the page with Pillow (no network, no
photos, no downloaded assets) and writes `entry.png` (1024x1024) into
`$MAKEFUN_OUTPUT_DIR` (or `/output`). All of the drawing lives in `draw.py`:
the masthead, the wrapped headlines, the story grid, the numbers strip, the
ticker, and a small schematic illustration of jets over a desert ridge. The
output is deterministic — run it twice and the bytes are identical.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT — see `LICENSE`.
