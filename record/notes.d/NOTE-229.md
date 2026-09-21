---
number: 229
status: Read
formerly:
- NOTE-tmpz4t8g
paper: LIT-480
title: 'Auditing Political Exposure Bias'
version: 1
date: '2026-09-21'
summary: >-
  Reading it to find out whether `deployment-and-society` earns its place: it
  does, and not because of the finding. The methods section is a sequence of
  stated trades about measuring a system you cannot inspect, and the sharpest
  result is that the arm following nobody gets the most diverse timeline.
---

# NOTE-229: Auditing Political Exposure Bias

## Contribution

A measurement of a recommender from outside it, with the instrument designed
rather than improvised. The finding is about Twitter/X in late 2024 and will
date; the instrument is about any deployed ranking system whose operator will
not help you, and will not.

What is true afterwards that was not before: the out-of-network half of a
personalized timeline — about 50% of what users see — has been measured for
concentration and partisan asymmetry with a controlled design, rather than
inferred from what users report seeing.

## Key insight

**Do not let the puppets interact.** This is the decision the rest depends on
and the one most likely to be gotten wrong, because interaction looks like
realism.

Three reasons, all given: interaction creates feedback loops, so you can no
longer tell the algorithm's prior from what your own clicks taught it;
partisan accounts would engage differently, so arms stop being comparable; and
the question is what the system does *before* a user teaches it anything.

The cost is ecological validity and the paper says so. What it buys is the
only thing that makes the neutral arm meaningful — and the neutral arm turns
out to carry the most interesting result.

## Assumptions

- **Follow sets curated to the subject**, not replicated from real users:
  ten AllSides-rated outlets (seven moderate, three strong) plus four
  political figures. Realism traded for confound control, explicitly.
- **Rank decays attention exponentially**, calibrated from TikTok and YouTube
  findings that the top 20% of items take ~70% of views — **transplanted
  across platforms**.
- **Political leaning assigned by hand** from the AllSides chart and public
  profiles, with the paper noting it may be wrong or stale.
- **The balanced arm is the baseline** for amplification, so "amplified" means
  relative to a timeline the same algorithm produced.
- **Randomized interests, randomized birthdates, VPN**, to suppress the
  attributes the platform forces you to supply.

## Key results

- Gini above **0.45** in every arm; all pairwise differences significant at
  p < 0.001 (Mann-Whitney U).
- Ordering: right-leaning most unequal, then balanced, then left, then
  **neutral least** — the arm following nobody sees the most diverse timeline.
- Prior work: Gini 0.6–0.7 for exposure to *friends'* tweets. Out-of-network
  is comparable.
- Neutral arm exposure share, right- vs left-leaning accounts: **30.16% vs
  12.92%** (top 20), 35.26% vs 22.34% (top 50), 31.39% vs 20.83% (top 100).
- Top aligned voices amplified **more than 50%** above the balanced baseline in
  both partisan arms.
- Left-arm amplification slightly larger in magnitude than right-arm;
  **de-amplification does not differ** significantly between them.
- Out-of-network share of the timeline: 100% neutral, 59.23% left, 55.88%
  right, 62.27% balanced.

## Claims

**Methodological, and the durable part:** that a non-interacting,
narrowly-followed sock-puppet fleet with rank-weighted exposure and a
balanced-arm baseline measures algorithmic prior rather than
algorithm-plus-user. Argued from three stated reasons rather than asserted.

**Empirical and dated:** the partisan asymmetries. One platform, six weeks,
one election, hand-assigned leanings.

**Interpretive:** that the neutral arm's diversity is cold start. Offered as
an explanation, not tested.

## Method

Four arms of 30 accounts; four timeline collections daily for six weeks; 9.79M
tweets; Gini and Lorenz curves for concentration; a mean amplification ratio
against the balanced arm; Mann-Whitney U throughout.

## Concepts

*Weighted occurrence per 1,000 tweets* — exposure discounted by rank;
*out-of-network* content as the object of study; *mean amplification ratio*
against a within-experiment baseline; the sock-puppet fleet as an instrument
with an explicit validity trade.

## Connections

- This is the first document filed under `deployment-and-society`
  ([ADR-052](../decisions.d/ADR-052.md)), and it is the paper that decision was measured against.
- The rank-weighting argument is the same shape as several practices this
  record already holds about measurement: a raw count is not the quantity you
  care about, and the correction is cheap and specific. [SOTA-200](../practices.d/SOTA-200.md)'s
  metric-artefact check and [SOTA-210](../practices.d/SOTA-210.md)'s pass@k are the same family of
  argument aimed at models rather than at deployed systems.
- Nothing in the record connects to it directly, which is what a first
  document in a new topic looks like.

## Bearing on the record

It settles the question [ADR-052](../decisions.d/ADR-052.md) left open. The decision added a topic
that named nothing and wrote down the falsifier: *if the first filing produces
a literature note and nothing actionable, the topic is a shelf.*

It produced a practice and an account. The practice is the audit design; the
account is that personalization concentrates exposure rather than broadening
it, with the no-follow arm as the evidence. So the topic is a category.

## Limitations

**A photograph of a moving target.** Six weeks of one platform around one
election. The ranking system has changed since and will again.

**The classification carries the headline.** Right-versus-left exposure shares
rest on hand-assigned leanings from profile text and an external media chart,
which the authors say may be inaccurate or stale.

**Calibration borrowed across platforms.** The attention decay comes from
TikTok and YouTube. Every exposure figure inherits that transplant, and no
sensitivity analysis over the decay parameters is reported.

**The baseline arm is not clean and the paper says so.** Neutral accounts
follow nobody, but trending topics and platform defaults still reach them — so
the arm meant to show the algorithm's prior shows the prior plus whatever the
platform promotes by default.

**Not users.** Non-interacting accounts with ten curated follows are an
instrument, not a sample of people. The numbers describe what the algorithm
does to that instrument.

## Open questions

- Does the no-follow-is-most-diverse result hold on other platforms? If it
  does, "personalization concentrates" is a property of the class rather than
  of this system, and that is the finding worth having.
- How sensitive is everything to the decay parameters? One sensitivity sweep
  would tell you whether the rank-weighting is doing work or decoration.
- Does the design survive a platform that detects and throttles sock-puppets?
  The paper works within rate limits for new non-premium accounts; a platform
  that wanted to defeat this could.
