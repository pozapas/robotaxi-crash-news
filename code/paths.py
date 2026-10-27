# -*- coding: utf-8 -*-
"""Where the analysis scripts find their inputs.

By default every script reads the CSV files in this repository's data/
folder. Set the environment variable ROBOTAXI_BUILD to a folder holding
pooled.parquet, articles.parquet and national_domains.csv to read the full
build instead; the two sources hold the same rows in the same order, so the
seeded resampling gives identical results.

r09_syndication.py and r12_lane_provenance.py also need the raw discovery
exports, which carry article text and are not redistributed. Point
ROBOTAXI_RAW_AV and ROBOTAXI_RAW_PED at those export folders to run them.
check_manuscript_numbers.py needs the manuscript source in ROBOTAXI_MANUSCRIPT.
"""
from __future__ import annotations
import os
from pathlib import Path
import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[1]
DATA = REPO / "data"
BUILD = Path(os.environ["ROBOTAXI_BUILD"]) if os.environ.get("ROBOTAXI_BUILD") else None


def _env_path(name):
    v = os.environ.get(name)
    return Path(v) if v else None


RAW_AV = _env_path("ROBOTAXI_RAW_AV")
RAW_PED = _env_path("ROBOTAXI_RAW_PED")
MANUSCRIPT = _env_path("ROBOTAXI_MANUSCRIPT")


def load_pooled() -> pd.DataFrame:
    """One row per event in the analysis frame."""
    if BUILD:
        return pd.read_parquet(BUILD / "pooled.parquet")
    d = pd.read_csv(DATA / "analysis_events.csv", parse_dates=["event_date"])
    d["year"] = d.event_date.dt.year
    d["log_n"] = np.log(d.n_articles)
    # The October 2023 Cruise crash is the most covered robotaxi event.
    top = d[d.AV == 1].n_articles.idxmax()
    d["is_cruise_drag"] = d.index == top
    d["mega_event"] = d["is_cruise_drag"]
    return d


def load_articles() -> pd.DataFrame:
    """One row per linked article."""
    if BUILD:
        return pd.read_parquet(BUILD / "articles.parquet")
    return pd.read_csv(DATA / "analysis_articles.csv", parse_dates=["pub", "event_date"])


def national_domains() -> pd.DataFrame:
    return pd.read_csv((BUILD or DATA) / "national_domains.csv")


def require(path, name):
    if path is None or not Path(path).exists():
        raise SystemExit(f"{name} is not set or does not exist; see code/paths.py.")
    return Path(path)
