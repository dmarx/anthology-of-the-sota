---
number: 340
status: Proposed
formerly:
- SOTA-tmp0m39u
promote_when: >-
  An independent serving benchmark, on more than one GPU class, measuring
  the speed-up of 4-bit weight-only kernels over FP16 against batch size,
  that confirms a near-full speed-up below the memory-bound crossover and
  its decay above it. The source's numbers are the kernel authors' own, all
  on NVIDIA Ampere-class GPUs.
title: 'Expect weight-only 4-bit quantization to speed up batched serving only while the batch keeps the matmul memory-bound, and use a kernel built to stay there'
version: 1
tags:
- inference-optimization
- numerics-and-precision
- systems-optimization
date: '2026-09-23'
source:
- LIT-567
introduced_by:
- LIT-567
consensus: unassessed
consensus_note: >-
  MARLIN is integrated in vLLM, which is adoption. Where the field stands
  on the batch-size limits of weight-only quantization has not been
  assessed here.
implementations:
- vLLM
summary: >-
  Frantar et al. (2024), [LIT-567](../literature.d/LIT-567.md) — weight-only quantization speeds up
  decoding by loading fewer bytes, so the gain lasts only while the layer is
  memory-bound. A kernel designed to stay memory-bound (MARLIN) holds about
  3.9× over FP16 up to batch 16–32 on an A10, decaying toward 1.5× at 128.
  End-to-end in vLLM, single-GPU, 2.3–3.2× at batch 16 or below and
  1.1–1.2× at 128, on four GPU classes. Pick the format for the batch you
  actually serve, and pay for it in accuracy only where it buys speed.
---

# SOTA-340: Expect weight-only 4-bit quantization to speed up batched serving only while the batch keeps the matmul memory-bound, and use a kernel built to stay there

## Source

Frantar et al. (2024), [LIT-567](../literature.d/LIT-567.md) — MARLIN. Read, as [NOTE-305](../notes.d/NOTE-305.md).
The quantization itself is [SOTA-185](SOTA-185.md) (GPTQ).

## The practice

- **Know which side of the roofline you serve on.** At small batch,
  decoding is memory-bound and 4-bit weights give close to 4× on the
  matmuls. As the batch grows, the same weights are reused across more rows,
  the matmul becomes compute-bound, and the advantage shrinks
- **Use a kernel designed to delay the crossover.** A generic dequantize
  then FP16 GEMM loses the speed-up early. MARLIN keeps near 3.9× to batch
  16–32 on an A10 by pipelining loads and dequantizing straight into the
  tensor-core layout, which needs its own weight format
- **At high batch, do not expect much from weight-only quantization.**
  About 1.5× at batch 128 in the paper's layer benchmark, and 1.1–1.2×
  end-to-end in vLLM (Table 2). Weight-and-activation quantization targets
  that regime
- **Remember what the speed-up costs.** The INT4 model the paper serves
  loses 3.3 points of mean accuracy (4.3 on MMLU) against FP16 (Table 1). A
  gain that has shrunk to 1.2× at your serving batch may not be worth that

## Conditions

- **The crossover depends on GPU and layer shape.** The headline curve is
  one large layer on an A10
- **Sharding shrinks it.** Split over eight A100s, Llama-2-70B gains 1.38×
  at batch 1, against 2.55× on two
- **Kernel authors' own benchmarks**, on Ampere-class GPUs
