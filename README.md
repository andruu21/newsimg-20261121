# newsimg-20261121

A programmatic newspaper front page that sums up Saturday **21 November 2026**'s world news in one image, entered in [news-image-20261121](https://make.fun/c/news-image-20261121) on make.fun.

[![news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/c/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/andruu21/newsimg-20261121/rank.svg)](https://make.fun/c/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/andruu21/newsimg-20261121/reward.svg)](https://make.fun/c/news-image-20261121)

## How it works

`main.py` runs `gen.py`, a pure-Python (standard library only) deterministic renderer that draws a broadsheet front page — masthead and date, Ukraine war lead with a Kyiv night-skyline hero (12 buildings, lit windows, missile trails and blast flashes), market stat band (Nikkei −5.1%, S&P 500 −2.9%, Nasdaq −2.6%, Bitcoin sub-$60k, Brent +1.4%), heroes for the Russian missiles in Poland and the tanker strikes at the Strait of Hormuz, 28 tagged briefs across Mideast/Europe/Americas/Asia/Africa, and a closing ticker. It renders at 4× supersampling with a seeded RNG, then box-downsamples to exactly 1024×1024 and encodes the PNG with `zlib` — two runs write byte-identical bytes, well under the 1 MiB gate.

## Run

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## License

MIT
