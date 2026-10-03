---
number: 118
status: Proposed
formerly:
- THEORY-tmp2ixql
promote_when: >-
  A run outside OpenAI's line that logs the two parts of the tangent
  separately through training, the spatial term ∇F·dx/dt and the time
  derivative ∂_t F, on a setting other than sCM's CIFAR-10 gradient-norm
  plots, and shows that the spikes normalization removes come from the
  second. It must then show that fixing the time derivative alone, by the
  identity time transform and positional embeddings without normalization,
  recovers most of normalization's FID gain. The localization of the
  instability is an empirical statement in one paper, and the evidence that
  the fixes work is FID curves from one setting. A further paper that adopts
  tangent normalization would not count.
title: "Continuous-time consistency training is unstable through the time derivative in its tangent, and tangent normalization, which MeanFlow's adaptive loss weight already is, controls it"
version: 1
tags:
- generative-modeling
- few-step-generation
- model-stability
date: '2026-10-03'
source:
- LIT-790
- LIT-783
- LIT-784
explains:
- SOTA-443
summary: >-
  Lu and Song (2024), [LIT-790](../literature.d/LIT-790.md), §4.1–4.2. The continuous-time
  consistency gradient follows the tangent df/dt along the ODE. Of its
  parts, the authors find the time derivative of the network unstable, and
  derive why: EDM's time transform contributes a factor 1/cos(t) that blows
  up at the noise end, and a large Fourier embedding scale oscillates.
  Normalizing the tangent caps the rest. Zheng et al. ([LIT-783](../literature.d/LIT-783.md)) find
  the same term fragile at 14B and in BF16, and state that MeanFlow's
  adaptive weight with p = 1 is tangent normalization, which is checkable
  algebra. The localization is measured on CIFAR-10 gradient norms, and the
  fixes on one ImageNet-512 setting.
---

<!-- inactive-ok-file: SOTA-443 — Proposed, and declared in `explains:`; the practice this account underwrites for its continuous-time and MeanFlow half. Explaining a practice not yet in force is the normal case. -->
<!-- inactive-ok-file: THEORY-124 — Proposed, filed in the same contribution; named to draw the boundary between the two accounts of consistency-training instability -->

# THEORY-118: Continuous-time consistency training is unstable through the time derivative in its tangent, and tangent normalization, which MeanFlow's adaptive loss weight already is, controls it

## Source

Lu and Song (2024), [LIT-790](../literature.d/LIT-790.md), §2.2, §4.1–4.2, Eqs. 2, 6–7 and Fig. 5.
Zheng et al. (2025), [LIT-783](../literature.d/LIT-783.md), §3.1, Eq. 4 and footnote 4, §3.3,
Eq. 5, §4.2 and App. F.2. Geng et al. (2025), [LIT-784](../literature.d/LIT-784.md), §4.3 and
Table 1e.

## The account

**The update is the tangent.** As the step shrinks, the consistency-model
gradient becomes E[w(t)·f_θᵀ·df_θ⁻/dt], where df/dt is the tangent of the
model along the probability-flow ODE ([LIT-790](../literature.d/LIT-790.md), Eq. 2, from Consistency
Models' Remark 10). Whatever makes that tangent large or erratic is what
reaches the weights.

**Its unstable part is the time derivative.** sCM ([LIT-790](../literature.d/LIT-790.md), §4.1)
writes the tangent in its TrigFlow parameterization (Eq. 6) and reports
that the network output, the ODE velocity and x_t are "relatively stable",
and that ∇F·dx/dt "is typically well-conditioned". That leaves sin(t)·∂_t F.
It factors through the time transform and the time embedding (Eq. 7), and
two of the factors are derivations anyone can check:

- EDM's time transform, written in TrigFlow, is c_noise(t) ∝ log(σ_d tan t),
  and sin(t)·∂_t c_noise = 1/cos(t), which "blows up whenever t → π/2".
- A Fourier embedding sin(s·2πω·c + φ) has derivative proportional to its
  scale s, so the default scale of 16 makes ∂_t F large and oscillating.

The fixes act on those factors: an identity time transform, positional
embeddings (about s = 0.02), and a normalization of the time-conditioning
layer. Then the remaining tangent is normalized,
df/dt ÷ (‖df/dt‖ + 0.1), or clipped (§4.2). The paper says "most gradient
variance in CM training comes from the tangent function", and Fig. 5a shows
either normalization or clipping giving "substantial improvements" in
ImageNet-512 distillation.

**At scale the same term is the weak point.** rCM ([LIT-783](../literature.d/LIT-783.md), §3.3,
Eq. 5) splits the target into a teacher term weighted by cos(t) and a
self-feedback term, the JVP of the network's own time derivative, weighted
by sin(t). At large t the teacher term vanishes and the update is dominated
by the self-feedback. That term is far more sensitive to BF16 than the
network output (App. F.2, Fig. 11). A finite difference for ∂_t F works at
2B parameters on images and not at 10B or on video, where the time
embedding layers are run in FP32 instead (§4.2).

**MeanFlow's loss weight is the same control.** MeanFlow ([LIT-784](../literature.d/LIT-784.md),
§4.3) multiplies the squared residual ‖Δ‖² by w = 1/(‖Δ‖² + c)^p under
stop-gradient. Its Table 1e has one-step FID 79.75 at p = 0, plain squared
L2, and 61.06 at p = 1. rCM's footnote 4 states that this weight at p = 1
"is the same as tangent normalization". The record checks it this way. The
gradient of sg(w)·‖Δ‖² is 2Δ/(‖Δ‖² + c) times the network's Jacobian. The
normalized-tangent loss in rCM's Eq. 4, ‖F_θ − F_θ⁻ − g/(‖g‖² + c)‖² with
g the weighted tangent, has gradient −2g/(‖g‖² + c) times the same
Jacobian at θ = θ⁻. The residual plays the tangent's role, so the two are
one per-sample rescaling. sCM's own form divides by ‖g‖ + c, not
‖g‖² + c, so it is the p = 0.5 neighbour. MeanFlow calls p = 0.5 "similar
to Pseudo-Huber", and its p = 0.5 gives 63.98.

## What it explains

**[SOTA-443](../practices.d/SOTA-443.md), for its continuous-time and MeanFlow half.** The practice
says to down-weight large residuals in consistency and MeanFlow training.
In these objectives the residual is the network's tangent. Its large values
come from the time derivative the parameterization makes unstable, and
down-weighting them is tangent normalization under another name. That is
why the practice's sCM Condition, "you already have the effect", holds. In
discrete-time consistency training the residual f(x_{t+Δ}) − f(x_t) is a
finite-difference tangent times Δ. Pseudo-Huber's gradient is the residual
divided by √(‖r‖² + c²), the same shape as sCM's normalization. The account
therefore covers iCT's choice by algebra. iCT's own evidence is lower
update variance ([LIT-786](../literature.d/LIT-786.md), Fig. 6b), and it does not locate the source.

## What this does not say

- **Not that the localization is proved.** That the spatial term is
  well-conditioned and the time derivative is not is reported as an
  empirical finding, shown through gradient norms on CIFAR-10 (Fig. 4). The
  1/cos(t) and Fourier-scale factors are derivations. That they are *the*
  source of the variance is not.
- **Not about the target's weights.** sCM uses current-weight targets under
  stop-gradient throughout. [THEORY-124](THEORY-124.md) is about why a lagging target
  fails, a separate mechanism.
- **Not the only reading of robust losses.** Inductive Moment Matching
  ([LIT-775](../literature.d/LIT-775.md), Lemmas 1–2) reads Pseudo-Huber as a kernel that matches
  all moments, where squared L2 matches only the first. That is an account
  of why the robust loss helps at its optimum. This one is about what it
  does to the update. Both could hold, and nothing measures either against
  the other.
- **Not a fix for fine detail at scale.** rCM finds pure sCM, with every
  stabilizer above, still loses small text and temporal coherence at
  14B, and adds a distribution-matching term. Stable training is not the
  same as a sufficient objective.
- **The p = 1 identity is about the gradient, not the training run.**
  Nobody has run MeanFlow's weight against sCM's normalization in one
  codebase.
