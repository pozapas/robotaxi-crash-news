# -*- coding: utf-8 -*-
"""Every headline number in the manuscript must appear in the reanalysis JSON.
Guards against a stale figure surviving the rewrite."""
import io, json, os, glob

SC = os.path.dirname(os.path.abspath(__file__))
REAN = os.path.join(SC, 'rean') if os.path.isdir(os.path.join(SC, 'rean')) else SC
import sys
sys.path.insert(0, SC)
from paths import MANUSCRIPT, require
ROOT = str(require(MANUSCRIPT, "ROBOTAXI_MANUSCRIPT"))

core = json.load(io.open(os.path.join(REAN, 'out_core.json'), encoding='utf-8'))
rest = json.load(io.open(os.path.join(REAN, 'out_rest.json'), encoding='utf-8'))
tab = json.load(io.open(os.path.join(REAN, 'out_table.json'), encoding='utf-8'))
syn = json.load(io.open(os.path.join(REAN, 'out_syndication.json'), encoding='utf-8'))
val = json.load(io.open(os.path.join(REAN, 'out_validation.json'), encoding='utf-8'))
sen = json.load(io.open(os.path.join(REAN, 'out_sensitivity.json'), encoding='utf-8'))

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
    ("kappa rel_av", "%.2f" % val['agreement']['rel_av']['kappa'], True),
    ("kappa sev", "%.2f" % val['agreement']['sev']['kappa'], True),
    ("kappa link_av", "%.2f" % val['agreement']['link_av']['kappa'], True),
    ("recall AV", "%.2f" % val['discovery']['robotaxi']['all']['recall'], True),
    ("recall Ped", "%.2f" % val['discovery']['pedestrian']['all']['recall'], True),
    ("recall Ped lo", "%.2f" % val['discovery']['pedestrian']['all']['rec_lo'], True),
    ("recall text Ped", "%.2f" % val['discovery']['pedestrian']['text_only']['recall'], True),
    ("false link AV", "%.1f" % (100*val['linkage']['robotaxi']['rate']), True),
    ("false link Ped", "%.1f" % (100*val['linkage']['pedestrian']['rate']), True),
    ("injury confirmed af", "%.2f" % val['injury_confirmed']['af'], True),
    ("injury confirmed lo", "%.2f" % val['injury_confirmed']['boot_lo'], True),
    ("pdo confirmed af", "%.2f" % val['pdo_confirmed']['af'], True),
    ("ac1 rel_av", "%.2f" % val['agreement']['rel_av']['ac1'], True),
    ("ac1 link_av", "%.2f" % val['agreement']['link_av']['ac1'], True),
    ("ac1 sev", "%.2f" % val['agreement']['sev']['ac1'], True),
    ("local inj drop4", "%.2f" % sen['n_local']['Injury_drop_top4']['af'], True),
    ("local inj drop4 lo", "%.2f" % sen['n_local']['Injury_drop_top4']['wald_lo'], True),
    ("early all", "%.2f" % sen['n_early']['all']['af'], True),
    ("early all lo", "%.2f" % sen['n_early']['all']['wald_lo'], True),
    ("early inj", "%.2f" % sen['n_early']['Injury']['af'], True),
    ("early inj drop4", "%.2f" % sen['n_early']['Injury_drop_top4']['af'], True),
    ("p90 event weighted", "%d days" % sen['timing']['AV']['p90_event_weighted'], True),
    ("p90 ew no cruise", "with or without the Cruise crash"
     if sen['timing']['AV']['no_cruise']['p90_event_weighted'] == sen['timing']['AV']['p90_event_weighted']
     else "*** no-Cruise p90 differs ***", True),
    ("first after 14 AV", "%d percent" % round(100*sen['timing']['AV']['first_after_14_share']), True),
    ("first after 14 Ped", "%d percent" % round(100*sen['timing']['Ped']['first_after_14_share']), True),
    ("multi tail AV", "%d percent" % round(100*sen['timing']['AV']['multi_tail_share_mean']), True),
    ("cell tail diff", "%d" % round(100*sen['within_cells']['tail_share']['diff']), True),
    ("cell nat diff", "%d [%d, %d]" % tuple(round(100*sen['within_cells']['national_share'][k]) for k in ('diff', 'lo', 'hi')), True),
    ("era pre ped", "%d human events" % sen['subset_sizes']['era_pre']['n_comp'], True),
    ("era post ped", "%d after" % sen['subset_sizes']['era_post']['n_comp'], True),
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
