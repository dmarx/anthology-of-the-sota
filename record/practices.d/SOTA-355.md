---
number: 355
status: Active
formerly:
- SOTA-tmphjeso
title: 'Isolate the emergent outlier feature dimensions into 16-bit and quantize the rest to int8'
version: 2
history:
- version: 2
  date: '2026-09-24'
  note: >-
    Adds a condition and leaves the recommendation alone. Ahmadian et al.
    (LIT-tmp7791d) hold the architecture fixed, vary weight decay, dropout,
    clipping and dtype from 410M to 52B, and find outlier dimensions track
    those rather than parameter count — so "emergent", in this title and in
    the source, is contested. They also could not make this document's
    step-2 detection recipe work: the published threshold of 6.0 did not
    classify outliers across their variants, and no adaptation they tried,
    including after correspondence with the original authors, correlated with
    quantization sensitivity. The decomposition still works on models that
    have outliers, which is why the status and consensus are unchanged.
tags:
- numerics-and-precision
- inference-optimization
consensus: converged
consensus_note: >-
  This is what `load_in_8bit=True` does in `transformers`, and `vllm` serves
  it too — the sweep in #289 found `bitsandbytes` carried by both indexes
  and reading the row apart showed it was two techniques, this one and NF4
  (SOTA-230). Adoption, not evidence (DP-005): what is converged is that
  int8 inference at scale requires handling outliers separately, rather than
  that this particular decomposition is the best way.
date: '2026-09-23'
source:
- LIT-586
introduced_by:
- LIT-586
summary: >-
  Dettmers et al. (2022), [ARXIV-2208.07339](https://arxiv.org/abs/2208.07339). Quantize the projections
  vector-wise to int8, but pull the handful of systematically large feature
  dimensions out into a separate 16-bit multiplication — 99.9% of values in
  8-bit, no measured quality cost up to 175B.
---

<!-- inactive-ok-file: SOTA-tmpqmou6, THEORY-tmp3s87v — both Proposed, filed in this same contribution and
     named in a condition that says this practice's framing is CONTESTED by
     them. The condition depends on their being unsettled: if they were
     Active this section would be a supersession rather than a caveat, and
     this practice would stand differently. -->
# SOTA-355: Isolate the emergent outlier feature dimensions into 16-bit and quantize the rest to int8

## Source

Dettmers et al. (2022), [LIT-586](../literature.d/LIT-586.md) — [ARXIV-2208.07339](https://arxiv.org/abs/2208.07339).

## Two conditions, one on the word in the title and one on step 2

**"Emergent" is contested.** Ahmadian et al. ([LIT-tmp7791d](../literature.d/LIT-tmp7791d.md)) ran the
controlled version of the question — same architecture, varying weight decay,
dropout, gradient clipping and half-precision format, 410M to 52B, every
variant from scratch and at comparable pre-quantization quality — and found
the sensitivity tracks those choices rather than parameter count. Their 52B
model loses nothing to plain INT8 where OPT-66B is reported to lose about 42%.
[THEORY-tmp3s87v](../theory.d/THEORY-tmp3s87v.md) holds that account; [SOTA-tmpqmou6](SOTA-tmpqmou6.md) is what to do about it
before training. The title keeps the word because it is the source's and the
technique is known by it.

**The detection step has failed an independent replication.** Step 2 below
asks you to find the outlier dimensions. The same group reports that the
published threshold of 6.0 was *"too high to classify a feature dimension as
an outlier for all the variants we consider"*, and that after corresponding
with the original authors and trying several adaptations, *"we did not observe
a clear correlation between these measures and sensitivity to quantization."*

That is the only independent attempt at this detection the record holds, and
it did not work. It does not make the practice wrong — the implementations
below ship a detector that works well enough in production — but a reader
implementing step 2 from the paper should know that one group could not, and
that the threshold may be specific to how the model was trained.

## What to do

For the feed-forward and attention projection matrices:

1. Quantize **vector-wise** — one normalization constant per inner product,
   not one per tensor.
2. Detect the feature dimensions whose magnitudes are far outside the rest,
   and route those columns into a separate 16-bit matrix multiplication.
3. Sum the two products.

More than 99.9% of values go through the 8-bit path.

## Why the decomposition is the whole method

Naive int8 works on small transformers and breaks on large ones, and for
years that read as "quantization gets harder with scale". The paper's
contribution is the diagnosis: **a small number of feature dimensions emerge
with very large magnitudes**, they recur across layers, and they dominate
attention and prediction. A per-tensor scale chosen to cover them destroys
the resolution of everything else.

So the fix is not a better global scale. It is to stop asking one scale to
cover two very different distributions.

## What it buys, and what it does not

Memory, and access. A 175B 16/32-bit checkpoint loads, converts and runs at
roughly half the memory — the stated payoff is OPT-175B or BLOOM on a single
server of consumer GPUs, not throughput. The extra 16-bit path and the
outlier detection cost time, and reports of int8 inference being *slower*
than 16-bit at small batch are consistent with this method rather than
evidence against it.

## The claim to watch

*"Without any performance degradation"* means *no degradation the authors
measured, on their evaluations, up to 175B*. It is a strong result and it is
an absence-of-evidence claim about a specific suite — the shape `DP-010`
names. The emergent-outlier characterization is the part later work has
built on; the no-degradation headline is the part a harder evaluation could
move, and this record holds no independent test of it.
