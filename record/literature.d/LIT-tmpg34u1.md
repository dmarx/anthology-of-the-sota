---
status: Active
title: 'Tulu 3: Pushing Frontiers in Open Language Model Post-Training'
version: 1
tags:
- adaptation-and-tuning
date: '2026-09-05'
published: '2024-11-01'
arxiv: '2411.15124'
first_author: 'Lambert'
keywords:
- 'post-training'
- 'rlvr'
- 'dpo'
- 'sft'
- 'open-recipes'
implementations:
- Tulu 3
summary: >-
  Lambert et al. (2024), [ARXIV-2411.15124](https://arxiv.org/abs/2411.15124). The post-training recipe
  published in full — data, code, decontamination and the negative results —
  and the origin of Reinforcement Learning with Verifiable Rewards as a named
  stage.
---

# LIT-tmpg34u1: Tulu 3: Pushing Frontiers in Open Language Model Post-Training

Lambert et al., Ai2 (2024) — [ARXIV-2411.15124](https://arxiv.org/abs/2411.15124)

## Key takeaways

- The gap it addresses is one of transparency rather than capability:
  post-training data and recipes are simultaneously the most decisive part of
  a modern model and the least published part. Tulu 3 releases the datasets,
  the curation toolkit, the training code and the report.
- The stages are SFT, then DPO, then **Reinforcement Learning with Verifiable
  Rewards** — the paper that names RLVR and treats it as a distinct final
  stage rather than as RLHF with a different reward source.
- Built on Llama 3.1 bases, it surpasses the instruct versions of Llama 3.1,
  Qwen 2.5 and Mistral, and closed models including GPT-4o-mini and Claude
  3.5 Haiku.
- A multi-task evaluation scheme with **development and unseen splits**, plus
  substantial decontamination of existing open datasets against the
  benchmarks — the methodological half, and the reason the numbers are worth
  something.
- It reports **what did not work**: a discussion of training methods that did
  not reliably improve performance, which is the part almost no post-training
  report includes and the part a record like this one should want.

## Standing in the anthology

The origin of the RLVR stage that [SOTA-129](../practices.d/SOTA-129.md) records and that [LIT-130](LIT-130.md)'s Olmo 3
and [LIT-154](LIT-154.md)'s OLMo 2 both end on — Ai2 wrote the recipe and then applied
it to two model generations, which is why it appears in the record three
times before its own note.

Filed for the recipe and for the negative results. Its `Standing` in one
sentence: this is the document that makes the three-stage curriculum
checkable by someone who is not at a frontier lab, and [SOTA-123](../practices.d/SOTA-123.md)'s
anti-curriculum claim — that the first two stages collapse at tiny scale —
is only interesting because this recipe is written down well enough to
depart from.
