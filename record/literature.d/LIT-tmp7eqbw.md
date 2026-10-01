---
status: Active
title: 'Position: Curvature Matrices Should Be Democratized via Linear Operators'
version: 1
tags:
- analysis-and-evaluation
- training-optimization
- systems-optimization
date: '2026-10-01'
published: '2025-01-31'
arxiv: '2501.19183'
first_author: 'Dangel'
keywords:
- 'linear-operators'
- 'curvature-matrices'
- 'hessian-vector-products'
- 'generalized-gauss-newton'
- 'kfac'
- 'randomized-linear-algebra'
- 'curvlinops'
implementations:
- 'curvlinops'
summary: >-
  Dangel et al. (2025), [ARXIV-2501.19183](https://arxiv.org/abs/2501.19183) — a position paper with a library
  behind it: expose the Hessian, GGN, Fisher flavours and (E)KFAC as linear
  operators, so applications ask only for matrix-vector products and the
  batching, scaling and determinism pitfalls live in one tested place. Its
  measurements are costs in units of a gradient, on ResNet-50 and nanoGPT:
  computing KFAC's factors takes 1.5–2.5 gradients and applying them
  0.1–0.2, while a Hessian-vector product takes 4.5–5.5 gradients and 3–4.5×
  the memory in PyTorch.
---

# LIT-tmp7eqbw: Position: Curvature Matrices Should Be Democratized via Linear Operators

Dangel et al. (2025) — [ARXIV-2501.19183](https://arxiv.org/abs/2501.19183)

## Key takeaways

- **The position.** Curvature matrices should be handled as linear
  operators — objects that supply matrix-vector products — rather than as
  dense matrices or bespoke code per application. The argument is made in
  three parts (they encapsulate complexity, simplify applications, and are
  extensible and interoperable) and carried by `curvlinops`, a PyTorch
  library offering the Hessian, GGN, Monte-Carlo and empirical Fisher, and
  several (E)KFAC flavours with their damped inverses, including the exact
  damping of Grosse et al. (2023) and the KFAC-reduce variant for
  weight-sharing layers.
- **What the operator hides is the part people get wrong.** Accumulating
  over batches with the right reduction factor; accepting parameters as one
  vector or as per-layer tensors; and determinism — dropout, data
  augmentation and batch normalization make the represented matrix change
  between calls, which destabilises iterative solvers such as conjugate
  gradients, so the library can check that two consecutive evaluations
  agree. KFAC is tested against the settings where it is exact.
- **Costs, measured** on an A40 with ResNet-50 (≈26M parameters, ImageNet)
  and nanoGPT (≈124M, Shakespeare), with the ordering KFAC (inverse) ≪
  Fisher/GGN < Hessian:
  - KFAC's Kronecker factors cost 1.5–2.5 gradients of time, more for
    convolutions; inverting them adds little; storing them adds no more than
    10–20% memory over a gradient; applying them costs 0.1–0.2 gradients.
  - A Hessian-vector product costs 4.5–5.5 gradients of time and 3–4.5× the
    memory, consistent with the 4–5 and 3–3.5× that Dagréou et al. report
    for PyTorch; the paper cites 2–4× time in JAX with forward mode and
    compilation, which `curvlinops` does not yet use.
  - GGN and Fisher products are faster and lighter than Hessian products,
    but not the factor of two Martens (2010) reported.
  - Caveats stated: KFAC skips normalization-layer parameters and nanoGPT's
    ≈50K-wide output layer, and PyTorch's efficient attention had to be
    disabled for some operators because it does not support double
    backpropagation.
- **Applications shown as code, not as results**: Newton-CG, Neumann and
  KFAC optimizer steps; influence functions with EKFAC; Fisher-weighted
  model merging, including a full-Fisher-via-CG variant the paper calls
  unexplored; Optimal-Brain-Surgeon pruning with a Hutchinson diagonal; and
  the overlap of the gradient with the Hessian's top eigenspace. It also
  wraps the preconditioners of inverse-free KFAC and inverse-free Shampoo
  optimizers as operators, so an optimizer's curvature estimate can be
  exported mid-training.
- **Its own alternative views**: encapsulation can duplicate work (a KFAC
  empirical-Fisher preconditioner computed inside an operator may need a
  second forward-backward pass that a fused optimizer would not); hiding
  complexity can promote using the wrong curvature matrix for the
  application; and some applications need sub-matrices, which a
  matrix-vector interface does not give.

## Standing in the anthology

**It puts a number on a cost the record states loosely.** [SOTA-011](../practices.d/SOTA-011.md) says the
extreme Hessian eigenvalues are found by Lanczos or power iteration on
Hessian-vector products, "each of which costs roughly a forward-backward
pass". A gradient is a forward-backward pass, and this paper measures a
Hessian-vector product at 4.5–5.5 of them in PyTorch on a 124M-parameter
transformer, with 3–4.5× the memory. The practice's conclusion — a diagnostic
run at intervals, not a per-step monitor — stands and is if anything
strengthened; its per-product cost was off by a factor of four to five, and
[SOTA-011](../practices.d/SOTA-011.md) is corrected from this measurement at its version 3.

**It is infrastructure under the influence-function line.** [LIT-401](LIT-401.md)
computes influence at scale with EK-FAC, and [LIT-403](LIT-403.md) introduced the method
with Hessian-vector products; this library offers both routes behind one
interface, with the damping scheme [LIT-401](LIT-401.md) used.

**It touches the Muon and Shampoo cluster only at the edge.** [SOTA-165](../practices.d/SOTA-165.md)'s
members precondition with matrices; this paper exposes the preconditioner of
an inverse-free Shampoo variant as an operator and reports nothing about
training with it. Its cost figures are for curvature *products*, not for an
optimizer step, so they do not bear on [LIT-158](LIT-158.md)'s 10% per-step overhead.

Unread — no NOTE.
