---
number: 222
status: Proposed
formerly:
- SOTA-tmpboy96
promote_when: >-
  The same measurement on a workload whose per-step compute is long enough to
  matter — a transformer pretraining step rather than a ResNet-20 step on
  CIFAR-10. The claim is about a ratio between communication time and one step
  of compute, and LIT-323 predicts its own advantage grows there without
  testing it. A second CIFAR result does not settle it.
consensus: unreplicated
consensus_note: >-
  One paper, one dataset. The general move — overlap the exchange with the
  next step's compute — is old and widely implemented; what is this paper's is
  the anchor construction that makes one step of slack enough.
title: 'Overlap the synchronisation with one or two local steps instead of communicating every step'
version: 1
tags:
- distributed-optimization
date: '2026-09-16'
source:
- LIT-323
introduced_by:
- LIT-323
implementations: []
summary: >-
  Wang et al. (2020), [LIT-323](../literature.d/LIT-323.md). Local SGD is usually argued for as a way to
  communicate rarely, which costs accuracy at large intervals. The cheaper
  reading is that it does not take a large interval to win: at `tau = 2` the
  communication-to-computation ratio falls from 34.6% to 1.5% with convergence
  per iteration roughly unchanged. The interval is not buying infrequency, it
  is buying somewhere to hide the exchange.
---

<!-- inactive-ok-file: SOTA-155, SOTA-216 — both Proposed, and named as the
     two practices in the same family that trade accuracy for bandwidth,
     which this one is claimed not to do. A contrast, not support. -->
<!-- inactive-ok-file: ADR-041 — Proposed, and the decision under which
     this document declines to file two constants. A Proposed decision is
     the resting state of most of this record's decisions. -->

# SOTA-222: Overlap the synchronisation with one or two local steps instead of communicating every step

## What to do

Keep an **anchor model** on each node alongside the local one. After every
`tau` local updates, pull the local model toward the anchor — no communication,
since each node holds its own copy — and let a separate thread average the
local models into a new anchor in the background. `tau = 1` or `2`.

The anchor is the method, not an option. Without it there is nothing to pull
toward while the average is still in flight, and the scheme degenerates to
ordinary local SGD, which has to wait.

## Why

**One step of slack is enough when the exchange has somewhere to go.** The
condition [LIT-323](../literature.d/LIT-323.md) states is simply that the parallel communication time be
smaller than `tau` steps of computation; past that, the latency is completely
hidden and more slack buys nothing while costing consensus. That is why the
recommendation is a small number rather than the largest tolerable one, and it
is the opposite of the reasoning behind [SOTA-216](SOTA-216.md) and [SOTA-155](SOTA-155.md), where a large
interval is the point and something has to recover what it costs.

**The reported number is a ratio.** At `tau = 2`, communication-to-computation
falls from **34.6% to 1.5%**, with loss-versus-iteration convergence roughly
matching fully synchronous SGD — about 0.1 s of additional latency per epoch
against 1.5 s. Accuracy holding is the premise that makes the ratio
interesting, and the paper reports `tau = 1` and `2` slightly *exceeding*
synchronous accuracy.

**It also removes the straggler wait.** Because the exchange is non-blocking,
a node that finishes its local updates first does not idle — which is a second
benefit from the same construction and is not priced into the 1.5%.

## Conditions

**It is a claim about a ratio, so it is a claim about your hardware.** The
34.6% baseline is what communication cost on the paper's cluster for that
model. On a fabric where the exchange is already cheap there is nothing to
hide. [LIT-323](../literature.d/LIT-323.md) expects its advantage to be "further magnified" on a slower
interconnect — it names 10 Gbps as an example of slower — or on a larger
network such as a transformer, and tests neither.

**CIFAR-10, 2020.** One dataset. Earlier drafts of this document said CIFAR-10
and ImageNet; the paper's experiments are CIFAR-10.

**`alpha = 0.6` and `beta = 0.7` are not filed here.** The pullback strength
and the anchor's momentum are algorithm-local constants tuned on this task —
the paper reports `alpha = 0.6` best for `tau >= 2` and `alpha = 0.5` at
`tau = 1` — and [ADR-041](../decisions.d/ADR-041.md) is why they stay in the reading. They are the
standard settings for the method, not, as an earlier draft here said, a
variant for skewed data.

**The construction is EASGD's, and the paper says so.** Pulling local models
toward an anchor is elastic averaging; what [LIT-323](../literature.d/LIT-323.md) adds is the asymmetric
mixing and the observation that EASGD "did not observe and utilize" the
overlap its own structure permits.

## Known implementations

None recorded.
