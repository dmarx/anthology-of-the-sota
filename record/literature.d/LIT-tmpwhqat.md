---
status: Active
title: 'Kronecker-factored Approximate Curvature (KFAC) From Scratch'
version: 1
tags:
- training-optimization
- analysis-and-evaluation
date: '2026-10-01'
published: '2025-07-01'
arxiv: '2507.05127'
first_author: 'Dangel'
keywords:
- 'kfac'
- 'natural-gradient-descent'
- 'curvature-matrices'
- 'generalized-gauss-newton'
- 'fisher-information'
- 'empirical-fisher'
- 'kronecker-factorization'
implementations:
- 'f-dangel/kfac-tutorial'
summary: >-
  Dangel et al. (2025), [ARXIV-2507.05127](https://arxiv.org/abs/2507.05127) — a tutorial, math and PyTorch side
  by side, for the original KFAC of Martens and Grosse: fully-connected
  layers, no weight sharing. One scaffold covers the GGN, the Monte-Carlo
  Fisher and the empirical Fisher, and the only thing that changes between
  them is which vectors are backpropagated. Its practical content is the
  tests: KFAC is exact on a single data point, and on a deep linear network
  with square loss for the GGN and MC Fisher but not for the empirical
  Fisher, which is how to catch the scaling and factor-order bugs it says
  are easy to ship.
---

# LIT-tmpwhqat: Kronecker-factored Approximate Curvature (KFAC) From Scratch

Dangel et al. (2025) — [ARXIV-2507.05127](https://arxiv.org/abs/2507.05127)

## Key takeaways

- **A tutorial, and says so.** The scope is deliberately the original
  Martens and Grosse setting — fully-connected layers, no weight sharing —
  extended to the GGN (equal to the type-II Fisher for common losses), the
  Monte-Carlo type-I Fisher and the empirical Fisher, under both the
  column-major flattening the literature uses and the row-major flattening
  PyTorch uses. There are no training experiments and no optimizer
  comparison: nothing here measures whether KFAC trains faster than
  anything.
- **One scaffold, three curvatures.** Each layer's curvature block is
  approximated as `A ⊗ B`, `A` from the layer's inputs and `B` from vectors
  backpropagated to its outputs. Which curvature matrix is being
  approximated is decided entirely by the backpropagated vectors (and a
  reduction factor): the columns of a square root of the loss Hessian for
  the GGN; `M` sampled "would-be" gradients for the MC Fisher, with `M = 1`
  usual in practice; and the actual loss gradient for the empirical Fisher,
  which is why that flavour can recycle the gradient's own backward pass.
- **The approximation, and when it is exact.** The step that makes KFAC a
  single Kronecker product — pulling the average over data inside each
  factor — is motivated as the Frobenius-optimal fit under a structural
  assumption, and is exact whenever either the layer inputs or the
  backpropagated gradients do not depend on the data point.
- **Two tests follow from that.** On a dataset of one point, KFAC equals the
  GGN, the MC flavour converges to it, and the empirical flavour equals the
  empirical Fisher. On a deep linear network with square loss and arbitrary
  data (after Bernacchia et al., 2018), KFAC still equals the GGN and the MC
  flavour still converges to it, but **KFAC of the empirical Fisher does not
  equal the empirical Fisher**, because its backpropagated vector depends on
  the prediction. The paper names this test as the one that catches scaling
  bugs.
- **Pitfalls named.** Changing the flattening convention swaps the order of
  the two Kronecker factors, which matters because PyTorch flattens the
  other way from the papers; and the loss's reduction factor has to be
  carried into the factors. The empirical Fisher is not the Fisher, and the
  tutorial notes Adam is motivated by, but not equivalent to, preconditioning
  with its diagonal.
- **Deferred to later versions**: eigenvalue-corrected KFAC (which it calls
  the de facto standard for influence-function data attribution), the
  expand and reduce variants needed for weight sharing in transformers and
  convolutions, and a functional-style implementation.

## Standing in the anthology

**The elder of the matrix-preconditioner family, filed as background, not
as evidence.** [SOTA-165](../practices.d/SOTA-165.md) recommends preconditioning with matrices rather than
entrywise, and its members are Muon ([SOTA-121](../practices.d/SOTA-121.md)) and Shampoo and SOAP
([LIT-158](LIT-158.md), [LIT-157](LIT-157.md)). KFAC is the Kronecker-factored per-layer curvature
approximation those sit beside, and [LIT-158](LIT-158.md) describes Shampoo's own
preconditioner as a Kronecker-product approximation, to full-matrix AdaGrad.
The two factorizations are not the same object — KFAC's factors are input
activations and backpropagated output gradients, Shampoo's are built from
the gradient matrix itself — and this tutorial does not mention Shampoo, SOAP
or Muon, so it supplies no comparison. What it does supply is the vocabulary
for the difference: which curvature matrix a preconditioner approximates
(GGN, Fisher or empirical Fisher) is a choice, and those choices disagree.

**It sits under the record's influence-function line.** [LIT-401](LIT-401.md) (Grosse et
al.) approximates the inverse-Hessian-vector product with EK-FAC at up to 52B
parameters; this tutorial says the first step of EK-FAC is KFAC, and leaves
the eigenvalue correction itself for a later version. [LIT-476](LIT-476.md) found K-FAC
working about as well as Adam's second moment as a preconditioner for its
volume estimates, and the full Fisher of the KL doing no better than none —
an instance of this tutorial's point that the curvature matrices are not
interchangeable. Neither result is touched; this is where a reader of them
learns what the approximation is.

**Practice candidate, not filed:** test a Kronecker-factored curvature
implementation against the cases where it is exact — one data point, and a
deep linear network under square loss — before trusting it. The paper is a
source for it and nothing in the record states it.

Unread — no NOTE.
