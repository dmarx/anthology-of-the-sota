---
number: 410
status: Active
formerly:
- SOTA-tmpylyb1
consensus: converged
consensus_note: >-
  Not doing this is what needs justifying. `DPMSolverMultistepScheduler` is in
  diffusers and is the default or near-default in the serving stacks this record
  can name, and the setting it is measured in — Stable Diffusion at guidance
  7.5 — is the shipped one. The grounds here are the evidence as well as the
  adoption: one paper, but a controlled table across three solver families and
  four evaluation budgets, with the failure it corrects measured rather than
  asserted. Read as of 2026-09.
title: 'For guided sampling, use a second-order multistep solver on the data-prediction parameterization, not a higher-order solver on the noise prediction'
version: 2
history:
- version: 2
  date: '2026-09-25'
  note: >-
    The ImageNet table's model is now held, LIT-tmpcq7qo. Its authors' tuned
    25-step DDIM classifier scale at 256×256 is 2.5 (FID 5.44), so the table's
    8.0 is a stress test at about three times that, and a classifier scale is
    not the same knob as Stable Diffusion's CFG weight of 7.5, which the text set
    beside it. One clarifying paragraph; recommendation, status and consensus
    unchanged.
tags:
- inference-optimization
- generative-modeling
date: '2026-09-25'
source:
- LIT-676
introduced_by:
- LIT-676
implementations:
- 'diffusers (DPMSolverMultistepScheduler)'
- 'DPM-Solver++'
explained_by:
- THEORY-104
summary: >-
  Lu et al. (2022), [LIT-676](../literature.d/LIT-676.md). [SOTA-203](SOTA-203.md)'s higher-order solver inverts under
  guidance: at scale 8.0 and 10 evaluations, FID is **13.04** for first-order
  DDIM against **114.62** at order 2 and **164.74** at order 3. Sample instead
  with a **second-order multistep** solver parameterized on the **data
  prediction** — which is also what makes [SOTA-202](SOTA-202.md)'s per-step clamping
  available at all, since you cannot clamp `x̂₀` if the solver's state is `ε̂`.
  20 evaluations then beat DDIM at 250.
---

# SOTA-410: For guided sampling, use a second-order multistep solver on the data-prediction parameterization, not a higher-order solver on the noise prediction

## Source

Lu, Zhou, Bao, Chen, Li and Zhu (2022), [LIT-676](../literature.d/LIT-676.md) —
[ARXIV-2211.01095](https://arxiv.org/abs/2211.01095).

## What to do

When you are sampling with classifier or classifier-free guidance at a scale
anybody would actually ship — 7.5 for Stable Diffusion, 8.0 in the ImageNet
experiments here — three choices, and they are not independent.

1. **Order 2. Not higher.** The authors decline to go past it: "high-order
   solvers may be unsuitable for large guidance scales, thus we mainly consider
   `k = 2`".
2. **Multistep, not singlestep.** Reuse the previous step's evaluation instead of
   taking an extra one inside the current step. This reduces the effective step
   size, which is what the guided regime needs.
3. **Parameterize on the data prediction `x̂₀`, not the noise prediction `ε̂`.**
   Both admit second-order solvers; only the first admits clamping.

`DPMSolverMultistepScheduler` in diffusers is this.

## What it buys, and what it avoids

ImageNet 256×256, classifier guidance 8.0, no thresholding, FID:

| sampler | 10 NFE | 15 | 20 | 25 | 250 |
| --- | --- | --- | --- | --- | --- |
| DDIM — order 1 | 13.04 | 11.27 | 10.21 | 9.87 | 9.37 |
| DPM-Solver-2 | 114.62 | 44.05 | 20.33 | 9.84 | — |
| DPM-Solver-3 | 164.74 | 91.59 | 64.11 | 29.40 | — |
| **this practice — (2M)** | 14.44 | **9.46** | **9.10** | **9.11** | — |

**What 8.0 is on this model.** The table is Dhariwal & Nichol's 256×256
classifier-guided model (LIT-tmpcq7qo), whose authors tuned its scale for 25 DDIM
steps at **2.5** (FID 5.44). 8.0 is a deliberate stress test at about three times
that, and a classifier-gradient scale is not the same knob as Stable Diffusion's
CFG weight of 7.5, however close the numbers look. The shipped-regime evidence is
LIT-676's Stable Diffusion comparison; the ImageNet table is where the failure is
cleanest, not where it is typical, and its FIDs are not the model's quality.

Two readings. Against the *right* thing to do, this saves an order of magnitude
of evaluations: **9.10 at 20 NFE beats DDIM's 9.37 at 250**. Against the *wrong*
thing to do — raising the order on the noise prediction, which is what
[SOTA-203](SOTA-203.md) reads as licensing — it avoids a catastrophe: 114.62 and 164.74 are not
degradations, they are broken images.

The singlestep variant (2S) is better at 10 NFE (12.20) and worse from 15
onwards. If your budget is truly minimal, measure both.

## Why the parameterization is not a detail

[SOTA-202](SOTA-202.md) already tells you to clamp the `x̂₀` prediction to the training range at
every step, because high guidance pushes it out of `[−1, 1]` and the excursion
compounds when the model is applied to its own output. That practice is `Active`
and `converged` and it has a precondition nobody had stated: **the clamp needs
`x̂₀` to be the thing the sampler is carrying.**

A high-order solver written on `ε̂` has no `x̂₀` to clamp at its intermediate
stages, so the one fix the record already recommends is unavailable exactly where
it is most needed. Choosing the data-prediction parameterization is what makes
the two practices composable.

## Conditions

**Guided sampling only, and that is the point.** Without guidance the ladder runs
the right way up and [SOTA-203](SOTA-203.md) applies unchanged — higher order is better there,
and DDIM is the weakest member of the family. This practice exists because that
sentence reverses under guidance, not because it was wrong.

**Order 2 is a ceiling of ignorance, not a proof.** The authors "leave the
solvers for higher orders for future study". Nobody has shown a third-order
method cannot be made to work under guidance; nobody has shown one that does.

**Image diffusion, pixel and latent space.** Evaluated on ImageNet with a
classifier-guided model and on COCO with Stable Diffusion. Nothing here is
measured on audio, video or a non-diffusion sampler.

**Thresholding composes but is reported separately.** The table above is
*without* thresholding, so these numbers are the solver's own. Combining the two
is the paper's §4.3 and [SOTA-202](SOTA-202.md)'s subject.

## Known implementations

- **diffusers**, as `DPMSolverMultistepScheduler`.
- **DPM-Solver++**, the authors' release, which is the same codebase as
  DPM-Solver.
