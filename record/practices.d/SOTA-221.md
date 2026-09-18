---
number: 221
status: Active
formerly:
- SOTA-tmp28q6x
consensus: unreplicated
consensus_note: >-
  Widely implemented and rarely re-measured, and those are different facts.
  Layerwise norm-ratio scaling ships in every major framework and has been the
  optimizer of record for large-batch BERT since 2019 — adoption, which is not
  evidence. The comparative claim underneath it, that it beats a grid-searched
  AdamW at batch sizes AdamW cannot reach, rests on one group's experiments on
  two workloads, and no second group has redrawn the comparison.
title: "To train past the batch size where your optimizer stalls, change the optimizer's conditioning rather than the scaling rule"
version: 2
history:
- version: 2
  date: '2026-09-18'
  note: >-
    Names the instrument behind the ImageNet number. "ImageNet" covers three
    different things in this record; the 16K ResNet-50 comparison is on
    ILSVRC, now filed. No change to the recommendation or the evidence.
tags:
- training-optimization
date: '2026-09-16'
source:
- LIT-265
- LIT-058
introduced_by:
- LIT-265
compared_against:
- SOTA-218
implementations: []
summary: >-
  You et al. (2019), [LIT-265](../literature.d/LIT-265.md). When a batch size stops reaching your accuracy
  target, the reflex is to look for a better learning-rate scaling rule.
  [LIT-058](../literature.d/LIT-058.md) is 168,160 training runs of evidence that there is no such rule to
  find. What moved the wall instead was the optimizer: normalizing each layer's
  update by the ratio of its parameter norm to its update norm, on top of
  per-coordinate adaptivity, carried BERT from 16K to 32K where a grid-searched
  AdamW could not follow. This does not license skipping the retuning in
  [SOTA-218](SOTA-218.md) — the two say different things about different activities, and
  [THEORY-012](../theory.d/THEORY-012.md) is why.
explained_by:
- THEORY-012
---

<!-- inactive-ok-file: THEORY-012 — Proposed, and cited here AS the
     Proposed account that reconciles this practice with SOTA-218. The
     instruction stands on LIT-265's measurements without it. -->
<!-- inactive-ok-file: SOTA-215 — Proposed, and named as the neighbouring
     answer for a different constraint (communication cost, not batch size),
     which is a pointer rather than support. -->

# SOTA-221: To train past the batch size where your optimizer stalls, change the optimizer's conditioning rather than the scaling rule

## What to do

When a batch size stops reaching the target and you are looking for a bigger
one, **spend the effort on the optimizer, not on the scaling heuristic.** The
specific move [LIT-265](../literature.d/LIT-265.md) supplies: take an Adam-style per-coordinate update `u`,
then scale each layer's step by `phi(||x_layer||) / ||u_layer||`, with `phi`
clipping the parameter norm into a fixed range so a degenerate layer cannot
blow the ratio up. Two levels of normalization — per coordinate underneath, per
layer on top.

Both levels are load-bearing, and the paper's own negative result is how you
know. LARS is the same layerwise ratio over momentum SGD with no per-coordinate
term; it reaches the ResNet-50 target and fails on BERT at every batch size
tried. If your model's layers differ as much as an attention stack's do, one
level is not enough.

## What it buys, exactly

On BERT-Large pre-training, with SQuAD v1.1 F1 as the target and a baseline of
90.395 from the public checkpoint:

- **AdamW stops at 16K.** [LIT-265](../literature.d/LIT-265.md) tried three tuning strategies for it — default
  hyperparameters, LAMB's hyperparameters, and a grid search — and past 16K it
  reaches 88.1 against a 90.4 target. At the 64K/32K mixed-batch schedule,
  "even after extensive tuning of the hyperparameters, we fail to get any
  reasonable result".
- **LAMB reaches 32K** with F1 at or above the baseline, and the mixed-batch run
  finishes in 76 minutes on a TPUv3 Pod against three days for the baseline.
- **On ImageNet/ResNet-50 at 16K**, comprehensively tuned Adagrad, Adam and
  AdamW reach 55.4%, 66.0% and 67.3% top-1 against a 76.3% target. LAMB reaches
  it. The instrument is ILSVRC ([LIT-tmpa2myh](../literature.d/LIT-tmpa2myh.md)), the thousand-class
  classification challenge — not the database it is drawn from, and not the
  downsampled ImageNet-64 that generative work reports FID on.

The baselines being tuned is what makes these numbers mean anything, and it is
worth saying plainly because the opposite is the usual failure: an optimizer
paper whose baseline inherited its learning rate is measuring the inheritance.
[LIT-265](../literature.d/LIT-265.md)'s baselines were grid-searched and its own appendix reports the search
spaces.

## What this is not

**It is not permission to skip the retuning in [SOTA-218](SOTA-218.md).** [LIT-265](../literature.d/LIT-265.md) reports its
large-batch results under the heading *untuned* and says in three places that
tuning does better — at 16K, changing the fine-tuning learning rate alone moves
F1 from the reported 91.345 to 91.688. The claim is that a square-root rule plus
linear-epoch warmup is *good enough to hit a fixed target without a sweep*, not
that the rule is right. [SOTA-218](SOTA-218.md) is about drawing a curve you intend to
reason from, and a curve drawn this way is still not one. [THEORY-012](../theory.d/THEORY-012.md) is the
account under both.

**[LIT-265](../literature.d/LIT-265.md) agrees with [LIT-058](../literature.d/LIT-058.md) and cites it saying so** — "learning rate
scaling heuristics with the batch size do not hold across all problems or
across all batch sizes" is [LIT-265](../literature.d/LIT-265.md)'s own summary of it, in its related-work
section, as motivation. The two papers were never in dispute. This record's
reading that they were is the thing being corrected here.

**It is not a claim that LAMB is the current answer.** The paper is from 2019,
its workloads are BERT-Large and ResNet-50, and it predates everything this
record holds about modern pretraining optimizers. [LIT-152](../literature.d/LIT-152.md) reports the same
shape from a 2025 model report: the architecture and Muon together move the
optimal learning rate and batch size upward and make batch-size warmup
unnecessary — a different mechanism reaching the same place, and the reason to
carry the instruction at the top forward rather than the specific algorithm.

## Conditions

**The convergence theory covers less than the algorithm.** Theorem 1 is proved
for simplified LAMB with `beta1 = 0` and `lambda = 0` — no momentum, no weight
decay — while every experiment uses both. The `L_avg`-not-`L_inf` result that
makes the mechanism legible is a statement about the simplified version.

**Scaling efficiency is not throughput.** At 64x hardware it falls to ~76.7% for
BERT's 300M parameters, on gradient communication. The 76-minute figure is a
TPUv3 Pod with that interconnect; a GPU cluster on commodity Ethernet is a
different machine, and what the record recommends there is [SOTA-215](SOTA-215.md) — freeze
Adam's variance and compress the momentum — which is an answer to the
communication cost rather than to the batch size, and composes with this one
rather than replacing it.

**Mixed-batch training is a separate moving part.** The 76-minute run changes
batch size and sequence length together between phases and re-warms the
optimizer at the transition. That re-warmup is tuned, and decreasing the batch
between phases is reported as an instability risk.

## Known implementations

None recorded. The BERT and ResNet-50 runs above are [LIT-265](../literature.d/LIT-265.md)'s own experiments
and belong to the evidence, not to adoption — counting them here would be
[DP-005](../../docs/design-principles.md#dp-5) exactly. That layerwise adaptation is in every framework is
recorded in `consensus_note`, where counting is the right operation.
