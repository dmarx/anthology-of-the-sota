---
number: 76
status: Active
formerly:
- THEORY-tmp9m644
title: 'Under the standard parametrization a learning rate that stays stable as width grows leaves the network training as a kernel, and µP is the parametrization that escapes this by updating every layer maximally'
version: 1
tags:
- training-optimization
- model-stability
- analysis-and-evaluation
date: '2026-09-22'
source:
- LIT-548
explains:
- SOTA-143
summary: >-
  Yang and Hu (2020), [LIT-548](../literature.d/LIT-548.md) — Tensor Programs IV. Under SP a learning
  rate large enough to move the features blows up the logits, and one small
  enough to be stable (`O(1/width)`) leaves the wide limit a kernel machine.
  µP rescales the readout and first layer so a width-independent rate is both
  stable and maximal for every layer. A theorem for SGD on MLPs. Why the
  *optimum* then transfers, and under Adam, is TP-V's claim, not this one.
extended_by:
- THEORY-037
---

<!-- inactive-ok-file: THEORY-024 — Proposed, named as the rival frame this account does not depend on, not leaned on -->

# THEORY-076: Under the standard parametrization a learning rate that stays stable as width grows leaves the network training as a kernel, and µP is the parametrization that escapes this by updating every layer maximally

## Source

Yang and Hu (2020), [LIT-548](../literature.d/LIT-548.md) — read as [NOTE-292](../notes.d/NOTE-292.md).

## What it explains

| practice | what it says to do | what this says it is |
|---|---|---|
| [SOTA-143](../practices.d/SOTA-143.md) | parametrize with µP, tune narrow, transfer across width | the parametrization whose maximum stable learning rate has no width exponent, so there is a width-free rate to transfer |

## The account

Take a hidden layer of width `n` and one SGD step. The update to a middle
weight matrix is an outer product, `δW ∝ dh xᵀ`. The next forward pass
multiplies it by an activation vector *correlated* with `x`. That inner
product is a sum of `n` correlated terms, so it grows like `n` (Law of Large
Numbers), not like `√n` (the Central Limit Theorem, which governs the random
initialization). Initialization and update therefore scale differently with
width, and one scaling of the learning rate cannot fit both.

Under the standard parametrization (PyTorch's default fan-in init, no
multipliers) this forces a choice:

- **Learning rate `ω(1/n)`:** after one step the logit changes by
  `Θ(n^(1−c))`, so it blows up as width grows (§4, Eq. 13)
- **Learning rate `O(1/n)`:** stable, but then each feature coordinate moves
  by `O(1/√n)`, so in the limit the features are frozen and the function
  evolves by kernel gradient descent (Theorem 4.1)

The Dynamical Dichotomy (Corollary 3.9) says the second outcome is not
specific to SP. Every stable, nontrivial parametrization in the family either
learns features or is a kernel, and which one is decided by a single exponent
`r`. SP sits on the kernel side at every stable learning rate.

µP makes three changes: it scales the readout by `1/√n`, gives the first
layer an effective update `n` times larger, and holds the learning rate
constant. With these, `r = 0` for every layer, so every weight's update
contributes `Θ(1)` to the next layer's preactivation and neither end blows
up. Among the parametrizations in the family it is the unique one with that
property (Appendix C.1).

For the practice, this is the sense in which "the learning rate does not
move": the maximum stable learning rate's scaling exponent in width is zero.
Under SP it is `−1`, so a rate at the edge of stability on the narrow model
is above that edge on the wide one, by the width ratio.

## What was actually shown

The classification is a theorem, proved for MLPs trained by SGD with
`tanh` or a smoothed ReLU (Assumption 3.1). It made a prediction about real
networks that could have failed: that the largest usable learning rate should
scale like `1/width` under SP and stay put under µP. The paper plots this on
two-hidden-layer ReLU MLPs on CIFAR-10 at widths 512–8192 (§1, page 3
figure). The SP curves line up only when the x-axis is `log(lr × width)`, and
the µP curves line up on `log(lr)`.

The real-task experiments (Word2Vec, Omniglot) test a different claim: that
the feature-learning limit is *better* than the kernel limit. They use the
exact infinite-width limit of a one-hidden-layer **linear** network, because
the nonlinear limit is intractable to compute beyond a few steps (§8).

## What this does not say

**It is about where the learning rate stops being stable, not where it is
best.** The theorem fixes the scaling of the *maximum* stable rate. That the
*optimal* rate also stops moving, so a narrow proxy's tuned value is right for
the wide model, is TP-V's empirical claim ([LIT-148](../literature.d/LIT-148.md)). [SOTA-143](../practices.d/SOTA-143.md) rests on that
claim, and this account makes it plausible without proving it. The window
[LIT-501](../literature.d/LIT-501.md) measures around the optimum is outside this theory's scope entirely.

**It is SGD.** The abc-family puts one learning-rate exponent on every layer.
Under Adam the per-layer exponents differ, and the Adam form of µP that
production recipes use is derived in TP-V, not here.

**It says nothing about depth, batch size or training length.** Width is the
only limit taken, and training time is held `O(1)` in width. Depth is
[THEORY-037](THEORY-037.md)'s subject.

**It does not say the standard parametrization fails to learn features at
any finite width.** The paper says so explicitly (footnote 6). The claim is
about the limit and about the exponents, which is what matters when a
proxy's hyperparameters are carried across a width ratio of 16 or 100.

**It is not a claim about geometry or duality.** [THEORY-024](THEORY-024.md) frames µP as a
partial approximation of a duality map. This account derives it from
scaling exponents and stability alone. Both describe the same object, and
neither requires the other.

## Why `Active`

The core is a proof, not an argument. The one prediction it makes about
training — how the maximum learning rate scales with width under each
parametrization — was measured and held. Groups outside the authors' own have
built on the parametrization rather than contested it: u-µP ([LIT-149](../literature.d/LIT-149.md)),
CompleteP ([LIT-150](../literature.d/LIT-150.md)) and the depth-width spectral condition ([LIT-462](../literature.d/LIT-462.md)). This is
evidence that the object is sound. It is not a replication of the theorem,
which needs none. Within the record, [LIT-437](../literature.d/LIT-437.md) and [THEORY-037](THEORY-037.md) re-derive or
extend it. The claim is kept to what the theorem covers. What it does not
cover is listed above.
