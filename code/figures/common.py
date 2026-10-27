# -*- coding: utf-8 -*-
"""Portable stand-in for the project's internal common.py, so that
r10_figs_revised.py redraws Figures 3 and 4 from this repository. Data come
from ../paths.py (data/*.csv by default); figures are written to
figures_out/ at the repository root."""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import paths  # noqa: E402

ROOT = paths.REPO / "figures_out"
FIGURES = ROOT / "figures"
DATA_BUILD = paths.BUILD or paths.DATA
for d in (FIGURES, ROOT / "RoboTaxi_CrashNews_Journal" / "figures"):
    d.mkdir(parents=True, exist_ok=True)


def use_style():
    import matplotlib as mpl
    mpl.use("Agg", force=True)
    import matplotlib.pyplot as plt
    mpl.rcParams.update(mpl.rcParamsDefault)
    plt.style.use(str(HERE / "trb_news.mplstyle"))
    import warnings
    warnings.filterwarnings("ignore", message="findfont")
    return plt


def pctile_ci(draws, lo=2.5, hi=97.5):
    d = np.asarray(draws, float)
    d = d[np.isfinite(d)]
    if d.size == 0:
        return (np.nan, np.nan)
    return (float(np.percentile(d, lo)), float(np.percentile(d, hi)))


def load_pooled():
    return paths.load_pooled()


def load_articles():
    return paths.load_articles()


def update_results(section, payload):
    """The internal build logs results here; the figures need nothing back."""


def write_qa_section(key, body):
    """The internal build writes a QA log here; not needed for the figures."""
