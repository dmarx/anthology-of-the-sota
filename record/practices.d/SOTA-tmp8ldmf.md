---
status: Proposed
promote_when: >-
  The method pre-trained into a decoder-only model at a scale the practice
  registry advises on — billions of parameters, a modern corpus — with the
  outlier metrics and the post-training-quantization result both reported, and
  the floating-point quality shown not to regress. What would NOT satisfy
  this: another demonstration that activation outliers break INT8, which is
  the problem this addresses rather than evidence the fix works; or a
  quantization result with no floating-point baseline, since the claim is that
  you lose nothing by removing the outliers.
consensus: unreplicated
consensus_note: >-
  One group, one paper. The sibling remedy from the same paper — gated
  attention — was independently confirmed at 15B two years later (LIT-138) and
  is now SOTA-134, which is a reason to take the diagnosis seriously and not
  evidence for this particular fix. Nobody has published clipped softmax at
  scale in either direction.
title: 'Stretch and clip the softmax so an attention head can output exact zeros'
version: 1
tags:
- attention-techniques
date: '2026-09-17'
source:
- LIT-tmpfe659
introduced_by:
- LIT-tmpfe659
implementations: []
summary: >-
  Bondarenko et al. (2023), [LIT-tmpfe659](../literature.d/LIT-tmpfe659.md) — a head that wants to do nothing has
  to drive its softmax input to infinity to approximate exact zeros, and that
  is what creates the activation outliers that break INT8. Stretch the softmax
  to (γ, ζ) and clip back to (0,1) and zeros become reachable from a finite
  input. On BERT-base: W8A8 perplexity 1294 → 4.55, max infinity-norm 735 →
  20, and the FP16 model gets slightly better rather than worse. Evidence is
  BERT-base, OPT-125M and ViT-S/16 — small and encoder-heavy.
---

# SOTA-tmp8ldmf: Stretch and clip the softmax so an attention head can output exact zeros

## Source

Bondarenko et al. (2023), [LIT-tmpfe659](../literature.d/LIT-tmpfe659.md) —
[ARXIV-2306.12929](https://arxiv.org/abs/2306.12929), NeurIPS 2023.

The reason it works is [THEORY-tmp1rmwn](../theory.d/THEORY-tmp1rmwn.md): the
softmax denominator forces a head to place its mass somewhere, so a head with
nothing to attend to can only approach a no-op by making its scores extreme.
This gives it a way to reach zero in finite range instead.

## The change

    clipped_softmax(x; ζ, γ) := clip((ζ − γ)·softmax(x) + γ, 0, 1)

with `γ ≤ 0` and `ζ ≥ 1`. Stretch the output to `(γ, ζ)`, clip back to
`(0,1)`. Exact zeros are now reachable — values below `−γ/(ζ−γ)` round to
zero — and a clipped value contributes **no gradient**, so nothing keeps
driving the score outward.

It is a drop-in replacement for the softmax and adds no parameters.

## What it bought, on BERT-base

| | FP16 ppl ↓ | max ‖x‖∞ | avg kurtosis | W8A8 ppl ↓ |
|---|--:|--:|--:|--:|
| vanilla | 4.49±0.01 | 735±55 | 3076±262 | **1294±1046** |
| `γ = −0.03` | **4.41±0.01** | **20±1** | **80±6** | **4.55±0.01** |

Two things worth separating. INT8 post-training quantization goes from
**broken to working** — 1294 perplexity is not a degraded model, it is a
destroyed one. And the floating-point model gets slightly *better*, so the
outliers were not carrying something the model needed.

`γ < 0` is where essentially all of the improvement comes from; stretching
only the top end (`ζ > 1`) does almost nothing. Reported across BERT-base
(109M), OPT-125M and ViT-S/16 on ImageNet-1K, each trained twice with each
quantization run repeated three times.

## What this does not claim

**It has to be pre-trained in.** This is an architectural change that shapes
how outliers form during training, not a post-hoc quantization technique. It
does nothing for a checkpoint you already have — which is the whole
difference between it and the calibration-side literature.

**The scale is the reason for `Proposed`.** 109M encoder, 125M decoder, 22M
vision. Nothing here is at the scale the practice registry mostly advises on,
and the outlier phenomenon is known to intensify with size, so the
extrapolation runs in the direction where it has not been checked.

**Its sibling has better standing.** Gated attention, from the same paper, was
confirmed at 15B by an independent group and is [SOTA-134](SOTA-134.md),
`Active`. That is evidence for the shared *diagnosis*, not for this remedy —
the two are different interventions and only one of them has been scaled.

**Untested against the third option.** `softmax₁` — one added to the
denominator ([LIT-tmpeajzz](../literature.d/LIT-tmpeajzz.md)) — reaches for the
same property by a simpler route and has never been evaluated against this.

## Known implementations

- None known outside the paper.
