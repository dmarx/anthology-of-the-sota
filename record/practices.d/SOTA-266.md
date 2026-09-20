---
number: 266
status: Active
formerly:
- SOTA-tmpwzlqh
consensus: emerging
consensus_note: >-
  Two groups, one controlled ablation and one 61-way sweep carried to 8B with
  weights released, and a production model shipped on it. Nothing in this
  record contests it. `emerging` rather than `converged` because the
  comparison at 8B is one run applying the smaller sweep's winner, and
  because no mechanism has been isolated.
title: 'Connect data and noise on a straight line, and sample the training timesteps from a logit-normal rather than uniformly'
version: 1
tags:
- generative-modeling
date: '2026-09-20'
source:
- LIT-449
- LIT-447
introduced_by:
- LIT-447
implementations:
- 'Stable Diffusion 3'
- 'SiT-XL'
summary: >-
  Esser et al. (2024), [LIT-449](../literature.d/LIT-449.md), and Ma et al. (2024),
  [LIT-447](../literature.d/LIT-447.md) — the straight-line path between data and noise beats the
  curved variance-preserving one at fixed architecture and compute, and the
  advantage is largest at few sampling steps. The timestep distribution is
  not a detail: rectified flow with uniform timesteps does not win, and with
  a logit-normal it does.
---

# SOTA-266: Connect data and noise on a straight line, and sample the training timesteps from a logit-normal rather than uniformly
<!-- inactive-ok-file: SOTA-157 — Proposed, and named to mark the boundary: this practice is about image synthesis and does not carry to discrete-token diffusion -->
<!-- inactive-ok-file: SOTA-254 — Proposed, and named in the same sentence and for the same reason -->

## Source

Ma et al. (2024), [LIT-447](../literature.d/LIT-447.md) — [ARXIV-2401.08740](https://arxiv.org/abs/2401.08740).

Esser et al. (2024), [LIT-449](../literature.d/LIT-449.md) — [ARXIV-2403.03206](https://arxiv.org/abs/2403.03206).

Both are load-bearing and they do different jobs. SiT is the controlled
attribution: DiT's architecture, parameter count and GFLOPs held exactly
fixed while the interpolant is changed and nothing else. SD3 is the scale and
the breadth: 61 formulations ranked, then the winner taken to 8B
text-to-image with weights released. A practice on either alone would be
weaker — one would be a small-scale ablation, the other a leaderboard entry.

## Both halves of the title are the practice

**The straight line.** Rectified flow connects data and noise along a
straight path rather than the curved one a variance-preserving diffusion
process traces. At fixed architecture and budget, switching the interpolant
from VP to linear or generalized-VP is one of the two changes carrying SiT's
improvement over DiT, and it removes a singularity the VP interpolant has at
one endpoint.

**The logit-normal.** This is the half that gets dropped in summary and
should not be. In SD3's ranking, **rectified flow with uniform timesteps does
not beat well-tuned epsilon-prediction; rectified flow with logit-normal
timesteps does.** The prior literature wrote rectified flow with uniform
sampling, which is why its advantage had looked equivocal for two years. A
reader who adopts the path and keeps uniform timesteps has adopted the
version that does not win.

## Where the advantage is largest

**At few sampling steps.** By 25 steps and above only the best-tuned
rectified-flow variant stays ahead of `eps/linear`; below that the gap is
wider. So the benefit lands where inference cost actually binds, which is a
better shape than a uniform improvement — it says when to bother.

## Relation to what the record already holds

The logit-normal over `t` is the rectified-flow expression of what
[SOTA-188](SOTA-188.md) records in EDM's coordinates: concentrate training where there is
something to learn, because the near-clean end is trivial and the
near-pure-noise end is nearly unlearnable. Two formulations, two coordinate
systems, one recommendation — and [SOTA-188](SOTA-188.md) had already listed Stable
Diffusion 3 as an implementation without the record holding the paper. The
listing was right, and now it has its reason.

[SOTA-195](SOTA-195.md) — predict `v` rather than the noise at low signal-to-noise — gets
independent support here too, from a different argument. That practice
reaches velocity prediction from the numerical failure of epsilon-prediction
near zero SNR; SiT reaches it from a clean ablation at fixed compute. Neither
knows about the other.

## Why `Active`

Two groups, a controlled ablation and a broad sweep, a released 8B model and
released weights, nothing in the record contesting it, and a production
system built on it. The evidence is better than most of what this record
files as `Active`.

## Conditions

**No mechanism has been isolated.** SiT offers reduced transport cost — the
path length falls — and that is an observation accompanying the result, not
an intervention separating it. An interpolant matched in path length but not
straight would tell them apart and nobody has run it. So the *whether* is
well established and the *why* is open.

The 61-way sweep is at a smaller scale than the 8B run, which applies its
winner rather than repeating it. SD3's own scaling argument says that should
be fine, and *should be fine* is what is established.

All of it is image synthesis — class-conditional ImageNet for the ablation,
latent text-to-image for the scale run. Nothing here is about the diffusion
*language* models the record also holds ([SOTA-157](SOTA-157.md), [SOTA-254](SOTA-254.md)), where the
data is discrete and the straight-line construction does not obviously
transfer.

The logit-normal's parameters are tuned, as EDM's log-normal is. `(0.00,
1.00)` is what SD3 reports for the variant that stays competitive at higher
step counts, and it is a fit rather than a derivation.

## Known implementations

- Stable Diffusion 3 (8B, weights released)
- SiT-XL
