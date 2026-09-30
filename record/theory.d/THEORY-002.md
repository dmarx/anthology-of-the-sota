---
number: 2
status: Proposed
formerly:
- THEORY-tmp6auqn
promote_when: >-
  A demonstration at language-model scale in which the winning subnetwork is
  rewound to its ORIGINAL initialization rather than to an early-training
  checkpoint. Rewinding to step k is a different claim and satisfies nothing
  here: it is what later work had to fall back on, and the fallback is the
  evidence against.
title: 'A dense network contains a sparse subnetwork that matches its accuracy when trained from the same initialization'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-15'
source:
- LIT-019
summary: >-
  Frankle and Carbin (2018), [LIT-019](../literature.d/LIT-019.md) — the lottery ticket hypothesis. A
  randomly-initialized dense network contains a subnetwork that, trained
  alone from the same initial values, matches the full network in at most
  the same number of steps. The reset is the claim; the same structure
  re-initialized randomly does not do it.
corrected_by:
- THEORY-004
---

# THEORY-002: A dense network contains a sparse subnetwork that matches its accuracy when trained from the same initialization

## Source

Frankle and Carbin (2018), [LIT-019](../literature.d/LIT-019.md).

## What was actually shown

Iterative magnitude pruning, then a rewind. Train the dense network, remove
the smallest-magnitude weights, restore the survivors to the values they were
*initialized* with, and train that sparse network alone. It reaches the dense
network's accuracy in at most the same number of iterations, at 10–20% of the
parameters, on the paper's vision benchmarks — sometimes faster and sometimes
generalizing better.

The control is what makes it a finding rather than a pruning result. Keep the
same sparse structure and re-initialize it randomly, and it does not work. So
what the dense run produced is not a better architecture; it is a *pairing* of
a structure with particular initial values, and neither half suffices.

## Why this is `Proposed` rather than `Active`

The result reproduces and is not in dispute on the networks it was run on.
What is unsettled is the scope, and the evidence against generality has a
specific shape: at larger scale, rewinding to initialization stopped working
and later work rewound to an early-training checkpoint instead. That is a
weaker claim wearing the same name — if the information has to be collected
over the first k steps, it was not in the initialization.

[THEORY-004](THEORY-004.md) is a second reason for the caution, and it is about what the
result means rather than where it holds.

## What this does not say

It does not say you can find the ticket without the dense run. The procedure
needs a full dense training pass before it produces anything, which is why
[LIT-019](../literature.d/LIT-019.md) carries no practice: as an instruction it reads "train the model,
then train a smaller one."

It does not say sparse structures are independently good architectures. That
is the reading the phrase "winning ticket" invites, it is the one
[THEORY-004](THEORY-004.md) takes apart, and the random-reinitialization control in this
very paper already argues against it.
