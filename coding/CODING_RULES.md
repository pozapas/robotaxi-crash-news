# Human validation: coding rules

Two coders, independent of the corpus construction and blind to the comparison
under study and to every pipeline label, coded the same 516 items. An
adjudicator resolved every disagreement. The item-level codes are in
`data/human_validation_codes.csv`, and `code/r13_human_validation.py`
reproduces every reported figure from that file.

## Items

| Task | Items | Question |
|---|---|---|
| Robotaxi relevance | 155 articles | Does this article report a specific crash in the United States that involved an automated, self-driving, driverless or robotaxi vehicle? |
| Pedestrian relevance | 150 articles | Does this article report a specific road crash in the United States in which a pedestrian was killed? |
| Robotaxi severity | 51 crashes | According to the articles, how severe was this crash? |
| Robotaxi linkage | 80 links | Does this article report this crash? |
| Pedestrian linkage | 80 links | Does this article report this crash? |

The relevance articles were sampled from four strata: articles the pipeline
kept, rejected articles that matched a keyword screen, other rejected articles
with retrieved text, and rejected articles whose text was never retrieved.
Population sizes are in `data/strata_sizes.json`. For articles with no
retrieved text, coders opened the link and recorded whether they read the live
page (`LIVE_PAGE`), judged from the address because the page did not open
(`URL_ONLY`), or found nothing usable (`NONE`). The severity items are the 51
robotaxi crashes in the analysis frame, and the linkage items are links of
events inside the frame.

## Rules

**Robotaxi relevance.** Yes when the article reports one specific US crash
involving a driverless, autonomous-mode or robotaxi vehicle; being struck, or
a minor crash, counts. No for business, permit, policy, recall, investigation
or software news with no particular crash; ordinary driver assistance with no
self-driving system claimed; crashes only as counts or statistics; a past
crash only as background; or a crash outside the United States.

**Pedestrian relevance.** Not about robotaxis. Yes when a person on foot was
struck by any vehicle and died, at the scene or later, including hit-and-run
deaths and follow-up, arrest or court stories that identify the crash. No when
the pedestrian survived, the person killed was on a bicycle, scooter or
motorcycle, the article is policy or statistics, the death was not a road
crash, or the crash was outside the United States.

**Robotaxi severity.** Applied in order. Fatal if anyone died as a result of
this crash. Injury if anyone was hurt, even minor or "complained of pain".
Property damage only if the articles describe damage and say nobody was hurt.
Can't tell if no article says whether anyone was hurt. An animal hurt with no
person hurt is property damage only.

**Robotaxi linkage.** Yes when the article reports the same crash (same date,
city, company and event), even weeks later or in different words, including
recalls, permit actions or lawsuits that refer to this crash. No for a
different incident, or general news that never mentions this crash. An article
published before the crash date is almost always No.

**Pedestrian linkage.** Not about robotaxis. Yes when the article reports the
same pedestrian death (same date, street or area and circumstances), including
later arrest or court stories. No for a different pedestrian death, even in
the same city.

## Protocol

Coders worked in a web application that showed one item at a time, with the
task restated in a banner on every item. Each task opened with these rules and
a check of three made-up examples that had to be answered correctly before
coding began. A first round without those aids was discarded, because the
instructions had been misread, and both coders then coded the full set under
the final protocol; only those codes are released. The adjudicator saw both
answers labelled Coder A and Coder B, in an order shuffled for each item, and
no pipeline label, and chose the answer that follows the rules above.

Reliability thresholds were fixed before coding: Cohen's kappa of at least
0.80 is reliable, 0.60 to 0.79 marginal, and below 0.60 the adjudicated codes
are used and the shortfall is reported. Gwet's AC1 is reported alongside.

The articles themselves belong to their publishers and are not redistributed;
each coded item is identified by the pipeline's article, event or link
identifier.
