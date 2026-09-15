---
number: 103
status: Read
formerly:
- NOTE-tmp71f2s
paper: LIT-027
title: 'ZeRO: Memory Optimizations Toward Training Trillion Parameter Models'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
summary: >-
  Data parallelism wastes memory by replicating all model states on every
  device; partitioning these states instead of replicating them yields linear
  memory reduction with device count while keeping communication volume nearly
  identical to standard data parallelism.
---
# NOTE-103: ZeRO: Memory Optimizations Toward Training Trillion Parameter Models

## Contribution

ZeRO (Zero Redundancy Optimizer) eliminates memory redundancy in data-
parallel training by partitioning optimizer states, gradients, and
parameters across devices instead of replicating them. This enables training
models with 8x more parameters and 10x higher throughput than state-of-the-
art, demonstrated on 170B parameter models on 400 GPUs.

## Key insight

Data parallelism wastes memory by replicating all model states on every
device; partitioning these states instead of replicating them yields linear
memory reduction with device count while keeping communication volume nearly
identical to standard data parallelism.

## Assumptions

- Data-parallel training with homogeneous workers sharing the same model
  replica pattern.
- Adam optimizer is used, giving the standard 16 bytes per parameter model-
  state baseline (fp16 param, fp32 param copy, fp32 momentum, fp32
  variance).
- All-to-all collective communication (reduce-scatter, all-gather) is
  available and efficient on the interconnect.
- Super-linear speedup at scale relies on larger per-GPU batch sizes
  becoming feasible as memory frees up.
- Worker communication follows the standard synchronous data-parallel
  regime.

## Key results

- **Memory reduction (ZeRO-DP stage 3).** Per-device model-state memory
  reduces by a factor of Nd (data-parallel degree), yielding 64x reduction
  at Nd=64.
  *Holds when:* Adam optimizer; mixed precision training; all three
  partitioning stages (Pos+g+p) enabled.
- **Communication cost of stage 2 (Pos+g).** Gradient and optimizer state
  partitioning adds zero communication overhead vs. standard all-reduce
  (both total 2*Psi bytes moved).
  *Holds when:* Reduce-scatter + all-gather decomposition of all-reduce; Psi
  = total parameter count.
- **Communication cost of stage 3 (Pos+g+p).** Parameter partitioning
  increases total communication volume by at most 1.5x (3*Psi vs. 2*Psi)
  while achieving Nd-x memory reduction.
  *Holds when:* Full parameter partitioning with on-demand all-gather before
  each forward/backward pass.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | ZeRO-DP with all three partitioning stages (Pos+g+p) reduces per-device model-state memory linearly with the DP degree Nd, enabling a 64x reduction at Nd=64. | strong | Analytical derivation of memory formulas and empirical measurement matching theoretical predictions. |
| C2 | Enabling Pos+g (optimizer state and gradient partitioning) incurs zero additional communication volume compared to standard data-parallel all-reduce. | strong | Formal communication analysis showing reduce-scatter + all-gather equals the same 2Psi data movement as baseline all-reduce. |
| C3 | Full parameter partitioning (Pos+g+p) increases total communication volume by at most 1.5x while achieving memory reduction proportional to Nd. | strong | Communication analysis showing 3Psi total vs 2Psi baseline; empirical throughput results confirm efficiency is retained. |
| C4 | ZeRO-100B achieves super-linear speedup when scaling from 64 to 400 GPUs on a 60B parameter model. | strong | Empirical scaling experiments on a 400 V100 GPU cluster showing throughput more than doubles when GPU count doubles. |

## Method

**ZeRO (Zero Redundancy Optimizer).**

ZeRO-DP partitions model states (optimizer states, gradients, parameters)
across data-parallel processes using three progressive stages. At each
training step, reduce-scatter collects only the gradient partition owned by
each process; after parameter updates, all-gather reconstructs the full
parameter tensor on demand. ZeRO-R complements this by partitioning
activation checkpoints across model-parallel GPUs, using constant-size
temporary buffers, and proactively defragmenting memory via pre-allocated
contiguous chunks.

- Pos: optimizer state partitioning (4x memory reduction, same
  communication)
- Pg: gradient partitioning (8x cumulative reduction, same communication)
- Pp: parameter partitioning (Nd-x reduction, 1.5x communication overhead)
- Pa: partitioned activation checkpointing (reduces activation memory by MP
  degree)
- CB: constant-size fused buffers for temporary tensors
- MD: on-the-fly memory defragmentation via pre-allocated contiguous buffers

## Concepts

- **Model States** — The set of tensors that must be stored during training:
  optimizer states (momentum, variance), gradients, and parameters.
- **Residual States** — Memory consumed by activations, temporary buffers,
  and fragmented memory—secondary bottlenecks after model states are
  optimized.
- **Mixed-Precision Training** — Training paradigm storing
  parameters/activations in fp16 for compute efficiency while maintaining
  fp32 copies of parameters and optimizer states for numerical stability;
  requires 16 bytes per parameter with Adam.
- **Reduce-Scatter** — Communication collective where each process receives
  the reduced result of a unique data partition, used by ZeRO to distribute
  gradient reduction.

## Connections

**Builds on.**

- Megatron-LM: Training Multi-Billion Parameter Language Models Using Model
  Parallelism — ZeRO is designed to complement and outperform Megatron-LM's
  tensor-slicing model parallelism, showing ZeRO-DP achieves comparable or
  better memory efficiency with higher scaling efficiency.
- Mixed Precision Training (Micikevicius et al., 2017) — ZeRO assumes and
  analyzes mixed-precision training, quantifying the 16-bytes-per-parameter
  memory footprint that motivates its partitioning approach.

**Related.**

- ZeRO-Infinity: Breaking the GPU Memory Wall for Extreme Scale Deep
  Learning ([LIT-367](../literature.d/LIT-367.md)) — Extends ZeRO-3 with heterogeneous NVMe/CPU
  offloading to break the GPU memory wall entirely.

## Recommendations

- **R1** — Use ZeRO-DP stage 2 (Pos+g) as a default drop-in replacement for
  standard data-parallel training; it yields up to 8x memory reduction with
  no communication overhead increase.
  *Topic:* distributed training memory efficiency · *Strength:* strong · *When:*
  Models too large for single-GPU memory; data-parallel setup with Adam
  optimizer.
- **R2** — Combine ZeRO with model parallelism when activation memory is the
  bottleneck or when batch size constraints require reducing DP degree.
  *Topic:* hybrid parallelism · *Strength:* moderate · *When:* Very large models
  (>100B parameters) where activations dominate memory or critical batch
  size limits DP scaling.
- **R3** — Enable ZeRO-R activation partitioning (Pa) when using model
  parallelism to eliminate redundant activation copies and reduce per-GPU
  activation memory by the MP degree.
  *Topic:* activation memory · *Strength:* moderate · *When:* Model-parallel
  training with large batch sizes and significant activation memory.

## Bearing on the record

The paper is already `LIT-027` and the record already carries three
practices staging ZeRO. This is its first reading, and the part those
practices do not say is which stage is free: stage 2 is an eight-fold memory
reduction at no extra communication, which makes it a default rather than a
tuning choice.

## Limitations

- Stage 3 parameter partitioning adds a 50% communication overhead, which
  may hurt efficiency at very high DP degrees with limited inter-node
  bandwidth.
- ZeRO's full potential (trillion-parameter training) requires ~1024 GPUs;
  compute capacity remains the binding constraint for trillion-parameter
  models.
- Implementation requires framework integration (DeepSpeed); arbitrary model
  architectures may need minor adaptation to work with ZeRO hooks.
- Super-linear speedup relies on fitting larger batch sizes per GPU as
  memory frees up, which eventually saturates or harms convergence at
  extreme batch sizes.

## Open questions

- What is the optimal combination of ZeRO stages, model parallelism, and
  pipeline parallelism for arbitrary model sizes and cluster configurations?
- Can ZeRO's communication schedule be further optimized to reduce the 1.5x
  overhead of stage 3 parameter partitioning?
- How does ZeRO interact with gradient compression or quantization methods?
