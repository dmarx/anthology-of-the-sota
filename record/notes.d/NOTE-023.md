---
number: 23
status: Read
formerly:
- NOTE-tmpxplbk
paper: LIT-112
title: 'PagedAttention and vLLM'
version: 1
tags:
- inference-optimization
date: '2026-09-09'
published: '2023-09-01'
summary: >-
  KV cache memory is huge, grows and shrinks dynamically, and was managed as one contiguous block — so fragmentation and duplication capped the batch size. PagedAttention borrows OS paging: near-zero waste, sharing within and across requests, 2–4× throughput at equal latency.
---

# NOTE-023: PagedAttention and vLLM

## Contribution

High-throughput serving needs large batches, and what actually limited the
batch was **memory management**, not compute. Each request's KV cache is large
and its size is not known in advance — it grows as the request generates and
disappears when it finishes — and existing systems allocated it contiguously
for a worst-case length. The waste from that is fragmentation and duplication,
and it caps how many requests fit. PagedAttention applies the classical OS
answer: allocate in fixed-size blocks, keep a table mapping logical to
physical blocks, and let the cache be non-contiguous.

## Key insight

The KV cache has exactly the shape virtual memory was invented for — a
dynamically sized, per-process allocation whose contiguity nobody actually
needs. Once you see that, the entire toolkit transfers: paging removes
fragmentation, a block table lets one physical block back several logical
ones, and **copy-on-write** makes sharing safe when only some of the sharers
diverge.

The sharing half is the part that is easy to undersell. Parallel sampling and
beam search generate several continuations from one prompt; without sharing,
each carries its own copy of the prompt's KV cache. That is why the paper's
gains are "more pronounced with ... more complex decoding algorithms" —
those are precisely the cases with the most duplication to remove.

## Assumptions

- Transformer decoder serving with a KV cache; the technique is about that
  data structure and nothing else.
- GPU serving with a memory manager the system controls. The block size is a
  tunable that trades internal fragmentation against block-table overhead.
- **Iteration-level scheduling is assumed, not introduced** — described in
  §2 as background and attributed to Orca, which is also one of the two
  baselines.
- Evaluated against FasterTransformer and Orca on popular LLMs of the period.

## Key results

- **Near-zero waste** in KV cache memory, against contiguous allocation's
  fragmentation and duplication.
- **Flexible sharing within and across requests**, via the block table and
  copy-on-write — the same physical blocks backing several sequences until
  one of them writes.
- **2–4× throughput at the same latency** against FasterTransformer and Orca.
- **The gain grows with longer sequences, larger models, and more complex
  decoding algorithms** — all three being cases where the cache is a larger
  fraction of memory or more duplicated.
- Internal fragmentation is bounded by the block size, which is the residual
  waste the design accepts.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | KV cache memory management, not compute, is what caps serving batch size | strong | the paper's framing, and the 2–4× obtained by changing only allocation |
| C2 | Paging reduces KV cache waste to near zero | strong | measured; residual waste is bounded by block size |
| C3 | Blocks can be shared within and across requests, with copy-on-write for divergence | strong | the mechanism, and the source of the complex-decoding gains |
| C4 | vLLM gives 2–4× throughput at equal latency over the state of the art | strong | evaluated against both FasterTransformer and Orca |
| C5 | The advantage grows with sequence length, model size, and decoding complexity | moderate | reported as a trend across their scenarios |

## Method

**Algorithm:** PagedAttention, and vLLM around it.

Partition each sequence's KV cache into fixed-size **blocks** holding a fixed
number of tokens. Keep a per-sequence **block table** mapping logical block
index to physical block. The attention kernel gathers from non-contiguous
physical blocks rather than assuming a contiguous buffer. Allocate blocks on
demand as a sequence grows, free them when it finishes, and share physical
blocks between sequences with identical prefixes, copying on write when one
diverges.

## Concepts

- **PagedAttention** — an attention kernel that reads its KV cache through a
  block table instead of from contiguous memory.
- **Internal fragmentation** — the unused tail of the last partially filled
  block. Paging trades unbounded external fragmentation for this bounded
  waste, which is the whole design decision.
- **Copy-on-write, for KV blocks** — several sequences share a physical block
  until one writes, at which point it gets its own copy. The OS technique,
  applied to a decoding tree.

## Connections

Explicitly built on **Orca**'s iteration-level scheduling, which it describes
as background and uses as a baseline. Its baselines are FasterTransformer and
Orca. Everything it borrows conceptually — paging, block tables,
copy-on-write — is 1960s operating-systems work, which the paper says
outright.

## Recommendations

- **R1** — Manage the KV cache in fixed-size blocks with a block table rather
  than contiguously. *Topic:* inference. *Status:* standard. *Strength:*
  strong. *Applies when:* serving with a KV cache at any batch size worth
  batching.
- **R2** — Share KV blocks across sequences with a common prefix, with
  copy-on-write. *Topic:* inference. *Status:* standard. *Strength:* strong.
  *Applies when:* parallel sampling, beam search, or a shared system prompt —
  where the duplication exists to remove.
- **R3** — When a system is throughput-bound, check whether the binding
  constraint is memory *management* before optimising compute. *Topic:*
  systems. *Status:* standard. *Strength:* moderate. *Applies when:* always;
  this paper found a 2–4× that no kernel work would have reached.

## Bearing on the record

**One practice confirmed, one re-sourced.**

| practice | disposition |
|---|---|
| [SOTA-105](../practices.d/SOTA-105.md) PagedAttention to accelerate batch inference | confirmed — R1 and R2 |
| [SOTA-113](../practices.d/SOTA-113.md) use continuous batching for inference | **re-sourced** to Orca |

**`SOTA-113` was sourced to the wrong paper.** vLLM describes iteration-level
scheduling in §2, its *background* section, and cites Orca (Yu et al., OSDI
'22) for it. vLLM's contribution is PagedAttention. Orca was not in the record
at all and is now filed as [LIT-224](../literature.d/LIT-224.md); `SOTA-113` names it first, with
`LIT-112` retained as the production system that carried the technique.

The name is why the citation drifted. **"Continuous batching" appears in
neither paper** — Orca says *iteration-level scheduling*, vLLM inherits that
term — so a practice filed under the popular name had no string tying it to
its origin. That is a fourth distinct failure mode for [#114](https://github.com/dmarx/anthology-of-the-sota/issues/114): not an
invented claim, not a transposed constant, not an inference in a citation's
place, but a **technique filed under a name its literature does not use**.

## Limitations

- The block size is a tunable with a real trade — larger blocks mean more
  internal fragmentation, smaller ones more block-table overhead — and the
  paper does not give a rule for it.
- 2023 models and hardware. The KV cache has since grown relative to weights,
  which if anything strengthens C1, but the specific multiples are dated.
- C5 is a reported trend rather than a characterised relationship.
- Nothing here addresses the KV cache's *size*, only its management —
  quantisation and architectural reductions like GQA are orthogonal and
  compose.

## Open questions

- How should block size be chosen? The trade is stated and unquantified.
- Prefix sharing is most valuable when many requests share a long system
  prompt, which is now the common serving pattern. Is there a measurement of
  that case specifically?
- C1 says management rather than compute was the constraint. What is the
  constraint now, after this and after chunked prefill?
