# The World in One Day — 17 November 2026

[![news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/yi948383-arch/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/yi948383-arch/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117)

A broadsheet front-page poster summing up the world's news of
**Tuesday, 17 November 2026** in a single 1024x1024 image: six stories
across six beats — Iran's drone strike on the US radar base in Bahrain,
the Crimea bridge collapse, Trump landing in Manila for the ASEAN summit,
the Optimizely supply-chain hack hitting BBC, CNN and 178 sites, the
Vulcan rocket failure that lost 40 Amazon satellites, and the US
tightening AI chip export rules. Every panel carries a region kicker, a
bold headline, a short factual summary and a hand-drawn pictogram; the
masthead names the day, and the footer repeats it.

The image is drawn entirely with Python PIL (`draw.py`) — no photos, no
downloaded artwork. `main.py` copies the finished poster to the output
directory, deterministically.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

This writes `out/entry.png` (1024x1024, under 1 MiB).

To redraw the poster from scratch:

```sh
python3 draw.py
```
