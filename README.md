# How Loud Is a Robotaxi Crash?

Replication material for *How Loud Is a Robotaxi Crash? Quantifying
Media-Attention Amplification Against a Human-Driven Comparator*.

The paper asks how much more news coverage a crash involving an automated
vehicle receives than a human-driven crash reported in the same metropolitan
area in the same period, whether that coverage persists longer, and whether it
is drawn from a different mix of outlets.

## What is here

| Path | Contents |
|---|---|
| `data/analysis_events.csv` | The 797 crashes in the analysis frame, one row each, with corpus, date, metropolitan area, severity, operator, article count and unique-outlet count. |
| `data/analysis_articles.csv` | The 1,498 linked articles, one row each, with source domain, publication date and publication lag. |
| `data/metro_map.csv` | City-to-metropolitan-area mapping, applied identically to both corpora. |
| `data/national_domains.csv` | The 92 national, syndication, technology, automotive and business-trade domains used for the outlet-composition measure. |
| `data/story_clusters.csv` | Articles and distinct stories per event, from the near-duplicate analysis. |
| `code/r08_core.py` | Headline and severity contrasts, bootstrap, permutation test, injury influence analysis. |
| `code/r08_rest.py` | Local-outlet models, equal-follow-up timing, outlet composition. |
| `code/r08_table.py` | Operator, era, jackknife, Cruise-exclusion, unique-outlet and zero-truncated rows. |
| `code/r09_syndication.py` | Near-duplicate clustering and the distinct-story models. |
| `code/check_manuscript_numbers.py` | Asserts every headline number in the manuscript matches these outputs. |
| `code/out_*.json` | Machine-readable estimates emitted by the scripts above. |
| `code/figures/` | The scripts that draw Figures 3 and 4, plus the shared style kit. See the README there for the one substitution needed to run them from this repository. |
| `pipeline/` | The GDELT BigQuery discovery statement and the extraction prompt, verbatim. |
| `code/r12_lane_provenance.py` | Lane provenance and the common-domain-universe test. |

## Reproducing the estimates

Requires Python 3.13 with pandas 2.3, numpy 2.2, statsmodels 0.14, scipy 1.13
and pyarrow 21. Every resampling procedure is seeded with `20260921`; the
bootstrap uses 2,000 replicates and the permutation test 5,000 relabelings.

```
python code/r08_core.py
python code/r08_rest.py
python code/r08_table.py
python code/r09_syndication.py
python code/r12_lane_provenance.py
python code/check_manuscript_numbers.py
```

The scripts read the parquet build by default. Point them at `data/*.csv`
instead if you are working from this repository alone.

## What is not here, and why

Article full text is the property of the publishers and is not redistributed.
Each article is identified by its source domain and publication date, so the
corpus can be reconstructed from the original publishers. `data/` contains no
article text and no identifying information about crash victims.

The near-duplicate analysis in `code/r09_syndication.py` needs article text and
therefore cannot be re-run from this repository alone. Its per-event output is
included as `data/story_clusters.csv` so the models that use it can be checked.

## Licence

Code is MIT. Data is CC BY 4.0. See `LICENSE`.
