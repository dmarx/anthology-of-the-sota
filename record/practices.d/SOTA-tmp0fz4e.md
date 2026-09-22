---
status: Proposed
promote_when: >-
  A group other than Qwen ablates n-gram table placement (one layer against
  the same budget split over several, early against deep) and the trade
  against expert parameters, and reports downstream benchmarks with seed
  variance, not loss alone. The present evidence is one team, one scale and
  single runs, with most placement differences under a point. A second paper
  that adopts one early table without ablating it does not count.
title: 'Add n-gram embedding memory as one table read early in the network, on top of the expert budget rather than in place of experts'
version: 1
tags:
- model-architecture
- systems-optimization
date: '2026-09-22'
source:
- LIT-152
introduced_by:
- LIT-152
consensus: unreplicated
implementations:
- Qwen3.8-Flash-Next
summary: >-
  Qiu et al. (2026), [LIT-152](../literature.d/LIT-152.md) — Qwen3.8-Flash-Next's ablations. One n-gram
  embedding table at layer 2 takes loss from 1.585 to 1.541 and the benchmark
  average from 45.44 to 47.94. Splitting the same table across two layers
  buys nothing, and no depth clearly wins. Trading experts for table
  parameters at a fixed total lowers loss slightly and moves no downstream
  benchmark. Grown on top of the budget, the table keeps lowering loss after
  downstream accuracy has flattened. Layer 2 is a systems choice: the
  host-memory prefetch overlaps layer 1.
---

# SOTA-tmp0fz4e: Add n-gram embedding memory as one table read early in the network, on top of the expert budget rather than in place of experts

## Source

Qiu et al. (2026), [LIT-152](../literature.d/LIT-152.md) — §2.3, Tables 7–9. All runs at 300 tokens per
active parameter.

## The practice

An n-gram embedding layer uses the short n-grams ending at each token as
keys into a large table, and adds the retrieved vectors to that token's
representation. It adds parameters without adding per-token FLOPs. Because
the addresses depend only on the input ids, the table can be kept in host
memory and prefetched. Qwen3.8-Flash-Next holds 51B parameters this way,
next to a 125B-A6B backbone.

The report's ablations support three instructions, and they are the whole
practice.

**Use one table, and put it early.** At a fixed table budget (Table 7):

| placement | loss | benchmark avg |
|---|--:|--:|
| no n-gram table | 1.585 | 45.44 |
| layer 1 | 1.541 | 47.30 |
| **layer 2** | **1.541** | **47.94** |
| layer 15 | 1.543 | 47.37 |
| layer 25 | 1.541 | 47.40 |
| layers 2 + 15 | 1.541 | 47.01 |
| layers 2 + 25 | 1.540 | 47.75 |

Adding a table is worth about 2.5 points of average. *Where* it goes is worth
well under one point, and the report reads that correctly: "No single depth
regime consistently dominates", and "a single N-gram embedding layer is
sufficient". The ordering was the same under full attention and under
Gated DeltaNet. **The reason for layer 2 is not quality.** It lets the
host-memory fetch overlap the first layer's compute, so the table costs no
latency.

**Do not pay for it with experts.** Holding the total parameter count fixed
and removing experts to fund the table (Table 8), loss is lowest at a 10×
vocabulary (25% of parameters): 1.197 against 1.202. That matches the
allocation sweet spot the report attributes to earlier work. Out-of-domain
perplexity barely moves, and the report finds "no clear improvement over
the MoE-only baseline" downstream. The table and the experts are not
substitutes. The table is capacity you add, not capacity you reallocate.

**Expect loss to overstate the gain as the table grows.** Adding table
parameters on top (Table 9), loss falls steadily from 20× to 200× of the
base vocabulary (1.553 → 1.526). MMLU is flat from 50× on, GSM8K *falls*
from 65.09 to 62.96, and C-Eval rises from 71.75 to 74.94. Past a modest
size, a bigger table buys mainly knowledge-heavy and Chinese-language
benchmarks. Choose its size on the benchmarks you care about, not on loss.

## Conditions

- **An MoE backbone at 300 tokens per active parameter.** The expert
  trade-off is measured against experts specifically. Against a dense
  model's width it is untested
- **Single runs.** The report gives no seed variance. Differences of 0.003
  in loss and one point of average, which is all that separates the
  placements, are the size single-seed noise often reaches
- **The table trains on Adam with weight decay off**, while the key/value
  projection that reads it trains on Muon with the rest of the matrices
  (§3.1). The report gives no reason for this. A plausible one is that
  decoupled weight decay shrinks every row at every step, including the
  many rows no batch reads
- **Parameter-efficiency tricks did not help.** Token normalization to
  compress the vocabulary, uneven allocation across n-gram orders and
  frequency-based partitioning were all tried with "no consistent
  performance gains"

## What this does not say

**It is not about per-layer embeddings.** Gemma 3n ([LIT-tmp5bcs0](../literature.d/LIT-tmp5bcs0.md)) reads a
small *token*-keyed table at *every* layer, and ships it on device for the
same off-accelerator reason. The two-layer result here is about splitting
an *n-gram* table's fixed budget. It does not test Gemma's design and does
not argue against it.

**It does not establish n-gram memory against the alternatives.** The
report compares table placements and table sizes with each other and
against no table. It does not compare against the same parameters spent on
width, depth or a larger unigram vocabulary.

## Consensus

`unreplicated`, for the instruction as stated: only one group has published
the placement and budget ablations. The broader idea, capacity in
deterministically addressed tables held off the accelerator, has several
independent adopters. Google ships a token-keyed version (Gemma 3n, Gemma 4
E2B/E4B), RWKV-8 has DeepEmbed, and the report cites Cheng et al.'s
conditional-memory lookup for the n-gram form and for offloading. That is
adoption and not evidence for this practice ([DP-005](../../docs/design-principles.md#dp-5)), and none of those
sources is in the record apart from Gemma 3n's documentation.

## Known implementations

- Qwen3.8-Flash-Next: one n-gram table at layer 2, 51B parameters,
  prefetched from host memory
