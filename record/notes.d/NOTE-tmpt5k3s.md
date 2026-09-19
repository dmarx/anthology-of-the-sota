---
status: Read
paper: LIT-004
title: 'Training Deep Nets with Sublinear Memory Cost'
version: 1
date: '2026-09-19'
summary: >-
  Two contributions, and the famous one is the second. First, treat memory
  allocation over the computation graph as a compiler problem — liveness
  analysis, in-place operations, memory sharing. Then, on top of that, drop
  most intermediate feature maps and recompute them segment by segment during
  the backward pass. Dividing an n-layer chain into sqrt(n) segments costs
  sqrt(n) memory for one extra forward pass; the extreme of the same analysis
  is log n memory for n log n extra forward computation.
---

# NOTE-tmpt5k3s: Training Deep Nets with Sublinear Memory Cost

## Contribution

A systematic method for trading computation against memory during training,
stated over the computation graph rather than for one architecture. The paper
separates two things that are usually conflated: **allocation** (what can
share memory, what can be done in place) and **rematerialization** (what to
drop and recompute). The first is framed explicitly as a compiler analogy —
*"memory allocation in deep networks is similar to register allocation in a
compiler"* — and the second is built on top of it.

## Key insight

The intermediate feature maps dominate training memory, not the parameters,
*"as the size of the parameters are relatively small comparing to the size of
the intermediate feature maps in many common deep architectures"*. And a
feature map is cheap to reproduce: it is a deterministic function of an
earlier one. So storage is optional, and what you actually choose is a
**segmentation** — where to put the boundaries you do keep.

## Concepts

- **Segment** — a run of layers whose output is kept and whose interior is
  dropped and recomputed during backpropagation
- **Rematerialization** — recomputing a dropped intermediate by running
  forward from the closest recorded result
- **Liveness / recycling** — the allocation half: a counter over a
  topological traversal marks when an output is dead, so its memory can be
  reused, computed statically before execution rather than by a runtime
  garbage collector

## Assumptions

- **Feature maps, not parameters, are the constraint.** Stated, and true of
  the architectures of the day; it is what makes the whole trade worth making
- **Recomputation is cheap relative to memory pressure.** The method buys
  nothing if you are compute-bound
- **The graph can be divided into segments.** Alg. 1 is for a linear chain;
  the generalization needs a user-specified function to identify the
  boundaries, which the paper acknowledges as a usability cost
- **Determinism.** Recomputing must reproduce what was dropped — which the
  paper does not dwell on and which is where randomness (dropout, sampling)
  needs care in practice

## Key results

- **O(sqrt(n)) memory for feature maps to train an n-layer network, at
  double the forward-pass cost** — that is, one extra forward pass per
  minibatch. *Holds when:* the network divides into segments; the accounting
  is over feature maps.
- **O(log n) memory with O(n log n) extra forward computation**, as the
  extreme of the same analysis. The point is that the trade is a curve.
- **1,000-layer deep residual network: 48G → 7G, +30% running time**, on
  ImageNet. *Holds when:* that architecture and that framework (MXNet, static
  allocation).
- **Significant reductions also on recurrent networks over very long
  sequences** — the case that transfers to long-context language models.
- **It composes with the alternatives.** CPU/GPU swapping and model
  parallelism are *"orthogonal approaches and can be used together"*, and
  this method *"does not need additional communication over PCI-E"*, so it
  does not compete with the interconnect that data and model parallelism are
  already using.

## Limitations

- **Two drawbacks the paper names about its own simple algorithm**: the user
  must divide the graph by hand and write a custom training loop, and doing
  so forfeits the allocation optimizations of the first half. The general
  gradient-graph construction exists to fix both, and needs the user to
  specify the boundary function
- **The 30% figure is one architecture in one framework.** It is a good
  anchor and not a constant
- **Nothing about numerics.** Recomputation under mixed precision, and
  reproducing dropout masks, are both live concerns and neither is discussed
- **2016 hardware and framework assumptions** throughout; the accounting
  predates the memory hierarchies that make `SOTA-087`'s HBM-traffic argument
  the sharper one for attention specifically

## Connections

`SOTA-087` recommends recomputation for attention, and argues it from HBM
traffic via `LIT-074` — a mechanism this paper does not have and a better
argument in that narrow setting. The general rule filed from here is the
earlier and broader member of the same line. `SOTA-017`, `SOTA-019` and
`SOTA-031` all do memory accounting that assumes this trade is being made.

The allocation half — liveness, in-place, sharing — has no practice and
probably should not: it is what a framework does for you, and the record's
`distributed-optimization` entries are about decisions a person makes.

## Bearing on the record

This reading is what `#85` said the note needed, and it changes one thing
about the practice filed from it. The abstract supports the rule; the body
adds the **conditions** — that the segmentation must exist, that the win is
over feature maps specifically, that it composes with swapping and model
parallelism without touching the interconnect, and that the 30% is one
architecture rather than a constant. It also supplies the limit the practice
should not over-claim: this is a 2016 accounting, and for attention
`SOTA-087`'s argument is better.
