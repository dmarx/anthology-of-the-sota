---
number: 318
status: Active
formerly:
- SOTA-tmpsbgvf
promote_when: >-
  An independent group running the matched-compression comparison —
  per-matrix rank against a single global rank at the same overall
  compression, on a model family the record holds, with the per-matrix ranks
  derived from the spectra rather than tuned against the evaluation. What
  would NOT meet it: another compression method reporting a better
  quality-versus-size curve than a uniform-rank baseline. That is this
  practice being used, not tested, since any method that beats uniform rank
  by choosing ranks is an instance of it.
consensus: unreplicated
consensus_note: >-
  The premise has three independent measurements and the remedy has one. That
  transformer weight matrices differ in how nearly low-rank they are is
  reported by LIT-516 (Hessian gaps and heavy tails), LIT-517
  (activation-covariance overlap and perplexity ablation) and LIT-519
  (effective-rank entropy across eleven checkpoints), by three unrelated
  instruments. That choosing the rank per matrix therefore beats choosing one
  globally has been measured by LIT-516 alone. The three do not agree on
  which matrices fall where, which is an argument for the instruction as
  stated — measure yours — and against any published list.
title: 'Choose the rank per matrix when you compress a transformer, because low-rank structure varies by component and by depth'
version: 1
tags:
- inference-optimization
- adaptation-and-tuning
date: '2026-09-22'
source:
- LIT-516
introduced_by:
- LIT-516
implementations: []
summary: >-
  Jaiswal et al. (2024), [LIT-516](../literature.d/LIT-516.md) — "transformer weights
  are low rank" is true of some matrices and false of others. Query, Key and
  MLP Gate converge to low rank; MLP Up, MLP Down and Value do not; middle
  blocks resist while the first and last few give way. Setting the rank per
  matrix instead of globally is **~6.4×** better in perplexity than uniform
  reduction at 30% on LLaMA-2 7B and **~47×** at 40% on 13B.
---

# SOTA-318: Choose the rank per matrix when you compress a transformer, because low-rank structure varies by component and by depth

## Source

Jaiswal, Wang, Yin, Liu, Chen, Zhao, Grama, Tian and Wang (2024),
[LIT-516](../literature.d/LIT-516.md) — read as [NOTE-264](../notes.d/NOTE-264.md).

## When this applies

Any time you are about to pick a rank: SVD compression of a finished
checkpoint, a low-rank branch beside a quantized one, deciding which matrices
a memory-constrained fine-tune will update. It does not apply to
[SOTA-184](SOTA-184.md)'s adapters, where the rank sets how much *new* capacity the
update has rather than how much existing structure it can capture.

## Do this

**Measure each matrix's spectrum before you compress it.** One SVD per
matrix, no data, no forward passes. The quantity is how concentrated the
Frobenius magnitude is — a heavy tail in the sorted singular values, or
equivalently a low entropy effective rank `exp(−Σ pᵢ log pᵢ)` on the
trace-normalized spectrum.

**Give each matrix its own reduction ratio.** Matrices whose magnitude is
concentrated take deep cuts; matrices whose spectrum is spread take shallow
ones or none. At 50% overall effective-rank reduction on LLaMA-2 7B this puts
`q_proj` and `k_proj` above **90%** compression and leaves others nearly
untouched.

**Expect the split to fall roughly along these lines — and check anyway.**

| tends to compress | tends to resist |
|---|---|
| Query, Key, MLP Gate | MLP Up, MLP Down, Value |
| first and last few blocks | middle blocks |

The table is one paper's classification and a second measurement disagrees
with it on two of six matrix types ([NOTE-263](../notes.d/NOTE-263.md)). Which is
the point: the instruction is to measure, not to adopt the list.

## What it buys

Against a single global rank at matched compression:

| LLaMA-7B, 25% compression | factoid QA | multi-turn | summarization |
|---|---|---|---|
| full model | 79.02 | 7.61 | 8.15 |
| uniform rank | **34.63** | 4.88 | 5.01 |
| per-matrix rank | **71.89** | 6.09 | 6.46 |

In perplexity: ~6.4× better than uniform at 30% reduction (LLaMA-2 7B), ~47×
at 40% (13B). Against *tuned* baselines the margin is ordinary — 71.89 against
SVD-LLM's 71.95 is a tie — and the large numbers are all against uniform.
Quote them that way.

**It composes with activation-aware SVD rather than replacing it.** C4
perplexity on LLaMA-7B: plain SVD gives 91.99 at 30% reduction and diverges
beyond; per-matrix ranks combined with ASVD give 7.87 at 30% and 14.76 at 50%.

## Why `Active` on one group's comparison

Because the premise is measured three times and the remedy is close to
arithmetic once the premise holds. If the spectra of two matrices differ in
how much magnitude sits in their top `r` directions, then one `r` cannot be
the right cut for both, and the only question is how much the difference
costs. The measurement is one SVD per matrix, data-free and one-shot, so the
instruction is cheap enough that being wrong about the magnitude is not
expensive.

What is genuinely unreplicated is the comparison itself, and that is what
`consensus` says.

## Conditions

**The classification is not settled, and the practice does not depend on it
being settled.** Three instruments agree that low-rank structure is
non-uniform and disagree on where the lines fall — Value and Gate land
differently in [NOTE-263](../notes.d/NOTE-263.md) and [NOTE-264](../notes.d/NOTE-264.md), and
[NOTE-262](../notes.d/NOTE-262.md) reports MLP Down among the most concentrated
matrices by entropy. Use your own spectra.

**Concentration is not importance.** Choosing a rank from the magnitude
spectrum tells you what you can subtract with least Frobenius error. It does
not tell you what the model needs — [SOTA-317](SOTA-317.md) is the practice
about that, and the two should be read together.

**Measured on language transformers.** LLaMA-2 7B and 13B, LLaMA-7B,
Mistral-7B, with the corroborating spectra on BERT, Pythia, Llama-3.1-8B and
eleven GPT-2-style checkpoints. No convolutional model, and no diffusion
transformer — which matters, because [SOTA-314](SOTA-314.md) applies a single global
rank to exactly that class.

**The ratios are derived, not swept.** The paper computes a per-matrix
reduction from the heavy-tail property; it does not show that ratio is near
the best available one.

**The spectral shape you read is stable, which is what makes one reading
enough.** [LIT-520](../literature.d/LIT-520.md) finds the trace-normalized spectrum
reaches stationarity within roughly the first thousand pretraining steps and
holds across architectures, schedules and optimizers. That licenses reading it
once; it does not license assuming the *directions* stay put.

## Known implementations

None beyond the authors' own release.
