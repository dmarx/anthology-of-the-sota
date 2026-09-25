---
status: Proposed
promote_when: >-
  **Precision and recall measured on autoguided against CFG-guided samples at
  matched FID** — the instrument SOTA-425 recommends, and the one this paper's own
  future work asks for and does not run. The account's distinctive prediction is
  that the two guidance schemes split on *coverage*, not on fidelity: CFG should
  lose recall where autoguidance holds it. Every number in the source is FID or
  `FD_DINOv2`, both Fréchet distances that mix the two, so the claim that
  diversity is preserved is currently a claim that a mixed metric improved. A
  second group reproducing the mismatched-degradation negative control on another
  architecture family would raise it further; the control is what makes this an
  account rather than a story.
title: "Classifier-free guidance improves image quality because its unconditional reference model is worse, not because it emphasizes the class, so guidance is adaptive truncation toward the better-fit density"
version: 1
tags:
- generative-modeling
- analysis-and-evaluation
date: '2026-09-25'
source:
- LIT-tmpbpv9d
summary: >-
  Karras et al. (2024), [LIT-tmpbpv9d](../literature.d/LIT-tmpbpv9d.md). Guidance adds a force toward higher
  `log[p₁/p₀]`. The reference `p₀` is *more spread out* than `p₁` — a harder task
  on a smaller training slice — so it falls off slower away from the data and the
  ratio's gradient points inward, concentrating samples on the manifold. That, not
  class emphasis, is where CFG's image-quality gain comes from; the class emphasis
  is the separate part that costs diversity. Tested with a negative control:
  degrade the two models *incompatibly* and guidance stops helping at any weight.
---

<!-- inactive-ok-file: SOTA-tmpj70gp, THEORY-104, THEORY-109 — SOTA-tmpj70gp is the practice this account explains, THEORY-104 is cited to be distinguished from it (a consequence of a large scale, not a reason guidance helps), and THEORY-109 as the record's holding on the question this account does not address. Their Proposed status is the point in two of the three cases. -->

# THEORY-tmput07n: Classifier-free guidance improves image quality because its unconditional reference model is worse, not because it emphasizes the class, so guidance is adaptive truncation toward the better-fit density

## Source

Karras, Aittala, Kynkäänniemi, Lehtinen, Aila and Laine (2024),
[LIT-tmpbpv9d](../literature.d/LIT-tmpbpv9d.md) — [ARXIV-2406.02507](https://arxiv.org/abs/2406.02507).

## The account

**The puzzle.** CFG is derived as a way to sharpen a conditional distribution, and
its effect on prompt alignment follows from that derivation. Its effect on *image
quality* does not. Guided samples are pulled toward the core of the data manifold
and away from low-probability intermediate regions, which boosting the likelihood
of a class label does not explain.

**Why the bad samples exist.** Score matching is closely related to maximum
likelihood, and ML is conservative: the KL divergence "incurs extreme penalties if
the model severely underestimates the likelihood of any training sample", so a
finite-capacity model covers the data's extremities rather than dropping them —
including regions it has not learned accurately. Those extremities are the broken
images. A second effect compounds it: the denoiser has only ever seen *real* noisy
images, so when a sampling trajectory hands it an implausible intermediate state
it is off-distribution in a way training never covered.

**The mechanism.** Guidance adds a force along `∇ₓ log[p₁(x|c;σ) / p₀(x|c;σ)]`.
The two implied densities differ in *quality*, not only in conditioning: `D₀` has
the harder job — every class at once — on "typically only a small slice of the
training budget", so its density is looser and flatter. A flatter denominator falls
off more slowly than the numerator as you leave the data, so the ratio *decreases*
with distance from the manifold and its gradient points **inward**. The contours of
the ratio follow the manifold's local orientation and branching, so pushing along
them concentrates samples on the manifold rather than toward a point.

So guidance is **adaptive truncation**: where the two models agree the force
vanishes, and where they disagree — which is where the stronger model is itself
likely under-fit, since both fail in similar places to different degrees — it
points toward better samples. The paper notes the correction "overshoots", giving a
narrower distribution than ground truth, without apparent harm to the images.

**The size of the asymmetry being exploited.** EDM2-S on ImageNet-512: FID
**2.56** conditional against **11.67** unconditional. The reference model in
every CFG deployment is that much worse than the model it is correcting.

## What makes this an account rather than a story

A synthetic-degradation experiment with a **negative control**, on one base model
so the undamaged version grounds the comparison:

| `D₁`, `D₀` constructed by | autoguided result |
| --- | --- |
| dropout 5% (FID 4.98) and 10% (15.00) | **2.55**, matching the undamaged 2.56 |
| input noise +10% (3.96) and +20% (9.73) | **2.56**, matching it again |
| dropout on one, input noise on the other | **no improvement at any weight** |

The mismatched arm is the point. If guidance worked by generic sharpening, any
worse reference would do. It does not: the optimum falls back to `w = 1`, guidance
off. The force is informative only when the two models' errors are *the same kind*,
which is what the density-ratio story predicts and what a class-emphasis story
does not.

## What follows if it is right

**CFG's fidelity-for-diversity trade is two effects stapled together**, and the
staple is the choice of reference model. The quality gain comes from the quality
gap; the diversity loss comes from the class emphasis. Replace the unconditional
model with a degraded copy of the conditional one and you keep the first without
the second — [SOTA-tmpj70gp](../practices.d/SOTA-tmpj70gp.md) — which is why [SOTA-424](../practices.d/SOTA-424.md)'s "diversity is what is being
spent" is a fact about CFG rather than about guidance.

**Guidance needs no condition.** If the mechanism is a quality gap, an
unconditional model can be guided by a worse unconditional model, and it is:
EDM2-S unguided 11.67 → 3.86.

**A scalar cannot substitute.** Uniformly lengthening the score by `w > 1`
concentrates samples "in an isotropic fashion that leaves the outer branches
empty". The density-ratio field is anisotropic and tracks the manifold's
branching; that shape is the mechanism, not an implementation detail.

## What this does not say

**Not that the class emphasis does nothing.** It is what CFG was derived for and
it is why prompt alignment improves. The claim is about which component carries
the *quality* gain.

**Not an account of classifier guidance.** [THEORY-109](THEORY-109.md) is the record's holding
there, and this paper explicitly excludes discriminator guidance from its analysis,
"in CFG the task is implicit and the distinction is between `p₁` and `p₀`". Whether
the same density-ratio reading applies to an explicitly trained classifier is open.

**Not established outside FID.** See the `promote_when`. The account's sharpest
prediction is about coverage and nothing here measures coverage directly.

**Not the same claim as [THEORY-104](THEORY-104.md).** That is about what a large guidance scale
does to a solver's convergence radius — a consequence of the amplified
derivatives. This is about why the force helps at all.
