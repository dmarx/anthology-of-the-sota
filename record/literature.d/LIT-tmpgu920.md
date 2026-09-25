---
status: Active
title: 'Model Merging in Pre-training of Large Language Models'
version: 1
tags:
- training-optimization
- model-stability
- analysis-and-evaluation
date: '2026-09-25'
published: '2025-05-17'
arxiv: '2505.12082'
first_author: 'Li'
keywords:
- 'checkpoint-averaging'
- 'model-merging'
- 'warmup-stable-decay'
- 'annealing-proxy'
- 'moe-pretraining'
- 'loss-spike-recovery'
implementations: []
extends:
- LIT-145
summary: >-
  Li et al. (ByteDance Seed, 2025), [ARXIV-2505.12082](https://arxiv.org/abs/2505.12082). A uniform average of
  about ten recent checkpoints on a constant-learning-rate (WSD stable-phase)
  run beats the latest checkpoint at every size tested, up to 20B/200B MoE and
  70B dense. It roughly tracks where an anneal would land. The travelling
  claim, that constant LR plus merging "can effectively match the performance
  of an annealed model at any point", rests on one fork of one 1.3B/13B
  model. At the end of that fork's 250B-token decay, the annealed model is
  about 1.5 MMLU ahead. The baselines in the big tables are unannealed
  checkpoints.
---

<!-- inactive-ok-file: SOTA-tmpc94s8 SOTA-156 SOTA-288 — all Proposed; the practice this
     paper sources, and two neighbours it is placed against without being
     relied on by either -->

# LIT-tmpgu920: Model Merging in Pre-training of Large Language Models

Li, Ma, Yan, Zhang, Liu, Lu, Xu, Chen, Wang, Zhan et al. (2025) — [ARXIV-2505.12082](https://arxiv.org/abs/2505.12082)

A preprint with private architecture and data. The composite metric is a
weighted average over 16 benchmarks whose weights are not given. There are
no seeds and no error bars. The figures carry no numbers in text, so the
values below are read off the paper's own bar labels, or estimated from line
plots where marked ≈.

## Key takeaways

**The method is plain trajectory averaging.** It averages `N` sequential
checkpoints spaced `V` tokens apart. The weighting is uniform (SMA), linear
(WMA) or exponential (EMA). The default after ablation is **SMA, N = 10**. It
is named "Pre-trained Model Average" (PMA).

**Stable phase against the latest stable checkpoint** (MoE, bar labels):

| model | HumanEval | BBH | MMLU | GSM8K |
| --- | --- | --- | --- | --- |
| 1.3B/13B | 31.1 → 36.6 | 50.8 → 56.5 | 65.9 → 68.5 | 65.1 → 70.1 |
| 10B/100B | 54.3 → 61.6 | 83.7 → 84.7 | 82.3 → 84.0 | 84.9 → 88.6 |
| 20B/200B | 59.8 → 66.5 | 85.2 → 87.4 | 84.6 → 85.6 | 87.0 → 89.3 |

Dense 70B goes from 85.9 → 91.3 on GSM8K. **The baseline is an unannealed
checkpoint**, so this measures averaging against no decay at all, not against
a model anyone would ship.

**The one controlled "replace the decay" arm (Fig. 3).** "we forked two
training runs from the stable phase of Seed-MoE-1.3B/13B at 1.4T tokens. One
continued with a constant learning rate, while another underwent annealing,
each training for an additional 250B tokens." At the end (≈):

| 1.6T | constant | annealed | constant + PMA |
| --- | --- | --- | --- |
| HumanEval | 31 | 34.4 | 36 |
| BBH | 51 | 56.5 | 56.5 |
| MMLU | 65.6 | **69.8** | 68.3 |
| GSM8K | 66 | 71.3 | 71.0 |

**Choices late in training barely matter.** At 1.6T tokens the weighting
schemes span 0.25 points, and `V` from 4B to 32B spans 0.5. Early they matter
a lot: at 204B tokens, `V = 32B` is **4.6 below** the unmerged checkpoint, and
`N = 15` is also below it.

## Traps

- **"Merging replaces annealing."** The paper's own endpoint has the anneal
  ahead on MMLU. "Early in training" the merged model beats an anneal that is
  only 50B tokens into its decay. The larger-model evidence (Fig. 2) merges
  checkpoints from *inside* the decay, which is not constant LR against
  annealing. What is supported is the weaker use: the average is a **cheap
  estimate of the annealed score**.
- **"The optimal merging interval scales with model size"** comes from three
  numbers named in prose (4B, 8B, 80B tokens). Only one size is swept, and
  there the late spread is 0.5.
- **PMA initialization for SFT did not replicate**, in the authors' words: "we
  were unable to replicate such significant gains in subsequent experiments
  with other model sizes".
- **The loss-spike rescue has no control.** One 330M/3.3B run at LR 6e-3,
  resumed from the average of three pre-spike checkpoints, recovers. Nothing
  resumes from the latest single pre-spike checkpoint, so averaging cannot be
  told apart from rolling back.
- **The mechanism is algebra, not measurement.** The second-order Taylor
  inequality holds for any average near a minimum. No `δᵢᵀHδⱼ` is measured.
- **The learning rate is not swept.** How much averaging buys depends on the
  stable-phase LR, which is set by a scaling law and held there.

## Standing in the anthology

Filed from the reading-time triage of 2026-09-25, where it was described as
"merges checkpoints along a constant-learning-rate run instead of annealing".
Read, it does not support "instead". It is the scaled-up extension of
[LIT-145](LIT-145.md)'s trajectory averaging on a constant-LR run, and it sources one
narrow practice, `SOTA-tmpc94s8`: estimate the annealed score from a
stable-phase checkpoint average, and still anneal the model you ship.

- [SOTA-140](../practices.d/SOTA-140.md) (WSD): supports it, with a cheaper way to use
  the stable phase. It is not a schedule comparison and does not join the
  sources.
- [SOTA-156](../practices.d/SOTA-156.md) (Schedule-Free) reaches the same end, no decay,
  by averaging inside the optimizer. Neither paper compares against the
  other. Fig. 3 is weak evidence against dropping the decay altogether at a
  fixed budget.
- [SOTA-288](../practices.d/SOTA-288.md) belongs to the same averaging family by a
  different method, and is unchanged.
- [LIT-445](LIT-445.md) uses constant LR with weight averaging as an instrument that
  "reaches comparable loss", an independent use of the same idea at
  85M–1.2B.
- [LIT-673](LIT-673.md) (SWA, Izmailov et al.) was filed on the same day in a
  parallel contribution. It is the origin of averaging along one trajectory,
  and this paper is its constant-learning-rate, pretraining-scale descendant.
  No relation is declared here, because this paper's reference list was not
  checked for it.
- The record holds **no account of why weight averaging works**.
