---
status: Active
title: 'Deep Learning and the Information Bottleneck Principle'
version: 1
tags:
- analysis-and-evaluation
- representation-and-encoding
- model-architecture
date: '2026-09-22'
published: '2015-03-09'
arxiv: '1503.02406'
first_author: 'Tishby'
keywords:
- 'information bottleneck'
- 'information plane'
- 'mutual information'
- 'generalization bounds'
- 'deep neural networks'
implementations: []
summary: >-
  Tishby and Zaslavsky (2015), [ARXIV-1503.02406](https://arxiv.org/abs/1503.02406) — the five-page
  position paper the whole information-bottleneck line descends from. It
  proposes quantifying every layer by `I(X;h)` and `I(Y;h)`, draws the
  information plane as an explicitly **qualitative** figure with a
  **hypothesized** layer path, and states that approaching the IB limit
  **requires stochastic mapping between the layers** — the condition its
  successors were later refuted for dropping. Read as
  NOTE-tmpguwlt.
---

# LIT-tmpyer2o: Deep Learning and the Information Bottleneck Principle

<!-- inactive-ok-file: THEORY-058 — Proposed, cited as the account this record filed from the downstream dispute, whose objection this paper is shown to have anticipated; it is the live reading of that dispute, not a retired one. -->

Tishby and Zaslavsky (2015) —
[ARXIV-1503.02406](https://arxiv.org/abs/1503.02406), IEEE Information Theory
Workshop 2015. Read as [NOTE-tmpguwlt](../notes.d/NOTE-tmpguwlt.md).

## Key takeaways

- **The proposal.** Quantify any DNN by the mutual information between each
  layer and the input and output variables, and treat the network as a
  sequence of points on an information plane.
- **The claims it makes for that frame:** optimal information-theoretic limits
  and finite-sample generalization bounds; the optimal architecture — number of
  layers, features per layer — related to **bifurcation points** of the IB
  tradeoff; hierarchical representations corresponding to **structural phase
  transitions** along the information curve.
- **The famous picture is labelled as a hypothesis.** Figure 2 is "a
  **qualitative** information plane, with a **hypothesized** path of the layers
  in a typical DNN". The authors' own words, in the caption.
- **And it names the condition.** "Getting closer to the optimal limit requires
  **stochastic mapping between the layers**."
- **Five pages**, no experiments.

## Standing in the anthology

**It is the trunk under a dispute this record filed without it.** For
[#220](https://github.com/dmarx/anthology-of-the-sota/issues/220) the record took [LIT-508](LIT-508.md) (Shwartz-Ziv and Tishby's measurement),
[LIT-509](LIT-509.md) (Saxe et al.'s rebuttal) and [LIT-507](LIT-507.md)
(Chelombiev et al.'s counter-rebuttal), and produced
[THEORY-058](../theory.d/THEORY-058.md) and [SOTA-312](../practices.d/SOTA-312.md). The paper all
three are arguing about was not here.

**Reading it changes who is owed what.** The 2018 rebuttal's central objection
is that `I(X;T)` is ill-defined for a deterministic network and that the
reported compression is an artifact of the binning. This paper says the
optimum requires stochastic maps — so the assumption whose absence the
rebuttal turns on is stated in the founding paper, and dropped downstream.

**`Active`, and the reason is narrow.** Its proposal is live, its picture is
labelled a hypothesis, and what the record disputes is a later paper's
measurement rather than this one's framing. The claims it makes *beyond* the
framing — bifurcation points fixing the optimal depth, phase transitions on
the information curve — are unevidenced here and untested since, and the
reading says so.
