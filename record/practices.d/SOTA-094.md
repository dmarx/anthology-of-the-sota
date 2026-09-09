---
number: 94
status: 'Active'
title: 'throughput (energy efficiency) wins out over theoretically optimal sample efficiency'
version: 1
tags:
- model-architecture
date: '2026-08-24'
published: '2022-04-01'
source:
- LIT-069
compared_against:
- SOTA-092
- SOTA-093
summary: >-
  Chowdhery et al. (2022), [LIT-069](../literature.d/LIT-069.md) — [ARXIV-2204.02311](https://arxiv.org/abs/2204.02311).
implementations:
- PaLM
---

# SOTA-094: throughput (energy efficiency) wins out over theoretically optimal sample efficiency

## Source

Chowdhery et al. (2022), [LIT-069](../literature.d/LIT-069.md) — [ARXIV-2204.02311](https://arxiv.org/abs/2204.02311).

## Known implementations

- PaLM

## The one of the three that decides what you run

[SOTA-092](SOTA-092.md) and [SOTA-093](SOTA-093.md) are statements about loss per token seen. This is the
statement that they are the wrong objective on their own: what a training run
spends is accelerator-hours, and a batch size chosen to optimise sample
efficiency can leave the hardware idle enough that the theoretically better
schedule finishes later.

So the practice is an ordering rule between two metrics rather than a setting.
Where they conflict, throughput wins, because the sample-efficiency advantage
is bounded and small while the utilisation penalty is not.

## Where it stops holding

At the extreme it obviously fails: a batch large enough to saturate the
hardware and then keep growing buys nothing per step past the critical batch
size ([SOTA-093](SOTA-093.md)) and still costs memory. The rule is "prefer throughput within
the range where both are defensible", not "maximise batch".

And the underlying quantity is *energy or cost per unit of progress*, not
throughput as such. Those come apart on heterogeneous hardware and under a
schedule that trades precision for speed, where the faster configuration is
not the cheaper one — worth naming, because the title's parenthetical treats
them as the same thing.
