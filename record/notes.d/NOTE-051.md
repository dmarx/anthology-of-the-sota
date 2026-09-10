---
number: 51
status: Read
formerly:
- NOTE-tmpm1ry1
paper: LIT-077
title: 'Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-09'
summary: >-
  204 tasks from 450 authors, evaluated across dense and sparse models from millions to hundreds of billions of parameters, with expert human raters as the baseline. Its most useful finding is about measurement: tasks showing "breakthrough" behaviour at a critical scale tend to involve multiple steps or brittle metrics, while smooth ones are knowledge-heavy.
---

# NOTE-051: Beyond the Imitation Game: Quantifying and extrapolating the capabilities of language models

## Contribution

A deliberately very hard, very broad benchmark — **204 tasks, 450 authors, 132
institutions** — spanning linguistics, childhood development, mathematics,
common-sense reasoning, biology, physics, social bias and software development,
built because existing benchmarks were saturating and could not resolve what
models could and could not do.

Evaluated on OpenAI GPT models, Google dense transformers and Switch-style
sparse transformers, from millions to hundreds of billions of parameters, with
**a team of human expert raters performing every task** as the baseline.

## Key insight

The finding worth carrying is about **what kind of task produces an apparent
discontinuity**:

> tasks that improve gradually and predictably commonly involve a large
> knowledge or memorization component, whereas tasks that exhibit "breakthrough"
> behavior at a critical scale often involve multiple steps or components, **or
> brittle metrics**

Three of those causes are about the task and the fourth is about the
*measurement*. A multi-step task scored all-or-nothing improves invisibly until
every step works; that is a property of the metric, not of the model. The paper
formalises this as an axis it calls **linearity vs breakthroughness** and
categorises scaling behaviours along it.

The second finding is uncomfortable and clearly stated: **social bias typically
increases with scale in settings with ambiguous context** — though prompting for
neutrality substantially reduces it on `bbq_lite`. Scale makes some things worse
by default and the mitigation is a prompt.

## Assumptions

- Aggregate performance over 204 heterogeneous tasks is meaningful. Every task
  is weighted equally in the aggregate, which is a choice.
- Human expert raters are the right ceiling.
- **Contamination is addressed rather than assumed away**: training data for all
  models except PaLM predates the repository, so direct leakage is impossible;
  indirect leakage is acknowledged as possible, and a `training_on_test_set`
  task is provided for future models to probe it.

## Key results

- **Performance and calibration both improve with scale, and are poor in
  absolute terms** — and poor relative to human raters.
- **Performance is remarkably similar across model classes**, with benefits from
  sparsity. Architecture matters less than scale across a broad task set.
- **Breakthroughness correlates with multi-step structure or brittle metrics**;
  smoothness with knowledge and memorization.
- **Average performance improves with both compute scale and number of shots.**
- **Social bias increases with scale under ambiguous context**, and few-shot
  prompting for neutrality reduces it.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Model performance is poor in absolute terms and against human experts | strong | 204 tasks, expert baseline |
| C2 | Model class matters little compared to scale | strong | three families compared |
| C3 | Breakthrough behaviour tracks multi-step structure and brittle metrics | moderate | categorised across tasks; a correlation over a heterogeneous set |
| C4 | Social bias increases with scale under ambiguity | strong | measured |
| C5 | Prompting can reduce that bias | moderate | one task family, `bbq_lite` |
| C6 | Direct contamination is impossible for these models | strong | by construction, and stated with its limits |

## Method

Solicit tasks openly with a review process. Evaluate three model families across
scales, with and without few-shot examples. Have expert humans do every task.
Categorise per-task scaling curves by linearity and breakthroughness.

## Concepts

- **Linearity vs breakthroughness** — an axis for scaling curves, and the reason
  "emergence" claims need to state their metric.
- **Brittle metrics as a cause of apparent emergence** — the part that has aged
  best.
- **A benchmark that documents its own contamination exposure**, and ships a
  probe for future models.

## Connections

`LIT-085` (grokking), read in the same batch, is the other half of this: it
takes one apparently discontinuous capability, reverse-engineers the network,
and finds continuous progress underneath — and separately that the discontinuity
disappears in a different data regime. **Both papers conclude that apparent
discontinuity is often a property of the measurement or the regime.** One
argues it from 204 tasks, the other from one solved network.

`LIT-073`'s reading found the same lesson in a third place: MS-COCO could not
distinguish two text encoders that human raters could, so the paper built
DrawBench. **Three independent instances in this pass of "the benchmark was the
problem".**

## Recommendations

- **R1** — Before claiming a capability emerges at a scale, check whether the
  metric is all-or-nothing over multiple steps. *Topic:* analysis and
  evaluation. *Strength:* strong.
- **R2** — Report calibration alongside accuracy. *Strength:* moderate; this is
  one of the few large evaluations that does.
- **R3** — Expect bias to worsen with scale under ambiguity, and test the
  prompt-level mitigation rather than assuming scale fixes it. *Strength:*
  moderate.
- **R4** — State a benchmark's contamination exposure and ship a probe for it.
  *Strength:* strong, and cheap.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice.**
Retagged from `model-architecture` — a benchmark paper is not an architecture
paper — to `analysis-and-evaluation`.

R1 is the finding the record could use and does not have. The corpus contains
several claims of the form "capability X appears at scale Y", and this paper's
categorisation says a large share of such observations are metric artefacts.
Together with `LIT-085`'s data-fraction result and `LIT-073`'s DrawBench, the
reading pass has now produced three independent arguments that **the
measurement, not the model, produced the surprise** — which is a stronger case
for a practice than any one of them.

The document's takeaways — "comprehensive evaluation framework", "systematic
capability analysis", "extrapolation of model scaling", "novel benchmark
suite" — describe the artefact and none of its findings.

## Limitations

- 2022 models. The absolute results are of historical interest only; the
  methodology is what survives.
- Aggregating 204 unequal tasks into an average is a choice with consequences
  the paper does not fully unpack.
- C3 is a categorisation over a heterogeneous set, not a controlled experiment.
- Indirect contamination is acknowledged and not quantified.

## Open questions

- How much measured emergence is metric brittleness? The paper introduces the
  axis and does not put a number on the share, which is the question everyone
  cites it for.
