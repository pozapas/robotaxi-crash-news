# Figure code

`r10_figs_revised.py` redraws Figures 3 and 4 by calling `fig3()` and `fig4()`
from `r04_decay_reach.py` unchanged, feeding them the corrected quantities from
the reanalysis. `palette.py` and `trb_news.mplstyle` are the shared style kit,
and `common.py` supplies the data loaders and output folder.

Run `python code/figures/r10_figs_revised.py` from the repository root. It
reads `data/*.csv` through `code/paths.py` and writes the PNG files to
`figures_out/`, which match the published figures pixel for pixel. The
half-life and its interval are read from `../out_rest.json` so the figure and
the manuscript cannot drift apart.
