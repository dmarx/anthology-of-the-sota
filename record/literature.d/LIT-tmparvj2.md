---
status: Active
title: 'Scaling Language-Image Pre-training via Masking'
version: 1
tags:
- multimodal-learning
- training-optimization
- systems-optimization
- vision-and-graphics
date: '2026-09-25'
published: '2022-12-01'
arxiv: '2212.00794'
first_author: 'Li'
keywords:
- 'contrastive-pretraining'
- 'image-masking'
- 'clip'
- 'batch-size'
- 'unmasked-tuning'
- 'scaling'
implementations:
- 'facebookresearch/flip'
summary: >-
  Li et al. (2022), ARXIV-2212.00794 — FLIP. Train CLIP with 50–75% of image
  patches removed and the image encoder run on the rest: the saved compute
  buys more pairs per hour and a 2–4× larger batch at the same memory, which
  outweighs the information lost per image. ViT-L/16 on LAION-400M reaches its
  CLIP reproduction's accuracy more than 3× faster. The accuracy *gain* at a
  fixed schedule is 1–2 points at L and nothing at B/16, and at equal batch
  size masking 50% buys nothing — the batch is doing the work.
extends:
- LIT-588
- LIT-601
compared_against:
- LIT-588
---

# LIT-tmparvj2: Scaling Language-Image Pre-training via Masking

Li, Fan, Hu, Feichtenhofer and He (2022) — ARXIV-2212.00794 (CVPR 2023).
Read in full as NOTE-tmpr24hg.

## Key takeaways

- **The method is one line.** Randomly remove 50% (or 75%) of image patches
  and run the ViT only on the visible ones, as MAE (LIT-601) does — but with
  no decoder and no reconstruction: the loss is CLIP's contrastive loss
  (LIT-588) and nothing else. At inference the encoder sees the whole image,
  with no adaptation, and that works.
- **What masking buys is sample throughput, and the paper says so.** It is a
  trade between "how carefully we look at a sample pair" and "how many sample
  pairs we can process". ViT-L/16, LAION-400M, 6.4 epochs, zero-shot
  ImageNet, at the memory limit of 256 TPU-v3 cores:

  | mask | batch | time | acc. |
  |---|---|---|--:|
  | 0% | 16k | 1.00× | 68.6 |
  | 50% | 32k | 0.50× | 69.6 |
  | 75% | 64k | 0.33× | 68.2 |

- **And the batch is carrying the accuracy.** At the *same* 16k batch, 50%
  masking gives 68.5 against 68.6 — parity, not a gain; 75% at 16k gives 65.8,
  a loss. Raising the batch at 50% masking from 16k to 64k goes 68.5 → 70.4.
  Masking is a way to afford the larger contrastive batch, not a regularizer
  that improves the representation on its own; the paper floats the
  regularization reading as "possible" and does not test it.
- **Three ablations that settle the details.** A brief unmasked tune (0.32
  epoch) adds +0.5 at 50% and +1.3 at 75%. Adding MAE's reconstruction loss
  gives nothing (69.6 → 69.4). Masking text costs accuracy (−2.2 random,
  −0.4 if padding is masked first) and saves little, because the text encoder
  is 4.4% of the compute.
- **At the full 32-epoch schedule** FLIP is about 1 point more accurate than
  its CLIP reproduction and 2× faster at 50% masking, and reaches the same
  accuracy more than 3× faster. Against CLIP on the same data at ViT-L/14:
  74.6 vs 73.1 (own reproduction) and 72.8 (OpenCLIP) zero-shot; it wins on
  linear probe, fine-tune, retrieval, robustness, captioning. At **ViT-B/16
  it does not win: 68.0 vs 68.2**.
- **Data scaling beats schedule scaling at equal samples seen.** With 12.8B
  samples fixed, moving from LAION-400M to LAION-2B raises zero-shot from
  74.3 to 75.8; doubling the schedule on 400M (25.6B samples) gives 73.9. Model
  and data scaling compound (77.6 with both, vs +1.2 and +1.5 alone).
- **Most of the robustness gap is the data, not the method.** Against the
  original WIT-trained CLIP, every LAION model including FLIP trails badly on
  ImageNet-A (FLIP 51.2, WIT CLIP 71.9 at the same evaluation) — a systematic
  data gap the paper names and does not close.

## Standing in the anthology

Filed from `#290`'s promoted list (item 21). The curation entry said it
"opens a leaf": the record's CLIP cluster — SOTA-359 and the practices around
it — held nothing on cutting the cost of contrastive pretraining by masking,
and the MAE practice SOTA-372 held the encoder design without its use outside
reconstruction.

It sources SOTA-tmpfo9e5, `Proposed`, which extends both. The practice is
written around the table above rather than the abstract, because the
abstract's "improves both accuracy and speed" is true only when the saved
compute is spent on batch or epochs, and false at B/16 — [DP-010](../../docs/design-principles.md#dp-10)'s shape, in
a paper whose own Table 1b states the correction.
