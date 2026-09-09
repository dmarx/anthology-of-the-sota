---
number: 172
status: Proposed
formerly:
- SOTA-tmpqgx8l
promote_when: >-
  A pretraining report that says its synthetic data was produced by editing
  human text rather than generating from a prompt, and reports what that
  bought; or an independent group reproducing the negative correlation
  between synthetic proportion and performance at a scale above this one's.
  What would not move it: a paper generating better synthetic data and
  reporting better results, which is the move this argues is the wrong one.
consensus: unreplicated
consensus_note: >-
  One group. The record's frontier reports use it from both ends without
  citing the mechanism — Kimi K3 rephrases its knowledge and mathematics
  corpora against a verified source, and DeepSeek-V4 filters batched
  auto-generated content out of the crawl "to mitigate the risk of model
  collapse" — but neither measures the effect this paper measures.
title: 'Build synthetic pretraining data by editing human text at the token level, not by generating from scratch'
version: 1
tags:
- data-pipeline
date: '2026-09-08'
published: '2024-12-01'
source:
- LIT-205
implementations: []
summary: >-
  Zhu et al. (2024), [LIT-205](../literature.d/LIT-205.md) — pretraining across proportions of synthetic
  data shows a *negative* correlation between the proportion and performance,
  caused by distributional shift and over-concentration of n-gram features.
  The remedy inverts the usual move: edit human data at the token level, so
  the result stays anchored to a real distribution and the test error is
  provably bounded.
---

# SOTA-172: Build synthetic pretraining data by editing human text at the token level, not by generating from scratch

## Source

Zhu et al. (2024), [LIT-205](../literature.d/LIT-205.md) — [ARXIV-2412.14689](https://arxiv.org/abs/2412.14689).

The premise is not hypothetical. As AI output proliferates, future models
will be trained on a blend of synthetic and human text whether or not anyone
chooses that, so the question is not whether to use synthetic data but what
happens when you do.

**What happens, measured.** Pretraining across different proportions of
synthetic data yields a **negative correlation** between the proportion and
performance. Statistical analysis locates why: distributional shift, and
over-concentration of n-gram features. Generated text is narrower than what
it imitates, and training on it narrows the next model further.

**The remedy inverts the usual move.** The instinct is to generate *better*
synthetic data. Instead: edit **human** data at the token level to produce
semi-synthetic data. Because the result stays anchored to a real
distribution, the authors prove the test error is bounded above — collapse is
prevented by construction rather than by filtering harder afterwards.

Validated on pretraining from scratch, continual pretraining and supervised
fine-tuning.

## Both ends of the pipeline, and the record uses both without saying so

<!-- inactive-ok-block: SOTA-124 — Proposed, named as the practice that leans
     on rephrasing without pricing it -->
- **Generation.** [SOTA-124](SOTA-124.md) and the recipes in [LIT-119](../literature.d/LIT-119.md) and [LIT-131](../literature.d/LIT-131.md) lean on
  *rephrasing* — Kimi K3 rephrases its knowledge and mathematics corpora with
  diverse prompting and verifies fidelity against the source. That is
  generation conditioned on human text, which is nearer to this paper's
  semi-synthetic prescription than to the pure synthesis it warns about. The
  difference is one of degree, and this practice is what makes the degree
  visible rather than a matter of taste.
- **Filtering.** DeepSeek-V4 ([LIT-139](../literature.d/LIT-139.md)) cites this paper for the other end:
  filtering batched auto-generated and templated content out of web data,
  explicitly "to mitigate the risk of model collapse".

So the record already had both uses — a reason to filter the crawl, and a
constraint on how to generate — and no document saying they are the same
finding.

## Conditions, and why this is Proposed

One group. The bound is proved for the semi-synthetic construction rather
than measured at frontier scale, and the negative correlation is measured at
this paper's scale rather than at the scale of the recipes that rephrase. The
practice is a constraint on *method*, and the record's adopters satisfy it by
accident rather than by design — which is exactly the situation `Proposed`
is for.

Read with the filtering-horizon practice drawn from [LIT-178](../literature.d/LIT-178.md), which
recommends rephrasing what a filter would discard at long token horizons:
that is the same operation, and this is the paper that says why it is safe
when generating from scratch is not.

## Known implementations

- None by name. Kimi K3's verified rephrasing and DeepSeek-V4's collapse
  filtering are the nearest things, and neither cites the construction.
