---
status: Proposed
promote_when: >-
  Two things, and they are independent. **Precision and recall, or a human
  preference study, on autoguided against CFG-guided samples at matched FID** —
  the measurement SOTA-425 asks for and this paper's own future work names without
  running, because "quality without losing variation" is currently a claim that a
  Fréchet distance improved and a Fréchet distance cannot separate the two. And
  **a run on an architecture family outside the EDM line**, by a group that did not
  write EDM2, since every number here comes from EDM2 checkpoints and the method
  leans on EDM2's post-hoc EMA. Either alone would move this; the diversity
  measurement matters more, because it is the claim the practice is chosen for.
  What would *not* count: a better FID from autoguidance on another EDM2 model,
  which is the same evidence again.
consensus: unreplicated
consensus_note: >-
  One group, one paper, and the group is the EDM/StyleGAN line whose own earlier
  work supplies both the baseline and the EMA machinery this depends on — so its
  antecedents are not independent support. The internal evidence is unusually good
  for a single paper: records on two resolutions, a mechanism, and a negative
  control that fails in the predicted way. What keeps it `Proposed` is the
  authors' own practical objection — an early snapshot of a smaller model is "easy
  to satisfy in principle, but these are not available for current large-scale
  image generators in practice" — plus the fact that every number is a Fréchet
  distance, so the central claim of *preserved diversity* has not been measured
  with a coverage metric. Per DP-005, no adoption is claimed either way; the
  record has not assessed whether serving stacks ship it. Read as of 2026-09.
title: 'Guide a diffusion model with a smaller, less-trained copy of itself rather than an unconditional model, and make sure the two models are degraded in the same way'
version: 1
tags:
- generative-modeling
- inference-optimization
- analysis-and-evaluation
date: '2026-09-25'
source:
- LIT-tmpbpv9d
introduced_by:
- LIT-tmpbpv9d
implementations:
- 'EDM2'
summary: >-
  Karras et al. (2024), [LIT-tmpbpv9d](../literature.d/LIT-tmpbpv9d.md). Replace classifier-free guidance's
  unconditional reference with a **degraded copy of the same conditional model** —
  smaller and under-trained, same task, same conditioning, same data. The quality
  gain survives and the diversity loss does not: ImageNet-512 FID **2.56 → 1.34**
  (EDM2-S), **1.25** (XXL), **1.01** at ImageNet-64, and unconditional EDM2-S
  **11.67 → 3.86**, which CFG cannot do at all. The binding condition is
  compatibility: degrade the two models differently and the method stops working
  entirely.
---

<!-- inactive-ok-file: SOTA-397, SOTA-428, THEORY-tmput07n — SOTA-428 is cited as a precondition measured in the source (equal EMA lengths cost FID 1.34 to 1.53), SOTA-397 as a neighbouring problem this practice is not solving, and THEORY-tmput07n as this practice's own account. All Proposed; none relied on as settled. -->

# SOTA-tmpj70gp: Guide a diffusion model with a smaller, less-trained copy of itself rather than an unconditional model, and make sure the two models are degraded in the same way

## Source

Karras, Aittala, Kynkäänniemi, Lehtinen, Aila and Laine (2024),
[LIT-tmpbpv9d](../literature.d/LIT-tmpbpv9d.md) — [ARXIV-2406.02507](https://arxiv.org/abs/2406.02507).
[THEORY-tmput07n](../theory.d/THEORY-tmput07n.md) is why it works.

## What to do

**Train, or keep, a deliberately worse version of the model you are going to
sample.** Same task, same conditioning, same data distribution — degraded on
capacity and training length. The paper's working configuration for EDM2-S: an
**XS-sized** guiding model at **1/16** of the main model's training iterations.
Both degradations together beat either alone.

**Guide with it in place of the unconditional model**, using the ordinary guidance
formula and a weight found by search.

**Give the two models independent EMA lengths.** Forcing them equal costs FID
1.34 → 1.53. That makes [SOTA-428](SOTA-428.md)'s post-hoc EMA a precondition for the full
benefit rather than an optional companion.

## The condition that actually binds

**The two models must be degraded in the same way.** This is not a caveat, it is
the mechanism, and the paper tested it by breaking it:

| `D₁`, `D₀` from one base model (FID 2.56) | autoguided |
| --- | --- |
| dropout 5% (4.98) and 10% (15.00) | **2.55** at `w = 2.25` |
| input noise +10% (3.96) and +20% (9.73) | **2.56** at `w = 2.00` |
| dropout on one, input noise on the other | **nothing works; best `w` is 1** |

A worse reference model is not sufficient. It has to be worse *in the same
direction*, so that the difference between the two predictions points along the
error the good model is making. Capacity and training length are recommended
precisely because any model already suffers from both to some degree.

**Do not read the synthetic corruptions as a recipe.** The authors are explicit
that they do not suggest guiding with dropout or input noise in practice; those were
constructed to test the hypothesis, and a real model does not have those particular
defects.

## What it buys

| setting | baseline | autoguided |
| --- | --- | --- |
| ImageNet-512, EDM2-S | 2.56 | **1.34** |
| ImageNet-512, EDM2-XXL | — | **1.25** |
| ImageNet-64 | — | **1.01** |
| ImageNet-512, **unconditional** EDM2-S | 11.67 | **3.86** |
| `FD_DINOv2`, ImageNet-512 | 29.16 | **24.18** |

The 1.34 also beats the concurrent CFG + Guidance Interval's 1.68, and the two were
not found to combine.

**The unconditional row is the one with no CFG analogue.** [SOTA-424](SOTA-424.md) requires a
condition to drop; this does not, so it reaches a regime that practice explicitly
excludes.

## Costs and conditions

**You need a second network at sampling time**, as with CFG — but a small one,
which is cheaper than CFG's full-size unconditional model. Against that, you need
to have *kept* an early small snapshot, and the authors name this as the practical
blocker: such snapshots are "not available for current large-scale image
generators in practice", and staged training whose data changes partway "would
violate our assumptions". If your pipeline does not already retain them, the cost
is a training run, not a checkpoint.

**The diversity claim is measured with mixed metrics.** FID and `FD_DINOv2` both
combine fidelity and coverage, so "quality without losing variation" currently
rests on a metric that cannot separate them — exactly what [SOTA-425](SOTA-425.md) exists to
say. The paper's own future work asks for precision and recall here and does not
report them. Treat preserved diversity as the hypothesis, not the finding.

**Guidance-weight and EMA search is part of the method, not tuning noise.** EDM2
networks are "known to be sensitive to the guidance weight and EMA length", and
the results come from a grid search over both. [SOTA-307](SOTA-307.md) and [SOTA-425](SOTA-425.md) apply to
reading any of these numbers.

**High-noise schedules may be unnecessary here.** Noise-level-dependent guidance
weights exist largely to suppress CFG where differently-conditioned distributions
diverge; the authors expect no such problem "as both models target the same
distribution". Untested.

## Related

- [SOTA-424](SOTA-424.md) — CFG. This replaces its reference model and thereby its trade; two of
  that practice's Conditions are CFG-specific rather than general, and it now says
  so.
- [SOTA-428](SOTA-428.md) — post-hoc EMA. A precondition for the best results here.
- [SOTA-425](SOTA-425.md) — report precision and recall beside FID. The measurement this
  practice's central claim is waiting on.
- [SOTA-397](SOTA-397.md) — conditioning an unconditionally trained model. Different problem:
  that adds a condition, this improves an unconditional model without one.
