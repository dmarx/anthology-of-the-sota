---
number: 287
status: Proposed
formerly:
- SOTA-tmp8b9jt
promote_when: >-
  A result on a task where backpropagation is not already at ceiling on the
  training set — anything large enough that fitting is the binding constraint
  — with the train-accuracy gap reported, from a group other than the
  authors. Another small-image classification result is not it: the method's
  parity on MNIST and CIFAR is established, and it is established in the
  regime where the gap costs nothing.
consensus: unreplicated
consensus_note: >-
  One paper, three small benchmarks. The backprop-free family it competes in
  is real and has several independent lines — forward-forward, target
  propagation, forward gradients — but nobody has reproduced this method, and
  the comparison against those lines is acknowledged by its own authors to be
  architecture-mismatched.
title: 'If you need to train without backpropagation, train each block to denoise a noisy label embedding conditioned on the raw input'
version: 1
tags:
- training-optimization
- model-architecture
date: '2026-09-21'
source:
- LIT-477
introduced_by:
- LIT-477
implementations: []
---

# SOTA-287: If you need to train without backpropagation, train each block to denoise a noisy label embedding conditioned on the raw input

## Source

Li, Teh and Pascanu (2025), [LIT-477](../literature.d/LIT-477.md) — read as
[NOTE-226](../notes.d/NOTE-226.md). MNIST, CIFAR-10 and CIFAR-100, no data
augmentation, 3 seeds × 5 inference runs.

## When this applies

Only when you have a reason not to backpropagate — biological plausibility,
activation memory you cannot afford, or a distributed setting where gradient
synchronisation is the bottleneck. **This is not a recommendation to stop
using backpropagation.** It is the answer to "which backprop-free method",
and within that question the answer is decisive.

## The claim

Embed the class label, run a fixed variance-preserving noising process on that
embedding to get a trajectory from label to noise, and train each block
independently to predict the clean embedding from the noisy one **and the raw
input**, under an L2 loss with a cross-entropy readout. At inference the
blocks run in sequence, each denoising what the previous one produced.

No forward pass across the network at training time, and no backward pass.
Each block's target comes from an analytic process, not from its neighbours.

**Use the discrete-time variant.** Continuous-time diffusion is several points
worse, and flow matching with one-hot embeddings **fails outright** on
CIFAR-100 (6.38 ± 4.9). Learned label embeddings rescue flow matching but do
not bring it level.

**Prefer a learned prototype embedding** at image dimension: it is the best
NoProp configuration on MNIST and CIFAR-10. Orthogonal and prototype
initialisations both beat random.

## What it buys

Against the prior backprop-free methods the margin is not close — CIFAR-10
test accuracy about 80, against 69.32 for local greedy forward gradients and
50.71 for difference target propagation; MNIST 99.54 against forward-forward's
98.63.

Memory roughly halves against backpropagation in discrete time (0.49 / 0.64 /
1.23 GB versus 0.87 / 1.17 / 1.73), and falls by four to thirteen times
against adjoint sensitivity in continuous time.

## Conditions

**It underfits, and that is the number to watch.** NoProp matches backprop on
*test* accuracy while sitting **8 to 15 points behind on train** — CIFAR-10
95.0–97.2 against 99.98, CIFAR-100 83.3–90.7 against 98.6–99.2. On MNIST and
CIFAR that is free, because backprop is at ceiling on the training set and
the test numbers are decided by generalization. In any setting where fitting
the training data is the binding constraint, it is the whole question, and
no result here speaks to it. The source does not raise it.

**The parity claim is against a structure-matched baseline, which cuts both
ways.** Building the backprop arm to share NoProp's forward structure is the
right comparison to have run — and that structure includes a direct connection
from the input into every block, which a conventional stack does not have. So
what is matched is a network designed around this method's constraint.

**And that structure is the method's condition, not a detail.** Every block
sees the raw input; that is what makes independent training possible. Whether
the stack is refining representations layer by layer, in the way depth is
normally supposed to work, is not investigated.

**Three small image classification benchmarks, no augmentation.** Nothing
here is sequence modelling, nothing is at a scale the record's other training
practices are argued at, and the paper's conclusion carries no limitations
section.

**The distributed-training motivation is unmeasured.** Independent blocks
ought to train on separate devices without gradient synchronisation, which is
one of the three reasons the introduction gives for wanting this. No
distributed experiment appears in the paper.
