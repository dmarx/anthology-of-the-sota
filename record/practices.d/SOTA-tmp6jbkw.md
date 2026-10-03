---
status: Proposed
promote_when: >-
  A second group RL-tunes a flow-matching image or video model through a
  same-marginal SDE with the per-step KL anchor, and checks quality with
  something other than reward models: human preference, or FID or a
  diversity measure on held-out prompts. It must report the run without the
  KL term as well. The source judged reward hacking only with other reward
  models, and the one task where reward and evaluation overlapped is where
  its KL ablation is weakest. Another method that reports a higher GenEval
  after training on GenEval's own templates does not count.
consensus: unreplicated
consensus_note: >-
  One group, one paper (LIT-tmpdktqx, CUHK, Tsinghua and Kuaishou), one
  base model for most results (SD3.5-Medium with LoRA) and one run per
  setting. Its pieces are not new: GRPO's group baseline is converged in
  language (SOTA-145), and the same-marginal SDE family is the
  stochastic-interpolant identity (SOTA-265). What is unreplicated is the
  combination on a flow model and the KL ablation that shows the anchor is
  needed. The record holds none of the RL-for-diffusion papers it builds
  on. Read as of 2026-10.
title: 'To RL-tune a flow-matching generator, roll it out as a same-marginal SDE built from its own velocity, and anchor each step with the closed-form KL to the reference'
version: 1
tags:
- adaptation-and-tuning
- generative-modeling
- flows-and-transport
date: '2026-10-03'
source:
- LIT-tmpdktqx
# Flow-GRPO cites concurrent GRPO on a flow-matching speech model (F5R-TTS)
# and earlier online reward-weighted fine-tuning of flow matching (ORW), and
# DDPO before it ran policy gradients on a diffusion model's stochastic
# sampler. None is held. Among held work, Flow-GRPO is the first to state
# the ODE-to-SDE conversion as the way to make a flow model an RL policy.
introduced_by:
- LIT-tmpdktqx
implementations:
- 'Flow-GRPO'
summary: >-
  Liu et al. (2025), [LIT-tmpdktqx](../literature.d/LIT-tmpdktqx.md). A flow model's ODE sampler is not a
  stochastic policy. Swapping it for an SDE with the same marginals, built
  from the trained velocity alone, makes each step an isotropic Gaussian, so
  GRPO's ratio and the KL to the reference model are both closed form. On
  SD3.5-M, GenEval goes 0.63 → 0.95 either way. Without the KL term,
  DrawBench aesthetic falls to 4.93 from a base of 5.39, against 5.25 with
  it (Table 2). Quality is judged by reward models only, one run each.
explained_by:
- THEORY-tmpr00tj
---

<!-- inactive-ok-file: SOTA-302 — Proposed; named as the opposite case, a distilled generator where this anchor is intractable, not cited as settled advice -->

# SOTA-tmp6jbkw: To RL-tune a flow-matching generator, roll it out as a same-marginal SDE built from its own velocity, and anchor each step with the closed-form KL to the reference

## Source

Liu, Liu, Liang, Li, Liu, Wang, Wan, Zhang and Ouyang (2025), [LIT-tmpdktqx](../literature.d/LIT-tmpdktqx.md) —
Flow-GRPO, §4, Table 2, Figs. 5–7 and App. A.

## What to do

A flow-matching model samples by integrating an ODE. The ODE is
deterministic given the starting noise, so it is not a policy that online
RL can explore with, and its likelihood ratio needs divergence estimates.
To RL-tune it:

1. **Sample rollouts from an SDE with the same marginals.** For the linear
   path the score is a function of the trained velocity,
   ∇log p_t(x) = −x/t − ((1 − t)/t)·v(x). The reverse SDE
   dx = [v − (σ_t²/2)∇log p_t] dt + σ_t dw therefore needs only v_θ and
   has the ODE's marginals for any σ_t. No retraining is needed. Flow-GRPO
   uses σ_t = a·√(t/(1 − t)) with a = 0.7.
2. **Treat each Euler–Maruyama step as a Gaussian policy.** The policy
   ratio is then a ratio of Gaussian densities.
3. **Anchor every step with the KL to the frozen reference model.** Between
   two isotropic Gaussians with the same σ_t it is closed form: a weighted
   squared difference of the two velocities at that step.
4. **Roll out with fewer steps than you evaluate with.** Flow-GRPO collects
   training samples with 10 steps and evaluates with the usual 40-step ODE.

The update itself is GRPO's ([LIT-127](../literature.d/LIT-127.md)), unchanged: a group-relative
advantage, a clipped ratio and a KL to a reference. That part is [SOTA-145](SOTA-145.md), and Flow-GRPO is that practice's first
evidence outside language.

## Evidence

All of it is from [LIT-tmpdktqx](../literature.d/LIT-tmpdktqx.md), on SD3.5-Medium at 512 px with LoRA rank 32,
group size 24 and KL weight β = 0.04 (0.01 for PickScore).

- **The method works on three rewards** (Tables 1–2). GenEval 0.63 → 0.95,
  visual text accuracy 0.59 → 0.92, PickScore 21.72 → 23.31. On FLUX.1-Dev
  with PickScore, 22.62 → 23.97 (App. C.4).
- **The KL anchor is what keeps quality** (Table 2, DrawBench). On GenEval
  training, aesthetic / DeQA / ImageReward are 4.93 / 2.77 / 0.44 without
  the KL term and 5.25 / 4.01 / 1.03 with it, from a base of
  5.39 / 4.07 / 0.87, at the same GenEval 0.95. On OCR training, without
  KL they are 5.13 / 3.66 / 0.58 and with it 5.32 / 4.06 / 0.95, at OCR
  0.93 and 0.92. On PickScore training the quality scores do not fall
  without KL (aesthetic 6.15 against 5.92 with it), but outputs collapse to
  one style, "different seeds producing nearly identical results" (§5.3,
  Fig. 6). The KL run reaches the same reward later (Fig. 12).
- **Short rollouts are enough** (Fig. 7a). Collecting with 10 steps instead
  of 40 gives "over a 4× speedup across all three tasks, without impacting
  final reward". Five steps does not consistently help. That ablation ran
  without the KL term.
- **The noise level is a real knob** (Fig. 7b). On OCR, a = 0.1 learns
  slowly, 0.7 and 1.0 learn equally fast, and too much noise drives images
  to zero reward.
- **The group must be large enough** (Fig. 5). G = 12 and G = 6 collapsed on
  PickScore, and G = 24 did not.
- Against other update rules on the same model and reward, it beats SFT on
  the best sample, reward-weighted regression and DPO, offline and online,
  on GenEval (Fig. 4). On PickScore, DDPO run through the same SDE
  "eventually collapses" (Fig. 8).

## Conditions

- **Quality is judged by reward models.** There is no human evaluation and
  no FID. Reward hacking is measured with other reward models on DrawBench,
  and on the PickScore task the reward and one evaluation metric are the same
  model. The paper says that overlap may be why quality looks intact without
  KL there.
- **GenEval 0.95 is in-distribution.** Training prompts come from GenEval's
  own templates and the reward is its detector. Out-of-template, on
  T2I-CompBench++, 2D-spatial rises 0.2850 → 0.5447 and texture falls
  0.7338 → 0.7236 (Table 3).
- **Training samples are not the evaluated samples.** The policy optimized
  is the 10-step SDE. The images reported use a 40-step ODE. That is sound
  only because the two share marginals, and at 10 steps they visibly do not:
  the training samples show colour drift and blur (Fig. 19).
- **The σ_t schedule is singular where sampling starts**, at t = 1. The
  paper does not say how the first step is taken.
- **Not for distilled generators.** The KL is closed form because each step
  of a multi-step stochastic sampler is Gaussian. A one- or few-step
  distilled generator has no such steps, and [SOTA-302](SOTA-302.md) shows weight-space
  reward tuning there degrading the model. For those, [SOTA-302](SOTA-302.md) steers the
  input noise instead. The two practices split the case by whether the
  generator samples in many stochastic steps.
- **Expensive.** GenEval training to 0.95 takes several thousand GPU hours
  (Fig. 7a), on 24 A800s.

## Beside the record's other practices

[SOTA-265](SOTA-265.md) says the stochastic sampler's diffusion coefficient is free after
training, because one velocity gives a whole family of same-marginal SDEs.
This practice uses that freedom for a different end: σ_t is set for
exploration, by how fast reward rises, and the SDE is used only during
training. Flow-GRPO measures nothing about what the coefficient does to
sample quality.

## Known implementations

- Flow-GRPO, the source's code.
