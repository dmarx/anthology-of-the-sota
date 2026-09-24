---
status: Active
title: 'FiT: Flexible Vision Transformer for Diffusion Model'
version: 1
tags:
- generative-modeling
- vision-and-graphics
- model-architecture
date: '2026-09-24'
published: '2024-02-01'
arxiv: '2402.12376'
first_author: 'Lu'
extends:
- LIT-448
keywords:
- 'native-aspect-ratio'
- 'flexible-resolution'
- 'resolution-extrapolation'
- '2d-rope'
- 'diffusion-transformer'
implementations:
- 'FiT'
summary: >-
  Lu et al. (2024), [ARXIV-2402.12376](https://arxiv.org/abs/2402.12376). A DiT variant trained on images
  without cropping or upsampling. Large images are only resized down to at
  most 256² pixels at native aspect ratio, and sequences are padded to 256
  tokens. Table 3 isolates this pipeline change on DiT-B/2 at 400K steps.
  At a square 256² output, FID moves 44.83 → 43.34 and sFID worsens
  8.49 → 11.11. At 160×320 and 224×448, FID falls from 91.32 and 109.1 to
  50.51 and 52.55, but the fixed model never trained on those shapes.
---
<!-- inactive-ok-file: SOTA-398 — Proposed practice this paper bears on; named to weigh the evidence, not as settled advice -->


# LIT-tmpkcykt: FiT: Flexible Vision Transformer for Diffusion Model

Lu, Wang, Huang, Wu, Liu, Ouyang and Bai (2024) — [ARXIV-2402.12376](https://arxiv.org/abs/2402.12376). Read:
§1–4, Tables 3–4 and the hyperparameter appendix.

## Key takeaways

- **The pipeline (§3.2).** DiT "resizes and crops the images to a fixed
  resolution 256×256". FiT does not crop and does not upsample small
  images. It resizes only images above HW ≤ 256² down to that bound,
  keeping aspect ratio, and pads each sequence to L_max = 256 tokens, the
  same as DiT's fixed length. Padding tokens are masked in attention and
  loss.
- **The pipeline alone (Table 3, DiT-B → Config A).** Same architecture,
  400K steps, batch 256, no guidance:

  | eval size | DiT-B fixed FID / sFID | Config A flexible FID / sFID |
  |---|---|---|
  | 256×256 | 44.83 / 8.49 | 43.34 / 11.11 |
  | 160×320 | 91.32 / 66.66 | 50.51 / 10.36 |
  | 224×448 | 109.1 / 110.71 | 52.55 / 16.05 |

- **The rest of FiT.** Switching to 2D RoPE and SwiGLU brings 256² FID to
  36.36 (Table 3). Training-free RoPE extrapolation methods (VisionNTK,
  VisionYaRN) extend it to unseen shapes (Table 4).

## Where the hedges are

Per [DP-010](../../docs/design-principles.md#dp-10):

- **At the square output everyone evaluates, the gain is small and
  mixed.** −1.49 FID (3%) with a worse sFID, from one run each. [SOTA-307](../practices.d/SOTA-307.md)'s
  floor is about 2%.
- **The non-square gains measure coverage as much as quality.** The fixed
  model trained only on 256² squares. The flexible one trained on the
  native shapes, which the table labels in-distribution at 160×320.
- **Two changes are bundled.** "No crop" and "no upsampling" change
  together. Small images are no longer enlarged, so the flexible model
  also sees fewer tokens on average per image.

## Standing in the anthology

This is the closest generative analogue to NaViT ([LIT-657](LIT-657.md)) that the
record holds, and it bears on [SOTA-398](../practices.d/SOTA-398.md). That practice measures no
generative model. FiT shows that for a diffusion transformer,
aspect-preserving training costs nothing at the square output and is
required for non-square output. It does not show that preserving aspect
ratio improves square generation, which is what isolating aspect ratio
would need.
