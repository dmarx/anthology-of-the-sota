---
number: 220
status: Read
formerly:
- NOTE-tmpnb7kf
paper: LIT-471
title: 'Emergence as a Mirage'
version: 1
date: '2026-09-21'
summary: >-
  Reading it: the strongest evidence is not the rebuttal of GPT-3's arithmetic
  curve but the vision experiments, where emergence is manufactured in models
  that had never shown it. The weakest part is what "mirage" gets read as —
  the paper explicitly declines the claim that emergence is impossible.
---

# NOTE-220: Emergence as a Mirage

## Contribution

An explanation for emergent abilities that requires nothing to happen inside
the model. Before it, the field had BIG-Bench's suspicion that metrics might
be implicated; after it, there is a mechanism with a functional form, three
tests of it, and a count of how much of the published evidence sits on the
two metrics the mechanism predicts. What is true afterwards that was not
before: you can take a published emergent curve, change nothing but the
scoring function, and watch it become smooth.

## Key insight

The metric is not merely coarse — it is a *transform*. Accuracy over an
`L`-token target composes the per-token success probability `L` times, so a
smooth `p(scale)` becomes `p^L`, which is flat then sharp on a log axis by
construction. Multiple Choice Grade is the step-function version of the same
thing. This is why "use a better benchmark" does not help and "use a
continuous metric on the same outputs" does: the outputs were never the
problem.

## Assumptions

- **Per-token cross entropy falls smoothly with scale.** Imported from
  scaling laws rather than shown here, and the paper is explicit that it does
  not need the power-law form specifically.
- **Token independence**, for the closed form `p^L`. The authors state it is
  false and claim only a qualitative match.
- **Emergence score as a screen.** The meta-analysis uses BIG-Bench's own
  emergence score to nominate triplets, then leans on the hand annotations
  for the load-bearing count.
- **Published curves are the evidence base.** Everything but GPT-3 and LaMDA
  is analysis of numbers other people reported.

## Key results

- **Fixed outputs, changed metric**: InstructGPT/GPT-3 (350M–175B) on 2-shot
  4-digit addition and 2-shot 2-digit multiplication shows emergence at 4–5
  digit targets under Accuracy and smooth improvement under Token Edit
  Distance. Outputs identical.
- **Better statistics**: with more test data, every model is above chance
  under Accuracy; the zeros were resolution.
- **Meta-analysis**: at most 5 of BIG-Bench's 39 preferred metrics show
  emergence by emergence score; 4/39 by hand annotation; **>92%** of
  hand-annotated emergent abilities fall under Multiple Choice Grade or
  Exact String Match.
- **LaMDA** loses its emergence when rescored under Brier Score.
- **Induced emergence**: CIFAR-100 autoencoders under a thresholded
  reconstruction count; Omniglot transformers under subset accuracy. Both
  produce sharp curves in architectures and domains with no prior emergence
  claims.
- **Multiple comparisons**: ≥220 tasks × ~40 metrics × ~10 families ≈ 10⁶
  triplets.

## Claims

Two claims, and they are not the same strength. The mechanism claim — a
nonlinear or discontinuous metric converts smooth into sharp — is
demonstrated conclusively, including constructively. The share claim — that
published emergent abilities are *mostly* this — rests on the >92% count,
which is a count of which metrics the claims sit under rather than a
rescoring of each claim.

## Method

Analytic model; rescoring of held outputs; meta-analysis over BIG-Bench's
published triplets and Wei et al.'s hand annotations; and construction of new
emergent curves in vision by choosing a discontinuous metric.

## Concepts

Nonlinear vs discontinuous metrics; *resolution* as the smallest measurable
interval, set by test-set size; proper scoring rules (Brier) as the continuous
counterpart of Multiple Choice Grade.

## Connections

- [LIT-077](../literature.d/LIT-077.md) hypothesized the metric role; this converts the
  hypothesis into predictions and tests them. `extends`.
- [LIT-470](../literature.d/LIT-470.md) is what it argues against, and specifically answers
  that paper's second §5.1 objection. `corrects`.
- [LIT-085](../literature.d/LIT-085.md) is the other half of [SOTA-200](../practices.d/SOTA-200.md)'s evidence and a different
  kind: grokking's discontinuity dissolves under a *regime* change (data
  fraction) rather than a metric change. Two mechanisms, same advice.
- [THEORY-039](../theory.d/THEORY-039.md) is the sibling account — the evaluation's auxiliary
  demands, which is about what the task asks of the model. This one is about
  the scoring function applied afterwards, and the two are independent.

## Bearing on the record

It supplies [SOTA-200](../practices.d/SOTA-200.md) with the source it was missing and, more usefully,
with a **cheap positive check**. The practice currently says finding the
continuous measure underneath is expensive — true of `LIT-085`'s progress
measures, which needed the network reverse-engineered first. It is not true
here: rescore the same outputs with Token Edit Distance, or use the proper
scoring rule the benchmark already ships. That is a real change to what the
practice recommends, not just a citation.

It also puts a number where the practice's `consensus_note` said there was
none — though the number is about which *metrics* carry the claims, which is
not quite the same as what share of emergence is artefactual.

## Limitations

**Sufficiency is not necessity.** Manufacturing emergence with a chosen metric
proves a metric can do it. It does not prove each published curve was made
that way, and the paper's own phrasing ("might likely be a mirage") concedes
this.

**The >92% is a property of the corpus, not of each claim.** Multiple Choice
Grade being the most common metric in a multiple-choice-heavy benchmark is
partly a fact about BIG-Bench.

**One family probed, by necessity.** The rest is downstream of what other
groups published — a limitation the paper turns into an argument for
releasing model outputs.

**It does not touch the intermediate-step objection**, which is
[LIT-470](../literature.d/LIT-470.md) §5.1's first reason and the one still standing.

## Open questions

- Does a continuous rescoring of MMLU, TruthfulQA and WiC — the curves this
  never reached — leave anything sharp?
- Caballero et al.'s broken scaling laws and Michaud et al.'s quantization
  model both predict real emergence. Neither is tested against this, and a
  test would have to distinguish a genuinely piecewise `p(scale)` from a
  smooth one seen through a step function.
- The paper's advice ("if you choose accuracy, have enough data to measure
  it") is a power-analysis prescription nobody has turned into a rule of
  thumb for benchmark construction.
