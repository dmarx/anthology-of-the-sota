---
number: 349
status: Active
formerly:
- SOTA-tmp7wtf2
title: 'Before crediting a graph transformer with long-range gains, retune the message-passing baselines under the same budget, including an MLP prediction head, positional encodings and input feature normalization'
version: 1
tags:
- analysis-and-evaluation
- graphs-and-networks
- model-architecture
date: '2026-09-23'
source:
- LIT-579
introduced_by:
- LIT-579
consensus: unreplicated
consensus_note: >-
  One group's re-evaluation on one benchmark. It retunes the transformer
  too, and the gap closes on two datasets and persists on two others, which
  makes it a careful result, not a one-sided one. Whether later
  graph-transformer papers adopted the retuned baselines has not been
  assessed here.
implementations: []
summary: >-
  Tönshoff et al. (2023), [LIT-579](../literature.d/LIT-579.md) — the Long-Range Graph Benchmark's
  case that graph transformers are needed rested partly on untuned
  message-passing baselines. With a basic sweep inside the same
  500k-parameter budget, GCN beats GPS on both Peptides tasks. Most of the
  gain is from replacing a linear prediction head with a 2-layer MLP.
  Normalizing input features lifts every model on the superpixel tasks,
  where GPS still leads. Tune both sides before attributing a gap to
  attention.
---

# SOTA-349: Before crediting a graph transformer with long-range gains, retune the message-passing baselines under the same budget, including an MLP prediction head, positional encodings and input feature normalization

## Source

Tönshoff et al. (2023), [LIT-579](../literature.d/LIT-579.md). Read as [NOTE-317](../notes.d/NOTE-317.md). The general
form is [SOTA-350](SOTA-350.md).

## The practice

The recommendation is [LIT-579](../literature.d/LIT-579.md)'s. Tönshoff et al. re-ran the Long-Range Graph
Benchmark with message-passing baselines tuned as carefully as the
transformer, in the same 500k-parameter budget. Retuned GCN went from 0.593
to 0.686 AP on Peptides-func and from 0.350 to 0.246 MAE on Peptides-struct,
past GPS at 0.653 and 0.251, and the MLP head alone accounts for most of that
gain. On PascalVOC-SP GPS still leads after tuning (F1 0.444 against
GatedGCN's 0.388), and normalization is at least half of most models' gain
there.

The handicap started in the benchmark and travelled. The Long Range Graph
Benchmark ([LIT-844](../literature.d/LIT-844.md)) sized each baseline to the budget at a fixed depth
and describes no sweep; its Peptides gap (best transformer AP 0.644 against
0.607, MAE 0.253 against 0.336) is the one [LIT-579](../literature.d/LIT-579.md) closed. GPS
([LIT-842](../literature.d/LIT-842.md)) and Exphormer ([LIT-821](../literature.d/LIT-821.md)) then copied those baseline rows
unchanged into their own LRGB tables while tuning their own models one
hyperparameter at a time, so each paper's lead over message passing was
measured against the same untuned configurations. Graphormer
([LIT-843](../literature.d/LIT-843.md)), on other benchmarks, compared against leaderboard models
tuned by their authors; its comparisons are confounded by model size and
pre-training instead.

- **Rerun the baselines; do not copy the benchmark's table.** A copied row
  carries whatever configuration produced it into every later comparison
- **Give the MPGNN an MLP readout.** A linear head on pooled node states was
  the largest single handicap on Peptides
- **Treat positional or structural encodings** (none, LapPE, RWSE) as a
  hyperparameter for every model, not only the transformer
- **Normalize input features per channel.** The superpixel datasets mix
  scales across orders of magnitude, and normalizing helped every model and
  cut variance
- **Tune depth, dropout and the other main hyperparameters** for baselines
  and proposal alike, under the same parameter budget
- **Check the metric's implementation against its definition.** The
  benchmark's code computed raw MRR instead of the filtered MRR it
  specified

## Conditions

- **The gap closed on Peptides and did not close on PascalVOC-SP or COCO-SP.**
  Long-range benefits of attention are dataset-specific, not absent
- **500k-parameter models**, the benchmark's budget. Whether the closure
  holds for larger models is not tested
- **Tuning the transformer too matters.** GPS gained 18% and 13% F1 on the
  superpixel sets from the same sweep, so retuning only the baselines would
  have understated it there
