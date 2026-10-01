---
status: Active
title: 'ZipNN: Lossless Compression for AI Models'
version: 1
tags:
- systems-optimization
- numerics-and-precision
- distributed-optimization
- inference-optimization
date: '2026-10-01'
published: '2024-11-07'
arxiv: '2411.05239'
first_author: 'Hershcovitch'
keywords:
- 'lossless-compression'
- 'floating-point-exponent'
- 'exponent-extraction'
- 'byte-grouping'
- 'huffman-coding'
- 'delta-compression'
- 'checkpointing'
- 'model-hubs'
implementations:
- 'zipnn/zipnn'
summary: >-
  Hershcovitch et al. (2024), [ARXIV-2411.05239](https://arxiv.org/abs/2411.05239). Losslessly compressing a
  trained model's file works almost entirely through the float exponent:
  about 40 of 256 values occur, and the exponent stream codes to ~33% while
  sign and mantissa stay near 100%. Regular BF16 models therefore shrink to
  ~66%, FP32 to ~83%, and models rounded after training ("clean") to as
  little as 34–48%. Splitting the exponent into its own stream and coding it
  with Huffman alone, without LZ, beats Zstd by 17% in size and 62% in
  single-thread speed on Llama-3.1 BF16.
---

# LIT-tmpbjxkg: ZipNN: Lossless Compression for AI Models

Hershcovitch et al. (2024), IBM Research and others — [ARXIV-2411.05239](https://arxiv.org/abs/2411.05239)

## Key takeaways

- **The redundancy is in the exponent, and only there in regular
  models.** In the four models histogrammed (1 GB samples), only around 40
  of the 256 exponent values occur, and the top 12 cover "almost 99.9%" of
  parameters. The histograms are strikingly similar across language models
  and dtypes. The exponent stream compresses about 3× (to ~33%); sign and
  fraction bytes stay at ~100%. Table II follows from that arithmetic:
  Falcon-7B, Mistral and Llama-3.1 (BF16) all land at 66.3–66.4%, and BERT,
  OLMo and wav2vec (FP32) at 83.0–83.3%.
- **There is nothing for LZ to find.** Shuffling the parameters at random
  changes Zstd's exponent compression by at most 0.05%. Neighbouring
  weights are unrelated, so the gain is single-symbol entropy coding. LZ4
  and Snappy save nothing. Dropping the LZ stage and using Zstd's Huffman
  coder alone, after exponent extraction, is both smaller and faster.
- **Single-thread numbers (Table III; 10 runs on 1 GB, s.d. ≤ 2%, Apple
  M1 Max).** Each row gives compressed size, then compression and
  decompression speed:

  | model | method | size | comp. | decomp. |
  |---|---|--:|--:|--:|
  | Llama-3.1 BF16 | Zstd | 77.7% | 0.71 GB/s | 1.02 GB/s |
  | | ZipNN | 66.4% | 1.15 GB/s | 1.65 GB/s |
  | OLMo-1B FP32 | Zstd | 92.3% | 0.97 GB/s | 1.02 GB/s |
  | | ZipNN | 83.2% | 1.64 GB/s | 2.48 GB/s |
  | xlm-RoBERTa FP32 (clean) | Zstd | 57.4% | 0.18 GB/s | 0.77 GB/s |
  | | ZipNN | 42.9% | 0.83 GB/s | 1.41 GB/s |

  Exponent extraction followed by Zstd sits between the two rows in size
  (68.8% on Llama). That isolates the two steps: separating the field
  gives most of the size gain, and Huffman-only coding gives the speed and
  the rest of the size. With multiple workers on a 224-core Xeon host it
  reaches up to 80 GB/s decompression and 13 GB/s compression.
- **"Clean" models compress further.** Some popular checkpoints were rounded
  or type-converted after training, which leaves low-order fraction bytes
  zero or low-entropy. With one stream per byte position ("byte
  grouping"), T5-base reaches 33.7%, xlm-RoBERTa 41.8% and CLIP 48.1%. The
  category is defined by the compressibility observed, and the authors
  report that further fine-tuning removes it.
- **Training artifacts and deltas.** In one BF16 RoBERTa fine-tune,
  gradients compress to about 47% and optimizer state to about 54%,
  against about 66% for the model. The difference comes from the token
  embedding layer. In one ResNet-18 fine-tune, the share of unchanged bytes
  between consecutive checkpoints rises as training converges, stepping
  with the LR schedule. XOR deltas then compress far better than
  standalone checkpoints, even against a base 5 or 10 checkpoints back
  (also shown on public Amber and OLMo checkpoints). Three RoBERTa
  fine-tunes from one base: 83.7% standalone, 56% as pairwise deltas.
- **Deployment.** Loading a 16 GB BF16 Granite-8B stored at ⅔ size into
  vLLM took about 3 s, "on par" with the uncompressed model. Some GPTQ and
  AWQ checkpoints still compress to 85–91%; GGUF ones do not compress at
  all.
- **What is weak.** The paper never computes an entropy, so how close its
  codes come to the bound is unknown. It gives a reason for the exponent
  skew in a paragraph of prose (initialization in [−1, 1], a floor from
  Adam's ε) without measuring it, and then concedes "No matter the
  reason". The gradient, optimizer and delta results each rest on a single
  run. The abstract's "over an ExaByte per year" saving is not derived in
  the body.

## Standing in the anthology

It is also held in the companion record as
[nucleation's note](https://github.com/dmarx/nucleation/blob/main/record/literature.d/LIT-268.md),
filed there for an information-theoretic reading. That close reading is
the source of the caveats above about the missing entropy measurement and
the unmeasured skew explanation. Here it is filed for what it offers as
practice.

Nothing in the anthology covers lossless compression of model files. Its
neighbours all trade accuracy for bits: GPTQ ([LIT-081](LIT-081.md), source of
[SOTA-185](../practices.d/SOTA-185.md)) and AWQ ([LIT-585](LIT-585.md)) quantize, and [LIT-197](LIT-197.md) and [LIT-186](LIT-186.md) choose the
format. This paper takes the format as given and asks how many of its bits
are redundant. Its answer, that only the exponent field is redundant,
holds for regular trained weights. Its measurement that GPTQ- and
AWQ-quantized checkpoints are still compressible is a small fact about
those papers' output, not a test of their methods. Gradient compression
for communication ([LIT-056](LIT-056.md)) is lossy and works on a different object.

The checkpoint results bear on [SOTA-054](../practices.d/SOTA-054.md), which sets the checkpoint
interval against an overhead bound. Smaller checkpoints lower that
overhead. The paper measures sizes and throughputs, though, not
checkpoint stall time inside a training run, so it informs the
practice's inputs without testing it.

Unread — no NOTE.
