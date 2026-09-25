---
number: 371
status: Read
formerly:
- NOTE-tmpr24hg
paper: LIT-706
title: 'FLIP'
version: 1
date: '2026-09-25'
summary: >-
  Removing 50% of image patches in CLIP training halves the image encoder's
  cost and lets the contrastive batch double at the same memory; ViT-L/16 on
  LAION-400M then matches its unmasked reproduction more than 3× faster and
  beats it by about a point at equal epochs. At equal batch the masking gains
  nothing, and at ViT-B/16 the full-schedule model is 0.2 behind — the
  improvement is the batch and the extra samples that masking pays for.
---

<!-- inactive-ok-file: SOTA-429 — Proposed practice filed from this reading; named as what it produced -->

# NOTE-371: FLIP

## Contribution

Shows that CLIP-style contrastive image-text pretraining tolerates discarding
half or three quarters of every image's patches, and that the compute saved
is worth more spent on more pairs and bigger batches than on looking at each
image fully. Establishes the recipe details — no reconstruction, no text
masking, full images at inference, a short unmasked tune — by ablation, and
uses the speedup to run controlled scaling comparisons (model, data, schedule)
at fixed samples seen.

## Key insight

In contrastive pretraining the per-sample encoding is not the bottleneck;
the number of pairs compared is. Masking converts image-encoder FLOPs and
activation memory into batch size and epochs, and on this objective that is
a favourable exchange rate.

## Assumptions

- **ViT image encoder**, because dropping patches only saves compute when the
  encoder can process a variable set of tokens (MAE's design, [LIT-601](../literature.d/LIT-601.md)).
- **The image encoder dominates cost.** Text encoder at 4.4% of image-encoder
  compute here; that is why masking text is not worth it.
- **Memory-bound batch.** The accuracy gain appears when the saved memory is
  spent on batch size; the paper's setting is at the memory limit of 256
  TPU-v3 cores.
- **Data:** LAION-400M (and LAION-2B for data scaling); zero-shot ImageNet-1K
  with 7 CLIP prompt templates is the ablation metric. Ablations at 6.4
  epochs; one run per cell.
- Implementation differs from CLIP: non-autoregressive text encoder,
  WordPiece, length 32, global average pooling. The paper reports these made
  "marginal differences" in its reproduction.

## Key results

- **Table 1a (matched memory).** 0% / 16k: 68.6, 1.00×; 50% / 32k: 69.6,
  0.50×; 75% / 64k: 68.2, 0.33×.
- **Table 1b (batch).** 50% masking: 16k 68.5, 32k 69.6, 64k 70.4. 75%: 65.8,
  67.3, 68.2.
- **Table 1c–f.** Text masking 50%: −2.2 random, −0.4 prioritising padding.
  Masked inference: −3.2 (50%) and −7.3 (75%); an ensemble of complementary
  masked views narrows but does not close it. Unmasked tuning 0.32 epoch:
  +0.5 / +1.3. MAE reconstruction loss added: −0.2 / −0.3.
- **Fig. 3, 32 epochs.** ~1 point over the CLIP reproduction at 2× less time
  (50% masking), and the reproduction's accuracy reached >3× sooner.
- **Table 2 (32 epochs, LAION-400M).** B/16: FLIP 68.0, reproduction 68.2.
  L/16: 74.3 vs 72.4. L/14: 74.6 vs 73.1, OpenCLIP 72.8, WIT CLIP 75.3.
- **Table 3.** Linear probe 83.6 vs 82.6; fine-tune 86.9 vs 86.3 (L/16).
- **Tables 4–7.** Better than the LAION-trained CLIPs on most zero-shot
  datasets, retrieval, robustness and captioning; VQA similar across LAION
  models; WIT-trained CLIP ahead on robustness by a data margin (IN-A 71.9 vs
  51.2).
- **Table 8 (scaling at fixed 12.8B samples).** Baseline L/400M 74.3; H 75.5;
  2B data 75.8; 2× schedule 73.9; H+2B 77.6; all three 78.8.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Masking 50–75% of image patches cuts image-encoder compute 2–4× with little loss when the saving buys batch | strong | Table 1a/b, Fig. 3; FLOPs are arithmetic, accuracy measured |
| C2 | At fixed wall-clock, masked training is more accurate than unmasked | strong | Fig. 3 at ViT-L/16; one architecture for the time curves |
| C3 | Masking improves accuracy at fixed epochs | weak | +1.5–1.9 at L, −0.2 at B/16 (Table 2); at equal batch, parity (Table 1b vs 1a) |
| C4 | The gain comes from the larger batch the saving affords | moderate | Table 1b; the paper's own reading, not isolated beyond that table |
| C5 | Masking regularises and improves robustness | weak | "we hypothesize"; robustness gains shown, mechanism untested |
| C6 | Reconstruction loss is unnecessary | moderate | Table 1f, one setting; authors allow suboptimal loss balancing |
| C7 | Text masking is not worth it | moderate | Table 1c; tied to text encoder being 4.4% of compute |
| C8 | A short unmasked tune closes most of the train/test shift | moderate | Table 1e, Fig. 3 |
| C9 | Data scaling beats schedule scaling at fixed samples seen | moderate | Table 8, Fig. 4; one model size for the single-axis runs |
| C10 | FLIP would beat WIT CLIP if trained on WIT | weak | stated as a hope; not run |

## Concepts

- **Masking ratio** — fraction of image patches removed before the encoder;
  removed tokens are dropped, not replaced with mask tokens.
- **Unmasked tuning** — continuing pretraining at 0% masking for a small
  fraction of an epoch (0.32 here) at a lower learning rate.
- **Schedule scaling** — more epochs over the same data; distinguished from
  data scaling, which holds samples seen fixed.

## Connections

Extends CLIP ([LIT-588](../literature.d/LIT-588.md)) — same objective, same evaluation, and the original
checkpoints are re-evaluated with the paper's own code — and borrows MAE's
([LIT-601](../literature.d/LIT-601.md)) sparse encoder while dropping MAE's decoder and loss, which Table 1f
tests directly. Its batch findings are CLIP's "the batch is the negative set"
([SOTA-359](../practices.d/SOTA-359.md)'s Conditions) measured; SigLIP ([LIT-605](../literature.d/LIT-605.md)) later attacks the same
memory ceiling from the loss side rather than the input side.

## Recommendations

- **R1** — In CLIP-style training with a ViT, drop 50% of image patches and
  spend the saving on batch and epochs; no reconstruction loss; full images
  at inference; a brief unmasked tune at the end. *Topic:*
  multimodal-learning. *Status:* experimental. *Strength:* moderate.
  *Applies when:* the image encoder dominates cost and batch is memory-bound.
- **R2** — Prefer more unique data to more epochs at fixed samples seen.
  *Topic:* data-pipeline. *Status:* standard. *Strength:* moderate.

## Bearing on the record

- **Produces** [SOTA-429](../practices.d/SOTA-429.md) (R1), `Proposed`, extending [SOTA-359](../practices.d/SOTA-359.md) and
  [SOTA-372](../practices.d/SOTA-372.md). Written around Table 1b rather than the abstract: masking is how
  to *afford* the batch, not a better objective.
- **[SOTA-359](../practices.d/SOTA-359.md)** — confirmed in the one place it is measured. Its Conditions
  say batch size sets the task's difficulty; Table 1b is a four-point swing
  on batch alone. Not added as a source: the practice's claim is about the
  objective, which FLIP holds fixed.
- **[SOTA-376](../practices.d/SOTA-376.md)** (SigLIP) — the rival route around the same memory ceiling. No
  one has run the two together or against each other in this record; no
  relation declared.
- **[SOTA-171](../practices.d/SOTA-171.md)** — R2 is consistent with it (2× epochs on 400M pairs bought
  nothing past 32 epochs), in a different modality and far past its four-epoch
  horizon. Not a source.
- **[SOTA-196](../practices.d/SOTA-196.md)** — FLIP's robustness gains are real within LAION and small
  against the WIT/LAION data gap; nothing here bears on the practice's
  zero-shot vs in-distribution conflict.

## Limitations

- Time curves for one architecture (ViT-L/16); the B/16 result is the only
  smaller-model evidence and it shows no gain at equal epochs.
- One run per ablation cell, differences of a few tenths in several cells.
- All models trained on LAION; the WIT-trained CLIP is still ahead on several
  benchmarks and the paper can only hope FLIP would close that on WIT.
- The regularization reading of masking is a hypothesis.

## Open questions

- Does the trade hold for a sigmoid loss, whose accuracy depends less on
  batch size above 16k ([LIT-605](../literature.d/LIT-605.md))? If the gain is the batch, it should shrink.
- What masking ratio is optimal at ViT-B and below, where the encoder is
  cheaper relative to the text tower and data loading?
