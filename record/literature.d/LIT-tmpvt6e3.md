---
status: Active
title: 'Scaling Laws for Fact Memorization of Large Language Models'
version: 1
tags:
- analysis-and-evaluation
- training-optimization
date: '2026-09-20'
published: '2024-06-01'
arxiv: '2406.15720'
first_author: 'Lu'
keywords:
- 'fact-memorization'
- 'model-capacity'
- 'scaling-laws'
- 'retrieval-augmentation'
- 'wikidata'
implementations: []
summary: >-
  Lu et al. (2024), [ARXIV-2406.15720](https://arxiv.org/abs/2406.15720). Fact capacity scales linearly
  with model size and saturates in training epochs along a negative
  exponential. Extrapolated, memorising all 15B Wikidata triples wants about
  1000B non-embedding parameters trained for 100 epochs. Redundant facts cost
  full price unless they share direction and structure, so parameters are an
  expensive place to keep a knowledge base.
---

# LIT-tmpvt6e3: Scaling Laws for Fact Memorization of Large Language Models
<!-- inactive-ok-file: THEORY-025 — Proposed, and the account this measurement corroborates through a second instrument -->

## Key takeaways

- **Two laws, in different variables.** Fact capacity — the maximum number of
  triples a model recalls accurately — is **linear in model size** at fixed
  epochs, and **negative-exponential in epochs**: rising then saturating.
- **The extrapolation is the headline and it is a negative result.**
  Memorising all of Wikidata's ~15B triples would want roughly **1000B
  non-embedding parameters trained for 100 epochs**. Not impossible in
  principle; implausible as a use of a pretraining budget.
- **Facts need far more than one epoch**, which makes them much more
  expensive per unit than the general-knowledge learning that happens in a
  single pass over pretraining data.
- **Redundant facts do not compress.** "Trump is Ivanka's father" and
  "Ivanka is Trump's daughter" are derivable from one another, and the model
  pays for both — memorisation rate for redundant and non-redundant sets of
  the same size is similar. Only when correlated facts share **direction and
  structure** does the model store them together.
- **Generalisation to unseen facts exists and scales like ordinary
  pretraining** — a Kaplan-shaped law. How well it works depends on the fact
  *type*, and the relationship is qualitative but consistent: the fact types
  easiest to memorise are the ones the model generalises best on, which the
  authors read as both being driven by input-output correlation strength.
- Models preferentially memorise **frequent** and **difficult** facts.

## Standing in the anthology

**It is a second, independent measurement of the linear-in-parameters
capacity law [THEORY-025](../theory.d/THEORY-025.md) rests on, in different units.** That account
measures storage in bits, on uniform random bitstrings where generalisation
is impossible, and gets ~3.6 bits per parameter linear in parameter count.
This measures storage in *facts*, on Wikidata, where generalisation is
possible and is separately quantified — and gets the same shape.

Two measurements of one quantity through different instruments agreeing on
the functional form is better evidence than either alone, and the record
should say so in both places. What neither supplies is the conversion: how
many bits a fact costs, which is the number that would let the two be checked
against each other rather than merely rhyming.

**It sources a recommendation the record has been missing.** [LIT-060](LIT-060.md) is
RETRO, which the record holds — and the only practice drawn from it is
[SOTA-197](../practices.d/SOTA-197.md), about contamination in evaluation. The record has the paper that
established retrieval-augmented pretraining works and no practice saying to
use it. This supplies the argument that makes the recommendation sharp: the
parameters are not merely a worse place to keep facts, they are a
quantifiably worse place, and the redundancy result says the inefficiency
compounds with how real corpora are actually written. [SOTA-tmppfvpd](../practices.d/SOTA-tmppfvpd.md) is the
practice.

**The generalisation result cuts the other way and should not be lost.**
Facts of some types transfer to unseen instances, at ordinary pretraining
scaling. So "do not memorise facts in parameters" is advice about a
*knowledge base*, not about factual competence, and a reader who takes it as
the latter has over-read it.
