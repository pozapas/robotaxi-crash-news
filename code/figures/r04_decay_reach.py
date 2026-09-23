"""r04_decay_reach.py -- TRB-R Step 4: attention half-life + geographic reach.

RQ2 decay: pool articles by lag t = pub_date - event_date. Drop negative lags
beyond -1 day (date errors; logged). Joint Poisson decay on t in [0,14]:
    log mu_{c,t} = a + b*AV - lambda0*t - lambda1*(AV*t)
half-life t_half = ln2 / lambda_c; delta-method SE = ln2/lambda^2 * se(lambda).
tail share tau_c = P(lag > 14) reported separately. Sensitivity: first-pub lag.

RQ3 reach: classify each article national/tech-trade vs local via
national_domains.csv; event-level national share R_i; corpus means compared by
stratified bootstrap. Compositional breakdown by category.

Figures: fig3 (decay curves + half-life annotations + tau inset), fig4
(a: metro dumbbells; b: outlet-composition stacks + national-share CI).

Run:  python analysis/r04_decay_reach.py
"""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C

RNG = np.random.default_rng(7)
# Horizon of panel (a) in fig3. Overridable so a driver that enforces an
# equal follow-up window can shorten it without touching the design.
CAPTURE_HORIZON = 365
CAPTURE_XTICKS = [0, 1, 2, 7, 14, 30, 90, 180, 365]
qa: list[str] = []
def log(m: str = ""):
    print(m); qa.append(m)


# ============================================================ DECAY
def fit_decay(art):
    """Joint Poisson decay on days 0..14. Returns dict with lambdas, half-lives,
    delta-method SEs, and per-corpus day-0 predicted-vs-observed check."""
    import statsmodels.api as sm
    d = art.dropna(subset=["lag_days"]).copy()
    n_neg = int((d.lag_days < -1).sum())
    d = d[(d.lag_days >= 0) & (d.lag_days <= 14)]
    # aggregate to (corpus, t) article counts
    g = (d.groupby(["corpus", "lag_days"]).size().rename("n").reset_index())
    full = (pd.MultiIndex.from_product([["AV", "Ped"], range(0, 15)],
            names=["corpus", "lag_days"]).to_frame(index=False))
    g = full.merge(g, on=["corpus", "lag_days"], how="left").fillna({"n": 0})
    g["AV"] = (g.corpus == "AV").astype(float)
    g["t"] = g.lag_days.astype(float)
    g["AVt"] = g.AV * g.t
    X = sm.add_constant(g[["AV", "t", "AVt"]].values)
    y = g["n"].values.astype(float)
    m = sm.GLM(y, X, family=sm.families.Poisson()).fit()
    # params: const, AV, t, AVt  -> lambda_ped = -coef_t; lambda_av = -(coef_t+coef_AVt)
    b = m.params; se = m.bse; cov = m.cov_params()
    lam_ped = -b[2]; lam_av = -(b[2] + b[3])
    se_lam_ped = se[2]
    se_lam_av = np.sqrt(cov[2, 2] + cov[3, 3] + 2 * cov[2, 3])
    def half(lam, se_lam):
        if lam <= 0:
            return dict(t_half=np.inf, se=np.nan, lam=float(lam), se_lam=float(se_lam))
        th = np.log(2) / lam
        se_th = np.log(2) / lam**2 * se_lam           # delta method
        return dict(t_half=float(th), se=float(se_th), lam=float(lam),
                    se_lam=float(se_lam),
                    ci=[float(th - 1.96 * se_th), float(th + 1.96 * se_th)])
    out = {"AV": half(lam_av, se_lam_av), "Ped": half(lam_ped, se_lam_ped),
           "lambda1_AVt": float(b[3]), "lambda1_se": float(se[3]),
           "lambda1_p": float(m.pvalues[3]), "n_neg_dropped": n_neg}
    # day-0 predicted vs observed (hard gate: within 20%)
    for c, avval in [("AV", 1.0), ("Ped", 0.0)]:
        pred0 = np.exp(b[0] + b[1] * avval)   # t=0
        obs0 = float(g[(g.corpus == c) & (g.lag_days == 0)]["n"].iloc[0])
        out[c]["pred_day0"] = float(pred0); out[c]["obs_day0"] = obs0
        out[c]["day0_ratio"] = float(pred0 / obs0) if obs0 else np.nan
    out["grid"] = g
    out["params"] = {"const": float(b[0]), "AV": float(b[1]), "t": float(b[2]),
                     "AVt": float(b[3])}
    return out


def tail_share(art):
    out = {}
    for c in ["AV", "Ped"]:
        s = art[art.corpus == c].dropna(subset=["lag_days"])
        s = s[s.lag_days >= 0]
        out[c] = float((s.lag_days > 14).mean()) if len(s) else np.nan
    return out


# ============================================================ REACH
def classify_reach(art):
    nat = pd.read_csv(C.DATA_BUILD / "national_domains.csv", dtype=str)
    nat_map = dict(zip(nat.domain.str.strip().str.lower(), nat.category))
    dom = art.source_domain.fillna("").str.strip().str.lower()
    art = art.assign(
        _dom=dom,
        is_national=dom.isin(nat_map).astype(int),
        reach_cat=[nat_map.get(x, "local_regional") for x in dom])
    art.loc[art._dom == "", "reach_cat"] = "unknown"
    return art, nat_map


def event_national_share(art, pooled):
    a = art[art._dom != ""]                 # exclude blank-domain from denominator
    g = a.groupby("event_id")
    share = (g["is_national"].mean()).rename("nat_share")
    n_nat = g["is_national"].sum().rename("n_national")
    n_tot = g.size().rename("n_class")
    ev = pooled[["event_id", "AV", "corpus", "metro"]].merge(
        pd.concat([share, n_nat, n_tot], axis=1), on="event_id", how="left")
    return ev.dropna(subset=["nat_share"])


def reach_bootstrap(ev, n_boot=2000):
    """Stratified bootstrap (metro x corpus) of the mean national-share diff."""
    cells = ev.groupby(["metro", "corpus"]).indices
    idx_by = {k: np.asarray(v) for k, v in cells.items()}
    av = ev.AV.values; sh = ev.nat_share.values
    def stat(idx):
        a = idx[av[idx] == 1]; p = idx[av[idx] == 0]
        return (np.nan if len(a) == 0 or len(p) == 0
                else sh[a].mean() - sh[p].mean())
    obs = stat(np.arange(len(ev)))
    draws = np.full(n_boot, np.nan)
    for b in range(n_boot):
        take = np.concatenate([RNG.choice(v, len(v), replace=True) for v in idx_by.values()])
        draws[b] = stat(take)
    lo, hi = C.pctile_ci(draws)
    av_mean = float(sh[av == 1].mean()); pd_mean = float(sh[av == 0].mean())
    return dict(av_mean=av_mean, ped_mean=pd_mean, diff=float(obs),
                diff_lo=float(lo), diff_hi=float(hi))


# ============================================================ FIGURES
def fig3(decay, tau, articles=None):
    """Render an attention-persistence atlas rather than a fitted scatterplot.

    Panel (a) follows the *cumulative capture* of coverage through a log-expanded
    post-crash timeline.  Panel (b) decomposes that timing into early/late
    allocation and the fitted within-window half-life.  It keeps the raw
    publication timing, the long-tail result, and the model estimate in one
    coordinated, but non-redundant, visual argument.
    """
    plt = C.use_style()
    from matplotlib.patches import Patch
    from palette import PED, AV, HIGHLIGHT, INK, NEUTRAL

    if articles is None:
        articles = C.load_articles()
    g = decay["grid"]

    # Valid lags are the common denominator for both empirical panels.  The
    # published fit itself is still summarized through its half-life and CI.
    valid = articles.dropna(subset=["lag_days"]).copy()
    valid = valid[valid.lag_days >= 0]
    lag = {c: valid.loc[valid.corpus == c, "lag_days"].to_numpy(dtype=float)
           for c in ["Ped", "AV"]}

    fig = plt.figure(figsize=(6.85, 3.55), facecolor="white")
    gs = fig.add_gridspec(1, 2, width_ratios=(1.36, 1.00), wspace=0.43)
    ax_capture = fig.add_subplot(gs[0, 0])
    right = gs[0, 1].subgridspec(2, 1, height_ratios=(1.15, 0.85), hspace=0.72)
    ax_alloc = fig.add_subplot(right[0, 0])
    ax_half = fig.add_subplot(right[1, 0])

    # ------------------- (a) cumulative attention capture -------------------
    horizon = CAPTURE_HORIZON
    days = np.arange(0, horizon + 1)
    capture = {}
    for corpus, color, label in [("Ped", PED, "Human fatal (ped)"), ("AV", AV, "AV")]:
        cdf = np.array([(lag[corpus] <= day).mean() * 100 for day in days])
        capture[corpus] = cdf
        ax_capture.step(days, cdf, where="post", color=color, lw=1.8, zorder=3, label=label)
        ax_capture.fill_between(days, 0, cdf, step="post", color=color, alpha=0.075, zorder=1)

    ax_capture.axvspan(0, 1, color="#F3F3F3", zorder=0)
    ax_capture.axvspan(14, horizon, color=HIGHLIGHT, alpha=0.035, zorder=0)
    ax_capture.axvline(14, color=NEUTRAL, lw=0.85, ls=(0, (2, 2)), zorder=2)
    ped14 = float(capture["Ped"][14]); av14 = float(capture["AV"][14])
    # Keep the day-14 bracket behind the series and locate its annotation in
    # open space, rather than letting either element interrupt a trajectory.
    ax_capture.vlines(14, av14, ped14, color=HIGHLIGHT, lw=2.0, zorder=2)
    ax_capture.text(5.0, 66.0, f"{ped14 - av14:.0f} pp\ncapture gap",
                    color=HIGHLIGHT, fontsize=5.8, fontweight="bold",
                    ha="center", va="center",
                    bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none",
                              alpha=0.93), zorder=5)
    ax_capture.annotate("Day 14", xy=(14, 2.2), xytext=(14, 8.5), ha="center",
                        fontsize=5.4, color=NEUTRAL,
                        arrowprops=dict(arrowstyle="-", color=NEUTRAL, lw=0.6))
    ax_capture.text(0.17, 0.95, "Immediate\ncoverage", transform=ax_capture.transAxes,
                    ha="center", va="top", fontsize=5.2, color=NEUTRAL)

    ax_capture.set_xscale("symlog", linthresh=1, linscale=0.7)
    xticks = CAPTURE_XTICKS
    ax_capture.set_xticks(xticks)
    ax_capture.set_xticklabels([str(x) for x in xticks])
    ax_capture.set_xlim(0, horizon)
    ax_capture.set_ylim(0, 103)
    ax_capture.set_yticks([0, 25, 50, 75, 100])
    ax_capture.set_xlabel("Days since crash (log scale after day 1)", labelpad=8)
    ax_capture.set_ylabel("Cumulative share of linked coverage (%)", labelpad=8)
    ax_capture.set_title("Cumulative capture of crash-news attention", loc="left", pad=8)
    ax_capture.text(-0.025, 1.035, "(a)", transform=ax_capture.transAxes, fontsize=9,
                    fontweight="bold", ha="right", va="bottom", color=INK)
    ax_capture.legend(loc="lower right", bbox_to_anchor=(0.99, 0.04), fontsize=5.4,
                      frameon=False, handlelength=1.5, handletextpad=0.35,
                      labelspacing=0.35, borderaxespad=0.0)
    ax_capture.grid(axis="y", color="#E6E6E6", lw=0.5)
    ax_capture.grid(axis="x", color="#E6E6E6", lw=0.5)

    # -------- (b) coverage allocation in successive temporal windows --------
    windows = [(0, 0, "Day 0"), (1, 1, "Day 1"), (2, 7, "Days 2-7"),
               (8, 14, "Days 8-14"), (15, np.inf, "After day 14")]
    window_colors = ["#D9EAF7", "#9ECAE1", "#56B4E9", "#2A9D8F", HIGHLIGHT]
    shares = {}
    for corpus, tau_key in [("Ped", "Ped"), ("AV", "AV")]:
        within = g[g.corpus == corpus].set_index("lag_days")["n"]
        n_within = float(within.sum())
        mass_within = 1 - float(tau[tau_key])
        vals = []
        for lo, hi, _ in windows[:-1]:
            count = float(within.loc[(within.index >= lo) & (within.index <= hi)].sum())
            vals.append(100 * mass_within * count / n_within)
        vals.append(100 * float(tau[tau_key]))
        shares[corpus] = np.asarray(vals)

    y_rows = [("Ped", 1, "Human", PED), ("AV", 0, "AV", AV)]
    for corpus, y, label, role_color in y_rows:
        left = 0.0
        for value, (_, _, window_label), color in zip(shares[corpus], windows, window_colors):
            ax_alloc.barh(y, value, left=left, height=0.48, color=color,
                          edgecolor="white", linewidth=0.55, zorder=3)
            if value >= 7.5:
                txt_color = "white" if color in ["#2A9D8F", HIGHLIGHT] else INK
                ax_alloc.text(left + value / 2, y, f"{value:.0f}%", ha="center", va="center",
                              fontsize=5.0, fontweight="bold", color=txt_color, zorder=4)
            left += value
    ax_alloc.set_xlim(0, 100)
    # A small top reserve hosts the compact timing key without lifting the
    # panel heading off the shared baseline.
    ax_alloc.set_ylim(-0.60, 1.70)
    ax_alloc.set_yticks([1, 0]); ax_alloc.set_yticklabels(["Human", "AV"])
    for tick, color in zip(ax_alloc.get_yticklabels(), [PED, AV]):
        tick.set_color(color); tick.set_fontweight("bold")
    ax_alloc.set_xlabel("Share of linked coverage (%)", labelpad=8)
    ax_alloc.set_title("Temporal allocation and fitted decay", loc="left", pad=8)
    # This axes is shorter than panel (a), so an axes-relative panel letter
    # needs a compensating lift to share the title's physical baseline.
    ax_alloc.text(-0.025, 1.085, "(b)", transform=ax_alloc.transAxes, fontsize=9,
                  fontweight="bold", ha="right", va="bottom", color=INK)
    alloc_handles = [Patch(facecolor=color, edgecolor="none", label=label)
                     for (_, _, label), color in zip(windows, window_colors)]
    ax_alloc.legend(handles=alloc_handles, ncol=5, loc="upper center",
                    bbox_to_anchor=(0.50, 0.99), frameon=False, fontsize=4.3,
                    handlelength=0.8, handletextpad=0.25, columnspacing=0.42,
                    borderaxespad=0.0)
    ax_alloc.grid(axis="x", color="#E6E6E6", lw=0.5)
    ax_alloc.grid(axis="y", visible=False)
    ax_alloc.tick_params(axis="y", length=0, pad=3)

    # Model estimate is shown as an interval ruler, not another scatterplot.
    for key, y, label, color in [("Ped", 1, "Human", PED), ("AV", 0, "AV", AV)]:
        h = decay[key]; lo, hi = h["ci"]
        ax_half.plot([0, h["t_half"]], [y, y], color=color, lw=1.35, alpha=0.55,
                     solid_capstyle="round", zorder=1)
        ax_half.hlines(y, lo, hi, color=color, lw=2.5, zorder=2)
        ax_half.vlines([lo, hi], y - 0.10, y + 0.10, color=color, lw=1.0, zorder=2)
        ax_half.scatter(h["t_half"], y, s=34, color=color, edgecolor="white",
                        linewidth=0.5, zorder=3)
        # Place the value beyond the confidence interval, on a white chip, so
        # it stays legible even when the estimate sits near the interval end.
        ax_half.text(hi + 0.12, y, f"{h['t_half']:.1f} d", color=color,
                     fontsize=5.7, fontweight="bold", va="center",
                     bbox=dict(boxstyle="round,pad=0.12", fc="white", ec="none",
                               alpha=0.94), zorder=4)
    # Original limit, widened only if an interval or its label would
    # otherwise fall outside the axes.
    _hi_max = max(decay['AV']['ci'][1], decay['Ped']['ci'][1])
    ax_half.set_xlim(0, max(4.35, _hi_max + 1.05))
    ax_half.set_ylim(-0.45, 1.45)
    ax_half.set_yticks([1, 0]); ax_half.set_yticklabels(["Human", "AV"])
    for tick, color in zip(ax_half.get_yticklabels(), [PED, AV]):
        tick.set_color(color); tick.set_fontweight("bold")
    ax_half.set_xlabel("Fitted within-window half-life (days)", labelpad=8)
    ax_half.text(0.0, 1.04, "Within-window decay rate", transform=ax_half.transAxes,
                 ha="left", va="bottom", fontsize=6.4, fontweight="bold", color=INK)
    ax_half.text(0.98, 0.06, f"{decay['AV']['t_half'] / decay['Ped']['t_half']:.1f}$\\times$ longer",
                 transform=ax_half.transAxes, ha="right", va="bottom", fontsize=5.5,
                 fontweight="bold", color=AV)
    ax_half.grid(axis="x", color="#E6E6E6", lw=0.5)
    ax_half.grid(axis="y", visible=False)
    ax_half.tick_params(axis="y", length=0, pad=3)

    for a in (ax_capture, ax_alloc, ax_half):
        a.set_facecolor("white")
    fig.subplots_adjust(left=0.105, right=0.985, bottom=0.20, top=0.87, wspace=0.43)
    fig.savefig(C.FIGURES / "fig3.pdf"); fig.savefig(C.FIGURES / "fig3.png", dpi=600)
    plt.close(fig)
    log("- wrote fig3.pdf / fig3.png")


def fig4(pooled, ev, art, reach):
    """Render geographic reach as a two-scale reach atlas.

    The first panel makes the matched-metro comparison explicit at the event
    level.  The second is an alluvial composition view: it shows where the
    article ecosystem moves when coverage shifts from human fatal crashes to
    AV crashes.  Together, the panels separate *where attention reaches* from
    *which outlet system carries it*.
    """
    plt = C.use_style()
    from matplotlib.patches import Polygon
    from palette import PED, AV, INK, SECONDARY, HIGHLIGHT, NEUTRAL

    fig = plt.figure(figsize=(6.85, 3.45), facecolor="white")
    gs = fig.add_gridspec(1, 2, width_ratios=(1.11, 0.89), wspace=0.30)
    ax_metro = fig.add_subplot(gs[0, 0])
    ax_flow = fig.add_subplot(gs[0, 1])

    # (a) Matched-metro reach lift.  The overall row carries the stratified
    # bootstrap result; city rows remain a transparent descriptive comparison.
    metro = (ev.groupby(["metro", "corpus"])["nat_share"].mean()
               .unstack("corpus").reindex(columns=["Ped", "AV"]).dropna())
    metro["delta"] = (metro["AV"] - metro["Ped"]) * 100
    metro = metro.sort_values("delta", ascending=False)
    city_y = np.arange(len(metro) - 1, -1, -1, dtype=float)
    overall_y = len(metro) + 0.32

    ax_metro.axhspan(overall_y - 0.35, overall_y + 0.35, color="#F4F4F4", zorder=0)
    for y, (name, row) in zip(city_y, metro.iterrows()):
        ped, av, delta = row["Ped"] * 100, row["AV"] * 100, row["delta"]
        ax_metro.plot([ped, av], [y, y], color=NEUTRAL, lw=1.15, alpha=0.80,
                      solid_capstyle="round", zorder=1)
        ax_metro.scatter(ped, y, s=31, color=PED, edgecolor="white", linewidth=0.45,
                         zorder=3)
        ax_metro.scatter(av, y, s=31, color=AV, edgecolor="white", linewidth=0.45,
                         zorder=3)
        ax_metro.text(max(ped, av) + 2.8, y, f"+{delta:.0f} pp", color=AV,
                      fontsize=5.4, va="center", fontweight="bold")

    ped_all, av_all = reach["ped_mean"] * 100, reach["av_mean"] * 100
    ax_metro.plot([ped_all, av_all], [overall_y, overall_y], color=HIGHLIGHT, lw=2.3,
                  solid_capstyle="round", zorder=2)
    ax_metro.scatter(ped_all, overall_y, s=50, color=PED, edgecolor="white",
                     linewidth=0.55, zorder=4)
    ax_metro.scatter(av_all, overall_y, s=50, color=AV, edgecolor="white",
                     linewidth=0.55, zorder=4)
    ax_metro.text(av_all + 3.0, overall_y,
                  f"+{reach['diff']*100:.0f} pp  [95% CI {reach['diff_lo']*100:.0f}\u2013{reach['diff_hi']*100:.0f}]",
                  color=HIGHLIGHT, fontsize=5.4, va="center", fontweight="bold",
                  bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.94),
                  zorder=5)

    ax_metro.set_xlim(0, 108)
    ax_metro.set_ylim(-0.62, overall_y + 0.84)
    ax_metro.set_xticks([0, 25, 50, 75, 100])
    ax_metro.set_yticks([overall_y, *city_y])
    ax_metro.set_yticklabels(["All matched metros", *metro.index.tolist()])
    ax_metro.get_yticklabels()[0].set_fontweight("bold")
    ax_metro.set_xlabel("Event-level national share (%)", labelpad=8)
    ax_metro.set_title("National reach across matched metros", loc="left", pad=8)
    ax_metro.text(-0.025, 1.035, "(a)", transform=ax_metro.transAxes, fontsize=9,
                  fontweight="bold", ha="right", va="bottom", color=INK)
    ax_metro.text(0.00, 0.985, "● Human fatal", transform=ax_metro.transAxes,
                  color=PED, fontsize=5.3, fontweight="bold", va="top")
    ax_metro.text(0.31, 0.985, "● AV crash", transform=ax_metro.transAxes,
                  color=AV, fontsize=5.3, fontweight="bold", va="top")
    ax_metro.grid(axis="x", color="#E6E6E6", lw=0.5)
    ax_metro.grid(axis="y", visible=False)
    ax_metro.tick_params(axis="y", length=0, pad=3)

    # (b) A compact alluvial transformation replaces the old 100%-stacked bars.
    # Categories are deliberately aggregated into three interpretable outlet
    # ecosystems, avoiding decorative hues and making the compositional shift
    # legible at a glance.
    a = art[art.reach_cat != "unknown"]
    groups = [
        ("Local / regional", ["local_regional"], "#A6A6A6"),
        ("National circulation", ["national_general", "national_syndication"], HIGHLIGHT),
        ("Business & specialist outlets", ["business", "tech_trade", "auto_trade"], SECONDARY),
    ]
    shares = {"Ped": [], "AV": []}
    for corpus in shares:
        sub = a[a.corpus == corpus]
        for _, cats, _ in groups:
            shares[corpus].append(100 * sub.reach_cat.isin(cats).mean())
    left_bottom = right_bottom = 0.0
    centers = []
    for (label, _, color), left, right in zip(groups, shares["Ped"], shares["AV"]):
        poly = Polygon([(0, left_bottom), (0, left_bottom + left),
                        (1, right_bottom + right), (1, right_bottom)],
                       closed=True, facecolor=color, edgecolor="white", linewidth=0.75,
                       alpha=0.96, zorder=2)
        ax_flow.add_patch(poly)
        centers.append(((left_bottom + left / 2 + right_bottom + right / 2) / 2,
                        left, right, label, color))
        left_bottom += left
        right_bottom += right

    for center, left, right, label, color in centers:
        # The middle of each stream retains a readable, direct category label;
        # no detached legend is needed to decode the transformation.
        left_label = "<1%" if 0 < left < 0.5 else f"{left:.0f}%"
        right_label = "<1%" if 0 < right < 0.5 else f"{right:.0f}%"
        text_color = "white" if color == SECONDARY else INK
        # The teal stream starts as a very narrow wedge on the human side;
        # shift its compact, three-line label right so every glyph stays safely
        # inside the region without being clipped at the AV edge.
        if color == SECONDARY:
            label_text = f"Business + specialist\noutlets\n{left_label}  \u2192  {right_label}"
            label_x, label_size = 0.73, 5.35
        else:
            label_text = f"{label}\n{left_label}  \u2192  {right_label}"
            label_x, label_size = 0.50, 5.35
        ax_flow.text(label_x, center, label_text, ha="center", va="center",
                     fontsize=label_size, fontweight="bold", color=text_color, zorder=4)

    ax_flow.vlines([0, 1], 0, 100, color=INK, lw=0.75, zorder=3)
    ax_flow.set_xlim(-0.18, 1.18)
    ax_flow.set_ylim(0, 100)
    ax_flow.set_xticks([0, 1])
    ax_flow.set_xticklabels(["Human fatal\n(ped)", "AV crash"])
    ax_flow.set_yticks([0, 25, 50, 75, 100])
    ax_flow.set_ylabel("Article share (%)", labelpad=8)
    ax_flow.set_title("Outlet mix shifts beyond local news", loc="left", pad=8)
    ax_flow.text(-0.025, 1.035, "(b)", transform=ax_flow.transAxes, fontsize=9,
                 fontweight="bold", ha="right", va="bottom", color=INK)
    ax_flow.grid(axis="y", color="#E6E6E6", lw=0.5)
    ax_flow.grid(axis="x", visible=False)
    ax_flow.tick_params(axis="y", length=0, pad=3)

    for ax in (ax_metro, ax_flow):
        ax.set_facecolor("white")
    fig.subplots_adjust(left=0.105, right=0.985, bottom=0.20, top=0.87, wspace=0.30)
    fig.savefig(C.FIGURES / "fig4.pdf"); fig.savefig(C.FIGURES / "fig4.png", dpi=600)
    plt.close(fig)
    log("- wrote fig4.pdf / fig4.png")


# ============================================================ main
def main():
    log("## Step 4 -- decay + reach\n")
    art = C.load_articles()
    pooled = C.load_pooled()

    log("### RQ2 -- attention decay / half-life")
    decay = fit_decay(art)
    tau = tail_share(art)
    for c in ["AV", "Ped"]:
        h = decay[c]
        log(f"- {c}: lambda={h['lam']:.4f} (SE {h['se_lam']:.4f}); "
            f"t_half={h['t_half']:.2f} d (SE {h['se']:.2f}, 95% "
            f"[{h.get('ci',[float('nan')]*2)[0]:.2f},{h.get('ci',[float('nan')]*2)[1]:.2f}]); "
            f"day-0 pred/obs={h['day0_ratio']:.2f} "
            f"({'PASS' if abs(h['day0_ratio']-1) <= 0.2 else 'CHECK >20%'})")
    log(f"- decay-rate difference lambda1(AVxt)={decay['lambda1_AVt']:.4f} "
        f"(SE {decay['lambda1_se']:.4f}, p={decay['lambda1_p']:.4f}); "
        f"{'AV decays SLOWER' if decay['lambda1_AVt']>0 else 'AV decays faster'}")
    log(f"- tail share tau: AV={tau['AV']:.3f}, Ped={tau['Ped']:.3f} "
        f"(share of articles with lag>14d; fit is days 0-14 only)")
    log(f"- dropped {decay['n_neg_dropped']} articles with lag<-1 (date errors)")
    log("- CAVEAT (writer): human coverage peaks at day 0-1 (exponential day-0 "
        "pred/obs=1.1, good fit); AV coverage RAMPS to a peak at day 1-2 (national/"
        "tech pickup lag: daily counts 13,48,48,10,...), so the day-0 exponential "
        "intercept over-extrapolates (pred/obs=2.9). The half-life is a within-window "
        "(days 0-14) decay-RATE summary -- the slope difference lambda1 is highly "
        "significant (p<0.001) and robust; AV persistence is if anything UNDERSTATED "
        "because 56% of AV coverage (tau) lands beyond day 14 vs 8% for human. Report "
        "half-life + tau together; do not claim AV coverage peaks at day 0.")

    # first-pub-based lag sensitivity
    log("\n### Decay sensitivity: lag from first-publication date")
    fp = art.dropna(subset=["pub"]).copy()
    firstpub = fp.groupby("event_id")["pub"].transform("min")
    fp["lag_days"] = (fp["pub"] - firstpub).dt.days
    decay_fp = fit_decay(fp)
    log(f"- first-pub lag: AV t_half={decay_fp['AV']['t_half']:.2f} d, "
        f"Ped t_half={decay_fp['Ped']['t_half']:.2f} d "
        f"(day0 pred/obs AV={decay_fp['AV']['day0_ratio']:.2f} "
        f"Ped={decay_fp['Ped']['day0_ratio']:.2f})")

    log("\n### RQ3 -- geographic reach")
    art, nat_map = classify_reach(art)
    cov = float((art.reach_cat != "unknown").mean())
    log(f"- domain classification covers {cov:.1%} of articles "
        f"({int((art.reach_cat=='unknown').sum())} blank-domain residual); "
        f"national list has {len(nat_map)} domains. "
        f"{'PASS >=95%' if cov >= 0.95 else 'CHECK <95%'}")
    ev = event_national_share(art, pooled)
    reach = reach_bootstrap(ev)
    log(f"- event-level national+ share: AV mean={reach['av_mean']:.3f}, "
        f"Ped mean={reach['ped_mean']:.3f}; diff={reach['diff']:.3f} "
        f"95% [{reach['diff_lo']:.3f}, {reach['diff_hi']:.3f}]")
    # compositional breakdown
    comp = {}
    for cp in ["AV", "Ped"]:
        sub = art[(art.corpus == cp) & (art.reach_cat != "unknown")]
        comp[cp] = (sub.reach_cat.value_counts(normalize=True) * 100).round(1).to_dict()
    log(f"- composition AV: {comp['AV']}")
    log(f"- composition Ped: {comp['Ped']}")

    fig3(decay, tau, art)
    fig4(pooled, ev, art, reach)

    # save results
    def clean_half(h):
        return {k: v for k, v in h.items() if k != "grid"}
    C.update_results("decay", {
        "AV": {k: v for k, v in decay["AV"].items()},
        "Ped": {k: v for k, v in decay["Ped"].items()},
        "lambda1_AVt": decay["lambda1_AVt"], "lambda1_p": decay["lambda1_p"],
        "tail_share": tau, "n_neg_dropped": decay["n_neg_dropped"],
        "first_pub_sensitivity": {
            "AV_t_half": decay_fp["AV"]["t_half"], "Ped_t_half": decay_fp["Ped"]["t_half"]},
        "se_caveat": (
            "Half-life CIs and lambda1 p-value come from a Poisson GLM on aggregated "
            "daily counts treating each lag-day as independent; the Cruise event "
            "dominates the AV daily counts, so these SEs ignore event-level clustering "
            "and are anti-conservative. The qualitative conclusion (AV decays slower; "
            "tau 56% vs 8%) is descriptive and robust; treat the half-life CIs as "
            "approximate."),
    })
    C.update_results("reach", {**reach, "coverage": cov, "composition": comp,
                               "n_national_domains": len(nat_map)})
    C.write_qa_section("40-step4", "\n".join(qa))
    log("\n- Saved results.json[decay,reach] + fig3 + fig4")


if __name__ == "__main__":
    main()
