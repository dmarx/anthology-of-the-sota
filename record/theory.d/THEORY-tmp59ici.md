---
status: Proposed
promote_when: >-
  An intervention, not a correlation: a QK-norm model given another way to
  shed attention mass, such as a learnable sink token, an output gate or a
  learned per-head temperature, extended under the same recipe as its
  ungated twin. The account predicts the long-context cost largely
  disappears while QK norm stays in place. A further cross-model correlation
  between sink mass and long-context score would not count, because the
  QK-norm models differ in several things at once.
title: 'QK normalization costs long-context extension because bounding the logits raises attention entropy and removes the sink a head uses to discard mass'
version: 1
tags:
- attention-techniques
- model-stability
- analysis-and-evaluation
date: '2026-10-06'
source:
- LIT-tmpnww11
- LIT-653
extends:
- THEORY-019
explains:
- SOTA-192
summary: >-
  Bertsch et al. (2026), [LIT-tmpnww11](../literature.d/LIT-tmpnww11.md), §5.4 and Fig. 7, with the dispersion
  bound of Veličković et al. (2024), [LIT-653](../literature.d/LIT-653.md). In 26 controlled 7B runs, QK
  norm costs about 4 to 6 HELMET points at 32K. The QK-norm models have
  higher attention entropy, less attention-sink mass and less attention on
  the needle, and sink mass correlates positively with long-context score
  (R² 0.38). The account: QK norm bounds the logit spread, so a head can be
  neither sharp at long range nor able to park surplus mass on a sink. All
  of the evidence is correlational, and QK norm also changed norm order in
  the cleanest pair.
---

<!-- inactive-ok-file: THEORY-061, THEORY-097 — Proposed; named as the
     neighbouring accounts of normalization, not relied on -->

# THEORY-tmp59ici: QK normalization costs long-context extension because bounding the logits raises attention entropy and removes the sink a head uses to discard mass

## Source

Bertsch, Soldaini, Gormley, Neubig, Hajishirzi, Lo and Groeneveld (2026),
[LIT-tmpnww11](../literature.d/LIT-tmpnww11.md) — §4, §5.4, Figs. 7–8, App. B. Veličković, Perivolaropoulos,
Barbero and Pascanu (2024), [LIT-653](../literature.d/LIT-653.md) — the softmax dispersion bound.

## The account

**Two things a head needs at long range, and one bound on both.** To
retrieve one token among tens of thousands, a head must put most of its mass
on it, which needs a large spread between that logit and the rest. When it
has nothing to retrieve, it must put the mass somewhere harmless, and in a
model without gating that is a sink on the first tokens ([THEORY-019](THEORY-019.md)). That
also needs the sink's logit to stand far above the rest. [LIT-653](../literature.d/LIT-653.md) proves that
the largest softmax coefficient over n items is capped at about
(1/n)·exp(δ/θ), where δ is the logit spread. Normalizing queries and keys
bounds their norms, and so bounds δ by the weights' singular values alone.

**So QK norm takes away both.** Long-context extension asks a head to be
sharp over a window many times longer than the one it was trained on. A
model with QK norm reaches it with a flatter attention distribution and a
weaker sink, and it extends worse.

**It widens [THEORY-019](THEORY-019.md) rather than replacing it.** That account says why
sinks form. This one adds that in a model without gating they are part of
how long-context attention works, so suppressing them has a cost unless
something else takes over their job.

## What was measured

- **The cost** (§4, App. A–B). Removing layerwise QK norm and post-norm from
  the Olmo 3 architecture raised HELMET at 32K from 47.5 to 53.7. Adding
  them to the Llama 3 architecture lowered it from 52.4 to 48.5. Headwise
  QK norm was slightly worse than layerwise. Norm order alone was
  inconsistent.
- **The attention statistics** (§5.4, Fig. 7). Over 100 long documents, the
  QK-norm models cluster at higher attention entropy at 32K and lower sink
  mass, in both full-attention and windowed layers. Across the pool, sink
  mass correlates with HELMET at R² 0.38. QK-norm models also put less
  attention on the needle at prefill.
- **What did not separate them.** Retrieval-head scores during generation
  were low and similar for every model. The authors suggest the models may
  be too weak for retrieval heads to show.

## What this does not say

- **Not that the mechanism is established.** Every link is a correlation
  across models that differ in more than QK norm. The cleanest pairs change
  QK norm and norm order together, because post-norm without QK norm
  diverged. Nobody has given a QK-norm model a sink or a gate and checked
  whether the cost goes away. That is the condition in `promote_when:`.
- **Not that sinks are good in general.** The gated-attention paper ([LIT-138](../literature.d/LIT-138.md))
  removes sinks with an output gate and reports better quality and
  stability. This account is consistent with that: a gate gives the head
  another way to shed mass. Whether the gated models also extend better is
  the test in `promote_when:`. Removing a sink is
  harmful only when nothing replaces it.
- **Not that QK norm should be dropped.** The same runs confirm its stability
  benefit (App. D.4). [SOTA-192](../practices.d/SOTA-192.md) records the trade.
- **Not [LIT-653](../literature.d/LIT-653.md)'s claim.** That paper proves the bound and names
  pre-attention normalization as tightening it. It measures neither long
  context in trained language models nor sinks. The connection is this
  account's.

## What it explains

The cost condition in [SOTA-192](../practices.d/SOTA-192.md). It also explains why the Cohere RNoPE paper
([LIT-208](../literature.d/LIT-208.md)) removed QK norm for "poorly shaped attention patterns" in a model
built for long context, and why that paper found sinks in exactly the layers
doing long-range retrieval. It sits beside [THEORY-061](THEORY-061.md), which bounds entropy
from below by the spectral norm of the query-key product, and [THEORY-097](THEORY-097.md),
which argues attention needs normalized vectors and a fitted temperature.
Read together, the record now holds the case for normalizing and a
mechanism for what normalizing costs.
