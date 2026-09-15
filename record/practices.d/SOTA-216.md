---
number: 216
status: Proposed
formerly:
- SOTA-tmpe3b5u
promote_when: >-
  The switch demonstrated on a transformer language-model pretraining run at
  a scale this record cares about. What would not satisfy this: another image
  benchmark, or a result that local SGD alone communicates less — that is
  established and is not the claim.
consensus: unreplicated
consensus_note: >-
  One group for the schedule, a second for the interval it uses. The
  generalization claim it rests on — that large-batch training loses something
  small-batch noise supplies — is itself contested elsewhere in this record.
title: 'Switch from minibatch SGD to local SGD at the first learning-rate decay, rather than choosing between them'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
source:
- LIT-362
# The synchronisation interval the schedule needs, derived rather than swept.
- LIT-361
introduced_by:
- LIT-362
implementations: []
summary: >-
  The two options are usually posed as a choice: minibatch SGD generalises and
  communicates every step, local SGD communicates rarely and generalises
  worse. Post-local SGD is the observation that they are wanted at different
  times — run minibatch SGD until the first learning-rate decay, then switch
  to local SGD with H around 16 to 32 for the rest. The early phase is where
  the gradient noise is doing work; the late phase is where communication is
  pure overhead.
---

# SOTA-216: Switch from minibatch SGD to local SGD at the first learning-rate decay, rather than choosing between them

## What to do

Run ordinary synchronous minibatch SGD from initialization until the first
learning-rate decay. Then switch to local SGD: each worker takes `H` steps on
its own and the workers average every `H` steps, with `H` of 16 to 32 as the
reported range.

When choosing `H` from first principles rather than from that range,
[LIT-361](../literature.d/LIT-361.md) gives `H = O(sqrt(T/(Kb)))` for `T` total steps, `K` workers and
local batch `b` — the largest interval that still preserves linear speedup.

## Why

**The two methods are not competing; they are suited to different phases.**
The argument in [LIT-362](../literature.d/LIT-362.md) is that large-batch SGD loses generalization
because it loses gradient noise, and that this matters in the early phase,
before the first decay, when the trajectory is still choosing a basin. After
that decay the noise is no longer buying anything and per-step communication
is paying for nothing.

**Local SGD is the better of the two at equal compute per round.** The same
paper's second finding is that local SGD beats minibatch SGD at matched
effective batch size on both generalization and communication — so the switch
is not a concession, and the only reason to run minibatch SGD at all is the
early phase.

## What this does not settle

**Image classification, 2018.** ResNets on CIFAR and ImageNet. Nothing here
tests it on a transformer, and DiLoCo — the local-update scheme this record
does carry a practice for — uses `H = 500`, an order of magnitude beyond this
paper's range, and does not do the early minibatch phase at all. Those two
facts are unreconciled.

**The generalization premise is not settled inside this record.** The claim
that large batches cost generalization, rather than costing tuning effort, is
exactly what [SOTA-218](SOTA-218.md) says to be careful about: a large-batch run whose
metaparameters were transferred rather than retuned will under-perform for
reasons that have nothing to do with noise.

**"The first learning-rate decay" presumes a schedule with decays.** Under a
cosine or schedule-free regime there is no such moment, and the practice gives
no rule for finding one.
