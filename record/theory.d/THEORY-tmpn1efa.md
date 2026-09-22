---
status: Proposed
promote_when: >-
  The sensitivity measure shown to be invariant to the choice it is defined
  relative to: the architecture ranking — transformers below MLPs, CNNs,
  ConvMixers and LSTMs — reproduced across a sweep of perturbation
  distributions rather than one per modality, at matched training accuracy.
  That would separate "transformers learn simpler functions" from "this probe
  favours transformers". What would NOT meet it: another benchmark on which
  transformers are more robust. Robustness rankings are what this account
  proposes to explain, and the record holds them already.
title: 'Transformers are biased toward low-sensitivity functions, and that bias is what their robustness is made of'
version: 1
tags:
- analysis-and-evaluation
- model-architecture
date: '2026-09-22'
source:
- LIT-tmpc05l0
summary: >-
  Vasudeva et al. (2024), [LIT-tmpc05l0](../literature.d/LIT-tmpc05l0.md) — the probability
  that a model's output changes under a random perturbation of one input token
  is lower for transformers than for MLPs, CNNs, ConvMixers or LSTMs, on
  vision and language alike. Low sensitivity is a simplicity bias in
  established senses, it provably implies robustness in the Boolean case, and
  it tracks flatness. `Proposed`: the theory is Boolean and NTK, the
  experiments are not, and the metric is defined relative to a perturbation
  distribution nobody has swept.
---

# THEORY-tmpn1efa: Transformers are biased toward low-sensitivity functions, and that bias is what their robustness is made of

## Source

Vasudeva, Fu, Zhou, Kau, Huang and Sharan (2024),
[LIT-tmpc05l0](../literature.d/LIT-tmpc05l0.md) — read as [NOTE-tmpwuv3u](../notes.d/NOTE-tmpwuv3u.md).
ICLR 2025.

## The account

**Sensitivity** is the probability that a model's output changes when one
input token is randomly perturbed, measured over a dataset and a perturbation
distribution. It is an old quantity in Boolean function analysis, where it is
tied to the degree of the representing multilinear polynomial and to the size
of the smallest decision tree — so a bias toward low sensitivity is a bias
toward simple functions in several independently motivated senses.

The claim has three parts.

**Transformers have it and other architectures have it less.** At matched
training accuracy, transformers show lower sensitivity than MLPs, CNNs,
ConvMixers and LSTMs, on vision and on language. One scalar, computable for
any architecture, separates them — which is unusual, because most
architecture comparisons are about parameterizations that share nothing.

**It is provable where proof is available.** In the NTK regime, the paper
derives the low-sensitivity bias from spectral bias. It separately proves that
low sensitivity implies better robustness, so the robustness of transformers
is not an additional empirical fact needing its own explanation — on this
account it is the same fact.

**It shows up in the loss landscape and in training dynamics.** Low sensitivity
corresponds to flatter minima. And on modular addition, sensitivity falls
during the grokking plateau while the training loss does not, which makes it
a progress measure for a transition the loss cannot see.

## Why `Proposed`

**The proofs and the experiments are in different regimes.** The theory is
Boolean and NTK; the interesting results are CIFAR, CIFAR-10-C and language.
Nothing establishes that the extended sensitivity notion inherits the Boolean
properties that make low sensitivity mean "simple".

**The metric is defined relative to a choice nobody swept.** Sensitivity
depends on the perturbation distribution `P` — Gaussian per patch for images,
uniform over vocabulary for tokens. Sensible choices, and unexamined ones. A
measure whose ranking might move with the probe is a measure that needs the
probe varied, which is what the `promote_when` asks for.

**Flatness is correlational here**, and this record already holds an account
([THEORY-035](THEORY-035.md)) under which sharpness is driven by the step size rather
than by the function class. Whether low sensitivity produces flatness or both
follow from something else is not addressed.

## What it does not say

**It does not say transformers are better.** It says they occupy a different
region of function space under one measure, and that the region has properties
which happen to include robustness. Simplicity bias is not uniformly good; a
model biased toward low-degree functions is biased *against* the high-degree
ones, and nothing here asks what that costs.

**It does not make sensitivity a validated progress measure.** The grokking
result is one synthetic task. [SOTA-200](../practices.d/SOTA-200.md) asks whether an apparent
capability jump is a measurement artefact and would be strictly better off
with a cheap architecture-agnostic progress measure; this is a candidate for
that role and is not yet evidence for it.

**It does not explain the mechanism inside the architecture.** Attention,
depth, normalization — nothing here says which component produces the bias,
only that models with attention have it and models without it have less.
