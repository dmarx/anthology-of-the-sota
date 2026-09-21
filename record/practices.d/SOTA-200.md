---
number: 200
status: Active
formerly:
- SOTA-tmpwccgh
consensus: emerging
consensus_note: >-
  That some emergence is a metric artefact is well evidenced and widely cited,
  and `LIT-tmpgnhq2` made the case directly enough to be hard to ignore. What
  share of it is remains open. The >92% figure counts which *metrics* the
  published claims sit under, not how many of those claims survive rescoring
  — most cannot be rescored, because the outputs were never released. So this
  practice still recommends the check rather than the conclusion, and stays
  `emerging` rather than `converged` on the grounds that nobody has measured
  where the field now stands.
title: 'Check whether an emergent capability is a metric artefact before believing it'
version: 2
history:
- version: 2
  date: '2026-09-21'
  note: >-
    Adds LIT-tmpgnhq2, which is the paper that made this argument, and
    LIT-tmpc4fk2, which is the claim it argues against — the practice
    previously recommended a check while the record held neither. Adds the
    discontinuous-metric check as a third question: the first two questions
    both missed Multiple Choice Grade, which is a step function rather than
    an all-or-nothing-over-steps metric, and which carries most of the
    published claims. Reverses this document's advice that the positive check
    is expensive: rescoring fixed outputs under a linear metric or a proper
    scoring rule is cheap, and only `LIT-085`'s progress measures needed the
    network reverse-engineered first. The recommendation itself — check,
    do not conclude — is unchanged.
tags:
- analysis-and-evaluation
date: '2026-09-10'
source:
- LIT-077
- LIT-085
- LIT-tmpgnhq2
introduced_by:
- LIT-077
implementations: []
explained_by:
- THEORY-039
- THEORY-tmpacv6c
---

# SOTA-200: Check whether an emergent capability is a metric artefact before believing it

## Source

Srivastava et al. (2022), [LIT-077](../literature.d/LIT-077.md) — BIG-bench, 204 tasks across three
model families from millions to hundreds of billions of parameters, with expert
human raters.

Nanda et al. (2023), [LIT-085](../literature.d/LIT-085.md) — the grokking analysis, which reverse-engineers
one network and recovers the continuous progress underneath its discontinuity.

Schaeffer et al. (2023), [LIT-tmpgnhq2](../literature.d/LIT-tmpgnhq2.md) — read as [NOTE-tmpnb7kf](../notes.d/NOTE-tmpnb7kf.md) — the
direct argument, which rescores fixed model outputs, counts which metrics the
published claims sit under, and then manufactures emergence on demand in
vision models that had never shown it.

The claim being checked is [LIT-tmpc4fk2](../literature.d/LIT-tmpc4fk2.md), which is worth reading first:
it raises the metric explanation itself and declines it for two stated
reasons, one of which is still standing.

## The claim

A capability that appears suddenly at some scale may be appearing suddenly in
your **measurement** rather than in the model. Before treating a jump as a
finding about learning, ask three things.

**Is the metric all-or-nothing over multiple steps?** BIG-bench's
categorisation is direct: tasks that improve gradually "commonly involve a large
knowledge or memorization component, whereas tasks that exhibit *breakthrough*
behavior at a critical scale often involve multiple steps or components, **or
brittle metrics**." A task scored only when every step is right improves
invisibly until the last step lands, and then appears to jump. Nothing about the
model was discontinuous.

**Is the metric discontinuous?** This is a separate question and it is the one
that catches most cases. Multiple Choice Grade scores 1 when the correct
option holds the highest probability mass and 0 otherwise — a step function
over a continuous quantity, with no long target and no compounding involved.
Of Wei et al.'s hand-annotated BIG-Bench emergent abilities, **>92% sit under
Multiple Choice Grade or Exact String Match**: one discontinuous, one
nonlinear. Asking only the first question would have cleared the
classification tasks, which is exactly the mistake [LIT-tmpc4fk2](../literature.d/LIT-tmpc4fk2.md) §5.1
made when it argued the metric explanation could not cover them.

**Is the discontinuity a property of the regime?** Grokking — delayed
generalization long after memorization — is the most-cited mysterious training
phenomenon of its period, and `LIT-085` finds it **disappears above roughly 60%
data**. At sufficiently large data fractions generalization is immediate.
Smaller fractions grok more slowly. The phenomenon is real and it is a
data-starved-regime phenomenon, not a fundamental one.

## What a positive check looks like

**Usually it is cheap, and this document used to say otherwise.** The test is
to change the scoring function and hold the model's outputs fixed. Rescoring
InstructGPT/GPT-3's arithmetic outputs with Token Edit Distance turns the
emergent curve smooth without regenerating anything; rescoring LaMDA under
Brier Score — a proper scoring rule BIG-bench already computes — removes its
emergence on the tasks where Multiple Choice Grade showed it. If you own the
outputs, this is an afternoon.

A second cheap test comes free with it: **add test data**. Composing a
per-token probability down to a small number leaves small models with a score
that is nonzero and below your resolution, and a zero you cannot resolve looks
like inability. More test data alone put every InstructGPT/GPT-3 model above
chance.

**The expensive case is real but narrower than it looked.** `LIT-085`'s
progress measures — restricted loss and excluded loss — are computed by
projecting onto or removing the five key frequencies the network was
**reverse-engineered** to be using, and they are meaningless without that
reverse-engineering. That is the cost of recovering a continuous measure when
no continuous metric over the *outputs* exists. It is not the cost of the
check in general.

## Conditions

`LIT-077` is a categorisation across 204 heterogeneous tasks, not a controlled
experiment, and it puts no number on what share of observed emergence is
artefactual. `LIT-085` is one modular-addition task on a one-layer transformer
with weight decay `λ = 1` — the authors call the generalisation to emergence "a
proof of concept" and it is nonetheless how the paper is usually cited.

`LIT-tmpgnhq2` is the strongest of the three and still does not license the
conclusion. It says so itself: *"nothing in this paper should be interpreted as
claiming that large language models cannot display emergent abilities"*. Its
demonstration that a metric **can** manufacture a sharp curve establishes
sufficiency, not necessity, and its meta-analysis counts metrics rather than
adjudicating claims. Caballero et al. and Michaud et al. both hold that some
emergence is real, and neither is refuted.

One objection survives all three sources. [LIT-tmpc4fk2](../literature.d/LIT-tmpc4fk2.md) §5.1 noted that
the *quality of intermediate reasoning steps* jumps too, which is not a
property of how a final answer is scored. Nobody has answered it, and this
record has independent reasons ([SOTA-278](SOTA-278.md)) to distrust reading traces as
evidence of anything — so the objection is open on both sides at once.

None of these sources licenses "emergence is not real". They license
**asking**, and they name three specific things to ask about.

## Known implementations

- BIG-bench's *linearity vs breakthroughness* axis is the categorisation itself
- BIG-bench ships Brier Score alongside Multiple Choice Grade on the same
  tasks, so the continuous counterpart is already computed for anything
  scored there
