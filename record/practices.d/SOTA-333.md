---
number: 333
status: Proposed
formerly:
- SOTA-tmpbc2oe
promote_when: >-
  A quantitative long-rollout comparison (FVD or a per-frame quality metric
  against rollout length) at transformer scale, between per-token-noise
  training with noised-history conditioning and teacher-forced next-frame
  diffusion under the same architecture and data, run by a group other than
  the authors. The source shows it on a small RNN with videos only. A system
  that adopts the recipe without reporting the ablation does not count.
title: 'For autoregressive generation of continuous sequences, train with an independent noise level per token and condition the rollout on slightly noised history'
version: 2
history:
- version: 2
  date: '2026-09-24'
  note: >-
    Self Forcing (LIT-629) and CausVid (LIT-631) were filed.
    Consensus moves from `unassessed` to `contested`. Self Forcing argues
    against the rollout half in writing and does not test it. Its controlled
    transformer-scale comparison of the training half is split: diffusion
    forcing loses to teacher forcing in the many-step rows and wins after
    distillation. Status and `promote_when` are unchanged, because neither
    paper measures quality against rollout length with noised history.
tags:
- generative-modeling
- vision-and-graphics
date: '2026-09-23'
source:
- LIT-554
introduced_by:
- LIT-554
consensus: contested
contested_by:
- LIT-629
consensus_note: >-
  CausVid (LIT-631) adopts per-chunk independent noise when training its
  causal student. Self Forcing (LIT-629) argues that noising the context
  at inference "sacrifices temporal consistency" and "does not fundamentally
  resolve the exposure bias problem", with no experiment. It proposes
  training on the model's own rollouts instead. Credible groups disagree in
  writing, and nobody has run the comparison. Read as of 2026-09.
implementations: []
summary: >-
  Chen et al. (2024), [LIT-554](../literature.d/LIT-554.md) — train a causal model to denoise tokens
  that each carry an independent noise level. At rollout, treat the
  generated history as slightly noisy, so accumulated errors look like
  training noise. The same model then samples autoregressively, plans with
  horizon-wide guidance, and keeps near-future tokens cleaner than far ones.
  Long-rollout stability is shown on video qualitatively, with a small RNN.
  Planning and robot gains are measured.
---

# SOTA-333: For autoregressive generation of continuous sequences, train with an independent noise level per token and condition the rollout on slightly noised history

## Source

Chen et al. (2024), [LIT-554](../literature.d/LIT-554.md) — Diffusion Forcing. Read as [NOTE-298](../notes.d/NOTE-298.md).

## The practice

When a model generates **continuous tokens one step at a time** (video
frames, trajectories, actions) and must run past the length it was trained
on:

- **Train with an independent noise level for every token** in the
  sequence, with a causal model and an ordinary denoising loss. This covers
  clean-history next-token prediction and equal-noise full-sequence
  diffusion as special cases
- **At rollout, mark the generated history as slightly noisy**
  (`0 < k ≪ K`) and do not treat it as clean ground truth. The model has
  seen noisy history in training, so its own small errors do not push it out
  of distribution
- **Choose the schedule at inference.** Keep the near future cleaner than
  the far future when planning, so uncertainty grows with the horizon, and
  guide over the whole horizon if there is a reward

## What was measured

- Minecraft and DMLab video: coherent to 1,000 frames, where teacher-forced
  and causal full-sequence baselines on the same RNN diverge. **Figure 3
  only, no metric**
- D4RL Maze2D: average reward 141.7 against Diffuser's 119.5, which needs a
  hand-coded controller and gets 8.7 executing its own actions
- A real robot task needing memory: 80% success. 76% with occluded
  observations, marked as noisy, against 48% for a next-frame baseline

## What has been measured since

Self Forcing ([LIT-629](../literature.d/LIT-629.md), Table 2) ran the first controlled comparison at
transformer scale by a group other than the authors: Wan2.1-1.3B, same
initialization and prompts, 5s clips, scored by VBench total. It bears on
the two halves differently.

- **Training half, per-token noise against teacher forcing: split.** In the
  many-step rows diffusion forcing loses (82.95 against 83.58 chunk-wise,
  77.24 against 80.34 frame-wise). After DMD distillation it wins (82.76
  against 82.32, 80.56 against 78.12). Both lose to training on the model's
  own rollouts (84.31, 84.26).
- **Rollout half, noised history: not tested.** The diffusion-forcing
  baselines appear to roll out on clean context. That is not stated, but
  the only inference procedure the paper gives caches clean outputs.

Neither result meets `promote_when`. It asks for quality against rollout
length with this practice's full recipe, and Table 2 measures neither.

## Conditions

- **A small convolutional RNN.** The authors name transformers and scale as
  future work
- **The anti-drift claim is qualitative** in the source
- **Continuous tokens.** For discrete tokens, teacher forcing does not
  diverge in the same way, and this is not a recommendation for language
  models
