---
number: 302
status: Proposed
formerly:
- SOTA-tmplndwz
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
version: 2
history:
- version: 2
  date: '2026-10-03'
  note: >-
    Conditions refined with Flow-GRPO (LIT-tmpdktqx), the opposite case: a
    multi-step flow sampled as an SDE has a closed-form per-step KL, and
    LoRA reward tuning with that anchor kept quality as judged by reward
    models. The weight-space failure is scoped to distilled generators. DDPO
    (LIT-tmp7vihu), with no anchor, and Diffusion-DPO (LIT-tmp4m2nj), with
    an offline one, are added as the multi-step cases either side. DPOK
    (LIT-tmp9ntgf), with a summed per-step KL, is a third multi-step case,
    and Lee et al. (LIT-tmpznned) and ReFL (LIT-tmppb4sm), anchored by
    pre-training data, are two where selection at inference beat
    fine-tuning under the same reward. Gao et al. (LIT-tmpylcrx) are cited
    for the general case: true reward falls with distance from the base,
    and an explicit KL penalty acted like early stopping. Not a test of
    this practice; promote_when is not met and status is unchanged.
tags:
- generative-modeling
- adaptation-and-tuning
- inference-optimization
date: '2026-09-21'
source:
- LIT-491
introduced_by:
- LIT-491
implementations: []
explained_by:
- THEORY-054
summary: >-
  Eyring et al. (2025), [LIT-491](../literature.d/LIT-491.md) — train a LoRA hypernetwork to
  predict an improved initial noise for a frozen step-distilled generator.
  GenEval on SANA-Sprint goes **0.70 → 0.75** for **0.1 s** of added latency,
  recovering about half of what 30-second test-time optimization buys. Reward
  fine-tuning the same model instead takes it **0.73 → 0.62**: the anchoring
  KL term is intractable in weight space and tractable in noise space.
---

<!-- inactive-ok-file: SOTA-301 — Proposed, and named as the opposite side of
     the same decision, with its cost profile quoted rather than its authority
     borrowed -->

<!-- inactive-ok-file: THEORY-054 — Proposed, filed in this same
     contribution, and the sentence citing it says it is why the penalty is
     the right one rather than merely convenient; the practice rests on the
     measured fine-tuning failure, not on the proof -->

# SOTA-302: Steer a distilled generator by modulating its input noise, not by fine-tuning its weights

## Source

Eyring, Karthik, Dosovitskiy, Ruiz and Akata (2025), [LIT-491](../literature.d/LIT-491.md) —
[ARXIV-2508.09968](https://arxiv.org/abs/2508.09968) — read as [NOTE-240](../notes.d/NOTE-240.md).

## What to do

This is [LIT-491](../literature.d/LIT-491.md)'s noise hypernetwork (HyperNoise), and the recommendation
starts there: on SD-Turbo, SANA-Sprint and FLUX-schnell it raises GenEval by
0.04–0.08 for about 0.1–0.2 s more per sample, while direct LoRA reward
fine-tuning of the same SANA-Sprint model fell below the untouched base.

Freeze the distilled generator. Train a lightweight network — LoRA over the
generator's own architecture, so it inherits the inductive biases and the
conditioning pathways — to map standard Gaussian noise to a modulated noise,
as a residual `ε ↦ ε + Δ(ε)`.

**Initialize `Δ` to output exactly zero.** Zero the second LoRA matrix and
have the final layer emit only the adapter's perturbation. This makes the
modulation start as the identity, which stabilizes training and keeps the
Lipschitz condition the objective's approximation depends on.

Train by maximizing the reward minus `½‖Δ(ε)‖²`. That penalty is the whole
anchoring mechanism, and [THEORY-054](../theory.d/THEORY-054.md) is why it is the right one
rather than a convenient one.

Training needs **no data samples** — only base noise, the frozen generator,
the reward, and the conditions.

## Why not just fine-tune the model

Because it makes things worse, measurably, and the paper ran the control.

Aligning to a reward means learning a tilted distribution: upweight high
reward, **stay near the base model**. Without that second term the result
reward-hacks — high scores, off-manifold images. Gao et al. ([LIT-tmpylcrx](../literature.d/LIT-tmpylcrx.md))
measured the general version in language-model RLHF: true reward rises then
falls with KL from the starting policy, a larger reward model moves the turn
later, and an explicit KL penalty did not change the gold reward reached at a
given distance; it stopped the policy earlier. What protects is staying near
the base, by whatever means. That fits the argument here, and it means the
LoRA control should be read with its stopping point in mind, which the
source note does not give. For a step-distilled
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

**The weight-space failure is a property of distilled generators.**
Flow-GRPO ([LIT-tmpdktqx](../literature.d/LIT-tmpdktqx.md)) is the opposite case, and it sharpens this
condition rather than contesting it. For a multi-step flow sampled as an
SDE, each step is a Gaussian, so the KL to the reference model is closed
form per step. LoRA reward tuning with that anchor held quality on the
other reward models it was checked against: DrawBench aesthetic 5.25 with
the KL against 4.93 without, from a base of 5.39, on GenEval training.
That is judged by reward models only, with no human evaluation, and nothing
there tests a distilled model. So the argument here — the anchor is
intractable in weight space — applies to step-distilled generators and does
not extend to multi-step stochastic samplers.

DDPO ([LIT-tmp7vihu](../literature.d/LIT-tmp7vihu.md)) shows what happens when the tractable anchor is not
used: it has no KL term, over-optimizes (an incompressibility model decays
to noise, and a model learns to write text that fools its LLaVA judge), and
its checkpoints are picked by hand before quality deteriorates (its App. A).
Diffusion-DPO ([LIT-tmp4m2nj](../literature.d/LIT-tmp4m2nj.md)) anchors offline instead, through β in a
preference loss against the frozen reference. Neither tests a distilled
model.

DPOK ([LIT-tmp9ntgf](../literature.d/LIT-tmp9ntgf.md)) is a third multi-step case, the closest to Flow-GRPO. It
LoRA-tunes Stable Diffusion v1.5 on ImageReward, anchored by the sum of
per-step Gaussian KLs, which by the data processing inequality bounds the KL
on the final image (its Lemma 4.2). On one prompt the run without the KL
oversaturated and the run with it kept the held-out aesthetic score (its
§5.3), on one aesthetic predictor and 50 samples. Two earlier papers anchor
with pre-training data instead, and both trail selection at inference
under the same reward, on fidelity or overall. Lee et al. ([LIT-tmpznned](../literature.d/LIT-tmpznned.md)) beat best-of-16 on
alignment 20% to 10% and lose on fidelity 3% to 20%. ReFL ([LIT-tmppb4sm](../literature.d/LIT-tmppb4sm.md))
wins 58.38% against the base where best-of-64 wins 73.33%. That is this
practice's amortized-against-per-sample trade, measured on multi-step
models. None of the three tests a distilled generator.

**The Lipschitz condition is engineered, not verified.** Zero initialization
makes it hold at the start; nothing measures that it holds later, and the
approximation's error bound degrades quadratically if it does not.
