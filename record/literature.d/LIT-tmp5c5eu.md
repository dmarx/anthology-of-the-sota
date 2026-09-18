---
status: Active
title: 'HybridFlow: A Flexible and Efficient RLHF Framework'
version: 1
tags:
- distributed-optimization
- systems-optimization
date: '2026-09-18'
published: '2024-09-28'
arxiv: '2409.19256'
first_author: 'Sheng'
keywords:
- 'rlhf'
- 'dataflow'
- 'single-controller'
- 'multi-controller'
- 'resharding'
implementations:
- 'verl'
summary: >-
  Sheng et al. (2024), [ARXIV-2409.19256](https://arxiv.org/abs/2409.19256). The paper behind verl — a hybrid
  single/multi-controller execution model for the RLHF dataflow, with a 3D
  resharding engine between the training and generation phases. Named in
  [ADR-032](../decisions.d/ADR-032.md) as one of the four references at the top of the backlog it
  opened.
---

# LIT-tmp5c5eu: HybridFlow: A Flexible and Efficient RLHF Framework

Sheng et al. (2024) — [ARXIV-2409.19256](https://arxiv.org/abs/2409.19256)

## Key takeaways

- **RLHF is a dataflow whose nodes are themselves distributed programs.** A
  single-controller design pays dispatch overhead per intra-node computation;
  a multi-controller design avoids that but makes the algorithm inflexible
  because distributed computation and communication are nested together.
  HybridFlow's claim is that the two paradigms belong at different levels —
  single-controller for orchestrating the dataflow, multi-controller inside a
  node
- **The 3D-HybridEngine** reshards the actor between its training and its
  generation phase with, by the authors' account, zero memory redundancy and
  much reduced communication. That transition is the part of an RLHF loop
  that has no analogue in ordinary pretraining, and it is where the systems
  work is
- **1.53×–20.57× throughput** over the systems baselines of the day, across
  several RLHF algorithms — a range wide enough that the number to quote is
  the algorithm-and-baseline pair, not the maximum

## Standing in the anthology

**Carries no practice, deliberately** — `ADR-032`.

This is the infrastructure entry that decision used as its example of the
third admissible category, and it names `ARXIV-2409.19256` in its consequences
as one of the four references at the top of the backlog, cited by three of the
twelve documents the sweep read.

Inside this record it is load-bearing in exactly one place, and that place
matters. `LIT-168` (DAPO) records that its training code was released **on
verl**, which is what makes its four techniques checkable — so the record's
claim that DAPO is reproducible rests on a codebase the record could not
name until now.

The reason to hold it beyond that single citation is the one `ADR-032`
gives for the category: a framework is a confounder a comparison cannot see.
Whether the record's RL baselines — the GRPO and PPO arms the
evolution-strategies line is measured against, the published checkpoints in
`SOTA-154` — were run on verl is not stated by the documents that cite them,
and this note is where that question now has an address.

Filed as infrastructure rather than as a method: nothing here recommends
HybridFlow over an alternative, and nothing in the record compares it to one.

Unread — no `NOTE`.
