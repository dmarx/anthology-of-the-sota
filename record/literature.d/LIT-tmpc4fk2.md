---
status: Active
title: Emergent Abilities of Large Language Models
version: 1
tags:
- analysis-and-evaluation
- training-optimization
- in-context-learning
date: '2026-09-21'
published: '2022-06-01'
arxiv: '2206.07682'
first_author: 'Wei'
keywords:
- 'emergent-abilities'
- 'scaling'
- 'phase-transition'
- 'few-shot-prompting'
- 'big-bench'
implementations: []
summary: >-
  Wei et al. (2022), [ARXIV-2206.07682](https://arxiv.org/abs/2206.07682). Names and defines
  *emergent abilities* — present in larger models, absent in smaller ones, and
  therefore not predictable by extrapolating a scaling law. A survey of
  existing curves rather than new experiments: eight few-shot examples across
  five model families, plus prompting strategies that only help past a
  threshold. Section 5.1 raises the metric explanation itself and argues
  against it on two specific grounds.
corrected_by:
- LIT-tmpgnhq2
---

# LIT-tmpc4fk2: Emergent Abilities of Large Language Models

## Why it's here

It is the paper the word comes from, and the object of the dispute
[SOTA-200](../practices.d/SOTA-200.md) tells you to enter. The record recommended checking whether
an emergent capability is a metric artefact before it held the paper that
made the emergence claim, which is a gap in the citation graph rather than a
disagreement about anything.

Worth reading for its own §5.1, which is not what the paper is usually
summarized as saying. The authors raise the metric explanation, run the
cross-entropy analysis, confirm that cross-entropy improves while the
downstream metric is flat, and then give two reasons they do not think that
settles it. Both reasons are checkable, and one of them was later checked.

## What it claims

The definition is deliberately narrow: *an ability is emergent if it is not
present in smaller models but is present in larger models* — so the curve is
near-random until a threshold and substantially above random after it, and
extrapolating the small models would not have found the threshold. The paper
calls this a phase transition and is explicit that the *scale* at which it
appears is not a property of the ability: better data moves it, and it "may
be wise to view emergence as a function of many correlated variables".

Eight few-shot examples (Fig. 2) across five families: BIG-Bench arithmetic,
IPA transliteration, word unscrambling and Persian QA; TruthfulQA; grounded
conceptual mappings; MMLU; and Word in Context. Section 4 adds prompting and
finetuning strategies — chain of thought among them — that are flat or
harmful below a scale and help above it.

The WiC history is the paper's best argument and is easy to miss. GPT-3 at
175B failed it, and Brown et al. proposed the autoregressive objective as the
cause and a bidirectional model as the remedy. PaLM at 540B then cleared it
with no architectural change at all. That is a documented case of scale
falsifying a published architectural diagnosis.

## What it already concedes

Section 5.1 is where the paper meets its own best objection:

> using exact string match as the evaluation metric for long-sequence targets
> may disguise compounding incremental improvements as emergence.

It then declines the explanation on two grounds:

1. **The intermediate steps also emerge.** "The jump in final answer accuracy
   does not explain why the quality of intermediate steps suddenly emerges to
   above random."
2. **Many of the tasks are classification.** Partial-credit arguments are "at
   best an incomplete explanation, because emergent abilities are still
   observed on many classification tasks" — Fig. 2 D–H.

The second was answered directly by [LIT-tmpgnhq2](LIT-tmpgnhq2.md): classification tasks are
scored by Multiple Choice Grade, which is *discontinuous* rather than
partial-credit-denying, so "it is a classification task" does not escape the
metric explanation. The first has not been answered and is still the sharpest
open objection.

The paper also reports its own cross-entropy analysis (App. A), which
reproduces BIG-Bench's finding that log-likelihood improves smoothly where
the downstream metric does not — and says plainly that this "does not explain
why downstream metrics are emergent or enable us to predict the scale".

## Conditions

**It is a survey, not an experiment.** Every curve is from prior work;
nothing here is a controlled comparison the authors ran, and the metric on
each curve is whichever metric that work used. That is the whole opening for
[LIT-tmpgnhq2](LIT-tmpgnhq2.md), and it is also why a reader should not treat the eight
examples as eight independent confirmations.

**Scale is proxied by training FLOPs**, with parameters in an appendix, on
the stated grounds that dense Transformer families scale the two roughly
together — which the paper notes is false for Chinchilla vs Gopher and for
sparse mixtures.

**"Above random" is doing structural work.** The definition needs a floor to
be near, so it is defined for tasks with a chance baseline and reported
against it. A task with no natural chance rate has no threshold to cross.
