---
number: 62
status: 'Superseded'
status_note: >-
  The decoupling experiment this practice's own body invited has been run:
  holding the token budget fixed, the dependence of batch size on model size
  very nearly vanishes. What the heuristic was tracking is the data that
  scaled alongside the model. `Superseded` rather than `Rejected` because
  following it along the Chinchilla line gives roughly the right answer for
  the wrong reason — the successor is [SOTA-258](SOTA-258.md).
title: 'Scale batch size with model size but sub-linearly'
version: 3
history:
- version: 3
  date: '2026-10-01'
  note: >-
    Re-sourced. Both relations named LIT-061 (Artetxe et al.), whose §3.1
    only sets batch size and learning rate "according to the model size
    following Brown et al. (2020)" — a borrowed setting, with no finding and
    nothing about sub-linearity. The evidence is Kaplan et al. (LIT-028),
    whose compute-optimal allocation grows batch far more slowly than model
    size, with McCandlish et al. (LIT-017) for the mechanism; GPT-3's
    Table 2.1 is the setting LIT-061 borrowed. The rule's status is
    unchanged.
- version: 2
  date: '2026-09-20'
  note: >-
    Superseded by SOTA-258, and retagged. Zhang et al. (LIT-445)
    ran the decoupling experiment this practice's body invited — hold the
    token budget fixed and vary model size — and the dependence very nearly
    disappears; Bergsma et al. (LIT-443) agree from a scaling-law fit.
    The retag from `model-architecture` to `training-optimization` is correct
    on its own terms and would be right with or without the supersession:
    `batch size` is named in the training-optimization blurb and nothing in
    the model-architecture blurb covers it. It also happens to be what lets
    the correction edge be declared, and saying so is better than not
    (ADR-035).
tags:
- training-optimization
date: '2026-08-24'
# Was LIT-061 (Artetxe et al.), which borrows GPT-3's batch sizes in one
# sentence and measures nothing about batch size. Moved to the work that
# produced the evidence: Kaplan's allocation fit first, McCandlish's
# noise-scale account of why size matters only through loss second.
# GPT-3 (LIT-035), whose table is the setting, is cited in the body but
# shares no topic with this practice, so it cannot be listed here.
source:
- LIT-028
- LIT-017
# Was LIT-061. GPT-3 §2.3 attributes "larger models can typically use a
# larger batch size" to Kaplan et al. and McCandlish et al.; McCandlish
# expects size to matter only through the loss reached, so the sub-linear
# pairing of batch with model size is Kaplan's: Eq. 1.7 and Figure 3 give
# both against compute, and the ratio is the rule.
introduced_by:
- LIT-028
superseded_by:
- SOTA-258
summary: >-
  Kaplan et al. (2020), LIT-028 — [ARXIV-2001.08361](https://arxiv.org/abs/2001.08361). Along the
  compute-optimal frontier the model grows as `C^0.73` and the batch as
  `C^0.24`: over a billion-fold increase in compute, more than a
  million-fold in model size against about a hundred-fold in batch.
corrected_by:
- SOTA-258
---

# SOTA-062: Scale batch size with model size but sub-linearly

## Source

Kaplan et al. (2020), LIT-028 — [ARXIV-2001.08361](https://arxiv.org/abs/2001.08361).

McCandlish et al. (2018), LIT-017 — [ARXIV-1812.06162](https://arxiv.org/abs/1812.06162).

The sub-linearity is LIT-028's. Its compute-optimal allocation (Eq. 1.7)
grows the model as `C^0.73` and the batch as `C^0.24`, and its Figure 3
draws what that means over a billion-fold increase in compute: more than
1,000,000× in model size, about 100× in batch, under 10× in serial steps.
The same paper measured critical batch size against loss at 3M and 85M
parameters (Figure 10) and found it depends on the loss, not directly on
model size — and Figure 3's own caption says the batch increase is drawn
from the increase in data. The model-size reading is a projection along that
frontier, which is the reading SOTA-258 later took apart.

LIT-017 is the mechanism. The gradient noise scale that sets the useful
batch rises as the loss falls, and on LSTM language models of several sizes
it was roughly independent of model size at a fixed loss; larger models
reach larger noise scales only because they reach lower loss.

Origin and evidence are the same paper here: LIT-028 does not write batch as
a function of model size, but its allocation is where the pairing first
appears, and GPT-3 credits it (with McCandlish) for "larger models can
typically use a larger batch size". This practice previously credited Artetxe et al. (LIT-061), which only sets
batch size by model size "following Brown et al. (2020)". That setting is
GPT-3's Table 2.1 (LIT-035): from 125M to 175B parameters — about 1,400× —
the batch went from 0.5M to 3.2M tokens, about 6×, chosen with the gradient
noise scale measured during training and justified by citing Kaplan and
McCandlish.

## Sub-linearly, and why the exponent matters more than the direction

Larger models tolerate — and want — larger batches, because the gradient noise
scale that sets the useful batch size rises as the model reaches a lower loss.
That the growth is *sub-linear* is the content: doubling parameters does not
double the batch, so the ratio of batch to model size falls as scale rises,
and a rule that scales them together over-shoots at the top end.

The practical failure is quiet. An over-large batch does not diverge; it
spends compute on samples that buy less than they cost, and the run simply
reaches a given loss later than it should have — attributed, usually, to the
data or the schedule.

## What the record has that is better

This is a heuristic read off a 2020 allocation fit and the GPT-3 table that
followed it, and the quantity it gropes toward — critical batch size — is measurable and has since been characterised
directly. The record's own material is stronger: [SOTA-092](SOTA-092.md) and [SOTA-093](SOTA-093.md) give
the mechanism, and the ramp implied by them is what large runs actually do.

Kept because it is true and because a rule of thumb is useful when nobody is
going to measure. But a reader with a measurement should prefer it, and the
practice should not be read as licensing a fixed batch-to-parameter ratio,
which is the reading its title most invites.

The alternative the record held beside it, [SOTA-061](SOTA-061.md), does not use model size
at all: it raises the batch while sample efficiency stays above 80% of its
small-batch value and stops there. That rule asks for a measurement, where
this one is a proxy for it. The proxy has since been shown to track the wrong
variable ([SOTA-258](SOTA-258.md)). No paper compared the two rules directly.
