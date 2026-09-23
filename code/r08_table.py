# -*- coding: utf-8 -*-
"""r08_table.py -- remaining Table 4 rows under the new primary specification
(PPML, metro-by-period cell fixed effects, overlap cells, design-preserving
stratified bootstrap that returns an estimate on every replicate).

Addresses issues #13, #14, #20, #21. Writes rean/out_table.json.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(r"D:\OneDrive - Texas State University\AIT\Papers\TRB2027\Crash News"
            r"\TRB2027\TRB_R_robotaxi_amplification")
DB = ROOT / "data_build"
OUT = Path(__file__).resolve().parent
SEED = 20260921
N_BOOT = 2000
rng = np.random.default_rng(SEED)

pooled = pd.read_parquet(DB / "pooled.parquet").copy()
pooled["cell"] = pooled.metro.astype(str) + " | " + pooled.year_bin.astype(str)


def overlap_of(df, treat):
    g = df.groupby("cell")[treat].agg(["sum", "count"])
    k = g[(g["sum"] > 0) & (g["sum"] < g["count"])].index
    return df[df.cell.isin(k)].copy()


def design(df, treat):
    parts = [np.ones((len(df), 1)), df[[treat]].values.astype(float)]
    names = ["const", treat]
    d = pd.get_dummies(df.cell.astype(str), prefix="fe", drop_first=True)
    d = d.loc[:, d.values.sum(axis=0) > 0]
    parts.append(d.values.astype(float))
    names += list(d.columns)
    return np.hstack(parts), names


def irls(X, y, iters=200, tol=1e-10):
    b = np.zeros(X.shape[1])
    for _ in range(iters):
        mu = np.exp(np.clip(X @ b, -30, 30))
        H = (X * mu[:, None]).T @ X
        try:
            step = np.linalg.solve(H + 1e-10 * np.eye(len(b)), X.T @ (y - mu))
        except np.linalg.LinAlgError:
            step = np.linalg.lstsq(H, X.T @ (y - mu), rcond=None)[0]
        b += step
        if np.max(np.abs(step)) < tol:
            break
    return b


def row(df, treat, outcome="n_articles", n_boot=N_BOOT):
    """Point estimate (PPML/HC1) + design-preserving bootstrap. Every replicate
    yields an estimate, so no replicate is ever discarded."""
    d = overlap_of(df, treat)
    if d[treat].sum() == 0 or len(d) == 0:
        return None
    X, names = design(d, treat)
    y = d[outcome].values.astype(float)
    m = sm.GLM(y, X, family=sm.families.Poisson()).fit(cov_type="HC1")
    i = names.index(treat)
    idx = [np.asarray(v) for v in d.groupby(["metro", "year_bin", "corpus"]).indices.values()]
    draws = np.empty(n_boot)
    for b in range(n_boot):
        take = np.concatenate([rng.choice(v, len(v), replace=True) for v in idx])
        Xb, yb = X[take], y[take]
        keep = Xb.sum(axis=0) != 0
        keep[0] = True
        keep[i] = True
        bb = irls(Xb[:, keep], yb)
        draws[b] = np.exp(bb[list(np.where(keep)[0]).index(i)])
    draws = np.clip(draws, 1e-6, 1e6)
    return {"af": float(np.exp(m.params[i])),
            "boot_lo": float(np.percentile(draws, 2.5)),
            "boot_hi": float(np.percentile(draws, 97.5)),
            "n_treat": int(d[treat].sum()), "n_total": int(len(d)),
            "n_replicates_used": int(n_boot), "n_replicates_discarded": 0}


res = {"seed": SEED, "n_boot": N_BOOT}

# ---- by operator -------------------------------------------------------
print("BY OPERATOR (every bootstrap replicate retained)")
ops = {}
for op in sorted(pooled[pooled.AV == 1].operator.dropna().unique()):
    sub = pooled[(pooled.AV == 0) | (pooled.operator == op)].copy()
    sub["T"] = ((sub.AV == 1) & (sub.operator == op)).astype(float)
    r = row(sub, "T")
    if r and r["n_treat"] >= 2:
        ops[op] = r
        print(f"  {op:9s} n={r['n_treat']:3d}  AF = {r['af']:6.2f}  "
              f"[{r['boot_lo']:.2f}, {r['boot_hi']:.2f}]  discarded={r['n_replicates_discarded']}")
res["operator"] = ops

# ---- by era ------------------------------------------------------------
print("\nBY ERA")
eras = {}
for era in ["pre", "post"]:
    sub = pooled[(pooled.AV == 0) | (pooled.era == era)].copy()
    sub["T"] = ((sub.AV == 1) & (sub.era == era)).astype(float)
    r = row(sub, "T")
    if r:
        eras[era] = r
        print(f"  {era:5s} n={r['n_treat']:3d}  AF = {r['af']:.2f}  "
              f"[{r['boot_lo']:.2f}, {r['boot_hi']:.2f}]")
res["era"] = eras

# ---- jackknife over metros (point estimates only) ----------------------
print("\nJACKKNIFE drop-one-metro (POINT estimates, not an interval)")
jk = {}
for mtr in sorted(pooled.metro.unique()):
    sub = pooled[pooled.metro != mtr].copy()
    d = overlap_of(sub, "AV")
    if d.AV.sum() == 0:
        continue
    X, names = design(d, "AV")
    m = sm.GLM(d.n_articles.values.astype(float), X,
               family=sm.families.Poisson()).fit(cov_type="HC1")
    jk[mtr] = float(np.exp(m.params[names.index("AV")]))
    print(f"  drop {mtr:12s} AF = {jk[mtr]:.2f}")
res["jackknife"] = {"by_metro": jk, "min": min(jk.values()), "max": max(jk.values())}

# ---- exclude the Cruise dragging event ---------------------------------
print("\nEXCLUDING the Cruise dragging event")
sub = pooled[~pooled.is_cruise_drag].copy()
r = row(sub, "AV")
res["excl_cruise"] = r
print(f"  n_AV={r['n_treat']}  AF = {r['af']:.2f}  [{r['boot_lo']:.2f}, {r['boot_hi']:.2f}]")

# ---- outcome: unique outlets -------------------------------------------
print("\nOUTCOME = unique outlets")
r = row(pooled, "AV", outcome="n_outlets")
res["unique_outlets"] = r
print(f"  AF = {r['af']:.2f}  [{r['boot_lo']:.2f}, {r['boot_hi']:.2f}]")

# ---- zero-truncated NB comparison --------------------------
print("\nZERO-TRUNCATED NB comparison")
try:
    from statsmodels.discrete.truncated_model import TruncatedLFNegativeBinomialP
    d = overlap_of(pooled, "AV")
    X, names = design(d, "AV")
    mt = TruncatedLFNegativeBinomialP(d.n_articles.values.astype(float), X,
                                      truncation=0, p=2).fit(disp=0, maxiter=300)
    i = names.index("AV")
    res["ztnb"] = {"af": float(np.exp(mt.params[i])),
                   "lo": float(np.exp(mt.params[i] - 1.96 * mt.bse[i])),
                   "hi": float(np.exp(mt.params[i] + 1.96 * mt.bse[i])),
                   "converged": bool(mt.mle_retvals.get("converged", False))}
    print(f"  ZTNB AF = {res['ztnb']['af']:.2f} "
          f"[{res['ztnb']['lo']:.2f}, {res['ztnb']['hi']:.2f}] "
          f"converged={res['ztnb']['converged']}")
except Exception as e:
    res["ztnb"] = {"error": str(e)}
    print("  ZTNB unavailable:", e)

(OUT / "out_table.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
print("\nwrote out_table.json")
