---
number: 113
status: Proposed
formerly:
- THEORY-tmp4cch6
promote_when: >-
  A third group removes the input multiplier from a gradient attribution and
  re-runs a parameter-randomization test, in a setting neither Inception nor a
  BERT text classifier, and reports whether the verdict moves. The prediction
  to test is directional and cheap: the local variant must lose similarity
  under randomization where the global variant keeps it, and the gap must
  shrink wherever the multiplier's structure is destroyed before scoring. What
  would NOT settle it: another sweep of image classifiers reporting that
  methods with multipliers fail, which is the observation this account explains
  rather than a test of it; or a paper adopting the local variant because it
  passes, which is adoption (DP-005).
title: 'A gradient attribution survives weight randomization because of its input multiplier, not because the attribution is insensitive to the weights'
version: 3
history:
- version: 2
  date: '2026-09-26'
  note: >-
    States the boundary now that a second account is held. LIT-729 shows a
    different mechanism — rank-1 convergence of a non-negative relevance chain —
    for the z+ family, and supports this account from outside by noting that
    methods relying on the gradient directly do not converge, so Integrated
    Gradients' failure is not that one. It also names the third mechanism, for
    guided backprop and deconv, as Nie et al. (2018), 1805.07039, unheld. The
    account itself is unchanged; what is new is that the cluster's failures now
    partition and this document says which part it owns.
- version: 3
  date: '2026-09-26'
  note: >-
    The third row of the partition is held. LIT-730 proves guided
    backpropagation recovers the input in a random CNN, so its family's failure is
    partial image recovery (THEORY-115) rather than anything this account
    covers. One table cell, and the reason it needed changing a day after being
    written is worth noting: v2 put a "not held" row into four documents at once,
    and all four went stale in the next unit.
tags:
- analysis-and-evaluation
- representation-and-encoding
date: '2026-09-26'
source:
- LIT-724
- LIT-713
explains:
- SOTA-430
summary: >-
  Kokhlikyan et al. (2021), [LIT-724](../literature.d/LIT-724.md). Integrated Gradients and its
  relatives multiply a path integral by `(x − x₀)`, which does not depend on
  the model. That factor carries the input's structure into the map, so the map
  keeps looking the same when the weights are destroyed. [LIT-713](../literature.d/LIT-713.md) suspected this
  and said it did not measure it; this does, with the arm that discriminates —
  drop the multiplier and the map becomes parameter-sensitive. A second, harder
  arm comes free: on text, where summing over embedding dimensions destroys the
  multiplier's structure, the *global* variant becomes parameter-sensitive too.
---

<!-- inactive-ok-file: SOTA-430 — Proposed, and declared in `explains:`; the practice this account underwrites, cited to say which of its cautions survive. An account explaining a not-yet-in-force practice is the normal case, not a defect. -->

# THEORY-113: A gradient attribution survives weight randomization because of its input multiplier, not because the attribution is insensitive to the weights

## Source

Kokhlikyan, Miglani, Alsallakh, Martin and Reblitz-Richardson (2021),
[LIT-724](../literature.d/LIT-724.md), §2–3 and Appendix A; with Adebayo et al. (2018),
[LIT-713](../literature.d/LIT-713.md), which states the conjecture and declines to measure it.

## The account

Global Integrated Gradients along input dimension `i` is

    Φ(F, xⁱ) = (xⁱ − x₀ⁱ) · ∫₀¹ ∂F(x₀ⁱ + α(xⁱ − x₀ⁱ))/∂xⁱ dα

The integral depends on the model. **The leading factor `(xⁱ − x₀ⁱ)` does
not.** With the usual zero or black baseline it is essentially the input. So
the map is a model-dependent quantity multiplied, pixel by pixel, by a
model-independent picture of the input — and a similarity metric that reads
spatial structure will report that the map is unchanged when the model is
destroyed, because the part of it carrying the structure never depended on the
model in the first place.

The same factor appears in InputXGradient, DeepLift and Gradient SHAP, which is
why they land in the same column of `LIT-713`'s verdicts. Guided Backprop and
Guided GradCAM are outside this account: they modify gradients during
back-propagation and fail for a separate reason.

**The boundary, now that a second account is held.** The cluster's failures
partition three ways, and this document owns the first row:

| family | mechanism | held as |
| --- | --- | --- |
| Integrated Gradients, InputXGradient, DeepLIFT, Gradient SHAP | **this account** — the model-independent input multiplier | here |
| DTD, LRP-α1β0, Excitation BP, PatternAttribution | rank-1 convergence of a non-negative chain | [THEORY-114](THEORY-114.md) |
| Guided Backprop, Deconv, RectGrad | partial image recovery | [THEORY-115](THEORY-115.md) |

[LIT-729](../literature.d/LIT-729.md) supports this account from outside its own subject: methods
that "rely on the gradient directly (Smilkov et al. 2017; Sundararajan et al.
2017) ... [do] not converge", so Integrated Gradients' randomization behaviour is
not the rank-1 mechanism, which is what leaves the multiplier as the explanation.
DeepLIFT sits in the first row and outside the second, which is not a
contradiction: it carries an input multiplier *and* keeps negative contributions,
so it has one of the two failure modes and escapes the other.

## Why this is an account rather than a restatement

`LIT-713` already suspected the multiplier. What it says is that parameter and
data invariance "is likely to be related to the input multiplier in some
gradient-based methods; **however, they do not measure input multiplier's
quantitative impact**". A suspicion that names the right factor and runs no arm
to isolate it is a hypothesis, and the record's standard is that a mechanism
claim earns its status when the experiment includes an arm the mechanism says
must behave differently.

There are two such arms here, and they point in opposite directions:

1. **Remove the multiplier, holding everything else fixed.** Local IG on
   Inception under cascading parameter randomization: the maps change, and
   SSIM for the local variant is about half the global variant's. If the
   insensitivity were a property of gradient attribution, dropping a
   model-independent scale factor would not fix it.
2. **Destroy the multiplier's structure without removing it.** On text, token
   scores are formed by summing over embedding dimensions. The account
   predicts that a multiplier whose spatial structure is summed away stops
   protecting the map — and on BERT/SST-2 the *global* variant becomes
   parameter-sensitive, with cosine-similarity medians near zero. Global IG
   fails the test on images and passes it on text, which a
   "gradient attributions are insensitive to weights" reading cannot
   accommodate at all.

The second arm is the one that makes this worth filing. An account that only
explained the image result would be indistinguishable from the label
"multiplier"; this one predicts a *sign change* across modality and gets it.

## What it does not say

- **It is not a defence of Integrated Gradients.** The account says the
  randomization test's verdict is about the multiplier. It says nothing about
  whether the local variant is *faithful* — `LIT-713`'s tests are necessary
  conditions, and passing one is not a certificate. Every caution
  [SOTA-430](../practices.d/SOTA-430.md) carries about that still holds.
- **It does not explain the metric split.** On the same Inception experiment,
  Spearman rank correlation drops to near zero for *both* variants while SSIM
  separates them. So SSIM is reading the structure this account is about and
  Spearman is not, which is consistent with it but is a fact about the metrics
  that no arm here isolates.
- **It does not cover the smoothness confound.** Randomization also degrades
  the integral approximation — infidelity rising from 2.84 to 1.27 × 10⁷ down
  the Inception stack — and that is a separate mechanism, diagnosed in the same
  paper and not separated from this one.
- **Two architectures, one group**, and that group maintains captum, whose API
  is where you switch the multiplier off. The measurement is a real control;
  the choice of which control to run is not disinterested.
