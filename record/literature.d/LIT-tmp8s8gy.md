---
status: Deferred
status_note: seeded from the abstract and a skim on 2026-09-25; not read in full
title: 'Surya: Foundation Model for Heliophysics'
version: 1
tags:
- vision-and-graphics
- model-architecture
- adaptation-and-tuning
date: '2026-09-25'
published: '2025-08-18'
arxiv: '2508.14112'
first_author: 'Roy'
keywords:
- 'heliophysics'
- 'foundation model'
- 'Solar Dynamics Observatory'
- 'space weather forecasting'
- 'spatiotemporal transformer'
implementations: []
summary: >-
  Roy et al. (2025), [ARXIV-2508.14112](https://arxiv.org/abs/2508.14112). A 366M-parameter transformer pretrained on full-resolution (4096²) multi-instrument SDO imagery to forecast the next frame, then rollout-tuned, forecasts solar dynamics zero-shot. With LoRA fine-tuning it beats task-specific baselines on four downstream heliophysics tasks.
---

# LIT-tmp8s8gy: Surya: Foundation Model for Heliophysics

Sujit Roy, Johannes Schmude, Rohit Lal, Vishal Gaur, Marcus Freitag, Julian Kuehnert, et al. (2025), *arXiv preprint* — [ARXIV-2508.14112](https://arxiv.org/abs/2508.14112)

## Key takeaways

- A 366M-parameter transformer pretrained on full-resolution (4096²) multi-instrument SDO imagery to forecast the next frame, then rollout-tuned, forecasts solar dynamics zero-shot. With LoRA fine-tuning it beats task-specific baselines on four downstream heliophysics tasks.

*Seeded from the abstract and a skim, not a reading. What follows is what the work says about itself.*

Surya is a foundation model for the Sun, trained on 8 AIA channels and 5 HMI products from the Solar Dynamics Observatory. Its architecture is a spatiotemporal transformer with spectral (FFT) gating and long-short range attention. The pretext task is forecasting the next image at a 12-minute cadence, followed by autoregressive rollout tuning. Zero-shot, it forecasts solar evolution and flare events. With LoRA fine-tuning it performs well on solar wind forecasting, active-region segmentation, flare forecasting and EUV spectra. The authors say it is the first heliophysics foundation model trained on full-resolution SDO data with time advancement as the pretext task.

## Standing in the record

Filed from the survey of 2026-09-25 of work the anthology set aside as out of scope (tier C): 375 seconds of active reading over 2 sessions in the papers-feed tracker. `Deferred` because nobody has read it closely here yet, not on merit.

It was a boundary case in the survey of work this anthology had set aside as out of scope, and it is filed here rather than in the catchall record, nucleation, under the rule that a work in doubt belongs in the anthology. It is an ML model and training recipe (a spectral-gated long-short-attention transformer, rollout tuning, LoRA transfer) applied to scientific imagery, so the anthology should hold it; the physics is the data, not the claim.

**Priority for a deeper reading: low — Moderate reading time (t = 375 s). The skim captures the recipe, and it is a domain application rather than a source of general practice. It matters mainly as the case that may force a new topic.**

What a deeper reading should check:

- The triage cites [ADR-059](../decisions.d/ADR-059.md): physics and climate models get their own topic word once the record holds them. None of the 22 topics names scientific or physical-domain foundation models. `vision-and-graphics` ("visual foundation models") is the nearest honest fit, and the vocabulary may want a word such as `scientific-modeling`. That call belongs to whoever files it.
- Practice-bearing details: the one-step-then-rollout pretraining recipe carried over from weather models (Pathak 2022, Lam 2023), MSE-induced blurring as a known failure of deterministic forecasters, and the statement that no LR warm-up was needed. Each could support or challenge an anthology practice.
- The baseline comparisons are with AlexNet, ResNet50 and U-Net. A deeper reading should check whether stronger domain baselines exist, and the authors' own caution that validation timestamps differ across models (§3).

Access when seeded: arXiv abs page (v1 18 Aug 2025, v2 21 Aug 2025) and the full v2 PDF, extracted with PyMuPDF. I read the section heads, §2.3 Architecture, §2.4 Scaling and Pretraining protocol, and §3 Discussion and Conclusions. I did not read the downstream sections §2.6.x beyond their headings and the results quoted in §3. The full author list (33 names) is in the arXiv metadata.
