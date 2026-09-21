---
status: Proposed
promote_when: >-
  A second group aligning a generator to a reward through its input rather
  than its weights, reporting the **direct fine-tuning baseline on the same
  model and reward** — that control is what makes this a recommendation
  rather than one more alignment method, and it is the half most likely to be
  dropped. A non-distilled or non-image setting would be worth more than
  another text-to-image result. What would not move it: a paper reporting
  better reward-model scores from some alignment scheme, which is a crowded
  field and does not speak to where the adaptation belongs.
consensus: unreplicated
consensus_note: >-
  One group, one paper, one modality. The pieces are all standard — LoRA,
  reward ensembles, tilted distributions — so adoption of any of them is not
  evidence for this. What is unreplicated is the comparison: that weight-space
  reward adaptation of a distilled generator degrades it while input-space
  adaptation improves it, on the same model, reward and budget.
title: 'Steer a distilled generator by modulating its input noise, not by fine-tuning its weights'
version: 1
tags:
- generative-modeling
- adaptation-and-tuning
- inference-optimization
date: '2026-09-21'
source:
- LIT-tmpksq2o
introduced_by:
- LIT-tmpksq2o
implementations: []
explained_by:
- THEORY-tmpq2xg2
summary: >-
  Eyring et al. (2025), [LIT-tmpksq2o](../literature.d/LIT-tmpksq2o.md) — train a LoRA hypernetwork to
  predict an improved initial noise for a frozen step-distilled generator.
  GenEval on SANA-Sprint goes **0.70 → 0.75** for **0.1 s** of added latency,
  recovering about half of what 30-second test-time optimization buys. Reward
  fine-tuning the same model instead takes it **0.73 → 0.62**: the anchoring
  KL term is intractable in weight space and tractable in noise space.
---

<!-- inactive-ok-file: SOTA-301 — Proposed, and named as the opposite side of
     the same decision, with its cost profile quoted rather than its authority
     borrowed -->

<!-- inactive-ok-file: THEORY-tmpq2xg2 — Proposed, filed in this same
     contribution, and the sentence citing it says it is why the penalty is
     the right one rather than merely convenient; the practice rests on the
     measured fine-tuning failure, not on the proof -->

# SOTA-tmplndwz: Steer a distilled generator by modulating its input noise, not by fine-tuning its weights

## Source

Eyring, Karthik, Dosovitskiy, Ruiz and Akata (2025), [LIT-tmpksq2o](../literature.d/LIT-tmpksq2o.md) —
[ARXIV-2508.09968](https://arxiv.org/abs/2508.09968) — read as [NOTE-tmptc2jq](../notes.d/NOTE-tmptc2jq.md).

## What to do

Freeze the distilled generator. Train a lightweight network — LoRA over the
generator's own architecture, so it inherits the inductive biases and the
conditioning pathways — to map standard Gaussian noise to a modulated noise,
as a residual `ε ↦ ε + Δ(ε)`.

**Initialize `Δ` to output exactly zero.** Zero the second LoRA matrix and
have the final layer emit only the adapter's perturbation. This makes the
modulation start as the identity, which stabilizes training and keeps the
Lipschitz condition the objective's approximation depends on.

Train by maximizing the reward minus `½‖Δ(ε)‖²`. That penalty is the whole
anchoring mechanism, and [THEORY-tmpq2xg2](../theory.d/THEORY-tmpq2xg2.md) is why it is the right one
rather than a convenient one.

Training needs **no data samples** — only base noise, the frozen generator,
the reward, and the conditions.

## Why not just fine-tune the model

Because it makes things worse, measurably, and the paper ran the control.

Aligning to a reward means learning a tilted distribution: upweight high
reward, **stay near the base model**. Without that second term the result
reward-hacks — high scores, off-manifold images. For a step-distilled
generator, the KL that enforces it needs a Jacobian determinant through the
network and is intractable, so weight-space fine-tuning is optimizing the
reward with a broken anchor.

On SANA-Sprint, direct LoRA reward fine-tuning against the same reward
ensemble scores **0.67 / 0.66 / 0.62** on GenEval at one, two and four
sampling steps — against an untouched baseline of **0.70 / 0.72 / 0.73**. It
is worse than doing nothing, monotonically worse the more steps you sample,
and worse still at lower adapter rank (0.59 at rank 8). Noise modulation on
the same model, reward and budget gives **0.75 / 0.76 / 0.77**.

## What it buys against paying at inference

| model | base | this | test-time optimization |
|---|---|---|---|
| SD-Turbo | 0.49 (0.2 s) | **0.57** (0.3 s) | 0.63 (20 s) |
| SANA-Sprint | 0.70 (0.2 s) | **0.75** (0.3 s) | 0.81 (30 s) |
| FLUX-schnell | 0.68 (0.7 s) | **0.72** (0.9 s) | 0.76 (40 s) |

About **half** the gain, at **33×–300×** lower inference cost — the authors'
own characterization and it matches the arithmetic. On SANA-Sprint it equals
LLM prompt optimization while being 300× faster. The tables count the
hypernetwork's forward pass as an extra NFE rather than hiding it.

This is the amortized side of a trade whose other side is [SOTA-301](SOTA-301.md):
steer the sampler at inference with a correctly-ordered gradient step, no
training, cost on every sample. Neither dominates. Pay once and get half, or
pay always and get all of it.

## Conditions

**Few-step generators only, and the decay is shown.** The gain shrinks as
sampling steps grow: at 8 NFEs 0.74 → 0.76, at 16 0.73 → 0.75, at 32
0.71 → 0.72. Past roughly eight steps there is little left to recover, which
is consistent with the initial noise having less leverage the longer the
trajectory.

**It recovers half, not all.** Where quality matters more than latency the
test-time method remains better and the paper says so.

**One modality, one task family, one group.** Text-to-image across three
distilled models. The noise-space argument is general in principle and
untested outside it.

**Reward-specific.** The hypernetwork learns one reward ensemble's tilt.
Whether it transfers to a different reward at inference is not examined, and
nothing here addresses the ordinary problem of the reward being a poor proxy
— this keeps you near the base distribution, not near the truth.

**The Lipschitz condition is engineered, not verified.** Zero initialization
makes it hold at the start; nothing measures that it holds later, and the
approximation's error bound degrades quadratically if it does not.
