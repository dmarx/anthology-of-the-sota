---
status: Active
consensus: converged
consensus_note: >-
  One paper for the model, and the field's behaviour is the corroboration:
  every serving stack this record holds a practice from — LIT-112's paged
  attention, LIT-103's chunked prefill, LIT-224's continuous batching — is an
  answer to a bottleneck this paper located. Disaggregated prefill/decode
  serving, now standard, is R1 taken to its conclusion. Nobody has published a
  second cost model because nobody needed one.
title: 'Pick the inference partitioning from where the bottleneck is, and expect it to move between prefill and decode'
version: 1
tags:
- inference-optimization
date: '2026-09-16'
source:
- LIT-110
introduced_by:
- LIT-110
implementations: []
summary: >-
  Pope et al. (2022), [LIT-110](../literature.d/LIT-110.md). Serving is not one workload: prefill
  parallelises over the prompt, decode is serial over the output, and the two
  are bounded by different things. Worse, the binding constraint moves — at
  small batch and short context it is loading the weights, and at large batch
  and long context it is loading the KV cache, which on a 500B model at batch
  512 and 2048 tokens reaches 3 TB, three times the parameters. Choose the
  layout from a cost model of the regime you are in, and re-choose it when the
  regime changes.
---

# SOTA-tmp52mks: Pick the inference partitioning from where the bottleneck is, and expect it to move between prefill and decode

## What to do

**Analyse prefill and decode separately.** Prefill runs in parallel over the
input length; decode runs sequentially over the generated length. They are
different workloads sharing a model, and a configuration tuned for one is
tuned against the other.

**Choose the partitioning layout from a cost model, not from habit or a
search.** Express compute, memory reads and chip-to-chip communication as
functions of batch, context, chip count and model dimensions, and pick the
layout that minimises whatever the application is actually paying for. [LIT-110](../literature.d/LIT-110.md)
shows this is tractable by hand, against prior work's black-box search over
layouts.

**Expect the answer to change.** For prefill, 2D weight-stationary minimises
communication at low tokens per batch and weight-gathered layouts win at high
— and weight-gathered is *inefficient* at low batch, so the crossover is real
in both directions. The paper reaches 76% MFU on the weight-gathered side
where communication overhead becomes negligible.

## Why

**The bottleneck moves, and it moves a long way.** At small batch and short
sequence, time goes to loading the weights. At larger ones — [LIT-110](../literature.d/LIT-110.md) names
2048+ tokens with batch 512+ — it goes to loading the KV cache. These call for
different layouts, and nothing about the model tells you which regime you are
in; only the batch and context do.

**The KV cache can be bigger than the model.** For a 500B+ model with
multihead attention at batch 512 and context 2048 it totals **3 TB — three
times the parameters** — re-read from off-chip memory for every generated
token while the compute core sits idle. That single number is the reason
grouped-query attention, paged attention and chunked prefill all exist, and
it is worth budgeting explicitly rather than discovering.

**And it makes the attention variant a partitioning decision.** With the right
partitioning, multiquery attention's smaller cache supports **32x longer
context** than multihead on the same 64 chips with 30% of memory reserved for
cache. The gain is conditional on partitioning it deliberately; a naive layout
does not collect it.

## What this record already builds on it

Three practices here answer bottlenecks this paper located, and all three
source other papers:

- **[SOTA-113](SOTA-113.md)** (continuous batching, from [LIT-224](../literature.d/LIT-224.md) and [LIT-112](../literature.d/LIT-112.md)) — keeping the
  batch full so the weight-loading cost is amortised.
- **[SOTA-115](SOTA-115.md)** (overlap prefill and decode, from [LIT-103](../literature.d/LIT-103.md)) — a direct response
  to the phase asymmetry in R1.
- **[SOTA-105](SOTA-105.md)** (paged attention, from [LIT-112](../literature.d/LIT-112.md)) — an answer to the 3 TB.

This is not a criticism of those practices; each cites the work that measured
its own mechanism. It is the reason this document exists: the analysis they
share had no entry, which is [DP-007](../../docs/design-principles.md#dp-7)'s shape and was written into [LIT-110](../literature.d/LIT-110.md)'s own
standing section before anybody acted on it.

## Conditions

**TPU v4, 2022.** The structure carries — two phases, moving bottleneck,
layout crossover — and the crossover *points* are measurements of one
interconnect. On a GPU fabric the same analysis applies and the numbers do
not.

**Dense models.** Nothing here covers mixture-of-experts routing, which
changes both the communication pattern and what "loading the weights" costs.

**It predates the responses to it.** Paged attention, chunked prefill,
continuous batching and disaggregated prefill/decode serving all postdate this
paper and all change the constants. What survives is the instruction to model
the regime rather than inherit a configuration.

**The model's accuracy is demonstrated, not bounded.** [LIT-110](../literature.d/LIT-110.md) shows its
predictions tracking the measured frontier; it gives no error analysis, so
treat it as a way to choose between layouts rather than as a performance
predictor.

## Known implementations

None recorded as such. The serving systems this record holds are responses to
this analysis rather than adopters of it, and are counted in `consensus_note`.
