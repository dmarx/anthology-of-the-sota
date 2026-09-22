---
status: Read
paper: LIT-tmphxv7m
title: 'Low-rank structure in a transformer is non-uniform, and a global rank is measurably the wrong choice'
version: 1
date: '2026-09-22'
summary: >-
  Read second in the spectral cluster, and it is the one that carries a
  recommendation. "Transformer weights are low rank" turns out to be true of
  some matrices and false of others, with the split systematic by component
  and by depth. The comparison against a uniform rank at matched compression
  was run and the margins are large.
---
<!-- inactive-ok-file: THEORY-059 — Proposed, and this reading is the
     load-bearing answer to its open question. Naming the account being tested
     is the point of the section. -->

<!-- inactive-ok-file: SOTA-274 — Proposed, named once in a DP-009 counting
     paragraph as the same shape one floor over, and explicitly not promoted
     to a principle. -->

# NOTE-tmpzvhd1: Low-rank structure in a transformer is non-uniform, and a global rank is measurably the wrong choice

## Contribution

Ask why LLM weights become low rank, answer through gradient-subspace
stabilization, and discover in the process that they do not all become low
rank. Then use the resulting per-matrix classification to pick compression
ratios, and to pick which matrices to fine-tune.

## Key results

**The classification.** Matrices split by whether the sorted singular values
have a heavy tail:

| group | matrices | Hessian gap | outcome |
|---|---|---|---|
| Low-rank Components | Query, Key, MLP Gate | clear | gradient subspace settles fast, weights go low rank |
| Non-Low-rank Components | MLP Up, MLP Down, Value | unclear | subspace converges slowly, weights stay high rank |

**And by depth.** Middle blocks have small Hessian gaps and resist; the first
and last few blocks go low rank. At 50% effective-rank reduction on LLaMA-2
7B, `q_proj` and `k_proj` accept **over 90%** compression while other matrices
accept almost none.

**Non-uniform against uniform, at matched compression.** This is the
comparison that makes it a practice rather than an observation.

| LLaMA-7B, 25% compression | factoid QA | multi-turn | summarization |
|---|---|---|---|
| full model | 79.02 | 7.61 | 8.15 |
| uniform reduction | **34.63** | 4.88 | 5.01 |
| OWL reduction | 54.42 | 5.27 | 5.16 |
| SVD-LLM | 71.95 | 5.79 | 6.12 |
| WeLore | 71.89 | **6.09** | **6.46** |

In perplexity terms: ~**6.4×** better than uniform at 30% reduction on
LLaMA-2 7B, ~**47×** better at 40% on 13B. Against stronger baselines the
margin is ordinary — 71.89 against SVD-LLM's 71.95 on factoid QA is a tie —
and it is against *uniform* that the gap is a different order of magnitude.

**Combined with activation-aware SVD** (C4 perplexity, LLaMA-7B): plain SVD
gives 91.99 at 30% and NaN beyond; WeLore + ASVD gives 7.87 at 30% and 14.76
at 50%.

**The fine-tuning half.** Updating only the Low-rank Components in decomposed
form matches or beats full fine-tuning with 35% of the trainable parameters,
3× throughput and 40% less GPU memory.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Low-rank structure is non-uniform across components | strong | Hessian-gap analysis plus spectra, three checkpoints |
| C2 | It is non-uniform across depth | strong | layer-wise ratios, and it agrees with an independently reported sparsity profile |
| C3 | Per-matrix rank beats global rank | strong against uniform, ordinary against tuned baselines | matched-compression comparisons on three models |
| C4 | LRC-only fine-tuning ≈ full fine-tuning | moderate | loss trajectories and downstream tasks, one model family |

## Limitations

**The theory is a framework, not a proof about transformers.** Hessian
Lipschitz continuity, a Kurdyka–Łojasiewicz condition, a uniform spectral gap
and architecture reversibility are all assumed. The empirical split stands on
its own; the explanation for it is the assumed part.

**Baselines are the authors' own runs.** Uniform reduction is the foil the
paper is built against, and no third party has repeated the comparison.

**The partition is not confirmed by the neighbouring measurement.**
[LIT-tmpmftzj](../literature.d/LIT-tmpmftzj.md) reaches the same conclusion about *non-uniformity*
by an unrelated instrument — activation-covariance overlap and perplexity
ablation rather than Hessian gaps — and agrees on four matrix types out of
six. It disagrees on Value, which this paper calls high-rank and that one
finds behaves like the other square matrices, and on Gate, which this paper
calls low-rank and that one finds carries informative small singular values in
Llama. Two instruments, one agreed conclusion, two disputed cells.

## Bearing on the record

**It is the load-bearing answer to [THEORY-059](../theory.d/THEORY-059.md)'s question.** Weight
spectra outside diffusion transformers *are* steep — for Query, Key and Gate,
at the ends of the network. They are not steep for the MLP Up and Down
projections, which hold most of the parameters. So the account generalizes
with a qualification the account does not currently carry.

**It is the source of [SOTA-tmpsbgvf](../practices.d/SOTA-tmpsbgvf.md)**, which the record did not
hold in any form. [SOTA-184](../practices.d/SOTA-184.md) trains a low-rank update and chooses one
rank; [SOTA-314](../practices.d/SOTA-314.md) peels a rank-32 branch at 4 bits regardless of which
matrix it is peeling. Neither says the rank is a per-matrix question.

**The shape is [SOTA-274](../practices.d/SOTA-274.md)'s, one floor down.** That practice says to
measure a block's stable rank before adopting a spectral optimizer rather than
assuming the geometry is uniform. This says the same about compression.
Different mechanisms and different literatures; recorded as a second instance
and not as a principle. [DP-009](../../docs/design-principles.md#dp-9).

## Open questions

- **Does the non-uniformity hold in a diffusion transformer?** That is the
  model class [SOTA-314](../practices.d/SOTA-314.md) applies a global rank to, and nobody has run
  this measurement on one.
- **Which instrument is right about Value and Gate?** Two independent
  measurements, two disputed cells, and no experiment addresses the
  disagreement directly.
- **Is the rank dial continuous in the right way?** The paper reports a
  reduction ratio per matrix derived from the heavy tail, not a sweep showing
  the chosen ratio is near-optimal.
