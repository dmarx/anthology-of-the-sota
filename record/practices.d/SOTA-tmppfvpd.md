---
status: Active
consensus: emerging
consensus_note: >-
  The cost measurement is one group's; that retrieval-augmented pretraining
  works is separately established and widely deployed. `emerging` rather than
  `converged` because the field's frontier models still put a great deal of
  factual knowledge in weights, so the recommendation describes a direction
  rather than a settled default.
title: 'Keep a knowledge base outside the weights; parameters are an expensive and lossy place to memorise facts'
version: 1
tags:
- inference-optimization
- training-optimization
date: '2026-09-20'
source:
# Lu et al. is the cost argument and the claim rests on it. LIT-060 is here
# because a recommendation to do X instead of Y needs X to be viable, and
# RETRO is the record's evidence that it is (ADR-017).
- LIT-tmpvt6e3
- LIT-060
introduced_by:
- LIT-tmpvt6e3
implementations:
- 'RETRO'
summary: >-
  Lu et al. (2024), [LIT-tmpvt6e3](../literature.d/LIT-tmpvt6e3.md) — fact capacity is linear in model size
  and saturates in epochs, and the extrapolation is damning: all of Wikidata
  would want about 1000B non-embedding parameters trained for 100 epochs.
  Derivable facts cost full price unless they happen to share direction and
  structure. Borgeaud et al., [LIT-060](../literature.d/LIT-060.md), is the record's evidence that the
  alternative works at scale.
---

# SOTA-tmppfvpd: Keep a knowledge base outside the weights; parameters are an expensive and lossy place to memorise facts
<!-- inactive-ok-file: THEORY-025 — Proposed, and named as the corroborating measurement in different units -->

## Source

Lu et al. (2024), [LIT-tmpvt6e3](../literature.d/LIT-tmpvt6e3.md) — [ARXIV-2406.15720](https://arxiv.org/abs/2406.15720). The cost argument, and
what this practice rests on.

Borgeaud et al. (2021), [LIT-060](../literature.d/LIT-060.md) — RETRO. Here because a recommendation to
do one thing instead of another needs the alternative to be viable, and this
is the record's evidence that it is.

## The price

Fact capacity is **linear in model size** and **negative-exponential in
training epochs** — rising, then saturating. Fitting both and extrapolating
to a real knowledge base: all ~15B Wikidata triples would want roughly
**1000B non-embedding parameters trained for 100 epochs**.

The constant is an extrapolation several orders of magnitude past the
measurements and should be read as an order of magnitude, not a number. The
conclusion survives that looseness comfortably.

Two things make it worse than the law alone says:

- **Facts want many epochs.** Far more than the single pass that general
  pretraining gets, so each fact costs more compute than the capacity figure
  suggests.
- **Redundant facts do not compress.** "Trump is Ivanka's father" and
  "Ivanka is Trump's daughter" are one fact to a person and two to the model:
  memorisation rate is the same for redundant and non-redundant sets of equal
  size. Only when correlated facts share direction *and* structure are they
  stored together. Real corpora are full of the same fact in many surface
  forms, and the model pays for each.

## What this is not saying

**It is not saying models cannot do facts.** The same paper shows models
generalise to *unseen* facts, with a scaling law it describes as close to
ordinary pretraining's, and with generalisability varying sharply by fact
type. The same quantity appears to drive both: fact types with strong
input-output correlation are easier to memorise and generalise better.

So the advice is about an **enumerable knowledge base** — the thing you could
have put in a database — not about factual competence. A reader who takes it
as the latter has over-read it, and would conclude wrongly that factual
capability must be bolted on rather than trained.

## A gap the record had

[LIT-060](../literature.d/LIT-060.md) has been in this record since early on, and the only practice
drawn from it is [SOTA-197](SOTA-197.md), about contamination in evaluation. The record
held the paper that established retrieval-augmented pretraining works and had
no practice saying to use it — an absence no query would have found, because
nothing was complaining about it.

## Why `Active`

Two independent halves. That parameters store facts linearly and expensively
is measured here and corroborated in different units by [THEORY-025](../theory.d/THEORY-025.md), which
gets ~3.6 bits per parameter on random bitstrings. That the alternative works
is established by [LIT-060](../literature.d/LIT-060.md) and by widespread deployment since.

## Conditions

**The extrapolation is the weakest link.** 1000B parameters at 100 epochs
comes from a fit extended several orders of magnitude. The qualitative
conclusion — a general-purpose pretraining budget is the wrong place to buy
this — does not depend on the constant.

Capacity here is measured under deliberate repeated-epoch training on fact
sets. Whether the same law governs the incidental acquisition that happens
during a single pretraining pass is not established, and that is the regime
most facts actually arrive in.

Wikidata triples are unusually clean. A knowledge base that does not
decompose into triples may not price the same way.

And the recommendation has a precondition the cost argument cannot supply: a
retrieval path has to exist, be maintained, and be fast enough at serving
time. This practice says where the facts should not live; it does not cost
the place they should.

## Known implementations

- RETRO ([LIT-060](../literature.d/LIT-060.md))
