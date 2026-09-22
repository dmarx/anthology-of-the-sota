---
number: 270
status: Active
formerly:
- SOTA-tmp8p02k
consensus: emerging
consensus_note: >-
  The caution rests on three independent measurements from three groups and
  nothing in the record contests it. `emerging` rather than `converged`
  because the instrument half — actually decomposing a run — has one
  implementation at 9M parameters, and because the field's default remains
  to read the curve.
title: 'Do not read a smooth loss curve as evidence of smooth training; decompose it when the answer matters'
version: 1
tags:
- analysis-and-evaluation
- training-optimization
date: '2026-09-20'
source:
- LIT-455
- LIT-453
- LIT-454
introduced_by:
- LIT-455
implementations:
- 'POLCA'
summary: >-
  Kangaslahti et al. (2025), [LIT-455](../literature.d/LIT-455.md), with Cohen et al.
  [LIT-453](../literature.d/LIT-453.md) and Kunin et al. [LIT-454](../literature.d/LIT-454.md) — the curve
  time-averages oscillation, sums over differently-timed abrupt transitions,
  and reads flat while the weights still travel. Smoothness is what many
  breakthroughs look like added up, so it is not evidence about the training.
explained_by:
- THEORY-031
---

# SOTA-270: Do not read a smooth loss curve as evidence of smooth training; decompose it when the answer matters

## Source

Kangaslahti et al. (2025), [LIT-455](../literature.d/LIT-455.md) — [ARXIV-2506.15872](https://arxiv.org/abs/2506.15872). The
decomposition and the negative control.

Cohen et al. (2024), [LIT-453](../literature.d/LIT-453.md) — [ARXIV-2410.24206](https://arxiv.org/abs/2410.24206), and Kunin et al.
(2021), [LIT-454](../literature.d/LIT-454.md) — [ARXIV-2107.09133](https://arxiv.org/abs/2107.09133). The other two collapses; the
caution rests on all three and not on any one.

## The free half and the expensive half

**The free half is what not to conclude.** A smooth loss curve is consistent
with many abrupt transitions happening at different times in different parts
of the data, because that is what their sum looks like. A flat stretch is
consistent with a component being built that the loss cannot see until it is
finished. A flat tail is consistent with the weights still travelling. None
of those readings costs anything to hold, and holding them changes how a run
gets debugged: *"the loss is smooth so nothing interesting is happening"* is
an inference the curve does not support.

**The expensive half is finding out.** POLCA decomposes the change in loss
per example *and* along directions in a low-rank basis built from the loss
Hessian at successive checkpoints. Both decompositions are needed — one
example can depend on several breakthroughs, and concepts arriving together
merge their clusters unless the directions separate them.

The validation is why this is worth having rather than plausible: on
synthetic arithmetic, clustering the raw per-example loss curves recovers
digit positions and misses the skill of carrying, at a maximum carry fraction
of 0.514 — chance. Clustering the POLCA curves recovers both.

## What the caution is made of

Three independent collapses, measured by three groups over four years, none
citing the others ([THEORY-031](../theory.d/THEORY-031.md)):

- **Time-averaging.** At the edge of stability the optimizer oscillates, and
  the plotted path is the average of one that is not smooth.
- **Summation over data and directions.** The result above.
- **Saturation before the weights stop.** Distance travelled keeps growing as
  a power law long after the curve flattens.

The record has a worked case of the second already: [THEORY-028](../theory.d/THEORY-028.md) shows one
plateau to be an attention recall circuit under construction, established by
patching the circuit in and watching the plateau vanish. That was one
transition made visible by intervention; this says the population is large
and supplies a way to look without one.

## Why `Active` when the instrument is small-scale

Because the two halves have different evidential burdens and only one of them
is load-bearing. The caution follows from three measurements and costs
nothing to adopt; the worst case of believing it is that somebody
investigates a run they would otherwise have assumed fine.

The decomposition is a genuine method with a clean negative control, and it
is demonstrated at 9M parameters because that is what per-example POLCA at
fine intervals can afford. `emerging` rather than `converged` says exactly
that.

## Conditions

**The measurement does not obviously scale.** Checkpoints, Hessian-vector
products at each, and a per-example forward pass at every interval. The
source chose its model size for feasibility and says so. Nothing here
suggests this as instrumentation for a frontier run.

**Absence of visible structure is not evidence of hidden structure either.**
The account says the curve cannot settle the question, in both directions. A
reader who takes this as licence to assume something interesting is always
being concealed has inverted it rather than understood it.

**The three legs have different scopes and are not three views of one
experiment.** Full-batch at the edge of stability; a 9M model; the limiting
regime at 2021 scale. They agree on the conclusion, which is what the caution
rests on, and they do not compose into a single mechanism.

**"Frequently" is unquantified.** How many hidden transitions a real
pretraining run contains is the obvious question and is exactly what the
method's cost prevents answering.

**One skill, one direction** is an idealisation the clustering leans on, and
the assumption that synchronised loss change implies a shared skill is
validated where ground truth exists and interpretive elsewhere.

## Known implementations

- POLCA, at 9M parameters, on synthetic arithmetic and natural language.
