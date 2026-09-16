---
status: Read
paper: LIT-110
title: 'Efficiently Scaling Transformer Inference'
version: 1
date: '2026-09-16'
summary: >-
  An analytical model of where inference time actually goes, used to pick a
  partitioning rather than searching for one. Its organising finding is that
  prefill and decode have different performance characteristics and must be
  analysed separately, and that the dominant cost moves — weights at small
  batch and short context, the KV cache at large. On PaLM 540B across 64 TPU
  v4 chips: 29 ms per token at low batch with int8 weights, 76% MFU at large
  batch, and 32x longer context from multiquery attention once the
  partitioning is right.
---

# NOTE-tmp9mp08: Efficiently Scaling Transformer Inference

## Contribution

A cost model for generative Transformer inference, simple enough to reason
with by hand, that selects a multi-dimensional partitioning layout from the
application's requirements — as against the black-box search over layouts that
prior work used. Combined with low-level optimizations it sets a new Pareto
frontier on latency against model FLOPS utilization for 500B+ models, beating
the FasterTransformer benchmarks.

## Key insight

Inference is not one workload. **Prefill parallelises over the input length;
decode is sequential over the generated length**, so the two have different
bottlenecks and want different partitionings — and the right layout for either
one moves as batch size and context length grow. A single configuration chosen
for "inference" is a configuration chosen for one point on that surface.

## Assumptions

- TPU v4 slices, with their specific interconnect topology and memory
  hierarchy. The model is analytic but its constants are this hardware's.
- Dense decoder-only Transformers at 500B+ scale; PaLM 540B throughout.
- Communication cost is estimable from the layout, which is what makes the
  model tractable and is where it would break on a less regular fabric.
- 30% of total memory reserved for the KV cache in the context-length results.
- Weights quantized to int8 for the low-latency figures; the model itself is
  not quantization-specific.

## Key results

- **Prefill and decode are analysed separately, on purpose.** Prefill runs in
  parallel over `L_input`; decode runs sequentially over `L_gen`.
  *Holds when:* any autoregressive generation with a non-trivial prompt.
- **The dominant cost moves with batch and context.** At small batch and
  sequence length, loading the *weights* dominates. At larger ones — the paper
  names 2048+ tokens with batch 512+ — loading the *KV cache* dominates.
  *Holds when:* the memory-bandwidth-bound regime this paper is about.
- **The optimal layout switches.** 2D weight-stationary minimises
  communication at low tokens per batch; weight-gathered layouts win at high,
  reaching **76% MFU** where communication overhead becomes negligible. The
  weight-gathered layouts are *inefficient* at low batch.
  *Holds when:* prefill, batch from 2048 tokens to 1M tokens; TPU v4.
- **Multiquery attention buys 32x context.** With appropriate partitioning,
  MQA's lower KV-cache footprint enables up to **32x larger context lengths**
  than multihead, on PaLM 540B across 64 chips.
  *Holds when:* 30% of memory reserved for KV cache; the optimised MQA
  partitioning, not a naive one.
- **The KV cache can exceed the model.** For a 500B+ model with multihead
  attention at batch 512 and context 2048, the KV cache totals **3 TB — three
  times the size of the parameters** — and must be re-read from off-chip
  memory for every generated token, with the compute core essentially idle.
  *Holds when:* multihead attention; this is the number MQA and paged
  attention exist to attack.
- **Headline configuration**: 29 ms per token at low batch with int8 weight
  quantization, and 76% MFU during large-batch prefill, at 2048 context on
  PaLM 540B across 64 TPU v4 chips.
  *Holds when:* that exact configuration.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Prefill and decode have different performance characteristics and require separate analysis and, often, different partitionings. | strong | Structural argument plus separate Pareto frontiers measured for each phase. |
| C2 | The communication-optimal partitioning switches from 2D weight-stationary to weight-gathered as tokens per batch grows. | strong | Analytical model plus measured MFU across batch sizes from 2048 to 1M tokens. |
| C3 | Multiquery attention enables up to 32x longer context than multihead at equal memory, given the right partitioning. | strong | Table 1, PaLM 540B on 64 chips with 30% memory reserved for KV cache. |
| C4 | A simple analytical model suffices to select layouts, without black-box search. | moderate | Demonstrated on one hardware family; the claim that it generalises is not tested. |

## Method

**An analytic cost model over partitioning layouts.**

Enumerate the layouts — 1D weight-stationary, 2D weight-stationary,
weight-gathered variants — and for each express compute, memory-read and
chip-to-chip communication time as functions of batch, context, chip count and
model dimensions. Choose the layout minimising the metric the application
cares about: latency, or cost per token, or context supported.

- Separate models for prefill and decode
- Multi-axis tensor partitioning rather than one-dimensional sharding
- Multiquery attention to shrink the KV cache
- int8 weight quantization for the latency frontier

## Concepts

- **Model FLOPS utilization (MFU)** — observed throughput over the theoretical
  peak. The efficiency axis this paper trades against latency.
- **Weight-stationary vs weight-gathered** — whether weights stay sharded and
  activations move, or weights are gathered to the chips that need them. The
  crossover between them is the paper's central practical result.
- **Prefill and decode** — the two phases, named here in the sense the serving
  literature has used since.
- **The three application regimes** — lowest latency (more chips, smaller
  batch, worse MFU, higher cost per token); long context (KV cache dominates);
  offline throughput (larger batch, better MFU).

## Connections

**Related.**

- [LIT-112](../literature.d/LIT-112.md) (PagedAttention) and [LIT-103](../literature.d/LIT-103.md) (SARATHI) — both attack costs this
  paper models: the KV cache's footprint and the prefill/decode imbalance.
- [LIT-024](../literature.d/LIT-024.md) (multi-query attention) — the mechanism whose payoff this paper
  quantifies at scale.

## Recommendations

- **R1** — Analyse prefill and decode separately and expect them to want
  different configurations.
  *Topic:* serving configuration · *Strength:* strong · *When:* Any
  latency-sensitive autoregressive serving.
- **R2** — Choose the partitioning layout from a cost model of the regime you
  are in, and re-choose it when batch size or context changes materially.
  *Topic:* partitioning · *Strength:* strong · *When:* Multi-chip serving of a
  model too large for one device.
- **R3** — Budget the KV cache explicitly against the parameters; at long
  context with multihead attention it is the larger of the two.
  *Topic:* memory budgeting · *Strength:* strong · *When:* Long context, large
  batch.
- **R4** — Use multiquery (or grouped-query) attention when context length is
  the binding constraint, and partition it deliberately.
  *Topic:* attention variant · *Strength:* strong · *When:* Context length is
  what limits the deployment.

## Bearing on the record

This is the analytical backing the serving practices here have been standing
on without citing. [SOTA-113](../practices.d/SOTA-113.md) (continuous batching) and [SOTA-115](../practices.d/SOTA-115.md) (prefill/decode
overlap) are both answers to imbalances this paper models, and both source
other work. [SOTA-tmp52mks](../practices.d/SOTA-tmp52mks.md) is what this note supports directly. R3 and R4 are
the quantitative case for practices the record already holds about attention
variants and cache layout.

## Limitations

- TPU v4. The structure of the argument carries; the crossover points are
  measurements of one interconnect, and the paper does not claim otherwise.
- Dense models. Nothing here addresses mixture-of-experts routing, which
  changes both the communication pattern and the weight-loading cost.
- 2022. It predates paged attention, continuous batching and the
  disaggregated prefill/decode deployments that are now common — all of which
  are responses to what it measured, and none of which it evaluates.
- The analytical model's accuracy is demonstrated rather than bounded; there
  is no error analysis against the measured frontier.

## Open questions

- How do the crossover points move on GPU fabrics, where the communication
  topology is less regular than a TPU slice's?
- Does the layout-switching result survive disaggregation, where prefill and
  decode run on separate pools and can be partitioned independently by
  construction?
