---
status: 'Active'
title: 'Skill-it! A Data-Driven Skills Framework for Understanding and Training Language Models'
version: 1
tags:
- data-pipeline
date: '2026-09-17'
published: '2023-07-26'
arxiv: '2307.14430'
first_author: 'Chen'
keywords:
- 'data-ordering'
- 'curriculum'
- 'data-efficiency'
- 'skills'
- 'online-sampling'
implementations:
- 'Skill-It'
summary: >-
  Chen et al. (2023), [ARXIV-2307.14430](https://arxiv.org/abs/2307.14430). Training data has a prerequisite
  structure: skills are learned in an order, and training on a prerequisite
  makes the dependent skill reachable with less data. Formalises a skill and
  an ordered skill set in terms of the data that induces them, and samples
  over skill mixtures online.
---

# LIT-tmpqofqz: Skill-it! A Data-Driven Skills Framework for Understanding and Training Language Models

<!-- inactive-ok-file: SOTA-166, SOTA-103, SOTA-129, SOTA-130 — Proposed or otherwise not in force, named to place this on a DIFFERENT axis from reweighting and from stage curricula -->
<!-- inactive-ok-file: SOTA-tmp7wadj — Proposed, filed in this same contribution as the practice this note sources -->

Chen et al. (2023) — [ARXIV-2307.14430](https://arxiv.org/abs/2307.14430)

## Key takeaways

- **The hypothesis is an ordering claim**, not a quality claim: "just as humans
  acquire interdependent skills in a deliberate order, language models also
  follow a natural order when learning a set of skills from their training
  data."
- **A skill is defined by its data.** The framework formalises a skill, and an
  ordered set of skills, "in terms of the associated data" — which is what
  makes the claim testable rather than a metaphor.
- **The payoff is data efficiency**: ordered skill sets exist, and "their
  existence enables more advanced skills to be learned with less data when we
  train on their prerequisite skills."
- **Skill-It** is the resulting online sampler over skill mixtures, in two
  regimes — continual pretraining, where the goal is many skills, and
  fine-tuning, where it is one.

## Standing in the anthology

Sources [SOTA-tmp7wadj](../practices.d/SOTA-tmp7wadj.md). Filed on the abstract and the framework statement
rather than a full reading, so it carries no `NOTE` ([ADR-025](../decisions.d/ADR-025.md)) — the ordering
claim and the data-efficiency consequence are what the practice rests on, and
both are stated there.

It occupies a slot the record had entirely empty. Twenty-six practices carry
`data-pipeline` and they answer *what to include* — filtering ([SOTA-170](../practices.d/SOTA-170.md)),
deduplication ([SOTA-164](../practices.d/SOTA-164.md)), proportions ([SOTA-166](../practices.d/SOTA-166.md), [SOTA-103](../practices.d/SOTA-103.md)), repetition
([SOTA-171](../practices.d/SOTA-171.md)) — and none answers *in what order*. The record's only "curriculum"
documents are about **training stages** (pretrain, SFT, RL — [SOTA-129](../practices.d/SOTA-129.md),
[SOTA-130](../practices.d/SOTA-130.md)), which is a different axis: that is ordering the objectives, this is
ordering the data.
