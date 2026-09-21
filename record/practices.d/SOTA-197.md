---
number: 197
status: Active
formerly:
- SOTA-tmpmx5mv
consensus: converged
consensus_note: >-
  That contamination invalidates benchmark results is universally agreed; what
  almost nobody does is state their exposure or ship a way to probe it. Three
  groups now do, and the third puts a price on it — which is what the
  agreement had been missing.
title: 'Account for test-set proximity to the training data when evaluating, and state your contamination exposure'
version: 2
history:
- version: 2
  date: '2026-09-21'
  note: >-
    Adds LIT-tmpgqsmp as a third source, and with it the practice's first
    number. v1 rested on a proposal (LIT-060) and a disclosure (LIT-077), and
    its consensus_note observed that what almost nobody does is state their
    exposure. A frontier lab now has, and priced it: a hundred fine-tuning
    steps on web extracts corresponding to a benchmark's training set moves
    HellaSwag enough to pass the competitor. No change to the recommendation.
tags:
- analysis-and-evaluation
date: '2026-09-10'
source:
- LIT-060
- LIT-077
- LIT-tmpgqsmp
introduced_by:
- LIT-060
implementations: []
---

# SOTA-197: Account for test-set proximity to the training data when evaluating, and state your contamination exposure

## Source

Borgeaud et al. (2021), [LIT-060](../literature.d/LIT-060.md) — Retro, which proposes "an evaluation aware
of proximity of test documents with the training set".

Srivastava et al. (2022), [LIT-077](../literature.d/LIT-077.md) — BIG-bench, which states its own exposure
and ships a probe for future models.

Gemini Team, Google (2023), [LIT-tmpgqsmp](../literature.d/LIT-tmpgqsmp.md) — read as
[NOTE-tmp13fue](../notes.d/NOTE-tmp13fue.md) — which does both and measures the size of the effect.

## What it is worth, measured

[LIT-tmpgqsmp](../literature.d/LIT-tmpgqsmp.md) supplies the number this practice lacked. An
**additional hundred fine-tuning steps** on website extracts corresponding to
the HellaSwag *training* set — extracts that were not in the pretraining data —
take validation accuracy to **89.6%** for Gemini Pro and **96.0%** for Gemini
Ultra at 1-shot, against GPT-4's measured **92.3%** 1-shot.

A hundred steps is nothing against any pretraining budget. So the distance
between a contaminated and an uncontaminated number, on a popular benchmark,
is smaller than the distance between two frontier models — and it is
purchasable with a rounding error of compute.

Two things follow, and the report does both. The extensive post-training leak
analysis led them to **drop LAMBADA** rather than report it. And HellaSwag is
reported decontaminated at 10-shot only, alongside new benchmarks chosen or
built to be leak-free: WMT23, Math-AMC 2022-2023, and Natural2Code, the last
generated from non-web sources.

This is a frontier lab stating its exposure against its own interest, which is
exactly what the `consensus_note` above says almost nobody does.

## The claim

Two things, and the second is the cheap one.

**Proximity is continuous, not binary.** Contamination is usually treated as a
yes/no question answered by exact-match deduplication, and `LIT-060` proposes
grading evaluation by **how close** each test document is to the training set.
That matters for every language model and, as the paper says, especially for
retrieval-augmented ones "since they have direct access to the training dataset
during evaluation" — a retrieval model can retrieve the answer, which is not
contamination in the usual sense and has the same effect.

**State your exposure, and ship a probe.** BIG-bench's handling is the model to
copy: training data for every evaluated model except PaLM predates the
repository, so **direct leakage is impossible by construction**; indirect leakage
through text already on the internet is **acknowledged rather than assumed
away**; and a `training_on_test_set` task ships so future models can be probed.

That is three sentences of disclosure and one task. It is not a research
contribution and almost nobody does it.

## Conditions

`LIT-060` proposes the proximity-aware evaluation and does not establish a
standard threshold; what counts as "too close" is unresolved and probably
task-dependent.

The disclosure half has no conditions. It costs nothing and its absence is not
evidence of cleanliness.

## Known implementations

- BIG-bench's `training_on_test_set` task
- Retro's proximity-filtered evaluation splits
