---
number: 14
status: Proposed
formerly:
- THEORY-tmpclzj7
promote_when: >-
  Post-local SGD's own schedule run with an outer momentum optimizer over the
  deltas, showing its usable H rising above the 16 to 32 it reports without
  one. That is the one experiment none of the three papers ran, and it
  isolates the claim: same workload, same inner optimizer, outer optimizer the
  only thing changed. A fourth local-update paper reporting a large H with an
  outer optimizer already in place does not settle it, because the two are
  confounded there exactly as they are in LIT-212.
title: 'The outer optimizer is what buys the inner step count'
version: 1
tags:
- distributed-optimization
date: '2026-09-16'
source:
- LIT-212
- LIT-373
- LIT-362
explains:
- SOTA-155
- SOTA-216
summary: >-
  Three papers in this record prescribe how many steps a worker takes between
  synchronisations, and they differ by a factor of thirty: [LIT-362](../literature.d/LIT-362.md) says 16 to
  32, [LIT-373](../literature.d/LIT-373.md) says 12 to 48, [LIT-212](../literature.d/LIT-212.md) says 500. They are not disagreeing about
  the same quantity. The two with small intervals average parameters and stop
  there; the one with a large interval runs Nesterov momentum over the
  accumulated deltas, and its own ablation reports that plain averaging at
  that interval performs poorly. The interval is not a constant to transfer.
  It is bought, and the outer optimizer is what pays for it.
---

<!-- inactive-ok-file: SOTA-155, SOTA-216 — both Proposed, and both cited
     here as what this account explains rather than as evidence for it.
     The evidence is LIT-212, LIT-373 and LIT-362; the two practices are
     the documents whose apparent disagreement it resolves, which is the
     whole reason a THEORY names an `explains` list. -->

# THEORY-014: The outer optimizer is what buys the inner step count

## The claim

Every local-update scheme has two knobs that look independent and are not:
how many steps `H` a worker takes alone, and what happens to the accumulated
deltas when the workers finally meet. The second sets the ceiling on the
first.

Read that way, the record's three prescriptions stop competing:

| | interval | what happens at the sync | workload |
|---|---|---|---|
| [LIT-362](../literature.d/LIT-362.md) (2018) | `H` = 16–32 | parameters averaged | ResNet, CIFAR/ImageNet, `K` = 16 |
| [LIT-373](../literature.d/LIT-373.md) (2019) | `tau` = 12–48 | averaged, then an outer momentum step | ImageNet, WMT |
| [LIT-212](../literature.d/LIT-212.md) (2023) | `H` = 500 | Nesterov momentum over the deltas | 400M transformer, C4, `k` = 8 |

The ordering is the wrong way round for a "correct value of `H`" story — the
paper with an outer optimizer and the smallest interval sits between the two
that disagree by thirty times. It is the right way round for this one, once
you notice that [LIT-373](../literature.d/LIT-373.md)'s interval is small because it is *matching a
communication budget*, not because that is as far as its method reaches.

## What was actually shown

**[LIT-212](../literature.d/LIT-212.md) ran the controlled version of this, and it is the strongest evidence
here.** Holding `H` = 500 fixed, it varies only the outer optimizer, and finds
that outer SGD — which is plain parameter averaging, which is what [LIT-362](../literature.d/LIT-362.md)
does — "performed poorly", as does outer Adam. Nesterov momentum at outer
learning rate 0.7 and outer momentum 0.9 is what works. So at the interval
[LIT-362](../literature.d/LIT-362.md) could not reach, the thing [LIT-362](../literature.d/LIT-362.md) does at the sync is reported to
fail, in the paper that reaches it.

**[LIT-373](../literature.d/LIT-373.md) ran the other half.** Slow outer momentum on top of local SGD or a
gossip optimizer improves optimization and generalization at negligible extra
communication, across ImageNet and WMT. It is a with-and-without comparison of
the outer step, by a different group, four years earlier, at intervals an
order of magnitude below [LIT-212](../literature.d/LIT-212.md)'s.

**And [LIT-212](../literature.d/LIT-212.md) cites [LIT-373](../literature.d/LIT-373.md) as where its outer optimizer came from.** Its
related work names [LIT-373](../literature.d/LIT-373.md) and FedOpt as having "extended [federated
averaging] to more powerful outer optimizers", and says that work "inspired
our use of Nesterov momentum in the outer optimization". This record had the
two filed as an unreconciled pair; one of them says it is descended from the
other.

**The interval is a plateau, not an optimum.** [LIT-212](../literature.d/LIT-212.md)'s sweep reports that
going below `H` = 500 has diminishing returns and that `H` = 1000 costs 2.9%
perplexity relative to `H` = 50 while communicating 20× less. That is a flat
curve over a 20-fold range, so 500 is a point chosen for its bandwidth rather
than a measured peak. [LIT-362](../literature.d/LIT-362.md)'s 16–32 is a peak, swept for accuracy. Two
numbers off the same axis, chosen against different objectives.

## What rests on it

[SOTA-155](../practices.d/SOTA-155.md) prescribes many inner steps *and* an outer momentum optimizer, and
the practice reads as though the first were the recommendation and the second
a detail. It is the other way round. If this account is right, a reader who
takes the interval and drops the outer optimizer has taken the part that does
not work alone.

[SOTA-216](../practices.d/SOTA-216.md) closes by naming [LIT-212](../literature.d/LIT-212.md)'s `H` = 500 as unreconciled with its own 16
to 32. It is reconciled here: the two are measuring different things, and the
gap is what the outer optimizer buys. What survives that reconciliation is
[SOTA-216](../practices.d/SOTA-216.md)'s *other* claim — the switch at the first learning-rate decay — which
is about when to start communicating rarely, not about how rarely, and which
[LIT-212](../literature.d/LIT-212.md) neither tests nor contradicts.

## What this does not say

**Nothing here is a controlled test of the reconciliation itself.** The
evidence is two controlled tests of the outer optimizer, at two intervals, on
different workloads, plus an inferred explanation of why the third number is
different. `promote_when` names the experiment that would settle it, and
nobody has run it.

**The confounds are real and they are not small.** [LIT-212](../literature.d/LIT-212.md) differs from
[LIT-362](../literature.d/LIT-362.md) in inner optimizer (AdamW against SGD), domain (language against
vision), model (transformer against ResNet), worker count (8 against 16) and
total steps (88,000 against a few thousand). Any of those could carry part of
the gap. [LIT-361](../literature.d/LIT-361.md)'s `H = O(sqrt(T/(Kb)))` accounts for some of it — more total
steps and fewer workers both push `H` up — but on the papers' own numbers that
factor is nearer five than thirty.

**It says nothing about how large `H` can get.** The claim is that the outer
optimizer raises the ceiling, not that it removes it. [LIT-212](../literature.d/LIT-212.md) sees degradation
by `H` = 1000, and the paper it cites for large-scale local SGD failing
(Ortiz et al.) reports trouble at `k` >= 16 replicas, which is twice what
[LIT-212](../literature.d/LIT-212.md) uses by default.

**It is silent on the streamed synchronisation.** That is [SOTA-155](../practices.d/SOTA-155.md)'s other
half, it comes from a different paper, and no result here bears on it.
