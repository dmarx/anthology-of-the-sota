---
number: 25
status: Proposed
formerly:
- THEORY-tmpqd9wu
promote_when: >-
  An independent measurement of bits-per-parameter capacity on a
  non-GPT-family architecture — a mixture-of-experts model, or one with
  heavily tied embeddings — that either reproduces the linear law or breaks
  it; and separately, a demonstration that the capacity crossing predicts the
  onset of overfitting under *repeated* data, not only under increasing
  unique data. What would not settle it: another double-descent curve with
  parameters and samples on the axes, which is the framing this replaces.
title: 'A transformer holds about 3.6 bits per parameter, and generalization begins where the data outgrows that budget'
version: 2
history:
- version: 2
  date: '2026-09-20'
  note: >-
    Two neighbours arrived. Lu et al. (LIT-452) measure fact capacity on
    Wikidata and find it linear in model size — the same functional form
    through a different instrument and different units, which is the second
    measurement this account's linear claim wanted. Gu et al. (LIT-451)
    bound it: the fixed-budget picture is the single-claimant case, and with
    two datasets competing the allocation between them is discrete
    (THEORY-029). `explains:` is still empty and the reason is unchanged.
    The account is not revised.
tags:
- analysis-and-evaluation
date: '2026-09-19'
source:
- LIT-440
explains: []
summary: >-
  Morris et al. (2025), [LIT-440](../literature.d/LIT-440.md) — measured on uniform random
  bitstrings where generalization is impossible, GPT-style transformers store
  3.5-4 bits per parameter, linear in parameter count and almost indifferent
  to weight precision. On real text, double descent begins exactly where the
  data's information content crosses that capacity. The proposed mechanism —
  that a model past capacity must share representation, and sharing is
  generalization — is an interpretation, not a measurement.
---

# THEORY-025: A transformer holds about 3.6 bits per parameter, and generalization begins where the data outgrows that budget
<!-- inactive-ok-file: THEORY-029 — Proposed, and filed in this same contribution as the account that bounds this one -->
<!-- inactive-ok-file: SOTA-124 — Proposed, and the practice whose linear-scaling conjecture this measurement half-checks -->
<!-- inactive-ok-file: SOTA-173 — Proposed, and named as one of the two positions this would bridge if the experiment were run -->

## Source

Morris et al. (2025), [LIT-440](../literature.d/LIT-440.md) — [ARXIV-2505.24832](https://arxiv.org/abs/2505.24832).

## What was actually shown

The measurement works by removing the thing that makes memorization hard to
measure. Train on **uniformly sampled random bitstrings**, whose Shannon
information is exactly computable and which contain no structure to
generalize to. Whatever the model then holds about the data is storage and
nothing else. Sum the per-datapoint compression gain, take the maximum over
dataset sizes, and that is capacity.

The result: **3.5–4 bits per parameter**, clustering at 3.61–3.68 across
widths and depths, and **linear in parameter count** across models from
roughly 500K to 1.5B. Capacity predictions hold across sequence length and
vocabulary size to about 1.8% error.

This could have come out otherwise in three ways, and did not. Capacity could
have depended on model shape rather than parameter count; it does not.
It could have scaled with the bits in the weights; **going from bfloat16 to
float32 doubles those bits and moves capacity from 3.51 to 3.83** — about 9%,
so nearly all the additional representational range is not used for storage.
And the plateau could have kept rising with more data; it does not, which is
what makes it a capacity rather than a rate.

On real text, with an oracle model standing in for the true distribution, the
same apparatus tracks memorization and generalization separately as the
dataset grows. Memorization rises to the capacity plateau and then *falls* as
the model substitutes shared structure. **Double descent begins at exactly
that crossing** — the first account of it with both quantities measured
rather than proxied by parameter and sample counts.

## The mechanism, and its status

The offered explanation: once a model cannot store datapoints separately it
is forced to share representation between them, and representation shared
across datapoints is what generalization is.

That is an interpretation. It fits the co-location of the two events and
nothing here isolates it — no intervention makes sharing easier or harder
while holding capacity fixed. The authors describe it as a theory. The
measurement stands without it.

## What this does not say

**It does not say a transformer *can* hold only 3.6 bits per parameter.**
Capacity here is what gradient descent reaches, so every number is a lower
bound on the architecture. A better optimizer would move it, and the paper
says so.

**It does not say the linear law survives sparsity.** Mixture-of-experts,
tied embeddings and aggressive quantization are all untested, and sparsity is
precisely the kind of thing a per-parameter law should break. The largest
model measured is 1.5B.

**It does not say your model has memorized your data.** The text-side
measurement is relative to an oracle model trained on the full distribution,
and inherits that oracle's errors. Without one, unintended memorization is
not separable from generalization by this method.

**It does not resolve the record's repetition dispute, though it is the
closest thing to a common unit for it.** [SOTA-124](../practices.d/SOTA-124.md) rests on a memorization
window that "scales linearly" in parameters, from a single figure its own
source calls early; the linear scaling is now measured, three orders of
magnitude of it. But Falcon's window is a *token* count and this is a *bit*
count, and nobody has done the conversion. [SOTA-171](../practices.d/SOTA-171.md) and [SOTA-173](../practices.d/SOTA-173.md)
disagree about whether repetition overfits; this predicts the turn should
occur at the capacity crossing, which is testable and untested — the double
descent measured here is at varying *unique* dataset size, not at varying
epoch count over a fixed corpus.

**It does not license the 3.6 figure as a design constant.** It is one
architecture family, one training procedure, one precision regime, measured
as a lower bound. Used to reason about orders of magnitude it is the best
number available; used to size a model it is an extrapolation past everything
that was checked.

## A second measurement, and a boundary

**Corroboration.** Lu et al., [LIT-452](../literature.d/LIT-452.md), measure how many Wikidata
triples a model can recall and find capacity **linear in model size**, with a
separate negative-exponential saturation in training epochs. That is this
account's linear claim reached through an entirely different instrument:
facts on a real knowledge base, where generalisation is possible and is
separately quantified, against bits on random bitstrings where it is
impossible by construction.

Two instruments agreeing on the functional form is better than either alone.
What is still missing is the conversion — how many bits a fact costs — which
is what would let the two be checked against each other rather than merely
rhyming. Until somebody does it, this is agreement in shape and not in
magnitude.

**Boundary.** Gu et al., [LIT-451](../literature.d/LIT-451.md), show that the clean picture here is
the **single-claimant** case. Mix a knowledge-dense dataset into web text and
knowledge acquisition acquires thresholds in both model size and mixing
ratio: below them, almost nothing is stored however long training runs. The
account offered is that bounded capacity allocated across datasets is a
discrete problem, so its optimum jumps — [THEORY-029](THEORY-029.md).

Nothing here is wrong; the measurements were made on one dataset at a time,
and that is exactly the case where the budget has one claimant and fills
smoothly. The plateau this account measures is the shape competition does not
produce.

## Why `Proposed`

One group, one measurement campaign, and the two halves have different
standing. The capacity number is a direct measurement and is strong. The
double-descent account is a co-location plus an interpretation, and the
interpretation is the part that would make this explain anything.

`explains:` is deliberately empty. This underwrites no practice in the record
yet, and the honest reason is that the bridge to the repetition dispute — the
experiment that would connect capacity to multi-epoch overfitting — has not
been run by anyone.
