---
status: Proposed
promote_when: >-
  An independent group training a normalized transformer at a scale where the
  record's other training-recipe practices are argued — and reporting the
  comparison in wall-clock or FLOPs rather than tokens, since the token figure
  is the one this paper's own step-time footnote halves. A group confirming
  that unconstrained transformer matrices drift toward poor conditioning is
  not it; that is the diagnosis, not the remedy.
consensus: unreplicated
consensus_note: >-
  One group, one codebase, two model sizes. The sphere argument has a
  literature behind it in representation learning, but nobody outside NVIDIA
  has trained a normalized transformer and reported the comparison.
title: 'Put every matrix and hidden state on the unit hypersphere, and make each block''s residual step size a learned per-dimension parameter'
version: 1
tags:
- model-architecture
- model-stability
- training-optimization
date: '2026-09-21'
source:
- LIT-tmp7z4xc
introduced_by:
- LIT-tmp7z4xc
implementations: []
explained_by:
- THEORY-tmp99061
---

<!-- inactive-ok-file: SOTA-122 — Proposed and unreplicated, exactly as this
     practice is, and named as the sibling remedy rather than as support. The
     section citing it says so in its own first sentence -->

# SOTA-tmpg9ovm: Put every matrix and hidden state on the unit hypersphere, and make each block's residual step size a learned per-dimension parameter

## Source

Loshchilov, Hsieh, Sun and Ginsburg (2024), [LIT-tmp7z4xc](../literature.d/LIT-tmp7z4xc.md) — read as
[NOTE-tmp04rue](../notes.d/NOTE-tmp04rue.md). 0.5B and 1B decoder-only models on OpenWebText at
1k, 4k and 8k context.

## The claim

Normalize every matrix along its embedding dimension after each optimizer
step — embeddings, `Q`, `K`, `V`, the output projection, both MLP matrices —
and keep every hidden state on the same unit sphere. Then:

1. **Delete every normalization layer.** No LayerNorm, no RMSNorm, and no
   placement question to argue about.
2. **Replace the residual add with a retraction.** `h ← Norm(h + α ⊙ (f(h) − h))`,
   where `f` is the attention or MLP block and `α` is a learned vector, one
   entry per embedding dimension. The block proposes a direction; `α` is how
   far you go.
3. **Restore scale only where normalization removed something load-bearing**:
   before the QK product, on the MLP intermediate, and on the logits. This is
   not optional — constraining the inputs of non-linear units is the failure
   the scaling factors exist to prevent.
4. **Set weight decay and learning-rate warmup to zero.** With norms fixed by
   construction, there is nothing for either to control.
5. Change the softmax scale from `1/√d_k` to `√d_k`.

The reported payoff is 4×, 10× and 20× fewer tokens to a given validation
loss at 1k, 4k and 8k context, at matched parameter count against a
learning-rate-tuned baseline.

## What the number means

**It is tokens, not time.** Step time is 80% higher at 4k context and 60%
higher at 8k, because there are six normalizations per layer instead of two
and they are not fused. As measured, 10× in tokens is about **5.5× in wall
clock**, and 20× is about 12.5×. The paper expects the overhead to fall with
kernel work and with depth; no optimized implementation has been published.

Quote the wall-clock figure. The token figure is correct and is not the one a
reader is deciding on.

## Conditions

**Scale.** 0.5B and 1B, on OpenWebText, which the authors themselves describe
as not of the highest quality. Their conclusion asks for larger models and
real data. The record's other training-recipe practices are argued one to
three orders of magnitude above this.

**One group.** NVIDIA, one internal Megatron-LM codebase. The public
re-implementation is stated by its authors to replicate the internal results
only qualitatively.

**Two hyperparameters out, one in.** At the largest configuration tested —
1B at 8k — Adam's `ε` on the `α` parameters had to be raised from its default
to 0.1 to keep the learning-rate curve smooth. That is the direction of
scaling, so treat "removes weight decay and warmup" as an even trade until
somebody shows otherwise.

**It collides with three practices this record already holds**, and the
collision is a gap in their conditions rather than a contradiction.
[SOTA-008](SOTA-008.md) and [SOTA-009](SOTA-009.md) recommend learning-rate warmup;
[SOTA-120](SOTA-120.md) recommends decoupled weight decay. All three are argued on
unconstrained-norm architectures, where the thing they manage is free to
drift. Here it cannot. Note also that `SOTA-008`'s claim is specifically about
**large batch size**, and global batch 512 at 1B is not that regime — so the
warmup removal is untested against the case warmup was introduced for.

**The implementation trap is real and named.** The optimizer's copy of the
parameters must be normalized, not only the instantiated model parameters.
The authors call missing it a common bug; a partial implementation will
silently be a different method.

## What is separable, and untested

The recipe bundles two independent ideas: putting everything on the sphere,
and making the residual step size a learned per-dimension vector. Nothing
requires them together — `α` could be added to an ordinary pre-norm
transformer tomorrow — and no ablation separates them. If most of the gain is
`α`, this practice is much cheaper than it looks; if it is the sphere, the
step-time overhead is unavoidable.

Two smaller knobs are known to be nearly free: dropping QK normalization costs
0.12% of validation loss and saves 12% of step time, and the scaling factors
can be fixed or shared globally with only slight degradation.

## Adjacent, by a different route

[SOTA-122](SOTA-122.md) reaches the same diagnosis — a weight matrix's norm should be
managed deliberately rather than left as a side effect of the learning rate
and weight decay — and applies a different remedy, learnable per-row and
per-column multipliers. Different groups, no citation either way, and both
`Proposed` and `unreplicated`. Two independent arrivals at one diagnosis is
worth more than either remedy's evidence.

## Known implementations

- `NVIDIA/ngpt` — the authors' nanoGPT re-implementation, published with the
  caveat that it qualitatively replicates the internal experiments and should
  not be used in production
