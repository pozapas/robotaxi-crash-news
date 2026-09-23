# -*- coding: utf-8 -*-
"""r09_syndication.py -- near-duplicate clustering and distinct-story models.

"Unique outlet counts do not rule out wire-story syndication." Correct: one
wire story republished by many outlets still counts once per outlet. We now
have article_text for both corpora, so we cluster near-duplicate articles
WITHIN each event and re-estimate the amplification factor with the outcome
redefined as the number of distinct stories rather than distinct articles.

Method. For each article we build a set of word 5-gram hashes over the
normalised body text (a shingle set). Two articles of the same event are the
same story when their Jaccard similarity is at least THRESH. Clusters are the
connected components of that graph. The outcome becomes the cluster count.

Writes rean/out_syndication.json.
"""
from __future__ import annotations
import glob, json, re, hashlib
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm

AV_EXP = Path(r"D:\OneDrive - Texas State University\AIT\n8n Robotaxi Crash News\exports")
PED_EXP = Path(r"D:\OneDrive - Texas State University\AIT\AAA\CrashNews\Data")
DB = Path(r"D:\OneDrive - Texas State University\AIT\Papers\TRB2027\Crash News"
          r"\TRB2027\TRB_R_robotaxi_amplification\data_build")
OUT = Path(__file__).resolve().parent
THRESH = 0.50
K = 5
SEED = 20260921
rng = np.random.default_rng(SEED)

pooled = pd.read_parquet(DB / "pooled.parquet").copy()
pooled["cell"] = pooled.metro.astype(str) + " | " + pooled.year_bin.astype(str)
arts = pd.read_parquet(DB / "articles.parquet").copy()


def load_text(root, pattern):
    fs = glob.glob(str(root / "*" / pattern))
    if not fs:
        return pd.DataFrame(columns=["article_id", "article_text"])
    frames = []
    for f in fs:
        for enc in ("utf-8", "utf-8-sig", "latin-1"):
            try:
                frames.append(pd.read_csv(
                    f, low_memory=False, encoding=enc,
                    encoding_errors="replace" if enc == "utf-8" else "strict",
                    usecols=lambda c: c in ("article_id", "article_text")))
                break
            except (UnicodeDecodeError, ValueError):
                continue
    d = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame(
        columns=["article_id", "article_text"])
    return d.drop_duplicates("article_id")


txt = pd.concat([load_text(AV_EXP, "news_articles_*.csv"),
                 load_text(PED_EXP, "news_articles_*.csv")],
                ignore_index=True).drop_duplicates("article_id")
arts = arts.merge(txt, on="article_id", how="left")
have = arts.article_text.notna() & arts.article_text.astype(str).str.len().ge(400)
print("articles in frame: %d | with usable text: %d (%.1f%%)"
      % (len(arts), int(have.sum()), 100 * have.mean()))
for c in ["AV", "Ped"]:
    s = arts[arts.corpus == c]
    h = s.article_text.notna() & s.article_text.astype(str).str.len().ge(400)
    print("   %-4s %4d articles, %4d with text (%.1f%%)" % (c, len(s), int(h.sum()),
                                                            100 * h.mean()))

BOILER = re.compile(r"(skip to main content|you are the owner of this article|"
                    r"sign up for|subscribe|newsletter|cookie|advertisement|"
                    r"all rights reserved|copyright)", re.I)


def shingles(t):
    t = str(t).lower()
    t = BOILER.sub(" ", t)
    t = re.sub(r"[^a-z0-9 ]+", " ", t)
    w = t.split()
    if len(w) < K + 5:
        return set()
    return {hashlib.blake2b(" ".join(w[i:i + K]).encode(), digest_size=8).digest()
            for i in range(len(w) - K + 1)}


def jac(a, b):
    if not a or not b:
        return 0.0
    inter = len(a & b)
    return inter / (len(a) + len(b) - inter)


def cluster_event(sub):
    """Connected components of the >=THRESH similarity graph. Articles with no
    usable text are each their own cluster, which is the conservative choice
    because it never merges two stories we could not compare."""
    ids = list(sub.article_id)
    sh = {r.article_id: shingles(r.article_text) if isinstance(r.article_text, str)
          else set() for r in sub.itertuples()}
    parent = {i: i for i in ids}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a in range(len(ids)):
        for b in range(a + 1, len(ids)):
            ia, ib = ids[a], ids[b]
            if sh[ia] and sh[ib] and jac(sh[ia], sh[ib]) >= THRESH:
                ra, rb = find(ia), find(ib)
                if ra != rb:
                    parent[ra] = rb
    return len({find(i) for i in ids})


rows = []
for eid, sub in arts.groupby("event_id"):
    rows.append({"event_id": eid, "n_articles": len(sub),
                 "n_stories": cluster_event(sub)})
cl = pd.DataFrame(rows)
p = pooled.merge(cl, on="event_id", how="left", suffixes=("", "_c"))
p["n_stories"] = p.n_stories.fillna(p.n_articles).astype(int)
p["dup_removed"] = p.n_articles - p.n_stories

print("\nnear-duplicate compression by corpus")
summ = {}
for c in ["AV", "Ped"]:
    s = p[p.corpus == c]
    summ[c] = {"articles": int(s.n_articles.sum()), "stories": int(s.n_stories.sum()),
               "pct_duplicate": float(1 - s.n_stories.sum() / s.n_articles.sum()),
               "events_with_any_dup": int((s.dup_removed > 0).sum()),
               "n_events": int(len(s))}
    print("   %-4s %4d articles -> %4d distinct stories (%.1f%% duplicate), "
          "%d/%d events affected"
          % (c, summ[c]["articles"], summ[c]["stories"],
             100 * summ[c]["pct_duplicate"], summ[c]["events_with_any_dup"],
             summ[c]["n_events"]))


# ---- re-estimate the amplification factor with stories as the outcome ----
def overlap(df, treat="AV"):
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


print("\namplification factor, articles vs distinct stories")
res = {"threshold_jaccard": THRESH, "shingle_k": K, "seed": SEED,
       "text_coverage": {"n_articles": int(len(arts)), "n_with_text": int(have.sum())},
       "compression": summ}
for lab, col in [("articles (published)", "n_articles"),
                 ("distinct stories", "n_stories")]:
    r = fit(p, col)
    res[col] = r
    print("   %-22s AF = %.2f  [%.2f, %.2f]" % (lab, r["af"], r["boot_lo"], r["boot_hi"]))

# severity strata on stories
for sev in ["PDO", "Injury"]:
    sub = p[(p.AV == 0) | (p.severity == sev)].copy()
    sub["T"] = ((sub.AV == 1) & (sub.severity == sev)).astype(float)
    r = fit(sub, "n_stories", treat="T", n_boot=1000)
    res["stories_" + sev] = r
    print("   stories, AV %-7s  AF = %.2f  [%.2f, %.2f]  n=%d"
          % (sev, r["af"], r["boot_lo"], r["boot_hi"], r["n_treat"]))

p[["event_id", "corpus", "n_articles", "n_stories", "dup_removed"]].to_csv(
    OUT / "story_clusters.csv", index=False)
(OUT / "out_syndication.json").write_text(json.dumps(res, indent=1), encoding="utf-8")
print("\nwrote out_syndication.json and story_clusters.csv")
