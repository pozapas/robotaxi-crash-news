# -*- coding: utf-8 -*-
"""r08_rest.py -- local-outlet models, equal-follow-up timing and outlet
composition.

#2  local-outlet test without selecting on the filtered outcome: PPML on the
    local-article count over ALL overlap events (zeros retained), plus a
    two-part decomposition into local-coverage incidence and positive intensity.
#5  timing without imposing decay from day zero: peak-aligned fit, plus
    nonparametric timing summaries.
#6  equal follow-up window for both corpora; event-weighted as well as
    article-weighted tail shares, with event-cluster bootstrap.
#15 outlet-composition measure reported event-weighted AND article-weighted.
#24 explicit denominators and exclusions behind every percentage.

Writes rean/out_rest.json.
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
rng = np.random.default_rng(SEED)

pooled = pd.read_parquet(DB / "pooled.parquet").copy()
arts = pd.read_parquet(DB / "articles.parquet").copy()
nat = pd.read_csv(DB / "national_domains.csv")
natset = set(nat.domain.astype(str).str.lower().str.strip())

pooled["cell"] = pooled.metro.astype(str) + " | " + pooled.year_bin.astype(str)
g = pooled.groupby("cell").AV.agg(["sum", "count"])
both = g[(g["sum"] > 0) & (g["sum"] < g["count"])].index
overlap = pooled[pooled.cell.isin(both)].copy()

arts["dom"] = arts.source_domain.astype(str).str.lower().str.strip()
arts["is_nat"] = arts.dom.isin(natset)
res = {"seed": SEED}


def design(df, treat, fe="cell"):
    parts = [np.ones((len(df), 1))]
    names = ["const"]
    parts.append(df[[treat]].values.astype(float))
    names.append(treat)
    d = pd.get_dummies(df[fe].astype(str), prefix="fe", drop_first=True)
    d = d.loc[:, d.values.sum(axis=0) > 0]
    parts.append(d.values.astype(float))
    names += list(d.columns)
    return np.hstack(parts), names


def ppml(df, outcome, treat="AV", fe="cell"):
    X, names = design(df, treat, fe)
    y = df[outcome].values.astype(float)
    m = sm.GLM(y, X, family=sm.families.Poisson()).fit(cov_type="HC1")
    i = names.index(treat)
    return {"ratio": float(np.exp(m.params[i])),
            "lo": float(np.exp(m.params[i] - 1.96 * m.bse[i])),
            "hi": float(np.exp(m.params[i] + 1.96 * m.bse[i]))}


# ===================== #2  LOCAL OUTLETS, ZEROS RETAINED =================
print("=" * 72)
print("local-outlet test retaining every event (zeros kept)")
print("=" * 72)
loc = arts[~arts.is_nat].groupby("event_id").size().rename("n_local")
ov = overlap.merge(loc, on="event_id", how="left")
ov["n_local"] = ov.n_local.fillna(0).astype(int)
ov["any_local"] = (ov.n_local > 0).astype(int)

print(f"  overlap events: {len(ov)}  (AV {int(ov.AV.sum())}, human {int((1-ov.AV).sum())})")
for c, lab in [(1, "AV"), (0, "human")]:
    s = ov[ov.AV == c]
    print(f"    {lab:6s} zero-local: {int((s.n_local==0).sum()):3d}/{len(s):3d} "
          f"({100*(s.n_local==0).mean():.1f}%)")

full_local = ppml(ov, "n_local")
print(f"  PPML on local count, ALL events   ratio = {full_local['ratio']:.2f} "
      f"[{full_local['lo']:.2f}, {full_local['hi']:.2f}]   <-- primary local test")

# two-part decomposition
Xi, ni = design(ov, "AV")
mi = sm.GLM(ov.any_local.values.astype(float), Xi,
            family=sm.families.Binomial()).fit(cov_type="HC1")
ii = ni.index("AV")
odds = float(np.exp(mi.params[ii]))
pos = ov[ov.n_local > 0].copy()
gg = pos.groupby("cell").AV.agg(["sum", "count"])
kp = gg[(gg["sum"] > 0) & (gg["sum"] < gg["count"])].index
pos_k = pos[pos.cell.isin(kp)]
int_pos = ppml(pos_k, "n_local")
print(f"  part 1 incidence  odds ratio of any local article = {odds:.2f}")
print(f"  part 2 intensity  ratio among events with local coverage = "
      f"{int_pos['ratio']:.2f} [{int_pos['lo']:.2f}, {int_pos['hi']:.2f}] (n={len(pos_k)})")
res["local"] = {"primary_all_events": full_local, "incidence_or": odds,
                "positive_intensity": int_pos,
                "n_events": int(len(ov)), "n_av": int(ov.AV.sum()),
                "zero_local_av": int((ov[ov.AV == 1].n_local == 0).sum()),
                "zero_local_hu": int((ov[ov.AV == 0].n_local == 0).sum()),
                "n_positive": int(len(pos_k))}

# severity-resolved local test, zeros retained
sev_loc = {}
for sev in ["PDO", "Injury"]:
    sub = ov[(ov.AV == 0) | (ov.severity == sev)].copy()
    sub["T"] = ((sub.AV == 1) & (sub.severity == sev)).astype(float)
    gg = sub.groupby("cell").T.agg(["sum", "count"])
    k = gg[(gg["sum"] > 0) & (gg["sum"] < gg["count"])].index
    sub = sub[sub.cell.isin(k)]
    e = ppml(sub, "n_local", treat="T")
    sev_loc[sev] = dict(e, n_treat=int(sub["T"].sum()))
    print(f"    local, AV {sev:7s} n={int(sub['T'].sum()):3d} ratio = {e['ratio']:.2f} "
          f"[{e['lo']:.2f}, {e['hi']:.2f}]")
res["local"]["by_severity"] = sev_loc

# ===================== #6  EQUAL FOLLOW-UP ===============================
print()
print("=" * 72)
print("equal follow-up window")
print("=" * 72)
cutoff = min(arts[arts.corpus == "AV"].pub.max(), arts[arts.corpus == "Ped"].pub.max())
print(f"  common article-observation cutoff: {cutoff.date()}")
ev = pooled[["event_id", "corpus", "event_date", "n_articles"]].copy()
ev["followup_days"] = (cutoff - ev.event_date).dt.days
W = 180
elig = ev[ev.followup_days >= W]
print(f"  events with >= {W} days follow-up: "
      + ", ".join(f"{c} {int((elig.corpus==c).sum())}/{int((ev.corpus==c).sum())}"
                  for c in ["AV", "Ped"]))
a = arts.merge(ev[["event_id", "followup_days"]], on="event_id", how="left")
a_ok = a[(a.lag_days >= -1) & (a.event_id.isin(set(elig.event_id))) & (a.lag_days <= W)]
print(f"  articles retained in equal-window analysis: {len(a_ok)} "
      + ", ".join(f"{c} {int((a_ok.corpus==c).sum())}" for c in ["AV", "Ped"]))

res["followup"] = {"cutoff": str(cutoff.date()), "window_days": W,
                   "n_events_eligible": {c: int((elig.corpus == c).sum()) for c in ["AV", "Ped"]},
                   "n_events_total": {c: int((ev.corpus == c).sum()) for c in ["AV", "Ped"]},
                   "n_articles": {c: int((a_ok.corpus == c).sum()) for c in ["AV", "Ped"]}}

# ---- article-weighted vs event-weighted tail share ----
print()
print("  tail share beyond day 14, equal window:")
tail = {}
for c in ["AV", "Ped"]:
    s = a_ok[a_ok.corpus == c]
    aw = float((s.lag_days > 14).mean())
    per = s.groupby("event_id").apply(lambda g: (g.lag_days > 14).mean(),
                                      include_groups=False)
    ew_mean = float(per.mean())
    ew_med = float(per.median())
    # event-cluster bootstrap on the event-weighted mean
    ids = per.index.values
    draws = [per.loc[rng.choice(ids, len(ids), replace=True)].mean() for _ in range(2000)]
    tail[c] = {"article_weighted": aw, "event_weighted_mean": ew_mean,
               "event_weighted_median": ew_med,
               "ew_lo": float(np.percentile(draws, 2.5)),
               "ew_hi": float(np.percentile(draws, 97.5)),
               "n_events": int(len(per))}
    print(f"    {c:4s} article-weighted {aw:.3f} | event-weighted mean {ew_mean:.3f} "
          f"[{tail[c]['ew_lo']:.3f}, {tail[c]['ew_hi']:.3f}] | median {ew_med:.3f}")
res["tail"] = tail

# ===================== #5  TIMING WITHOUT IMPOSED DECAY ==================
print()
print("=" * 72)
print("daily profile and peak-aligned decay")
print("=" * 72)
prof = {}
for c in ["AV", "Ped"]:
    s = a_ok[(a_ok.corpus == c) & (a_ok.lag_days >= 0)]
    daily = s.groupby("lag_days").size().reindex(range(0, 15), fill_value=0)
    peak = int(daily.idxmax())
    prof[c] = {"daily_0_14": [int(x) for x in daily.values], "peak_day": peak}
    print(f"    {c:4s} days 0-14 counts: {list(daily.values)}  peak day {peak}")

# peak-aligned exponential, fitted from each corpus's own peak to day 14,
# with event-cluster bootstrap for the half-life
def halflife_from_peak(sub, peak):
    d = sub[(sub.lag_days >= peak) & (sub.lag_days <= 14)]
    cnt = d.groupby("lag_days").size().reindex(range(peak, 15), fill_value=0)
    t = np.arange(len(cnt), dtype=float)
    y = cnt.values.astype(float)
    X = sm.add_constant(t)
    m = sm.GLM(y, X, family=sm.families.Poisson()).fit()
    lam = -float(m.params[1])
    return (np.log(2) / lam) if lam > 0 else np.nan

hl = {}
for c in ["AV", "Ped"]:
    s = a_ok[(a_ok.corpus == c) & (a_ok.lag_days >= 0)]
    pk = prof[c]["peak_day"]
    point = halflife_from_peak(s, pk)
    ids = s.event_id.unique()
    draws = []
    for _ in range(1000):
        pick = rng.choice(ids, len(ids), replace=True)
        bs = pd.concat([s[s.event_id == i] for i in pick])
        v = halflife_from_peak(bs, pk)
        if np.isfinite(v):
            draws.append(v)
    hl[c] = {"peak_day": pk, "half_life": float(point),
             "lo": float(np.percentile(draws, 2.5)),
             "hi": float(np.percentile(draws, 97.5)),
             "n_boot_ok": len(draws)}
    print(f"    {c:4s} peak-aligned half-life = {point:.2f} d "
          f"[{hl[c]['lo']:.2f}, {hl[c]['hi']:.2f}] (event-cluster bootstrap)")
res["halflife_peak"] = hl
res["daily_profile"] = prof

# nonparametric timing summaries (no model at all)
np_tim = {}
for c in ["AV", "Ped"]:
    s = a_ok[(a_ok.corpus == c) & (a_ok.lag_days >= 0)]
    per = s.groupby("event_id").lag_days.median()
    np_tim[c] = {"median_lag_article_weighted": float(s.lag_days.median()),
                 "median_of_event_medians": float(per.median()),
                 "p75_article": float(s.lag_days.quantile(.75)),
                 "p90_article": float(s.lag_days.quantile(.90))}
    print(f"    {c:4s} median lag {np_tim[c]['median_lag_article_weighted']:.0f} d "
          f"| median of event medians {np_tim[c]['median_of_event_medians']:.0f} d "
          f"| p75 {np_tim[c]['p75_article']:.0f} | p90 {np_tim[c]['p90_article']:.0f}")
res["timing_nonparametric"] = np_tim

# ===================== #15 OUTLET COMPOSITION ============================
print()
print("=" * 72)
print("outlet composition, event-weighted vs article-weighted")
print("=" * 72)
comp = {}
am = arts[arts.event_id.isin(set(pooled.event_id))]
for c in ["AV", "Ped"]:
    s = am[am.corpus == c]
    aw = float(s.is_nat.mean())
    per = s.groupby("event_id").is_nat.mean()
    ids = per.index.values
    draws = [per.loc[rng.choice(ids, len(ids), replace=True)].mean() for _ in range(2000)]
    comp[c] = {"article_weighted_share": aw,
               "event_weighted_mean": float(per.mean()),
               "ew_lo": float(np.percentile(draws, 2.5)),
               "ew_hi": float(np.percentile(draws, 97.5)),
               "n_articles": int(len(s)), "n_events": int(len(per))}
    print(f"    {c:4s} article-weighted {100*aw:.1f}%  |  event-weighted mean "
          f"{100*per.mean():.1f}% [{100*comp[c]['ew_lo']:.1f}, {100*comp[c]['ew_hi']:.1f}]")
res["composition"] = comp

(OUT / "out_rest.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
print("\nwrote out_rest.json")
