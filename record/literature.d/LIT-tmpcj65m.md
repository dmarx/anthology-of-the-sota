---
status: Active
title: 'Breaking the Computation and Communication Abstraction Barrier in Distributed Machine Learning Workloads'
version: 1
tags:
- distributed-optimization
- systems-optimization
date: '2026-10-01'
published: '2021-05-12'
arxiv: '2105.05720'
first_author: 'Jangda'
keywords:
- 'communication-computation-overlap'
- 'collective-communication'
- 'kernel-fusion'
- 'model-parallelism'
- 'pipeline-parallelism'
- 'data-parallelism'
- 'dsl'
implementations:
- 'CoCoNet'
summary: >-
  Jangda et al. (2021), [ARXIV-2105.05720](https://arxiv.org/abs/2105.05720) — CoCoNet (ASPLOS 2022). A DSL and
  compiler that treat computation and collectives as one program, so they can
  be fused and overlapped. Overlapping a tensor-parallel MatMul with its
  AllReduce in fine-grained chunks hides over 80% of the MatMul and runs
  1.36x faster than issuing them in sequence; in Megatron-LM, the overlapped
  schedules speed up model-parallel inference 1.48-1.51x and pipeline-parallel
  inference further, and the data-parallel gain on BERT training comes from
  fusing the optimizer into the collective rather than from overlap.
---

# LIT-tmpcj65m: Breaking the Computation and Communication Abstraction Barrier in Distributed Machine Learning Workloads

Jangda et al. (2021) — [ARXIV-2105.05720](https://arxiv.org/abs/2105.05720) (ASPLOS 2022)

## Key takeaways

- **The argument is that the kernel boundary is the obstacle.** Frameworks
  call computation and communication as separate library kernels, so
  optimizations that span the two — fusing pointwise work into a collective,
  splitting an AllReduce into a ReduceScatter and AllGather around the
  computation, overlapping a producer with the collective that consumes it —
  are each a hand-written CUDA project. CoCoNet expresses them as
  transformations over one program and autotunes the schedule.
- **Overlap on the tensor-parallel axis, measured in isolation.** For the
  model-parallel MatMul-then-AllReduce in a GPT-2 layer on 16 V100s,
  overlapping the two in chunks hides more than 80% of the MatMul time and is
  up to 1.36x faster than running them in sequence (Figure 1). On the 8.3B
  GPT-2 attention and MLP blocks, the overlapped and fused schedule is
  1.42-1.70x faster than Megatron-LM's implementation and 1.21-1.34x faster
  than the same fusion without overlap (§6.2.1).
- **Integrated into Megatron-LM**, the model-parallel overlap schedule cuts
  inference time of a 3.9B BERT by 1.51x and the 8.3B GPT-2 by 1.48x
  (§6.2.2).
- **On the pipeline axis** the best schedule slices the point-to-point sends,
  fuses computation into them, and overlaps the ReduceScatter, the
  cross-node sends and the AllGather with each other — NVLink inside a node,
  InfiniBand across — rather than using one link at a time. The standalone
  pipeline-plus-model-parallel segment for GPT-3 175B runs 11.75-12.21x
  faster than Megatron-LM's, with the paper attributing the gain jointly to
  slicing, fusion and overlap (§6.3.1).
- **The data-parallel result is fusion, not overlap.** CoCoNet's fused
  ReduceScatter-optimizer-AllGather beats PyTorch DDP, which already overlaps
  bucketed AllReduce with the backward pass, by 1.22-1.52x on BERT training
  with Adam, and fits larger micro-batches by sharding optimizer state.
- **Scope.** The model- and pipeline-parallel numbers are inference only;
  training is measured only for the data-parallel case.

## Standing in the anthology

Filed as the source and origin of [SOTA-059](../practices.d/SOTA-059.md), which had pointed at
[LIT-043](LIT-043.md), a paper that does not propose or measure overlap and mentions it
only when describing ZeRO.
