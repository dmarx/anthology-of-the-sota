---
number: 68
status: Rejected
formerly:
- THEORY-tmpvwjjo
title: 'In-context learning is gradient descent on an implicit model'
version: 1
tags:
- in-context-learning
- analysis-and-evaluation
- training-optimization
date: '2026-09-22'
source:
- LIT-533
- LIT-532
summary: >-
  The identification the field read off [LIT-533](../literature.d/LIT-533.md)'s title: that what a
  transformer does with its context is gradient descent on a model held in its
  activations. Filed `Rejected` and kept, on three separate grounds. Beyond one
  layer the source paper's own models match GD++ — gradient descent on data
  transformed by `I − γXXᵀ` — not gradient descent. [LIT-535](../literature.d/LIT-535.md) matches layers
  to steps and finds a linear correspondence with Iterative Newton and an
  exponential one with GD, and a conditioning regime GD cannot reach.
  [LIT-536](../literature.d/LIT-536.md) proves an equivalent algorithm must share ICL's order
  sensitivity, which GD has none of. What survives is [THEORY-067](THEORY-067.md), the
  frame without the name.
corrected_by:
- THEORY-067
---

# THEORY-068: In-context learning is gradient descent on an implicit model

## The claim, as it was made

A transformer given a prompt of `(x, y)` pairs and a query does not merely
pattern-match; it *trains*. Specific weights make one linear-self-attention
layer compute exactly one gradient-descent step on an implicit linear model
([LIT-533](../literature.d/LIT-533.md), Proposition 1), a single trained layer approximately finds
those weights, and stacking layers stacks steps. [LIT-532](../literature.d/LIT-532.md) arrives at a
compatible construction independently, and reports that its shallowest trained
learners sit nearest gradient descent among the reference predictors.

Read together, and compressed into one sentence, this became the standard
answer to "how does in-context learning work". The compression is the problem.

## Why it is `Rejected`

**Three refutations, at three different depths, and none of them is the
others' argument.**

**1. Beyond one layer, the source paper reports a different algorithm.**
[LIT-533](../literature.d/LIT-533.md)'s looped two-layer and unrolled five-layer models outperform `K`
steps of gradient descent, and align instead with GD++: gradient descent on
data transformed by `H(X) = (I − γ X Xᵀ)`, with a learning rate and a `γ`
fitted per layer. A first-order step in a data-dependent transformed geometry
is a preconditioned method, not gradient descent. The exact result is about a
single layer, and a single layer is not a transformer.

**2. The layer-to-step correspondence has the wrong shape.** [LIT-535](../literature.d/LIT-535.md)
matches each layer of a trained model to the best-fitting number of steps of
each candidate algorithm. Against Iterative Newton the relation is **linear**
— roughly 3 iterations per middle layer, layers 3 through 9. Against gradient
descent it is **exponential**, and individual layers advance as far as
hundreds of GD steps. Independently, on data with condition number 100 and a
per-sequence random eigenbasis, the transformer matches Newton at 21
iterations exactly as in the isotropic case while GD needs about 2,000 steps —
more than a twelve-layer model can hold, and not fixable by any preconditioner
available across the data distribution. Two separations, same direction.

**3. For a naturally pretrained model, the equivalence contradicts itself.**
[LIT-536](../literature.d/LIT-536.md)'s Theorem 1: if `A` is equivalent to ICL then for any two
demonstration orderings `M_Θ0(σ_A ∘ x_t) − M_Θ0(σ_B ∘ x_t) =
M_{Θ_σA}(x_t) − M_{Θ_σB}(x_t)`. Gradient descent averages over the batch, so
the right side is zero; in-context learning's order sensitivity is a
well-measured fact, so the left side is not. Measured on LLaMA-7B, ICL is more
order-sensitive than GD, SGD and Adam alike. The paper adds that the
construction's required sparsity — above 99.99% in `W_K` and `W_Q` at LLaMA's
width — is nowhere near what real weights show, and that ICL accuracy stays
flat across GPT-J checkpoints whose parameters keep moving, so equivalence at
one point in weight space would not be the claim anyway.

## What is *not* rejected

**The frame.** [THEORY-067](THEORY-067.md) — a transformer can run a learning algorithm
on a model carried in its activations — is `Active`, and every refutation
above is stated inside it. [ADR-031](../decisions.d/ADR-031.md) is exactly this case: the explanation was
wrong and the phenomenon it explained is real.

**The one-layer result.** [LIT-533](../literature.d/LIT-533.md)'s Proposition 1 is a proof and a single
trained linear-self-attention layer does approximately implement it. Nothing
here touches that.

**"Something gradient-like".** [LIT-536](../literature.d/LIT-536.md) concludes that the equivalence
"remains an open hypothesis", not that the resemblance is illusory, and this
record follows it. What is rejected is the identification of the algorithm as
gradient descent, which is the form in which the claim actually travels.

## What the record is left needing

Nobody has measured the layer-to-iteration correspondence on a model
pretrained on text. Every result above is either a construction, or a
measurement on a model trained on the task family it was then tested on.
[LIT-535](../literature.d/LIT-535.md)'s method would transfer — pick a prompt task whose optimal
algorithm is known, probe a pretrained model layer by layer, and see whether
the rate is first-order, second-order or neither — and the record can find
nobody who has run it.
