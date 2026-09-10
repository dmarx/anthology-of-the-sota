---
number: 197
status: Active
formerly:
- SOTA-tmpmx5mv
consensus: converged
consensus_note: >-
  That contamination invalidates benchmark results is universally agreed; what
  almost nobody does is state their exposure or ship a way to probe it.
title: 'Account for test-set proximity to the training data when evaluating, and state your contamination exposure'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-10'
published: '2021-12-01'
source:
- LIT-060
- LIT-077
implementations: []
---

# SOTA-197: Account for test-set proximity to the training data when evaluating, and state your contamination exposure

## Source

Borgeaud et al. (2021), [LIT-060](../literature.d/LIT-060.md) — Retro, which proposes "an evaluation aware
of proximity of test documents with the training set".

Srivastava et al. (2022), [LIT-077](../literature.d/LIT-077.md) — BIG-bench, which states its own exposure
and ships a probe for future models.

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
