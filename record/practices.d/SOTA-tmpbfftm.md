---
status: Proposed
promote_when: >-
  A second group running pretraining at or near batch size one with the
  half-life rule applied, at 1B or above and at a Chinchilla-or-better token
  ratio, against a tuned large-batch baseline; or a released model trained
  this way. What would not move it: another demonstration that small batches
  are stable, which is already established here — the open question is
  whether they are preferable at scale and in sharded training.
consensus: unreplicated
consensus_note: >-
  One group. The mechanism is convincingly isolated and the largest check is
  a single under-trained 1.3B run against an untuned baseline. It also
  contradicts what essentially every pretraining recipe in this record does,
  which is a reason for care rather than for dismissal.
title: 'Use the smallest batch size that still saturates the device, and do not gradient-accumulate to avoid it'
version: 1
tags:
- training-optimization
date: '2026-09-20'
source:
- LIT-tmp5ytk5
introduced_by:
- LIT-tmp5ytk5
implementations: []
summary: >-
  Marek et al. (2025), [LIT-tmp5ytk5](../literature.d/LIT-tmp5ytk5.md) — batch size one trains stably once
  Adam's second-moment half-life is held fixed in tokens, matches or beats
  large batches per FLOP, and is far more robust to hyperparameter
  misspecification. Gradient accumulation costs memory for the accumulated
  gradient and forgoes optimizer steps, and is worth it only when multiple
  device replicas are bottlenecked on interconnect bandwidth.
---

# SOTA-tmpbfftm: Use the smallest batch size that still saturates the device, and do not gradient-accumulate to avoid it
<!-- inactive-ok-file: SOTA-097 — Superseded in this same change; named as one of the practices whose shared assumption this one disputes -->
<!-- inactive-ok-file: SOTA-062 — Superseded in this same change; named in the same list -->
<!-- inactive-ok-file: SOTA-tmp1t2ao — Proposed, and filed in this same contribution as this practice's safety condition -->
<!-- inactive-ok-file: SOTA-tmpuz5ea — Proposed, and filed in this same contribution; named for the unexamined interaction with weight decay -->

## Source

Marek et al. (2025), [LIT-tmp5ytk5](../literature.d/LIT-tmp5ytk5.md) — [ARXIV-2507.07101](https://arxiv.org/abs/2507.07101).

## The recommendation, and the one it replaces

Standard practice is to use the largest batch that fits, and to simulate a
larger one with gradient accumulation when it does not. This says the target
is the **smallest** batch that still maximizes throughput — in practice at
least a few hundred tokens per device, so memory bandwidth does not become
the bottleneck, and raised again if a second-order optimizer's per-step
overhead starts to cost more than the step buys.

Gradient accumulation is then the wrong tool almost everywhere: it *increases*
memory, because the accumulated gradient must be stored, and it trades away
optimizer steps for a batch size the paper argues you did not want. The stated
exception is multiple device replicas bottlenecked on interconnect bandwidth,
where the larger effective batch is buying communication savings rather than
optimization.

## This is only safe with the half-life rule

[SOTA-tmp1t2ao](SOTA-tmp1t2ao.md) is not an optional companion. The entire reputation of small
batches for instability comes from holding `beta_2` fixed while shrinking the
batch, which shortens the second moment's averaging window in tokens by the
same factor. A reader who adopts the small batch without rescaling `beta_2`
gets precisely the instability this practice is explaining away.

## What it buys beyond parity

- **Robustness.** At batch size 1 the loss surface over learning rate and the
  decay rates is markedly flatter than at 512. Less tuning is needed, which
  for most practitioners is worth more than the last few thousandths of a nat.
- **Optimizer choice stops mattering.** SGD, Adafactor, Adam and Muon reach
  similar loss at batch size 1 on a 30M model; the spread opens up as the
  batch grows. Vanilla SGD with no momentum and no optimizer state matched
  the GPT-3 AdamW configuration on a 1.3B model.
- **Memory**, both from the batch itself and from not storing an accumulated
  gradient — and, where SGD becomes viable, from carrying no optimizer state
  at all.

## Where it sits against the ceiling

[SOTA-tmp0cq3b](SOTA-tmp0cq3b.md) establishes that critical batch size grows with the token
budget. That is a ceiling above which parallelism stops paying; this is an
argument about where to sit below it, and the two are compatible. Together
they give a range with a reason at each end, which the record did not have:
every other batch-size practice it holds — [SOTA-097](SOTA-097.md), [SOTA-062](SOTA-062.md), [SOTA-093](SOTA-093.md),
[SOTA-198](SOTA-198.md) — assumes bigger is what you want and asks only how much you can
afford.

## The uncomfortable implication

If optimizer sophistication buys little at small batch, then part of what the
record's optimizer practices recommend is robustness at a batch size this
practice says not to use. That is not a refutation of any of them, and it is a
question none of them answers.

## Conditions, and why this is `Proposed`

**Batch size has to be a free choice, and often it is not.** In sharded
training the global batch is largely set by the parallelism topology, and
nothing here addresses that regime. The recommendation is for the case where
the model fits on a device.

The optimizer sweeps are at 30M parameters. The scale checks are 124M and a
single 1.3B run trained at about 10 tokens per parameter — under-trained
relative to Chinchilla — against an untuned baseline configuration. The case
against gradient accumulation follows from the other results plus a memory
argument rather than from a matched-conditions measurement.

Weight decay is switched off rather than rescaled in the batch-size-1
configurations, which leaves its interaction with the half-life rule
unexamined — and [SOTA-tmpuz5ea](SOTA-tmpuz5ea.md) says weight decay is the hyperparameter that
should be moving.

## Known implementations

- None. Every pretraining recipe in this record uses a large batch, and most
  accumulate.
