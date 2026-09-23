---
number: 305
status: Read
formerly:
- NOTE-tmpngzlz
paper: LIT-567
title: 'MARLIN'
version: 1
date: '2026-09-23'
summary: >-
  An FP16×INT4 GEMM kernel that stays memory-bound, and so near the 3.87×
  ideal 4-bit speed-up, up to batch 16–32 on a large layer, decaying toward
  1.5× at 128. End-to-end in vLLM the same shape holds on four GPU classes
  (Table 2): 2.3–3.2× single-GPU at batch ≤16, 1.1–1.2× at 128, and
  much less when the model is sharded over eight A100s. The INT4 model it
  serves loses 3.3 points of mean accuracy (Table 1).
---

# NOTE-305: MARLIN

## Contribution

Evidence that weight-only 4-bit quantization's speed-up can extend from
single-stream decoding into batched serving, and the kernel that achieves
it.

## Key insight

**The speed-up of weight-only quantization is a memory-bandwidth speed-up,
so it lasts exactly as long as the matmul is memory-bound.** Batching raises
the arithmetic per loaded weight until compute dominates. A kernel can only
move that crossover point, not remove it. The paper's roofline (Figure 11,
A10) puts the crossover below batch 64 across four matrix sizes.

## Key results

- **Layer level** (Figure 1, 72k×18k, group 128, A10): close to the 3.87×
  ideal up to batch 16–32, about 1.5× at 128. Existing kernels
  (ExLlamaV2, AWQ, bitsandbytes, torch) are near-ideal at batch 1 and
  degrade quickly. At locked base clock MARLIN holds and the others lose
  ground (Figure 13)
- **Real layer shapes at batch 16** (Figure 9): larger speed-ups on a 3090,
  smaller on an A100, whose bandwidth makes fixed overheads relatively
  larger
- **End-to-end in vLLM** (Table 2), speed-up over FP16 at batch 1 / 16 /
  128:
  - Llama-2-7B, A10: 2.93 / 2.74 / 1.20. RTX 3090: 2.69 / 2.30 / 1.11
  - Llama-2-13B, A6000: 3.17 / 2.77 / 1.23. Yi-34B, A100: 2.90 / 2.69 / 1.18
  - Llama-2-70B on 8×A100: 1.38 / 1.44 / 1.07. Falcon-180B on 8×A100:
    1.76 / 1.70 / 1.08
- **Serving benchmark** (Figure 15, Llama-2-7B, A6000): about 2.8× lower
  time per output token. Sparse-MARLIN about 3.3×. This is where the
  abstract's "2.8×" comes from
- **Prefill** (A100): MARLIN roughly matches an FP16 compute-bound matmul up
  to batch 1024, with about 10% slow-down beyond

## Limitations

- **The accuracy of what is served is not the paper's subject, and it has a
  cost.** Table 1: the GPTQ INT4 Llama-2-7B loses 4.3 MMLU points (47.88 to
  43.59), and 3.3 points on the three-task mean. The INT4 + 2:4 model scores
  *above* the baseline, but only because it was further fine-tuned by
  distillation on synthetic data. It is not a like-for-like comparison, and
  it is not evidence that sparsity is free
- **Sharding erodes the gain.** The more GPUs a model is split across, the
  less time each spends on weight loads, and the smaller the speed-up (8×A100
  at batch 1: 1.38× for Llama-2-70B)
- **All numbers are the kernel authors' own**, on NVIDIA Ampere-class GPUs.
  The kernel design sections (§4) were read for what they do, not checked in
  detail
