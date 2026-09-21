---
status: Active
consensus: unassessed
consensus_note: >-
  One report, and no assessment of what the field does. The measurement behind
  it is unusually clean — one harness, two models, three procedures, the
  ordering flipping twice — but it is a single source and nobody has surveyed
  how often published comparisons vary the procedure. What is established is
  that the procedure can decide the winner; what is unknown is how often it
  does.
title: 'Treat the inference-time decision procedure as part of what you are comparing, and report the ordering under each one'
version: 1
tags:
- analysis-and-evaluation
- in-context-learning
date: '2026-09-21'
source:
- LIT-tmpgqsmp
introduced_by:
- LIT-tmpgqsmp
implementations: []
summary: >-
  Gemini Team (2023), [LIT-tmpgqsmp](../literature.d/LIT-tmpgqsmp.md) — on MMLU, greedy sampling puts
  GPT-4 ahead by 0.2, plain chain-of-thought at 32 samples puts it ahead by
  2.3, and uncertainty-routed CoT at 32 samples puts Gemini Ultra ahead by
  **2.7**. Same models, same benchmark, same harness. The procedure is worth
  **6.0** points to one model and **3.1** to the other, so running the same
  procedure on both is not enough — the ordering is a property of the
  procedure you chose to report.
---

<!-- inactive-ok-file: SOTA-309 — Proposed, and named only as one item in
     the tally of five measurement-sensitivity practices this document
     declines to join. Citing a practice in order to say the count does NOT
     extend to it is not citing it as settled. -->

# SOTA-tmpecji3: Treat the inference-time decision procedure as part of what you are comparing, and report the ordering under each one

## Source

Gemini Team, Google (2023), [LIT-tmpgqsmp](../literature.d/LIT-tmpgqsmp.md) — read as
[NOTE-tmp13fue](../notes.d/NOTE-tmp13fue.md). Appendix 10.2.

## When this applies

You are comparing two or more models on a benchmark, and the numbers were
produced with anything other than a single greedy forward pass — few-shot
prompting, chain-of-thought, self-consistency, best-of-`n`, a verifier, a
routing rule, a tuned stopping criterion. Which is to say: almost every
published model comparison.

## The measurement

Uncertainty-routed chain-of-thought draws `k` samples, takes the majority if
consensus clears a threshold, and otherwise falls back to the greedy answer
with no chain of thought. The threshold is **optimized for each model on that
model's own validation split**.

| procedure | Gemini Ultra | GPT-4 | ahead |
|---|---|---|---|
| greedy sample | 84.0% | 84.2% | GPT-4, by 0.2 |
| chain-of-thought @32 | 85.0% | 87.3% | GPT-4, by 2.3 |
| **uncertainty-routed CoT@32** | **90.0%** | 87.3% | **Gemini, by 2.7** |

*(MMLU. Human-expert performance is 89.8%, so only the third row crosses it.)*

## Do this

**Report the sweep, not the best row.** Every procedure you ran, on every
model you compare, in one table. The cost is a table; the alternative is a
claim that cannot be checked.

**Do not assume that applying one procedure to both models makes it fair.**
This is the finding and it is not obvious. Running the same procedure on both
is *necessary* and it is not *sufficient*, because the procedure interacts
with the model: here it is worth **6.0** points to Gemini Ultra and **3.1** to
GPT-4. Worse, the two gains have different sources — GPT-4 gets all of its
from plain chain-of-thought, with the routing rule adding nothing, while
Gemini Ultra gets almost none from plain chain-of-thought and nearly all of it
from the routing. A procedure that is a no-op for one model and a six-point
lift for another is not a measurement harness. It is a component of one of the
systems.

**Say where any tuned constant in the procedure came from.** The routing
threshold here is fitted per model on the validation split. That is a fitted
parameter sitting inside what is presented as an evaluation protocol, and it
should be reported the way a hyperparameter is reported.

**Put the matched-protocol number where the claim is.** When the baseline's
published number uses a different procedure, the comparable row is the one the
abstract should carry. In the main table Gemini Ultra is **83.7%** at 5-shot,
the protocol every other model in that table is scored on, against GPT-4's
86.4%.

## Why `Active` on one source

Because the measurement does not need replicating to be believed: it is a
single harness applied to two models under three procedures, published by the
group with the most to lose from it, and the ordering flips twice inside it.
The recommendation that follows costs a table.

What one source cannot establish is how often this bites, which is why
`consensus` is `unassessed` and why the conditions below are longer than the
instruction.

## Conditions

**This is not a claim that Gemini Ultra is worse than GPT-4.** It is a claim
that the published comparison does not settle it, in either direction, and
that the report's own appendix is what shows this. The 2.7-point margin is
also a single run with no seeds — see [SOTA-307](SOTA-307.md) for what a single-run
margin of that size is worth.

**It does not say inference-time procedures are illegitimate.** They are how
models are actually used, and a comparison at the procedure you will deploy
under is the *most* relevant one. The claim is that the procedure has to be
named as part of the system, and that a single row cannot carry a comparison
whose ordering depends on it.

**One benchmark, one pair of models, one procedure family.** Nothing here says
how large the effect is for best-of-`n`, verifier reranking, or tool use,
though the mechanism gives no reason to expect it smaller.

**The disclosure was complete.** Unlike every other measurement-sensitivity
practice in this record — [SOTA-305](SOTA-305.md), [SOTA-307](SOTA-307.md), [SOTA-308](SOTA-308.md),
[SOTA-309](SOTA-309.md), [SOTA-312](SOTA-312.md) — the source here states the protocol on every
row and publishes the full sweep. The failure is not concealment but which row
reached the abstract, which is [DP-010](../../docs/design-principles.md#dp-10) and not the shape the others
share. Five of those and this one is a count, not a principle —
[DP-009](../../docs/design-principles.md#dp-9).

## Known implementations

None recorded as a reporting standard. [LIT-tmpgqsmp](../literature.d/LIT-tmpgqsmp.md)'s own Appendix
10.2 is the worked example, which is the awkward and accurate position: the
paper that demonstrates the problem also demonstrates the remedy, one appendix
away from the abstract that needed it.
