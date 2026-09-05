---
status: Active
title: 'DeepSeek-V3 Technical Report'
version: 1
tags:
- model-architecture
date: '2026-09-05'
published: '2024-12-01'
arxiv: '2412.19437'
first_author: 'DeepSeek-AI'
keywords:
- 'mixture-of-experts'
- 'multi-token-prediction'
- 'load-balancing'
- 'training-stability'
- 'fp8'
implementations:
- DeepSeek-V3
summary: >-
  DeepSeek-AI (2024), [ARXIV-2412.19437](https://arxiv.org/abs/2412.19437). 671B total, 37B activated, 14.8T
  tokens, 2.788M H800 hours — and no irrecoverable loss spike and no rollback
  in the entire run, which is the claim worth carrying.
---

# LIT-tmp0brdl: DeepSeek-V3 Technical Report

DeepSeek-AI (2024) — [ARXIV-2412.19437](https://arxiv.org/abs/2412.19437)

## Key takeaways

- The model everything in the record's DeepSeek line descends from: 671B
  total with 37B activated, MLA ([LIT-tmplzb5g](LIT-tmplzb5g.md)) and DeepSeekMoE
  ([LIT-tmpe49t1](LIT-tmpe49t1.md)) carried over from V2, pretrained on 14.8T tokens.
- Two things it introduces. An **auxiliary-loss-free load balancing
  strategy** ([LIT-tmpfuwjw](LIT-tmpfuwjw.md)), and a **multi-token-prediction training
  objective** ([LIT-tmp52sif](LIT-tmp52sif.md)) — both of which the subsequent frontier models in
  the record ship.
- 2.788M H800 GPU hours for the full training, which is the number that made
  the report notable at the time.
- **"Throughout the entire training process, we did not experience any
  irrecoverable loss spikes or perform any rollbacks."** That is the
  strongest stability claim any report in the corpus makes, and it is worth
  setting against the instability literature: [LIT-155](LIT-155.md) on attention-logit
  growth, [LIT-154](LIT-154.md) and [LIT-132](LIT-132.md) on the interventions that keep a run alive.

## Standing in the anthology

The MoE recipe K2, K3 and V4 descend from, and the middle of the DeepSeek
line the record now holds end to end: V2's MLA ([LIT-tmplzb5g](LIT-tmplzb5g.md)) → this →
V3.2's sparse attention ([LIT-142](LIT-142.md)) → V4's compressed sparse attention and mHC
([LIT-139](LIT-139.md)).

Its stability claim is the one to return to. [SOTA-131](../practices.d/SOTA-131.md) exists because Muon at
a trillion parameters drove attention logits past 1000; V3 trained at 671B
on AdamW without a rollback. Whether that is the optimizer, the architecture
or the infrastructure is not something either report isolates, and the
record should not pretend otherwise.
