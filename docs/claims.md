# Claims file

One entry per citation instance in the live manuscript text (Sections 1 to 7),
giving the citation key, the sentence that cites it, a short verbatim excerpt
from the source that bears on it, and where the excerpt was found. Each entry
carries a verdict: SUPPORTED, PARTLY (the source supports a narrower or weaker
version), NOT_SUPPORTED, or UNVERIFIED (no accessible text settles it; the
author must check the source). Excerpts are kept under 25 words.

Instances: 73. Sources: 33. NOT_SUPPORTED 1, PARTLY 22, UNVERIFIED 0, SUPPORTED 50.


**Status, 27 October 2026.** The manuscript was revised to the wording each
source supports for every PARTLY and NOT SUPPORTED entry (ids 4, 6, 9, 10, 12,
14, 16, 18, 19, 27, 31, 33, 35, 36, 37, 48, 52, 53, 54, 57, 59, 62, 70, 71).
The sentences quoted below are the pre-revision versions. The formerly
unverified entries were checked against full texts the author supplied, and
entry 68 now cites the Third Amended Standing General Order 2021-01.

## Not Supported (1)

**35. `koopman2024`** (02_literature)

- Sentence: Yet a single low-severity crash contributed to the end of a company's operations [koopman2024,cadmv2023].
- Source: "resulted not only in a severe injury, but also dramatic upheaval at that company" (abstract; p.14: 'Cruise operations eventually had to be shut down' (https://arxiv.org/pdf/2402.06046v3))
- Action: Yet a single crash, and the company's handling of it, contributed to the shutdown of a company's driverless operations [koopman2024,cadmv2023].
- Note: Koopman contradicts 'low-severity': the source calls the injury 'severe' (abstract) and 'a dramatic, severe pedestrian injury' (p.13). Koopman does support the 'end of operations' part ('Cruise ultimately shutting down their public robotaxi operations for an extended period', p.4), but attributes it mainly to the communication failure: 'this communication mistake (rather than the mishap itself) was the main reason' (p.14). The sentence contrasts this crash with the mostly non-injury SGO crashes, so the 'low-severity' label carries the argument and must change. The same wording appears in the commented-out paragraph in 02_literature.tex and in review_results/render_build. Also: Koopman says operations shut down 'for an extended period', not that they ended permanently, and cadmv2023 is a suspension order. Cruise's final end of robotaxi operations (GM, Dec 2024) postdates Koopman v3 (Aug 2024), which is why the fix says 'shutdown'.

## Partly (22)

**4. `jelinski2021`** (01_introduction)

- Sentence: Studies of automated-vehicle crash coverage show that crashes drive volume and sentiment within automated-vehicle discourse [jelinski2021,penmetsa2021], but disproportionate implies a comparator, and none of that work has one.
- Source: "accidents with automated or autonomous cars increase the frequency and negativity of the coverage" (Discussion, p.13 (https://jcom.sissa.it/archive/20/04/JCOM_2004_2021_A02.pdf))
- Action: Studies of automated-vehicle crash coverage show that crashes drive volume and sentiment within automated-vehicle discourse [jelinski2021,penmetsa2021], but disproportionate implies a comparator, and none of that work compares automated-vehicle crashes with human-driven crashes.
- Note: Jelinski supports the volume and negativity part, and penmetsa2021 the sentiment part. However, 'none of that work has one [a comparator]' clashes with Jelinski, which compares routine articles with articles published within 14 days of an accident (p.8). The manuscript's own Table (tab:gap) rates Jelinski's Comparator as partial. Saying what kind of comparator is missing removes the contradiction. Minor: penmetsa2021 studies tweets rather than news coverage.

**6. `anania2018`** (01_introduction)

- Sentence: Public risk perception shapes willingness to use automated vehicles [anania2018] and the regulatory environment.
- Source: "Consumer perceptions will ultimately determine the success or failure of driverless vehicles, and potentially drive policy changes" (abstract (Objectives) via Semantic Scholar API)
- Action: Public perceptions, which media portrayals can shift, shape willingness to ride in automated vehicles [anania2018] and may drive policy changes.
- Note: The source frames this as consumer perceptions in general, not risk perception specifically. Its experiment manipulates positive or negative information and measures willingness to ride; it does not measure risk perception. The regulatory part is stated only as 'potentially drive policy changes'.

**9. `stilgoe2018`** (01_introduction)

- Sentence: If coverage volume is a poor proxy for harm, decisions tuned to public reaction rest on a distorted signal, and measuring that distortion is also a precondition for the normative debate about whether the attention is warranted [stilgoe2018].
- Source: "Except in cases of total cover-up, accidents can force public reframing and institutional reflection." (https://discovery.ucl.ac.uk/id/eprint/10038434 (author accepted manuscript), p. 4 of AAM)
- Action: Make it clear that the precondition argument is the authors' own and that Stilgoe is cited only for the social-learning view, e.g. '...is also a precondition for the normative debate about whether the attention is warranted, since crashes can also prompt legitimate public reframing and institutional reflection [stilgoe2018].'
- Note: Stilgoe argues that crashes enable social learning, using the 2016 Tesla crash as his case. He does not discuss coverage volume as a distorted proxy for harm, and he does not discuss measuring media attention. Only the normative or social-learning framing is supported.

**10. `kasperson1988`** (02_literature)

- Sentence: \section{Background}\label{sec:lit} The social amplification of risk framework explains why hazards with identical expected losses provoke very different public responses, since risk signals pass through stations that intensify or attenuate them, with news media the most consequential [kasperson1988].
- Source: "Signals about risk are processed by individual and social amplification stations, including the scientist who communicates the risk assessment, the news media" (abstract; station list p. 181; media discussion p. 185 (Risk Analysis 8(2)))
- Action: '...since risk signals pass through amplification stations, such as scientists, the news media, activist groups and personal networks, that intensify or attenuate them, with the news media among the most studied [kasperson1988].'
- Note: The framework and the intensify/attenuate mechanism are supported (p. 180: amplification 'denotes the process of intensifying or attenuating signals'). 'News media the most consequential' is not stated: the media are one of seven listed stations. The closest wording is p. 185: news media 'have received the bulk of scientific attention for their critical role in public opinion formation'. The 'identical expected losses' clause is supported by p. 177 ('a high-consequence/low-probability risk with identical expected values') together with the abstract's 'relatively minor risks... elicit strong public concerns'.

**12. `kasperson2022sarf`** (02_literature)

- Sentence: After three decades of empirical work, its originators note how much of the amplification literature remains conceptual [kasperson2022sarf], and a recent review of automated-vehicle risk perception asks whether social amplification operates for automated vehicles at all [naiseh2025].
- Source: "more effort is put into measuring media coverage than is put into clarifying the process by which media coverage influences risk perceptions" (https://www.ebi.ac.uk/europepmc/webservices/rest/PMC10360138/fullTextXML (PMC10360138), section 'Literature review'; also 'SARF is a conceptual framework and not a theory' (section 2))
- Action: 'After three decades of empirical work, Kasperson and colleagues describe SARF as a conceptual framework rather than a predictive theory, and note that studies measure media coverage more than they clarify how it shapes risk perceptions [kasperson2022sarf]...'
- Note: The source does not say that much of the literature 'remains conceptual'. It reviews more than 50 empirical studies since 2003 and calls SARF a conceptual framework, not a theory, useful as an organizing tool or post hoc. Also, of the four authors only Kasperson is an original 1988 author, so 'its originators' is loose; 'Kasperson and colleagues' is safer. 'Three decades of empirical research' is supported by the abstract ('close to three decades of empirical research').

**14. `jelinski2021`** (02_literature)

- Sentence: In five German newspapers, accidents sharply raised both the frequency and the negativity of automated-driving coverage [jelinski2021].
- Source: "as soon as an accident involving an autonomous vehicle occurs, the frequency of reporting, as well as the extent of negativity and detail increase" (abstract; Results pp.8-11 (https://jcom.sissa.it/archive/20/04/JCOM_2004_2021_A02.pdf))
- Action: In five German newspapers, accidents raised both the frequency and the negativity of automated-driving coverage [jelinski2021].
- Note: Five outlets is right: FAZ and SZ (print) plus Spiegel Online, Bild.de and Zeit Online, 359 articles, May 2017 to Oct 2018. 'Sharply' overstates the evidence. The frequency result is descriptive only: monthly peaks 'can most probably be attributed to accidents', with no test and 'no significant trend'. Tone (p.11) is 'considerably more negative' within 14 days of an accident (Cramer's V = .228 for headings). Either drop 'sharply' or say 'markedly' for negativity only. Rule applied across ids 4/14/55: only explicit intensifiers beyond the source ('sharply') are flagged; plain 'raise', 'drive' and 'spike' match the source's own 'increase the frequency and negativity' (p.13).

**16. `sun2025`** (02_literature)

- Sentence: On social media, sentiment shifted measurably across roughly 1.7 million posts after the 2018 Uber and Tesla crashes [penmetsa2021], and blame follows recognizable patterns when an automated vehicle crashes [sun2025].
- Source: "Regarding the topic AV system, the public appeared to have difficulty in classifying AV levels, with the highest blame volume and most negative sentiments." (abstract, p. 1 (full text supplied by the author))
- Action: Revised to 'in social-media comments on automated-vehicle crashes the automated system draws the most blame'.
- Note: Source analyses 90,426 Chinese social-media comments; 'recognizable patterns' was vaguer than the finding.

**18. `liu2019`** (02_literature)

- Sentence: Participants shown otherwise identical crash scenarios rate the automated-vehicle crash as more severe and assign responsibility differently, a response attributed mainly to affective risk perception [liu2019].
- Source: "participants had a tendency to perceive traffic crashes involving SDVs to be more severe than those involving conventionally human-driven vehicles" (abstract (via Semantic Scholar API); full text paywalled)
- Action: 'Participants shown otherwise identical crash scenarios rate the automated-vehicle crash as more severe and less acceptable, a response attributed to the affect heuristic [liu2019].' If the responsibility finding is wanted, consider citing Liu & Du, 'Blame Attribution Asymmetry in Human-Automation Cooperation', Risk Analysis 42 (online 2021), DOI 10.1111/risa.13674 (Crossref-verified). Note its scope differs: it studies semi-automated vehicles where the human or the automation is at fault.
- Note: Severity and the affect explanation are supported: 'this biased response could be a result of people's reliance on the affect heuristic' (five vignette experiments, N = 1267). Responsibility does not appear in the abstract; the measured outcomes are perceived severity and acceptability. The secondary evidence is mixed: one citing paper credits Liu et al. 2019 with 'severity and acceptance' and credits blame and responsibility to Waytz et al., while other citing papers group Liu et al. 2019 with studies showing more blame. The author must check the Methods. 'Mainly' is stronger than the source's 'could be'. Full text not reached.

**19. `anania2018`** (02_literature)

- Sentence: Negative information about automated vehicles moves stated willingness to ride more than positive information does [anania2018], and the appetite for negative news is general, since in about 105,000 randomized headline variants each additional negative word raised the click-through rate [robertson2023negativity].
- Source: "individuals are more willing to ride in driverless vehicles after hearing positive information about them, and less willing to ride after hearing negative information" (abstract and Studies 1 and 2, pp. 221-222 (full text supplied by the author))
- Action: Revised to 'lowers stated willingness to ride and positive information raises it'.
- Note: Both directions are tested against a no-information baseline, but no asymmetry between them is tested.

**27. `eisensee2007`** (02_literature)

- Sentence: Coverage of a disaster depends partly on competition from other events, which yields an exchange rate in attention between groups of victims [eisensee2007].
- Source: "we have computed the casualties ratio that would make media coverage equally likely, all else equal" (working-paper version (perseus.iies.su.se/ dstro/wpdisasters.pdf via web.archive.org), p. 29 and Table VIII; published abstract for crowding out)
- Action: Coverage of a disaster depends partly on competition from other news, and the number of deaths needed for equal coverage differs widely across types of disaster [eisensee2007].
- Note: Both parts are in the paper: crowding out by other news, and a 'casualties ratio' (e.g. 38,920 food-shortage deaths per volcano death). But the ratio between groups of victims comes from disaster-type and region fixed effects, not from news competition, so 'which yields' links them wrongly. The working paper (p. 28) does give a news-pressure casualty ratio: six times as many deaths at the highest versus the lowest news pressure, and three times during the Olympics. But that ratio is for the chance of relief, not coverage, and it compares disasters at different times, not groups of victims. The ratios between groups (Tables VIII and IX) come from type and region fixed effects. The paper never uses the term 'exchange rate'. Page numbers are from the working paper, not the QJE pagination (693-728), and the published wording may differ slightly.

**31. `vasterman2005hypes`** (02_literature)

- Sentence: Coverage can also sustain itself, since a media hype after a disaster is driven by self-reinforcing newsroom attention rather than by the event [vasterman2005hypes].
- Source: "pushed forward mainly by self-reinforcing processes within the news production itself" (section 'Media Hypes and Risk Amplification', subsection 'Media hype' (academic.oup.com/epirev/article/27/1/107/520580))
- Action: Coverage can also sustain itself, since a media hype after a disaster, once triggered by the event, is driven mainly by self-reinforcing newsroom attention [vasterman2005hypes].
- Note: Source says hypes are 'triggered by unusual or shocking events' and pushed forward 'mainly' by self-reinforcing news production; 'rather than by the event' overstates this.

**33. `garciagavilanes2016`** (02_literature)

- Sentence: Decay of crash-related attention has been estimated once, for aircraft crashes, where Wikipedia attention peaks within days and then declines exponentially with half-lives from about one day to several weeks, unrelated to the number of fatalities [garciagavilanes2016].
- Source: "the rate and time span of the decay of attention is independent of the number of deaths" (abstract; Table 4 (half-life min 0.3 d, max 24 d English / 30 d Spanish); section 2.3)
- Action: ... where Wikipedia attention peaks within days and then declines exponentially, with half-lives from a few hours to several weeks, unrelated to the number of fatalities [garciagavilanes2016].
- Note: Exponential decay after an initial boost (sec 2.3) and independence from deaths (Fig 6, Spearman) are supported. Peak: boost within 5 days of page creation in 73% of cases (measured from page creation, not event date). Table 4 half-life range is 0.3 to 24 (En) / 30 (Sp) days, so the lower bound is about 7 hours, not 'about one day'; the distribution is concentrated at the low end and the paper summarizes decay as 'on the order of a few days'. The 'estimated once' novelty claim is the authors' own and cannot be checked against this source.

**36. `cadmv2023`** (02_literature)

- Sentence: Yet a single low-severity crash contributed to the end of a company's operations [koopman2024,cadmv2023].
- Source: "the immediate suspension of Cruise LLC's deployment and driverless testing permits" (https://www.dmv.ca.gov/portal/news-and-media/dmv-statement-on-cruise-llc-suspension/)
- Action: Yet a single crash led to the suspension of a company's driverless permits [cadmv2023]. (If 'contributed to the end of its operations' is kept, it needs a separate source: neither cadmv2023 nor koopman2024 [Feb 2024; abstract says only 'dramatic upheaval at that company'] reports an end of operations.)
- Note: The DMV statement supports only the permit suspension; it says nothing on crash severity or the end of operations. More important, 'low-severity' conflicts with the record: the pedestrian was severely injured (koopman2024 abstract: 'resulted not only in a severe injury'). Drop 'low-severity'. koopman2024 is checked in another part; its reviewer should test the same 'end of operations' and 'low-severity' points.

**37. `stilgoe2018`** (02_literature)

- Sentence: Whether intensified scrutiny of an emerging technology is disproportionate attention or legitimate social learning is a normative question [stilgoe2018] whose answer first requires an estimate of the magnitude, persistence and outlet composition of the coverage differential.
- Source: "Accidents therefore provide a constructive opportunity for reframing." (https://discovery.ucl.ac.uk/id/eprint/10038434 (author accepted manuscript), p. 21 of AAM (end of section before 'Responding to the first self-driving death'))
- Action: 'Intensified scrutiny of an emerging technology after a crash can be legitimate social learning [stilgoe2018] rather than mere disproportion, and judging which first requires an estimate of...'
- Note: Stilgoe supports the social-learning side (accidents 'can force public reframing and institutional reflection', p. 4). He does not set up a 'disproportionate attention versus social learning' normative question and does not mention media attention volume. The dichotomy is the authors' framing.

**48. `ralph2019`** (03_data)

- Sentence: The groups also differ in configuration, since the human-driven sample is pedestrian-involved by construction and the robotaxi sample is dominated by vehicle-to-vehicle and property-damage-only events, and pedestrian crashes carry distinct reporting frames [ralph2019].
- Source: "examine local news coverage of vehicle crashes involving someone walking or biking" (abstract)
- Action: ... and news coverage of pedestrian crashes tends to shift blame toward the pedestrian [ralph2019].
- Note: Ralph et al. analyze only pedestrian/bicyclist crash articles and do not compare them with vehicle-to-vehicle or property-damage crashes. They document the frames used but do not show the frames are 'distinct' from those used for other crash types.

**52. `naiseh2025`** (06_discussion)

- Sentence: \section{Discussion}\label{sec:discussion} The social amplification of risk framework has been applied to automated vehicles descriptively for years, and a recent review states that whether amplification operates for them remains open [naiseh2025,kasperson1988].
- Source: "the AV research community may need to further examine whether social amplification exists in AV" (https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11968569/fullTextXML (PMC11968569), section 'Theoretical implications')
- Action: Split the citations and support or drop the first clause: 'The social amplification of risk framework [kasperson1988] has been invoked for automated vehicles [cite an AV study that actually applies SARF; jelinski2021 does not mention amplification or Kasperson (checked jelinski.txt in the scratchpad)], and a recent review states that whether amplification operates for them remains open [naiseh2025].'
- Note: 'whether amplification operates for them remains open' is supported. 'Applied to automated vehicles descriptively for years' is not: Naiseh et al. say the AV literature they reviewed limited risk perception to the individual level, which runs against the clause.

**53. `kasperson1988`** (06_discussion)

- Sentence: \section{Discussion}\label{sec:discussion} The social amplification of risk framework has been applied to automated vehicles descriptively for years, and a recent review states that whether amplification operates for them remains open [naiseh2025,kasperson1988].
- Source: "hazards interact with psychological, social, institutional, and cultural processes in ways that may amplify or attenuate public responses" (abstract)
- Action: Attach [kasperson1988] to 'The social amplification of risk framework' only, and leave [naiseh2025] on the 'remains open' clause (see id 52).
- Note: A 1988 paper cannot support claims about automated vehicles or a 'recent review'. It only supports the existence and definition of the framework. The joint citation as placed does not support the whole sentence.

**57. `sun2025`** (06_discussion)

- Sentence: Coverage spikes and turns negative after crashes [jelinski2021], sentiment shifts in response [penmetsa2021], and blame follows recognizable patterns [sun2025].
- Source: "Regarding the topic AV system, the public appeared to have difficulty in classifying AV levels, with the highest blame volume and most negative sentiments." (abstract, p. 1 (full text supplied by the author))
- Action: Revised to 'blame falls most heavily on the automated system'.

**59. `koopman2024`** (06_discussion)

- Sentence: The Cruise case shows how tightly these move together, since sustained coverage there reflected the company's information handling, permit suspension, and federal defect investigation as well as the injury event [koopman2024,cadmv2023,nhtsa2023pe].
- Source: "later revelations/clarifications that pedestrian dragging had been under-disclosed caused a furor" (p.14; timeline p.13 (DMV suspension order Oct. 24; NHTSA reports and 950-vehicle recall) (https://arxiv.org/pdf/2402.06046v3))
- Action: The Cruise case shows how tightly these move together, since the episode combined the injury event with the company's information handling, a permit suspension, and a federal defect investigation [koopman2024,cadmv2023,nhtsa2023pe]; or keep 'sustained coverage reflected' only if the paper's own coverage data show it.
- Note: Koopman documents the information handling (non-disclosure of the dragging to the DMV, NHTSA and the media), the DMV permit suspension, and the NHTSA reports and recall. It also notes the 'fear of triggering a negative media cycle'. It does not analyze news coverage, so the claim that sustained coverage 'reflected' these factors is an inference that none of the three sources appears to measure. The defect investigation itself would come from nhtsa2023pe, which was not checked here.

**62. `kusano2025`** (06_discussion)

- Sentence: The differential should also be read against the reported safety profile of automated vehicles, for which operator studies report a 79 percent reduction in injury crashes over 56.7 million rider-only miles [kusano2025].
- Source: "statistically significant reductions in Any-Injury-Reported and Airbag Deployment outcomes when considered in all locations combined (79% CI: [71%, 85%]" (Discussion, p.21 of arXiv:2505.01515v1 (https://arxiv.org/pdf/2505.01515v1); also p.43: 'a 79% reduction in Any-Injury-Reported (72% to 86% 95% confidence interval)')
- Action: The differential should also be read against the reported safety profile of automated vehicles; an operator study of Waymo's rider-only service reports a 79 percent reduction in injury crashes over 56.7 million rider-only miles [kusano2025].
- Note: The numbers are correct: 79% fewer Any-Injury-Reported crashes over 56.7 million rider-only miles through January 2025, read in the arXiv preprint (the T&F journal version returned 403). It is PARTLY because the sentence generalizes one Waymo-authored study of one operator to 'automated vehicles' and to 'operator studies' (plural). 'Injury crashes' means any-injury-reported crashed-vehicle rates. The preprint gives two slightly different CIs for the 79% figure ([71%, 85%] on p.21 and 72%-86% on p.43); the author may want to check which one the journal version uses. If other operator studies are meant, cite them to justify the plural.

**70. `cadmv2023`** (06_discussion)

- Sentence: A horizon of about 90 days is the planning figure these data support for a robotaxi crash that reaches the news, conditional on that coverage and partly produced by the regulatory action itself, as the Cruise case shows [cadmv2023,nhtsa2023pe].
- Source: "the immediate suspension of Cruise LLC's deployment and driverless testing permits" (https://www.dmv.ca.gov/portal/news-and-media/dmv-statement-on-cruise-llc-suspension/)
- Action: ... conditional on that coverage and partly produced by the regulatory action itself, as in the Cruise case, where a permit suspension and a federal investigation followed the crash [cadmv2023,nhtsa2023pe].
- Note: The source documents the regulatory action only; that this action produced coverage, and the 90-day horizon, come from the authors' data. Rephrase so the citation attaches to the regulatory facts.

**71. `nhtsa2023pe`** (06_discussion)

- Sentence: A horizon of about 90 days is the planning figure these data support for a robotaxi crash that reaches the news, conditional on that coverage and partly produced by the regulatory action itself, as the Cruise case shows [cadmv2023,nhtsa2023pe].
- Source: "Date Opened: 10/16/2023 ... Action: A Preliminary Evaluation (PE) has been opened." (ODI Resume PE23018, p.1)
- Action: Same as id 70.
- Note: Documents the federal investigation only; not evidence that regulatory action generated coverage.

## Supported (50)

**1. `shariff2017`** (01_introduction)

- Sentence: Research on automated-vehicle adoption expects the public to overreact to automated-vehicle crashes [shariff2017], and media research describes such crashes as scandalized events [jelinski2021], yet few studies have quantified how much more coverage they receive.
- Source: "We discuss three: ethical dilemmas, overreactions to accidents, and the opacity of the cars' decision-making algorithms" (abstract (HAL record hal-04947166 via api.archives-ouvertes.fr))
- Note: Full text blocked (HAL bot wall, MIT DSpace 429, Nature paywall); the abstract names overreaction to accidents as a roadblock to adoption, which matches the citing clause.

**2. `jelinski2021`** (01_introduction)

- Sentence: Research on automated-vehicle adoption expects the public to overreact to automated-vehicle crashes [shariff2017], and media research describes such crashes as scandalized events [jelinski2021], yet few studies have quantified how much more coverage they receive.
- Source: "Undifferentiated optimism and scandalized accidents: the media coverage of autonomous driving in Germany" (title; see also p.5: 'scandalization, for example in the case of accidents, may decrease acceptance')
- Note: 'Scandalized accidents' is the paper's own framing (title). The p.5 scandalization remark is a literature claim (Grunwald 2015; Fleischer and Schippl 2018) that the paper then tests.

**3. `naiseh2025`** (01_introduction)

- Sentence: A recent review of trust and risk perception in automated vehicles notes that the field may need to examine whether social amplification operates for automated vehicles at all [naiseh2025].
- Source: "the AV research community may need to further examine whether social amplification exists in AV and propose potential methods and approaches to mitigate it" (https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11968569/fullTextXML (PMC11968569), section 'Theoretical implications')
- Note: Excerpt is 25 words. 'at all' is the manuscript's emphasis, not the source's wording, but the meaning is the same. It is a bibliometric review (Web of Science), so 'review' is accurate.

**5. `penmetsa2021`** (01_introduction)

- Sentence: Studies of automated-vehicle crash coverage show that crashes drive volume and sentiment within automated-vehicle discourse [jelinski2021,penmetsa2021], but disproportionate implies a comparator, and none of that work has one.
- Source: "the negative tweets on “self-driving/autonomous” technology increased by 32 percentage points (from 14% to 46%)" (abstract)
- Note: Supports the sentiment half only; volume comes from jelinski2021, so the pair supports the sentence jointly. Minor: penmetsa2021 studies tweets (public reaction), not news 'coverage', so 'studies of AV crash coverage' is slightly loose for this source.

**7. `cadmv2023`** (01_introduction)

- Sentence: Within weeks of the October 2023 crash, an operator's permits were suspended and a federal defect investigation was opened [cadmv2023,nhtsa2023pe].
- Source: "the immediate suspension of Cruise LLC's deployment and driverless testing permits" (https://www.dmv.ca.gov/portal/news-and-media/dmv-statement-on-cruise-llc-suspension/ (statement dated 24 Oct 2023))
- Note: Suspension dated 24 Oct 2023, 22 days after the 2 Oct crash, so 'within weeks' holds. The statement itself does not mention the 2 Oct crash; the link to the crash rests on timing (and koopman2024). Jointly with nhtsa2023pe the sentence is supported.

**8. `nhtsa2023pe`** (01_introduction)

- Sentence: Within weeks of the October 2023 crash, an operator's permits were suspended and a federal defect investigation was opened [cadmv2023,nhtsa2023pe].
- Source: "Date Opened: 10/16/2023 ... Action: A Preliminary Evaluation (PE) has been opened." (ODI Resume PE23018, p.1 (https://static.nhtsa.gov/odi/inv/2023/INOA-PE23018-11587.pdf))
- Note: PE opened 16 Oct 2023 (14 days after the crash); manufacturer Cruise LLC, subject ADS, prompted by 'SGO and social media reports' of pedestrian incidents. An ODI Preliminary Evaluation is a defect investigation, so 'federal defect investigation' is accurate.

**11. `slovic1987`** (02_literature)

- Sentence: The psychometric tradition explains why some hazards amplify readily, since people judge risks that are dreaded, involuntary, unfamiliar and poorly understood as more serious than statistically larger risks [slovic1987].
- Source: "their judgments of "risk" are related more to other hazard characteristics (for example, catastrophic potential, threat to future generations)" (p. 283 (Revealed and Expressed Preferences); factor definitions p. 283 (Factor-Analytic Representations); Fig. 1 p. 282)
- Note: Factor 1 'dread risk' includes uncontrollable, dread, catastrophic, fatal, inequitable and involuntary (Fig. 1). Factor 2 'unknown risk' covers 'unobservable, unknown, new, and delayed'. A higher dread score means higher perceived risk. Lay risk judgments 'differ from their own (and experts') estimates of annual fatalities', which supports 'more serious than statistically larger risks'. Read from a scanned copy (fbaum.unc.edu).

**13. `naiseh2025`** (02_literature)

- Sentence: After three decades of empirical work, its originators note how much of the amplification literature remains conceptual [kasperson2022sarf], and a recent review of automated-vehicle risk perception asks whether social amplification operates for automated vehicles at all [naiseh2025].
- Source: "the AV research community may need to further examine whether social amplification exists in AV" (https://www.ebi.ac.uk/europepmc/webservices/rest/PMC11968569/fullTextXML (PMC11968569), section 'Theoretical implications')
- Note: Same passage as id 3. 'asks whether... at all' paraphrases 'may need to further examine whether social amplification exists in AV'.

**15. `penmetsa2021`** (02_literature)

- Sentence: On social media, sentiment shifted measurably across roughly 1.7 million posts after the 2018 Uber and Tesla crashes [penmetsa2021], and blame follows recognizable patterns when an automated vehicle crashes [sun2025].
- Source: "Over 1.7 million tweets were found within 15 days before and after the incidents" (abstract)
- Note: Numbers check: 'over 1.7 million' tweets, 15 days before and after the March 2018 Uber pedestrian crash and Tesla Model X crash. Sentiment shift is reported (negative share 14% to 46%). 'Posts' = tweets (Twitter only).

**17. `penmetsa2023news`** (02_literature)

- Sentence: More than 1.7 million automated-driving news articles published between 2015 and 2021 show headline negativity rising sharply in the year of those two fatal crashes [penmetsa2023news], without attaching articles to individual crashes or to a human-driven comparison group.
- Source: "The number of negative sentiments in the title of articles published on the web in 2018 increased 12 times compared to the previous year." (abstract)
- Note: Numbers check: 'Over 1.7 million articles were collected ... published between May 1, 2015 to May 24, 2021' (abstract). One caveat: 1.7 million is the number collected, and the analysis ran on 'cleaned data' whose size is not given in the abstract. The 'without attaching articles to individual crashes or to a human-driven comparison group' clause is the authors' description of what the study lacks. It fits the abstract (year-level sentiment by keyword), but the full text (ScienceDirect, 403) was not checked. Also note that the '12 times' figure is a count of negative titles, not a share of titles. 2018 also had the most articles, so 'headline negativity rising sharply' may mix volume with tone. A safer wording is 'the number of negative headlines rising twelvefold in the year of those two fatal crashes'.

**20. `robertson2023negativity`** (02_literature)

- Sentence: Negative information about automated vehicles moves stated willingness to ride more than positive information does [anania2018], and the appetite for negative news is general, since in about 105,000 randomized headline variants each additional negative word raised the click-through rate [robertson2023negativity].
- Source: "For a headline of average length, each additional negative word increased the click-through rate by 2.3%." (abstract)
- Note: Numbers check: ' 105,000 different variations of news stories from Upworthy.com', 'a series of randomized controlled trials (N = 22,743)'. 'Randomized headline variants' is accurate.

**21. `connor2004`** (02_literature)

- Sentence: In four Midwestern cities only about one third of fatal crashes in federal records appeared in local newspapers [connor2004], and of 12,987 police-reported fatal crashes in Japan the two largest-circulation titles carried 45 and 22 percent [ichikawa2025news].
- Source: "Papers covered 278 fatal crashes over the two year period, in contrast to 846 fatal crashes documented in FARS." (abstract (Results))
- Note: 278/846 = 32.9%, so 'about one third' is correct. FARS is NHTSA's federal Fatality Analysis Reporting System; four Midwestern cities, 1999-2000.

**22. `ichikawa2025news`** (02_literature)

- Sentence: In four Midwestern cities only about one third of fatal crashes in federal records appeared in local newspapers [connor2004], and of 12,987 police-reported fatal crashes in Japan the two largest-circulation titles carried 45 and 22 percent [ichikawa2025news].
- Source: "Of 12,987 police-reported fatal crashes, 5,888 (45%) and 2,909 (22%) crashes were reported in Yomiuri and Asahi newspapers, respectively." (abstract (Results))
- Note: Source says 'the two best-selling newspapers', which matches 'largest-circulation'. Period Jan 2016 to Dec 2020.

**23. `ralph2019`** (02_literature)

- Sentence: Where coverage occurs, pedestrian and bicyclist crashes are routinely framed to foreground the victim's behavior [ralph2019], and randomizing the framing of a single crash shifts both attributed blame and preferred countermeasures [goddard2019news].
- Source: "The results reveal that local news coverage tends to shift blame toward VRUs and away from drivers." (abstract)
- Note: Content analysis of 200 local news articles on crashes involving people walking or biking. 'Routinely' is slightly stronger than 'tends to' but acceptable.

**24. `goddard2019news`** (02_literature)

- Sentence: Where coverage occurs, pedestrian and bicyclist crashes are routinely framed to foreground the victim's behavior [ralph2019], and randomizing the framing of a single crash shifts both attributed blame and preferred countermeasures [goddard2019news].
- Source: "even relatively subtle differences in editorial patterns significantly affected readers' interpretation of both what happened and what to do about it" (abstract)
- Note: 999 subjects were randomly assigned one of three versions of an article about a single pedestrian crash. Both blame and support for countermeasures shifted (a thematic frame raised support for infrastructure improvements).

**25. `gruenewald2009race`** (02_literature)

- Sentence: [gruenewald2009race] linked 664 Newark homicides to newspaper coverage and modeled both whether an incident was covered and how many articles it received.
- Source: "Overall, the data consisted of 664 homicide incidents that occurred from January 1, 1997 to December 31, 2005." (Data and methods (full text supplied by the author))
- Note: Logistic regression for covered or not, negative binomial regression for the number of articles.

**26. `scourfield2019reports`** (02_literature)

- Sentence: [scourfield2019reports] fitted negative binomial models to the number of reports about young people's deaths, with road traffic deaths as one of two death types.
- Source: "To determine which features of cases resulted in a higher count of reporting, negative binomial regression was used." (p. 513 (Method, Analysis); p. 514 (four models, DV = number of reports within a peak period))
- Note: Four NB models (Twitter and newspapers x suicides and RTAs). The DV is the number of reports within a 48-hour peak period. Deaths were of 11-18-year-olds in England; reports came from all UK publications. Sample: 81 suicides and 68 RTAs.

**28. `wu2007novelty`** (02_literature)

- Sentence: Collective attention to a news item decays over a characteristic time scale [wu2007novelty], attention to cultural products decays in two phases rather than one [candia2019decay], and successive topics hold attention for steadily shorter periods [lorenzspreen2019accelerating].
- Source: "novelty within groups decays with a stretched-exponential law, suggesting the existence of a natural time scale over which attention fades." (abstract)
- Note: Data are digg.com news stories, so 'news item' fits.

**29. `candia2019decay`** (02_literature)

- Sentence: Collective attention to a news item decays over a characteristic time scale [wu2007novelty], attention to cultural products decays in two phases rather than one [candia2019decay], and successive topics hold attention for steadily shorter periods [lorenzspreen2019accelerating].
- Source: "the average attention received by cultural products decays following a universal biexponential function" (abstract (via Europe PMC record))
- Note: Biexponential = two phases (communicative and cultural memory); domains are papers, patents, songs, movies, biographies, so 'cultural products' is the source's own term.

**30. `lorenzspreen2019accelerating`** (02_literature)

- Sentence: Collective attention to a news item decays over a characteristic time scale [wu2007novelty], attention to cultural products decays in two phases rather than one [candia2019decay], and successive topics hold attention for steadily shorter periods [lorenzspreen2019accelerating].
- Source: "this causes growing turnover rates and individual topics receiving shorter intervals of collective attention." (abstract)
- Note: Abstract also reports 'shortened periods in the trajectories' across multi-decade datasets.

**32. `vandermeer2022news`** (02_literature)

- Sentence: Across two decades of United States coverage, attention to aviation and road accidents grew out of proportion to accident trends [vandermeer2022news], which compares aggregate attention with aggregate exposure rather than coverage per crash.
- Source: "Negative incidents—i.e., both aviation and road accidents—become more prominent in the news over time, rather than accurately reflecting real-world trends." (abstract)
- Note: Time series 1996-2017 (22 years, so 'two decades' is fine) of US media attention compared with travel-behavior and fatal-accident data. That supports the 'aggregate attention vs aggregate exposure' description.

**34. `nhtsa2022sgo`** (02_literature)

- Sentence: Of 130 automated driving system crashes in the first reporting period of the Standing General Order of the National Highway Traffic Safety Administration (NHTSA), 108 involved no reported injury [nhtsa2022sgo].
- Source: "108 of the specified crashes had no reported injuries." (ADS Highest Injury Severity (report supplied by the author))
- Note: Same page: 130 ADS crashes reported from July 2021 to May 15, 2022.

**38. `jelinski2021`** (02_literature)

- Sentence: \begin{table}[pos=!htbp] \caption{Nearest Prior Work and the Coverage Properties It Measures} \label{tab:gap} \tblbody{\footnotesize\setlength{\tabcolsep}{4pt} \begin{tabular}{l l ccccc} \toprule & & \multicolumn{2}{c}{Design} & \multicolumn{3}{c}{Coverage outputs} \\ \cmidrule(lr){3-4}\cmidrule(lr){5-7} Study & Domain (scale) & Unit & Comparator & Volume & Persist. & Outlets \\ \midrule [jelinski2021] & AV news, Germany (5 papers) & \noglyph & \halfglyph & \halfglyph & \noglyph & \noglyph \\ [penmetsa2023news] & AV news (1.7M articles) & \noglyph & \noglyph & \halfglyph & \noglyph & \noglyph \\ [penmetsa2021] & AV crash posts (social media) & \halfglyph & \noglyph & \noglyph & \noglyph & \noglyph \\ [connor2004] & Fatal crash news, U.S. (4 cities) & \yesglyph & \noglyph & \halfglyph & \noglyph & \noglyph \\ [ichikawa2025news] & Fatal crash news, Japan (12,987) & \yesglyph & \noglyph & \halfglyph & \noglyph & \noglyph \\ [gruenewald2009race] & Homicide news, Newark (664) & \yesglyph & \halfglyph & \yesglyph & \noglyph & \noglyph \\ [scourfield2019reports] & Youth death news, U.K. & \yesglyph & \halfglyph & \yesglyph & \noglyph & \noglyph \\ [vandermeer2022news] & Aviation vs.\ road news (1996--2017) & \noglyph & \halfglyph & \halfglyph & \noglyph & \noglyph \\ [garciagavilanes2016] & Air crash attention (Wikipedia) & \yesglyph & \noglyph & \halfglyph & \halfglyph & \noglyph \\ [candia2019decay] & Collective attention (multi-domain) & \halfglyph & \noglyph & \noglyph & \halfglyph & \noglyph \\ \midrule \multicolumn{2}{l}{\emph{Prior studies meeting each criterion fully or partly, of 10}} & 7 & 4 & 8 & 2 & 0 \\ \midrule \textbf{This study} & Robotaxi vs.\ human crashes (51 vs.\ 746) & \yesglyph & \halfglyph & \yesglyph & \yesglyph & \halfglyph \\ \bottomrule \end{tabular}} \tblnote{\yesglyph{} full, \halfglyph{} partial, \noglyph{} absent.
- Source: "routinely published articles were distinguished from those that appeared within 14 days after an accident" (Method, p.8 (https://jcom.sissa.it/archive/20/04/JCOM_2004_2021_A02.pdf))
- Note: Table row is defensible. 'AV news, Germany (5 papers)' is correct. Unit absent (article level, not crash level). Comparator partial (regular vs. 14-day post-accident window, no human-crash group). Volume partial (descriptive monthly counts, Fig. 1). Persistence absent: the paper's only decay remark is about level of detail ('vanishes shortly after the event', p.12), not volume.

**39. `penmetsa2023news`** (02_literature)

- Sentence: \begin{table}[pos=!htbp] \caption{Nearest Prior Work and the Coverage Properties It Measures} \label{tab:gap} \tblbody{\footnotesize\setlength{\tabcolsep}{4pt} \begin{tabular}{l l ccccc} \toprule & & \multicolumn{2}{c}{Design} & \multicolumn{3}{c}{Coverage outputs} \\ \cmidrule(lr){3-4}\cmidrule(lr){5-7} Study & Domain (scale) & Unit & Comparator & Volume & Persist. & Outlets \\ \midrule [jelinski2021] & AV news, Germany (5 papers) & \noglyph & \halfglyph & \halfglyph & \noglyph & \noglyph \\ [penmetsa2023news] & AV news (1.7M articles) & \noglyph & \noglyph & \halfglyph & \noglyph & \noglyph \\ [penmetsa2021] & AV crash posts (social media) & \halfglyph & \noglyph & \noglyph & \noglyph & \noglyph \\ [connor2004] & Fatal crash news, U.S. (4 cities) & \yesglyph & \noglyph & \halfglyph & \noglyph & \noglyph \\ [ichikawa2025news] & Fatal crash news, Japan (12,987) & \yesglyph & \noglyph & \halfglyph & \noglyph & \noglyph \\ [gruenewald2009race] & Homicide news, Newark (664) & \yesglyph & \halfglyph & \yesglyph & \noglyph & \noglyph \\ [scourfield2019reports] & Youth death news, U.K. & \yesglyph & \halfglyph & \yesglyph & \noglyph & \noglyph \\ [vandermeer2022news] & Aviation vs.\ road news (1996--2017) & \noglyph & \halfglyph & \halfglyph & \noglyph & \noglyph \\ [garciagavilanes2016] & Air crash attention (Wikipedia) & \yesglyph & \noglyph & \halfglyph & \halfglyph & \noglyph \\ [candia2019decay] & Collective attention (multi-domain) & \halfglyph & \noglyph & \noglyph & \halfglyph & \noglyph \\ \midrule \multicolumn{2}{l}{\emph{Prior studies meeting each criterion fully or partly, of 10}} & 7 & 4 & 8 & 2 & 0 \\ \midrule \textbf{This study} & Robotaxi vs.\ human crashes (51 vs.\ 746) & \yesglyph & \halfglyph & \yesglyph & \yesglyph & \halfglyph \\ \bottomrule \end{tabular}} \tblnote{\yesglyph{} full, \halfglyph{} partial, \noglyph{} absent.
- Source: "Over 1.7 million articles were collected on the keywords for relevant articles published between May 1, 2015 to May 24, 2021." (abstract)
- Note: 'AV news (1.7M articles)' and the partial Volume rating ('2018 recorded the highest number of news articles') are fine. Minor flag: the abstract makes a coarse persistence claim ('The negativity induced in 2018 in the news media did not continue in the next year ... short term effects'). The authors may want Persist. = \halfglyph, which would change the column count from 2 to 3. Absent is defensible if Persist. means decay after an individual crash.

**40. `penmetsa2021`** (02_literature)

- Sentence: \begin{table}[pos=!htbp] \caption{Nearest Prior Work and the Coverage Properties It Measures} \label{tab:gap} \tblbody{\footnotesize\setlength{\tabcolsep}{4pt} \begin{tabular}{l l ccccc} \toprule & & \multicolumn{2}{c}{Design} & \multicolumn{3}{c}{Coverage outputs} \\ \cmidrule(lr){3-4}\cmidrule(lr){5-7} Study & Domain (scale) & Unit & Comparator & Volume & Persist. & Outlets \\ \midrule [jelinski2021] & AV news, Germany (5 papers) & \noglyph & \halfglyph & \halfglyph & \noglyph & \noglyph \\ [penmetsa2023news] & AV news (1.7M articles) & \noglyph & \noglyph & \halfglyph & \noglyph & \noglyph \\ [penmetsa2021] & AV crash posts (social media) & \halfglyph & \noglyph & \noglyph & \noglyph & \noglyph \\ [connor2004] & Fatal crash news, U.S. (4 cities) & \yesglyph & \noglyph & \halfglyph & \noglyph & \noglyph \\ [ichikawa2025news] & Fatal crash news, Japan (12,987) & \yesglyph & \noglyph & \halfglyph & \noglyph & \noglyph \\ [gruenewald2009race] & Homicide news, Newark (664) & \yesglyph & \halfglyph & \yesglyph & \noglyph & \noglyph \\ [scourfield2019reports] & Youth death news, U.K. & \yesglyph & \halfglyph & \yesglyph & \noglyph & \noglyph \\ [vandermeer2022news] & Aviation vs.\ road news (1996--2017) & \noglyph & \halfglyph & \halfglyph & \noglyph & \noglyph \\ [garciagavilanes2016] & Air crash attention (Wikipedia) & \yesglyph & \noglyph & \halfglyph & \halfglyph & \noglyph \\ [candia2019decay] & Collective attention (multi-domain) & \halfglyph & \noglyph & \noglyph & \halfglyph & \noglyph \\ \midrule \multicolumn{2}{l}{\emph{Prior studies meeting each criterion fully or partly, of 10}} & 7 & 4 & 8 & 2 & 0 \\ \midrule \textbf{This study} & Robotaxi vs.\ human crashes (51 vs.\ 746) & \yesglyph & \halfglyph & \yesglyph & \yesglyph & \halfglyph \\ \bottomrule \end{tabular}} \tblnote{\yesglyph{} full, \halfglyph{} partial, \noglyph{} absent.
- Source: "before-and-after sentiment analysis to examine how these two fatal crashes have affected people's perceptions" (abstract)
- Note: Table row is defensible: two specific crashes give a partial crash unit. There is no human comparator. Volume is not reported as an outcome (sentiment shares only).

**41. `connor2004`** (02_literature)

- Sentence: \begin{table}[pos=!htbp] \caption{Nearest Prior Work and the Coverage Properties It Measures} \label{tab:gap} \tblbody{\footnotesize\setlength{\tabcolsep}{4pt} \begin{tabular}{l l ccccc} \toprule & & \multicolumn{2}{c}{Design} & \multicolumn{3}{c}{Coverage outputs} \\ \cmidrule(lr){3-4}\cmidrule(lr){5-7} Study & Domain (scale) & Unit & Comparator & Volume & Persist. & Outlets \\ \midrule [jelinski2021] & AV news, Germany (5 papers) & \noglyph & \halfglyph & \halfglyph & \noglyph & \noglyph \\ [penmetsa2023news] & AV news (1.7M articles) & \noglyph & \noglyph & \halfglyph & \noglyph & \noglyph \\ [penmetsa2021] & AV crash posts (social media) & \halfglyph & \noglyph & \noglyph & \noglyph & \noglyph \\ [connor2004] & Fatal crash news, U.S. (4 cities) & \yesglyph & \noglyph & \halfglyph & \noglyph & \noglyph \\ [ichikawa2025news] & Fatal crash news, Japan (12,987) & \yesglyph & \noglyph & \halfglyph & \noglyph & \noglyph \\ [gruenewald2009race] & Homicide news, Newark (664) & \yesglyph & \halfglyph & \yesglyph & \noglyph & \noglyph \\ [scourfield2019reports] & Youth death news, U.K. & \yesglyph & \halfglyph & \yesglyph & \noglyph & \noglyph \\ [vandermeer2022news] & Aviation vs.\ road news (1996--2017) & \noglyph & \halfglyph & \halfglyph & \noglyph & \noglyph \\ [garciagavilanes2016] & Air crash attention (Wikipedia) & \yesglyph & \noglyph & \halfglyph & \halfglyph & \noglyph \\ [candia2019decay] & Collective attention (multi-domain) & \halfglyph & \noglyph & \noglyph & \halfglyph & \noglyph \\ \midrule \multicolumn{2}{l}{\emph{Prior studies meeting each criterion fully or partly, of 10}} & 7 & 4 & 8 & 2 & 0 \\ \midrule \textbf{This study} & Robotaxi vs.\ human crashes (51 vs.\ 746) & \yesglyph & \halfglyph & \yesglyph & \yesglyph & \halfglyph \\ \bottomrule \end{tabular}} \tblnote{\yesglyph{} full, \halfglyph{} partial, \noglyph{} absent.
- Source: "Crash details were extracted from two years of newspaper coverage of fatal crashes in four Midwestern cities in the United States." (abstract (Methods))
- Note: Table 1 row 'Fatal crash news, U.S. (4 cities)' is accurate. Unit = crash compared with FARS (full) is reasonable; Volume is partial because the study records coverage yes/no only.

**42. `ichikawa2025news`** (02_literature)

- Sentence: \begin{table}[pos=!htbp] \caption{Nearest Prior Work and the Coverage Properties It Measures} \label{tab:gap} \tblbody{\footnotesize\setlength{\tabcolsep}{4pt} \begin{tabular}{l l ccccc} \toprule & & \multicolumn{2}{c}{Design} & \multicolumn{3}{c}{Coverage outputs} \\ \cmidrule(lr){3-4}\cmidrule(lr){5-7} Study & Domain (scale) & Unit & Comparator & Volume & Persist. & Outlets \\ \midrule [jelinski2021] & AV news, Germany (5 papers) & \noglyph & \halfglyph & \halfglyph & \noglyph & \noglyph \\ [penmetsa2023news] & AV news (1.7M articles) & \noglyph & \noglyph & \halfglyph & \noglyph & \noglyph \\ [penmetsa2021] & AV crash posts (social media) & \halfglyph & \noglyph & \noglyph & \noglyph & \noglyph \\ [connor2004] & Fatal crash news, U.S. (4 cities) & \yesglyph & \noglyph & \halfglyph & \noglyph & \noglyph \\ [ichikawa2025news] & Fatal crash news, Japan (12,987) & \yesglyph & \noglyph & \halfglyph & \noglyph & \noglyph \\ [gruenewald2009race] & Homicide news, Newark (664) & \yesglyph & \halfglyph & \yesglyph & \noglyph & \noglyph \\ [scourfield2019reports] & Youth death news, U.K. & \yesglyph & \halfglyph & \yesglyph & \noglyph & \noglyph \\ [vandermeer2022news] & Aviation vs.\ road news (1996--2017) & \noglyph & \halfglyph & \halfglyph & \noglyph & \noglyph \\ [garciagavilanes2016] & Air crash attention (Wikipedia) & \yesglyph & \noglyph & \halfglyph & \halfglyph & \noglyph \\ [candia2019decay] & Collective attention (multi-domain) & \halfglyph & \noglyph & \noglyph & \halfglyph & \noglyph \\ \midrule \multicolumn{2}{l}{\emph{Prior studies meeting each criterion fully or partly, of 10}} & 7 & 4 & 8 & 2 & 0 \\ \midrule \textbf{This study} & Robotaxi vs.\ human crashes (51 vs.\ 746) & \yesglyph & \halfglyph & \yesglyph & \yesglyph & \halfglyph \\ \bottomrule \end{tabular}} \tblnote{\yesglyph{} full, \halfglyph{} partial, \noglyph{} absent.
- Source: "Of 12,987 police-reported fatal crashes, 5,888 (45%) and 2,909 (22%) crashes were reported" (abstract)
- Note: Table 1 row 'Fatal crash news, Japan (12,987)' is accurate.

**43. `gruenewald2009race`** (02_literature)

- Sentence: \begin{table}[pos=!htbp] \caption{Nearest Prior Work and the Coverage Properties It Measures} \label{tab:gap} \tblbody{\footnotesize\setlength{\tabcolsep}{4pt} \begin{tabular}{l l ccccc} \toprule & & \multicolumn{2}{c}{Design} & \multicolumn{3}{c}{Coverage outputs} \\ \cmidrule(lr){3-4}\cmidrule(lr){5-7} Study & Domain (scale) & Unit & Comparator & Volume & Persist. & Outlets \\ \midrule [jelinski2021] & AV news, Germany (5 papers) & \noglyph & \halfglyph & \halfglyph & \noglyph & \noglyph \\ [penmetsa2023news] & AV news (1.7M articles) & \noglyph & \noglyph & \halfglyph & \noglyph & \noglyph \\ [penmetsa2021] & AV crash posts (social media) & \halfglyph & \noglyph & \noglyph & \noglyph & \noglyph \\ [connor2004] & Fatal crash news, U.S. (4 cities) & \yesglyph & \noglyph & \halfglyph & \noglyph & \noglyph \\ [ichikawa2025news] & Fatal crash news, Japan (12,987) & \yesglyph & \noglyph & \halfglyph & \noglyph & \noglyph \\ [gruenewald2009race] & Homicide news, Newark (664) & \yesglyph & \halfglyph & \yesglyph & \noglyph & \noglyph \\ [scourfield2019reports] & Youth death news, U.K. & \yesglyph & \halfglyph & \yesglyph & \noglyph & \noglyph \\ [vandermeer2022news] & Aviation vs.\ road news (1996--2017) & \noglyph & \halfglyph & \halfglyph & \noglyph & \noglyph \\ [garciagavilanes2016] & Air crash attention (Wikipedia) & \yesglyph & \noglyph & \halfglyph & \halfglyph & \noglyph \\ [candia2019decay] & Collective attention (multi-domain) & \halfglyph & \noglyph & \noglyph & \halfglyph & \noglyph \\ \midrule \multicolumn{2}{l}{\emph{Prior studies meeting each criterion fully or partly, of 10}} & 7 & 4 & 8 & 2 & 0 \\ \midrule \textbf{This study} & Robotaxi vs.\ human crashes (51 vs.\ 746) & \yesglyph & \halfglyph & \yesglyph & \yesglyph & \halfglyph \\ \bottomrule \end{tabular}} \tblnote{\yesglyph{} full, \halfglyph{} partial, \noglyph{} absent.
- Source: "Negative binomial regression was used to examine the effects of the homicide variables on the continuous dependent variable, number of specific articles." (Findings (full text supplied by the author))
- Note: Confirms the full Volume mark and the (664) in Table 1.

**44. `scourfield2019reports`** (02_literature)

- Sentence: \begin{table}[pos=!htbp] \caption{Nearest Prior Work and the Coverage Properties It Measures} \label{tab:gap} \tblbody{\footnotesize\setlength{\tabcolsep}{4pt} \begin{tabular}{l l ccccc} \toprule & & \multicolumn{2}{c}{Design} & \multicolumn{3}{c}{Coverage outputs} \\ \cmidrule(lr){3-4}\cmidrule(lr){5-7} Study & Domain (scale) & Unit & Comparator & Volume & Persist. & Outlets \\ \midrule [jelinski2021] & AV news, Germany (5 papers) & \noglyph & \halfglyph & \halfglyph & \noglyph & \noglyph \\ [penmetsa2023news] & AV news (1.7M articles) & \noglyph & \noglyph & \halfglyph & \noglyph & \noglyph \\ [penmetsa2021] & AV crash posts (social media) & \halfglyph & \noglyph & \noglyph & \noglyph & \noglyph \\ [connor2004] & Fatal crash news, U.S. (4 cities) & \yesglyph & \noglyph & \halfglyph & \noglyph & \noglyph \\ [ichikawa2025news] & Fatal crash news, Japan (12,987) & \yesglyph & \noglyph & \halfglyph & \noglyph & \noglyph \\ [gruenewald2009race] & Homicide news, Newark (664) & \yesglyph & \halfglyph & \yesglyph & \noglyph & \noglyph \\ [scourfield2019reports] & Youth death news, U.K. & \yesglyph & \halfglyph & \yesglyph & \noglyph & \noglyph \\ [vandermeer2022news] & Aviation vs.\ road news (1996--2017) & \noglyph & \halfglyph & \halfglyph & \noglyph & \noglyph \\ [garciagavilanes2016] & Air crash attention (Wikipedia) & \yesglyph & \noglyph & \halfglyph & \halfglyph & \noglyph \\ [candia2019decay] & Collective attention (multi-domain) & \halfglyph & \noglyph & \noglyph & \halfglyph & \noglyph \\ \midrule \multicolumn{2}{l}{\emph{Prior studies meeting each criterion fully or partly, of 10}} & 7 & 4 & 8 & 2 & 0 \\ \midrule \textbf{This study} & Robotaxi vs.\ human crashes (51 vs.\ 746) & \yesglyph & \halfglyph & \yesglyph & \yesglyph & \halfglyph \\ \bottomrule \end{tabular}} \tblnote{\yesglyph{} full, \halfglyph{} partial, \noglyph{} absent.
- Source: "any death by suicide or RTA of a young person aged 11–18 in England that was reported in a newspaper" (p. 510 (Method, Identifying Cases))
- Note: Table 1 row 'Youth death news, U.K.': the deaths were in England and reports came from all UK publications, so 'England' would be more precise. Volume = full is justified by the NB models of report counts.

**45. `vandermeer2022news`** (02_literature)

- Sentence: \begin{table}[pos=!htbp] \caption{Nearest Prior Work and the Coverage Properties It Measures} \label{tab:gap} \tblbody{\footnotesize\setlength{\tabcolsep}{4pt} \begin{tabular}{l l ccccc} \toprule & & \multicolumn{2}{c}{Design} & \multicolumn{3}{c}{Coverage outputs} \\ \cmidrule(lr){3-4}\cmidrule(lr){5-7} Study & Domain (scale) & Unit & Comparator & Volume & Persist. & Outlets \\ \midrule [jelinski2021] & AV news, Germany (5 papers) & \noglyph & \halfglyph & \halfglyph & \noglyph & \noglyph \\ [penmetsa2023news] & AV news (1.7M articles) & \noglyph & \noglyph & \halfglyph & \noglyph & \noglyph \\ [penmetsa2021] & AV crash posts (social media) & \halfglyph & \noglyph & \noglyph & \noglyph & \noglyph \\ [connor2004] & Fatal crash news, U.S. (4 cities) & \yesglyph & \noglyph & \halfglyph & \noglyph & \noglyph \\ [ichikawa2025news] & Fatal crash news, Japan (12,987) & \yesglyph & \noglyph & \halfglyph & \noglyph & \noglyph \\ [gruenewald2009race] & Homicide news, Newark (664) & \yesglyph & \halfglyph & \yesglyph & \noglyph & \noglyph \\ [scourfield2019reports] & Youth death news, U.K. & \yesglyph & \halfglyph & \yesglyph & \noglyph & \noglyph \\ [vandermeer2022news] & Aviation vs.\ road news (1996--2017) & \noglyph & \halfglyph & \halfglyph & \noglyph & \noglyph \\ [garciagavilanes2016] & Air crash attention (Wikipedia) & \yesglyph & \noglyph & \halfglyph & \halfglyph & \noglyph \\ [candia2019decay] & Collective attention (multi-domain) & \halfglyph & \noglyph & \noglyph & \halfglyph & \noglyph \\ \midrule \multicolumn{2}{l}{\emph{Prior studies meeting each criterion fully or partly, of 10}} & 7 & 4 & 8 & 2 & 0 \\ \midrule \textbf{This study} & Robotaxi vs.\ human crashes (51 vs.\ 746) & \yesglyph & \halfglyph & \yesglyph & \yesglyph & \halfglyph \\ \bottomrule \end{tabular}} \tblnote{\yesglyph{} full, \halfglyph{} partial, \noglyph{} absent.
- Source: "time-series analyses (1996–2017) on US media attention for aviation and road accidents" (abstract)
- Note: Table 1 row 'Aviation vs. road news (1996--2017)' is accurate. Unit = absent is correct (aggregate time series).

**46. `garciagavilanes2016`** (02_literature)

- Sentence: \begin{table}[pos=!htbp] \caption{Nearest Prior Work and the Coverage Properties It Measures} \label{tab:gap} \tblbody{\footnotesize\setlength{\tabcolsep}{4pt} \begin{tabular}{l l ccccc} \toprule & & \multicolumn{2}{c}{Design} & \multicolumn{3}{c}{Coverage outputs} \\ \cmidrule(lr){3-4}\cmidrule(lr){5-7} Study & Domain (scale) & Unit & Comparator & Volume & Persist. & Outlets \\ \midrule [jelinski2021] & AV news, Germany (5 papers) & \noglyph & \halfglyph & \halfglyph & \noglyph & \noglyph \\ [penmetsa2023news] & AV news (1.7M articles) & \noglyph & \noglyph & \halfglyph & \noglyph & \noglyph \\ [penmetsa2021] & AV crash posts (social media) & \halfglyph & \noglyph & \noglyph & \noglyph & \noglyph \\ [connor2004] & Fatal crash news, U.S. (4 cities) & \yesglyph & \noglyph & \halfglyph & \noglyph & \noglyph \\ [ichikawa2025news] & Fatal crash news, Japan (12,987) & \yesglyph & \noglyph & \halfglyph & \noglyph & \noglyph \\ [gruenewald2009race] & Homicide news, Newark (664) & \yesglyph & \halfglyph & \yesglyph & \noglyph & \noglyph \\ [scourfield2019reports] & Youth death news, U.K. & \yesglyph & \halfglyph & \yesglyph & \noglyph & \noglyph \\ [vandermeer2022news] & Aviation vs.\ road news (1996--2017) & \noglyph & \halfglyph & \halfglyph & \noglyph & \noglyph \\ [garciagavilanes2016] & Air crash attention (Wikipedia) & \yesglyph & \noglyph & \halfglyph & \halfglyph & \noglyph \\ [candia2019decay] & Collective attention (multi-domain) & \halfglyph & \noglyph & \noglyph & \halfglyph & \noglyph \\ \midrule \multicolumn{2}{l}{\emph{Prior studies meeting each criterion fully or partly, of 10}} & 7 & 4 & 8 & 2 & 0 \\ \midrule \textbf{This study} & Robotaxi vs.\ human crashes (51 vs.\ 746) & \yesglyph & \halfglyph & \yesglyph & \yesglyph & \halfglyph \\ \bottomrule \end{tabular}} \tblnote{\yesglyph{} full, \halfglyph{} partial, \noglyph{} absent.
- Source: "We study both the editorial activities on and the viewership of the articles about airline crashes." (abstract; section 2.3; Table 4)
- Note: Row 'Air crash attention (Wikipedia)': per-event unit (full), no comparator, volume partial (views/edits), persistence partial (decay modelled), no outlets - consistent with the paper. Ratings are author judgments.

**47. `candia2019decay`** (02_literature)

- Sentence: \begin{table}[pos=!htbp] \caption{Nearest Prior Work and the Coverage Properties It Measures} \label{tab:gap} \tblbody{\footnotesize\setlength{\tabcolsep}{4pt} \begin{tabular}{l l ccccc} \toprule & & \multicolumn{2}{c}{Design} & \multicolumn{3}{c}{Coverage outputs} \\ \cmidrule(lr){3-4}\cmidrule(lr){5-7} Study & Domain (scale) & Unit & Comparator & Volume & Persist. & Outlets \\ \midrule [jelinski2021] & AV news, Germany (5 papers) & \noglyph & \halfglyph & \halfglyph & \noglyph & \noglyph \\ [penmetsa2023news] & AV news (1.7M articles) & \noglyph & \noglyph & \halfglyph & \noglyph & \noglyph \\ [penmetsa2021] & AV crash posts (social media) & \halfglyph & \noglyph & \noglyph & \noglyph & \noglyph \\ [connor2004] & Fatal crash news, U.S. (4 cities) & \yesglyph & \noglyph & \halfglyph & \noglyph & \noglyph \\ [ichikawa2025news] & Fatal crash news, Japan (12,987) & \yesglyph & \noglyph & \halfglyph & \noglyph & \noglyph \\ [gruenewald2009race] & Homicide news, Newark (664) & \yesglyph & \halfglyph & \yesglyph & \noglyph & \noglyph \\ [scourfield2019reports] & Youth death news, U.K. & \yesglyph & \halfglyph & \yesglyph & \noglyph & \noglyph \\ [vandermeer2022news] & Aviation vs.\ road news (1996--2017) & \noglyph & \halfglyph & \halfglyph & \noglyph & \noglyph \\ [garciagavilanes2016] & Air crash attention (Wikipedia) & \yesglyph & \noglyph & \halfglyph & \halfglyph & \noglyph \\ [candia2019decay] & Collective attention (multi-domain) & \halfglyph & \noglyph & \noglyph & \halfglyph & \noglyph \\ \midrule \multicolumn{2}{l}{\emph{Prior studies meeting each criterion fully or partly, of 10}} & 7 & 4 & 8 & 2 & 0 \\ \midrule \textbf{This study} & Robotaxi vs.\ human crashes (51 vs.\ 746) & \yesglyph & \halfglyph & \yesglyph & \yesglyph & \halfglyph \\ \bottomrule \end{tabular}} \tblnote{\yesglyph{} full, \halfglyph{} partial, \noglyph{} absent.
- Source: "the average attention received by cultural products decays following a universal biexponential function" (abstract (Europe PMC))
- Note: Row 'Collective attention (multi-domain)' matches papers/patents/songs/movies/biographies; persistence partial fits a decay model. Ratings are author judgments.

**49. `connor2004`** (03_data)

- Sentence: Most fatal crashes never reach a newspaper, and only about a third of those in federal records appeared in the papers of the four cities studied by [connor2004].
- Source: "Papers covered 278 fatal crashes over the two year period, in contrast to 846 fatal crashes documented in FARS." (abstract)
- Note: 'About a third' is exact (32.9%). The opening generalization 'Most fatal crashes never reach a newspaper' is uncited and rests only on Connor's four cities. Ichikawa does not support it: 45% and 22% are per-paper figures, so the two papers together covered somewhere between 45% and 67%.

**50. `nhtsa2022sgo`** (03_data)

- Sentence: Crashes reported under the Standing General Order are overwhelmingly minor [nhtsa2022sgo], so the two corpora truncate their populations at different points.
- Source: "One crash resulted in serious injuries while most caused no injuries." (Scribd summary of DOT HS 813 324 (scribd.com/document/578451851); reporting threshold from report text in search snippets)
- Note: 'Overwhelmingly minor' holds on the report's property-damage-or-injury reporting threshold plus 'most caused no injuries'; the exact 108/130 split is unverified (see id 34).

**51. `cameron2013`** (04_method)

- Sentence: Poisson quasi-maximum-likelihood estimation is consistent for the conditional mean whatever the true variance function, which matters because the two margins are dispersed very differently, with robotaxi counts overdispersed at a variance-to-mean ratio of 65 and human counts mildly underdispersed at 0.87 [cameron2013].
- Source: "Consistency requires correct specification of the conditional mean. It does not require that the dependent variable y be Poisson distributed." (Ch. 3 'Basic Count Regression' (pp. 69-110), chapter summary item 1, Cambridge Core chapter abstract page)
- Note: Supports the QMLE consistency statement (textbook result). The dispersion ratios (65 and 0.87) are the paper's own sample statistics, not from Cameron and Trivedi. Consider moving [cameron2013] to right after 'whatever the true variance function' so the numbers are not read as cited. The full book text was not checked, so no exact page is given.

**54. `eisensee2007`** (06_discussion)

- Sentence: For crash types, the design produces the kind of exchange rate that disaster-relief work expressed between categories of victim [eisensee2007].
- Source: "for every person that dies in a volcano disaster, 38,920 people must die of food shortage to receive the same expected media coverage" (working-paper version p. 29; Table VIII ('Equal coverage casualties ratio'))
- Note: The paper calls this a 'casualties ratio', not an 'exchange rate'. The analogy is fair, but 'casualties ratio' would track the source more closely. Page numbers are from the working paper, not the QJE pagination.

**55. `jelinski2021`** (06_discussion)

- Sentence: Coverage spikes and turns negative after crashes [jelinski2021], sentiment shifts in response [penmetsa2021], and blame follows recognizable patterns [sun2025].
- Source: "In the direct aftermath (within 14 days) of an accident the overall tone is considerably more negative than during a regular period" (Results, p.11 (https://jcom.sissa.it/archive/20/04/JCOM_2004_2021_A02.pdf))
- Note: 'Spikes' rests on descriptive monthly peaks (p.8: 'can most probably be attributed to accidents'). Jelinski's Discussion says accidents 'increase the frequency and negativity of the coverage' (p.13), so plain 'spikes' is acceptable. See id 14 for 'sharply'.

**56. `penmetsa2021`** (06_discussion)

- Sentence: Coverage spikes and turns negative after crashes [jelinski2021], sentiment shifts in response [penmetsa2021], and blame follows recognizable patterns [sun2025].
- Source: "the negativity in the tweets and the percentage of negative tweets on self-driving/autonomous technology have increased after their involvement in fatal crashes" (abstract)

**58. `liu2019`** (06_discussion)

- Sentence: Our finding also mirrors, at the ecosystem level, an individual-level bias, since people judge an identical crash more severely when an automated vehicle is involved [liu2019].
- Source: "participants had a tendency to perceive traffic crashes involving SDVs to be more severe than those involving conventionally human-driven vehicles" (abstract (via Semantic Scholar API))
- Note: Vignette crashes differing only in vehicle type, across 'five vignette-based experiments in two studies (total N = 1267)'. The 'regardless of their severity... or cause' part supports 'identical crash'.

**60. `cadmv2023`** (06_discussion)

- Sentence: The Cruise case shows how tightly these move together, since sustained coverage there reflected the company's information handling, permit suspension, and federal defect investigation as well as the injury event [koopman2024,cadmv2023,nhtsa2023pe].
- Source: "has misrepresented any information related to safety of the autonomous technology of its vehicles" (https://www.dmv.ca.gov/portal/news-and-media/dmv-statement-on-cruise-llc-suspension/ (grounds for suspension))
- Note: Supports the permit suspension and, via the misrepresentation ground, information handling. That coverage 'reflected' these is the authors' reading of their corpus (with koopman2024).

**61. `nhtsa2023pe`** (06_discussion)

- Sentence: The Cruise case shows how tightly these move together, since sustained coverage there reflected the company's information handling, permit suspension, and federal defect investigation as well as the injury event [koopman2024,cadmv2023,nhtsa2023pe].
- Source: "Action: A Preliminary Evaluation (PE) has been opened." (ODI Resume PE23018, p.1)
- Note: Supports the federal defect investigation element.

**63. `stilgoe2018`** (06_discussion)

- Sentence: Media attention measures coverage supply, not crash risk, and disproportionate coverage does not in itself indicate poor journalism, since heightened scrutiny may be legitimate public learning about a new technology on public roads [stilgoe2018].
- Source: "Except in cases of total cover-up, accidents can force public reframing and institutional reflection." (https://discovery.ucl.ac.uk/id/eprint/10038434 (author accepted manuscript), p. 4 of AAM; also p. 21 'Accidents therefore provide a constructive opportunity for reframing.')
- Note: Stilgoe supports the claim that scrutiny after crashes can be legitimate public or social learning about a technology being tested on public roads. His case is the 2016 Tesla Autopilot crash, a driver-assistance system, not a driverless robotaxi. The first half of the sentence, about attention measuring coverage supply, is the authors' own claim.

**64. `wu2007novelty`** (06_discussion)

- Sentence: Prior studies find that attention decays over a characteristic time scale [wu2007novelty] and in two phases [candia2019decay], so we report the half-life and the tail share separately.
- Source: "suggesting the existence of a natural time scale over which attention fades." (abstract)

**65. `candia2019decay`** (06_discussion)

- Sentence: Prior studies find that attention decays over a characteristic time scale [wu2007novelty] and in two phases [candia2019decay], so we report the half-life and the tail share separately.
- Source: "the average attention received by cultural products decays following a universal biexponential function" (abstract (Europe PMC))
- Note: Biexponential decay = two phases.

**66. `vasterman2005hypes`** (06_discussion)

- Sentence: A closer match is the self-reinforcing pattern documented for disaster reporting [vasterman2005hypes], sustained in our corpus by investigation and regulatory action rather than by the crash.
- Source: "This self-referential system creates positive feedback loops, expanding the news wave." (subsection 'Media hype'; case 'The Bijlmermeer plane crash')
- Note: Self-reinforcing pattern in disaster reporting is the paper's core point. The second clause (investigation and regulatory action in our corpus) is the authors' own finding.

**67. `lorenzspreen2019accelerating`** (06_discussion)

- Sentence: If successive topics hold attention for ever shorter periods [lorenzspreen2019accelerating], both half-lives would compress and their ratio is the more durable quantity.
- Source: "individual topics receiving shorter intervals of collective attention." (abstract)
- Note: Conditional premise matches the source; the implication about half-lives and their ratio is the authors' inference.

**68. `nhtsa2022sgo`** (06_discussion)

- Sentence: Operator notification clocks should stay short, since the Standing General Order requires the most serious crashes to be reported within days so hazards can be triaged [nhtsa2022sgo].
- Source: "submit an incident report not later than five calendar days after receipt of notice of such incident" (Third Amended SGO 2021-01, Request No. 1, p. 12 (supplied by the author))
- Note: Order dated 24 April 2025, effective 16 June 2025.

**69. `cadmv2026avim`** (06_discussion)

- Sentence: California now requires deployment permit holders to file a five-day collision report in line with that order [cadmv2026avim].
- Source: "A collision shall be reported to the Department as a 5-day, update, and monthly report using the Collision Reporting Template." (AVIM 2026-001A, p.4 'Deployment' (ref. CCR Title 13, Art. 3.8, s228.34); p.1 Summary)
- Note: p.1: collision reports must be submitted 'in alignment with the National Highway Traffic Safety Administration Standing General Order 2021-01 (June 2025)', effective 28 Apr 2026. The five-day report comes with update and monthly reports; the same requirement applies to drivered and driverless testing permits. 'That order' in the manuscript currently resolves to nhtsa2022sgo (a 2022 report on the 2021 order), while the memo aligns with the June 2025 amended order; see id 68 fix.

**72. `ralph2019`** (06_discussion)

- Sentence: They add the relative quantity to existing work on how crash reporting is framed [ralph2019] and how little of it there is [connor2004].
- Source: "Not only does media coverage help determine which issues merit attention, coverage also shapes how issues are framed." (abstract)
- Note: Ralph et al. is a content analysis of how ped/bike crash reporting is framed (blame, public-health frame).

**73. `connor2004`** (06_discussion)

- Sentence: They add the relative quantity to existing work on how crash reporting is framed [ralph2019] and how little of it there is [connor2004].
- Source: "Papers covered 278 fatal crashes over the two year period, in contrast to 846 fatal crashes documented in FARS." (abstract)
- Note: Supports 'how little of it there is'.
