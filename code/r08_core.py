# -*- coding: utf-8 -*-
"""r08_core.py -- headline and severity contrasts, inference routes and the
injury influence analysis.

Refits the amplification contrast under metro-by-period CELL fixed effects
restricted to cells containing both corpora (common support), with PPML as the
primary mean-model estimator, a design-preserving stratified bootstrap that
returns a statistic on every replicate, and a within-cell permutation test.
Adds leave-one-event-out and prespecified top-k exclusions for the injury
contrast.

Writes rean/out_core.json. Reads only; never regenerates the parquets.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(r"D:\OneDrive - Texas State University\AIT\Papers\TRB2027\Crash News"
            r"\TRB2027\TRB_R_robotaxi_amplification")
DB = ROOT / "data_build"
OUT = Path(__file__).resolve().parent

SEED = 20260921
N_BOOT = 2000
B_PERM = 5000
rng = np.random.default_rng(SEED)

pooled = pd.read_parquet(DB / "pooled.parquet").copy()
pooled["cell"] = pooled.metro.astype(str) + " | " + pooled.year_bin.astype(str)

# ---- common support: cells containing BOTH corpora -----------------------
g = pooled.groupby("cell").AV.agg(["sum", "count"])
both = g[(g["sum"] > 0) & (g["sum"] < g["count"])].index
overlap = pooled[pooled.cell.isin(both)].copy()


# ---------------- estimation engine ---------------------------------------
def pois_irls(X, y, iters=200, tol=1e-10):
    """Poisson IRLS. Always returns a coefficient vector (no convergence flag
    needed for resampling)."""
    b = np.zeros(X.shape[1])
    for _ in range(iters):
        mu = np.exp(np.clip(X @ b, -30, 30))
        gr = X.T @ (y - mu)
        H = (X * mu[:, None]).T @ X
        try:
            step = np.linalg.solve(H + 1e-10 * np.eye(len(b)), gr)
        except np.linalg.LinAlgError:
            step = np.linalg.lstsq(H, gr, rcond=None)[0]
        b += step
        if np.max(np.abs(step)) < tol:
            break
    return b


def design(df, treat_cols, fe_col="cell"):
    parts = [np.ones((len(df), 1))]
    names = ["const"]
    for c in treat_cols:
        parts.append(df[[c]].values.astype(float))
        names.append(c)
    d = pd.get_dummies(df[fe_col].astype(str), prefix="fe", drop_first=True)
    # drop all-zero columns that can appear after subsetting
    d = d.loc[:, d.values.sum(axis=0) > 0]
    parts.append(d.values.astype(float))
    names += list(d.columns)
    return np.hstack(parts), names


def ppml(df, treat_cols, fe_col="cell"):
    """Poisson QMLE with HC1 robust covariance -- consistent for the
    conditional-mean ratio regardless of the true variance function."""
    import statsmodels.api as sm
    X, names = design(df, treat_cols, fe_col)
    y = df["n_articles"].values.astype(float)
    m = sm.GLM(y, X, family=sm.families.Poisson()).fit(cov_type="HC1")
    out = {}
    for c in treat_cols:
        i = names.index(c)
        out[c] = {"af": float(np.exp(m.params[i])),
                  "lo": float(np.exp(m.params[i] - 1.96 * m.bse[i])),
                  "hi": float(np.exp(m.params[i] + 1.96 * m.bse[i]))}
    return out, X, names


def boot_af(df, treat_cols, fe_col="cell", strata=("metro", "year_bin", "corpus"),
            n_boot=N_BOOT):
    """Stratified bootstrap preserving metro x period x corpus.
    Poisson IRLS returns an estimate on every replicate."""
    idx = [np.asarray(v) for v in df.groupby(list(strata)).indices.values()]
    X, names = design(df, treat_cols, fe_col)
    y = df["n_articles"].values.astype(float)
    ti = [names.index(c) for c in treat_cols]
    draws = {c: [] for c in treat_cols}
    n_singular = 0
    for _ in range(n_boot):
        take = np.concatenate([rng.choice(v, size=len(v), replace=True) for v in idx])
        Xb, yb = X[take], y[take]
        keep = Xb.sum(axis=0) != 0
        keep[0] = True
        for t in ti:
            keep[t] = True
        if np.linalg.matrix_rank(Xb[:, keep]) < keep.sum():
            n_singular += 1
        b = pois_irls(Xb[:, keep], yb)
        pos = np.where(keep)[0]
        for c, t in zip(treat_cols, ti):
            draws[c].append(float(np.exp(b[list(pos).index(t)])))
    return ({c: {"lo": float(np.percentile(v, 2.5)),
                 "hi": float(np.percentile(v, 97.5)),
                 "median": float(np.median(v)),
                 "n_ok": int(np.isfinite(v).sum())}
             for c, v in draws.items()},
            n_singular)


def perm_p(df, treat_col, fe_col="cell", b=B_PERM):
    """Shuffle the corpus label WITHIN each metro-by-period cell and refit.
    For a severity contrast the permuted label is assigned only among the
    human-fatal events and the robotaxi events of that severity."""
    X, names = design(df, [treat_col], fe_col)
    y = df["n_articles"].values.astype(float)
    ti = names.index(treat_col)
    obs = abs(pois_irls(X, y)[ti])
    cells = df[fe_col].values
    lab = df[treat_col].values.astype(float).copy()
    cnt = 0
    for _ in range(b):
        sh = lab.copy()
        for c in np.unique(cells):
            m = cells == c
            sh[m] = rng.permutation(sh[m])
        Xp = X.copy()
        Xp[:, ti] = sh
        if abs(pois_irls(Xp, y)[ti]) >= obs:
            cnt += 1
    return (1 + cnt) / (b + 1)


res = {"seed": SEED, "n_boot": N_BOOT, "b_perm": B_PERM}

# ---------------- 1. headline, additive FE vs cell FE ---------------------
print("=" * 72)
print("additive metro+period FE  vs  metro-by-period CELL FE")
print("=" * 72)

add, _, _ = ppml(pooled, ["AV"], fe_col="cell")  # placeholder replaced below
# additive FE on the full frame, exactly as the paper currently does
import statsmodels.api as sm


def ppml_additive(df, treat_cols):
    parts = [np.ones((len(df), 1))]
    names = ["const"]
    for c in treat_cols:
        parts.append(df[[c]].values.astype(float))
        names.append(c)
    for f in ("metro", "year_bin"):
        d = pd.get_dummies(df[f].astype(str), prefix=f, drop_first=True)
        d = d.loc[:, d.values.sum(axis=0) > 0]
        parts.append(d.values.astype(float))
        names += list(d.columns)
    X = np.hstack(parts)
    y = df["n_articles"].values.astype(float)
    m = sm.GLM(y, X, family=sm.families.Poisson()).fit(cov_type="HC1")
    return {c: {"af": float(np.exp(m.params[names.index(c)])),
                "lo": float(np.exp(m.params[names.index(c)] - 1.96 * m.bse[names.index(c)])),
                "hi": float(np.exp(m.params[names.index(c)] + 1.96 * m.bse[names.index(c)]))}
            for c in treat_cols}


a_full = ppml_additive(pooled, ["AV"])["AV"]
a_ovl = ppml_additive(overlap, ["AV"])["AV"]
c_ovl, _, _ = ppml(overlap, ["AV"])
c_ovl = c_ovl["AV"]
print(f"  additive FE, all 797      AF = {a_full['af']:.2f}  [{a_full['lo']:.2f}, {a_full['hi']:.2f}]")
print(f"  additive FE, 429 overlap  AF = {a_ovl['af']:.2f}  [{a_ovl['lo']:.2f}, {a_ovl['hi']:.2f}]")
print(f"  CELL FE,     429 overlap  AF = {c_ovl['af']:.2f}  [{c_ovl['lo']:.2f}, {c_ovl['hi']:.2f}]  <-- primary")
res["headline"] = {"additive_full": a_full, "additive_overlap": a_ovl,
                   "cell_overlap": c_ovl,
                   "n_overlap": int(len(overlap)),
                   "n_cells_both": int(len(both)),
                   "n_av_overlap": int(overlap.AV.sum())}

bb, nsing = boot_af(overlap, ["AV"])
res["headline"]["cell_overlap_boot"] = bb["AV"]
res["headline"]["boot_singular"] = nsing
pv = perm_p(overlap, "AV")
res["headline"]["cell_overlap_perm_p"] = pv
print(f"  bootstrap [{bb['AV']['lo']:.2f}, {bb['AV']['hi']:.2f}] "
      f"(rank-deficient replicates: {nsing}/{N_BOOT}) | permutation p = {pv:.4f}")

# ---------------- 2. severity contrasts under cell FE --------------------
print()
print("=" * 72)
print("SEVERITY CONTRASTS under cell FE on overlap cells")
print("=" * 72)
sev_out = {}
for sev in ["PDO", "Injury"]:
    sub = overlap[(overlap.AV == 0) | (overlap.severity == sev)].copy()
    sub["T"] = ((sub.AV == 1) & (sub.severity == sev)).astype(float)
    # keep only cells that still contain both groups after subsetting
    gg = sub.groupby("cell").T.agg(["sum", "count"])
    keep = gg[(gg["sum"] > 0) & (gg["sum"] < gg["count"])].index
    sub = sub[sub.cell.isin(keep)]
    est, _, _ = ppml(sub, ["T"])
    b2, ns2 = boot_af(sub, ["T"])
    p2 = perm_p(sub, "T")
    n_t = int(sub["T"].sum())
    sev_out[sev] = {"af": est["T"]["af"], "wald_lo": est["T"]["lo"], "wald_hi": est["T"]["hi"],
                    "boot_lo": b2["T"]["lo"], "boot_hi": b2["T"]["hi"],
                    "perm_p": p2, "n_treat": n_t, "n_total": int(len(sub)),
                    "n_cells": int(len(keep)), "boot_singular": ns2}
    print(f"  AV {sev:7s} n={n_t:3d}  AF = {est['T']['af']:.2f}  "
          f"boot [{b2['T']['lo']:.2f}, {b2['T']['hi']:.2f}]  perm p = {p2:.4f}")
res["severity"] = sev_out

# ---------------- 3. injury influence analysis ----------------
print()
print("=" * 72)
print("influence of individual injury events")
print("=" * 72)
sub = overlap[(overlap.AV == 0) | (overlap.severity == "Injury")].copy()
sub["T"] = ((sub.AV == 1) & (sub.severity == "Injury")).astype(float)
gg = sub.groupby("cell").T.agg(["sum", "count"])
keep = gg[(gg["sum"] > 0) & (gg["sum"] < gg["count"])].index
sub = sub[sub.cell.isin(keep)].copy()
inj = sub[sub["T"] == 1].sort_values("n_articles", ascending=False)
print(f"  injury events in estimation set: {len(inj)}  "
      f"articles: {sorted(inj.n_articles.tolist(), reverse=True)}")

loo = []
for eid in inj.event_id:
    s2 = sub[sub.event_id != eid]
    gg2 = s2.groupby("cell").T.agg(["sum", "count"])
    k2 = gg2[(gg2["sum"] > 0) & (gg2["sum"] < gg2["count"])].index
    s2 = s2[s2.cell.isin(k2)]
    if s2["T"].sum() == 0:
        continue
    e = ppml(s2, ["T"])[0]["T"]["af"]
    loo.append({"dropped": eid,
                "n_articles": int(inj.loc[inj.event_id == eid, "n_articles"].iloc[0]),
                "af": e})
loo_af = [x["af"] for x in loo]
print(f"  leave-one-injury-event-out AF range: {min(loo_af):.2f} to {max(loo_af):.2f}")
for x in sorted(loo, key=lambda z: z["af"])[:3]:
    print(f"     dropping the {x['n_articles']}-article event -> AF {x['af']:.2f}")

topk = {}
for k in (1, 2, 4):
    drop = set(inj.event_id.head(k))
    s2 = sub[~sub.event_id.isin(drop)]
    gg2 = s2.groupby("cell").T.agg(["sum", "count"])
    k2 = gg2[(gg2["sum"] > 0) & (gg2["sum"] < gg2["count"])].index
    s2 = s2[s2.cell.isin(k2)].copy()
    e = ppml(s2, ["T"])[0]["T"]
    b3, _ = boot_af(s2, ["T"], n_boot=1000)
    p3 = perm_p(s2, "T", b=2000)
    topk[f"drop_top{k}"] = {"af": e["af"], "boot_lo": b3["T"]["lo"],
                            "boot_hi": b3["T"]["hi"], "perm_p": p3,
                            "n_treat": int(s2["T"].sum())}
    print(f"  drop top-{k}: n={int(s2['T'].sum()):2d}  AF = {e['af']:.2f}  "
          f"boot [{b3['T']['lo']:.2f}, {b3['T']['hi']:.2f}]  perm p = {p3:.4f}")
res["injury_influence"] = {"loo": loo, "loo_min": min(loo_af), "loo_max": max(loo_af),
                           "topk": topk}

(OUT / "out_core.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
print("\nwrote out_core.json")
