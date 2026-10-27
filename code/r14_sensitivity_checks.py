# -*- coding: utf-8 -*-
"""r14_sensitivity_checks.py -- further sensitivity checks on the three
coverage contrasts.

1. Local-outlet injury contrast after the prespecified top-k exclusions.
2. Amplification factor on coverage published within 14 days of the crash,
   where articles in both lanes are direct incident reports.
3. Event-weighted lag quantiles, lag quantiles without the most covered
   events, and the lag to the first article of each event.
4. The persistence and outlet-composition contrasts within the overlap cells,
   with cell fixed effects.
5. Cells, comparison events and singleton strata behind each subset fit.

Writes out_sensitivity.json. Reads only; never regenerates the parquets.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
from paths import load_pooled, load_articles, national_domains
import statsmodels.api as sm

HERE = Path(__file__).resolve().parent
SEED, N_BOOT, W = 20260921, 2000, 180
rng = np.random.default_rng(SEED)

pooled = load_pooled().copy()
arts = load_articles().copy()
natset = set(national_domains().domain.astype(str).str.lower().str.strip())
arts["is_nat"] = arts.source_domain.astype(str).str.lower().str.strip().isin(natset)
pooled["cell"] = pooled.metro.astype(str) + " | " + pooled.year_bin.astype(str)


def overlap_of(df, treat):
    g = df.groupby("cell")[treat].agg(["sum", "count"])
    k = g[(g["sum"] > 0) & (g["sum"] < g["count"])].index
    return df[df.cell.isin(k)].copy()


overlap = overlap_of(pooled, "AV")
cnt = lambda mask: arts[mask].groupby("event_id").size()
for col, mask in [("n_local", ~arts.is_nat),
                  ("n_early", (arts.lag_days >= -1) & (arts.lag_days <= 14))]:
    pooled[col] = pooled.event_id.map(cnt(mask)).fillna(0).astype(int)
    overlap[col] = overlap.event_id.map(cnt(mask)).fillna(0).astype(int)


def design(df, treat):
    d = pd.get_dummies(df.cell.astype(str), prefix="fe", drop_first=True)
    d = d.loc[:, d.values.sum(axis=0) > 0]
    X = np.hstack([np.ones((len(df), 1)), df[[treat]].values.astype(float), d.values.astype(float)])
    return X


def irls(X, y, iters=200, tol=1e-10):
    b = np.zeros(X.shape[1])
    for _ in range(iters):
        mu = np.exp(np.clip(X @ b, -30, 30))
        step = np.linalg.lstsq((X * mu[:, None]).T @ X + 1e-10 * np.eye(len(b)),
                               X.T @ (y - mu), rcond=None)[0]
        b += step
        if np.max(np.abs(step)) < tol:
            break
    return b


def fit(df, outcome, treat, n_boot=N_BOOT):
    """PPML with HC1 Wald bounds and the metro x period x corpus bootstrap."""
    X = design(df, treat)
    y = df[outcome].values.astype(float)
    m = sm.GLM(y, X, family=sm.families.Poisson()).fit(cov_type="HC1")
    idx = [np.asarray(v) for v in df.groupby(["metro", "year_bin", "corpus"]).indices.values()]
    draws = np.empty(n_boot)
    for b in range(n_boot):
        take = np.concatenate([rng.choice(v, len(v), replace=True) for v in idx])
        Xb, yb = X[take], y[take]
        keep = Xb.sum(axis=0) != 0
        keep[:2] = True
        draws[b] = np.exp(irls(Xb[:, keep], yb)[1])
    tc = df[df[treat] == 1].groupby("cell").size()
    return {"af": float(np.exp(m.params[1])),
            "wald_lo": float(np.exp(m.params[1] - 1.96 * m.bse[1])),
            "wald_hi": float(np.exp(m.params[1] + 1.96 * m.bse[1])),
            "boot_lo": float(np.percentile(draws, 2.5)),
            "boot_hi": float(np.percentile(draws, 97.5)),
            "n_treat": int(df[treat].sum()), "n_comp": int((df.AV == 0).sum()),
            "n_cells": int(df.cell.nunique()), "singleton_cells": int((tc == 1).sum())}


def stratum(base, sev=None, drop=(), ids=None):
    sub = base[(base.AV == 0) | ((base.severity == sev) if sev else (base.AV == 1))].copy()
    if ids is not None:
        sub = sub[(sub.AV == 0) | sub.event_id.isin(ids)]
    sub = sub[~sub.event_id.isin(set(drop))]
    sub["T"] = sub.AV.astype(float)
    return overlap_of(sub, "T")


res = {"seed": SEED, "n_boot": N_BOOT}
inj_rank = overlap[(overlap.AV == 1) & (overlap.severity == "Injury")] \
    .sort_values("n_articles", ascending=False).event_id.tolist()

# ---- 1 and 2: local-outlet and early-window contrasts ----------------------
print("local-outlet and early-window contrasts (zeros retained)")
for outcome in ["n_local", "n_early"]:
    rows = {"all": fit(stratum(overlap), outcome, "T"),
            "PDO": fit(stratum(overlap, "PDO"), outcome, "T"),
            "Injury": fit(stratum(overlap, "Injury"), outcome, "T")}
    for k in (1, 4):
        rows[f"Injury_drop_top{k}"] = fit(stratum(overlap, "Injury", inj_rank[:k]), outcome, "T")
    res[outcome] = rows
    for lab, r in rows.items():
        print(f"  {outcome:8s} {lab:17s} n={r['n_treat']:2d}  AF {r['af']:6.2f} "
              f"boot [{r['boot_lo']:.2f}, {r['boot_hi']:.2f}]  cells {r['n_cells']}")

# ---- 5: what sits behind each subset fit ------------------------------------
codes = pd.read_csv(HERE.parent / "data" / "human_validation_codes.csv", keep_default_na=False)
sv = codes[codes.task == "sev"]
conf = {s: set(sv[(sv.pipeline_label == lab) & (sv.adjudicated == s.upper())].source_id)
        for s, lab in [("Injury", "Injury"), ("PDO", "Property Damage Only")]}
specs = {"all": stratum(overlap), "PDO": stratum(overlap, "PDO"),
         "Injury": stratum(overlap, "Injury"),
         "Injury_confirmed": stratum(overlap, "Injury", ids=conf["Injury"]),
         "PDO_confirmed": stratum(overlap, "PDO", ids=conf["PDO"])}
for k in (1, 2, 4):
    specs[f"Injury_drop_top{k}"] = stratum(overlap, "Injury", inj_rank[:k])
for era in ["pre", "post"]:
    s = pooled[(pooled.AV == 0) | (pooled.era == era)].copy()
    s["T"] = ((s.AV == 1) & (s.era == era)).astype(float)
    specs[f"era_{era}"] = overlap_of(s, "T")
for op in ["Waymo", "Cruise", "Zoox", "Tesla"]:
    s = pooled[(pooled.AV == 0) | (pooled.operator == op)].copy()
    s["T"] = ((s.AV == 1) & (s.operator == op)).astype(float)
    specs[f"op_{op}"] = overlap_of(s, "T")
sizes = {}
for lab, d in specs.items():
    tc = d[d["T"] == 1].groupby("cell").size()
    sizes[lab] = {"n_treat": int(d["T"].sum()), "n_comp": int((d["T"] == 0).sum()),
                  "n_cells": int(d.cell.nunique()), "singleton_cells": int((tc == 1).sum())}
    print(f"  {lab:18s} {sizes[lab]}")
res["subset_sizes"] = sizes
res["in_window_operators"] = pooled[pooled.AV == 1].operator.value_counts().to_dict()

# ---- 3: timing on the equal follow-up window --------------------------------
cutoff = min(arts[arts.corpus == "AV"].pub.max(), arts[arts.corpus == "Ped"].pub.max())
ev = pooled[["event_id", "corpus", "event_date", "cell", "AV", "is_cruise_drag"]].copy()
elig = set(ev[(cutoff - ev.event_date).dt.days >= W].event_id)
a = arts[(arts.lag_days >= -1) & (arts.lag_days <= W) & arts.event_id.isin(elig)].copy()
a["w"] = 1.0 / a.groupby("event_id").event_id.transform("size")


def wq(x, w, q):
    o = np.argsort(x)
    x, w = np.asarray(x)[o], np.asarray(w)[o]
    c = np.cumsum(w) / w.sum()
    return float(x[np.searchsorted(c, q)])


top4 = pooled[pooled.AV == 1].sort_values("n_articles", ascending=False).event_id.head(4).tolist()
cruise = pooled[pooled.is_cruise_drag == 1].event_id.tolist()
timing = {}
for c in ["AV", "Ped"]:
    s = a[a.corpus == c]
    first = s.groupby("event_id").lag_days.min()
    n_ev = s.groupby("event_id").size()
    multi = n_ev[n_ev > 1].index
    tail_ev = s.groupby("event_id").apply(lambda g: (g.lag_days > 14).mean(), include_groups=False)
    t = {"n_events": int(s.event_id.nunique()), "n_articles": int(len(s)),
         "p50_article": float(s.lag_days.median()), "p90_article": float(s.lag_days.quantile(.9)),
         "p50_event_weighted": wq(s.lag_days, s.w, .5), "p90_event_weighted": wq(s.lag_days, s.w, .9),
         "first_lag_median": float(first.median()),
         "first_after_14_share": float((first > 14).mean()),
         "n_single": int((n_ev == 1).sum()),
         "single_after_14_share": float((first[n_ev[n_ev == 1].index] > 14).mean()),
         "multi_tail_share_mean": float(tail_ev[multi].mean()) if len(multi) else None,
         "n_multi": int(len(multi))}
    if c == "AV":
        for lab, drop in [("no_cruise", cruise), ("no_top4", top4)]:
            r = s[~s.event_id.isin(drop)]
            te = tail_ev.drop([x for x in drop if x in tail_ev.index])
            t[lab] = {"n_events": int(r.event_id.nunique()), "n_articles": int(len(r)),
                      "p50_article": float(r.lag_days.median()),
                      "p90_article": float(r.lag_days.quantile(.9)),
                      "p90_event_weighted": wq(r.lag_days, r.w, .9),
                      "tail_share_event_mean": float(te.mean())}
    timing[c] = t
    print(f"  timing {c}: {t}")
res["timing"] = timing


# ---- 4: persistence and composition within the overlap cells ----------------
def cell_diff(df, ycol):
    d = pd.get_dummies(df.cell.astype(str), prefix="fe", drop_first=True).astype(float)
    X = np.hstack([np.ones((len(df), 1)), df[["AV"]].values.astype(float), d.values])
    m = sm.OLS(df[ycol].values.astype(float), X).fit(cov_type="HC1")
    return {"diff": float(m.params[1]), "lo": float(m.params[1] - 1.96 * m.bse[1]),
            "hi": float(m.params[1] + 1.96 * m.bse[1]),
            "mean_av": float(df[df.AV == 1][ycol].mean()), "mean_ped": float(df[df.AV == 0][ycol].mean()),
            "n_av": int(df.AV.sum()), "n_ped": int((df.AV == 0).sum()), "n_cells": int(df.cell.nunique())}


tail_share = a.groupby("event_id").apply(lambda g: (g.lag_days > 14).mean(), include_groups=False)
nat_share = arts.groupby("event_id").is_nat.mean()
ot = overlap[overlap.event_id.isin(tail_share.index)].copy()
ot["tail"] = ot.event_id.map(tail_share)
ot = overlap_of(ot, "AV")
on = overlap.copy()
on["nat"] = on.event_id.map(nat_share)
res["within_cells"] = {"tail_share": cell_diff(ot, "tail"), "national_share": cell_diff(on, "nat")}
print(f"  within cells: {res['within_cells']}")

(HERE / "out_sensitivity.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
print("wrote out_sensitivity.json")
