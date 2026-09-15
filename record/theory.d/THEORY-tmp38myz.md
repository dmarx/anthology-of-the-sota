---
status: Proposed
promote_when: >-
  The density measurement repeated by a group unconnected to the authors, on
  a model family other than Qwen2.5, with the scaling trend holding — or a
  mechanism that predicts where the transition sits rather than observing it.
  What would not satisfy this: a further post-training method that works and
  is read back as evidence for the account, which is the direction this
  document is most likely to be misused in.
title: 'Task-improving weight perturbations are dense around pretrained weights, and denser the larger the model'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-15'
source:
- LIT-tmphm6g2
explains:
- SOTA-154
- SOTA-tmpm80i3
summary: >-
  Gan and Isola (2026), [LIT-tmphm6g2](../literature.d/LIT-tmphm6g2.md) — the fraction of random Gaussian weight
  perturbations that improve a downstream task rises monotonically with model
  scale, from 0% at 0.5B to 64% at 32B on GSM8K, and the perturbations that
  help are task specialists rather than uniform improvements. It is the
  record's account of why gradient-free post-training works at all, measured
  on one model family by one group.
---

# THEORY-tmp38myz: Task-improving weight perturbations are dense around pretrained weights, and denser the larger the model

## Source

Gan and Isola (2026), [LIT-tmphm6g2](../literature.d/LIT-tmphm6g2.md).

## What was actually shown

Two measurements, and the second is the one that makes the first mean
something.

**Density.** For a performance metric `s` and a Gaussian neighbourhood of the
pretrained weights `θ`, define `δ(m) = P[s(θ+ε) ≥ s(θ)+m]` with
`ε ~ N(0, σ²I)` — the hit rate of guessing at margin `m`. Sampling Qwen2.5
instruction-tuned models from 0.5B to 32B at σ = 1e-3, `δ` rises
monotonically with scale, at every margin tested. On GSM8K the fraction of
perturbations at least matching the base model goes from 0% at 0.5B to 64% at
32B. Projected into 2D, the small models sit on a local peak of task accuracy
and the large ones in a valley surrounded by higher ground.

**Diversity.** Take the percentile-rank matrix of 500 perturbations over
seven tasks in four domains, correlate its columns, and read the spread of
that correlation matrix's spectrum — the paper's "spectral discordance". It
too rises with model size. The perturbation that most improves one task tends
to *hurt* the others; a PCA of the per-seed performance vectors separates
into clusters with complementary strengths. So the nearby solutions are
specialists, and the neighbourhood is not simply a region where the base
model happened to be undertrained.

**What could have come out the other way.** The diversity measurement is a
real test of a real alternative: if the pretrained weights were merely a poor
model that anything nearby improved, the task rankings would have been
parallel rather than orthogonal, and the discordance statistic would have
fallen rather than risen with scale. It does not. The density measurement is
falsifiable in the other direction and the paper reports where: at 0.5B and
at GPT-2 scale there is no thicket, and starting from un-pretrained weights
there is none at any scale.

**A minimal setting where the same three regimes appear.** An MLP next-value
predictor over a mixture of 1D signal families reproduces
needle-in-a-haystack (no pretraining), thicket (pretraining on the mixture)
and a third regime the LLM experiments do not show: a *plateau*, where
pretraining on one signal family alone leaves the base model already at
ceiling and perturbation buys nothing. That the effect survives the removal
of language, scale and the transformer is the strongest evidence the account
is about pretraining rather than about LLMs.

## What this explains, and how much

It is an account of why the gradient-free post-training line works at all.
[SOTA-154](../practices.d/SOTA-154.md) recommends evolution strategies over policy-gradient RL on the
evidence that it wins a tilted comparison; nothing in the record said *why* a
method with no gradient should be able to find anything in a billion
dimensions. This says what property of the search space makes it possible,
and predicts the boundary: below roughly 1.5B parameters, or from an
untrained initialization, the property is absent and the methods that depend
on it should fail. That prediction is testable and the paper tests one side
of it.

<!-- inactive-ok-block: SOTA-tmpm80i3 — Proposed, filed from the same paper
     in this same change; this paragraph is about how far the two should be
     held together, which is what the citation is for -->
For [SOTA-tmpm80i3](../practices.d/SOTA-tmpm80i3.md) the relation is tighter, because the practice is the
account's own probe. Density is what makes guessing land on anything;
diversity is what makes majority-voting the survivors better than taking the
best one. The practice's two halves are the theory's two measurements, which
is a reason to hold the practice no more firmly than the account.

## What this does not say

**It does not say what a "task expert" is.** Expertise here is defined as
doing well on a benchmark, and the paper's own decomposition finds that a
substantial share of the improvement is the model emitting an answer the
strict checker accepts rather than solving anything it could not solve
before. Some of the thicket is a thicket of output formats. The paper says
this in its own words and reports the same of GRPO, so it is not a defect of
the measurement — but "diverse task experts are dense" reads as a claim about
capability and is partly a claim about formatting.

**It does not explain the mechanism, and says so.** What about pretraining
produces the density — the objective, the data variety, the learning dynamics
— is left open. The 1D experiment points at variety in the pretraining
distribution and does not establish it for language models. An account that
cannot yet say why the transition happens also cannot say where it happens,
and "around 1.5B" is an observation on one family and one task, not a
threshold.

**It does not license reading a successful post-training method as
confirmation.** The account predicts that gradient-free search works because
solutions are dense; a method working is consistent with that and with
several other explanations, including that the benchmark is easy to move.
Only the direct measurement of `δ` is evidence for the account, and that has
been made once, by one group, on one model family.

<!-- inactive-ok-block: THEORY-002 — Proposed, and this paragraph exists to
     refuse a link between the two accounts; naming it is the point -->
**It does not reach the lottery-ticket line, in either direction.**
[THEORY-002](THEORY-002.md) is about random initialization, where good subnetworks are rare.
This is about a pretrained starting point. The paper calls the two compatible
and different in regime, and that is all the record should carry: neither is
a correction of the other, and the thicket claim is not evidence about what
happens at initialization.
