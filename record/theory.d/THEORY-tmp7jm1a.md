---
status: Active
title: 'Layer importance is not uniform with depth: middle layers tolerate deletion and reordering, the first and last do not'
version: 1
tags:
- model-architecture
date: '2026-09-17'
source:
- LIT-tmpyn738
explains: []
summary: >-
  Lad et al. (2024), [LIT-tmpyn738](../literature.d/LIT-tmpyn738.md) — deleting a layer outright, or swapping two
  adjacent ones, at inference and without fine-tuning, leaves 72-95% of top-1
  predictions unchanged. The degradation is localized rather than uniform: the
  first and last layers are fragile, the middle is not, and swapping hurts
  less than dropping. Measured layer by layer across four GPT-2 and four
  Pythia models and confirmed on HellaSwag, ARC-Easy and LAMBADA. Robustness
  grows with depth, so it is not a small-model artifact.
---

<!-- inactive-ok-file: THEORY-tmpvyj77 — Proposed, and named here precisely
     to say the framework is weaker than this measurement. That is the
     reason the two are separate documents. -->

# THEORY-tmp7jm1a: Layer importance is not uniform with depth: middle layers tolerate deletion and reordering, the first and last do not

## Source

Lad et al. (2024), [LIT-tmpyn738](../literature.d/LIT-tmpyn738.md) —
[ARXIV-2406.19384](https://arxiv.org/abs/2406.19384).

## What was actually shown

**The intervention is crude on purpose.** Delete a layer from the forward pass
entirely, or swap two adjacent layers, at inference time, with no fine-tuning
and no repair. Applied to **every** layer in turn, across four GPT-2 and four
Pythia models, scored two ways: KL divergence between the intervened and
nominal output distributions, and the fraction of top-1 predictions that stay
the same.

**Models retain 72-95% of their top-1 predictions.** For an architecture whose
every layer is trained in place, in sequence, that is the result worth
starting from.

**But the average conceals the finding.** Degradation is **not uniform with
depth**. Interventions on the early and final layers cause the most damage;
the middle is robust to both deletion and to minor reordering. The same shape
appears on HellaSwag, ARC-Easy and LAMBADA, so it is not an artifact of the
distributional metrics.

**Swapping hurts less than dropping**, in the middle. So for those layers even
the *order* is partly negotiable, which is a stronger claim than redundancy:
a layer that can be moved is not merely duplicating a neighbour, it is doing
something whose position in the sequence is not what makes it work.

**Robustness increases with the number of layers.** Deeper models tolerate
more, which rules out the reading that this is small-model slack.

**What could have come out the other way.** A transformer trained end to end
in a fixed order had every opportunity to be brittle to both interventions at
every depth, and it is brittle — at exactly two places. The negative result
across the middle is what makes the positive result at the ends interpretable.

## Where the sensitivity is argued to come from

For the first layer the paper gives a structural reason rather than an
empirical one, and it is worth separating from the measurement. The first
layer is the only one mapping from the embedding basis into the residual
stream, and it is a function of the current token alone; ablating it leaves
the rest of the network "blind to the instant context and thrown off
distribution". On that reading the first layer is an extension of the
embedding rather than a layer, which would explain why it behaves unlike
every layer after it.

That is an argument, not a measurement, and it is the entry point to the
four-stage framework — which the record files separately and at a weaker
status, as [THEORY-tmpvyj77](THEORY-tmpvyj77.md).

## What this does not say

**It does not say the middle layers are useless.** 72-95% retention is a large
loss at the top of that range and an enormous one at the bottom, measured on
top-1 agreement rather than on task quality. "Robust" here means degrades
gracefully, not free.

**It is not a pruning result and does not license one.** No practice is filed
from it, deliberately. Deleting a layer at inference to measure sensitivity
and deleting one to ship a smaller model are different claims: the second
needs a quality target, a comparison against a pruning method that repairs
what it removes, and a measurement nobody in this line ran. The record holds
no layer-pruning practice, and this document is not an argument for adding
one.

**Aggregate, not per-token.** The paper's own limitation: the pattern
describes aggregate trends, and individual tokens may take different paths
through the network.

**Five families, one corpus.** Pythia, GPT-2, Qwen 2.5, LLaMA 3.2 and Phi,
124M to 6.9B, on a million tokens of the Pile — and the layer-by-layer
intervention grids are GPT-2 and Pythia. Whether the shape survives at the
scales the practice registry mostly advises on is untested here. The paper
does not isolate what drives the model-specific differences it does see.
