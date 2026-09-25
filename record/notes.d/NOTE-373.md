---
number: 373
status: Skimmed
formerly:
- NOTE-tmpb1tto
paper: LIT-719
title: 'Tiny RNNs discover cognitive strategies'
version: 1
date: '2026-09-25'
summary: >-
  GRUs with only 1–4 units predict individual animals' and humans' choices in six reward-learning tasks better than 30+ classical cognitive models of the same dimensionality. Because they are so small, they can be read as dynamical systems, exposing strategies (state-dependent learning rates, perseveration, reward-induced indifference) that no classical model contains.
---

<!-- inactive-ok-file: LIT-719 — Deferred: this is the seeded skim of the paper, filed with it on 2026-09-25 -->

# NOTE-373: Tiny RNNs discover cognitive strategies

## Contribution

Normative cognitive models such as Bayesian inference and reinforcement learning are interpretable but too simple, and they lead to cycles of subjective hand-tuning. The authors fit small recurrent networks directly to individual subjects' choices. Networks with one to four units usually beat classical models and match larger networks across six reward-learning tasks in monkeys, rats, mice and humans. Dynamical-systems tools make the fitted networks interpretable, so different cognitive models can be compared on common terms. The method also estimates the dimensionality of behaviour and sheds light on what meta-reinforcement-learning agents learn.

## Skim

*Abstract, figures and selected sections, read when the work was seeded. Not enough to state its assumptions or results exactly; a `Read` note replaces this one.*

- Setup (Main, Fig. 1): cognitive models and RNNs share one input–output structure: the previous action, state and reward update dynamical variables, which output action probabilities through a softmax. Fitting is by maximum likelihood with nested 10-fold cross-validation over consecutive trials. The authors explain why AIC and BIC are unsuitable, given the 4–40× difference in parameter counts.
- Animal results: RNNs outperform every classical variant, including ideal Bayesian observers, so the animals are suboptimal. The best models have 2 units (reversal learning, two-stage task) or 4 units (transition-reversal task), statistically equal to larger networks. The authors read this as behaviour of dimensionality around 2.
- Ground-truth simulations: tiny RNNs recover the dimensionality and performance of simulated RL and Bayesian agents, so they act as a superset of the classical models, and the procedure does not overfit.
- Data cost: RNNs need 500–3,000 trials per subject to beat cognitive models. A distillation scheme (a large multi-subject teacher with subject embeddings, and a tiny per-subject student trained on the teacher's policy) brings that down to about 350 trials and makes the method usable on human data. In humans, 5–20-unit students fit best, and even 2–4-unit students beat equal-dimension cognitive models.
- Interpretation: phase portraits of logit against logit change, fixed points, and "preference setpoints" separate model-free RL from Bayesian signatures. They also expose new ones: state-dependent learning rate, state-dependent perseveration, reward-dependent bias, and reward-induced indifference after rare transitions. The authors say they validated these with targeted hypothesis tests (Supplementary Results).

## Open questions

- In anthology terms it is an evaluation and interpretability claim: a model small enough to read can beat hand-built models, and cross-validation should replace information criteria when parameter counts differ widely. It also ties to `tiny-models`, as a case where the smallest network is the right one.
- A deeper reading should look at the critical commentary (bioRxiv 2025, "RNN dynamics may not purely reflect cognitive strategies") before treating the discovered "strategies" as facts about cognition.
- The vocabulary has no word for behavioural or cognitive modelling as an application. If more such papers arrive, that is a candidate new topic under [ADR-059](../decisions.d/ADR-059.md).
