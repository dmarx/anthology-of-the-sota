---
status: Proposed
promote_when: >-
  The curve extended — a second target model, or a second benchmark, or a data
  range wider than the one reported — showing speedup still rising. What would
  not satisfy it: another draft architecture reporting a high speedup, which
  is a claim about that architecture rather than about the returns to data;
  the content here is that the returns do not flatten.
consensus: unreplicated
consensus_note: >-
  One group, one target model, one benchmark, and a data range that is not
  large. The architecture ships in SGLang, which is adoption of the method and
  not a second measurement of the scaling claim.
title: "Scale the draft model's training data, once nothing constrains it to predict the target's features"
version: 1
tags:
- inference-optimization
date: '2026-09-16'
source:
- LIT-185
introduced_by:
- LIT-185
extends:
- SOTA-227
implementations: []
summary: >-
  Draft models had stopped improving with more training data, and [LIT-185](../literature.d/LIT-185.md)
  identifies why: EAGLE trained its draft to predict the target's hidden
  features and read tokens off them, which supplies multi-step training signal
  and caps expressiveness. Remove the constraint — predict tokens directly,
  fuse features from several depths, and simulate the multi-step draft during
  training — and the speedup rises with the data instead of flattening. Up to
  6.5x, about 1.4x over the previous version, on roughly 8x the data.
---

<!-- inactive-ok-file: ADR-041 — Proposed, and cited as the decision under
     which this practice declines to file the draft's layer and data
     settings. The practice does not rest on it. -->

# SOTA-tmpe5h20: Scale the draft model's training data, once nothing constrains it to predict the target's features

## What to do

If you train your own draft model for speculative decoding ([SOTA-227](SOTA-227.md)), treat
its training data as a lever that keeps paying, and remove the thing that
stops it paying:

- **Predict tokens directly.** Do not train the draft to reproduce the
  target's hidden features and derive tokens from them.
- **Fuse features from several depths** of the target rather than reusing the
  top layer alone.
- **Simulate the multi-step draft during training** — feed the draft's own
  step-one output into step two — which [LIT-185](../literature.d/LIT-185.md) calls *training-time test* and
  which is not optional once the feature loss is gone.

Then scale the data. [LIT-185](../literature.d/LIT-185.md) uses roughly 8x EAGLE's and reports the speedup
still climbing.

## Why

**The ceiling was an objective, not a capacity limit.** Predicting the
target's features is a useful scaffold: it gives the draft a signal for
multi-step generation that pure token prediction does not. It is also a
constraint on what the draft can express, and [LIT-185](../literature.d/LIT-185.md)'s observation is that it
is the binding one — remove it and first-token acceptance improves
immediately with more data.

**Removing it alone breaks the second step**, which is the part worth
understanding rather than copying. Without the feature loss, the draft's
step-one output no longer lands near the ground-truth feature that step two
was trained against, so step-two acceptance collapses. Training-time test
closes that gap by making the training distribution the serving distribution.
The three changes are one change.

**And the reason top-layer features were never enough**: for a full-rank LM
head, the top-layer feature is information-equivalent to the *next* token's
logits. Predicting the *next-next* token from it is asking for information it
provably does not carry. Intermediate layers have it, and only become usable
once the feature loss is removed.

## What it is worth

Up to **6.5x** speedup, about **1.4x over EAGLE-2** at batch size 1, across
five tasks on both chat and reasoning targets — MT-bench and GSM8K, at
temperature 0.

And, separately: **+40% throughput at batch 64** in SGLang. That number
belongs to [SOTA-227](SOTA-227.md)'s conditions more than to this practice, and it is
recorded there.

## Conditions

**You have to be training the draft.** Everything here is about how a draft is
built. If you are using someone else's, [SOTA-227](SOTA-227.md) is the practice and this one
is why theirs improved.

**The draft needs the target's intermediate layers.** That rules it out for a
target served behind an API, and couples the draft to a specific target — with
nothing published about what acceptance does when that target is updated.

**"Scaling law" is the paper's word for a trend.** One target, one benchmark,
a data range that is not large, and no fitted exponent or range of validity.
The claim this practice makes is that returns had flattened and no longer do —
not that a particular curve holds.

**The two architectural changes are not ablated apart.** Direct token
prediction and multi-layer fusion are motivated together and measured
together, so their separate contributions are not recoverable from this paper.

**The settings are algorithm-local and stay in the reading.** Layer choices,
fusion details and data volumes belong to [NOTE-tmpoib77](../notes.d/NOTE-tmpoib77.md) under [ADR-041](../decisions.d/ADR-041.md).

## Known implementations

- SGLang ships the method. That is adoption of the architecture, not an
  independent measurement of the scaling claim, and is counted in
  `consensus_note` per [DP-005](../../docs/design-principles.md#dp-5).
