---
status: Active
title: 'The Computational Foundations of Collective Intelligence'
version: 1
tags:
- agents-and-environments
date: '2026-10-01'
published: '2025-09-06'
arxiv: '2509.07999'
first_author: 'Pilgrim'
keywords:
- 'collective intelligence'
- 'Marr''s levels'
- 'wisdom of the crowd'
- 'collective sensing'
- 'division of labour'
- 'cultural learning'
- 'animal collective behaviour'
implementations: []
summary: >-
  Pilgrim et al. (2025), [ARXIV-2509.07999](https://arxiv.org/abs/2509.07999). A conceptual framework with no
  new data or model. A collective differs from an individual in its
  computational resources, which are sensing, state (memory), processes and
  actions, and in the constraints that distribution imposes on them:
  coordination and cooperation. Wisdom of the crowd, collective sensing,
  division of labour and cultural learning are each read as one of those
  resource advantages being put to use. It is illustrated with golden
  shiners, ant nest-site choice and pigeon homing.
---
<!-- inactive-ok-file: SOTA-257 — Proposed, named as an analogy the note labels as one -->

# LIT-tmp5juts: The Computational Foundations of Collective Intelligence

Pilgrim et al. (2025) — [ARXIV-2509.07999](https://arxiv.org/abs/2509.07999)

## Key takeaways

- **Marr's levels run bottom-up.** The framework starts at implementation
  and asks what resources a collective has. Its sensory input is the
  union of its members'. Its state space is the product of their states
  plus group structure. Its processes include interactions between
  members, and its action space is the product of their actions (Table 1).
  The framework then asks which representations and algorithms those
  resources allow (Table 2), and which problems they solve.
- **The constraints are where collectives differ in kind.** Synchronization,
  communication cost, splitting and recombining tasks, and bandwidth limit
  coordination. Diverging preferences and free-riding limit cooperation.
  Some mechanisms avoid the cooperation problem through "participatory
  computation": a pigeon in a flock cannot avoid contributing its
  heading.
- **Known forms of collective intelligence, mapped to resources.**
  - Wisdom of the crowd is aggregation of independent errors. Its benefit
    depends on the errors being uncorrelated.
  - Collective sensing is distributed sampling. It is how golden shiners
    track a light gradient no individual can sense.
  - Distributional representations across members allow inference-like
    updates.
  - Redundant memory across members allows cultural learning that outlives
    any individual.
  - The joint action space allows division of labour.
- **Predictions, not tests.** The paper proposes that collectives may be
  capable of disjunctive and counterfactual reasoning that their members
  are not. It also proposes that a collective switches from fast to
  deliberative decision-making when its members disagree. Neither is
  tested.
- **The case studies cut both ways.** Ant colonies outperform individual
  ants on hard nest-site discriminations and underperform them on easy
  ones, because early noisy assessments are amplified (the paper's citation
  [114]).
- **Not shown.** The central claim is that the known forms are "aspects of
  a single unifying principle". It is asserted and illustrated, not
  derived. The framework yields no quantitative prediction that the
  mechanism-specific models it unifies do not already make.

## Standing in the anthology

Filed under `agents-and-environments` for its multi-agent and collective
clause. The paper is about animal groups, says its principles apply to
"human societies, neural circuits, and other biological systems", and
mentions artificial intelligence only as something to integrate into
society. Nothing in the record depends on it, and it carries no
instruction for ML practice.

The connections the record could make are analogies, not support. [SOTA-257](../practices.d/SOTA-257.md)
spends surplus compute on an ensemble of independently seeded models. The
paper's account of wisdom of the crowd names the same condition, uncorrelated
errors, as what makes aggregation pay. [LIT-502](LIT-502.md) (MemGraphRAG) is a
multi-agent LLM system. This paper's resource-and-constraint accounting
(communication cost, bandwidth, splitting and recombining tasks) is a
vocabulary for asking what such a system gains over a single agent, but the
paper does not apply it to one. It is a seed, not a gap.

The paper is also held in the companion record:
[nucleation's note](https://github.com/dmarx/nucleation/blob/main/record/literature.d/LIT-046.md),
which has a full reading.

Unread — no NOTE.
