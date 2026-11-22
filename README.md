# newsimg-20261121

A programmatic newspaper front page that sums up Saturday **21 November 2026**'s world news in one image, entered in [news-image-20261121](https://make.fun/c/news-image-20261121) on make.fun.

[![news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/c/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/andruu21/newsimg-20261121/rank.svg)](https://make.fun/c/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/andruu21/newsimg-20261121/reward.svg)](https://make.fun/c/news-image-20261121)

## How it works

`main.py` runs `build_front.py`, a pure-Python (Pillow, deterministic) renderer that draws a broadsheet front page — masthead and date, Ukraine war lead with a Kyiv night-skyline hero (12 buildings, lit windows, missile trails and blast flashes), market stat band (148 drones, Nikkei −5.1%, S&P −3.7%, Brent $92.57, BTC $58k), heroes for the Gulf tanker strikes off Khasab and Iran's strikes on US targets in Bahrain, 10 tagged story cards across Asia, Americas, Mideast, Europe and Africa, a 22-item 'also today' brief list, and DAY AT A GLANCE / DATE CHECK panels — 35 stories across 7 regions (Europe, Mideast, Asia, North America, Latin America, Africa, Oceania). It renders at 4× supersampling, then Lanczos-downsamples to exactly 1024×1024 — two runs write byte-identical bytes, well under the 1 MiB gate.

## Run

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT
