---
number: 7
status: Read
formerly:
- NOTE-tmpuanf4
paper: LIT-106
title: 'FlashAttention-2'
version: 1
tags:
- attention-techniques
date: '2026-09-09'
published: '2023-07-01'
summary: >-
  FlashAttention reached only 25–40% of peak FLOPs/s; the loss was work partitioning between thread blocks and warps, not the algorithm. Three changes — fewer non-matmul FLOPs, parallelism over sequence length, better warp partitioning — give ~2× and 50–73% of peak.
---

# NOTE-007: FlashAttention-2

## Contribution

FlashAttention solved the memory-traffic problem and left a performance one:
it reaches only **25–40% of theoretical peak FLOPs/s**, well short of an
optimised GEMM. This paper diagnoses that gap as *work partitioning* — how
the computation is divided across thread blocks and warps — rather than
anything about the tiling or the IO analysis. Three changes to the
partitioning, no change to what is computed, roughly **2×**.

## Key insight

Once an algorithm is IO-optimal, the remaining performance is a scheduling
problem on the hardware, and the units that matter are the ones the
programming model exposes: thread blocks and warps. Two specific costs
dominate. **Non-matmul FLOPs** are disproportionately expensive because
tensor cores run matmul at many times the rate of everything else, so
rescaling and bookkeeping consume time out of proportion to their FLOP count.
And **occupancy** collapses when the parallel dimensions — batch × heads —
are too few to fill the GPU, which is exactly the long-context small-batch
regime the kernel exists to serve.

The general lesson is that "IO-optimal" and "fast" are different properties,
and the second one is not implied by the first.

## Assumptions

- NVIDIA GPUs with tensor cores; A100 80GB SXM4 for all measurements. The
  analysis is in CUDA's thread-block/warp model and does not obviously
  transfer to another execution model.
- Head dimension 64 or 128 throughout; hidden dimension 2048; sequence
  lengths 512 to 16k with batch set so total tokens are 16k.
- Block sizes from `{64,128} × {64,128}`, chosen by head dimension and device
  shared memory.
- Exactness is inherited from FlashAttention and not re-argued.

## Key results

- **The diagnosis** — FlashAttention reaches 25–40% of theoretical maximum
  FLOPs/s. The cause is "suboptimal work partitioning between different
  thread blocks and warps", producing either low occupancy or unnecessary
  shared-memory traffic.
- **Three changes**:
  1. tweak the algorithm to **reduce non-matmul FLOPs**;
  2. **parallelise across thread blocks even for a single head**, adding the
     sequence-length dimension to batch and heads, to raise occupancy;
  3. **distribute work between warps** within a thread block, cutting
     shared-memory communication.
- **~2× over FlashAttention**, reaching **50–73% of theoretical peak** — for
  reference, FlashAttention's own gain over optimised baselines was 2–4×.
- **FLOP accounting** for the forward pass: `4 · seqlen² · head_dim ·
  n_heads`; the backward pass has 5 matmuls to the forward's 2, due to
  recomputation.
- **Block sizes are manually tuned.** "We manually tune for each head
  dimension since there are essentially only 4 choices" — `{64,128}²`,
  bounded by shared memory, beyond which the kernel cannot run at all.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | FlashAttention's remaining gap to peak is work partitioning, not the algorithm | strong | the 25–40% measurement plus the ~2× recovered by changing only the partitioning |
| C2 | Non-matmul FLOPs cost disproportionately on tensor-core hardware | strong | architectural, and the basis of change (1) |
| C3 | Parallelising over sequence length raises occupancy when batch × heads is small | strong | change (2), measured across sequence lengths at fixed total tokens |
| C4 | The result is ~2× and 50–73% of peak | strong | Figures 4–6 on A100 |
| C5 | Block sizes are best chosen by tuning over a small discrete set | moderate | asserted from practice — "essentially only 4 choices" — not derived |

## Method

Same computation, different schedule. Reorder the loops so the online-softmax
rescaling happens fewer times per output tile, reducing non-matmul work.
Add the sequence-length dimension to the parallelisation so a single head can
occupy multiple thread blocks. Within a block, split work across warps so
that partial results need less exchange through shared memory.

## Concepts

- **Work partitioning** — the assignment of computation to thread blocks and
  warps. The paper's subject, and distinct from the *algorithmic* tiling
  FlashAttention introduced.
- **Non-matmul FLOPs** — arithmetic outside the matrix multiplies; cheap by
  FLOP count and expensive in time, because it does not run on tensor cores.
- **Occupancy** — how much of the GPU has work. Falls when the parallel
  dimensions are too few, independent of how efficient each unit of work is.

## Connections

Strictly a successor to FlashAttention: same exact output, same tiled
never-materialised route, different schedule. It takes that paper's
optimised-GEMM comparison as its target rather than its baseline.

## Recommendations

- **R1** — Prefer FlashAttention-2 to FlashAttention wherever available.
  *Topic:* attention. *Status:* standard. *Strength:* strong. *Applies when:*
  always — same outputs, so there is no accuracy trade.
- **R2** — When a kernel is IO-optimal and still slow, look at occupancy and
  non-matmul work before the algorithm. *Topic:* kernels. *Status:* standard.
  *Strength:* strong. *Applies when:* any tensor-core kernel below peak.
- **R3** — Parallelise over sequence length when batch × heads cannot fill
  the device. *Topic:* kernels. *Status:* standard. *Strength:* moderate.
  *Applies when:* long context with small batch, which is the case the
  kernel exists for.

## Bearing on the record

**One of three practices confirmed; two retired.**

<!-- inactive-ok-block: SOTA-107, SOTA-108 — Rejected in this same change; the table is the record of why -->
| practice | disposition |
|---|---|
| [SOTA-106](../practices.d/SOTA-106.md) prefer FA-2 to FA-1 | confirmed — R1, and its body's three changes match the paper exactly |
| [SOTA-107](../practices.d/SOTA-107.md) keep sequence lengths a multiple of 128 | `Rejected` |
| [SOTA-108](../practices.d/SOTA-108.md) pad attention masks to block boundaries | `Rejected` |

<!-- inactive-ok-block: SOTA-107 — Rejected in this same change; the paragraph is the record of why -->
**`SOTA-107`'s 128 is traced, and it belongs to a different quantity.** The
string `128` occurs fifteen times in the paper. Every one of them is a **head
dimension** (64 or 128) or a **block size** (`{64,128} × {64,128}`). Not one
is a sequence length, and `multiple of` and `divisible` appear **zero times**.
The constant is real and the practice attaches it to the wrong axis.

<!-- inactive-ok-block: SOTA-108 — Rejected in this same change; the paragraph is the record of why -->
**`SOTA-108` is not in the paper at all.** `padding`, `padded`, `pad`,
`block boundar` and `divisible` are **zero** each.

Both bodies contained sound kernel reasoning — partial blocks cost a full
block, fully-masked blocks can be skipped — which is true and is mine, not
the source's. That is a distinct failure from the earlier clusters: not a
takeaway describing another paper, but a plausible inference written in a
place reserved for what a paper says.

## Limitations

- One GPU generation. The partitioning strategy is tuned to A100's shared
  memory and warp scheduler, and C5 says as much by admitting the block sizes
  are hand-tuned.
- No ablation separating the three changes, so their individual contributions
  are unknown.
- 50–73% of peak is a wide band, and the paper does not characterise what
  puts a configuration at one end or the other.

## Open questions

- What is the remaining 27–50%? The paper closes one gap and does not say
  what bounds the next.
- FlashAttention derived block sizes from SRAM capacity
  (`B_c = ⌈M/4d⌉`); this one tunes them by hand over four choices. Which is
  right, and does the derivation stop holding once the schedule changes?
