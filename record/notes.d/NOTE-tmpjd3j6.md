---
status: Read
paper: LIT-083
title: 'PyTorch FSDP'
version: 1
tags:
- distributed-optimization
date: '2026-09-09'
summary: >-
  Fully Sharded Data Parallel as an industry-grade PyTorch component: a sharding factor F generalising replication through full sharding, communication overlapped by backward prefetching, and a rate limiter over the CUDA caching allocator. The first cluster in [#114](https://github.com/dmarx/anthology-of-the-sota/issues/114) whose practices its paper actually supports.
---

# NOTE-tmpjd3j6: PyTorch FSDP

## Contribution

ZeRO established that optimizer state, gradients and parameters can be
sharded across data-parallel ranks rather than replicated. This paper is the
engineering account of making that an ordinary PyTorch component rather than
a specialist framework — co-designed with the Tensor implementation, the
dispatcher, and the CUDA caching allocator, so that using it does not mean
restructuring the model. It generalises the sharding choice into a single
parameter, and it names the specific systems problems that arise when
sharding meets PyTorch's execution model: the collectives serialising on one
NCCL stream, and the caching allocator's behaviour under multiple streams.

## Key insight

The interesting content is not the sharding — ZeRO had that — but the
observation that **sharding is a continuum with one knob**, and that the
knob's setting is a memory-against-communication trade rather than a mode.
`F = 1` is DDP. `F = W` is full sharding. Everything in between is hybrid
sharding, and the right value is wherever the model stops fitting.

The second insight is that on real hardware the bottleneck moves from the
algorithm into the runtime. Once you shard, the collectives are on the
critical path, and whether they overlap with compute depends on stream
scheduling and allocator behaviour that has nothing to do with the
distributed algorithm at all.

## Assumptions

An engineering paper; there are no theorems and no formal assumptions. The
operating conditions that bound the results:

- **One CUDA device per rank**, and a single process group serving both
  `AllGather` and `ReduceScatter` — the constraint that makes backward
  prefetching necessary in the first place.
- **PyTorch's CUDA caching allocator** as the memory layer. The rate limiter
  exists to manage its behaviour specifically, and the finding does not
  obviously transfer to another runtime.
- Homogeneous accelerators, a datacentre interconnect, and NCCL.
- Evaluated on models up to 1T parameters on A100s; the comparison baseline
  is DDP.

## Key results

- **The sharding factor `F`** — the number of ranks parameters are sharded
  over — generalises the strategy space:

  | `F` | strategy | behaviour |
  |---|---|---|
  | `1` | full replication | reduces to vanilla data parallelism, `AllReduce` for gradients |
  | `W` (world size) | full sharding | each device holds `1/W` of the model |
  | `1 < F < W` | hybrid sharding | the trade between memory and communication |

- **Backward prefetching.** With one NCCL stream, the `ReduceScatter` for the
  current `FlatParameter` blocks the `AllGather` for the next, which blocks
  the next gradient computation — two consecutive exposed communication calls
  on the critical path. FSDP issues the next `AllGather` **before** the
  current `ReduceScatter` to avoid it.
- **Forward overlap.** Collective synchronisation operates on *streams*, not
  `Work` objects, so each `AllGather` can overlap the preceding computation.
  The outermost FSDP unit's parameters are deliberately kept resident, to
  avoid freeing at the end of forward and immediately re-gathering for
  backward.
- **The rate limiter.** The caching allocator runs on the CPU thread and
  decides block reuse without returning memory to CUDA; with several CUDA
  streams and a fast CPU thread it can over-allocate. FSDP throttles to bound
  this.
- **Near-linear TFLOPS scalability**, at performance comparable to DDP while
  supporting substantially larger models.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Sharding strategies form a continuum parameterised by the sharding factor `F` | strong | definitional, and the implementation realises it |
| C2 | FSDP matches DDP throughput while supporting much larger models | strong | the paper's headline experiments, up to 1T parameters |
| C3 | Backward prefetching removes exposed communication from the critical path | strong | follows from the single-NCCL-stream analysis; measured |
| C4 | Scaling is near-linear in TFLOPS | moderate | measured on their hardware; "near-linear" is not quantified as a bound |
| C5 | The caching allocator needs an explicit rate limiter under multi-stream FSDP | moderate | argued from allocator mechanics and addressed by the implementation |
| C6 | Mixed precision reduces memory and communication volume without a quality cost here | moderate | reported as a supported configuration rather than ablated |

## Method

**Algorithm:** Fully Sharded Data Parallel.

Decompose the model into FSDP units. Move one unit to the device at a time
and replay recorded initialisation ops for its tensors — so a model larger
than one device can be constructed at all. In the forward pass, `AllGather`
each unit's parameters before use and free them after. In the backward pass,
`ReduceScatter` gradients, with the next unit's `AllGather` issued first.

**Key components**

- `FlatParameter` — the unit of sharding and of collective communication
- The sharding factor `F`, exposing replication → hybrid → full sharding
- Backward prefetching, against single-stream serialisation
- Stream-based collective synchronisation for forward overlap
- The rate limiter, against caching-allocator over-allocation
- Mixed precision, applied to parameters and communication

## Concepts

- **Sharding factor `F`** — the number of ranks over which parameters are
  sharded. The paper's own generalisation; `F=1` is DDP and `F=W` is ZeRO-3,
  which makes those two points on one axis rather than separate systems.
- **Hybrid sharding** — `1 < F < W`. Shard within a group, replicate across
  groups. The regime where the interconnect topology starts to matter.
- **FSDP unit** — the granularity at which parameters are gathered and freed.
  Choosing it is choosing the memory/communication granularity.
- **Exposed communication** — a collective that is not overlapped by
  computation and therefore appears directly in step time.

## Connections

The direct predecessor is ZeRO, whose sharding stages FSDP generalises and
productionises; the paper positions `F=1` as equivalent to DDP, which is the
other lineage it joins. Distributed Data Parallel is the baseline throughout.

## Recommendations

- **R1** — Use FSDP over DDP once the model, its gradients and its optimizer
  state no longer fit on one device. *Topic:* distributed training. *Status:*
  standard. *Strength:* strong. *Applies when:* memory is the binding
  constraint; below that DDP is simpler and no slower.
- **R2** — Enable backward prefetching. *Topic:* distributed training.
  *Status:* standard. *Strength:* strong. *Applies when:* running FSDP with a
  single process group, which is the default — without it two collectives sit
  exposed on the critical path.
- **R3** — Use mixed precision, for communication volume as much as memory.
  *Topic:* distributed training. *Status:* standard. *Strength:* moderate.
  *Applies when:* the accelerator has the hardware support.
- **R4** — Choose the sharding factor from what actually fits, not by
  defaulting to full sharding. *Topic:* distributed training. *Status:*
  standard. *Strength:* moderate. *Applies when:* the model fits at some
  `F < W`; full sharding then pays communication for memory you did not need.

## Bearing on the record

**All four practices sourced to this note are supported by it**, which makes
this the first cluster in [#114](https://github.com/dmarx/anthology-of-the-sota/issues/114) that confirms rather than corrects.

| practice | disposition |
|---|---|
| [SOTA-116](../practices.d/SOTA-116.md) FSDP over DDP past single-GPU memory | confirmed — R1 |
| [SOTA-117](../practices.d/SOTA-117.md) overlap communication using backward prefetch | confirmed — R2, §3.3.2 |
| [SOTA-118](../practices.d/SOTA-118.md) mixed precision to reduce memory | confirmed — R3 |
| [SOTA-119](../practices.d/SOTA-119.md) choose sharding factor by model and GPU memory | confirmed — R4, and `F` is the paper's own term |

That result is worth stating as loudly as the failures. Three clusters in
[#114](https://github.com/dmarx/anthology-of-the-sota/issues/114) inverted their sources and this one does not, so the base rate for the
remaining eighteen notes is not the 100% the first three suggest. The generic
bullet shape is a signal that a note was never read, not evidence that it is
wrong.

`SOTA-119` is the one that gains most from the reading. Its title says
"choose sharding factor based on model and GPU memory size" and states no
rule; the paper gives the axis its endpoints and their meanings, which is
what makes the choice describable at all.

## Limitations

- No ablation isolating the contribution of each optimisation — prefetching,
  rate limiting and the allocator work are presented as an engineering
  package.
- "Near-linear" scalability is not quantified as a bound, so C4 is a
  description of their curves rather than a claim that transfers.
- The rate limiter addresses PyTorch's caching allocator specifically. How
  much of that finding is about sharding and how much about one runtime is
  not separated.
- Mixed precision is a supported configuration, not a studied variable, so C6
  is the weakest of the four confirmations.

## Open questions

- Where is the optimal `F` for a given model, interconnect and topology?
  The paper gives the axis and not the rule, which is exactly the gap
  `SOTA-119` inherits.
- How much of the engineering transfers to runtimes with different allocator
  behaviour?
- Hybrid sharding interacts with the network topology it shards across, and
  nothing here characterises that interaction.
