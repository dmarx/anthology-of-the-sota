---
number: 5
status: Read
formerly:
- NOTE-tmpq23b2
paper: LIT-074
title: 'FlashAttention'
version: 1
tags:
- attention-techniques
date: '2026-09-09'
published: '2022-05-01'
summary: >-
  Attention is bounded by HBM traffic rather than FLOPs. Tiling to on-chip SRAM and recomputing the attention matrix in the backward pass gives exact attention in Θ(N²d²M⁻¹) HBM accesses against standard attention's Θ(Nd + N²) — and Proposition 3 proves no exact algorithm beats that across all SRAM sizes.
---

# NOTE-005: FlashAttention

## Contribution

Every prior attempt to make attention cheaper on long sequences approximated
it, trading model quality for compute complexity — and frequently failed to
produce a wall-clock speedup even so. This paper identifies why: the
bottleneck is not arithmetic but **memory traffic between HBM and on-chip
SRAM**, which the FLOP count does not model. It gives an exact algorithm that
reduces that traffic by tiling, proves an IO-complexity bound for it, and
proves a matching lower bound showing no exact attention algorithm can do
asymptotically better across all SRAM sizes.

## Key insight

If you are optimising the wrong cost model you can win on the metric and lose
on the clock. Attention's `O(N²d)` FLOP count invites approximations that
reduce FLOPs; the actual constraint is the `O(N²)` intermediate matrix moving
between memory levels. Once the cost is counted in **HBM accesses**, the
right move is not to compute less but to *never materialise the intermediate*
— keep tiles in SRAM, fuse the whole operation, and pay recomputation in the
backward pass instead of a round trip.

The consequence is the important part: this is **exact**. The entire
approximate-attention literature was solving a problem that was partly an
artefact of how the cost was counted.

## Assumptions

- `d ≤ M ≤ Nd`, where `N` is sequence length, `d` head dimension, `M` SRAM
  size. Both Theorem 2 and Proposition 3 hold only in this range.
- A two-level memory hierarchy — large slow HBM, small fast SRAM — with the
  attention inputs resident in HBM.
- Typical values are the reason the bound bites: `d` of 64–128 and `M` around
  **100KB**, so `d²` is many times smaller than `M`.
- GPU-shaped hardware throughout. The analysis is architecture-agnostic in
  form and the constants are not.

## Key results

- **Theorem 1** (correctness, cost) — Algorithm 1 returns
  `O = softmax(QKᵀ)V` with `O(N²d)` FLOPs and **`O(N)` additional memory**
  beyond inputs and output. The FLOP count is unchanged; the memory is
  linear rather than quadratic.
- **Theorem 2** (IO complexity) — for `d ≤ M ≤ Nd`:

  | algorithm | HBM accesses |
  |---|---|
  | standard attention | `Θ(Nd + N²)` |
  | FlashAttention | `Θ(N²d²M⁻¹)` |

  With `d ∈ [64,128]` and `M ≈ 100KB`, `d² ≪ M`, so the ratio is many-fold.
- **Proposition 3** (lower bound) — there is **no** algorithm computing exact
  attention in `o(N²d²M⁻¹)` HBM accesses for all `M ∈ [d, Nd]`. FlashAttention
  is IO-optimal in that sense. The proof turns on `M = Θ(Nd)`, where any
  algorithm needs `Ω(Nd)` accesses.
- **Block sizes** — `B_c = ⌈M/4d⌉`, `B_r = min(⌈M/4d⌉, d)`. The tile is
  derived from the SRAM size, not tuned.
- **Speedups** — 15% end-to-end over the MLPerf 1.1 BERT-large record (seq
  512); **3× on GPT-2** (seq 1K); 2.4× on long-range arena (seq 1K–4K).
- **New capability, not just speed** — 0.7 better perplexity on GPT-2 from
  longer context, 6.4 points on long-document classification, and the first
  Transformers above chance on Path-X (seq 16K, 61.4%) and Path-256 (seq 64K,
  63.1%).

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Attention is bounded by HBM traffic, not FLOPs | strong | Theorem 2 plus the measured speedups at unchanged FLOP count |
| C2 | Exact attention can be computed in `O(N)` extra memory | strong | Theorem 1 |
| C3 | FlashAttention is IO-optimal for exact attention over the SRAM range | strong | Proposition 3, a proved lower bound |
| C4 | Recomputing the attention matrix in backward beats storing it | strong | follows from C1 — recomputation is FLOPs, storage is HBM traffic — and is measured |
| C5 | Tile size should be derived from SRAM capacity | strong | `B_c = ⌈M/4d⌉` is stated as the algorithm's own step 1, not swept |
| C6 | Longer context yields better models, not merely faster ones | moderate | Path-X and Path-256 are new capabilities; the perplexity and classification lifts are single results |

## Method

**Algorithm:** FlashAttention — tiled, fused, exact attention.

Set `B_c = ⌈M/4d⌉` and `B_r = min(⌈M/4d⌉, d)`. Split `Q` into `T_r = ⌈N/B_r⌉`
blocks and `K, V` into `T_c = ⌈N/B_c⌉` blocks. Loop over `K, V` blocks in the
outer loop and `Q` blocks in the inner; load tiles into SRAM, compute the
block of `QKᵀ` there, and update the output with **online softmax** —
maintaining running max `m` and normaliser `ℓ` so the softmax is correct
without ever holding the full `N × N` matrix. In the backward pass,
**recompute** the attention block from the stored `m` and `ℓ` rather than
reading a saved matrix from HBM.

**Key components**

- Tiling sized from SRAM capacity
- Online softmax with running statistics `(m, ℓ)`, which is what makes the
  tiling exact
- Kernel fusion, so the intermediate never reaches HBM
- Backward recomputation, trading FLOPs for memory traffic
- A block-sparse extension, which *is* approximate and is faster than any
  prior approximate method

## Concepts

- **IO-awareness** — designing an algorithm around reads and writes between
  memory levels rather than around arithmetic. The paper's framing, and the
  thing it argues was the missing principle.
- **HBM vs SRAM** — high-bandwidth memory is large and comparatively slow;
  on-chip SRAM is ~100KB and fast. The whole result is the ratio between them.
- **Online softmax** — computing a numerically stable softmax incrementally
  over blocks by carrying a running maximum and normaliser. Without it, tiling
  would force either a second pass or an approximation.
- **Exact attention** — produces the same output as the standard computation,
  as distinct from the approximate-attention line this paper displaces.

## Connections

Positioned directly against the approximate-attention literature —
Reformer, Performer, Linformer and relatives — whose premise it undermines by
showing the cost model was wrong. It draws its lower-bound technique from
streaming algorithms. Its own successor, FlashAttention-2, is separately in
the record.

## Recommendations

- **R1** — Use an exact IO-aware attention kernel wherever the hardware has
  one. *Topic:* attention. *Status:* standard. *Strength:* strong. *Applies
  when:* always on supported hardware; it is exact, so there is no quality
  trade to weigh.
- **R2** — Derive tile size from SRAM capacity rather than tuning it.
  *Topic:* kernels. *Status:* standard. *Strength:* strong. *Applies when:*
  writing or configuring a tiled kernel — `B_c = ⌈M/4d⌉` is the paper's own
  rule.
- **R3** — Recompute rather than store, when the stored thing is large and
  the recomputation is arithmetic. *Topic:* memory. *Status:* standard.
  *Strength:* strong. *Applies when:* the operation is memory-bound, which is
  the condition, not a detail.
- **R4** — Count HBM accesses, not FLOPs, when reasoning about an
  attention-shaped kernel. *Topic:* performance analysis. *Status:* standard.
  *Strength:* strong. *Applies when:* any judgement about whether an
  optimisation will show up on the clock.

## Bearing on the record

**All four practices sourced to this note are supported by it** — the second
confirming cluster in [#114](https://github.com/dmarx/anthology-of-the-sota/issues/114), after `LIT-083`.

| practice | disposition |
|---|---|
| [SOTA-085](../practices.d/SOTA-085.md) use flash attention when hardware supports it | confirmed — R1, and *exact* is why there is no trade |
| [SOTA-086](../practices.d/SOTA-086.md) tiling size should match hardware SRAM size | confirmed — R2, and the paper supplies the formula the title only gestures at |
| [SOTA-087](../practices.d/SOTA-087.md) recompute attention in backward instead of storing | confirmed — R3 |
| [SOTA-114](../practices.d/SOTA-114.md) fuse attention operations where possible | confirmed — fusion is what keeps the intermediate out of HBM |

`SOTA-086` is the one that gains a rule. Its title says the tile "should
match hardware SRAM size" and stops; step 1 of Algorithm 1 is
`B_c = ⌈M/4d⌉`, which is a formula a reader can apply.

`SOTA-085` gains its actual justification. "Use it when the hardware supports
it" reads like a performance tip; the reason it is unconditional is
Proposition 3 — this is IO-optimal for *exact* attention, so unlike every
approximate method there is no quality question to ask.

## Limitations

- The lower bound is asymptotic and over a range of `M`; it does not say
  FlashAttention's constants are optimal, and the successor paper improves
  them substantially.
- `M ≈ 100KB` and `d ∈ [64,128]` are the regime where `d² ≪ M` makes the
  ratio large. Very large head dimensions erode it.
- C6 rests on single results per benchmark. That longer context helps is
  plausible and not established here at any breadth.
- The block-sparse extension is approximate and inherits every question the
  approximate literature has; only the dense algorithm is exact.

## Open questions

- Does the `Θ(N²d²M⁻¹)` bound remain the right target on hardware with a
  different memory hierarchy — larger SRAM, or a third level?
- The lower bound is proved for exact attention. What is the corresponding
  bound for a given approximation quality?
- How much of the record's attention-efficiency work is, like the approximate
  line this displaced, optimising a cost model rather than a cost?
