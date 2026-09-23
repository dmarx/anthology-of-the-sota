---
status: Active
title: 'MARLIN: Mixed-Precision Auto-Regressive Parallel Inference on Large Language Models'
version: 1
tags:
- inference-optimization
- numerics-and-precision
- systems-optimization
date: '2026-09-23'
published: '2024-08-01'
arxiv: '2408.11743'
first_author: 'Frantar'
keywords:
- 'marlin'
- 'weight-only-quantization'
- 'mixed-precision-gemm'
- 'batched-inference'
- 'vllm'
implementations:
- vLLM
extends:
- LIT-081
summary: >-
  Frantar, Castro, Chen, Hoefler, Alistarh (2024), [ARXIV-2408.11743](https://arxiv.org/abs/2408.11743). An
  FP16×INT4 matrix-multiply kernel, the "Marlin format" being its
  quantization-specific weight layout. It keeps weight-only quantization's
  memory-bandwidth speed-up through batched serving: about 3.9× over FP16
  (near the 3.87× ideal for 4-bit, group 128) up to batch 16–32, falling
  toward 1.5× at 128 as the problem turns compute-bound. In vLLM, about
  2.8× lower time per output token on an A6000, and 2.3–3.2× single-GPU
  end-to-end at batch 16 or below, falling to 1.1–1.2× at 128.
---

# LIT-tmpjvhmz: MARLIN: Mixed-Precision Auto-Regressive Parallel Inference on Large Language Models

Frantar, Castro, Chen, Hoefler, Alistarh, ISTA, Universidade da Coruña and
ETH Zürich (2024) — [ARXIV-2408.11743](https://arxiv.org/abs/2408.11743)

## Key takeaways

- **The question:** weight-only quantization clearly speeds up
  single-user decoding, which is memory-bound. Does it survive batching, as
  the arithmetic per weight loaded grows?
- **The answer is a roofline.** A 4-bit kernel can stay memory-bound, and
  so keep close to the full 4× speed-up, until the batch makes the matmul
  compute-bound. On an A10 that is around batch 16–32 for large layers,
  after which the speed-up decays toward 1.5× at batch 128
- **How:** asynchronous global loads, careful shared-memory and warp
  layouts, pipelining, and dequantization straight into the tensor-core
  register layout. This requires a bespoke weight layout, which is what
  "Marlin format" names
- **End-to-end:** integrated in vLLM, the same curve on four GPU classes
  (Table 2): 2.3–3.2× single-GPU at batch 16 or below, 1.1–1.2× at 128,
  less when sharded (1.38× at batch 1 for Llama-2-70B on eight A100s). About
  2.8× lower time per output token in a serving benchmark, and 3.3× with 2:4
  sparsity. The sparse model's accuracy beats the FP16 baseline only
  because it was further distilled on synthetic data

## Standing in the anthology

**Filed from `#163`** ("marlin format"). It `extends` GPTQ ([LIT-081](LIT-081.md)), whose
quantized weights it serves, from the same first author. It sources
[SOTA-tmp0m39u](../practices.d/SOTA-tmp0m39u.md).

**What travels and what the practice keeps.** "2.8×" is the travelling
number, and it is a latency figure from one serving benchmark. The more useful result is the shape of the curve:
the speed-up is set by whether the layer is memory-bound, which depends on
batch size and GPU. The practice is stated in those terms.

Read — [NOTE-tmpngzlz](../notes.d/NOTE-tmpngzlz.md).
<!-- inactive-ok-file: SOTA-tmp0m39u — Proposed, filed in this same contribution from this paper -->
