---
status: Proposed
title: 'Attach learnable per-row and per-column multipliers to weight matrices so their norms are learned, not set by LR and WD'
version: 1
tags:
- training-optimization
- tiny-models
date: '2026-09-05'
published: '2026-01-15'
source:
- LIT-119
summary: >-
  Falcon-LLM Team (2026), [LIT-119](../literature.d/LIT-119.md) — the Falcon-H1-Tiny technical blogpost. Up to 20% relative gain on MMLU, BBH and GSM8K over a Muon baseline at 200 GT.
---

# SOTA-122: Attach learnable per-row and per-column multipliers to weight matrices so their norms are learned, not set by LR and WD

## Source

Falcon-LLM Team (2026), [LIT-119](../literature.d/LIT-119.md) — the Falcon-H1-Tiny technical blogpost.

The claim, from [ARXIV-2601.04890](https://arxiv.org/abs/2601.04890) ([LIT-121](../literature.d/LIT-121.md)) and validated in the blogpost at the 90M
scale: under a decoupled weight decay, a matrix layer settles into an
equilibrium norm determined by the learning rate and the weight decay
coefficient rather than by the data. Attaching a learnable scalar multiplier
to each row and each column of every weight matrix (the authors' *learnable
multipliers*, LRM) lets the norm be learned, and lets the forward multipliers
that µP would otherwise fix be learned too.

Evidence: two 200 GT runs (50 GT of decay), Muon alone against Muon with
LRMs, on the final 90M architecture. Improvements on most benchmarks, up to a
20% relative gain on MMLU, BBH and GSM8K. The authors then used LRMs for
every model in the series.

Why *Proposed* and not *Active*: one team, one architecture family, and the
larger-scale results live in the preprint rather than in this source.

The condition as first written — "an independent reproduction **or** a result
above 1B" — has since been half-met in a way that shows the *or* was doing
too much work. [LIT-153](../literature.d/LIT-153.md) is an independent group, at up to 1.2B, working on
exactly the phenomenon this practice rests on: the weight-decay equilibrium
that fixes a matrix's norm by hyperparameters rather than data. They confirm
the diagnosis and go further, arguing that equilibrium is *why* matrix
optimizers' advantage shrinks with scale.

But their remedy is the opposite of this one. Learnable multipliers give the
scale its own learned parameter; Hyperball pins the Frobenius norms to
constants and removes the degree of freedom. So an independent group above 1B
has confirmed the *mechanism* and declined the *fix*, which the original
condition would read as a promotion and which plainly is not one.

Promote when an independent group reports gains from **learned per-row and
per-column multipliers specifically** — not from another intervention on the
same equilibrium.

## Known implementations

- Falcon-H1-Tiny (all released checkpoints)
