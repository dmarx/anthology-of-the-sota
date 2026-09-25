---
number: 404
status: Proposed
formerly:
- SOTA-tmpvgm7o
consensus: unassessed
consensus_note: >-
  Nobody has assessed where the field stands on ablation design as such. What
  the record can say is that two papers in two different literatures have now
  reversed a published conclusion by separating a knob that moved two things,
  and that neither framed the lesson as a general one. Read as of 2026-09.
promote_when: >-
  A published ablation is re-run under this rule and the original conclusion
  *survives* — the case the record is missing, because two reversals establish
  that the confound can matter and say nothing about how often it does. A
  third reversal would not settle it; a third paper naming the rule and
  applying it prospectively would.
title: 'When you ablate an auxiliary loss, ablate the input construction that came with it, or the result is about both'
version: 1
tags:
- analysis-and-evaluation
- training-optimization
date: '2026-09-25'
source:
- LIT-671
- LIT-667
# Same code as `source:`'s first entry. Liu et al. both found the confound and
# stated the corrective, though only for their own case; nobody has written it
# as a rule, which is what this document is doing (ADR-030).
introduced_by:
- LIT-671
implementations: []
summary: >-
  Liu et al. (2019), [LIT-671](../literature.d/LIT-671.md). BERT reported that removing next sentence
  prediction hurts; RoBERTa observed that the ablation had probably "only
  removed the loss term while still retaining the segment-pair input format",
  separated the two, and found **removing the loss matches or slightly
  improves** while the *input format* was what mattered. [LIT-667](../literature.d/LIT-667.md) is the same
  defect in another literature: four grokking papers varied the training
  fraction of a fixed universe, so dataset size and dataset composition moved
  together, and the conclusion reversed when somebody turned them one at a
  time.
---

# SOTA-404: When you ablate an auxiliary loss, ablate the input construction that came with it, or the result is about both

## What to do

An auxiliary objective almost never arrives alone. It brings a way of building
inputs that exists to make it well-posed — a pair of segments for a
pair-classification loss, a corrupted span for a denoising loss, two views for
a contrastive one. Deleting the loss term and leaving that construction in
place is a single edit to the code and a **double** edit to the experiment,
because the input pipeline is still paying for a task nobody is training on.

So when you report "objective X is unnecessary", say which of these you ran:

- **loss removed, inputs unchanged** — what most ablations do, and what
  licenses no conclusion about the loss alone;
- **loss removed, inputs rebuilt for the remaining objective** — what the
  claim usually means;
- **both, separately** — the only version that attributes the effect.

The same rule reads backwards. If an ablation changes the input construction,
it has to say what happened to the losses that construction was serving.

## Where this comes from

**The naming case.** BERT — [LIT-670](../literature.d/LIT-670.md) — reported that dropping next sentence
prediction "hurts performance significantly on QNLI, MNLI, and SQuAD 1.1",
describing its `No NSP` condition only as a model "trained using the masked LM
but without the next sentence prediction task". RoBERTa, a year later:

> It is possible that the original BERT implementation may only have removed
> the loss term while still retaining the segment-pair input format.

Split into four conditions, the attribution inverts. Keeping the loss and
shortening the inputs to single sentences **hurts** — long-range dependencies
go. Dropping the loss and packing contiguous text to the full length **matches
or slightly improves**. The loss was not carrying the result; the input
construction was, and the original ablation could not have told them apart
because it only ever moved one knob that held both.

**The independent case, in another literature.** [LIT-667](../literature.d/LIT-667.md) reports the same
defect on grokking. Four papers establish that the transition is controlled by
dataset size; every one of them varies the *training fraction of a fixed
universe of examples*, which moves how much data there is and what proportion
of the possible examples it covers, together. Given two knobs and turned one at
a time, the size does nothing and the composition does everything.

Different fields, different objects, one shape: **a single experimental knob
that two design decisions are wired to.** Neither paper drew the general
lesson, which is why this document exists rather than pointing at one of them.

## What this does not claim

**Not that such ablations are usually wrong.** Two reversals establish that the
confound can matter. They say nothing about how often it does, and the
`promote_when` asks for the missing case — a re-run where the original
conclusion survives — precisely because a record that only collects reversals
will overstate the rate.

**Not a claim about effect sizes.** BERT's `No NSP` row falls 3.5 on QNLI and
0.5 on MNLI and 0.6 on SQuAD, which the paper reads as three significant drops.
Whether the original conclusion would have looked fragile under a seed sweep is
a separate question this does not answer, and a practice about attribution is
not a substitute for reporting variance.

**Not specific to auxiliary losses**, though that is where it was named. The
general form is that a component and its scaffolding are one knob unless you
build them as two — but the record has instances for losses and for dataset
construction only, so the title stays where the evidence is.

## Known implementations

- None to name. This is a rule about how to run an experiment, and the two
  sources applied it to their own cases without stating it.
