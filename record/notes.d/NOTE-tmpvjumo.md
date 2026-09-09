---
status: Skimmed
paper: LIT-075
title: 'Elucidating the Design Space of Diffusion-Based Generative Models'
version: 1
tags:
- generative-modeling
date: '2026-09-09'
summary: >-
  Separates diffusion's tangled design choices into independent axes — sampling, training, and preconditioning of the score network. FID 1.79 on class-conditional CIFAR-10 at 35 network evaluations. Read from the abstract only.
---

# NOTE-tmpvjumo: Elucidating the Design Space of Diffusion-Based Generative Models

**This note is `Skimmed`, not `Read`.** The full text was not available
through the route used for the rest of [#114](https://github.com/dmarx/anthology-of-the-sota/issues/114) — ar5iv has no rendering for
`arXiv:2206.00364` — so what follows comes from the abstract and listing
metadata. Under [ADR-025](../decisions.d/ADR-025.md) that is **not enough to source a practice from**, and
this note deliberately has no claims table.

## Contribution

Argues that "the theory and practice of diffusion-based generative models are
currently unnecessarily convoluted", and remedies it by presenting a **design
space that separates the concrete design choices** rather than a new model.
From that separation it identifies changes to sampling, to training, and to
**preconditioning of the score networks**.

## Key insight

*(From the abstract; the mechanism is not verified here.)* The field's
formulations were entangled — a change to one part of a diffusion model
implied changes elsewhere because the parameterisations were coupled. Laying
the choices out as independent axes makes them separately improvable, and the
paper's evidence for that framing is **modularity**: the same changes improve
*pre-trained* score networks from previous work, not only models trained under
the new recipe.

## Assumptions

Not established from the abstract. Image generation — CIFAR-10 and
ImageNet-64 — at 2022 scales, NeurIPS 2022.

## Key results

*(As stated in the abstract.)*

- **FID 1.79** on CIFAR-10 class-conditional, **1.97** unconditional.
- **35 network evaluations per image** — "much faster sampling than prior
  designs".
- A **previously trained** ImageNet-64 model improved from FID **2.07 → 1.55**
  by design changes alone; **1.36** after re-training with the improvements.

That last is the modularity argument in numbers: most of the gain arrives
without retraining.

## Concepts

- **Design space** — the paper's framing device: the set of independent
  choices a diffusion model makes, presented separately rather than as one
  formulation.
- **Preconditioning** — the parameterisation of what the score network is
  asked to predict. The axis `SOTA-188` draws on, and the one this note
  cannot verify in detail.

## Bearing on the record

| practice | disposition |
|---|---|
| [SOTA-188](../practices.d/SOTA-188.md) parametrize the network so its prediction target has unit variance | **not verified** |

The abstract confirms that **preconditioning of the score networks** is one of
this paper's three axes, which is consistent with `SOTA-188` and is not the
same as confirming it. The specific claim — that the target should be
parameterised to unit variance — is a detail of the preconditioning section,
and that section was not read.

So `SOTA-188` is left exactly as it is, and this note records **why it is
still unchecked** rather than implying it was checked. That is the whole
reason the `Skimmed` status exists: `LIT-052` and `LIT-025` were, in this
vocabulary, never read at all, and the record had no way to say so.

## Limitations

Of this note, not the paper: everything above is the abstract's own summary.
No assumptions, no theorem statements, no method detail, and no claims table.

## Open questions

- **Get the full text and upgrade this note to `Read`**, then check
  `SOTA-188`'s unit-variance claim against the preconditioning section. That
  is the one open item, and it is about this reading rather than about the
  field.
- The modularity result — most of the gain transferring to pre-trained
  networks — is the kind of finding that generalises past diffusion, and
  whether it does is not something the abstract can answer.
