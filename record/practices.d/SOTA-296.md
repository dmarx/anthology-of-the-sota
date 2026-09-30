---
number: 296
status: Proposed
formerly:
- SOTA-tmp91kxm
promote_when: >-
  A division point chosen by measurement rather than by assertion — a sweep
  over what fraction of the token budget the parallel stage needs, at one
  scale, showing where the gain saturates. That is the number this practice
  is missing and the authors name it as open. What would not satisfy it:
  another run using 2% and reporting that it worked, which is this result
  again.
consensus: unreplicated
consensus_note: >-
  One group, one division point, chosen and not swept. The general shape —
  put the expensive phase at the end of pretraining — is well established
  elsewhere in this record, which is a reason to find the result plausible
  and not a replication of it.
title: 'Add the parallel streams in a short final training stage, not from the start'
version: 1
tags:
- training-optimization
- inference-optimization
date: '2026-09-21'
source:
- LIT-486
introduced_by:
- LIT-486
implementations: []
summary: >-
  Chen et al. (2025), [LIT-486](../literature.d/LIT-486.md) — parallel scaling costs `P`× the
  training FLOPs, which is what would otherwise make it unaffordable. Train
  1T tokens the ordinary way, then switch the streams on for **20B tokens,
  2% of the budget**. The loss spikes when the random prefixes appear and
  recovers within **0.0002T tokens**, and the logarithmic gains in `P` are
  the same ones the from-scratch runs show.
---

# SOTA-296: Add the parallel streams in a short final training stage, not from the start

## Source

Chen et al. (2025), [LIT-486](../literature.d/LIT-486.md) — [ARXIV-2505.10475](https://arxiv.org/abs/2505.10475) §4, read as
[NOTE-235](../notes.d/NOTE-235.md).

## What to do

Pretrain normally. Near the end, initialize the prefix embeddings and the
aggregation MLP randomly — standard deviation 0.02 in the reported run — and
continue on a small final slice of the token budget with the streams active.
The authors use **1T tokens plain, then 20B with streams**, annealing the
learning rate over the second stage as a warmup-stable-decay schedule would.

The same move works on a model you did not train: continual pretraining of
Qwen-2.5-3B picks up the streams, and so does **freezing the backbone
entirely** and training only the prefixes and the aggregator.

## Why it works, as far as anyone has shown

The model adapts to the new parameters **fast**. The stage-2 loss initially
rises above the `P = 1` baseline because the prefixes are random noise in a
converged network, and it recovers within **0.0002T tokens** — 0.001% of the
first stage — after which the curve is stable and the gains in `P` are
logarithmic exactly as in the from-scratch fits.

So whatever the backbone has to learn in order to use parallel streams, it is
not much, and it is not what the first trillion tokens were for. That is the
whole argument, and it is an empirical one.

## What it buys

At 1.8B parameters on 1T tokens, going `P = 1 → 8`:

- **+2.6%** on seven general tasks,
- **+4.3%** on eight coding tasks,
- **+7.3%** on three maths tasks,
- **+10 points on GSM8K** — a 34% relative improvement on identical training
  data,

and the gains survive instruction tuning (+5% on IFEval from `P = 1` to
`P = 8`) and compose with chain-of-thought prompting rather than being
substituted by it.

**The frozen-backbone variant buys something different and arguably better:**
one set of weights, `P` chosen at deployment. High-throughput and
low-throughput serving from the same checkpoint, with capacity traded against
batch size at the point where you actually know the batch size.

## Conditions

**The division point is asserted, not measured.** 1T/20B is one point,
chosen, and the paper names finding a better one as open work. There is no
sweep, so "2%" should be read as *an* amount that sufficed at this scale
rather than as a recommended fraction — and nothing says how it moves with
model size or first-stage length.

**The backbone was not trained in anticipation of the streams.** That is the
point of the practice and it is also an untested assumption about generality:
it worked on a model the same authors had just trained, and on Qwen-2.5,
which is their own lab's model.

**It does not make parallel scaling cheap, it makes it affordable.** The
second stage is still `P`× FLOPs on its own tokens. At `P = 8` over 20B
tokens that is 160B token-equivalents of compute, which is 16% of the first
stage — real, and a different order from paying it on the whole run.

**The retrofit evidence is a loss curve and one benchmark.** Continual
pretraining is reported as training loss on corpora Qwen-2.5 had likely
already seen; the frozen-backbone result is code generation only.

**General practice in this record already favours the shape.**
[SOTA-139](SOTA-139.md) extends context in stages for the same reason, and
[SOTA-140](SOTA-140.md)'s warmup-stable-decay schedule is what the second stage anneals
under. That makes this plausible rather than replicated — a familiar shape is
not a second measurement.
