---
status: Proposed
promote_when: >-
  A group other than DDPO's runs online reward fine-tuning (policy gradient,
  GRPO-style or reward-weighted regression, with several rounds of sampling
  from the current model) on a classifier-free-guided diffusion or flow
  model twice, once training the guided prediction at the sampling weight
  and once training the conditional prediction alone, everything else held,
  and reports the reward and a held-out quality metric across rounds for
  both arms. The arm that trains only the conditional prediction must be run
  to more than one round, since DDPO saw no difference after one. A paper
  that trains through the guided prediction without the other arm does not
  count; that is adoption.
consensus: unreplicated
consensus_note: >-
  One figure from one group (LIT-tmp7vihu, App. E.1, Fig. 10): one
  algorithm (RWR with sparse weights), one reward (JPEG compressibility),
  one run per arm on Stable Diffusion v1.4. DDPO itself is not run without
  it. Flow-GRPO (LIT-tmpdktqx), the line's flow-matching successor, says
  nothing about guidance during training in its text, and Diffusion-DPO
  (LIT-tmp4m2nj) is offline and does not face the question. Read as of
  2026-10.
title: 'When reward-tuning a classifier-free-guided diffusion model over several rounds of sampling, train the guided prediction at the fixed sampling guidance weight, not the conditional prediction alone'
version: 1
tags:
- adaptation-and-tuning
- generative-modeling
date: '2026-10-03'
source:
- LIT-tmp7vihu
introduced_by:
- LIT-tmp7vihu
implementations:
- 'DDPO'
summary: >-
  Black et al. (2023), [LIT-tmp7vihu](../literature.d/LIT-tmp7vihu.md), App. E.1 and Fig. 10. Reward
  fine-tuning should not train the unconditional branch, since the reward
  depends on the prompt. Training the conditional prediction alone made
  performance deteriorate after the first round of fine-tuning, which the
  authors attribute to the guidance weight becoming miscalibrated. Fixing
  the weight (5 in their runs) and training through the guided prediction
  used for sampling fixed it. One curve per arm, on reward-weighted
  regression and JPEG compressibility.
---

<!-- inactive-ok-file: SOTA-tmplmlbx — Proposed, filed in the same contribution; named as the offline counterpart from the same line of work, not as settled advice -->

# SOTA-tmprz581: When reward-tuning a classifier-free-guided diffusion model over several rounds of sampling, train the guided prediction at the fixed sampling guidance weight, not the conditional prediction alone

## Source

Black, Janner, Du, Kostrikov and Levine (2023), [LIT-tmp7vihu](../literature.d/LIT-tmp7vihu.md) — DDPO,
App. E.1, Fig. 10 and App. D.5.

## What to do

A text-to-image diffusion model is sampled with classifier-free guidance:
the step uses ε̃ = w·ε(x_t, t, c) + (1 − w)·ε(x_t, t), a mix of the
conditional and unconditional predictions. When fine-tuning such a model
on a reward, by policy gradient or reward-weighted regression, with several
rounds of sampling from the current model:

- Choose the guidance weight w you will sample with, and keep it fixed.
- Compute the likelihoods or losses through the guided prediction ε̃, the
  quantity that actually produces the samples, not through the conditional
  prediction ε(x_t, t, c) alone.
- Do not train the unconditional objective on its own. The reward depends
  on the prompt, so there is nothing for the unconditional branch to be
  rewarded for.

DDPO calls this "CFG training".

## Evidence

**The ablation** ([LIT-tmp7vihu](../literature.d/LIT-tmp7vihu.md), App. E.1, Fig. 10). On Stable Diffusion
v1.4 with JPEG compressibility as the reward, the paper runs its sparse
reward-weighted regression baseline (RWR_sparse) both ways. Training only
the conditional ε-prediction, the reward stops improving after the first
round and then falls back over the next ones, read from the plot. Training
the guided prediction, it keeps rising across all of them. The paper: CFG
training "has no effect after a single round of finetuning, but becomes
essential for subsequent rounds".

**The reason offered** is a hypothesis. Each update changes the
conditional prediction but not the unconditional one, so the same w
mixes two predictions that have drifted apart. The samples degrade, the
next round trains on worse samples, "and so on". Nothing in the paper
measures the miscalibration directly.

**DDPO's own runs** use guidance weight 5 for every method (App. D.5), and
the appendix lists CFG training among the paper's design decisions. The
main text does not mention it, and DDPO itself is never run without it.

## Conditions

- **One algorithm, one reward, one curve.** The ablation is RWR_sparse on
  compressibility, not DDPO's policy gradient, and has one run per arm. The
  paper's claim that it is "essential for methods that do more than one
  round of interleaved sampling and training" generalizes from that.
- **Single-round training does not need it.** By the paper's own reading,
  the difference appears only once the model trains on its own updated
  samples. An offline method trained once on fixed pairs, such as
  Diffusion-DPO ([LIT-tmp4m2nj](../literature.d/LIT-tmp4m2nj.md)), is outside the claim; [SOTA-tmplmlbx](SOTA-tmplmlbx.md) is
  the record's practice for that case.
- **The fixed weight is baked in.** The tuned model is calibrated for the
  w it was trained at. Sampling it at another guidance weight was not
  tested.
- **The flow-matching successors are silent.** Flow-GRPO ([LIT-tmpdktqx](../literature.d/LIT-tmpdktqx.md))
  carries DDPO's policy to flow models and does not say whether guidance
  is applied during training. Whether this matters for a model whose
  guidance has been distilled into the weights is untested.
- **It is the RL counterpart of an Active practice.** [SOTA-424](SOTA-424.md) trains one
  network for both scores by dropping the condition, then picks the
  weight at sampling. During reward tuning this practice keeps that
  network and fixes the weight before training instead.

## Known implementations

- DDPO, the source's code, with guidance weight 5.
