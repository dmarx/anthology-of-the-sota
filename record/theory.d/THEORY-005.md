---
number: 5
status: Proposed
formerly:
- THEORY-tmptabiw
promote_when: >-
  The co-activation partition measured by a group unconnected to Zhang et al.,
  or measured inside a trained mixture of experts rather than inside a dense
  model. Both findings here come from one lab's line of work, and a third
  paper from that line satisfies nothing.
title: 'Dense feed-forward layers are already mixtures of experts, and pre-training settles the partition before the neurons'
version: 1
tags:
- model-architecture
date: '2026-09-15'
source:
- LIT-226
- LIT-228
explains:
- SOTA-150
- SOTA-149
summary: >-
  Zhang et al. (2021, 2023), [LIT-226](../literature.d/LIT-226.md) and [LIT-228](../literature.d/LIT-228.md) — a trained dense
  FFN uses a tiny fraction of its neurons per input, the co-activating
  neurons partition into functional experts that can be recovered post hoc
  with the same parameters, and through pre-training the partition stabilizes
  earlier than the neurons in it. A mixture of experts makes explicit a
  structure dense training arrives at anyway.
---

# THEORY-005: Dense feed-forward layers are already mixtures of experts, and pre-training settles the partition before the neurons

## Source

Zhang et al. (2021), [LIT-226](../literature.d/LIT-226.md), and Zhang et al. (2023), [LIT-228](../literature.d/LIT-228.md).

## What was actually shown

Three results, and the third is the one that changes how the first two read.

**The dense layer is sparse in use.** Most inputs activate only a tiny ratio
of an FFN's neurons. Density is a property of how the parameters are stored
and run, not of how many of them any given token needs.

**The sparsity has structure, and the structure is recoverable.**
[LIT-226](../literature.d/LIT-226.md) partitions a *trained* FFN's parameters into experts by which
neurons co-activate, bolts a router on, and changes nothing else — same
parameters, conditionally used. 10–30% of FFN parameters per input retains
over 95% of performance. [LIT-228](../literature.d/LIT-228.md) then supplies the causal half:
the clusters are functionally specialized, and perturbing one damages the
corresponding function rather than degrading the model generally.

**The partition comes first.** Tracking modularity across pre-training,
[LIT-228](../literature.d/LIT-228.md) finds the modular structure stabilizes at an early stage —
*faster than the neurons themselves stabilize*. The reading offered is that
transformers "first construct the modular structure and then learn
fine-grained neuron functions."

## What this explains

It is the account under [SOTA-150](../practices.d/SOTA-150.md). Making the feed-forward layers a sparse
mixture of experts is usually argued for on the economics — total parameters
stop determining per-token compute — which says why you would *want* it to
work and not why it *does*. This says why it does: the architecture is not
imposing a constraint the model must be coaxed into satisfying, it is
declaring one dense training arrives at on its own. The router replaces an
implicit selection with an explicit one.

It also bears on [SOTA-149](../practices.d/SOTA-149.md), and more sharply than on [SOTA-150](../practices.d/SOTA-150.md). That practice's
diagnosis is that conventional top-K-of-N routing fails to deliver expert
specialisation, and that fine segmentation into many small experts fixes it.
If specialisation in a dense model is a property of *neuron-level* clusters,
then a handful of large experts is the wrong granularity for the structure
that is actually there, and fine segmentation is not a tuning choice but a
match to it.

## What this has to do with the lottery ticket

<!-- inactive-ok-block: THEORY-002 — Proposed, and cited here for the
     shape it shares with this account rather than as a settled claim. -->
It rhymes with [THEORY-002](THEORY-002.md) and [THEORY-004](THEORY-004.md), and the ways it does not
are worth stating, because the analogy is easy to take too far.

What they share is the direction of the arrow: **the dense run is what
produces the sparse structure.** Neither line gives you the structure without
paying for the dense training first, and in both the sparse object is
recovered from a completed run rather than discovered independently.

They differ in what is sparse. A lottery ticket is *static, weight-level*
sparsity — pruned weights are gone, one subnetwork survives, and the claim
turns on rewinding it to its original values. This is *conditional,
activation-level* sparsity in a trained network: nothing is removed, the
subnetwork is different for every input, and no rewind is involved.

<!-- inactive-ok-block: SOTA-148 — Proposed, and named for what its
     existence demonstrates rather than as a settled recommendation: a
     mechanism that keeps every expert loaded is evidence that no expert is
     meant to go unused. -->
The difference resolves something the two lines would otherwise leave
contradictory. [THEORY-004](THEORY-004.md)'s account of why sparse-from-scratch
underperforms is poor gradient flow at initialization — yet mixtures of
experts train from scratch and work. The reason is that a mixture of experts
is not sparse in the sense that argument is about: no parameter is removed,
every expert is dense internally and receives full gradients on the tokens
routed to it, and load balancing ([SOTA-148](../practices.d/SOTA-148.md)) exists precisely to keep any
expert from going unused. What is sparse is FLOPs per token, not parameters.
That reading is this record's, drawn from the two accounts, and is not a claim
either paper makes.

## What this does not say

It does not say the emergent partition is the partition an architect should
impose. Both papers measure *dense* models; neither measures the experts of a
trained MoE, and "the structure is MoE-shaped" is a weaker statement than "the
shape we chose is the structure."

It does not say a converted model equals a natively sparse one. [LIT-226](../literature.d/LIT-226.md)
is a post-hoc conversion evaluated on inference cost, with no comparison
against a model trained sparse from the start.

And both results come from one group. That is why this is `Proposed` rather
than `Active`: the finding is specific and well-measured, and the record has
one lab's word for it.
