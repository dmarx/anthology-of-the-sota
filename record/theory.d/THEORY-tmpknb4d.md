---
status: Active
title: 'A transformer can run a learning algorithm on a model held in its activations, and the architecture admits several, so a construction identifies none'
version: 1
tags:
- in-context-learning
- model-architecture
- analysis-and-evaluation
date: '2026-09-22'
source:
- LIT-tmpehkbl
- LIT-tmp700y6
- LIT-tmprd6ad
corrects:
- THEORY-tmpvwjjo
summary: >-
  Three groups have constructed transformer weights that run a named learning
  algorithm in the forward pass on a model carried in the activations: one
  gradient step per linear-self-attention layer (von Oswald et al.,
  [LIT-tmpehkbl](../literature.d/LIT-tmpehkbl.md)), a Sherman–Morrison ridge update in constant depth and `O(d²)`
  width (Akyürek et al., [LIT-tmp700y6](../literature.d/LIT-tmp700y6.md)), and `k` Iterative Newton steps in
  `k + 8` layers (Fu et al., [LIT-tmprd6ad](../literature.d/LIT-tmprd6ad.md)). The frame is what survives the
  dispute about which algorithm; the corollary is that no construction can
  settle that dispute, because the architecture admits all three.
explains:
- SOTA-tmpaocvh
- SOTA-tmpxlbv7
---

# THEORY-tmpknb4d: A transformer can run a learning algorithm on a model held in its activations, and the architecture admits several, so a construction identifies none

<!-- inactive-ok-file: THEORY-tmpvwjjo — Rejected, and cited as the rejected account itself: this document is part of the evidence that retired it, not a recommendation resting on it. -->
<!-- inactive-ok-file: ADR-031 — Proposed, cited as the decision that lets an explanation be retired while the practice it explained goes on working; that is the schema this document is filed under, and Proposed is the resting state of an unmoved decision here. -->

## The account

Write the in-context examples into the token stream as `(x_j, y_j)` pairs.
Then some of the network's activations can be read as the parameters of a
small model, and a layer can be read as an update to those parameters. On this
view a forward pass over a prompt is a training run over a dataset, and the
prediction for the query token is the trained model's output.

The frame is not an analogy. It has been made precise three times, for three
different algorithms, by three groups working independently.

## What is established

- **One gradient step per layer.** [LIT-tmpehkbl](../literature.d/LIT-tmpehkbl.md), Proposition 1: with
  `W_K = W_Q = [[I_x, 0], [0, 0]]`, `W_V = [[0, 0], [W_0, −I_y]]` and
  `P = (η/N)I`, a linear self-attention step on every token is exactly the
  token change `(0, −ΔW x_j)` that one gradient-descent step on the regression
  loss induces.
- **A closed-form ridge update.** [LIT-tmp700y6](../literature.d/LIT-tmp700y6.md), Theorem 2: a transformer
  predicts according to a single Sherman–Morrison update with a constant number
  of layers and `O(d²)` hidden space. Theorem 1 gives the gradient step in
  `O(d)`.
- **A second-order method.** [LIT-tmprd6ad](../literature.d/LIT-tmprd6ad.md), Theorem 5.1: for any `k` there exist
  weights predicting `x_testᵀ ŵ_k^Newton` from
  `M_j = 2M_{j−1} − M_{j−1} S M_{j−1}`, `M_0 = αS`, `S = XᵀX`, in `k + 8`
  layers with `O(d)` hidden dimension.
- **Trained models do land in the frame.** Across all three papers,
  transformers trained on in-context regression improve their predictions
  monotonically with depth and converge to the problem's optimal estimator.
  Whatever they are running, they are running something iterative on something
  model-shaped.

## And what the same evidence rules out

**No construction of this kind can identify the algorithm.** That follows from
the constructions themselves: the architecture expresses first-order,
closed-form and second-order solvers alike, at comparable and modest cost. A
proof that a transformer *can* implement algorithm `A` is therefore evidence
about the architecture, not about any particular trained model — and it is the
step most often skipped when this literature is summarized.

This is why the record files the identification separately, as
[THEORY-tmpvwjjo](THEORY-tmpvwjjo.md), and why that document is `Rejected` while this one is
`Active`. [ADR-031](../decisions.d/ADR-031.md): an account can be wrong about the reason while the thing it
was invoked to explain goes on happening.

## Standing

`Active`. Nothing in the dispute touches the constructions; [LIT-tmpvwpn4](../literature.d/LIT-tmpvwpn4.md),
which argues hardest against the gradient-descent reading, is explicit that
what the constructions establish is architectural expressivity and lets that
stand.

## What would change this

A demonstration that in-context learning in some model is *not* organized
around anything activation-resident and model-shaped — for instance a
mechanistic account of a competitive in-context learner whose per-layer
behaviour has no iterative reading at all. [LIT-tmprd6ad](../literature.d/LIT-tmprd6ad.md)'s LSTM result is the
nearest thing: trained identically, LSTMs weight recent examples more than
early ones and their predictions do not improve across layers, which shows
this frame is architectural rather than generic. It is a limit on the frame's
scope, not a counterexample within it.
