---
status: Active
title: 'When a model''s latent space is meant to be read by people, measure its interpretability with a human task such as word or topic intrusion, not by held-out likelihood'
version: 1
tags:
- analysis-and-evaluation
- representation-and-encoding
date: '2026-09-23'
source:
- LIT-tmpmiyeb
introduced_by:
- LIT-tmpmiyeb
consensus: unreplicated
consensus_note: >-
  One group's study, with three models and two corpora. Its central
  counterexample is clean: the model with the best likelihood had the least
  interpretable topics. Word intrusion became a standard evaluation, but
  adoption is not evidence (DP-005), and the follow-up work on automated
  coherence has not been filed here.
implementations: []
summary: >-
  Chang et al. (2009), [LIT-tmpmiyeb](../literature.d/LIT-tmpmiyeb.md) — topic models are used for their topics,
  but they are judged by held-out likelihood, which measures the probability
  of observations and ignores the representation. On NYT and Wikipedia, CTM
  had the best likelihood and the worst human scores. Test the latent space
  directly. Plant an improbable word among a topic's top words, or an
  improbable topic among a document's top topics, and measure how often
  people find it.
---

# SOTA-tmpa7058: When a model's latent space is meant to be read by people, measure its interpretability with a human task such as word or topic intrusion, not by held-out likelihood

## Source

Chang et al. (2009), [LIT-tmpmiyeb](../literature.d/LIT-tmpmiyeb.md). Read as [NOTE-tmppi0z8](../notes.d/NOTE-tmppi0z8.md).

## The practice

- **Decide what the model is for.** If the product is a prediction,
  likelihood measures it. If the product is a latent space people will
  browse, label or explore, likelihood does not measure that, and choosing
  models by it can select the less interpretable one
- **Word intrusion for components:** show a component's top words plus one
  word that is improbable in it and probable elsewhere, and score the rate at
  which people find the planted word
- **Topic intrusion for assignments:** show an item with its top components
  and one improbable component, and score how often people reject the
  planted one
- **Report both beside the likelihood**, per model and per number of
  components

## Conditions

- **Shown for topic models of text.** The argument, that a predictive score
  ignores the representation, applies to any latent space meant for people.
  The evidence is for topics
- **The strong form is not established.** "Better likelihood means worse
  topics" rests on one model, CTM. "Likelihood does not tell you" is what the
  data supports
