---
number: 30
status: Read
formerly:
- NOTE-tmp4mbyl
paper: LIT-022
title: 'Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism'
version: 1
tags:
- distributed-optimization
date: '2026-09-09'
published: '2019-09-01'
summary: >-
  Splits a transformer layer across GPUs by choosing the partition that needs no communication in the middle — column-parallel then row-parallel — so a whole layer costs two all-reduces forward and two backward. No compiler, no library changes, a few lines of PyTorch. 8.3B parameters on 512 GPUs at 76% scaling efficiency.
---

# NOTE-030: Megatron-LM: Training Multi-Billion Parameter Language Models Using Model Parallelism

## Contribution

**Tensor parallelism**, as it is now practised. The paper's claim is not that
intra-layer model parallelism is possible — it is that a *particular choice* of
how to split each matrix multiply removes almost all the communication, and
that the result needs no new infrastructure: "a few extra all-reduce operations
added to the forward and backward pass", implementable in native PyTorch.

## Key insight

The partition is chosen so that the nonlinearity between two GEMMs does not
force a synchronisation.

For the MLP block, `Y = GeLU(XA)` then `Z = YB`:

- Splitting `A` along its **rows** requires `X` split along columns, and the
  GeLU cannot be applied independently to the pieces — you must synchronise
  before the nonlinearity.
- Splitting `A` along its **columns**, `A = [A₁, A₂]`, lets GeLU apply
  independently to each partition's output. Then split `B` along its **rows**,
  so it consumes the GeLU output directly with no communication.

So: **column-parallel, then row-parallel**, one all-reduce at the end. The
same shape works for attention — partition `Q`, `K`, `V` column-wise so each
head's matmul is local, then the output projection row-wise. **Two all-reduces
forward and two backward for an entire transformer layer.**

The `f`/`g` operator pair is the whole implementation: `f` is identity forward
and all-reduce backward, `g` is all-reduce forward and identity backward. They
are conjugates, and each is a few lines.

## Assumptions

- **High-bandwidth interconnect within a model-parallel group.** Model-parallel
  groups sit inside a server (NVLink); data-parallel groups span servers.
  Everything here assumes that hierarchy.
- Model parallelism is **orthogonal to and composable with** data parallelism
  and pipeline parallelism — asserted and demonstrated, and it is what makes
  3D parallelism possible later.
- Weight-tied input and output embeddings, which forces the vocabulary-parallel
  handling below.

## Key results

- **8.3B parameters on 512 GPUs**, sustaining **15.1 PetaFLOPs at 76% scaling
  efficiency** against a single-GPU baseline of 39 TeraFLOPs (30% of peak).
- **Fuse the parallel output GEMM with the cross-entropy loss.** The naive
  all-gather of logits communicates `b×s×v` elements; fusing reduces it to
  `b×s`. Communicating scalar losses instead of logits is, in their words, "a
  huge reduction".
- **Per-GPU vocabulary size should be a multiple of 128.** With 8-way model
  parallelism they pad 50,257 → **51,200**, divisible by `128 × 8 = 1024`.
- **LayerNorm placement is critical for BERT-like models as they grow** —
  called out in the abstract as a prerequisite for the gains, not a detail.
- **More attention heads hurts model-parallel scaling.** At 8.3B with 8-way
  MP, going from 16 to 32 heads shrinks the per-head GEMMs and grows the
  softmax, and scaling efficiency falls. The paper explicitly warns future
  work to treat head count as a systems hyperparameter, not only an
  architectural one.
- Hidden size per head held at **96** across configurations, to keep GEMM
  shapes consistent.
- SOTA at the time: WikiText-103 perplexity 10.8 (from 15.8), LAMBADA 66.5%
  (from 63.2%), RACE 90.9% (from 89.4%).

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Column-then-row partitioning removes the intra-layer synchronisation | strong | derived from where the nonlinearity sits; measured |
| C2 | Two all-reduces each way suffice per transformer layer | strong | the implementation |
| C3 | 76% scaling efficiency to 512 GPUs | strong | measured |
| C4 | Fusing the logit GEMM with cross-entropy is a large communication win | strong | `b×s×v → b×s`, argued exactly |
| C5 | Head count trades against model-parallel efficiency | moderate | one configuration, 16 vs 32 heads |
| C6 | LayerNorm placement matters increasingly with scale for BERT-like models | moderate | stated as essential, demonstrated for their models |

## Method

Partition each MLP's first GEMM column-wise and second row-wise; partition
attention's `Q`/`K`/`V` column-wise and the output projection row-wise; insert
`f` and `g`. Partition the embedding along the vocabulary dimension and fuse
the output GEMM into the cross-entropy. Pad the vocabulary so the per-GPU slice
is a multiple of 128. Compose with data parallelism across servers.

## Concepts

- **Choosing the partition so the nonlinearity needs no synchronisation** —
  the transferable idea. It is a statement about where communication is forced,
  not about matrices.
- **`f`/`g` conjugate operators** — the minimal abstraction that makes it a few
  lines rather than a framework.
- **Architecture hyperparameters as systems hyperparameters** — head count,
  head dimension, vocabulary padding. C5 is the clearest instance in the
  corpus of an architectural choice priced in throughput.

## Connections

The tensor-parallel half of what later becomes 3D parallelism — `LIT-065`
composes exactly this with ZeRO data parallelism and pipeline parallelism to
train 530B. Complementary to `SOTA-017`'s pipeline parallelism, which the paper
explicitly says it is orthogonal to.

<!-- inactive-ok-block: SOTA-107 — Rejected in #114 for exactly this reason, and named as the retired practice this constant explains -->
The **multiple of 128** here is worth pinning next to `SOTA-107`. `#114` found
that practice's "multiple of 128" was a head dimension and block size in
FlashAttention, never a sequence length. Megatron's 128 is a *third* thing —
per-GPU vocabulary slice, for logit-layer GEMM efficiency. Three real 128s in
three different places, which is exactly how a constant ends up attached to the
wrong axis.

## Recommendations

- **R1** — Partition a fused pair of matmuls column-then-row so the
  nonlinearity between them needs no communication. *Topic:* distributed
  optimization. *Strength:* strong; universal practice now.
- **R2** — Fuse the parallel logit GEMM into the loss rather than all-gathering
  logits. *Strength:* strong, and the size of the win is arithmetic.
- **R3** — Pad the vocabulary so the per-device slice is a multiple of 128.
  *Strength:* moderate, hardware-specific.
- **R4** — Price attention-head count in throughput, not only in quality.
  *Strength:* moderate.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice** — the
tensor-parallel partition is so universal that the record carries it the way it
carries backpropagation, which is to say not at all. That is a gap, but it is a
gap about the record's coverage of systems technique rather than an error, and
filing it belongs to a session with that scope.

<!-- inactive-ok-block: SOTA-023, SOTA-024 — both Superseded by GQA, and named as the practices that reason about head structure at all -->
R4 is the one the record could act on today and does not: `SOTA-023`/`SOTA-024`
(multi-query and grouped-query attention) reason about head structure entirely
in memory-bandwidth terms at inference. Megatron says head *count* also prices
in training throughput under tensor parallelism, in the opposite direction.
Recorded here rather than filed.

The document's takeaways — "model parallel transformers", "intra-layer model
parallelism" — restate the title twice. "Mixed-precision implementation" is
close to unsupported: the paper is not about mixed precision.

## Limitations

- 2019, 512 GPUs, 8-way tensor parallelism. Modern practice is far past this
  and the partition is unchanged, which is the point.
- The scaling numbers assume intra-server NVLink; the paper does not
  characterise degradation across slower links.
- C5 rests on a single 16-vs-32-head comparison.

## Open questions

- The head-count/throughput trade is stated as a warning and never quantified
  into a rule. Given how much architecture work now moves head structure
  around (MQA, GQA, MLA), the missing curve is conspicuous.
