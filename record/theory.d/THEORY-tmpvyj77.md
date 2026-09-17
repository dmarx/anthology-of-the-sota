---
status: Proposed
promote_when: >-
  A stage boundary predicted in advance and then confirmed by an independent
  intervention — for instance, a model family where the framework says
  detokenization should end at a given depth and a targeted ablation there
  degrades local-context integration specifically, while the same ablation one
  stage later does not. What would NOT satisfy this: another model family
  showing the same smooth depth-dependent curves, which is the observation the
  framework exists to interpret; or a new metric whose profile is read off as
  agreeing with stage boundaries drawn after the fact.
title: 'Depth-dependent computation in a transformer falls into four stages, of which detokenization is the first'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-17'
source:
- LIT-tmpyn738
explains: []
summary: >-
  Lad et al. (2024), [LIT-tmpyn738](../literature.d/LIT-tmpyn738.md) — the reading the authors put on their own
  localized-sensitivity result, and they put a question mark in the title.
  Four stages: detokenization lifts raw token embeddings into contextual ones
  by integrating local context; feature engineering refines task and entity
  features; prediction ensembling aggregates hidden states toward next-token
  predictions; residual sharpening suppresses irrelevant features at the end.
  The fourth carries a real experiment. The boundaries are approximate by the
  authors' own account, and stages may co-occur in one layer.
---

# THEORY-tmpvyj77: Depth-dependent computation in a transformer falls into four stages, of which detokenization is the first

## Source

Lad et al. (2024), [LIT-tmpyn738](../literature.d/LIT-tmpyn738.md) —
[ARXIV-2406.19384](https://arxiv.org/abs/2406.19384).

## What the account says

Four stages, hypothesized across five model families from the
localized-sensitivity result in [THEORY-tmp7jm1a](THEORY-tmp7jm1a.md):

1. **Detokenization** — local context is integrated to lift raw token
   embeddings into higher-level representations.
2. **Feature engineering** — task- and entity-specific features are
   iteratively refined.
3. **Prediction ensembling** — hidden states are aggregated into plausible
   next-token predictions.
4. **Residual sharpening** — irrelevant features are suppressed to finalize
   the output distribution.

The framework is offered as a resolution of a standing tension the paper names
in its introduction: **iterative inference**, where every layer nudges the same
distribution, against the **circuit hypothesis**, where components have
delineated specialized roles. Stages are the shape that would let both be
partly right — specialization between stages, iteration within them.

## What is actually measured, and what is inferred

**Stage 4 carries an experiment, and it is the strongest part.** Duplicating
blocks of layers in the latter half of a model **consistently lowers output
entropy** against baseline, and repeats at 80-90% depth improve benchmark
performance. That is a prediction with a direction that could have come out
the other way, and it did not. It is supported by a measured rise in
suppression neurons near the end of the network, outstripping prediction
neurons in the final few layers.

**Stage 1 rests on a structural argument plus other people's results.** The
first layer is the only one mapping from the embedding basis into the residual
stream and is a function of the current token alone — so ablating it makes the
rest of the network blind to local context. What happens next, the
concatenation of nearby tokens belonging to the same word or entity, is
imported from prior work rather than established here.

**Stages 2 and 3 are read off depth-dependent curves.** They are consistent
with the measurements and they are not independently tested.

So the four stages are not four findings. They are one measurement, one
experiment, one structural argument and two interpolations, and the status
here reflects that rather than the framework's plausibility.

## What this does not say

**The authors hedge it themselves, in the title and in the limitations.**
Stage boundaries are approximate; multiple stages may co-occur within a single
layer; the framework reflects aggregate trends while individual tokens may
follow distinct paths; model-specific differences are not isolated. A
framework whose boundaries are approximate and whose stages overlap is
difficult to falsify, which is why `promote_when` above asks for a boundary
predicted *before* it is tested.

**It does not establish that detokenization is a stage rather than an
artifact of where the tokenizer split things.** The strong version — that a
network must spend early depth reassembling units its vocabulary broke — is
the interesting claim and is not what was shown. The direct evidence for it
is the detokenization and inner-lexicon line (`ARXIV-2410.05864`,
`ARXIV-2406.20086`), which this paper cites and **the record does not hold**.

**It does not connect to the signal-side claim, yet.**
[THEORY-tmprceog](THEORY-tmprceog.md) says the lexical unit in English is
delimited by construction rather than frequency, which is what a
frequency-merge vocabulary cannot represent. This says early layers integrate
local context into coherent units. Those two fit together suggestively and
neither was measured against the other; treating the pair as a single account
of "the network repairs what the tokenizer broke" would be the record
asserting a result nobody has produced.

**And it is not a claim about where to cut a model.** No practice follows —
see the same section in [THEORY-tmp7jm1a](THEORY-tmp7jm1a.md).
