---
number: 437
status: 'Proposed'
formerly:
- SOTA-tmpcasx3
promote_when: >-
  A training run at language-model scale that writes its checkpoints this way
  and reports what the record actually turns on: checkpoint write and restore
  time inside the run against uncompressed writes on the same storage, and the
  delta-against-base size across a pretraining run's checkpoint series, in a
  table rather than a figure. A second group's measurement of the exponent
  stream's compressed size on other model families would firm up the
  standalone half. The standalone saving is close to arithmetic once the
  exponent ratio is known, so another table of model sizes does not count. What
  is unmeasured is the cost inside a training loop and the delta half at scale.
consensus: unreplicated
consensus_note: >-
  One group (LIT-750). Exponent-only coding of float streams existed
  before it, in general float-compression work and in the dietgpu code, but
  the record holds no measurement of it on model files from anyone else, and
  the delta and gradient results rest on single runs. Read as of 2026-10.
title: 'Store and move model checkpoints losslessly compressed: code the float exponent as its own stream with an entropy coder alone, and store successive checkpoints as deltas against a periodic full base'
version: 1
tags:
- distributed-optimization
- numerics-and-precision
- systems-optimization
date: '2026-10-01'
source:
- LIT-750
# Separating the exponent from the mantissa is older than the source in
# float compression generally (its refs [58], [59]: Chen et al. 2006, MPC
# 2015), and dietgpu, a code release with no paper, already offered
# exponent-only coding. Delta compression against a stored base is credited to
# Git-theta, now held (LIT-762) and read for this: it stores a model
# version as typed updates against the previous one, but its deltas are sparse
# or low-rank, a dense fine-tune is stored nearly whole, and it has no periodic
# base. It is a precedent for part of step 4, not its origin; the periodic full
# base is called "customary" and credited to nobody. The recommendation as
# filed, applied to model files and checkpoints with the LZ stage dropped, is
# stated first by the source.
introduced_by:
- LIT-750
implementations:
- 'ZipNN (zipnn/zipnn)'
summary: >-
  Hershcovitch et al. (2024), [LIT-750](../literature.d/LIT-750.md) — ZipNN. In regular trained
  weights only the float exponent is redundant: about 40 of its 256 values
  occur and it codes to about a third, while sign and mantissa barely
  compress. So split the exponent into its own stream and Huffman-code it
  without an LZ stage. Llama-3.1 BF16 goes to 66.4% against Zstd's 77.7%,
  and is faster in both directions. Between checkpoints, XOR deltas against a
  base up to 10 checkpoints back compress better than standalone files. Sizes
  and throughputs are measured. Stall time inside a training run is not.
---

<!-- inactive-ok-file: SOTA-189 — Proposed; named only as SOTA-054's other half, not cited as support -->

# SOTA-437: Store and move model checkpoints losslessly compressed: code the float exponent as its own stream with an entropy coder alone, and store successive checkpoints as deltas against a periodic full base

## Source

Hershcovitch et al. (2024), [LIT-750](../literature.d/LIT-750.md) — ZipNN, §III–V.

## What to do

For BF16 or FP32 weights, gradients or optimizer state on disk or on the
wire:

1. **Exponent extraction.** Regroup the bytes so all exponents form one
   stream and sign and mantissa form the rest.
2. **Entropy-code the exponent stream without an LZ stage.** Huffman alone.
   The mantissa stream is close to incompressible, so detect that and store it
   raw.
3. **For models rounded or type-converted after training, split further.**
   Give each mantissa byte its own stream ("byte grouping"). A low-order byte
   that is all zeros then costs almost nothing.
4. **For a series of checkpoints, store deltas.** XOR each checkpoint against
   a full base, compress the delta, and write a new full base periodically so
   restoring one never walks a long chain.

The method is lossless, so none of this touches accuracy. The trade is CPU
time on compression against bytes stored and moved.

## Evidence

All measurements are from [LIT-750](../literature.d/LIT-750.md), which introduced the method and
measured it against Zstd.

**Why the exponent.** In four models histogrammed, about 40 of 256 exponent
values occur and the top 12 cover "almost 99.9%" of parameters. The exponent
stream compresses about 3×, to about 33%, and sign and mantissa hardly
compress at all. The model's compressed size then follows from how much of
each parameter is exponent. BF16 is half exponent, and Falcon-7B, Mistral and
Llama-3.1 land at 66.3–66.4%. FP32 is a quarter exponent, and BERT, OLMo and
wav2vec land at 83.0–83.3%.

**Why no LZ.** Shuffling the parameters at random changes Zstd's exponent
compression by at most 0.05%, so there are no real repeats for LZ to find.
LZ4 and Snappy save nothing on these models. With the LZ stage dropped the
code is both smaller and faster (Table III, single thread, 10 runs on 1 GB,
standard deviation at most 2%):

| model | method | size | compress | decompress |
|---|---|--:|--:|--:|
| Llama-3.1 BF16 | Zstd | 77.7% | 0.71 GB/s | 1.02 GB/s |
| | exponent extraction + Zstd | 68.8% | 0.51 GB/s | 1.21 GB/s |
| | ZipNN | **66.4%** | **1.15 GB/s** | **1.65 GB/s** |
| OLMo-1B FP32 | Zstd | 92.3% | 0.97 GB/s | 1.02 GB/s |
| | ZipNN | **83.2%** | **1.64 GB/s** | **2.48 GB/s** |
| xlm-RoBERTa FP32, rounded | Zstd | 57.4% | 0.18 GB/s | 0.77 GB/s |
| | ZipNN | **42.9%** | **0.83 GB/s** | **1.41 GB/s** |

The middle Llama row separates the two steps. Separating the exponent gives
most of the size gain. Dropping LZ gives the speed and the rest of the size.
Separating the exponent alone, under Zstd, is slower to compress than plain
Zstd.

**Checkpoints.** In one ResNet-18 fine-tune, the share of bytes unchanged
between consecutive checkpoints rises as training converges, stepping with
the learning-rate schedule. XOR deltas against a base 5 or 10 checkpoints
back are, in the paper's words, "still far better than standalone
compression". It shows the same on the public Amber (BF16) and OLMo (FP32)
checkpoint series. Those results are shown as figures, not tables. One
number is given in the text, from three RoBERTa fine-tunes of one base: 83.7%
standalone, 56% as pairwise deltas.

**Where the delta half came from.** The source credits the idea of storing
a base and then only differences to Git-Theta ([LIT-762](../literature.d/LIT-762.md)), a Git extension that
versions a checkpoint per parameter group. Git-Theta does store a later
version as a delta against an earlier one, restored by walking back through
history, so the half of step 4 that says "store differences, not copies"
originates there or earlier. The delta it stores is a different kind,
though. It is typed by how the model was trained: indices and values for a
sparse update, factors for a low-rank one, and the full new values for a
dense one. In its one benchmark a LoRA commit took 0.27 GB against Git LFS's
11.4, but dense fine-tunes of the same 3B model took 10.4–10.62 GB, nearly
the whole checkpoint. It has no periodic base and bounds no chain. What
this practice adds is a bytewise XOR delta of dense checkpoints,
entropy-coded, against a base rewritten periodically. That is the source's,
and it is what the checkpoint results above measure, so `introduced_by`
stays with the source.

**Training artifacts.** In one BF16 RoBERTa fine-tune, gradients compress to
about 47% and optimizer state to about 54%, against about 66% for the
weights. The difference is in the token-embedding layer.

## Conditions and limits

- **"No LZ" is for weights, not for everything.** In deltas, and in the
  embedding layer of gradients and optimizer state, Zstd beats Huffman. The
  source switches to Zstd per chunk once more than 90% of it is zeros, or when
  a long run of zeros appears. Use an encoder that chooses per chunk, as the
  source's does.
- **Nothing measures the cost inside a training run.** The source measures
  sizes and throughputs on a CPU, and argues that checkpoint offload "can, for
  the most part, be done offline", so the saving is storage rather than GPU
  time. Whether compressing every checkpoint delays a run is not tested.
- **The delta and artifact results are single runs.** They come from one
  ResNet-18 fine-tune, one RoBERTa fine-tune and two public checkpoint series,
  read off figures. The paper does not report deltas over a pretraining run of
  its own.
- **The saving has a ceiling.** On regular weights it is about a third for
  BF16 and a sixth for FP32. The larger savings are for "clean" models,
  defined by the compressibility observed, and the authors report that further
  fine-tuning removes the property.
- **Quantized files mostly do not benefit.** Some GPTQ and AWQ checkpoints
  still compress to 85–91%, and GGUF ones do not compress at all.
- **The explanation for the skew is not measured.** The paper offers
  initialization in [−1, 1] and a floor from Adam's ε, then says "No matter
  the reason". It never computes an entropy, so how close its codes come to
  the bound is unknown. The practice does not depend on the reason. It
  depends on the measured skew holding for the model at hand, which can be
  checked by histogramming the exponents before choosing.

## Beside the record's other practices

[SOTA-054](SOTA-054.md) sets the checkpoint interval from profiled write cost against an
overhead bound. Smaller checkpoints lower the write cost, so this practice
changes that practice's input and not its rule. The source does not measure
the write cost inside a run, so it does not test [SOTA-054](SOTA-054.md) either. [SOTA-054](SOTA-054.md)'s
risk-side companion, [SOTA-189](SOTA-189.md), is not affected.

The record's other practices about bits in model files are all lossy:
quantization trades accuracy for size. This practice keeps every bit. It
applies after any of those choices, and on GPTQ and AWQ output it gains little.

## Known implementations

- ZipNN (zipnn/zipnn), the source's open-source library.
