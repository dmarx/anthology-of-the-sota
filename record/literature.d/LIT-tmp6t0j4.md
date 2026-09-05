---
status: Active
title: 'DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning'
version: 1
tags:
- adaptation-and-tuning
date: '2026-09-05'
published: '2025-01-01'
arxiv: '2501.12948'
first_author: 'DeepSeek-AI'
keywords:
- 'reasoning'
- 'reinforcement-learning'
- 'rlvr'
- 'emergent-behaviour'
- 'distillation'
implementations:
- DeepSeek-R1
- DeepSeek-R1-Zero
summary: >-
  DeepSeek-AI (2025), [ARXIV-2501.12948](https://arxiv.org/abs/2501.12948). Reasoning incentivised by pure RL
  on verifiable tasks, with no human-labelled reasoning traces: self-
  reflection, verification and strategy adaptation emerge rather than being
  demonstrated.
---

# LIT-tmp6t0j4: DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning

DeepSeek-AI (2025) — [ARXIV-2501.12948](https://arxiv.org/abs/2501.12948)

## Key takeaways

- The claim: reasoning can be **incentivised** rather than demonstrated.
  Pure reinforcement learning against verifiable outcomes — mathematics,
  competitive programming, STEM — develops the capability without any
  human-annotated reasoning trajectories, which is what every prior recipe
  depended on and what limited them.
- What emerges under that pressure is behavioural rather than merely
  numerical: self-reflection, verification of intermediate results, and
  dynamic strategy adaptation appear without being specified.
- The resulting model beats counterparts trained conventionally on human
  demonstrations at the same verifiable tasks.
- The emergent patterns transfer: they can be harnessed systematically to
  improve **smaller** models, which is the distillation half that put R1-style
  traces into everyone else's training mixtures.

## Standing in the anthology

<!-- inactive-ok: SOTA-130 — the Proposed practice whose missing source this is -->
The code [SOTA-130](../practices.d/SOTA-130.md) has been naming without one. That practice — skip the
reasoning SFT stage and run RLVR directly on the base model — is called the
"R1-Zero" style in its own body, with the note that "that work is not in the
record". It is now.

This is the origin of a great deal the record already holds downstream.
[LIT-119](LIT-119.md)'s tiny reasoning models are pretrained on synthetic traces of this
kind; [LIT-123](LIT-123.md)'s looping analysis is about models distilled from teachers like
this one; [LIT-130](LIT-130.md)'s RL-Zero track is Ai2 reproducing the pathway as an open
benchmark. Filing it late is the same pattern as the Muon blog post — the
record accumulated the descendants first.

[LIT-tmp8p6dy](LIT-tmp8p6dy.md) is the critical reading of it, and belongs next to it: the
"Aha moment" it reports may be partly a property of the base model rather
than of the RL.
