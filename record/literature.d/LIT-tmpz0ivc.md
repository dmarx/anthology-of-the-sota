---
status: Active
title: Moving towards informative and actionable social media research
version: 1
tags:
- deployment-and-society
- analysis-and-evaluation
date: '2026-09-21'
published: '2025-05-01'
arxiv: '2505.09254'
first_author: 'Bak-Coleman'
keywords:
- 'causal-inference'
- 'complex-systems'
- 'randomized-trials'
- 'sutva'
- 'estimand'
implementations: []
summary: >-
  Bak-Coleman, Lewandowsky, Lorenz-Spreen, Narayanan, Orben and Oswald (2025),
  [ARXIV-2505.09254](https://arxiv.org/abs/2505.09254). Individual-level randomized trials do not
  estimate collective effects, for four named reasons — non-linearity across
  scale, hysteresis, feedback in time, and SUTVA violation through the network.
  A null from such a trial is not evidence of no effect, and the positive
  recommendation is to evaluate specific interventions instead of net effects.
---

# LIT-tmpz0ivc: Moving towards informative and actionable social media research

## Why it's here

The argument is about social media and it is not limited to social media. It
is about what happens when you randomize individuals and ask about a
collective outcome, in any system where the units interact and the state
depends on its history — which describes every deployed recommender, ranking
system and assistant at scale.

It is also the sharpest thing this record holds about the gap between an
*estimand* and an *estimate*, which is a concern it already has in the
model-evaluation direction ([SOTA-200](../practices.d/SOTA-200.md), [SOTA-278](../practices.d/SOTA-278.md)) and had
nothing on for deployed systems.

## The four reasons

The paper's device is a power grid, and it earns the space. Suppose you
suspect demand spikes cause blackouts, and you randomize substations to
receive spikes.

**1. Non-linearity across scale.** Treat a small share and the grid absorbs
it — no effect. Treat a large enough share and the grid fails, blacking out
*the controls too* — again no difference between arms. Both readings say "no
effect" and both are wrong, because the estimated quantity was never the
estimand.

**2. Hysteresis.** After a failure, relieving load on some substations brings
none of them back. Concluding load did not cause the failure would be wrong.
**This besets every withdrawal study** — deactivation, reduced use, feature
removal — because they all assume the effect of the platform is the opposite
of the effect of removing it. The paper's social example: randomize long-time
Duolingo users to stop for a week, find fluency retained, conclude Duolingo
does not teach language.

**3. Feedback in time.** Effects unfold non-monotonically and depend on when
you look. Ask long-term smokers to stop for two weeks and they become
irritable and gain weight; by the reasoning common in this literature, short
trials would establish smoking as a safe way to lose weight and reduce
stress. And because recommendation algorithms learn from behaviour, the
system is changing while you measure it — so experiments of different lengths
should be *expected* to conflict.

**4. SUTVA violation.** The stable unit treatment value assumption requires
that one unit's outcome not depend on another unit's treatment. People are
coupled. Randomize someone to a chronological feed and they still receive
algorithmically-curated content, because their neighbours share what the
algorithm showed *them*. A teenager taken off social media is still affected
by whether their friends were. Avoidable only by randomizing whole
subnetworks, **and the paper reports that no existing trial does this**.

## The positive half

Stop asking for the net effect of the system and evaluate **specific
interventions on specific affordances** — down-ranking toxic content, bridging
ranking, cross-partisan prompts. Three stated advantages: the counterfactual
is coherent so the estimand is meaningful; small treatments can run far longer
than a deactivation study can; and the result maps onto a decision somebody
can take.

Two riders. Because effects are time- and state-dependent, intervention
evaluation has to be **continuous** rather than one-shot — which is what
platforms already do for their own commercial metrics. And no single modality
is a gold standard here, so the path forward is triangulation across trials,
observation and models rather than a better trial.

## Conditions

**It is a review and an argument, not a measurement.** No new data. The four
mechanisms are established and the application is reasoned; what is not shown
is how large each distortion is in any specific published study.

**"Bound to be of limited value" is a judgement.** That individual-level
trials cannot cleanly identify macro-level outcomes follows from the four
mechanisms. How much value remains is not quantified, and a reader who wants
to keep using such trials for narrower estimands is not refuted here.

**The withdrawal-study criticism is the strongest claim and the most
general.** It applies to a specific, popular design and the argument against
it is symmetry, which is hard to escape. It is also the claim most likely to
be read as dismissing a literature rather than as bounding what that
literature can conclude.

**Shared authorship with [LIT-tmpvcocw](LIT-tmpvcocw.md).** Bak-Coleman is first author on
both this and the industry-influence study, which are filed together and
argue complementary halves. They are not independent sources.
