---
status: Active
title: 'ESSAM: A Novel Competitive Evolution Strategies Approach to Reinforcement Learning for Memory Efficient LLMs Fine-Tuning'
version: 1
tags:
- adaptation-and-tuning
date: '2026-09-15'
published: '2026-02-01'
arxiv: '2602.01003'
first_author: 'Sun'
keywords:
- 'evolution-strategies'
- 'sharpness-aware-minimization'
- 'memory-efficiency'
- 'mathematical-reasoning'
- 'zeroth-order'
extends:
- LIT-211
compared_against:
- LIT-127
implementations: []
summary: >-
  Sun et al. (2026), [ARXIV-2602.01003](https://arxiv.org/abs/2602.01003). Adds a sharpness-aware step to ES: move
  the parameters against the reward-weighted direction first, recompute the
  update at that neighbouring point, and apply it at the original — steering
  the solution toward flat regions. On GSM8K across Qwen2.5 at 0.5B-7B it
  averages 78.27% against standard ES's 75.97%, PPO's 77.72% and GRPO's
  78.34%, at inference-level GPU memory.
---

# LIT-tmprde8b: ESSAM: A Novel Competitive Evolution Strategies Approach to Reinforcement Learning for Memory Efficient LLMs Fine-Tuning

Sun et al. (2026) — [ARXIV-2602.01003](https://arxiv.org/abs/2602.01003)

## Key takeaways

**The gap it closes is standard ES's, not GRPO's.** Standard ES averages
75.97% on GSM8K across the four models; ESSAM reaches 78.27%. Against the RL
baselines it is a tie — PPO 77.72%, GRPO 78.34% — which the paper states
plainly rather than dressing up. **The honest headline is that a
sharpness-aware ES matches RL at inference-level memory**, not that it beats
it.

**The mechanism is SAM transposed into zeroth order.** Sharpness-aware
minimization normally needs a gradient to find the adversarial neighbour.
ESSAM uses the reward-weighted ES aggregate instead: move the parameters in
the direction that *would* increase sharpness, recompute perturbations and
rewards at that neighbouring point, then apply the resulting direction to the
original parameters. The effect is to prefer flat regions without ever
computing a gradient.

**Memory is the point and the numbers are large.** ESSAM holds the same GPU
memory footprint as plain ES — inference level, since only forward passes are
required — which the paper reports as a 10–18× reduction against PPO and
GRPO. That is the "10× space-efficiency" figure [LIT-231](LIT-231.md) cites this paper
for.

**It is a direct answer to an observed weakness.** The motivation is that ES
underperforms on mainstream mathematical reasoning benchmarks like GSM8K, and
the fix targets generalization rather than optimization speed — the paper's
own diagnosis is that plain ES overfits its sampled rewards.

## What the evidence does not cover

**One benchmark.** GSM8K, four Qwen2.5-Instruct models at 0.5B, 1.5B, 3B and
7B. No second task, no second family.

<!-- inactive-ok-block: SOTA-211 — Proposed, and named as the practice this paper’s design points away from; the contrast is the citation’s point -->
**No ablation isolating the SAM step from the extra evaluations it costs.**
The two-stage update evaluates perturbations twice per iteration; whether the
gain comes from sharpness-seeking or from the additional sampling is not
separated, which matters given that [SOTA-211](../practices.d/SOTA-211.md) is about exactly how ES
should spend a doubled evaluation budget.

**The flat-minima argument is inherited rather than tested.** The claim that
flatter solutions generalize better is imported from the SAM literature; no
sharpness measurement is reported for the resulting checkpoints.

## Standing in the anthology

<!-- inactive-ok-block: SOTA-211 — Proposed, and named as the practice this paper’s design points away from -->
**A second way of spending an ES evaluation budget, and it points the other
way from [SOTA-211](../practices.d/SOTA-211.md).** That practice says do not spend two evaluations on
one direction — the antithetic pair's second evaluation buys nothing when
responses are regenerated. ESSAM spends a second round of evaluations too, on
something else entirely: probing a neighbouring point to steer toward flat
regions. The two are not in conflict, and the contrast is the useful part —
**the question for an ES practitioner is not whether to spend more
evaluations but on what**, and the record now holds two answers with different
evidence behind them.

<!-- inactive-ok-block: THEORY-006 — Proposed, named as the account whose
     scale reading this paper's 0.5B row is consistent with -->
It is also a small corroboration of the scale pattern [THEORY-006](../theory.d/THEORY-006.md) predicts,
from a paper not looking for it: the per-model table is where standard ES is
weakest at the small end, and the paper's framing of ES as overfitting its
sampled rewards at small scale is what a low density of task-improving
perturbations would look like from the inside.
