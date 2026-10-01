---
number: 84
status: 'Active'
title: 'Profile-guided optimization for hot paths'
version: 1
tags:
- systems-optimization
date: '2026-08-24'
source:
- LIT-063
introduced_by:
- LIT-063
summary: >-
  Chen et al. (2018), [LIT-063](../literature.d/LIT-063.md) — [ARXIV-1802.04799](https://arxiv.org/abs/1802.04799).
---

# SOTA-084: Profile-guided optimization for hot paths

## Source

Chen et al. (2018), [LIT-063](../literature.d/LIT-063.md) — [ARXIV-1802.04799](https://arxiv.org/abs/1802.04799).

## What "profile-guided" means when the compiler is doing it

TVM's operator level searches a large space of schedules — tiling, unrolling,
vectorisation, memory scope — and the space is far too big to enumerate. The
search is guided by measurement: candidate schedules are run on the target
hardware, and a learned cost model trained on those measurements proposes the
next candidates.

That design is [LIT-063](../literature.d/LIT-063.md)'s, and the recommendation in the form this practice
states it — let measurements on the target device steer a learned search over
schedules — starts there; blackbox autotuning is older, and the paper measures
itself against it. Its explorer runs simulated annealing over predicted costs,
measures each round's most promising batch on the device, and retrains a
gradient-boosted tree model on the results. The model predicts in 0.67 ms on
average, thousands of times faster than a real measurement, and on a ResNet-18
conv2d on a TITAN X it found better configurations much faster than genetic or
random search. End to end, TVM reported 1.2× to 3.8× over frameworks backed by
hand-optimised libraries.

So this is not a human profiling hot paths and rewriting them. It is the
optimiser itself being empirical, and the reason it works is that a cost model
fitted to the real device beats an analytical model of an architecture nobody
fully documents.

## Cost, which is the reason this is not free

Autotuning takes device time — hours, historically, for a network on a new
target — and it produces a result valid for that operator shape on that
device. Change the batch size, the sequence length or the GPU and the tuned
schedule may no longer be the right one, which is why tuned artefacts are
cached and shipped rather than regenerated.

The practical shape of the practice is therefore: tune once per (target,
shape) that matters, cache it, and treat a shape outside the cache as a
performance cliff to know about rather than a failure. That last part is what
makes it a recommendation for a reader rather than a description of a
compiler — an inference stack that quietly hits an untuned shape is slow for a
reason nothing in the model explains.
