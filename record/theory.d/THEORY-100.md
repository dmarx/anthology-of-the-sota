---
number: 100
status: Proposed
formerly:
- THEORY-tmp3s87v
promote_when: >-
  A second group training matched models under different optimization settings
  and reproducing the separation — ideally including a model deliberately
  trained to HAVE outliers and one trained not to, at the same scale and
  quality. Or a public frontier model whose report says its weight decay,
  dropout or dtype was chosen with post-training quantization in view, and
  whose activations lack the outlier structure. What would NOT meet it:
  another model that quantizes well (which could be any number of things), or
  further measurement of LayerNorm gain spread, which is the correlate this
  account already rests on.
title: 'Activation outliers are a product of pre-training optimization choices, not an emergent property of scale'
version: 1
tags:
- numerics-and-precision
- capability-thresholds
date: '2026-09-24'
source:
- LIT-656
explains:
- SOTA-399
summary: >-
  Ahmadian et al. (2023), [LIT-656](../literature.d/LIT-656.md). The sharp post-training quantization
  failure above ~6B was described as emergent. Hold the architecture fixed and
  vary weight decay, dropout, gradient clipping and half-precision format, and
  the failure moves with those instead: 0.09% degradation against 1.36% at 6B,
  and a 52B model that loses nothing where OPT-66B loses about 42%. **The
  discontinuity is in the recipe, not the parameter count.**
---

<!-- inactive-ok-file: SOTA-399 — Proposed, filed in this same contribution as the practice this
     account explains; the relation is declared, so the citation is the
     relation. Both rest on the same single study, which is the state being
     recorded rather than a problem. -->
# THEORY-100: Activation outliers are a product of pre-training optimization choices, not an emergent property of scale

## Source

Ahmadian, Dash, Chen, Venkitesh, Gou, Blunsom, Üstün and Hooker (2023),
`LIT-656`.

## The claim

Large-magnitude activation outliers in a handful of feature dimensions are
what breaks naive INT8 quantization, and their appearance above roughly 6B
parameters was read as an emergent property of scale — behaviour absent in
small models and present in large ones.

This account says the size is a confound. Hold the architecture fixed and
vary only the optimization conditions, and quantization sensitivity tracks
**weight decay, dropout, gradient clipping and the half-precision format**,
not the parameter count. The proposed mechanism is the LayerNorm gain: in a
pre-norm block it sets the spread of the activations entering the projections,
its standard deviation is larger in the variants that degrade, and settings
that keep weights small keep it small.

The consequence for a practitioner is `SOTA-399`. The consequence for
the record is that a cliff attributed to scale had a second variable nobody
was holding fixed — **the two public models the story was measured on differ
in training dtype**, and one of them has its LayerNorm gains hardcoded.

## What it is evidence for, and how strong

The design is what makes it more than a demonstration: same architecture, one
axis at a time, every variant from random initialization, and — the control
that matters — **comparable pre-quantization quality across variants**. So the
comparison is between models of similar quality that differ in how they
survive quantization.

The separation is large. **0.09% degradation at weight decay 0.1 against 1.36%
at 0.001**, and at 52B a model that *gains* 0.08% on the zero-shot average
after plain INT8 while OPT-66B is reported to lose about 42%.

## Why `Proposed`

**One group, one architecture family, one set of models.** The counter-example
is to inevitability, and a single counter-example does that job — but the
positive claim, that these four knobs are the operative ones, rests on their
runs alone.

**The mechanism is a correlate.** `STD(g)` of the LayerNorm gain is higher in
the degrading variants, and 2× higher for fp16 than bf16. Nobody has
intervened on the gain distribution directly while holding the optimizer
fixed, so gain spread is measured alongside the effect rather than shown to
cause it.

**The negative result inside it is not fully explained.** They could not make
the published outlier-detection threshold work across their variants, and
found no adaptation that correlated with quantization sensitivity even after
corresponding with its authors. That is consistent with this account — if
outliers are recipe-dependent, a threshold calibrated on one recipe should
generalise badly — and it is also consistent with the detection criterion
simply being fragile. The account does not distinguish them.

## What it does not say

**It does not say outliers are not real.** They are, in OPT and BLOOM, and
`SOTA-355` handles them correctly for models that have them.

**It does not say every model can be made quantization-friendly.** It says
the failure is not a function of size alone, which is a weaker and much more
useful claim.

**It does not price the knobs.** Weight decay, dropout and clipping are chosen
for other reasons, and this account is silent on what the
quantization-friendly settings cost elsewhere beyond the observation that
pre-quantization quality was comparable in their runs.

## Why it matters past quantization

The paper's own framing, and the reason it carries `capability-thresholds`:
if one property described as emergent turns out to be conditioned by
optimization choices, that is a reason to ask the question of the others. A
discontinuity measured across a family of models trained by different groups
with different recipes is not the same object as a discontinuity measured
across a family trained identically at increasing size, and the literature
frequently has only the first kind.
