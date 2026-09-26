---
status: Active
consensus: unreplicated
consensus_note: >-
  One group for both properties, and replication is the wrong test for most of
  it: the constant-explanation minimiser follows from max-sensitivity's own
  definition, and "several published methods are each optimal for some
  perturbation" is Propositions 2.2–2.5 rather than a measurement. What is
  empirical is that the ordering moves with the perturbation, and the paper
  demonstrates that by construction rather than by sweeping it. The one part
  with independent support is the sibling claim this shares with SOTA-430 step
  3 — that a similarity metric's choice flips the verdict — which three groups
  have now found (LIT-713, LIT-724, LIT-tmp0ve4d). `Active` because the
  cautions cost nothing to follow and the alternative is a comparison nobody
  can reproduce. Read as of 2026-09.
title: 'Never rank attribution methods by a single faithfulness or stability score, and report the perturbation distribution when you report infidelity'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-26'
source:
- LIT-tmp0ve4d
introduced_by:
- LIT-tmp0ve4d
extends:
- SOTA-430
implementations: []
summary: >-
  Yeh et al. (2019), [LIT-tmp0ve4d](../literature.d/LIT-tmp0ve4d.md). **Max-sensitivity is minimised by a constant
  explanation** — an explanation that ignores the input entirely wins it — so it
  can never be a quality score on its own. **Infidelity is defined relative to a
  perturbation distribution** you choose, and Propositions 2.2–2.5 show several
  published methods are each the optimum for some choice, which the paper
  confirms by giving SHAP the lowest infidelity under SHAP's own perturbation.
  Both cautions are free to follow: report the pair, and name the perturbation.
---

<!-- inactive-ok-file: SOTA-430 — Proposed, and declared in `extends:`; this practice is the same warning one level down, about the faithfulness metrics rather than the similarity metrics. Extending a not-yet-in-force practice is the normal case: what is Proposed there is the randomization recommendation, not the metric caution this builds on. -->

# SOTA-tmp34edx: Never rank attribution methods by a single faithfulness or stability score, and report the perturbation distribution when you report infidelity

## Source

Yeh, Hsieh, Suggala, Inouye and Ravikumar (2019), [LIT-tmp0ve4d](../literature.d/LIT-tmp0ve4d.md) —
NeurIPS 2019, §2–3.

## Do this

1. **Report infidelity and sensitivity together, never either alone.** They
   have opposite degenerate optima. Max-sensitivity,

       SENS_MAX(Φ, f, x, r) = max_{‖δ‖ ≤ r} ‖Φ(f, x + δ) − Φ(f, x)‖

   is minimised by **a constant explanation** — the paper's words: "the optimal
   explanation that minimizes the above max-sensitivity measure is simply a
   constant explanation that just outputs a (potentially nonsensical) constant
   value for all possible test inputs." An attribution that ignores the input
   scores perfectly. Infidelity has no such degenerate winner, but it is the
   one that moves with the perturbation choice, below.

2. **Name the perturbation distribution whenever you report an infidelity
   number.** Infidelity is

       INFD(Φ, f, x) = E_{I ~ μ_I}[ (Iᵀ Φ(f, x) − (f(x) − f(x − I)))² ]

   and `μ_I` is yours to pick: difference-to-baseline, a subset of it, a noisy
   baseline, random square patches. Propositions 2.2–2.5 show that several
   published explanations are each the infidelity optimum under some `μ_I`,
   and the paper demonstrates it by giving SHAP the lowest infidelity when the
   perturbation is SHAP's own. **An infidelity number without its perturbation
   is not comparable to anybody else's.**

3. **Do not read a low sensitivity as a virtue on its own.** The paper's second
   objection is the substantive one: "natural explanations might have a certain
   amount of sensitivity by their very nature, either because the model is
   sensitive, or because the explanations themselves are constructed by
   measuring the sensitivities of the predictor function". A faithful
   explanation of a sensitive model should move. What the paper recommends is
   *restrained* lowering, and it shows kernel smoothing does that: Theorem 4.1
   bounds the smoothed explanation's max-sensitivity by the kernel-average of
   the unsmoothed one's, and empirically "Smooth-Grad improves both sensitivity
   and infidelity for all base explanations across all datasets".

## Why this is `Active` on one paper

Most of it is not the kind of claim replication tests. The constant-explanation
minimiser falls out of max-sensitivity's definition, and the perturbation
dependence is proved rather than measured. What it costs to follow is a
sentence naming `μ_I` and a second column in a table. What it costs to ignore
is a comparison no one else can reproduce, or a score won by saying nothing.

## How this sits against what the record already holds

[SOTA-430](SOTA-430.md) says to run the randomization checks and, in step 3, to compare
signed rank correlation against absolute or perceptual similarity because "a
single metric can hand you either verdict". This practice is the same warning
one level down, about the *faithfulness* metrics rather than the *similarity*
metrics, and from a different group.

[LIT-724](../literature.d/LIT-724.md) is the document that makes it load-bearing here: it reports
infidelity and max-sensitivity as a pair of trustworthiness measures across its
whole randomization study, including the 2.84 → 1.27 × 10⁷ infidelity climb
`SOTA-430` now carries. It specifies its perturbations — `N(0, 0.03)` and
`x − x₀` — which is step 2 done correctly, and it reports max-sensitivity
"almost unchanged" without the caveat in step 1.

## Conditions

- **These are properties of two specific measures**, not of explanation
  evaluation in general. A different faithfulness measure needs its own
  degenerate-optimum check; the transferable habit is to *run* that check, and
  the finding is that two measures in wide use fail it in opposite directions.
- **Vision models, 2019.** MNIST, CIFAR-10, ImageNet. The definitions are
  modality-agnostic and the experiments are not.
- **The infidelity-optimal explanations the paper introduces are optimal by
  construction**, so the table where they win is not evidence that infidelity
  is the right objective. The human study is the evidence offered for that, and
  it is 16 users on one synthetic construction.
