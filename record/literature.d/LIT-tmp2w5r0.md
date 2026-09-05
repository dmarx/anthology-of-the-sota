---
status: Active
title: 'Mamba: Linear-Time Sequence Modeling with Selective State Spaces'
version: 1
tags:
- model-architecture
date: '2026-09-05'
published: '2023-12-01'
arxiv: '2312.00752'
first_author: 'Gu'
keywords:
- 'state-space-models'
- 'selective-ssm'
- 'linear-time'
- 'long-sequences'
- 'hardware-aware'
implementations:
- Mamba
summary: >-
  Gu and Dao (2023), [ARXIV-2312.00752](https://arxiv.org/abs/2312.00752). Make the SSM parameters functions
  of the input and the model can decide what to remember; a hardware-aware
  recurrent kernel keeps it fast without convolutions.
---

<!-- inactive-ok-file: SOTA-125 — the Proposed practice whose SSM-width claim this paper is the root of -->
# LIT-tmp2w5r0: Mamba: Linear-Time Sequence Modeling with Selective State Spaces

Gu and Dao (2023) — [ARXIV-2312.00752](https://arxiv.org/abs/2312.00752)

## Key takeaways

- The diagnosis that unlocked the subquadratic line: linear attention, gated
  convolutions, recurrences and structured SSMs had all failed to match
  attention on language, and the shared weakness is **inability to do
  content-based reasoning** — the state evolves the same way regardless of
  what the current token is.
- The fix is one sentence long: let the SSM parameters be **functions of the
  input**. The model can then selectively propagate or forget along the
  sequence depending on the token it is looking at, which is exactly the
  capability discrete modalities need.
- That breaks the convolutional formulation the efficiency depended on, so
  the paper supplies a **hardware-aware parallel algorithm in recurrent
  mode** — the part that made selective SSMs practical rather than merely
  correct.
- Packaged as a simplified architecture with no attention and no MLP blocks
  at all. 5× higher inference throughput than Transformers, linear scaling
  in sequence length, improving on real data to million-length sequences.
- Mamba-3B beats Transformers its own size and matches Transformers twice its
  size.

## Standing in the anthology

The root of the record's state-space line, and a note several entries have
needed. Falcon-H1 ([LIT-120](LIT-120.md)) runs Mamba-2 heads in parallel with attention
heads in every block; Gated DeltaNet ([LIT-137](LIT-137.md)) is described in the record as
"improving Mamba2 with the delta rule" and is the module three layers in four
of the Qwen line are built from; [SOTA-125](../practices.d/SOTA-125.md) spends a tiny parameter budget on
SSM state width.

The selectivity argument is the one to carry forward. Every linear-attention
variant the record holds is a different answer to the same question — how
does a fixed-size state decide what to keep — and this is where the question
was posed sharply enough to be answerable.
