---
status: Proposed
promote_when: >-
  The design applied to a different platform by a group unconnected to this
  one, with the non-interaction choice and the rank weighting carried over and
  their effect reported — ideally a sensitivity sweep showing what the decay
  parameters are worth. Another audit of Twitter/X is not it.
consensus: unreplicated
consensus_note: >-
  Sock-puppet auditing itself has independent precedent, which this source
  cites and argues against on two points: prior audits replicate real users'
  follows, and radicalization studies let their bots interact. What is
  unreplicated is this configuration — non-interacting accounts, follow sets
  curated to the subject, rank-weighted exposure, and a within-experiment
  balanced baseline.
title: 'To measure what a deployed recommender does, use sock-puppets that never interact, follow sets curated to your question, and exposure weighted by rank'
version: 1
tags:
- deployment-and-society
- analysis-and-evaluation
date: '2026-09-21'
source:
- LIT-tmpq6fna
introduced_by:
- LIT-tmpq6fna
implementations: []
explained_by:
- THEORY-tmp0qzbq
---

<!-- inactive-ok-file: THEORY-tmp0qzbq — Proposed, and the account this practice
     declares as its explanation. Both rest on one six-week audit of one platform,
     which is the state being recorded -->

# SOTA-tmpxtcgk: To measure what a deployed recommender does, use sock-puppets that never interact, follow sets curated to your question, and exposure weighted by rank

## Source

Ye, Luceri and Ferrara (2024), [LIT-tmpq6fna](../literature.d/LIT-tmpq6fna.md) — read as
[NOTE-tmpz4t8g](../notes.d/NOTE-tmpz4t8g.md). 120 accounts, six weeks, 9.79M tweets from
Twitter/X's "For You" timeline.

## When this applies

You want to know what a ranking system does, you cannot inspect the model, and
its operator will not help. That is the normal case for any deployed
recommender, and it is increasingly the case for systems whose research APIs
have been withdrawn.

## The claim

Four design decisions, and the first is the one that makes the rest mean
something.

**Do not let the accounts interact.** No clicks, no follows taken from
recommendations, no engagement. This is against the practice in radicalization
studies, and the reasons are specific: interaction creates feedback loops, so
you can no longer separate the system's prior from what your own behaviour
taught it; different arms would engage differently, so cross-arm comparison
stops being clean; and the question is what the system does *before* a user
teaches it anything.

**Curate the follow sets to your question, not to realism.** Prior audits
replicate real users' follow graphs for ecological validity. Do not — real
users follow diverse things unrelated to what you are measuring, and every one
of them is a confound. Here: ten media outlets drawn from a published bias
chart, seven moderate and three strong, plus four political figures.

**Weight exposure by rank.** A raw count of appearances is not exposure,
because nobody reads to the bottom of a feed. Apply a decay over position —
here exponential, calibrated so the top 20% of a timeline carries about 70% of
attention.

**Baseline against an arm of your own experiment.** Amplification is measured
against the balanced accounts, not left against right, so "amplified" means
relative to a timeline the same algorithm produced under the same conditions.

Plus the hygiene that makes the arms comparable: **randomize everything the
platform forces you to supply** — required interests, birthdates — and use a
VPN so location does not vary.

## Include an arm that follows nobody

The most useful result in the source comes from the arm designed as a control.
Accounts following nobody receive the **most diverse** recommendations of any
group, which is what [THEORY-tmp0qzbq](../theory.d/THEORY-tmp0qzbq.md) is about, and it is the only arm
that measures what a new user gets before personalization starts.

It is also the arm that shows the system's defaults, which is usually the
thing a reader outside the platform most wants to know.

## Conditions

**Ecological validity is the price and it is not small.** Non-interacting
accounts with ten curated follows are an instrument, not a sample of people.
What you measure is what the algorithm does to that instrument. The source
argues this is the right trade for a question about algorithmic prior and
names the literature that disagrees; do not report the numbers as what a
person would experience.

**The rank-decay parameters are a borrowed assumption.** The 20%/70% attention
figure in the source comes from TikTok and YouTube studies and is transplanted
to Twitter/X. Every exposure number inherits it, and the source reports **no
sensitivity analysis** over the decay. If you use this design, run one.

**Your control arm is not clean.** Accounts following nobody still receive
trending topics and platform defaults, so the arm meant to isolate the
algorithm's prior shows the prior plus whatever the platform promotes anyway.
The source flags this about its own baseline.

**Hand-assigned labels will carry your headline.** Here the partisan
asymmetries rest on leanings assigned from a published media chart and from
profile text, which the authors say may be inaccurate or stale. Whatever
categorisation you apply to the recommended accounts is load-bearing and
should be reported as such.

**Rate limits shape the design.** Four collections a day at 2,000–3,000 tweets
per account was what the platform's terms allowed for new non-premium
accounts. A platform that wanted to defeat this could, and a withdrawn API is
the normal direction of travel.

**One platform, six weeks, one election.** The source is a photograph of a
moving target, and a design validated on one system is not thereby validated
on another — which is what this practice's promotion condition asks for.
