# -*- coding: utf-8 -*-
"""r13_human_validation.py -- human validation of the extracted fields.

Reads data/human_validation_codes.csv (two independent coders on 516 items,
with adjudication of every disagreement) and reports, per task, raw agreement,
Cohen's kappa and Gwet's AC1; the adjudicated discovery precision and recall
per lane, reweighted to the four sampling strata with a stratified bootstrap;
the adjudicated false-link rates; agreement of the pipeline's severity label
with the adjudicated code; and the severity contrasts refitted on events whose
severity the coders confirmed. Writes out_validation.json.
"""
from __future__ import annotations
import json
from pathlib import Path
import numpy as np
import pandas as pd
from paths import load_pooled, load_articles, national_domains
import statsmodels.api as sm

HERE = Path(__file__).resolve().parent
DATA = HERE.parent / "data"
SEED, N_BOOT = 20260921, 2000
rng = np.random.default_rng(SEED)
codes = pd.read_csv(DATA / "human_validation_codes.csv", keep_default_na=False)
sizes = json.loads((DATA / "strata_sizes.json").read_text(encoding="utf-8"))
res = {"seed": SEED, "n_items": int(len(codes))}


def kappa(a, b):
    labs = sorted(set(a) | set(b))
    M = pd.crosstab(pd.Categorical(a, labs), pd.Categorical(b, labs), dropna=False).values.astype(float)
    n = M.sum(); po = np.trace(M) / n; pe = (M.sum(0) * M.sum(1)).sum() / n ** 2
    return (po - pe) / (1 - pe), po


def ac1(a, b):
    labs = sorted(set(a) | set(b)); q = len(labs)
    po = float(np.mean(np.asarray(a) == np.asarray(b)))
    pi = np.array([((np.asarray(a) == k).mean() + (np.asarray(b) == k).mean()) / 2 for k in labs])
    pe = (pi * (1 - pi)).sum() / (q - 1)
    return (po - pe) / (1 - pe)


def wilson(k, n, z=1.96):
    p = k / n; d = 1 + z * z / n; c = (p + z * z / (2 * n)) / d
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, c - h), min(1.0, c + h)


# ---------------- agreement ----------------
print("=" * 72); print("INTER-CODER AGREEMENT (516 items, two coders)"); print("=" * 72)
agree = {}
for t in ["rel_av", "rel_ped", "sev", "link_av", "link_ped"]:
    s = codes[codes.task == t]
    k, po = kappa(s.coder_1, s.coder_2)
    a = ac1(s.coder_1.values, s.coder_2.values)
    agree[t] = {"n": int(len(s)), "raw": po, "kappa": k, "ac1": a,
                "disagreements": int((s.coder_1 != s.coder_2).sum())}
    print("  %-9s n=%3d  raw %.3f  kappa %.3f  AC1 %.3f  disagreements %d"
          % (t, len(s), po, k, a, agree[t]["disagreements"]))
res["agreement"] = agree
res["n_adjudicated"] = int(sum(v["disagreements"] for v in agree.values()))

# ---------------- discovery precision and recall ----------------
print(); print("=" * 72); print("DISCOVERY (adjudicated, reweighted to strata)"); print("=" * 72)
ST = ["candidate", "rejected_high_risk", "rejected_other_text", "rejected_no_text"]
disc = {}
for t, lane in [("rel_av", "robotaxi"), ("rel_ped", "pedestrian")]:
    s = codes[codes.task == t].reset_index(drop=True).copy()
    s["y"] = s.adjudicated.eq("YES").astype(float)
    N = sizes[lane]

    def est(g, text_only=False):
        p = {st: (g[g.stratum == st].y.mean() if (g.stratum == st).any() else 0.0) for st in ST}
        use = ST[:-1] if text_only else ST
        tp = p["candidate"] * N["candidate"]
        return p["candidate"], tp / sum(p[st] * N[st] for st in use)
    idx = {st: s.index[s.stratum == st].values for st in ST}
    out = {}
    for lab, kw in [("all", {}), ("text_only", {"text_only": True})]:
        pr, rc = est(s, **kw)
        bs = np.array([est(s.loc[np.concatenate([rng.choice(v, len(v)) for v in idx.values()])], **kw)
                       for _ in range(N_BOOT)])
        lo, hi = np.nanpercentile(bs, [2.5, 97.5], axis=0)
        out[lab] = {"precision": pr, "prec_lo": lo[0], "prec_hi": hi[0],
                    "recall": rc, "rec_lo": lo[1], "rec_hi": hi[1]}
        print("  %-10s %-9s precision %.3f [%.3f, %.3f]  recall %.3f [%.3f, %.3f]"
              % (lane, lab, pr, lo[0], hi[0], rc, lo[1], hi[1]))
    disc[lane] = out
res["discovery"] = disc

# ---------------- linkage ----------------
print(); print("=" * 72); print("FALSE-LINK RATES (adjudicated, in-frame links)"); print("=" * 72)
link = {}
for t, lane in [("link_av", "robotaxi"), ("link_ped", "pedestrian")]:
    s = codes[codes.task == t]
    no = int(s.adjudicated.eq("NO").sum()); n = int(len(s)); lo, hi = wilson(no, n)
    link[lane] = {"false": no, "n": n, "rate": no / n, "lo": lo, "hi": hi,
                  "unclear": int(s.adjudicated.eq("UNCLEAR").sum())}
    print("  %-10s %d of %d = %.1f%% [%.1f, %.1f]" % (lane, no, n, 100 * no / n, 100 * lo, 100 * hi))
res["linkage"] = link

# ---------------- severity ----------------
print(); print("=" * 72); print("SEVERITY: pipeline label vs adjudicated code (51 in-frame events)"); print("=" * 72)
MAP = {"Property Damage Only": "PDO", "Injury": "INJURY", "Fatal": "FATAL", "Unknown": "UNCLEAR"}
sv = codes[codes.task == "sev"].copy()
sv["plab"] = sv["pipeline_label"].map(lambda v: MAP.get(v, v.upper()))
tab = pd.crosstab(sv["plab"], sv["adjudicated"])
print(tab.to_string())
definite = sv[(sv.adjudicated != "UNCLEAR") & (sv.plab != "UNCLEAR")]
contradicted = int((definite.adjudicated != definite.plab).sum())
conf_inj = set(sv[(sv.plab == "INJURY") & (sv.adjudicated == "INJURY")].source_id)
conf_pdo = set(sv[(sv.plab == "PDO") & (sv.adjudicated == "PDO")].source_id)
res["severity"] = {"table": {r: {c: int(tab.loc[r, c]) for c in tab.columns} for r in tab.index},
                   "definite_both": int(len(definite)), "contradicted": contradicted,
                   "injury_confirmed": len(conf_inj), "injury_total": int((sv.plab == "INJURY").sum()),
                   "pdo_confirmed": len(conf_pdo), "pdo_total": int((sv.plab == "PDO").sum()),
                   "pdo_unclear": int(((sv.plab == "PDO") & (sv.adjudicated == "UNCLEAR")).sum())}
print("  definite on both sides: %d, contradicted: %d; injury confirmed %d of %d; PDO confirmed %d of %d"
      % (len(definite), contradicted, len(conf_inj), res["severity"]["injury_total"],
         len(conf_pdo), res["severity"]["pdo_total"]))

# ---------------- refit on confirmed events ----------------
pooled = load_pooled().copy()
pooled["cell"] = pooled.metro.astype(str) + " | " + pooled.year_bin.astype(str)
g = pooled.groupby("cell").AV.agg(["sum", "count"])
overlap = pooled[pooled.cell.isin(g[(g["sum"] > 0) & (g["sum"] < g["count"])].index)].copy()


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


def design(df):
    d = pd.get_dummies(df.cell.astype(str), prefix="fe", drop_first=True)
    d = d.loc[:, d.values.sum(axis=0) > 0]
    return np.hstack([np.ones((len(df), 1)), df[["T"]].values.astype(float), d.values.astype(float)])


def refit(ids, sev):
    sub = overlap[(overlap.AV == 0) | ((overlap.severity == sev) & overlap.event_id.isin(ids))].copy()
    sub["T"] = (sub.AV == 1).astype(float)
    gg = sub.groupby("cell").T.agg(["sum", "count"])
    sub = sub[sub.cell.isin(gg[(gg["sum"] > 0) & (gg["sum"] < gg["count"])].index)].reset_index(drop=True)
    X = design(sub); y = sub.n_articles.values.astype(float)
    m = sm.GLM(y, X, family=sm.families.Poisson()).fit(cov_type="HC1")
    idx = [np.asarray(v) for v in sub.groupby(["metro", "year_bin", "corpus"]).indices.values()]
    draws = []
    for _ in range(N_BOOT):
        take = np.concatenate([rng.choice(v, len(v)) for v in idx])
        Xb, yb = X[take], y[take]
        keep = Xb.sum(axis=0) != 0; keep[:2] = True
        draws.append(np.exp(irls(Xb[:, keep], yb)[1]))
    return {"af": float(np.exp(m.params[1])), "boot_lo": float(np.percentile(draws, 2.5)),
            "boot_hi": float(np.percentile(draws, 97.5)), "n_treat": int(sub["T"].sum())}


print(); print("=" * 72); print("SEVERITY CONTRASTS ON HUMAN-CONFIRMED EVENTS"); print("=" * 72)
for lab, ids, sev in [("injury_confirmed", conf_inj, "Injury"), ("pdo_confirmed", conf_pdo, "Property Damage Only")]:
    if sev not in set(overlap.severity):
        sev = {"Property Damage Only": "PDO"}.get(sev, sev)
    r = refit(ids, sev)
    res[lab] = r
    print("  %-17s n=%2d  AF = %.2f  bootstrap [%.2f, %.2f]" % (lab, r["n_treat"], r["af"], r["boot_lo"], r["boot_hi"]))

(HERE / "out_validation.json").write_text(json.dumps(res, indent=1, default=float), encoding="utf-8")
print("\nwrote out_validation.json")
