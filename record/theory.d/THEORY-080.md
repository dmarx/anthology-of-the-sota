---
number: 80
status: Proposed
formerly:
- THEORY-tmpyyfqg
promote_when: >-
  A direct measurement that high blur-to-noise processes send intermediate
  samples off the data manifold (for example a density, classifier or
  nearest-neighbour score of reverse-process states against forward-process
  states at the same step), together with the same BNR sweep degrading at
  higher resolution or in a latent space. Another sweep showing FID
  worsening at high BNR does not settle it. That is the observation the
  account was built to explain, not a test of its mechanism.
title: 'A diffusion process needs noise to keep its intermediate states on the data manifold, and blur helps only while noise still dominates the bands it removes'
version: 1
tags:
- generative-modeling
- analysis-and-evaluation
date: '2026-09-23'
source:
- LIT-555
- LIT-553
corrects:
- THEORY-079
summary: >-
  Hsueh et al. (2025), [LIT-555](../literature.d/LIT-555.md) — blur removes high frequencies
  deterministically, so many images share a blurry one and the deblurring
  target is their mean. Stepping toward it leaves the manifold unless noise
  has already made those images indistinguishable. Natural spectra fall as
  1/f² against flat noise, so blur is safe in a band only once noise
  dominates it. That puts the useful ratio near 0.5 on CIFAR-10. The FID
  sweep fits the account, and the manifold departure itself is not
  measured.
---

# THEORY-080: A diffusion process needs noise to keep its intermediate states on the data manifold, and blur helps only while noise still dominates the bands it removes

## Source

Hsueh et al. (2025), [LIT-555](../literature.d/LIT-555.md) — read as [NOTE-297](../notes.d/NOTE-297.md). The cold end of
the evidence is Bansal et al. (2022), [LIT-553](../literature.d/LIT-553.md). Filed for `#163`'s
"[theory] warm diffusion".

## The account

**Two degradations, two effects.** Noise hides information randomly and
isotropically, and its forward marginals cover the space between data
points. Blur deletes high frequencies deterministically, and its forward
marginals collapse many data points onto one.

**Why the cold side fails.** When many clean images map to one blurry
image, the deblurring prediction is their mean, which is not itself a
natural image. A reverse step toward it lands somewhere the forward process
never went, so the network sees an input unlike its training data and its
prediction is unreliable. Noise prevents this by making the collapsed
images indistinguishable *before* blur merges them, so the reverse process
never has to choose deterministically between them.

**Why some blur helps.** Fine detail in natural images is predictable from
coarse structure. A deblurring head can use that dependency, while a pure
denoiser has to rebuild detail as if it were independent of the coarse
structure. Natural spectra fall roughly as `1/f²` and noise is flat, so in
high bands noise dominates early. Blur applied to a band only after noise
has swamped it keeps the manifold intact and still hands work to the
deblurrer. On CIFAR-10 that is about BNR = 0.5.

## What was actually shown

- **The degradation curve.** At fixed model, sampler and 35 steps, FID
  1.97 → 1.85 → 2.01 → 2.57 → 11.97 as BNR goes 0 → 0.5 → 1 → 2 → 10
  ([LIT-555](../literature.d/LIT-555.md), Table 3). Higher BNR also needs more steps to recover
  (Figure 5)
- **The cold end, independently.** Cold Diffusion's noiseless generation is
  FID 97.00 on CelebA, and σ = 0.002 of noise halves it ([LIT-553](../literature.d/LIT-553.md),
  Table 5)

## What this does not say

**The manifold departure is inferred, not observed.** Nothing measures
where reverse-process states sit relative to forward-process states. The
FID curve is the thing to be explained, and it is consistent with other
explanations: for example that a two-headed model at high BNR simply
learns a harder deblurring problem.

**The "blur helps" half is thin.** 1.97 → 1.85 FID, best of three sampling
rounds, one dataset, no variance.

**Nothing about latent diffusion.** Latent spectra are not `1/f²` image
spectra, and the BNR rule is derived from pixel statistics.

## Why `Proposed`

It replaces an account the record has rejected and fits both papers'
numbers, but its mechanism has not been measured, and the half about blur
helping rests on a margin smaller than the unreported variance plausibly
is.
