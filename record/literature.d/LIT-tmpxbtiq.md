---
status: Active
title: 'Muon: An optimizer for hidden layers in neural networks'
version: 1
tags:
- training-optimization
date: '2026-09-05'
published: '2024-12-01'
# A blog post, never posted to arXiv, and the origin of an optimizer three
# frontier labs now pretrain with. Filed under the source field group
# (ADR-009) for the same reason LIT-119 and LIT-051 are.
url: 'https://kellerjordan.github.io/posts/muon/'
first_author: 'Jordan'
keywords:
- 'optimizer'
- 'muon'
- 'orthogonalization'
- 'newton-schulz'
- 'momentum'
implementations:
- Muon
summary: >-
  Jordan et al. (2024), blog post. Where Muon comes from: take the momentum
  matrix for a hidden weight, orthogonalise it with a few Newton–Schulz
  iterations, and step in that direction — leaving embeddings, the classifier
  head and the gains and biases to AdamW.
---

# LIT-tmpxbtiq: Muon: An optimizer for hidden layers in neural networks

Keller Jordan, Yuchen Jin, Vlado Boza, You Jiacheng, Franz Cesista, Laker
Newhouse and Jeremy Bernstein (2024) —
[kellerjordan.github.io/posts/muon](https://kellerjordan.github.io/posts/muon/)

## Key takeaways

- The rule: for a hidden weight *matrix*, take the SGD-momentum update and
  replace it with its nearest orthogonal matrix, approximated by a handful of
  Newton–Schulz iterations, then step. Everything that is not a hidden matrix
  — embeddings, the classifier head, gains and biases — stays on AdamW, and
  the scoping is part of the method rather than an implementation detail.
- The claim it was published on is sample efficiency at small wall-clock
  cost: substantially fewer tokens to a target, with the orthogonalisation
  adding only a few percent per step because Newton–Schulz is a short
  sequence of matrix multiplies.
- It is a *speedrunning* artefact — developed against NanoGPT and CIFAR
  wall-clock records — which is why it arrived without scaling evidence and
  why the papers that followed are all about whether it survives scale.

## Standing in the anthology

The origin of the record's optimizer chain, and until now the one link in it
the corpus did not hold. [LIT-122](LIT-122.md), [SOTA-121](../practices.d/SOTA-121.md) and [SOTA-131](../practices.d/SOTA-131.md) each name it as "a 2024
blog post by Jordan and collaborators, which is not in the corpus"; it is now.

Filed with a `url:`, the third such source after [LIT-119](LIT-119.md) and [LIT-051](LIT-051.md), and the
clearest case yet for [ADR-009](../decisions.d/ADR-009.md) — three laboratories pretrain frontier models
with this and there is no paper to cite. The chain now reads: this →
production form and scaling evidence ([LIT-122](LIT-122.md)) → QK-Clip at a trillion
parameters ([LIT-132](LIT-132.md)) → per-head orthogonalisation at 2.8T ([LIT-131](LIT-131.md)), with
[LIT-tmpqpka6](LIT-tmpqpka6.md) as the outside comparison and [LIT-tmp2hq9o](LIT-tmp2hq9o.md) as the diagnosis of
where its advantage goes at scale.
