---
number: 278
status: Read
formerly:
- NOTE-tmpnpngw
paper: LIT-535
title: 'Linear in Newton steps, exponential in gradient steps: a rate is what separates the rivals'
version: 1
date: '2026-09-22'
summary: >-
  Read as the challenge from inside the gradient-descent line's own setup.
  Matching each transformer layer to the best number of steps of a candidate
  algorithm gives a linear trend against Iterative Newton — about 3 iterations
  per middle layer — and an exponential one against gradient descent; on data
  with condition number 100 the transformer is unchanged while GD needs 2,000
  steps a 12-layer model cannot hold. The method is the contribution: fits
  cannot separate these rivals and rates can.
---

# NOTE-278: Linear in Newton steps, exponential in gradient steps: a rate is what separates the rivals

<!-- inactive-ok-file: THEORY-068 — Rejected, and cited as the rejected account itself: this document is part of the evidence that retired it, not a recommendation resting on it. -->
<!-- inactive-ok-file: SOTA-324 — Proposed, the sibling practice filed in this same contribution and named as its counterpart; it is new, not retired. -->

## Contribution

It takes the mesa-optimization setup as given and asks a question the earlier
papers did not: not *does the output look like algorithm A's output*, but *do
successive layers advance at algorithm A's rate*. Under that measurement the
transformer is a second-order method, and gradient descent is not a
description of it — a conclusion reached in the same task, the same GPT-2
backbone and the same training objective as the papers it contests.

## Key insight

**Two algorithms that converge to the same answer can be told apart by how
fast they get there.** GD converges at `O(κ log(1/ε))`, Iterative Newton at
`O(log κ + log log(1/ε))`. So if each transformer layer is one step of some
algorithm, matching layers to steps gives a straight line for the algorithm
with the right rate and a curve for the wrong one — and the curve is the
diagnosis. This is a general move for identifying an internal computation,
and it is why this record files the practice separately from the finding.

## Assumptions

- **Trained on the ICL objective**, exactly Garg et al.'s setup: GPT-2, 12
  layers, 8 heads, `d = 20` linear regression.
- Layerwise predictions are obtained by **re-training only a read-out head**
  per layer, everything else frozen — the layer's hidden state is assumed to
  carry a prediction a linear head can extract.
- The similarity measure compares each layer against the best-matching step
  count of each candidate algorithm; the same trends hold under a second
  measure based on induced weights.
- Theorem 5.1 uses **full attention and ReLU activations**, not causal
  attention — stated by the authors.
- Ill-conditioned experiments draw `x ~ N(0, Σ)` with `κ(Σ) = 100`, first
  `d/2` eigenvalues 100 and last `d/2` equal to 1, **eigenbasis resampled
  uniformly per sequence**.

## Key results

- **Predictions improve monotonically with layer index**, so the layers behave
  like the steps of an iterative algorithm at all.
- **Linear against Newton, exponential against GD.** Between layers 3 and 9,
  each layer corresponds to roughly **3 additional Iterative Newton
  iterations**; against gradient descent the best-matching step count grows
  exponentially, becoming linear only in log scale. The trend stops at the last
  layers because both have converged to OLS. Some single layers advance as far
  as **hundreds** of GD steps.
- **Ill-conditioning.** At `κ(Σ) = 100` the transformer still matches Iterative
  Newton at **21 iterations**, the same as at `Σ = I`; GD needs about **2,000**
  steps, which twelve layers cannot implement. No fixed or sparse
  preconditioner is available, because the eigenbasis is resampled per
  sequence.
- **Theorem 5.1.** For any `k` there exist transformer weights predicting
  `x_testᵀ ŵ_k^Newton`, with `M_j = 2M_{j−1} − M_{j−1} S M_{j−1}`, `M_0 = αS`,
  `S = XᵀX`; hidden dimension `O(d)`, **`k + 8` layers** — one per iteration,
  3 to initialize `M_0`, 5 to read out. *Holds when:* full attention, ReLU
  self-attention layers.
- **BFGS shows the same linear trend**, so the claim is *a* second-order
  method, not Iterative Newton in particular. The paper says this explicitly.
- **`O(d)` hidden dimension is needed** to mimic OLS at `d = 20` — hidden size
  32 or 64 works, 8 and 16 do not.
- **LSTMs are different.** Trained identically, they weight recent in-context
  examples more than early ones — online gradient descent's signature — and
  their predictions do not improve across layers.

## Limitations

**It is still a model trained on the ICL objective.** The Hypothesis-1 problem
[ARXIV-2310.08540](https://arxiv.org/abs/2310.08540) raises applies here as much as to the papers this contests;
this note does not credit it with evidence about pretrained language models.

**"Some second-order method" is where the evidence stops**, and the paper is
disciplined about saying so. Any reading that upgrades this to "transformers
implement Newton's method" is reading past it.

**Theorem 5.1 uses full attention**, so the construction is not directly a
statement about a causal decoder.

## Bearing on the record

It is the strongest evidence in this cluster, and the reason the record files
[THEORY-068](../theory.d/THEORY-068.md) as `Rejected` rather than `Proposed` for the deep-model case:
the rate measurement and the conditioning probe are two independent
separations, and both point the same way.

The method — separate rival accounts of an internal computation by a rate and
by a regime where they must differ, rather than by output similarity — is
filed as [SOTA-324](../practices.d/SOTA-324.md), because it generalizes past this dispute and the record
holds nothing else that says it.

## Open questions

- **What does the rate measurement say about a pretrained language model?**
  The layer-to-iteration heatmap needs a task with a known optimal algorithm;
  running it on a model pretrained on text is the experiment neither side of
  this dispute has done.
