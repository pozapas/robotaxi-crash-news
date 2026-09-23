# -*- coding: utf-8 -*-
"""Every headline number in the manuscript must appear in the reanalysis JSON.
Guards against a stale figure surviving the rewrite."""
import io, json, os, glob

SC = os.path.dirname(os.path.abspath(__file__))
REAN = os.path.join(SC, 'rean')
ROOT = (u"D:/OneDrive - Texas State University/AIT/Papers/TRB2027/Crash News/"
        u"TRB2027/TRB_R_robotaxi_amplification/RoboTaxi_CrashNews_Journal")

core = json.load(io.open(os.path.join(REAN, 'out_core.json'), encoding='utf-8'))
rest = json.load(io.open(os.path.join(REAN, 'out_rest.json'), encoding='utf-8'))
tab = json.load(io.open(os.path.join(REAN, 'out_table.json'), encoding='utf-8'))
syn = json.load(io.open(os.path.join(REAN, 'out_syndication.json'), encoding='utf-8'))

text = u''
for f in sorted(glob.glob(os.path.join(ROOT, 'sections', '*.tex'))):
    if os.path.basename(f) == '00_abstract.tex':
        continue
    for l in io.open(f, encoding='utf-8'):
        if not l.lstrip().startswith('%'):
            text += l
for l in io.open(os.path.join(ROOT, 'main.tex'), encoding='utf-8'):
    if not l.lstrip().startswith('%'):
        text += l
text += io.open(os.path.join(ROOT, 'table3.tex'), encoding='utf-8').read()

CHECKS = [
    ("headline AF", "%.2f" % core['headline']['cell_overlap']['af'], True),
    ("headline boot lo", "%.2f" % core['headline']['cell_overlap_boot']['lo'], True),
    ("headline boot hi", "%.2f" % core['headline']['cell_overlap_boot']['hi'], True),
    ("additive full", "%.2f" % core['headline']['additive_full']['af'], True),
    ("PDO af", "%.2f" % core['severity']['PDO']['af'], True),
    ("Injury af", "%.2f" % core['severity']['Injury']['af'], True),
    ("Injury boot lo", "%.2f" % core['severity']['Injury']['boot_lo'], True),
    ("Injury boot hi", "%.2f" % core['severity']['Injury']['boot_hi'], True),
    ("loo min", "%.2f" % core['injury_influence']['loo_min'], True),
    ("loo max", "%.2f" % core['injury_influence']['loo_max'], True),
    ("drop top1", "%.2f" % core['injury_influence']['topk']['drop_top1']['af'], True),
    ("drop top2", "%.2f" % core['injury_influence']['topk']['drop_top2']['af'], True),
    ("drop top4", "%.2f" % core['injury_influence']['topk']['drop_top4']['af'], True),
    ("local primary", "%.2f" % rest['local']['primary_all_events']['ratio'], True),
    ("local incidence OR", "%.2f" % rest['local']['incidence_or'], True),
    ("local pos intensity", "%.2f" % rest['local']['positive_intensity']['ratio'], True),
    ("local injury", "%.2f" % rest['local']['by_severity']['Injury']['ratio'], True),
    ("local PDO", "%.2f" % rest['local']['by_severity']['PDO']['ratio'], True),
    ("half-life AV", "%.2f" % rest['halflife_peak']['AV']['half_life'], True),
    ("half-life Ped", "%.2f" % rest['halflife_peak']['Ped']['half_life'], True),
    ("median lag AV", "%d" % rest['timing_nonparametric']['AV']['median_lag_article_weighted'], True),
    ("p90 AV", "%d" % rest['timing_nonparametric']['AV']['p90_article'], True),
    ("excl cruise", "%.2f" % tab['excl_cruise']['af'], True),
    ("unique outlets", "%.2f" % tab['unique_outlets']['af'], True),
    ("jackknife min", "%.2f" % tab['jackknife']['min'], True),
    ("jackknife max", "%.2f" % tab['jackknife']['max'], True),
    ("ztnb", "%.2f" % tab['ztnb']['af'], True),
    ("stories af", "%.2f" % syn['n_stories']['af'], True),
    ("stories lo", "%.2f" % syn['n_stories']['boot_lo'], True),
    ("stories hi", "%.2f" % syn['n_stories']['boot_hi'], True),
    ("stories PDO", "%.2f" % syn['stories_PDO']['af'], True),
    ("stories Injury", "%.2f" % syn['stories_Injury']['af'], True),
    ("dup pct AV", "%.1f" % (100*syn['compression']['AV']['pct_duplicate']), True),
    ("dup pct Ped", "%.1f" % (100*syn['compression']['Ped']['pct_duplicate']), True),
]

bad = 0
for label, val, must in CHECKS:
    ok = val in text
    if not ok:
        bad += 1
    print("%-24s %-8s %s" % (label, val, "OK" if ok else "*** NOT IN TEXT ***"))

# stale values that must NOT survive
STALE = ["4.28 times", "10.01", "3.75", "8.55", "1.79", "2.9 days", "56 percent of robotaxi",
         "1.64 times", "3.06", "3.95", "4.97"]
print("\n--- superseded values that must be gone ---")
for s in STALE:
    present = s in text
    if present:
        bad += 1
    print("%-28s %s" % (s, "*** STILL PRESENT ***" if present else "gone"))
print("\nproblems:", bad)
