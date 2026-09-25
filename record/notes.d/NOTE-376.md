---
number: 376
status: Skimmed
formerly:
- NOTE-tmpvnq0r
paper: LIT-715
title: 'Surya: heliophysics foundation model'
version: 1
date: '2026-09-25'
summary: >-
  A 366M-parameter transformer pretrained on full-resolution (4096²) multi-instrument SDO imagery to forecast the next frame, then rollout-tuned, forecasts solar dynamics zero-shot. With LoRA fine-tuning it beats task-specific baselines on four downstream heliophysics tasks.
---

<!-- inactive-ok-file: LIT-715 — Deferred: this is the seeded skim of the paper, filed with it on 2026-09-25 -->

# NOTE-376: Surya: heliophysics foundation model

## Contribution

Surya is a foundation model for the Sun, trained on 8 AIA channels and 5 HMI products from the Solar Dynamics Observatory. Its architecture is a spatiotemporal transformer with spectral (FFT) gating and long-short range attention. The pretext task is forecasting the next image at a 12-minute cadence, followed by autoregressive rollout tuning. Zero-shot, it forecasts solar evolution and flare events. With LoRA fine-tuning it performs well on solar wind forecasting, active-region segmentation, flare forecasting and EUV spectra. The authors say it is the first heliophysics foundation model trained on full-resolution SDO data with time advancement as the pretext task.

## Skim

*Abstract, figures and selected sections, read when the work was seeded. Not enough to state its assumptions or results exactly; a `Read` note replaces this one.*

- Architecture (§2.3, Fig. 4): two spectral-gating blocks, with a learnable complex weight over the rFFT (≈84.5M parameters alone); eight long-short attention blocks (windowed local attention plus low-rank dynamic-projection global attention, after Zhu et al. 2021); and a linear decoder. Input is 13 channels × 2 timesteps × 4096², patched at 16×16 into 65,536 tokens of width 1280, with Fourier position embeddings.
- Scaling (§2.4.1): FSDP, bf16 transformer layers with fp32 I/O and FFTs, and gradient checkpointing. Spectral gating reaches the same loss as extra attention layers with 6% less GPU memory (Table 8).
- Protocol (§2.4.2): 160k steps on 128 A100s at batch size 128 (1 per GPU); cosine LR from 1e-4 to 1e-5; no warm-up needed; gradient clipping at 0.1; AdamW with defaults. Rollout tuning then runs 2-step for 20k steps at 1e-5, then 3-, 4- and 5-step for 4k steps each at 1e-6, on 64 GPUs.
- Results (§3): rollout tuning improves 12-hour-lead skill by up to 17.8%. Active-region segmentation reaches IoU 0.768 against 0.688 for U-Net. Flare forecasting reaches TSS 0.436 against 0.358 for AlexNet. Solar-wind RMSE is 75.9 against 93.8 km/s for ResNet50.
- Limitations (§3): the MSE objective blurs sharp features, and the authors suggest diffusion or CRPS losses. The bottleneck was data throughput during rollout training, not model scale. Model and data are on Hugging Face (nasa-ibm-ai4science) and code is at github.com/NASA-IMPACT/Surya.

## Open questions

- The triage cites [ADR-059](../decisions.d/ADR-059.md): physics and climate models get their own topic word once the record holds them. None of the 22 topics names scientific or physical-domain foundation models. `vision-and-graphics` ("visual foundation models") is the nearest honest fit, and the vocabulary may want a word such as `scientific-modeling`. That call belongs to whoever files it.
- Practice-bearing details: the one-step-then-rollout pretraining recipe carried over from weather models (Pathak 2022, Lam 2023), MSE-induced blurring as a known failure of deterministic forecasters, and the statement that no LR warm-up was needed. Each could support or challenge an anthology practice.
- The baseline comparisons are with AlexNet, ResNet50 and U-Net. A deeper reading should check whether stronger domain baselines exist, and the authors' own caution that validation timestamps differ across models (§3).
