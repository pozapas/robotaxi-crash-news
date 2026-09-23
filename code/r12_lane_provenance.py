# -*- coding: utf-8 -*-
"""r12_lane_provenance.py -- lane provenance and the common-domain-universe
test of lane comparability.

Everything here is derived from the delivered data and the pipeline source.
"""
from __future__ import annotations
import glob, json
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm

AV = Path(r"D:\OneDrive - Texas State University\AIT\n8n Robotaxi Crash News\exports")
PED = Path(r"D:\OneDrive - Texas State University\AIT\AAA\CrashNews\Data")
DB = Path(r"D:\OneDrive - Texas State University\AIT\Papers\TRB2027\Crash News"
          r"\TRB2027\TRB_R_robotaxi_amplification\data_build")
OUT = Path(__file__).resolve().parent
SEED = 20260921
rng = np.random.default_rng(SEED)
COLS = ["article_id", "source_domain", "discovery_source", "search_run_id",
        "llm_model", "relevance_status", "publication_date", "ingested_at"]


def load(root):
    fr = []
    for f in glob.glob(str(root / "*" / "news_articles_*.csv")):
        for enc in ("utf-8", "latin-1"):
            try:
                fr.append(pd.read_csv(f, low_memory=False, encoding=enc,
                                      encoding_errors="replace" if enc == "utf-8" else "strict",
                                      usecols=lambda c: c in COLS))
                break
            except (UnicodeDecodeError, ValueError):
                continue
    return pd.concat(fr, ignore_index=True).drop_duplicates("article_id")


av, pe = load(AV), load(PED)
res = {}
print("=" * 74)
print("LANE PROVENANCE")
print("=" * 74)
for lab, d in [("robotaxi", av), ("pedestrian", pe)]:
    ing = pd.to_datetime(d.get("ingested_at"), errors="coerce", format="mixed", utc=True)
    pub = pd.to_datetime(d.get("publication_date"), errors="coerce", format="mixed", utc=True)
    rec = {
        "n_articles": int(len(d)),
        "discovery_source": d.discovery_source.dropna().unique().tolist()[:4]
        if "discovery_source" in d else [],
        "llm_models": d.llm_model.dropna().value_counts().head(3).to_dict()
        if "llm_model" in d else {},
        "n_search_runs": int(d.search_run_id.nunique()) if "search_run_id" in d else None,
        "ingest_first": str(ing.min().date()) if ing.notna().any() else None,
        "ingest_last": str(ing.max().date()) if ing.notna().any() else None,
        "pub_first": str(pub.min().date()) if pub.notna().any() else None,
        "pub_last": str(pub.max().date()) if pub.notna().any() else None,
        "n_domains": int(d.source_domain.nunique()),
    }
    if pub.notna().any():
        per_month = pub.dt.to_period("M").value_counts()
        rec["max_articles_in_one_month"] = int(per_month.max())
    res[lab] = rec
    print("\n  %s" % lab.upper())
    for k, v in rec.items():
        print("    %-26s %s" % (k, v))

print("\n  BigQuery row cap PFC_MAX_ARTICLES_PER_RUN = 9200 per monthly window")
print("    robotaxi busiest month held %d articles, so the cap did not bind"
      % res["robotaxi"]["max_articles_in_one_month"])

# ===================== #1 COMMON DOMAIN UNIVERSE =========================
print()
print("=" * 74)
print("LANE COMPARABILITY ON A COMMON DOMAIN UNIVERSE")
print("=" * 74)


def dom(s):
    return s.astype(str).str.lower().str.strip()


av_dom = set(dom(av.source_domain).dropna()) - {"", "nan"}
pe_dom = set(dom(pe.source_domain).dropna()) - {"", "nan"}
both = av_dom & pe_dom
print("  domains reached by the robotaxi lane   : %d" % len(av_dom))
print("  domains reached by the pedestrian lane : %d" % len(pe_dom))
print("  reached by BOTH                        : %d" % len(both))

pooled = pd.read_parquet(DB / "pooled.parquet").copy()
pooled["cell"] = pooled.metro.astype(str) + " | " + pooled.year_bin.astype(str)
arts = pd.read_parquet(DB / "articles.parquet").copy()
arts["dom"] = dom(arts.source_domain)
arts["in_both"] = arts.dom.isin(both)
print()
for c in ["AV", "Ped"]:
    s = arts[arts.corpus == c]
    print("  %-4s frame articles %4d, of which on a shared domain %4d (%.1f%%)"
          % (c, len(s), int(s.in_both.sum()), 100 * s.in_both.mean()))

shared = arts[arts.in_both].groupby("event_id").size().rename("n_shared")
p = pooled.merge(shared, on="event_id", how="left")
p["n_shared"] = p.n_shared.fillna(0).astype(int)


def overlap(df, treat):
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
        Hm = (X * mu[:, None]).T @ X
        try:
            step = np.linalg.solve(Hm + 1e-10 * np.eye(len(b)), X.T @ (y - mu))
        except np.linalg.LinAlgError:
            step = np.linalg.lstsq(Hm, X.T @ (y - mu), rcond=None)[0]
        b += step
        if np.max(np.abs(step)) < tol:
            break
    return b


def fit(df, outcome, treat="AV", n_boot=2000):
    d = overlap(df, treat)
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
    return {"af": float(np.exp(m.params[i])),
            "boot_lo": float(np.percentile(draws, 2.5)),
            "boot_hi": float(np.percentile(draws, 97.5)),
            "n_treat": int(d[treat].sum()), "n_total": int(len(d))}


print()
r_all = fit(p, "n_articles")
r_sh = fit(p, "n_shared")
print("  all articles                    AF = %.2f [%.2f, %.2f]"
      % (r_all["af"], r_all["boot_lo"], r_all["boot_hi"]))
print("  common-domain articles only     AF = %.2f [%.2f, %.2f]"
      % (r_sh["af"], r_sh["boot_lo"], r_sh["boot_hi"]))

sev = {}
for s in ["PDO", "Injury"]:
    sub = p[(p.AV == 0) | (p.severity == s)].copy()
    sub["T"] = ((sub.AV == 1) & (sub.severity == s)).astype(float)
    e = fit(sub, "n_shared", treat="T", n_boot=1000)
    sev[s] = e
    print("  common-domain, AV %-7s      AF = %.2f [%.2f, %.2f] (n=%d)"
          % (s, e["af"], e["boot_lo"], e["boot_hi"], e["n_treat"]))

res["common_domain"] = {
    "n_domains_av": len(av_dom), "n_domains_ped": len(pe_dom), "n_shared": len(both),
    "share_av_on_shared": float(arts[arts.corpus == "AV"].in_both.mean()),
    "share_ped_on_shared": float(arts[arts.corpus == "Ped"].in_both.mean()),
    "af_all": r_all, "af_shared": r_sh, "af_shared_by_severity": sev}
(OUT / "out_provenance.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
print("\nwrote out_provenance.json")
