---
status: Deferred
status_note: seeded from the abstract and a skim on 2026-09-25; not read in full
title: 'Discovering cognitive strategies with tiny recurrent neural networks'
version: 1
tags:
- analysis-and-evaluation
- tiny-models
date: '2026-09-25'
published: '2023-04-13'
doi: '10.1038/s41586-025-09142-4'
first_author: 'Ji-An'
keywords:
- 'recurrent neural networks'
- 'cognitive modelling'
- 'reinforcement learning'
- 'decision-making'
- 'dynamical systems'
- 'interpretability'
implementations: []
summary: >-
  Ji-An et al. (2023), DOI-10.1038/s41586-025-09142-4. GRUs with only 1–4 units predict individual animals' and humans' choices in six reward-learning tasks better than 30+ classical cognitive models of the same dimensionality. Because they are so small, they can be read as dynamical systems, exposing strategies (state-dependent learning rates, perseveration, reward-induced indifference) that no classical model contains.
---

# LIT-tmpxyqya: Discovering cognitive strategies with tiny recurrent neural networks

Li Ji-An, Marcus K. Benna, Marcelo G. Mattar (2023), *Nature 644, 993–1001 (2025); first posted as a bioRxiv preprint* — DOI-10.1038/s41586-025-09142-4

## Key takeaways

- GRUs with only 1–4 units predict individual animals' and humans' choices in six reward-learning tasks better than 30+ classical cognitive models of the same dimensionality. Because they are so small, they can be read as dynamical systems, exposing strategies (state-dependent learning rates, perseveration, reward-induced indifference) that no classical model contains.

*Seeded from the abstract and a skim, not a reading. What follows is what the work says about itself.*

Normative cognitive models such as Bayesian inference and reinforcement learning are interpretable but too simple, and they lead to cycles of subjective hand-tuning. The authors fit small recurrent networks directly to individual subjects' choices. Networks with one to four units usually beat classical models and match larger networks across six reward-learning tasks in monkeys, rats, mice and humans. Dynamical-systems tools make the fitted networks interpretable, so different cognitive models can be compared on common terms. The method also estimates the dimensionality of behaviour and sheds light on what meta-reinforcement-learning agents learn.

## Standing in the record

Filed from the survey of 2026-09-25 of work the anthology set aside as out of scope (tier C): 350 seconds of active reading over 1 session in the papers-feed tracker. `Deferred` because nobody has read it closely here yet, not on merit.

It was a boundary case in the survey of work this anthology had set aside as out of scope, and it is filed here rather than in the catchall record, nucleation, under the rule that a work in doubt belongs in the anthology. Its contribution is an ML method (fitting and interpreting 1–4-unit GRUs, with nested cross-validation and teacher–student distillation) whose claims are about interpretability and model comparison, so it is ML practice that happens to be applied to behaviour.

**Priority for a deeper reading: medium — A Nature paper with a methodological point that travels (small interpretable models, CV over AIC/BIC, and distillation for data-poor individuals), and moderate reading time (t = 350 s). The published critique makes a deeper reading worth more than the skim.**

What a deeper reading should check:

- In anthology terms it is an evaluation and interpretability claim: a model small enough to read can beat hand-built models, and cross-validation should replace information criteria when parameter counts differ widely. It also ties to `tiny-models`, as a case where the smallest network is the right one.
- A deeper reading should look at the critical commentary (bioRxiv 2025, "RNN dynamics may not purely reflect cognitive strategies") before treating the discovered "strategies" as facts about cognition.
- The vocabulary has no word for behavioural or cognitive modelling as an application. If more such papers arrive, that is a candidate new topic under [ADR-059](../decisions.d/ADR-059.md).

Access when seeded: Crossref metadata and abstract for the Nature DOI (published 2025-07-02; received 15 May 2023, accepted 12 May 2025). Full open-access HTML on nature.com, from which I read Main and the Results through the phase-portrait and preference-setpoint analyses, and the Methods and Discussion headings. A Crossref search found the earlier bioRxiv preprint 10.1101/2023.04.12.536629 ("Discovering Cognitive Strategies with Tiny Recurrent Neural Networks", posted 2023-04-13), which is where the published date comes from; I did not read the preprint itself. It also found a Nature Reviews Neuroscience piece (10.1038/s41583-025-01007-z) and a critical bioRxiv commentary (10.1101/2025.10.30.685524, 2025-11-17), neither read.
