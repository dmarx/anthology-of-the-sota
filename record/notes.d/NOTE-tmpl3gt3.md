---
status: Read
paper: LIT-tmppbfp5
title: 'Evolutionary Strategies lead to Catastrophic Forgetting in LLMs'
version: 1
tags:
- adaptation-and-tuning
date: '2026-09-15'
summary: >-
  The first independent replication attempt of ES-beats-GRPO, which fails —
  ES lands close but GRPO stays ahead on three of four settings at 1B and
  1.5B — and the first measurement of what ES costs on a held-out capability:
  HellaSwag declines steadily as Countdown training continues past the point
  Countdown itself converged.
---

# NOTE-tmpl3gt3: Evolutionary Strategies lead to Catastrophic Forgetting in LLMs

## Contribution

Two things, and the paper leads with the wrong one for this record's purposes.
Its stated contribution is the forgetting curve — the first measurement of
what ES post-training costs on a capability nobody is training. Its unstated
contribution is that it is the first independent attempt to reproduce the
ES-beats-GRPO result and does not reproduce it.

## Key insight

**The forgetting is concentrated in the part of training that buys nothing.**
ES reaches near-maximum Countdown accuracy by roughly 200 iterations. The run
continues to 500. Across that stretch, new-task accuracy is flat and
held-out HellaSwag keeps falling — which is what makes the Pareto front convex
rather than a straight trade. So the headline "ES causes catastrophic
forgetting" is, on the paper's own data, closer to *ES keeps moving after it
has stopped learning, and the movement costs something*. That distinction is
the difference between a reason not to use ES and a reason to stop it on time.

## Assumptions

- **Verifiable, rule-based rewards** throughout; answers extracted by regex
  from the final 300 characters of the response.
- **A single held-out benchmark stands in for "prior ability"** — HellaSwag,
  and the authors flag this as a limitation in those terms.
- **Sparsity is defined as the fraction of update coordinates below a fixed
  magnitude threshold**, following prior work. This is a property of the raw
  update, not of which coordinates carry function.
- **The ES implementation is a replication of the original authors'**, with
  two documented deviations: fp16 rather than bf16, and the Qwen chat template
  applied to task prompts. Runs were done with and without the template.
- Compute budgets are matched between ES and GRPO.

## Key results

- **Accuracy.** Across Countdown, GSM8K, MATH and OlympiadBench on
  Qwen2.5-1.5B-Instruct and Llama-3.2-1B-Instruct, "GRPO still outperforms ES
  for all but the GSM8K dataset with Llama-3.2-1B model". ES is close
  everywhere — the authors' framing is that this establishes ES as viable, not
  that it fails.
- **Convergence speed.** For all tasks except Countdown, ES reaches peak
  performance in a similar number of update steps to GRPO.
- **Forgetting.** On Qwen2.5-1.5B-Instruct trained on Countdown, HellaSwag
  declines systematically with iterations, tracing a **convex Pareto front**;
  ES reaches near-maximum Countdown by ~200 iterations and the decline
  continues past it.
- **Drift.** Frobenius norm between checkpoints grows monotonically with
  iterations for both methods. After 500 iterations ES's is **on the order of
  1000× GRPO's**, and the paper reports a clear association between the norm
  increases and the prior-task decline.
- **Sparsity.** GRPO updates are near **95% sparse** across all parameter
  types and layers. ES updates are dense almost everywhere, with LayerNorm the
  most sparse exception — and the paper notes LayerNorm holds a negligible
  parameter count.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | ES reaches accuracy close to GRPO on math and reasoning at matched compute | strong | four tasks, two models, code and checkpoints released |
| C2 | GRPO outperforms ES on three of four settings | moderate | measured, but the authors themselves name implementation and protocol differences as possible causes |
| C3 | ES training past target-task convergence degrades a held-out capability | strong | the convex Pareto front, and the 200-vs-500 iteration gap is the cleanest part of it |
| C4 | ES parameter drift is ~1000x GRPO's | strong | direct measurement, one task, one model |
| C5 | ES updates are much denser than GRPO's | strong for the threshold definition used | and see the caveat below — a different sparsity question gets a different answer |
| C6 | The large dense drift *causes* the forgetting | weak | association across a single training run; no intervention holds drift fixed |

## Method

Replicate ES post-training, extend the comparison from Countdown to GSM8K,
MATH and OlympiadBench, run both methods at matched compute on two models, and
evaluate held-out HellaSwag across the ES and GRPO training trajectories.
Analyse update Frobenius norm between checkpoints and layerwise update
sparsity, grouped by architectural component — attention projections, the
attention output projection, MLP layers, LayerNorms — and aggregated by layer
index.

## Concepts

- **Forgetting curve** — prior-task accuracy as a function of new-task
  training iterations; the object this paper is built to produce.
- **Update sparsity** — percentage of update coordinates below a fixed
  magnitude threshold. Higher means fewer parameters meaningfully moved.
- **Convex Pareto front** — the shape that says the trade is getting worse:
  late iterations cost prior-task accuracy without buying new-task accuracy.

## Connections

It positions itself against the ES-at-scale result directly, extending that
paper's task set and reporting a different ordering. Its framing is continual
learning — the motivation is deployment-time adaptation, where forgetting is
disqualifying rather than merely unfortunate. Lineage is on the LIT.

## Recommendations

<!-- inactive-ok-block: SOTA-tmpdcmgg — Proposed, filed from this reading in this same change -->
- **R1** — Stop ES training when the target task converges; the drift keeps
  accumulating and the gains do not. *Topic:* post-training. *Strength:*
  strong on this paper's own data. Filed as [SOTA-tmpdcmgg](../practices.d/SOTA-tmpdcmgg.md).
- **R2** — Report a held-out capability alongside the target metric for any
  gradient-free post-training run. *Topic:* evaluation. *Strength:* strong.
- **R3** — Do not treat ES as drop-in for continual or online learning without
  a drift control. *Topic:* post-training. *Strength:* moderate, and it is the
  paper's own conclusion.

## Bearing on the record

<!-- inactive-ok-block: SOTA-154 is Active, and this paragraph is the
     evidence against it that makes its consensus contested -->
**The independent negative result [SOTA-154](../practices.d/SOTA-154.md) was missing.** Until this note
the case against that practice was [LIT-231](../literature.d/LIT-231.md)'s, which argues from lemmas and
never runs full-parameter ES at scale. This runs it, extends the task set, and
reports GRPO ahead. It is now a second `contested_by:`.

**It is also the paper [LIT-230](../literature.d/LIT-230.md)'s entire RQ2 is a reply to, and the record
held the reply first.** That is [DP-004](../../docs/design-principles.md#dp-4) in its purest form: the citation graph
was followed forward from a 2026 paper and never backward, so the record
acquired an answer to a question it had not filed.

**The contradiction with [LIT-230](../literature.d/LIT-230.md) is narrower than the headlines.** Both
measure the same drift; this one calls the updates dense, that one calls the
*gains* sparse. Those are different questions and both answers can hold —
most coordinates move a little, few matter. The horizons differ too, and that
is probably the substance: [LIT-230](../literature.d/LIT-230.md) evaluates at a single-task horizon and
finds no broad forgetting, while this trains 2.5× past convergence.

<!-- inactive-ok-block: THEORY-006 — Proposed, named as the account whose
     scale boundary this paper's models sit under -->
**Its models are at 1.5B and below**, which now makes three papers in this
line whose negative results sit at or under [THEORY-006](../theory.d/THEORY-006.md)'s boundary, with no
negative reported above it.

## Limitations

Stated: the single held-out benchmark, and that the relative-performance
difference from prior work may come from GRPO implementation, hyperparameters
or evaluation protocol. From this reading: the causal claim from drift to
forgetting is an association within one run; the sparsity threshold is
inherited rather than justified; and 500 iterations on a task that converges
at 200 is a choice that shapes the headline.

## Open questions

- **Does the forgetting appear at all if training stops at convergence?** The
  paper's own data suggests much of it would not. Nobody has run it.
- **Does the failed replication survive at 4B and above?** Every positive in
  this line is above 1.5B and every negative is at or below it, and no paper
  has tested both sides of that line in one protocol.
- **Is the drift or the density the operative variable?** Both move together
  here. [LIT-tmp4w505](../literature.d/LIT-tmp4w505.md) later argues neither is, and that the relevant quantity
  is how much of the drift lies off the loss manifold.
