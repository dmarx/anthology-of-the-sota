---
number: 254
status: Proposed
formerly:
- SOTA-tmp4dbv9
promote_when: >-
  A second group measuring the AR-versus-diffusion crossover at a unique-token
  budget an order of magnitude above 100M, with both arms swept over epoch
  count; or any released model trained as masked diffusion specifically
  because its corpus was fixed. What would not move it: a diffusion language
  model beating an autoregressive one on benchmarks at a single epoch, which
  is the comparison this practice says is the wrong one.
consensus: unreplicated
consensus_note: >-
  One group, one sweep, and the crossover it turns on is fitted below 100M
  unique tokens. Nothing in the record contests it; nothing replicates it
  either. It strengthens SOTA-157 rather than competing with it.
title: 'Train the language model as a masked diffusion model when the corpus is fixed and the compute is not'
version: 2
history:
- version: 2
  date: '2026-09-25'
  note: >-
    The inference-cost paragraph said the cost was "not accounted anywhere".
    MDLM (LIT-702) and SEDD (LIT-701), filed today, report sampling
    wall-clock at small scale, so the sentence now says what is measured and
    what still is not. Neither paper is a source: neither varies the
    unique-token count. Recommendation, sources and `promote_when:`
    unchanged.
tags:
- model-architecture
- training-optimization
- generative-modeling
date: '2026-09-19'
source:
- LIT-442
introduced_by:
- LIT-442
extends:
- SOTA-157
implementations: []
summary: >-
  Prabhudesai et al. (2025), [LIT-442](../literature.d/LIT-442.md) — masked diffusion keeps
  extracting signal from a repeated corpus for roughly 512 epochs where
  autoregressive training stops at 32. Below a critical compute threshold,
  given in closed form from the unique-token count, autoregressive training
  is better and by a wide margin; above it, diffusion is better. The
  recommendation is the condition, not the objective.
---

# SOTA-254: Train the language model as a masked diffusion model when the corpus is fixed and the compute is not
<!-- inactive-ok-file: SOTA-124 — Proposed, and named as one of the three positions this practice is placed among -->
<!-- inactive-ok-file: SOTA-157 — Proposed, and the practice this one specializes; the pairing is declared in `extends:` -->
<!-- inactive-ok-file: SOTA-173 — Proposed, and the practice whose remedy this one parts company with -->

## Source

Prabhudesai et al. (2025), [LIT-442](../literature.d/LIT-442.md) — [ARXIV-2507.15857](https://arxiv.org/abs/2507.15857).

## The recommendation is a conditional, and both arms of it are the practice

**Below the crossover, train autoregressively.** At the Chinchilla-optimal
single-epoch point, masked diffusion is not slightly worse but badly worse —
validation loss 10.65 against 7.07 in the 100M-unique-token regime. A reader
who takes "diffusion beats autoregressive" out of its condition will spend a
pretraining budget getting a much worse model.

**Above it, train as masked diffusion.** Trained on over repeated data, the
autoregressive model bottoms out around 50 epochs and then deteriorates;
the diffusion model keeps improving to 500 epochs and past, reaching a lower
final loss (3.55 against 3.71) with no overfitting visible inside the budget
explored.

The crossover itself is computable: the training FLOPs at which the two
fitted losses are equal follows a power law in the unique-token count, given
in closed form. That is what makes this a practice rather than an
observation — a practitioner with a fixed corpus can work out which side they
are on before committing the budget.

## The quantity behind it

`R*` is [LIT-166](../literature.d/LIT-166.md)'s learned constant for the epoch count past which repetition
stops paying. Refitting the same law with the objective swapped gives
**512.85 for masked diffusion against 31.93 for autoregressive**. Repetition
tracks fresh data for about 4 epochs under AR and about 100 under diffusion.

The reading the authors offer is implicit augmentation: masked diffusion
draws a new masking pattern each pass, so the *n*-th epoch is a different
prediction problem, where autoregressive training's fixed factorization makes
it nearly the same one. That reading is not established — see below.

## What this changes about the repetition dispute

The record holds three positions on how far a corpus may be repeated:
[SOTA-124](SOTA-124.md) (epoch size against the memorization window), [SOTA-171](SOTA-171.md) (four
epochs) and [SOTA-173](SOTA-173.md) (repetition overfits, and the overfitting belongs to
the objective rather than to repetition).

This does not add a fourth. It **reproduces [SOTA-171](SOTA-171.md)'s four-epoch bound for
autoregressive training and shows it is a fact about that objective**, which
is [SOTA-173](SOTA-173.md)'s diagnosis arrived at independently. Where it parts company with
[SOTA-173](SOTA-173.md) is the remedy: rather than patching the autoregressive objective
with augmentation, change it. Appendix 7 applies random token masking and
attention dropout to the autoregressive arm — two of [SOTA-173](SOTA-173.md)'s three
families, in the setting it describes — and the gap does not close.

That is not a refutation. [SOTA-173](SOTA-173.md) claims augmentation *delays* overfitting
rather than removing it, and its source combines three families where this
tries two. But it is the first evidence in the record on that practice from
outside its own source, and it points the other way.

## Conditions, and why this is `Proposed`

One group. The fitted law comes from unique-token budgets of 25M, 50M and
100M; the single larger run — 2.3B parameters on 500M unique tokens, 130
epochs — was terminated before convergence. The data constraint the practice
addresses is arriving at corpus sizes four orders of magnitude above where
the crossover was measured, and nothing here says the power law reaches
there.

**Inference cost is not accounted for in the comparison.** Every comparison is at matched
*training* compute. A masked diffusion model pays sampling costs an
autoregressive one does not, and the practitioner's real budget includes
them. Whether the crossover survives at matched total cost is unmeasured.
The record now holds only sampling-side numbers, at GPT-2 scale and apart
from any data-constrained comparison. SEDD ([LIT-701](../literature.d/LIT-701.md)) matches
autoregressive wall-clock at about 100 sampling steps in unoptimized code.
MDLM ([LIT-702](../literature.d/LIT-702.md)) halves its own sampling time by caching a denoiser that
ignores the timestep. Neither is a source here, since neither varies the
unique-token count. MDLM's LM1B gap to AR narrows from 4.7 to 2.1 perplexity
points between 33B and 327B tokens without crossing, which is the direction
this practice predicts and is not a test of it.

The mechanism is the weakest part. Implicit augmentation is asserted, and in
the one place it is tested — by giving the autoregressive arm explicit
augmentation — it does not reproduce the benefit. So the *whether* is well
measured and the *why* is open.

## Relation to [SOTA-157](SOTA-157.md)

[SOTA-157](SOTA-157.md) says train as a masked diffusion model, full stop, on the strength
of LLaDA's capability parity. This is that instruction with a condition and a
different kind of evidence behind it: a scaling law with a stated boundary
rather than a benchmark comparison. A conditional recommendation that says
where it stops being true is the stronger of the two, and it is why this is
filed separately rather than folded in.

## Known implementations

- None. No model in this record was trained as a diffusion model because its
  corpus was fixed.
