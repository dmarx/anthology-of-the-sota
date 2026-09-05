---
status: Active
title: 'Build a reasoning model in three stages: pretrain on general data, SFT on reasoning traces, then RL with verifiable rewards'
version: 1
tags:
- training-optimization
date: '2026-09-05'
published: '2025-12-01'
source: LIT-130
# inactive-ok: SOTA-130 — a Proposed variation, named in the summary on purpose
summary: >-
  Olmo Team (2025), [LIT-130](../literature.d/LIT-130.md) — the recipe behind every open reasoning model
  at 7B and above, released in Olmo 3 with every stage and checkpoint in
  the open. Filed so its variations ([SOTA-130](SOTA-130.md)) and its tiny-scale successor
  ([SOTA-123](SOTA-123.md)) have something to be traced back to.
---

# SOTA-129: Build a reasoning model in three stages: pretrain on general data, SFT on reasoning traces, then RL with verifiable rewards

## Source

Olmo Team (2025), [LIT-130](../literature.d/LIT-130.md) — the Olmo 3 model flow.

The standard reasoning curriculum, stated as Olmo 3 runs it in the open: a
base model pretrained on a general mixture; supervised fine-tuning on
reasoning traces so the model produces long chains of thought in the
expected format; a preference-tuning stage; then reinforcement learning with
verifiable rewards — rule-based checkers for math, test cases for code — to
push accuracy past what imitation reaches. GRPO ([LIT-127](../literature.d/LIT-127.md)) is the usual RL
algorithm. Falcon-H1R ([LIT-128](../literature.d/LIT-128.md)) is the same recipe on a hybrid 7B base, and
the 135M write-up in [LIT-129](../literature.d/LIT-129.md) is a small instance of the SFT-then-preference
half.

Conditions: this is the recipe at 7B and above, where the reasoning corpus
is small next to the model's memorization window and a from-scratch mix
could not carry it ([LIT-119](../literature.d/LIT-119.md)'s own arithmetic gives a 100B model a window
near 5000 GT against a 5 GT SFT set). Each stage costs a separate run and a
separate set of hyperparameters, and the RL stage is the sensitive one.

## Successors and variations

<!-- inactive-ok: SOTA-130 — a Proposed variation, named as such -->
- **Drop the SFT stage** ([SOTA-130](SOTA-130.md)): RL with verifiable rewards directly on
  the base model, Olmo 3's RL-Zero track. Filed as *Proposed* because its
  source frames it as an experimental pathway.
- **Collapse pretraining and SFT** ([SOTA-123](SOTA-123.md)): for tiny models, pretrain
  from scratch on the reasoning or SFT mixture and keep only the RL stage.
  [LIT-119](../literature.d/LIT-119.md) shows it beating this recipe at 90M and 0.6B; the same source
  says it should not hold at 100B.
- **Collapse all three**: [LIT-119](../literature.d/LIT-119.md) lists merging the RL phase into
  pretraining as future work. Nothing in the record does it yet.
