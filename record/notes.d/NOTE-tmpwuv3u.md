---
status: Read
paper: LIT-tmpc05l0
title: 'One metric that separates transformers from every other architecture, and what it buys'
version: 1
date: '2026-09-22'
summary: >-
  Read for whether the record wants an inductive-bias claim. It does, because
  the claim comes with a computable scalar rather than an adjective, and the
  scalar does four jobs — separates architectures, predicts robustness,
  correlates with flatness, and moves during a grokking plateau. The fourth
  is the one this record has an existing use for.
---
<!-- inactive-ok-file: THEORY-041 — Proposed, named alongside THEORY-035 and
     SOTA-012 as the record's existing accounts, to say what this measure adds
     that they do not. -->

# NOTE-tmpwuv3u: One metric that separates transformers from every other architecture, and what it buys

## Contribution

Take sensitivity — the probability that the output changes under a random
perturbation of one input token — which was previously studied for Boolean
functions, extend it to real data modalities, and show it functions as a
unified description of the transformer's inductive bias.

## Key results

**The definition generalizes.** Definition 4.1 computes sensitivity of a model
`Φ` over dataset `D` under a perturbation distribution `P`: Gaussian
`N(0, σ²I)` per patch for images, uniform over the vocabulary for synthetic
token tasks. The Boolean case is the anchor where theory is available.

**The theoretical base is inherited and extended.** On Boolean functions,
sensitivity relates to the degree of the representing multilinear polynomial
— Huang's `D(f) ≤ S(f)²` — and to decision-tree size, so low sensitivity is
low complexity in several established senses. The paper proves transformers
show a low-sensitivity bias in the NTK regime by way of spectral bias, and
proves separately that low sensitivity implies better robustness.

**The architecture separation.** Transformers have lower sensitivity than
MLPs, CNNs, ConvMixers and LSTMs, on both vision and language, compared at
similar training accuracy — which is the control that makes the comparison
mean something.

**Three implications, in the paper's own order.** Sensitivity correlates with
robustness and can be *regularized for*, improving robustness on CIFAR-10-C
beyond the architecture's default. It corresponds to flatter minima. And on
modular addition it decreases while the training loss is flat, tracking the
stages of grokking.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Transformers have lower sensitivity than other architectures | strong | multiple architectures, two modalities, matched training accuracy |
| C2 | Low sensitivity is a simplicity bias | strong in the Boolean case | established equivalences, plus an NTK-regime proof |
| C3 | Low sensitivity implies better robustness | proved in the Boolean setting, correlational elsewhere | theorem plus CIFAR-10-C |
| C4 | Sensitivity regularization improves robustness | moderate | an intervention, on one corruption benchmark |
| C5 | Sensitivity tracks flatness | moderate | correlational |
| C6 | Sensitivity is a grokking progress measure | suggestive | one synthetic task, modular addition |

## Limitations

**The theory is in the Boolean and NTK regimes; the experiments are not.** The
proofs live where analysis is possible and the interesting claims live on
CIFAR and language. That gap is standard and should still be stated: nothing
proves the extended sensitivity notion inherits the Boolean properties.

**C6 rests on modular addition.** The task where grokking is easiest to
produce and least like anything deployed. A progress measure demonstrated
there is a candidate, not an instrument.

**The perturbation distribution is a choice.** Sensitivity is defined relative
to `P`, and the numbers move with it. The paper fixes sensible choices per
modality; nothing shows the architecture ranking is invariant to them, which
is the shape of failure this record has been counting all week.

**Architecture comparisons at matched training accuracy are not matched
compute or matched parameters**, so "transformers are less sensitive" carries
whatever the training budget carries.

## Bearing on the record

**The grokking result has an existing home.** [SOTA-200](../practices.d/SOTA-200.md) says to
check whether an emergent capability is a metric artefact, and its sources
include the reverse-engineering that recovered continuous progress beneath one
network's discontinuity. Sensitivity is a progress measure requiring no
reverse engineering and defined for any architecture, which is a strictly more
usable instrument — *if* it generalizes past modular addition. The record does
not fold it into the practice on one synthetic task, and names it here so the
next person checking an apparent jump knows a cheap candidate exists.

**It is the record's first architecture-comparable inductive-bias scalar.**
[THEORY-041](../theory.d/THEORY-041.md) describes conditioning drift,
[THEORY-035](../theory.d/THEORY-035.md) describes sharpness rising to the step size's
tolerance, [SOTA-012](../practices.d/SOTA-012.md) relates sharpness to test error. All are
properties of weights or of the landscape. This is a property of the learned
*function*, which is what makes it comparable across architectures that share
no parameterization.

**The robustness ranking is not why this is filed.** "Transformers are more
robust than CNNs" is a leaderboard claim and [DP-005](../../docs/design-principles.md#dp-5) is about
what adoption and comparison do not establish. The scalar is the contribution.

## Open questions

- **Does sensitivity track progress on a real plateau?** Modular addition is
  the easy case. One language or vision run with an apparent capability jump,
  sensitivity plotted alongside, would turn C6 into something
  [SOTA-200](../practices.d/SOTA-200.md) could cite as an instrument.
- **Is the architecture ranking invariant to the perturbation distribution?**
  One sweep over `P` would settle whether this is a fact about models or a
  fact about the noise chosen to probe them.
- **Does sensitivity regularization cost accuracy?** The robustness gain is
  reported; the trade, if any, is not prominent.
