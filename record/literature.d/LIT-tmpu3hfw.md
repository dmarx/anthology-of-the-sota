---
status: 'Active'
title: 'QLoRA: Efficient Finetuning of Quantized LLMs'
version: 1
tags:
- adaptation-and-tuning
- systems-optimization
date: '2026-09-17'
published: '2023-05-23'
arxiv: '2305.14314'
first_author: 'Dettmers'
keywords:
- 'parameter-efficient-finetuning'
- 'quantization'
- 'lora'
- 'nf4'
- 'memory-efficiency'
implementations:
- 'bitsandbytes'
- 'Guanaco'
summary: >-
  Dettmers et al. (2023), [ARXIV-2305.14314](https://arxiv.org/abs/2305.14314). Back-propagate through a frozen
  4-bit base model into 16-bit LoRA adapters: 65B fine-tuning drops from
  >780GB to <48GB with no loss against a 16-bit fully fine-tuned baseline.
  Carries a second finding the quantization headline tends to bury — LoRA on
  the query and value projections alone does not reach full fine-tuning at
  scale, and the adapter COUNT, not the rank, is what closes the gap.
---

# LIT-tmpu3hfw: QLoRA: Efficient Finetuning of Quantized LLMs

Dettmers et al. (2023) — [ARXIV-2305.14314](https://arxiv.org/abs/2305.14314)

## Key takeaways

- **One storage type, one compute type.** The base weights are stored in 4-bit
  and dequantized to BFloat16 for each matrix multiply; gradients are computed
  in BFloat16 and only for the LoRA parameters. Quantization is a storage
  decision, not an arithmetic one — nothing is multiplied in 4 bits.
- **4-bit NormalFloat (NF4)** is built for weights that are approximately
  normally distributed, and beats the generic 4-bit types empirically rather
  than only in theory. Pile Common Crawl mean perplexity across 125M–13B OPT,
  BLOOM, LLaMA and Pythia: Int4 **34.34**, Float4 (E2M1) **31.07**, Float4
  (E3M0) **29.48**, NF4 with double quantization **27.41**.
- **Double quantization** quantizes the quantization constants themselves,
  saving about **0.37 bits per parameter** — roughly 3GB on a 65B model.
- **Paged optimizers** move optimizer state between GPU and CPU on NVIDIA
  unified memory to survive the gradient-checkpointing memory spikes that
  would otherwise OOM.
- **The headline:** >780GB → <48GB for 65B fine-tuning, without degrading
  runtime or predictive performance against a 16-bit fully fine-tuned
  baseline.
- **The finding that is not about quantization at all:** applying LoRA to the
  query and value projections — the standard practice inherited from the LoRA
  paper — *fails to replicate full fine-tuning for large base models*. The
  most critical hyperparameter is how many adapters are used in total, and
  adapters on **all linear transformer block layers** are required. The
  projection rank `r` does not affect performance.

## Standing in the anthology

Two practices are sourced here, and they are independent claims that happen to
share a paper. The quantized-base method is the headline. The adapter
placement result is the one worth reading the paper for: it is a **correction
to how the record's own LoRA practice is applied in the wild**, measured by a
later paper on the earlier one.

That second finding also qualifies something the record already says.
[SOTA-184](../practices.d/SOTA-184.md)'s conditions note that rank is a real hyperparameter and that
the LoRA paper's tasks do well at small `r`. This paper agrees about `r` and
adds the variable that actually matters — *where* the adapters go, not how
wide they are. A reader who tuned `r` and left the placement at the default
was tuning the hyperparameter the evidence says is inert.

Worth holding alongside [LIT-055](LIT-055.md), which carries no practice deliberately: prefix
tuning lost to low-rank adaptation on deployment shape rather than quality.
This paper is the other half of why the low-rank branch won — it is the one
that made the branch cheap enough to run on hardware people own.
