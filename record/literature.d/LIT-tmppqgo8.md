---
status: Active
title: 'SmoothGrad: removing noise by adding noise'
version: 1
tags:
- analysis-and-evaluation
- vision-and-graphics
date: '2026-09-26'
published: '2017-06-12'
arxiv: '1706.03825'
first_author: 'Smilkov'
keywords:
- SmoothGrad
- sensitivity maps
- saliency visualization
- gradient smoothing
implementations:
- captum
- saliency
- innvestigate
summary: >-
  Smilkov, Thorat, Kim, Viégas and Wattenberg (2017), [ARXIV-1706.03825](https://arxiv.org/abs/1706.03825). The
  smoothing eight held documents name — averaging the gradient over `n` noisy
  copies of the input, with **10–20% noise** and **`n ≈ 50`**, past which "there
  was little apparent change". Its own evidence is **entirely qualitative and it
  says so**: "since quantitative evaluation of a map remains an unsolved problem,
  we again focus on qualitative evaluation." And its §3.1 visualization lessons
  contain informal statements of two things this record spent two days building
  accounts for: the signed-versus-absolute ambiguity, and the input multiplier
  putting the input's own edges into the map.
---

<!-- inactive-ok-file: SOTA-430 — Proposed, and cited for what it says about this method rather than as advice relied on: this paper is in its pass row, its step 3 is the measurement form of §3.1's colour-scale ambiguity, and its do-not-validate-by-eye rule is the standard this paper's own evidence does not meet. -->
<!-- inactive-ok-file: THEORY-113 — Proposed, and cited for provenance: §3.1 states that account informally in 2017, four years before the measurement it rests on. Naming an antecedent is a claim about who wrote something first, not about whether the account is in force. -->

# LIT-tmppqgo8: SmoothGrad: removing noise by adding noise

Smilkov, Thorat, Kim, Viégas and Wattenberg (2017) —
[ARXIV-1706.03825](https://arxiv.org/abs/1706.03825)

## Key takeaways

- **The method is one line.** Average the vanilla gradient over `n` copies of
  the input perturbed with `N(0, σ²)`. Two hyper-parameters: the noise level `σ`,
  reported as a fraction `σ/(x_max − x_min)`, and the sample count `n`.
- **The numbers, and how they were chosen.** 10–20% noise "seems to balance the
  sharpness of sensitivity map and maintain the structure of the original
  image", and `n > 50` shows "little apparent change" — diminishing returns at
  fifty. Inception on ImageNet, with a matching MNIST figure, and the paper adds
  that "the ideal noise level depends on the input".
- **The evidence is qualitative throughout, and the paper states why.** "Since
  quantitative evaluation of a map remains an unsolved problem, we again focus on
  qualitative evaluation." Both of its assessments — visual coherence and
  discriminativity — are judged by eye, the latter by differencing two classes'
  maps onto a diverging colour scale.
- **It asked a question the record answered yesterday.** "It remains an open
  question to understand which properties affect the discriminativity of a given
  method — e.g. understanding why Guided BackProp seems to show the weakest
  discriminativity." [LIT-730](LIT-730.md) answers it: guided backprop is doing partial
  image recovery, which is class-insensitive by construction.
- **§3.1 is a visualization-practices section and it is the most interesting
  part.** Three lessons, each of which the record has since rebuilt from a later
  paper:

  | §3.1 lesson, 2017 | what the record now holds |
  | --- | --- |
  | "There is considerable ambiguity in how to convert signed values to colors" — and whether absolute value helps is dataset-dependent (MNIST digits are always white, so signed gradients mean something; on ImageNet "taking the absolute value of the gradient produced clearer pictures") | [SOTA-430](../practices.d/SOTA-430.md) step 3, where the signed-versus-absolute choice flips a randomization verdict — three groups, three model families |
  | multiplying by the input "does tend to produce visually simpler and sharper images, although it can be unclear how much of this can be attributed to sharpness in the original image itself … a black/white edge in the input can lead to an edge-like structure on the final visualization even if the underlying sensitivity map has no edges" | [THEORY-113](../theory.d/THEORY-113.md), the input-multiplier account |
  | cap at the 99th percentile, because a few pixels with far-above-average gradients "have the potential to throw off color scales completely" and "without this post-processing step, maps may end up almost entirely black" | nothing — a display artefact that can masquerade as a finding |

- **And a structural objection to gradient⊙input, also 2017.** "Pixels with
  values of 0 will never show up on the sensitivity map. For example, if we
  encode black as 0, the image of a classifier that correctly predicts a black
  ball on a white background will never highlight the black ball." The paper
  still shows results both ways, and gives the case for multiplying: in a linear
  `y = Wx`, `x_i w_i` is what `x_i` contributes.

## Standing in the anthology

**Eight held documents named this paper and none held it.** It is in
[SOTA-430](../practices.d/SOTA-430.md)'s *pass* row, in [SOTA-435](../practices.d/SOTA-435.md) step 3's recommendation, in
[LIT-725](LIT-725.md) twice (Proposition 2.1's infidelity optimum is "a smoothing operation
reminiscent of SmoothGrad on Integrated Gradients", and Theorem 4.1's
meta-algorithm "encompasses Smooth-Grad"), in [LIT-713](LIT-713.md) and [NOTE-365](../notes.d/NOTE-365.md) as a
method that changes under both randomization tests, and in [LIT-729](LIT-729.md),
[THEORY-113](../theory.d/THEORY-113.md) and [THEORY-114](../theory.d/THEORY-114.md) as a gradient method outside both mechanism
accounts.

**So it is the one method in this cluster that nothing faults — and the one with
the least evidence behind it.** It passes both randomization tests ([LIT-713](LIT-713.md)),
it does not carry an input multiplier ([THEORY-113](../theory.d/THEORY-113.md)), it does not converge to
rank 1 ([THEORY-114](../theory.d/THEORY-114.md)), and it is not doing image recovery ([LIT-730](LIT-730.md) leaves the
saliency family alone). Its own paper offers no quantitative result at all.

That is not a contradiction in the record and it is worth being precise about
why. [SOTA-435](../practices.d/SOTA-435.md) recommends restrained smoothing on **[LIT-725](LIT-725.md)'s** evidence —
Theorem 4.1, which is proved, and a measured improvement in infidelity and
max-sensitivity across three datasets — not on this paper's figures. The
practice happens to be sourced to the paper that supplied numbers rather than to
the paper that supplied the method, which is the right way round and was not
deliberate.

**Its §3.1 changes the provenance of [THEORY-113](../theory.d/THEORY-113.md).** That account's history in the
record ran: [LIT-713](LIT-713.md) (2018) suspects the input multiplier and says it does not
measure it; [LIT-725](LIT-725.md) (2021) measures it. The edge-injection observation is
here in 2017, informally, in a section about choosing colour scales — which is
why nobody cites it for mechanism and why the record rebuilt the account from
the 2021 measurement. Recorded on `THEORY-113` v4.

**No practice is filed and no theory.** The parameters belong on
[SOTA-435](../practices.d/SOTA-435.md), which already recommends the smoothing, rather than in a second
practice about the same technique — the call [LIT-728](LIT-728.md) got for occlusion
sensitivity. And the paper offers no mechanism: it does not say *why* averaging
over noise sharpens a map, beyond the observation that the gradient fluctuates
sharply at small scales.

## Limitations

- **Every claim is qualitative, by the authors' own statement.** The parameters
  were selected by looking at pictures, so 10–20% and `n = 50` are defaults with
  no measured objective behind them. [SOTA-435](../practices.d/SOTA-435.md) v2 carries them with that
  provenance attached.
- **One architecture for the headline figures** (Inception on ImageNet), plus
  MNIST in the appendix. The paper's own closing question is "whether the
  de-noising techniques described here generalize to other network architectures
  and tasks".
- **The discriminativity test is two objects and a colour difference.** No
  ground truth, no metric, and the paper says systematic measurement "could also
  be valuable".
- **It is the method [SOTA-430](../practices.d/SOTA-430.md) would forbid validating the way this paper
  validates it.** That practice's negative half is "do not accept a method
  because its maps look like the object", and this paper accepts one on exactly
  that basis — reasonably, in 2017, when it says the quantitative problem was
  unsolved. The record's own position is that it was solved enough by 2019
  ([LIT-725](LIT-725.md)) and that is where the recommendation's support comes from.
