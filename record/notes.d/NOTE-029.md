---
number: 29
status: Read
formerly:
- NOTE-tmp4f54r
paper: LIT-102
title: 'ZeRO++: Extremely Efficient Collective Communication for Giant Model Training'
version: 1
tags:
- distributed-optimization
date: '2026-09-09'
published: '2023-06-01'
summary: >-
  Attacks each of ZeRO's three communication collectives separately — block-quantized weight all-gather, a secondary weight shard held redundantly to trade memory for communication, and an all-to-all quantized gradient reduction replacing reduce-scatter. 4× less communication, up to 2.16× throughput at 384 GPUs.
---

# NOTE-029: ZeRO++: Extremely Efficient Collective Communication for Giant Model Training

## Contribution

ZeRO's bargain is that sharding optimizer state, gradients and parameters
removes memory redundancy at the price of gathering what you need, when you
need it. That price is fine on a fat interconnect with a large per-GPU batch
and ruinous otherwise — on low-bandwidth clusters, or at a scale where the
per-GPU batch is forced small, communication dominates.

ZeRO++ takes the three collectives ZeRO uses and treats each as a separate
problem:

1. **Forward weight all-gather → block quantization.** Send weights at reduced
   precision, quantized per block rather than per tensor.
2. **Backward weight all-gather → data remapping.** Hold a *secondary*
   redundant shard of the weights so the backward gather is local, explicitly
   trading memory back for communication.
3. **Gradient reduce-scatter → `qgZ`, an all-to-all quantized reduction.**
   Replace the collective entirely rather than compressing it.

## Key insight

The third is the real contribution and the one worth stating carefully.
Quantizing a reduce-scatter naively is destructive: reduce-scatter is a
*sequence* of add-then-forward hops, so low-precision values get quantized,
summed, requantized, summed again, and error compounds with the hop count.

The fix is to change the collective's shape, not its precision. An
**all-to-all** exchanges data once, so each value is quantized once and summed
once — the reduction happens in full precision locally after a single
low-precision hop. That is why INT4 survives here and would not survive a
compressed reduce-scatter.

The general form: **when compression fights a collective's structure, replace
the collective.**

## Assumptions

- **Communication, not computation, is the bottleneck.** Explicitly the
  low-bandwidth-cluster and small-per-GPU-batch regime; on a fat interconnect
  with large batches, ZeRO++ has less to buy.
- Quantization error at INT4 is tolerable for gradients when each value is
  quantized exactly once — the paper's engineering, not a general licence.
- Enough spare memory to hold the secondary weight shard. Optimization 2 is a
  trade, and it costs memory ZeRO was designed to free.

## Key results

- **4× reduction in ZeRO's total communication volume.**
- **Up to 2.16× throughput at 384 GPUs.**
- FP16 → **INT4** for the gradient reduction with accuracy preserved, which is
  the claim the all-to-all restructuring exists to make true.
- Block-wise quantization for the weight all-gather, rather than per-tensor —
  finer scaling granularity is what keeps the weights usable.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | ZeRO's communication dominates on low-bandwidth clusters or at small per-GPU batch | strong | the paper's premise, and the regime it measures in |
| C2 | Block quantization makes the weight all-gather affordable | moderate | measured as part of the whole |
| C3 | An all-to-all reduction tolerates INT4 where a compressed reduce-scatter does not | strong | the error-compounding argument is structural, not empirical |
| C4 | 4× communication reduction, 2.16× throughput at 384 GPUs | strong | measured |
| C5 | Trading memory back for communication is worth it in this regime | moderate | one design point |

## Method

Quantize the forward weight all-gather block-wise. Keep a secondary weight
shard so the backward gather is local. Replace gradient reduce-scatter with
`qgZ`: quantize once, all-to-all, reduce locally in higher precision.

## Concepts

- **Per-collective optimization** — three different techniques for three
  collectives, because they have different error and bandwidth profiles.
  The framing is the contribution as much as any one technique.
- **Restructuring a collective to make compression safe** — the transferable
  idea, and it applies wherever a multi-hop reduction meets low precision.
- **Deliberate re-introduction of redundancy** — ZeRO removes redundancy for
  memory; ZeRO++ puts some back for bandwidth. A system's own premise as a
  tunable.

## Connections

Directly downstream of ZeRO and of `LIT-065`, which uses ZeRO-style data
parallelism as one leg of 3D parallelism — this is the work on making that leg
cheaper. Complementary to `LIT-022`: tensor parallelism reduces what must be
communicated by splitting the model; ZeRO++ reduces the cost of what remains.

<!-- inactive-ok-block: SOTA-158 — Proposed, named as a parallel argument rather than relied on -->
The error-compounding argument in C3 is the same shape as the low-precision
reasoning in `SOTA-158` (bound the activation range when training in low
precision): both are about where in a computation a quantization error is
allowed to accumulate.

## Recommendations

- **R1** — When compression fights a collective's structure, change the
  collective rather than the precision. *Topic:* distributed optimization.
  *Strength:* strong, and the most portable thing here.
- **R2** — Count quantization *events* along a data path, not just the bit
  width. A single INT4 hop and four INT4 hops are different problems.
  *Strength:* strong.
- **R3** — Treat a memory-optimizing system's own sharding as a dial that can
  be turned back when bandwidth is scarcer than memory. *Strength:* moderate.
- **R4** — Quantize weights block-wise rather than per-tensor. *Strength:*
  moderate; standard now in inference quantization for the same reason.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice.**
ZeRO++ is a systems optimization for a regime — low-bandwidth clusters, small
per-GPU batches — that the record's practices do not currently address, and
the record does not carry ZeRO itself either.

<!-- inactive-ok-block: SOTA-158, SOTA-159, SOTA-160 — all Proposed, named as the record's low-precision neighbourhood rather than relied on -->
R2 is the one worth keeping visible. The record has low-precision practices
(`SOTA-158`, `SOTA-159`, `SOTA-160`) that reason about bit width and range, and
none that reasons about how many times a value is quantized on its way through
a distributed computation. This paper's central engineering decision turns
entirely on that count.

The document's takeaways — "communication optimization", "memory efficiency",
"distributed training", "scaling improvements" — are four category labels. None
survives contact with the paper: the interesting claim is that a *reduce-
scatter cannot be safely quantized and an all-to-all can*, which is a specific,
checkable, transferable statement.

## Limitations

- 384 GPUs, 2023, and the gains are defined against a bottleneck that a fat
  interconnect removes.
- Accuracy preservation under INT4 gradients is demonstrated for their models
  and budgets; no scaling study of where it breaks.
- Optimization 2 spends memory, which contradicts ZeRO's purpose — the
  conditions under which that is the right trade are not mapped.
- No interaction study with tensor or pipeline parallelism, which is how the
  data-parallel leg actually appears in practice.

## Open questions

- How many quantization events can a gradient survive? C3 says one is fine and
  a reduce-scatter's several are not; the boundary is where the interesting
  engineering is and it is not measured.
- Does the all-to-all restructuring still pay once tensor parallelism has
  already shrunk the data-parallel degree — which is the configuration
  `LIT-065` actually runs?
