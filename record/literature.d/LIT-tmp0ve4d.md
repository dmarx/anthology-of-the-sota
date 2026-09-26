---
status: Active
title: 'On the (In)fidelity and Sensitivity for Explanations'
version: 1
tags:
- analysis-and-evaluation
- representation-and-encoding
date: '2026-09-26'
published: '2019-01-27'
arxiv: '1901.09392'
first_author: 'Yeh'
keywords:
- infidelity
- max-sensitivity
- saliency explanations
- SmoothGrad
- explanation evaluation
implementations:
- captum
- saliency_evaluation
summary: >-
  Yeh, Hsieh, Suggala, Inouye and Ravikumar (2019), [ARXIV-1901.09392](https://arxiv.org/abs/1901.09392), NeurIPS
  2019. The definitions behind the two numbers [LIT-724](LIT-724.md) reports and this record
  had started quoting: **infidelity** and **max-sensitivity**. Two properties a
  reader needs and neither citing document carried — max-sensitivity is
  minimised by a **constant explanation**, and infidelity is defined relative to
  a chosen perturbation distribution for which several existing methods are each
  the optimum. It also reproduces [SOTA-430](../practices.d/SOTA-430.md)'s metric split on a third model
  family, and builds the planted-feature setting [SOTA-430](../practices.d/SOTA-430.md)'s `promote_when` asks
  for while pointing it at a different question.
---

<!-- inactive-ok-file: SOTA-430 — Proposed, and that is this note's subject rather than its support: the practice is cited for the metric split its step 3 warns about, for the promote_when this paper nearly meets, and for the Condition its infidelity figures sit in. Whether the recommendation is in force is beside every one of those. -->

# LIT-tmp0ve4d: On the (In)fidelity and Sensitivity for Explanations

Yeh, Hsieh, Suggala, Inouye and Ravikumar (2019) —
[ARXIV-1901.09392](https://arxiv.org/abs/1901.09392)

## Key takeaways

- **Infidelity, Definition 2.1**, generalising the completeness axiom from a
  single baseline to a distribution of perturbations:

      INFD(Φ, f, x) = E_{I ~ μ_I}[ (Iᵀ Φ(f, x) − (f(x) − f(x − I)))² ]

  It asks whether the attribution, dotted with a perturbation, predicts the
  change in the function that perturbation causes. **`μ_I` is a free choice**,
  and the paper lists several: difference-to-baseline, subsets of it, a noisy
  baseline, and random square patches for images.

- **The metric has a known optimum, and it is an existing method.**
  Proposition 2.1: the infidelity-minimising explanation is kernel-smoothed
  Integrated Gradients with kernel `IIᵀ` — "a smoothing operation reminiscent of
  SmoothGrad on Integrated Gradients (or any explanation that satisfies the
  Completeness Axiom)". Propositions 2.2–2.5 then show several *other* published
  explanations are each the optimum for some specific `μ_I`, and the paper
  checks this by construction: under SHAP's own perturbation, SHAP has the
  lowest infidelity. So an infidelity comparison between methods is in part a
  statement about which perturbation distribution was chosen.

- **Max-sensitivity, Definition 3.1**, and the property that governs how it can
  be used:

      SENS_MAX(Φ, f, x, r) = max_{‖δ‖ ≤ r} ‖Φ(f, x + δ) − Φ(f, x)‖

  chosen over a local-Lipschitz variant because Lipschitz continuity "may be
  unbounded in a deep network (such as using ReLU activation function for
  gradient explanations, which is a common setting)", while max-sensitivity is
  finite and Monte-Carlo estimable. And: **"the optimal explanation that
  minimizes the above max-sensitivity measure is simply a constant explanation
  that just outputs a (potentially nonsensical) constant value for all possible
  test inputs."** The paper raises a second objection in the same breath —
  a faithful explanation of a sensitive model *should* be sensitive, so driving
  sensitivity down can cost fidelity.

- **Smoothing lowers sensitivity provably and infidelity empirically.**
  Theorem 4.1 bounds the smoothed explanation's max-sensitivity by the
  kernel-average of the unsmoothed one's. Experimentally, "Smooth-Grad improves
  both sensitivity and infidelity for all base explanations across all
  datasets" (MNIST, CIFAR-10, ImageNet) — which the paper notes is the
  non-obvious half, since smoothing might have been expected to cost fidelity.

- **A third independent reproduction of the signed-versus-absolute split.**
  Table 2, ResNet-50 with the final fully-connected layer randomized, rank
  correlation between the original and randomized model's explanations:

  | | Grad | Grad-SG | IG | IG-SG | Square |
  |---|---|---|---|---|---|
  | signed | 0.17 | 0.10 | 0.18 | 0.16 | 0.13 |
  | absolute value | 0.57 | 0.62 | 0.61 | 0.62 | **0.28** |

  "All explanations without the absolute value pass the sanity check, but the
  rank correlation for explanations with the absolute value between the
  original model and the randomized model is high." Same explanations, same
  randomization, opposite verdicts.

- **A planted-feature setting, pointed somewhere else.** Bird-versus-frog
  images with a caption occupying one half. At noise `p = 0` the trained model
  relies on the image (image-only accuracy 0.9, caption-only 0.5); at `p = 0.6`
  it relies on the caption (0.98 against 0.5). Both models test above 0.95, so
  which half the model uses is **known by construction**. 16 users, 8 tasks
  each, asked to infer that half from the explanation:

  | | Grad | Grad-SG | IG | OPT |
  |---|---|---|---|---|
  | infidelity | 0.55 | 0.38 | 0.35 | **0.00** |
  | human accuracy | 0.47 | 0.50 | 0.53 | **0.88** |

  OPT is optimal for the perturbation "left half or right half", so its zero is
  by construction; the ordering of the other three is not.

## Standing in the anthology

**The record started quoting these two metrics yesterday and did not hold their
definition.** [LIT-724](LIT-724.md) reports infidelity and max-sensitivity throughout,
including the 2.84 → 1.27 × 10⁷ climb down the Inception randomization cascade
that [SOTA-430](../practices.d/SOTA-430.md) now carries as a Condition, and neither document could say
what either number is. Same shape as the precision/recall filing ([LIT-703](LIT-703.md)) a
day earlier: an instrument used to carry a quantitative claim, with its defining
paper unheld.

Two of its properties change how the numbers already in the record should be
read, and are why [SOTA-tmp34edx](../practices.d/SOTA-tmp34edx.md) is filed:

1. `LIT-724` reports max-sensitivity "remains almost unchanged" under
   randomization, alongside infidelity as a pair of trustworthiness measures.
   A measure minimised by a constant explanation cannot carry that weight on
   its own, and neither paper says so.
2. Infidelity's perturbation distribution is a free parameter with a
   method-dependent optimum. `LIT-724` specifies its perturbations — normal
   `N(0, 0.03)`, and `x − x₀` for global IG — which is the right practice and
   is exactly what makes its numbers comparable only to themselves.

**The metric split now has three groups behind it.** [LIT-713](LIT-713.md) found it on
Inception and MNIST (signed rank correlation against SSIM and absolute rank
correlation), `LIT-724` on Inception and BERT (SSIM against Spearman), and this
paper on ResNet-50 (signed against absolute rank correlation). Three model
families, three metric pairs, the same result — which makes `SOTA-430`'s step 3
the best-supported thing in a practice whose headline is still `Proposed`.

**It builds the experiment `SOTA-430`'s `promote_when` asks for and points it at
a different question.** That `promote_when` wants both randomization tests run
"where the true dependence of the output on the input is KNOWN by
construction — a synthetic task or a planted feature". This paper has the
planted feature, in Figure 4's caption-versus-image construction, and it has the
randomization test, in Table 2. It never crosses them: the planted feature
validates *infidelity against human judgement*, and the randomization test runs
on ImageNet with no ground truth. **The experiment is one table-join away inside
a published paper and nobody has run it**, which sharpens the `promote_when`
rather than meeting it.

**No theory is filed.** Proposition 2.1's "the optimum is smoothed IG" is a
derivation from the definition, not a contested explanation of why something
works — the same call made about the conditional-score decomposition in
[LIT-722](LIT-722.md). Filing it would be filing on novelty.

## Limitations

- **The infidelity-optimal explanations are optimal by construction.** Square
  and Noisy Baseline win on the infidelity defined by their own perturbations,
  and the paper says so. The evidence that this tracks something real is the
  human study and the visualizations, not the infidelity table.
- **The human study is small**: 16 users, two models, four explanations, eight
  tasks each, one synthetic construction.
- **The sanity-check table is one randomization step** — the final
  fully-connected layer — not [LIT-713](LIT-713.md)'s cascade.
- **Title drift.** arXiv's metadata reads "…Sensitivity *for* Explanations";
  the rendered paper and the NeurIPS 2019 version read "…Sensitivity *of*
  Explanations". The `arxiv:` field is what resolves, so the arXiv spelling is
  the one recorded here.
