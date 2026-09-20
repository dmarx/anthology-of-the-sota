---
status: Proposed
promote_when: >-
  A measurement of alignment that is not pairwise-distance agreement — a
  stronger notion of representational sameness — showing convergence
  persists under it; or a third modality entering the converged regime, which
  would separate the hypothesis from a fact about vision and language. What
  would not settle it: more vision-language alignment measured the same way
  at larger scale, which is the trend already established and is what the
  conjecture is offered to explain.
title: 'Representations converge across architectures, objectives and modalities, and the endpoint is a model of what generated the data'
version: 1
tags:
- representation-and-encoding
date: '2026-09-20'
source:
- LIT-tmpglvdv
explains:
- SOTA-tmp121r8
summary: >-
  Huh et al. (2024), [LIT-tmpglvdv](../literature.d/LIT-tmpglvdv.md) — vision and language models measure
  distance between datapoints increasingly alike as they scale, across
  architectures and objectives. The conjecture is that they are converging on
  a representation of the joint distribution that generated the observations.
  The convergence is measured; the endpoint is proved only for a world of
  bijective observations.
---

# THEORY-tmpwwu1v: Representations converge across architectures, objectives and modalities, and the endpoint is a model of what generated the data
<!-- inactive-ok-file: SOTA-tmp121r8 — Proposed, and filed in this same contribution as the practice this account underwrites; also named in `explains:` -->

## Source

Huh et al. (2024), [LIT-tmpglvdv](../literature.d/LIT-tmpglvdv.md) — [ARXIV-2405.07987](https://arxiv.org/abs/2405.07987).

## Two claims, and the record should keep them apart

**The convergence is measured.** Vision models and language models agree
increasingly about pairwise distances between datapoints as they get larger,
and the agreement spans architectures, objectives and datasets. Prior results
line up with it: a model trained on ImageNet aligns with one trained on
Places-365 with performance retained; early layers are more interchangeable
than later ones; same-architecture models land in the same weight basin up to
permutation, which is why merging works at all.

**The endpoint is conjectured.** That models are converging *on a
representation of the world that generated the data* — the platonic
representation — is a hypothesis with a proof in an idealised setting only.
In a world of discrete events with **bijective** observation functions,
contrastive learners converge to the same kernel whichever projection they
see. Real observation is neither discrete nor bijective.

A document that ran the two together would be claiming a conjecture is
measured, which is the available mistake here and the reason this is
`Proposed` rather than `Active` while its first half is well supported.

## What could have gone otherwise

The convergence could have been an artefact of shared training data, shared
architecture or shared inductive bias; the interesting cases — a vision model
and a language model with none of those in common — are the ones where it
persists.

And the authors probe their own assumption rather than around it. Bijectivity
predicts that a *more informative* observation should align better. Varying
caption density on fixed images: denser captions align better with the visual
representation. That is the prediction the weakest premise makes, measured,
in the direction that would have embarrassed them.

## What this does not say

**It does not say two models converge when they saw different information.**
Language can state "I believe in the freedom of speech" and an image cannot.
The authors propose the nuanced form themselves: alignment capped by the
mutual information between the signals and by each model's capacity. Whether
that cap matters in practice is open — CLIP is optimised to capture only the
shared information and is nonetheless strong on pure vision tasks.

**It does not say convergence is happening everywhere.** Robotics has no
standardised world-state representation, which the authors attribute to a
hardware-driven data bottleneck rather than to anything about the hypothesis.
Two modalities is the evidence.

**It does not establish the mechanism.** Three pressures are offered — task
diversity, data diversity, and the simplicity bias of larger models — as
arguments, none isolated by intervention.

**Alignment is pairwise-distance agreement**, which is a weak notion of
sameness. Two representations can agree on every pairwise distance and still
differ in ways a downstream task would notice, and nothing here rules that
out.

**And the hallucination implication is not a finding.** That scale should
reduce hallucination and bias amplification follows from the conjecture and
is explicitly conditioned on training data being a sufficiently lossless and
diverse set of measurements. It is the claim most likely to be quoted without
its condition.

## What it underwrites

[SOTA-tmp121r8](../practices.d/SOTA-tmp121r8.md) — train on a second modality even when the target is
single-modality. That practice follows from the conjecture rather than from
the measurement, which is why it is `Proposed` too, and why its conditions
name this account's bijectivity assumption rather than hiding behind it.

## Why `Proposed`

Because the interesting half is the conjecture and the conjecture's proof is
for a world nobody trains in. What is `Active`-grade here is "representations
are converging", which on its own is a survey finding rather than an
explanation. `promote_when:` asks for the two things that would make the
account carry its own weight: a stronger notion of alignment that survives,
and a third modality entering the regime.
