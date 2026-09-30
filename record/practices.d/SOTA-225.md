---
number: 225
status: Active
formerly:
- SOTA-tmpjynpv
consensus: unreplicated
consensus_note: >-
  One paper for the crossover. The claim underneath it — that decentralized
  SGD matches centralized convergence while removing the central bottleneck —
  has been built on repeatedly since, including by LIT-254 and LIT-315 in this
  record, which corroborates the regime rather than the measurement.
title: 'Drop the parameter server for gossip once the network is the bottleneck, and measure where that is rather than inheriting a threshold'
version: 1
tags:
- distributed-optimization
date: '2026-09-16'
source:
- LIT-302
introduced_by:
- LIT-302
implementations: []
summary: >-
  Lian et al. (2017), [LIT-302](../literature.d/LIT-302.md). The question is whether a decentralized
  algorithm can ever beat a centralized one, and the answer is that it can —
  not by converging better, since the rates match, but by having no node that
  every other node talks to. The advantage appears where the central node's
  link is the constraint, and the paper establishes that by sweeping bandwidth
  and latency rather than by naming a threshold.
extended_by:
- SOTA-223
- SOTA-226
---

<!-- inactive-ok-file: SOTA-223, SOTA-222 — both Proposed, and
     both named as open questions this practice leaves to other documents:
     which topology to use, and whether the overlap it assumes is filed
     elsewhere. Neither is support. -->

# SOTA-225: Drop the parameter server for gossip once the network is the bottleneck, and measure where that is rather than inheriting a threshold

## What to do

When the parameter server's link is what limits step time, replace it with
decentralized parallel SGD: each worker keeps its own parameters, computes a
local gradient, and averages with its neighbours in a communication graph
rather than with a central node.

Where that point falls is a measurement on your cluster, not a constant.
[LIT-302](../literature.d/LIT-302.md) establishes it by sweeping — one figure over `1/bandwidth` down to 1
Mbps, another over latency out to 140 ms — and its two illustrative
configurations are **ResNet-20 on 7 GPUs at 10 Mbps** and the same at **5 ms
latency**, where decentralized SGD is up to an order of magnitude faster than
a well-optimized centralized implementation.

**This record previously carried "below about 1 Gbps" here and it was wrong.**
That number is not in the paper, and it is a hundred times the bandwidth of
the configuration the paper actually ran. On a 1 Gbps link the paper's sweeps
put both methods in the flat region where the network is not the constraint.

## Why

**The convergence rates match, so the argument is entirely about the
network.** [LIT-302](../literature.d/LIT-302.md)'s theoretical contribution is that D-PSGD attains the same
`O(1/sqrt(nK))` rate as centralized SGD on smooth non-convex objectives, with
linear speedup in the worker count. Given that, choosing between them is a
systems question.

**And as a systems question the parameter server has one bad property**: every
worker's traffic crosses one node's link, so the busiest node's requirement
grows with the worker count. In gossip it does not — each node talks to its
neighbours and the degree is a design choice. The crossover is where that
difference starts to dominate.

**The result holds across implementations**, which is what makes it a claim
about the arrangement rather than about one codebase: CNTK and Torch, up to
112 GPUs, against centralized baselines including the framework's own
AllReduce.

## Conditions

**Homogeneous or mildly heterogeneous data.** The analysis assumes the
workers' distributions are not wildly different. Severe skew is the federated
regime and is not what this measures.

**The topology is not a free choice, and this practice does not make it.**
[LIT-302](../literature.d/LIT-302.md)'s own secondary finding is that a ring is easy and bad — its consensus
rate is poor enough that the paper puts the linear-speedup requirement at
`K = Omega(n^13)`. What graph to use instead is [SOTA-226](SOTA-226.md) and
[SOTA-223](SOTA-223.md), which disagree with each other.

**Overlapping is assumed.** The measured advantage assumes the gossip exchange
runs concurrently with local gradient computation. Serialise them and the
comparison changes; [SOTA-222](SOTA-222.md) is the same assumption in a different
family.

**2017 hardware.** The shape of the argument is the durable part. A crossover
measured on K20s and 10 Mbps links says which way the curve bends, not where
it bends on anything you own.

## Known implementations

None recorded.
