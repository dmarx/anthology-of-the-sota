---
status: Active
consensus: emerging
consensus_note: >-
  The demand gap is measured across five model families and the mechanism is
  borrowed from a field that has used it for decades, so the caution is well
  founded. Not `converged`: the field's default is still to report a
  benchmark number as a capability, and nobody has put a figure on what share
  of any reported limit is demand rather than absence.
title: 'Before reporting that a model cannot do something, rule out the evaluation'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-21'
source:
- LIT-tmpmftfr
- LIT-tmp85dyu
introduced_by:
- LIT-tmpmftfr
implementations: []
summary: >-
  Hu and Frank (2024), [LIT-tmpmftfr](../literature.d/LIT-tmpmftfr.md) — the same capacity asked two
  ways scores differently, and the gap widens as the model weakens. Lawsen
  (2025), [LIT-tmp85dyu](../literature.d/LIT-tmp85dyu.md), is the worked example: an output cap, a
  scorer that cannot express refusal, and instances with no solution.
explained_by:
- THEORY-tmptybdn
---

# SOTA-tmpwqjj5: Before reporting that a model cannot do something, rule out the evaluation

## Source

Hu and Frank (2024), [LIT-tmpmftfr](../literature.d/LIT-tmpmftfr.md) — [ARXIV-2404.02418](https://arxiv.org/abs/2404.02418),
read as [NOTE-tmpzsxfv](../notes.d/NOTE-tmpzsxfv.md) — for the systematic evidence. Lawsen (2025),
[LIT-tmp85dyu](../literature.d/LIT-tmp85dyu.md), for the worked example. Accounted for by
[THEORY-tmptybdn](../theory.d/THEORY-tmptybdn.md).

## What to check

Four checks, in rough order of how often they bite.

**Are any of the instances impossible?** Verify solvability before scoring.
The River Crossing benchmark in [LIT-tmpzsiks](../literature.d/LIT-tmpzsiks.md) includes
configurations with no solution — the Missionaries–Cannibals family has none
for more than five pairs with a boat of three — and models were scored zero
for not solving them. This is the cheapest check and the one that produced an
unambiguous error in a widely-read paper.

**Can the answer fit?** An evaluation requiring an exponentially long
enumeration measures output willingness past some size. Separately, and more
awkwardly, a model may stop *before* its real limit because it misjudges its
own remaining budget — both papers in that dispute agree the collapse happens
below the token cap and disagree only about what that means.

**Can the scorer express anything but wrong?** A programmatic checker that
collapses "declined", "impossible" and "incorrect" into one bucket will
report reasoning failures it has not observed.

**Is the prompt asking for more than the scorer checks?** In the same
benchmark the Blocks World prompt demands the *minimum* sequence while the
checker accepts any valid one — so a compliant model attempts an NP-hard
optimization while being graded on an easy validity test.

Then, if you can: **ask the same thing a lower-demand way.** Read the
probability instead of asking for a judgement; offer a forced choice instead
of free production; ask for a generating procedure instead of an enumeration.
The gap between the two is a measurement, and it is larger for smaller and
less-trained models — significantly so across five model families.

## Why `Active`

Because the check is cheap, the mechanism is measured rather than argued, and
the failure it prevents is expensive: a published claim that a class of model
cannot do something, when what was observed is that an evaluation did not let
it. [LIT-tmpmftfr](../literature.d/LIT-tmpmftfr.md) is a peer-reviewed study across 13 models and five
families with a stated statistical test, and it is the source of record here.
The dispute that supplies the vivid example is *not* settled and the practice
does not need it to be.

## Conditions

- **This is a check, not a conclusion.** Nothing here says measured limits
  are usually artefacts, and no one has put a number on the share. A limit
  that survives these checks is more credible, not proved.
- **The systematic evidence is base models, open weights, 1B–70B.**
  Instruction tuning targets task-demand competence directly, so the gap may
  be much smaller on tuned and frontier models — which is where the loudest
  capability claims are made, and where nobody has measured it.
- **A low-demand readout does not always exist.** Probability readout works
  for word prediction. There is no equivalent for multi-step planning, so in
  the cases people argue about hardest, the strongest form of this check is
  unavailable and the four structural checks above are what is left.
- **The worked example is a preprint with known weaknesses**, and they are
  recorded in [NOTE-tmp8e2j0](../notes.d/NOTE-tmp8e2j0.md): single author, underpowered central
  experiment, already publicly corrected once. Its unsolvable-instance claim
  is a mathematical fact and does not depend on any of that; the rest of it
  is argument.
- **Do not read this as a verdict on [LIT-tmpzsiks](../literature.d/LIT-tmpzsiks.md).** That paper is
  NeurIPS 2025, revised after the comment, and its three-regime result is
  untouched. It is the example because it is well documented, not because the
  record has decided it is wrong.

## Relation to the neighbours

[SOTA-200](../practices.d/SOTA-200.md) says to check whether an emergent capability is a metric
artefact. This is the same caution with the sign reversed: whether an absent
capability is a demand artefact. One guards against believing a model can do
something; this guards against believing it cannot. They come from unrelated
literatures — emergence-and-metrics on one side, developmental psychology on
the other — and the record now holds both ends of the instrument problem.
