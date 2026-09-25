---
status: Proposed
promote_when: >-
  A group outside NVIDIA applies magnitude-preserving layers with forced
  weight normalization to a denoiser that is not an ADM-style U-Net — a
  diffusion transformer is the obvious case — and reports it against the same
  backbone with its usual normalization, at matched compute and each at its
  own best EMA length. A paper that adopts the EDM2 network wholesale and
  reports a good number is not it; that is adoption of the U-Net, not a test
  of the principle on anything else.
title: 'Make every layer of a diffusion denoiser preserve activation magnitude, and force each weight vector back to fixed norm after every step'
version: 1
tags:
- model-architecture
- training-optimization
- model-stability
- generative-modeling
date: '2026-09-25'
source:
- LIT-tmpzn7w1
introduced_by:
- LIT-tmpzn7w1
extends:
- SOTA-188
implementations:
- 'NVlabs/edm2'
summary: >-
  Karras et al. (2023), [LIT-tmpzn7w1](../literature.d/LIT-tmpzn7w1.md) — EDM2. Normalize each output channel's
  weight vector on use, re-normalize the stored weights after every step,
  scale every fixed operation to preserve unit magnitude, and drop the group
  norms. On the ADM U-Net at ImageNet-512 this takes FID from 6.96 to 2.56 at
  equal compute, with on-use weight normalization alone worth 6.96 → 3.75.
  One architecture family; untested on transformers.
---

<!-- inactive-ok-file: SOTA-282 — Proposed; named as the transformer-side sibling this practice has never been compared against, not as support -->

# SOTA-tmpui8n0: Make every layer of a diffusion denoiser preserve activation magnitude, and force each weight vector back to fixed norm after every step

## Source

Karras et al. (2023), [LIT-tmpzn7w1](../literature.d/LIT-tmpzn7w1.md) — [ARXIV-2312.02696](https://arxiv.org/abs/2312.02696), §2 and Appendix B;
read as [NOTE-tmpod74g](../notes.d/NOTE-tmpod74g.md).

## The problem it removes

In the ADM U-Net, activation magnitudes on the residual main path grow
throughout training and never level off; the group norms inside each block do
not reach the main path, and putting normalization there instead made results
significantly worse. Weight magnitudes grow too, and because a normalized
layer's gradient is orthogonal to its weight, every step lengthens the weight
and shrinks the *effective* learning rate — unequally across layers and
without anybody having scheduled it.

## What to do

1. **Normalize every learned layer's weights on use.** For each output
   channel, divide the weight vector by its norm before applying it, with
   gradients flowing through the norm and no learned gain. Initialise weights
   from `N(0, 1)`. Activation magnitude no longer depends on weight magnitude.
2. **Force the stored weights back to fixed norm after every step** — and keep
   step 1 as well. Step 1 projects the gradient onto the sphere's tangent plane
   *before* the optimizer sees it; without it, Adam's second-moment estimate
   includes a normal component that the re-projection then throws away, and
   steps come out much smaller than intended. The whole implementation is two
   calls to one `normalize()` function.
3. **Schedule the learning rate explicitly.** With the norm fixed, the
   effective learning rate is the nominal one, so the implicit decay is gone;
   EDM2 adds inverse-square-root decay and raises the base rate to 0.01.
4. **Make the fixed operations magnitude-preserving too**: divide SiLU by
   0.596, scale Fourier features by √2, replace residual additions with a
   normalized blend (`t = 0.3` for the residual branch), rebalance
   concatenations so each input contributes equally whatever its channel
   count. Learned gains only where the loss needs a non-unit scale — at the
   output and on the conditioning, zero-initialised.
5. **Then remove the data-dependent normalization.** EDM2 drops every group
   norm and keeps a few cheap pixel norms at encoder-block inputs, because the
   independence assumption behind step 1 is not exact.

## What was measured

ImageNet-512 latents, ~300M parameters, 2³¹ training images, FID without
guidance, each config at its own best EMA length, cumulative:

| step | FID |
|---|--:|
| streamlined baseline | 6.96 |
| + on-use weight normalization (1) | **3.75** |
| + forced weight normalization and explicit decay (2, 3) | 3.02 |
| + group norms removed (5) | 2.71 |
| + magnitude-preserving fixed operations (4) | 2.56 |

Gflops are unchanged throughout. Scaled up, the same design sets records at
ImageNet-512 (1.81 guided) and ImageNet-64 (1.33) with a deterministic
63-evaluation sampler.

## Why it extends [SOTA-188](SOTA-188.md)

[SOTA-188](SOTA-188.md) asks for unit variance at the network's input and output, derived by
preconditioning. This carries the same requirement inside the network, layer
by layer, and for the same reason: a network whose internal scales drift is
solving a differently-sized problem at every point in training. EDM2 is
EDM's successor from the same group and presents it that way.

## Conditions

- **One architecture family.** Every number above is an ADM-style U-Net. The
  authors ask in their own discussion whether it would help RIN or DiT, and
  do not try. That is the whole of `promote_when`.
- **One run per step, and the ladder is cumulative.** Each gain is measured
  given every change before it, and several rows bundle changes — the forced
  normalization arrives together with a new learning-rate schedule. The
  per-step gaps (6–46%) are all outside the ±2% the paper gives for FID
  noise, so the ordering is not in doubt; the attribution within a row is.
- **It changes the hyperparameters around it.** Learning rate, schedule,
  dropout (off at small sizes, back on for the large models that overfit)
  and EMA length all moved. Transplanting the layers without re-sweeping them
  is not what was tested.
- **Magnitudes are preserved on expectation, under an independence
  assumption** the authors say is not strictly true; the results hold anyway,
  and the pixel norms are there to catch what the assumption misses.

## Its neighbour on the language side

[SOTA-282](SOTA-282.md) (nGPT) re-projects every weight matrix onto the unit sphere after
each step and deletes the normalization layers — the same move, in decoder-only
language models, ten months later. The two have
never been run against each other, and they differ in what they keep: nGPT
normalizes the hidden states as well, EDM2 preserves their magnitude by
construction and keeps a few pixel norms. No relation is declared between
them because nobody has compared them.

## Known implementations

- `NVlabs/edm2`.
