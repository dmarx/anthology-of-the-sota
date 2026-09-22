---
number: 298
status: Read
formerly:
- NOTE-tmp0rqt2
paper: LIT-554
title: 'Diffusion Forcing'
version: 1
date: '2026-09-23'
summary: >-
  Independent per-token noise levels during training give one causal model
  both autoregressive sampling and horizon-wide guidance, with sampling
  schedules chosen at inference. Stable long video rollouts are shown
  qualitatively. Planning and robot results are measured. Read §1–5; the
  appendix proofs and time-series results were not read.
---

<!-- inactive-ok-file: SOTA-333 — Proposed, filed in this same contribution from this paper -->

# NOTE-298: Diffusion Forcing

## Contribution

A training objective, independent noise per token over a causal model, that
turns the choice between next-token prediction and full-sequence diffusion
into a choice made at sampling time. Also sampling schemes that use this,
including zig-zag schedules and Monte Carlo Guidance.

## Key insight

**Noise level is a continuous mask.** Teacher forcing trains "clean past,
predict next". Full-sequence diffusion trains "equally noisy everything".
Training on random per-token noise covers both and everything in between,
so the sampler can hold the past slightly noisy (for robustness), keep the
future noisier than the present (for causal uncertainty), or guide the
whole horizon.

## Assumptions

- **A causal architecture** with a latent state. The implementation is a
  convolutional RNN
- **Standard DDPM hyperparameters**
- **Small, continuous-token domains:** 2D mazes, Minecraft and DMLab video,
  one robot task, time series

## Key results

- **Video (Figure 3):** stable to 1,000 frames where baselines with the same
  RNN diverge. Qualitative only
- **Maze2D (Table 1):** single-task average 141.7 against Diffuser 119.5
  (with a PD controller) and 8.7 (without). 129.7 without MCG
- **Robot:** 80% success, 76% under occlusion, against 48% for a next-frame
  diffusion baseline

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | The objective lower-bounds the likelihood of all training subsequences | strong | proof (appendix, not read) |
| C2 | Conditioning on slightly noised history stabilizes long autoregressive rollouts of continuous tokens | weak | qualitative video only |
| C3 | Per-token noise enables better guided planning than full-sequence diffusion | moderate | D4RL mazes, with ablation of MCG |
| C4 | The generated actions are causally consistent with the generated states | moderate | Diffuser collapses when executing its own actions and DF does not |

## Concepts

- **Teacher forcing** — training on the ground-truth history
- **Zig-zag schedule** — denoise the near future ahead of the far future
- **Monte Carlo Guidance** — average guidance gradients over several
  sampled futures

## Connections

It unifies next-token prediction and full-sequence diffusion (video
diffusion, Diffuser for planning, diffusion policy for control). SIREN
([LIT-551](../literature.d/LIT-551.md)) shares an author, Sitzmann, but no method.

## Recommendations

- **R1** — For autoregressive generation of continuous tokens, train with
  per-token noise and condition on slightly noised history. Filed as
  [SOTA-333](../practices.d/SOTA-333.md)

## Bearing on the record

- **[SOTA-333](../practices.d/SOTA-333.md)** is new

## Limitations

- **The headline video result is unquantified**
- **RNN only**, small scale. Transformer and scaling are named as future
  work
- **Few tasks** in each domain

## Open questions

- How much of the rollout stability survives in large transformer video
  models, and how it compares with other anti-drift methods
