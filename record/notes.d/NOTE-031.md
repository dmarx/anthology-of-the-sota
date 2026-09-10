---
number: 31
status: Read
formerly:
- NOTE-tmp4r97h
paper: LIT-087
title: 'Data Selection for Language Models via Importance Resampling'
version: 1
tags:
- data-pipeline
date: '2026-09-09'
published: '2023-02-01'
summary: >-
  Selects pretraining data by importance resampling in a hashed n-gram feature space — 10,000 buckets of unigram and bigram counts — to match a target distribution. The more useful result is the metric: KL reduction in that feature space predicts downstream performance across selection methods, including manual curation, which uses no n-grams at all.
---

# NOTE-031: Data Selection for Language Models via Importance Resampling

## Contribution

Formalises pretraining data selection as a distribution-matching problem —
given a large raw corpus and a small sample from a desired target, select a
subset distributed like the target — and solves it with classical **importance
resampling**, made tractable by doing everything in a **reduced feature space**.

The feature space is deliberately crude: hash unigrams and bigrams into
`m = 10,000` buckets and count. Importance weights are estimated there, and
data is resampled according to them.

## Key insight

The crude features are the point, and the paper's second contribution is what
justifies them. **KL reduction** — how much a selection reduces distance to the
target relative to random selection, measured in the hashed n-gram space —
**strongly correlates with downstream performance across selection methods,
including methods that use no n-grams at all, such as manual curation.**

That is a much bigger claim than DSIR itself. It says a **cheap, model-free
proxy predicts the outcome of data selection in general**, so a curation
decision can be evaluated without training a model on it. The feature space is
not being claimed as the right representation of text; it is being claimed as
one where the *ordering* of data selections is preserved.

## Assumptions

- **A target distribution is available as unlabeled samples.** The method needs
  a description of what you want, not a quality criterion.
- Hashed n-grams preserve enough of the distributional difference that matters.
  The KL-reduction correlation is the evidence, and it is correlational.
- Generative (Naive-Bayes-like) estimation over discriminative, justified by the
  low-sample regime, citing Ng & Jordan.

## Key results

- **DSIR improves over heuristic classification by 0.9%** and is comparable to
  top-`k` heuristic classification.
- **Top-`k` is competitive for domain-specific selection** — the paper's own
  qualification, on the reasoning that "diversity may be less important than in
  the general-domain setting". Selection method depends on target breadth.
- **Within-domain F1 82.9% vs cross-domain 81.2%** — a 1.7-point average gap
  when data is selected for a target in a different domain. Small, and worth
  knowing.
- **KL reduction predicts downstream performance**, across methods.
- **DSIR selects the most diverse source distribution** for CS targets, which
  the authors offer as the reason for its broad performance.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Importance resampling in a hashed n-gram space is a tractable data-selection method | strong | the method works at Pile scale |
| C2 | KL reduction in that space predicts downstream performance across methods | strong-ish | measured across several methods, correlational |
| C3 | DSIR beats heuristic classification | moderate | 0.9%, and comparable to a top-`k` variant |
| C4 | Diversity matters more for general-domain than domain-specific targets | moderate | inferred from the top-`k` result |
| C5 | Generative estimation suits the low-sample regime | moderate | argued from prior work, consistent with results |

## Method

Hash unigrams and bigrams into 10,000 buckets. Estimate the target and raw
distributions in that space. Compute importance weights. Resample. To evaluate a
selection without training, compute its KL reduction against random selection in
the same space.

## Concepts

- **A cheap proxy that preserves ordering** — the transferable idea. The
  features need not be good, only monotone with respect to the outcome.
- **Target distribution rather than quality score** — data selection framed as
  matching something you can sample from, instead of scoring what is "good".
- **KL reduction** — a metric for a data selection, computable before training.

## Connections

<!-- inactive-ok-block: SOTA-166 — Proposed, named as the record's adjacent data practice rather than relied on -->
Directly adjacent to `SOTA-166` (set the pretraining data proportions by fitting
a mixing law on small runs, not by argument). Both replace argument with
measurement; they differ in cost, and that is the interesting comparison. A
mixing law needs a set of small training runs; KL reduction needs a hash and a
counter.

`LIT-099`'s reading records that PaLM 2 ranks the data mixture above
architecture for final quality. That is the motivation for both; this is the
cheapest instrument for acting on it.

## Recommendations

- **R1** — Evaluate a data selection with a model-free proxy before training on
  it. *Topic:* data pipeline. *Strength:* moderate — C2 is correlational, and
  it is the cheapest available check.
- **R2** — Frame selection as matching a target distribution you can sample
  from, not as scoring quality. *Strength:* moderate.
- **R3** — Use crude features deliberately when only the ordering of candidates
  matters. *Strength:* strong, and general.
- **R4** — Expect the best selection method to depend on target breadth: top-`k`
  for narrow, diversity-preserving resampling for broad. *Strength:* moderate.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice.**

The reading puts a cheaper instrument next to one the record already carries.
<!-- inactive-ok-block: SOTA-166 — Proposed, named as the record's adjacent data practice rather than relied on -->
`SOTA-166` says to fit a mixing law on small runs rather than arguing about
proportions — right, and it costs a set of training runs. **C2 says a hashed
n-gram KL reduction predicts downstream performance well enough to rank
selections, including selections made by hand.** If that holds, it is a
pre-training-run filter that makes the mixing law cheaper to search.

Whether the record should carry it is a registry decision. The correlational
evidence is 2023 and at a scale below where mixing laws are now fitted, and that
is exactly the caveat a practice would need.

The document's takeaways get the subject wrong in a small way that matters.
**"Data quality assessment" and "quality-aware data mixing"** describe scoring
data for quality; this paper deliberately does not do that. It matches a target
distribution, which is a different framing and the one the paper is careful
about.

## Limitations

- 2023, and the models trained for evaluation are small.
- C2 is a correlation across a handful of selection methods.
- C3's margin is 0.9%.
- Hashed n-grams cannot express anything about structure, reasoning or
  correctness, so "match the target" is only as good as the target.

## Open questions

- Does the KL-reduction correlation survive at frontier scale, where selection
  methods are model-based and targets are implicit? That is exactly the regime
  the record's data practices live in and the one this paper cannot reach.
