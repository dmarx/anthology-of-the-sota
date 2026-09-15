---
number: 122
status: Read
formerly:
- NOTE-tmphhx3v
paper: LIT-367
title: 'ZeRO-Infinity: Breaking the GPU Memory Wall for Extreme Scale Deep Learning'
version: 1
tags:
- systems-optimization
date: '2026-09-15'
summary: >-
  By partitioning model states across all parallel devices and using a
  bandwidth-centric allgather strategy (rather than per-device broadcast),
  ZeRO-Infinity aggregates PCIe bandwidth linearly with device count, making
  NVMe and CPU offloading fast enough to sustain efficient training despite
  their individually slow bandwidths.
---
# NOTE-122: ZeRO-Infinity: Breaking the GPU Memory Wall for Extreme Scale Deep Learning

## Contribution

ZeRO-Infinity extends the ZeRO family with an infinity offload engine that
simultaneously leverages GPU, CPU, and NVMe memory to train models with tens
of trillions of parameters on current GPU clusters—50x larger than 3D
parallelism—without requiring model code refactoring.

## Key insight

By partitioning model states across all parallel devices and using a
bandwidth-centric allgather strategy (rather than per-device broadcast),
ZeRO-Infinity aggregates PCIe bandwidth linearly with device count, making
NVMe and CPU offloading fast enough to sustain efficient training despite
their individually slow bandwidths.

## Assumptions

- NVMe and CPU memory are available as secondary storage tiers with
  individually insufficient bandwidth but collectively sufficient aggregate
  bandwidth when accessed in parallel.
- The training workload has high arithmetic intensity (large transformer
  layers), so NVMe/CPU latency can be hidden by overlapping with GPU
  compute.
- Bandwidth-centric allgather scales linearly with DP degree; PCIe links
  across nodes are not saturated by competing traffic.
- The dynamic prefetcher can predict the operator execution order accurately
  enough to pipeline transfers effectively.
- PyTorch hook-based data movement does not introduce significant framework
  overhead relative to training step cost.

## Key results

- **Bandwidth-centric partitioning scaling.** Effective NVMe/CPU-to-GPU
  bandwidth scales linearly with data-parallel degree: 48 GB/s aggregate at
  16-way DP vs. 12 GB/s for single-PCIe broadcast.
  *Holds when:* 16-GPU data-parallel setup; CPU offloading; allgather vs.
  broadcast comparison.
- **Extreme-scale training capacity.** 32 trillion parameter models can be
  trained on 512 V100 GPUs, 50x larger than what 3D parallelism supports on
  identical hardware.
  *Holds when:* 32 DGX-2 nodes (512 V100 GPUs); ZeRO-Infinity with full NVMe
  offloading.
- **Throughput at scale.** Over 25 petaflops (40% of peak) sustained
  throughput on 512 V100 GPUs during extreme-scale training.
  *Holds when:* 512 V100 GPUs; large transformer models with high arithmetic
  intensity.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | ZeRO-Infinity can train models with 32 trillion parameters on 512 NVIDIA V100 GPUs, 50x larger than 3D parallelism on identical hardware. | strong | Empirical demonstration of 32T parameter model training on 32 DGX-2 nodes (512 GPUs) reported in evaluation section. |
| C2 | Bandwidth-centric partitioning (allgather-based) achieves linearly increasing effective NVMe/CPU-to-GPU bandwidth with data-parallel degree, unlike broadcast-based approaches limited to single-PCIe bandwidth. | strong | Analytical argument and empirical measurement showing 48 GB/s aggregate CPU bandwidth at 16-way DP vs 12 GB/s for broadcast. |
| C3 | ZeRO-Infinity achieves over 25 petaflops (40% of peak) on 512 V100 GPUs while training models at scales inaccessible to 3D parallelism. | strong | Empirical throughput measurements reported in evaluation Section 8. |
| C4 | Memory-centric tiling enables training layers with hidden dimensions up to 64K without model parallelism, even under 2GB memory fragmentation constraints. | strong | Ablation experiment training single-layer transformers with tiling factor 16 reaching 64K hidden size vs 8K maximum without tiling. |

## Method

**ZeRO-Infinity.**

ZeRO-Infinity builds on ZeRO-3 and adds five innovations: (1) an infinity
offload engine that moves partitioned model states to CPU or NVMe using the
DeepNVMe library with near-peak NVMe bandwidth; (2) bandwidth-centric
partitioning where each parameter shard is owned by a different process and
reconstructed via allgather rather than broadcast, enabling aggregate PCIe
bandwidth to scale linearly; (3) memory-centric tiling that decomposes large
operators into sequential tiles to reduce working memory without model
parallelism; (4) an overlap-centric design with a dynamic prefetcher that
pipelines NVMe-CPU, CPU-GPU, and GPU-GPU transfers simultaneously; and (5)
ease-inspired PyTorch hooks that automate all data movement and model
partitioning during initialization without requiring code changes.

- Infinity offload engine (DeepNVMe + pinned memory management layer)
- Bandwidth-centric partitioning (allgather instead of broadcast for
  offloaded parameters)
- Memory-centric tiling (tile large operators to avoid model parallelism)
- Overlap-centric design (dynamic prefetcher for three-stage NVMe->CPU->GPU
  pipeline)
- Ease-inspired implementation (PyTorch hooks for automated data movement
  and initialization partitioning)

## Concepts

- **GPU Memory Wall** — The constraint that GPU HBM capacity grows much
  slower (5x in 3 years) than model size (1000x), making GPU memory the
  primary bottleneck for extreme-scale training.
- **Arithmetic Intensity (AIT)** — Ratio of computation to data movement for
  a workload; high AIT workloads can tolerate slower memory bandwidths
  because compute time dominates.
- **Model State Working Memory (MSWM)** — The minimum GPU memory required to
  execute forward/backward on the largest single operator after all other
  model states have been offloaded.
- **Bandwidth-Centric Partitioning** — Mapping each parameter shard to a
  distinct data-parallel process so that parameter reconstruction uses
  allgather, activating all PCIe links simultaneously instead of a single
  one.
- **Memory-Centric Tiling** — Decomposing a large operator into
  mathematically equivalent smaller tiled sub-operations executed
  sequentially, reducing working memory proportional to the number of tiles.

## Connections

**Builds on.**

- ZeRO: Memory Optimizations Toward Training Trillion Parameter Models
  ([LIT-027](../literature.d/LIT-027.md)) — ZeRO-Infinity extends ZeRO-3 with heterogeneous offloading and
  bandwidth-centric partitioning to transcend the GPU memory wall entirely.
- ZeRO-Offload: Democratizing Billion-Scale Model Training — ZeRO-Infinity
  addresses ZeRO-Offload's limitations: broadcast-based parameter ownership
  bottlenecked on single-PCIe bandwidth and inability to scale parameters
  beyond single-GPU memory.

## Recommendations

- **R1** — Use ZeRO-Infinity's NVMe offload when GPU count is insufficient
  to hold model states, rather than reducing model size or requiring
  additional GPU hardware.
  *Topic:* extreme-scale model training · *Strength:* strong · *When:* Models
  with >100B parameters on clusters where aggregate GPU memory is
  insufficient; requires NVMe storage and adequate CPU memory.
- **R2** — Enable bandwidth-centric partitioning (allgather-based) instead
  of broadcast-based parameter ownership when offloading to CPU/NVMe, to
  scale effective bandwidth linearly with DP degree.
  *Topic:* heterogeneous memory bandwidth · *Strength:* strong · *When:* Multi-
  GPU setup with CPU or NVMe offloading; gains increase with higher data-
  parallel degree.
- **R3** — Use memory-centric tiling to eliminate the need for tensor-
  slicing model parallelism when individual layers are too large for GPU
  working memory.
  *Topic:* large operator memory · *Strength:* moderate · *When:* Single layers
  with very large hidden dimensions (>8K) under fragmented GPU memory
  conditions.

## Bearing on the record

ZeRO-Infinity extends the partitioning the record already recommends in
three practices down to NVMe. The part that bears is bandwidth-centric
partitioning: the reason offload scales is that ownership is spread, not
that the device is fast.

## Limitations

- NVMe bandwidth is still the ultimate bottleneck for the optimizer update
  step; achieving >1.5 TB/s aggregate NVMe bandwidth requires many nodes.
- Training at tens-of-trillions scale requires enormous compute (exa-flop
  class systems) even if memory is no longer the binding constraint.
- Activation checkpoint offloading reduces efficiency for small hidden sizes
  (<8K); the technique is only bandwidth-efficient for large transformer
  layers.
- The overlap-centric design assumes a relatively stable operator execution
  order; dynamic computation graphs may reduce prefetching effectiveness.

## Open questions

- As accelerator compute scales by 10x-100x, will the required NVMe/CPU
  bandwidth remain achievable, or will a new memory wall emerge?
- Can ZeRO-Infinity be combined with pipeline parallelism to further improve
  compute utilization at extreme scale?
- How does the overhead of the Python hook-based automated data movement
  compare to hand-optimized model-parallel implementations for production
  workloads?
