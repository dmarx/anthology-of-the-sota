---
number: 212
status: Read
formerly:
- NOTE-tmp3rkau
paper: LIT-466
title: 'The Illusion of Thinking'
version: 1
date: '2026-09-21'
summary: >-
  Controllable puzzles replace contaminated benchmarks; reasoning models
  collapse to zero past a threshold and reduce thinking tokens as they do.
  Reading it: the three-regime result is solid, and the collapse reading is
  contested on scoring grounds the paper does not address.
---

# NOTE-212: The Illusion of Thinking

## Contribution

Reasoning-model evaluation had been running on maths and coding benchmarks
that are contaminated and score only the final answer. This substitutes
controllable puzzle environments where compositional complexity is a dial and
the logical structure is held fixed, and where a simulator can check every
intermediate state in the reasoning trace. What is new afterwards is a
measurement of *how* performance changes with complexity rather than whether
a model passes, and a companion measurement of thinking-token spend along the
same axis.

## Key insight

Reasoning models do not degrade; they fall off a cliff, and just before the
cliff they start trying less. Thinking-token usage rises with complexity up
to a model-specific threshold and then declines — while budget remains
available. Whatever is happening at the threshold, it is not the model
running out of room.

## Assumptions

- **Puzzle complexity is a proxy for reasoning complexity.** The dial is
  problem size — disk count, checker count, block count. The paper treats
  this as compositional depth.
- **The programmatic checker's verdict is the model's capability.** A failed
  check is read as a reasoning failure. This is the assumption
  [LIT-463](../literature.d/LIT-463.md) attacks.
- **Models with visible thinking tokens.** Claude 3.7 Sonnet (thinking and
  not) and DeepSeek-R1/V3, chosen because the traces are accessible; o-series
  appears for final accuracy only.
- **25 samples per instance**, maximum token budget allowed.

## Key results

- **Three regimes** — at low complexity, non-thinking models match or beat
  thinking models and use fewer tokens; at medium complexity the thinking
  models pull ahead; at high complexity both go to zero. Established on
  matched backbones (Claude 3.7 with/without thinking, R1 vs V3) and under
  matched inference compute with pass@k.
- **Accuracy collapse** — every one of five reasoning models declines to
  exactly zero past a model-specific threshold.
- **Effort declines before the cliff** — thinking tokens rise with complexity
  and then fall near the collapse point, most sharply for o3-mini, least for
  Claude 3.7 Sonnet thinking. The paper is explicit that this happens "well
  below their generation length limits with ample inference budget
  available".
- **Trace structure shifts with regime** — at `N = 1–3` the correct solution
  appears early and the model keeps exploring wrong ones afterwards
  (overthinking); at `N = 4–7` wrong solutions come first and correct ones
  later; at `N ≥ 8` accuracy within the trace is near zero throughout.
- **Failure to execute a given algorithm** — supplying the algorithm does not
  rescue performance.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Three regimes by complexity, with non-thinking models better at the bottom | strong | matched backbones, matched compute, pass@k, across four puzzle families |
| C2 | Reasoning effort declines as problems approach the collapse threshold | strong | direct token measurement, five models; the "well below the limit" observation is the paper's own and is not disputed by its critic |
| C3 | Accuracy collapses to zero past a threshold | moderate | measured, but the measurement counts unsolvable River Crossing instances as failures, so the location of at least one threshold is affected |
| C4 | The collapse is a fundamental limitation of reasoning | weak | an interpretation of C3; the alternative reading — output-length decisions and scoring artefacts — is argued in [LIT-463](../literature.d/LIT-463.md) and not addressed here |
| C5 | Models cannot execute an explicitly supplied algorithm | moderate | measured, and subject to the same enumeration-versus-reasoning objection |

## Concepts

- **Large Reasoning Model** — a model that emits a thinking trace before its
  answer.
- **Compositional complexity** — operationalized as puzzle size.
- **Overthinking** — finding the right answer early and then wandering.

## Connections

Positioned against contaminated benchmark evaluation. The puzzle-simulator
apparatus is the methodological contribution. [LIT-463](../literature.d/LIT-463.md) is a
public comment on it.

## Bearing on the record

- **C1 and C2 are the parts the record should carry**, and they are useful
  independently of the dispute: at low complexity a reasoning model is worse
  and more expensive than its own non-thinking twin, which is an inference
  decision somebody makes daily.
- **C4 is what [SOTA-278](../practices.d/SOTA-278.md) exists to caution against**, and this
  paper is the worked example rather than the villain: the collapse is
  measured correctly and the step from "the scorer returned zero" to "the
  model cannot reason" is the step the practice says to check.
- **The record holds no other evaluation of reasoning models by trace**, so
  the instrument is worth having on its own.

## Limitations

- Puzzle size is not obviously reasoning complexity — Tower of Hanoi is
  exponentially long and trivial per move, which the critic makes something
  of.
- The checker verifies validity; for Blocks World the prompt asks for the
  *minimum* sequence, so a compliant model solves a harder problem than the
  one being scored.
- Four puzzle families, all planning puzzles.
- Models are closed except for the DeepSeek pair.
- **The unsolvable instances.** The evaluation includes River Crossing
  configurations that have no solution. The paper does not address this and
  it is not an interpretive matter.

## Open questions

- Why does effort decline before the threshold, if not budget? Poor
  self-calibration about remaining context is one hypothesis and the paper
  does not test it.
- Does the collapse survive an evaluation that asks for a generating
  procedure rather than an enumeration? The critic's preliminary answer is
  no; nobody has run it properly.
- How much of the threshold's *location* moves once unsolvable instances are
  removed?
