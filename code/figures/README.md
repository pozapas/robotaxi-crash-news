# Figure code

`r10_figs_revised.py` redraws Figures 3 and 4 by calling `fig3()` and `fig4()`
from `r04_decay_reach.py` unchanged, feeding them the corrected quantities from
the reanalysis. `palette.py` and `trb_news.mplstyle` are the shared style kit.

These scripts read the project's internal parquet build through a `common.py`
module that is not redistributed, because it holds absolute paths to the raw
corpora. To run them from this repository, replace the two `C.load_articles()`
and `C.load_pooled()` calls with reads of `../../data/analysis_articles.csv` and
`../../data/analysis_events.csv`, and point `C.FIGURES` at an output folder.

The half-life and its interval are read from `../out_rest.json` so the figure
and the manuscript cannot drift apart.
