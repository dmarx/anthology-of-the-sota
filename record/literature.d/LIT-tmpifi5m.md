---
status: Active
title: 'Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture'
version: 1
tags:
- vision-and-graphics
date: '2026-09-07'
published: '2023-01-01'
arxiv: '2301.08243'
first_author: 'Assran'
keywords:
- 'self-supervised-learning'
- 'joint-embedding-predictive-architecture'
- 'representation-learning'
- 'masking'
- 'vision-transformer'
extended_by:
- LIT-tmp0kze1
summary: >-
  Assran et al. (2023), [ARXIV-2301.08243](https://arxiv.org/abs/2301.08243). I-JEPA: predict the
  *representations* of target blocks from a context block in the same image,
  rather than the pixels or an augmentation-invariant embedding. No
  hand-crafted augmentations, and the masking strategy is the design choice
  that does the work — large semantic targets, a spatially distributed
  context. A ViT-Huge/14 trains on ImageNet in under 72 hours on 16 A100s.
---

# LIT-tmpifi5m: Self-Supervised Learning from Images with a Joint-Embedding Predictive Architecture

Assran et al. (2023) — [ARXIV-2301.08243](https://arxiv.org/abs/2301.08243)

## Key takeaways

**The prediction target is a representation, and that is the whole idea.**
Generative self-supervision predicts pixels and spends capacity on detail
that carries no semantics; invariance-based self-supervision predicts
sameness across hand-crafted augmentations and inherits whatever biases the
augmentation set encodes. Predicting the *embedding* of a masked region from
the embedding of a visible one is neither — it is non-generative and needs no
augmentations.

**The masking strategy is the load-bearing hyperparameter.** Two conditions
are called out as crucial: target blocks large enough to be semantic, and a
context block informative enough — spatially distributed — to make the
prediction possible without being trivial. This is the part that later
JEPA work carries forward unchanged in spirit.

**Efficiency is a reported result, not a footnote.** ViT-Huge/14 on ImageNet,
16 A100s, under 72 hours, with strong downstream performance from linear
classification through object counting and depth prediction. The breadth of
that list is the claim that the representations are semantic rather than
task-tuned.

## Standing in the anthology

**The architectural idea, filed for its successor's sake.** The record holds
no vision self-supervision material — the vision cluster it inherited is
generative (diffusion, radiance fields, detection) and none of it is about
learning representations by prediction in latent space. I-JEPA is here
because [LIT-tmp0kze1](LIT-tmp0kze1.md) is here, and a line whose origin is missing is a line
the reader cannot check.

**Not a practice, and not close to one.** Nothing in this record trains a
vision encoder. The reason to hold it is that the JEPA argument — predict in
representation space, not in observation space — is a claim about objectives
that is stated generally and has been tried outside vision. If it ever
arrives in language-model training, this is where the line starts.
