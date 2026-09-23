# -*- coding: utf-8 -*-
"""r10_figs_revised.py -- redraw Figures 3 and 4 in the ORIGINAL r04 template,
using the corrected quantities from the review reanalysis.

Nothing about the design changes. This script imports r04's fig3() and fig4()
unchanged and feeds them corrected inputs:

  * an equal follow-up window for both corpora, so panel (a) runs to
    180 days rather than 365;
  * a peak-aligned decay fit with event-cluster bootstrap intervals,
    replacing the from-day-zero fit and its lag-day standard errors.

Reach is event-weighted and unchanged by the reanalysis, so fig4 is redrawn
from the same inputs as before.

Outputs PNG at 600 dpi into figures/ and copies into the journal folder. PDFs
are removed afterwards because the manuscript includes the PNG.

Run:  python analysis/r10_figs_revised.py
"""
from __future__ import annotations
import shutil, sys
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import common as C                                   # noqa: E402
import r04_decay_reach as R4                         # noqa: E402

JOURNAL_FIGS = C.ROOT / "RoboTaxi_CrashNews_Journal" / "figures"
WINDOW = 180
SEED = 20260921
rng = np.random.default_rng(SEED)

art = C.load_articles()
pooled = C.load_pooled()

# ---------------------------------------------------------------- equal window
cutoff = min(art.loc[art.corpus == "AV", "pub"].max(),
             art.loc[art.corpus == "Ped", "pub"].max())
ev_fu = pooled[["event_id", "corpus", "event_date"]].copy()
ev_fu["fu"] = (cutoff - ev_fu.event_date).dt.days
eligible = set(ev_fu.loc[ev_fu.fu >= WINDOW, "event_id"])
a = art[(art.lag_days >= -1) & (art.event_id.isin(eligible))
        & (art.lag_days <= WINDOW)].copy()

print("equal follow-up window")
print("  cutoff %s, %d-day window" % (cutoff.date(), WINDOW))
for c in ["AV", "Ped"]:
    n_e = int((ev_fu.corpus == c).sum())
    n_k = int(ev_fu[(ev_fu.corpus == c) & (ev_fu.fu >= WINDOW)].shape[0])
    print("  %-4s events %3d of %3d retained, articles %4d"
          % (c, n_k, n_e, int((a.corpus == c).sum())))

# ---------------------------------------------------------------- decay inputs
pos = a[a.lag_days >= 0]
grid = (pd.MultiIndex.from_product([["AV", "Ped"], range(0, 15)],
                                   names=["corpus", "lag_days"]).to_frame(index=False))
cnt = pos.groupby(["corpus", "lag_days"]).size().rename("n").reset_index()
grid = grid.merge(cnt, on=["corpus", "lag_days"], how="left").fillna({"n": 0.0})


def halflife(sub, peak):
    d = sub[(sub.lag_days >= peak) & (sub.lag_days <= 14)]
    c = d.groupby("lag_days").size().reindex(range(peak, 15), fill_value=0)
    t = np.arange(len(c), dtype=float)
    X = sm.add_constant(t)
    m = sm.GLM(c.values.astype(float), X, family=sm.families.Poisson()).fit()
    lam = -float(m.params[1])
    return (np.log(2) / lam) if lam > 0 else np.nan


decay = {"grid": grid}
# The half-life and its interval come from the analysis of record
# (r08_rest.py -> out_rest.json) so the figure and the manuscript cannot drift
# apart through independent bootstrap draws. Recomputed only if that is absent.
import json
CANON = C.ROOT / "RoboTaxi_CrashNews_Journal" / "supplement" / "code" / "out_rest.json"
canon = json.loads(CANON.read_text(encoding="utf-8")) if CANON.exists() else None
print("")
print("peak-aligned decay, event-cluster bootstrap")
for c in ["AV", "Ped"]:
    s = pos[pos.corpus == c]
    peak = int(s.groupby("lag_days").size().reindex(range(0, 15), fill_value=0).idxmax())
    if canon and "halflife_peak" in canon:
        h = canon["halflife_peak"][c]
        point, lo, hi = float(h["half_life"]), float(h["lo"]), float(h["hi"])
        src = "out_rest.json"
    else:
        point = halflife(s, peak)
        ids = s.event_id.unique()
        draws = []
        for _ in range(1000):
            bs = pd.concat([s[s.event_id == i]
                            for i in rng.choice(ids, len(ids), replace=True)])
            v = halflife(bs, peak)
            if np.isfinite(v):
                draws.append(v)
        lo = float(np.percentile(draws, 2.5))
        hi = float(np.percentile(draws, 97.5))
        src = "recomputed"
    decay[c] = {"t_half": point, "ci": [lo, hi], "peak_day": peak}
    print("  %-4s peak day %d, half-life %.2f d [%.2f, %.2f]  (%s)"
          % (c, peak, point, lo, hi, src))

# tail share is article-weighted, matching the allocation bars in panel (b)
tau = {c: float((a.loc[(a.corpus == c) & (a.lag_days >= 0), "lag_days"] > 14).mean())
       for c in ["AV", "Ped"]}
print("\narticle-weighted tail beyond day 14: AV %.3f, Ped %.3f" % (tau["AV"], tau["Ped"]))

# ---------------------------------------------------------------- draw
R4.CAPTURE_HORIZON = WINDOW
R4.CAPTURE_XTICKS = [0, 1, 2, 7, 14, 30, 90, 180]
R4.fig3(decay, tau, articles=a)

art_r, _ = R4.classify_reach(art)
ev_share = R4.event_national_share(art_r, pooled)
reach = R4.reach_bootstrap(ev_share)
R4.fig4(pooled, ev_share, art_r, reach)

for n in ("fig3", "fig4"):
    png = C.FIGURES / (n + ".png")
    shutil.copy(png, JOURNAL_FIGS / (n + ".png"))
    pdf = C.FIGURES / (n + ".pdf")
    if pdf.exists():
        pdf.unlink()
    jpdf = JOURNAL_FIGS / (n + ".pdf")
    if jpdf.exists():
        jpdf.unlink()
    print("wrote %s.png at 600 dpi and removed the PDF" % n)
