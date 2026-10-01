---
status: Active
title: 'SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features'
version: 1
tags:
- multimodal-learning
- vision-and-graphics
- data-pipeline
- representation-and-encoding
date: '2026-10-01'
published: '2025-02-20'
arxiv: '2502.14786'
first_author: 'Tschannen'
keywords:
- 'vision-language-encoders'
- 'sigmoid-loss'
- 'captioning-pretraining'
- 'self-distillation'
- 'masked-prediction'
- 'multilingual'
- 'native-aspect-ratio'
- 'active-data-curation'
- 'dense-features'
implementations:
- 'google-research/big_vision'
summary: >-
  Tschannen et al. (2025), ARXIV-2502.14786. Keep SigLIP's architecture and
  sigmoid loss, and add a captioning-and-grounding decoder loss (LocCa)
  throughout, self-distillation and masked prediction for the last 20% of
  training, a 90/10 English/multilingual mix with de-biasing filters, and
  distillation through active data selection for the smallest models. It
  beats SigLIP at every size and resolution compared on zero-shot
  classification, retrieval, VLM transfer, dense probing and localization (RefCOCO val, L/256: 67.3 →
  86.0). None of the ingredients is ablated, so the gains cannot be
  credited to any one of them.
extends:
- LIT-605
compared_against:
- LIT-605
---

# LIT-tmp6b0jl: SigLIP 2: Multilingual Vision-Language Encoders with Improved Semantic Understanding, Localization, and Dense Features

Tschannen et al. (2025) — ARXIV-2502.14786

## Key takeaways

- **The recipe is staged.** The base is SigLIP's sigmoid image-text loss
  plus LocCa's decoder loss, weighted equally. The decoder is a transformer
  with cross-attention to the *un-pooled* vision features, half as deep as
  the text encoder, and it is trained on captioning, referring-expression
  prediction (boxes from region captions) and grounded captioning (captions
  from boxes). The decoder is discarded after pretraining. At 80% of
  training two more losses switch on: SILC's local-to-global
  self-distillation (an EMA teacher sees the full image, the student sees 8
  local crops) and TIPS's masked prediction (50% of student patches
  masked, matched to teacher features per patch). They are weighted 1 and
  0.25, then rescaled by model size: 0.25, 0.5, 1.0 and 0.5 for B, L,
  So400m and g. The additional losses use separately augmented views, so
  the augmentation does not touch the image-text pairs.
- **Training setup.** WebLI (10B images, 12B alt-texts, 109 languages),
  mixed 90% English and 10% non-English, with de-biasing filters applied.
  The text side uses the Gemma tokenizer (256k vocabulary). Adam at 1e-3,
  weight decay 1e-4, gradient clipping at 1, batch **32k**, cosine
  schedule, 40B examples, up to 2048 TPUv5e chips. The architecture is
  SigLIP's, with a MAP-head pooler, so released SigLIP weights can be
  swapped out.
- **Resolution.** Fixed-resolution variants resume the 95% checkpoint at
  the target resolution with all losses on. The authors report that the
  usual low-LR fine-tune of the final checkpoint "did not lead to good
  results across all sizes and resolutions". NaFlex, a single checkpoint
  that keeps native aspect ratio and takes sequence lengths sampled from
  {128, 256, 576, 784, 1024}, resumes from 90% without the
  self-distillation losses. It beats the square variant on OCR, document
  and screen retrieval, especially at short sequence lengths. On natural
  images it trails at B and ties at So400m. It interpolates between the
  trained sequence lengths and does not extrapolate beyond them.
- **Small models are distilled through data selection.** B/16 and B/32
  get 4B more examples at LR 1e-5 under ACID. Each step selects a 32k
  batch from a 64k super-batch by learnability, as scored by the learner
  and a teacher (B/32 uses a 0.75 filtering ratio). The teacher is SigLIP 2
  So400m fine-tuned for 1B examples on curated data. The authors claim this
  recovers the benefit of explicit distillation (ACED) without its
  compute.
- **Results against SigLIP, matched size and resolution.** ImageNet
  zero-shot: B/16-224 76.2 → 78.2, L/16-256 80.5 → 82.5, So/14-384 83.2 →
  84.1; g/16-384 reaches 85.0. XM3600 text→image recall, B/16-224:
  22.4 → 40.3, close to mSigLIP (50.0 at So/16) while English results also
  rise. Frozen dense probing, So/14-224: ADE20k 37.6 → 41.8 mIoU, NYUv2
  depth RMSE 0.576 → 0.493. RefCOCO val, L-256: 67.3 → 86.0, still below
  LocCa's 88.3. Representation bias, L/16-256: 35.5% → 7.3%. Income- and
  region-disaggregated accuracy improves very little or not at all.
- **What is not ablated: all of it.** The paper contains no ablation of
  any ingredient. Loss terms, data mix, de-biasing, tokenizer, the
  resolution-adaptation method and (for B) distillation all change at once
  between SigLIP and SigLIP 2. The attributions in the text are argued, not
  measured: B-size gains "owing to distillation", localization gains
  "attributed to the decoder-based pretraining", and the LocCa gap "might
  be due to" multilingual data.

## Standing in the anthology

It extends LIT-605, the original SigLIP. It keeps that paper's
architecture and its pairwise sigmoid loss and calls it "the original
implementation", so the loss SOTA-376 recommends is unchanged here. What
the extension adds is the decoder and self-supervised terms described
above. It is compared against LIT-605 throughout: released SigLIP
checkpoints are evaluated at matched size and resolution in every table,
and are run through the same downstream training for VLM transfer and
open-vocabulary detection. SigLIP 2 wins on every axis, which is
the point of the paper and also why it is weak as evidence for any single
change.

That weakness is SOTA-194's case. A new objective arrives with a new
dataset, here a multilingual, de-biased mixture and a new tokenizer, and
the improvement is reported against a predecessor that had neither. The
paper itself offers a composition explanation for its one loss, to LocCa
on RefCOCO. Anything this paper might source would have to be a
recommendation about the bundle; no single ingredient is isolated.

Two smaller points of contact. It trains at batch 32k, the size at which
LIT-605 found contrastive benefit saturating (SOTA-377). That is
adoption by the same group, not new evidence (DP-005). NaFlex keeps
native aspect ratio and samples sequence length per batch in the spirit
of LIT-657 and SOTA-398. It resizes and pads one image per sequence
rather than packing several, and it is reported against SigLIP 2's own
square checkpoints, not against NaViT. The self-distillation and
masked-prediction terms come from the DINO line the record holds as
LIT-664 and LIT-599, by way of SILC and TIPS, which are not in the record.
CLIP (LIT-588) appears in its tables, but this note does not establish
whether those numbers were rerun.

Unread — no NOTE.
