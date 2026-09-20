---
status: Active
consensus: emerging
consensus_note: >-
  Two groups, independently, on different architectures, corpora, context
  lengths, parameterizations, schedules and tuning strategies, measuring
  critical batch size against the token budget and getting 0.462 and 0.47.
  Neither ran the other's protocol, which is why the agreement carries
  weight: it is two ways of asking with one answer, not a re-run.
title: 'Scale batch size with the token budget, not with compute or model size'
version: 1
tags:
- training-optimization
date: '2026-09-20'
source:
- LIT-tmphgpkf
- LIT-tmp5olz5
introduced_by:
- LIT-tmphgpkf
corrects:
- SOTA-097
- SOTA-062
implementations: []
summary: >-
  Zhang et al. (2024), [LIT-tmphgpkf](../literature.d/LIT-tmphgpkf.md), and Bergsma et al. (2025),
  [LIT-tmp5olz5](../literature.d/LIT-tmp5olz5.md) — critical batch size scales as `D^0.46` and `D^0.47`
  respectively, and is nearly flat in model size once the token budget is held
  fixed. Optimal batch size likewise goes as `D^0.38`. The compute exponent
  the field has used since Kaplan fits a projection: along the Chinchilla
  line `C` and `D` move together and only `D` is doing the work.
explained_by:
- THEORY-tmpzbrsl
---

# SOTA-tmp0cq3b: Scale batch size with the token budget, not with compute or model size
<!-- inactive-ok-file: THEORY-tmpzbrsl — Proposed, and filed in this same contribution as the explanation of this practice -->
<!-- inactive-ok-file: SOTA-097 — Superseded by THIS practice; naming it is how the succession is legible -->
<!-- inactive-ok-file: SOTA-062 — Superseded by THIS practice, for the same reason -->
<!-- inactive-ok-file: SOTA-tmpbfftm — Proposed, and filed in this same contribution as the argument from the other end of the range -->

## Source

Zhang et al. (2024), [LIT-tmphgpkf](../literature.d/LIT-tmphgpkf.md) — [ARXIV-2410.21676](https://arxiv.org/abs/2410.21676).

Bergsma et al. (2025), [LIT-tmp5olz5](../literature.d/LIT-tmp5olz5.md) — [ARXIV-2505.13738](https://arxiv.org/abs/2505.13738).

Both are load-bearing and they are not the same evidence. Zhang et al. is the
decoupling experiment — hold model size fixed, hold data fixed, see which one
moves the answer. Bergsma et al. is the scaling-law fit across a wide
tokens-per-parameter grid, arriving at the same exponent from the other
direction.

## The numbers

    B_crit ∝ D^0.462   (Zhang et al.)
    B_crit ∝ D^0.47    (Bergsma et al., R² = 0.940)
    B_opt  ∝ D^0.38    (Bergsma et al., R² = 0.984)

At fixed token budget, the dependence on model size very nearly disappears.
Models of different sizes trained on the same number of tokens have almost
the same critical batch size.

**What makes this strong is the disagreement in everything else.** The two
groups differ in architecture, dataset, context length, parameterization,
learning-rate schedule, whether weight decay was used, and hyperparameter
strategy. They agree on the exponent to about 2%. Neither replicated the
other; that they converge is evidence about the quantity rather than about a
protocol.

## What was wrong before, and it was not the fit

[SOTA-097](SOTA-097.md) gave `B ∝ C^0.24` from Kaplan's equation 1.7. That fit is not bad
arithmetic. Along the Chinchilla line `N` and `D` scale together, so `C ≈ 6ND`
moves with `D`, and a power law in either describes the data. Kaplan measured
a projection and reported it as the thing.

Bergsma et al. show the tell directly: plot `B` against `C` and a single
power law does not fit the whole cloud, but points at equal `D` — or equal
tokens-per-parameter — fall on parallel lines. That is the signature of a
confounded variable, and it is only visible once you have runs off the
Chinchilla line.

[SOTA-062](SOTA-062.md) made the model-size version of the same error, from a 2021 heuristic.
Its own body said "a reader with a measurement should prefer it". This is the
measurement.

## Why it matters in practice

The consequence is not academic. **Growing the token budget hands you extra
data parallelism for free; growing the model does not.** A team planning a
parallelism strategy from model size is planning from the wrong variable, and
will under-parallelize a long run and over-parallelize a large one.

It also reframes the over-training decision. Because `B_crit` grows with `D`,
a small over-trained model can take larger batches and hence fewer serial
steps — which is why Bergsma et al.'s Pareto analysis over training time and
compute puts small over-trained models on the frontier and shows
under-trained models dominated on both axes.

## What this does not disturb

[SOTA-198](SOTA-198.md) says to measure the gradient noise scale rather than sweep, and to
expect it to rise during a run. Nothing here disputes that instrument or that
observation — a noise scale rising through training is exactly what "critical
batch size grows with tokens seen" looks like from inside a run. What changes
is the reported variable, not the measurement.

[SOTA-093](SOTA-093.md)'s ramp survives for the same reason.

## Why `Active`

Two independent measurements agreeing on an exponent, one of them from a
controlled decoupling experiment designed to answer exactly this question,
plus a theoretical account of the split ([THEORY-tmpzbrsl](../theory.d/THEORY-tmpzbrsl.md)). The practice it
replaces rested on a single 2020 fit that its own entry in this record had
already flagged as never re-derived.

## Conditions

**`B_crit` is a ceiling, not a target.** It marks where extra parallelism
stops buying speed; it does not say to sit there. [SOTA-tmpbfftm](SOTA-tmpbfftm.md) argues from
the other end that the useful operating point is well below it.

The exponent is robust across two groups; the *level* is not, and it depends
on the overhead threshold chosen to define `B_crit`. Two studies at the same
exponent with different constants still prescribe different batch sizes.

Largest models measured are 1.2B and 3.3B. Both studies are single-epoch.
Neither models communication cost, which is where the free parallelism would
actually be spent.

## Known implementations

- None reports having chosen a batch size this way. The record's recipes
  either follow the compute heuristic or do not say.
