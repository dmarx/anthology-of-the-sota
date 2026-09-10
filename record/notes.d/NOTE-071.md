---
number: 71
status: Read
formerly:
- NOTE-tmpxtt2c
paper: LIT-089
title: 'Adding Conditional Control to Text-to-Image Diffusion Models'
version: 1
tags:
- adaptation-and-tuning
date: '2026-09-09'
summary: >-
  Adds spatial control to a frozen diffusion model by cloning its encoder into a trainable branch joined to the original by zero-initialized convolutions, so the adapter starts as an exact no-op and grows away from it. Trains robustly on datasets from under 50k to over a million.
---

# NOTE-071: Adding Conditional Control to Text-to-Image Diffusion Models

## Contribution

**ControlNet**: spatial conditioning — edges, depth, segmentation, human pose —
added to a large pretrained text-to-image model that is **locked** and reused as
a backbone. The trainable branch is a copy of the model's encoding layers,
connected to the frozen original through **zero convolutions**: convolution
layers initialised to zero.

## Key insight

The zero initialisation is the whole design, and it solves a specific problem.
An adapter attached to a production model injects noise into it from step one,
before it has learned anything useful — and that noise is being added to
representations built from "billions of images". Initialising the connections at
zero makes the adapter an **exact identity at initialisation**: the frozen model
behaves exactly as before, and the parameters "progressively grow from zero",
so "no harmful noise could affect the finetuning."

This is the same instrument as a residual branch initialised to zero, and the
same reasoning as `SOTA-052`'s initialisation scaling: **start the new thing at
nothing and let training decide how much of it to use.** The advantage over a
small random initialisation is that zero is not small — it is exactly neutral,
so the guarantee is structural rather than probabilistic.

The second decision is reuse: the trainable branch is a **copy of the frozen
encoder's weights**, not a fresh network. The adapter starts already knowing how
to encode images.

## Assumptions

- **The frozen backbone's representations are worth preserving intact** — the
  premise of locking it.
- Spatial conditions can be encoded by the same architecture that encodes
  images, which is why cloning the encoder works.
- Stable Diffusion as the base; results are for that family.

## Key results

- Works across **edges, depth, segmentation, human pose**, singly and in
  combination, **with or without text prompts**.
- **Robust at both ends of the data range**: under 50k and over 1m training
  examples. Adapter methods usually have a data floor; this reports not having
  one.
- The frozen model is unchanged, so the original capability is retained
  exactly.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Zero-initialized connections prevent early training noise from damaging the frozen backbone | strong | structural — the branch is exactly neutral at init |
| C2 | Cloning the pretrained encoder is a better adapter initialisation than a fresh network | moderate | the design; the ablation is present but the claim is architectural |
| C3 | One architecture handles many condition types | strong | demonstrated across six-plus |
| C4 | Training is robust from <50k to >1m examples | strong | measured at both ends |
| C5 | Multiple conditions compose | moderate | shown |

## Method

Lock the pretrained model. Clone its encoding layers into a trainable branch.
Connect input and output of that branch to the frozen model with zero-
initialized convolutions. Train the branch on (condition, image) pairs.

## Concepts

- **Zero-initialized connection** — the transferable idea, and the sharpest
  version of "start at the identity".
- **Cloning rather than initialising** — reuse pretrained weights as an
  adapter's starting point.
- **Locking the production model** — the deployment constraint that shapes the
  design.

## Connections

The counterpart to `LIT-091` (T2I-Adapter), which pursues the same goal with a
much smaller external network rather than a cloned encoder. The two are the
heavy and light ends of the same idea, published weeks apart.

C1 belongs beside the record's initialisation practices. `SOTA-052` (DeepNet)
scales initialisation down as depth grows so a deep residual stack does not
destabilise; zero-init connections are the limiting case of the same argument
for an *added* branch. The record has the scaling and not the limit.

## Recommendations

- **R1** — Initialise an added branch's output projection to zero so it is an
  exact no-op at the start of training. *Topic:* adaptation and tuning.
  *Strength:* strong; standard now, in adapters and in residual blocks.
- **R2** — Initialise an adapter from the frozen model's own weights rather
  than randomly. *Strength:* moderate.
- **R3** — Report an adaptation method's behaviour at both ends of the dataset
  size range; the small-data end is where adapters usually fail. *Topic:*
  analysis and evaluation. *Strength:* moderate.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice.**
Retagged to `adaptation-and-tuning`: the generative model is frozen and
untouched, and everything the paper does is adaptation.

R1 is the finding with the widest reach and the record does not state it.
Zero-initialising the output of a new branch appears in residual architectures,
in LoRA (whose `B` matrix is zero-initialised for exactly this reason, noted in
`LIT-067`'s neighbourhood as "LoRA best practices"), and here. Three
independent places, one idea, no statement of it in the record.

The document's takeaway **"zero-shot conditioning" is wrong.** ControlNet
trains an adapter per condition type; nothing about it is zero-shot. The word
that belongs there is *zero-initialized*, which is a different thing and is the
actual mechanism.

## Limitations

- Stable Diffusion family, 2023.
- C2 is an architectural claim more than a measured one.
- Cloning the encoder makes the adapter large — the cost that `LIT-091` exists
  to avoid, and it is not compared here.
- Condition types are all spatial; nothing is said about non-spatial control.

## Open questions

- How much of the benefit is the zero-init and how much the cloned weights?
  The two changes arrive together and the record would like them separated.
