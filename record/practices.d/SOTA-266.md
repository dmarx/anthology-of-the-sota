---
number: 266
status: Active
formerly:
- SOTA-tmpwzlqh
consensus: emerging
consensus_note: >-
  Converged for the straight path, emerging for the logit-normal. The path
  is now the default objective of the video line: Movie Gen, HunyuanVideo,
  Step-Video and Wan all train with it (LIT-626, LIT-620, LIT-624, LIT-619).
  That is adoption, per DP-005. The logit-normal half has one controlled
  source, SD3. Among the video reports, Movie Gen, HunyuanVideo, Open-Sora
  2.0 and Wan state that they use it, and LTX-Video cites SD3's distribution.
  Movie Gen's Table 8a changes the path and the timestep distribution
  together, so it supports the combination and cannot separate the halves.
  `emerging` stands because the practice is both halves together. Read as of 2026-09.
title: 'Connect data and noise on a straight line, and sample the training timesteps from a logit-normal rather than uniformly'
version: 4
history:
- version: 2
  date: '2026-09-24'
  note: >-
    The originating papers were filed (LIT-630, LIT-636), and
    Movie Gen's 5B video ablation was added as evidence. `introduced_by`
    named SiT, which is 2024. The straight path is from 2022. The claim
    that uniform-timestep rectified flow "does not win" is scoped to SD3's
    setting. Both originating papers win with uniform timesteps in
    controlled pixel-space comparisons, and the earlier "equivocal for two
    years" gloss had no source. The conditions no longer say "all of it is
    image synthesis".
- version: 3
  date: '2026-09-24'
  note: >-
    Corrected against full readings of Flow Matching (NOTE-340),
    Rectified Flow (NOTE-337) and Movie Gen (NOTE-334). The
    logit-normal is stated by four video reports, not only Wan. Rectified
    Flow's Table 1a is partly controlled, since its training budget is
    unstated. Flow Matching's path comparison replicates at ImageNet-32 and
    64 inside the same paper.
- version: 4
  date: '2026-09-24'
  note: >-
    Source corrected: stochastic interpolants are no longer named as a third
    origin of the straight path. ARXIV-2209.15571 uses a trigonometric
    interpolant and credits the linear path to Liu et al.; it is now filed and
    cited for what it did originate, the simulation-free interpolant objective.
    The recommendation is unchanged.
tags:
- generative-modeling
date: '2026-09-20'
source:
- LIT-449
- LIT-447
- LIT-630
- LIT-626
introduced_by:
- LIT-636
- LIT-630
implementations:
- 'Stable Diffusion 3'
- 'SiT-XL'
- 'Movie Gen'
- 'HunyuanVideo'
- 'Step-Video-T2V'
- 'Wan2.1'
summary: >-
  Esser et al. (2024), [LIT-449](../literature.d/LIT-449.md), and Ma et al. (2024),
  [LIT-447](../literature.d/LIT-447.md) — the straight-line path between data and noise beats the
  curved variance-preserving one at fixed architecture and compute, and the
  advantage is largest at few sampling steps. Movie Gen (LIT-626) confirms
  it for video at 5B. In SD3's latent text-to-image sweep, the timestep
  distribution decides the ranking: uniform does not beat tuned
  ε-prediction and logit-normal does.
---

# SOTA-266: Connect data and noise on a straight line, and sample the training timesteps from a logit-normal rather than uniformly
<!-- inactive-ok-file: SOTA-157 — Proposed, and named to mark the boundary: this practice is about image synthesis and does not carry to discrete-token diffusion -->
<!-- inactive-ok-file: SOTA-254 — Proposed, and named in the same sentence and for the same reason -->

## Source

Liu, Gong and Liu (2022), [LIT-636](../literature.d/LIT-636.md), and Lipman et al. (2022),
[LIT-630](../literature.d/LIT-630.md), introduced the straight path concurrently. Albergo and Vanden-Eijnden's
stochastic interpolants ([LIT-tmp90ynr](../literature.d/LIT-tmp90ynr.md)) are a concurrent origin of the
simulation-free objective but not of the straight path: they use a
trigonometric interpolant and credit the linear one to Liu et al. Flow Matching contributes the
first controlled comparison: the same U-Net, hyperparameters and epochs
give CIFAR-10 FID 6.35 on the straight path against 8.06 on the diffusion
path (its Table 1). The same comparison holds at ImageNet-32 and
ImageNet-64 in the same table. It trained with uniform timesteps.

Ma et al. (2024), [LIT-447](../literature.d/LIT-447.md) — [ARXIV-2401.08740](https://arxiv.org/abs/2401.08740).

Esser et al. (2024), [LIT-449](../literature.d/LIT-449.md) — [ARXIV-2403.03206](https://arxiv.org/abs/2403.03206).

Both are load-bearing and they do different jobs. SiT is the controlled
attribution: DiT's architecture, parameter count and GFLOPs held exactly
fixed while the interpolant is changed and nothing else. SD3 is the scale and
the breadth: 61 formulations ranked, then the winner taken to 8B
text-to-image with weights released. A practice on either alone would be
weaker — one would be a small-scale ablation, the other a leaderboard entry.

The Movie Gen team (2024), [LIT-626](../literature.d/LIT-626.md), is the video evidence. At 5B, on video
at 352×192, it compares flow matching against v-prediction diffusion with
zero terminal SNR, with everything else held constant. Flow matching wins
by a net +16.5 on human-rated quality and +7.1 on text alignment (its Table
8a). That is the only controlled comparison of the objective in the video
line. Every other video report adopts it.

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
timesteps does.** That is a finding about SD3's setting: latent
text-to-image, against a tuned ε-prediction baseline. It is not a finding
that uniform timesteps fail in general. The originating papers used uniform
sampling and beat VP diffusion in pixel space. Flow Matching's comparison
is controlled ([LIT-630](../literature.d/LIT-630.md) Table 1). Rectified Flow's is partly controlled,
because its training budget is unstated ([LIT-636](../literature.d/LIT-636.md) Table 1a). At SD3's scale the
logit-normal decides the ranking. At small scale the path alone was enough.
A reader training a large latent model should take both halves.

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
well established and the *why* is open. The closest anyone has come is a
2-D toy in Rectified Flow ([LIT-636](../literature.d/LIT-636.md) Fig. 5), which runs VP with a linear
α_t to separate path speed from curvature. It is qualitative. Rectified
Flow's straightness theorems apply to the reflowed coupling, not the
single-pass model this practice recommends.

The 61-way sweep is at a smaller scale than the 8B run, which applies its
winner rather than repeating it. SD3's own scaling argument says that should
be fine, and *should be fine* is what is established.

The image evidence is class-conditional ImageNet for the ablation and
latent text-to-image for the scale run. The video evidence is one 5B
ablation ([LIT-626](../literature.d/LIT-626.md)), judged by humans on 381 prompts. Its alignment margin
is under twice the annotation σ that Movie Gen reports elsewhere. Nothing
here is about the diffusion *language* models the record also holds ([SOTA-157](SOTA-157.md), [SOTA-254](SOTA-254.md)), where the
data is discrete and the straight-line construction does not obviously
transfer.

The logit-normal's parameters are tuned, as EDM's log-normal is. `(0.00,
1.00)` is what SD3 reports for the variant that stays competitive at higher
step counts, and it is a fit rather than a derivation.

## Known implementations

- Stable Diffusion 3 (8B, weights released)
- SiT-XL
- Movie Gen, HunyuanVideo, Step-Video-T2V, Wan2.1 (video)
