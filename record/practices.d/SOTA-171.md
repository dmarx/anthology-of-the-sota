---
number: 171
# inactive-ok-file: SOTA-124 — Proposed, and named throughout on purpose: it
# is the position this practice disagrees with, and the disagreement is what
# both documents are for.
status: Active
formerly:
- SOTA-tmp54nas
consensus: contested
consensus_note: >-
  Three positions, and they disagree about the quantity. This says four
  epochs from 400 runs. SOTA-124 says the governing quantity is epoch *size*
  against the memorization window, not epoch count, and on that basis
  Falcon-H1-Tiny repeated sources a hundred times. LIT-175 says repetition
  overfits severely and the overfitting is a property of the objective,
  removable with augmentation. Nobody has run the experiment that tells them
  apart.
contested_by:
- LIT-119
- LIT-175
title: 'Repeat a data-constrained corpus for up to about four epochs; past that, added compute stops paying'
version: 2
history:
- version: 2
  date: '2026-09-19'
  note: >-
    The four-epoch bound was reproduced independently and relocated.
    Prabhudesai et al. (LIT-tmp5xe2h) re-ran this sweep with the objective
    swapped and recovered R* = 31.93 for autoregressive training against
    512.85 for masked diffusion — so the number holds, and it is a fact about
    the autoregressive objective rather than about repetition. The
    recommendation is unchanged; the body now says what it is a bound on.
tags:
- data-pipeline
date: '2026-09-08'
source:
- LIT-166
introduced_by:
- LIT-166
implementations: []
summary: >-
  Muennighoff et al. (2023), [LIT-166](../literature.d/LIT-166.md) — with constrained data at fixed
  compute, up to four epochs of repeated data changes the loss negligibly
  against having that much unique data. Past that point the value of adding
  compute decays toward zero. 400 training runs, up to 900B tokens and 9B
  parameters, with a scaling law that prices repeated tokens and excess
  parameters.
---

# SOTA-171: Repeat a data-constrained corpus for up to about four epochs; past that, added compute stops paying
<!-- inactive-ok-file: SOTA-tmp9rfqy — Proposed, and filed in this same contribution as the third lever this section names -->

## Source

Muennighoff et al. (2023), [LIT-166](../literature.d/LIT-166.md) — [ARXIV-2305.16264](https://arxiv.org/abs/2305.16264).

The regime is the one the field has since entered: extrapolating the
parameters-and-tokens trend runs into the amount of text that exists, so the
binding constraint stops being compute and becomes data.

**Both halves of the result are the practice.** With constrained data at
fixed compute, training on up to four epochs of repeated data changes the
loss negligibly against having that much unique data — repetition is close to
free. Past that point it is not: with more repetition, the value of adding
compute decays toward zero. The first half licenses repetition and the second
bounds it, and quoting either alone gets you a different recommendation.

A scaling law for compute optimality falls out, pricing in the decreasing
value of repeated tokens *and* of excess parameters, validated empirically
across a sweep up to 900B tokens and 9B parameters. 400 training runs, with
models and datasets released.

Two mitigations for data scarcity are tested alongside: adding code data to
the mixture, and removing commonly used filters.

## Contested, and the disagreement is about the quantity

[SOTA-124](SOTA-124.md) says the quantity governing safe repetition is not epoch *count*
but epoch *size* relative to the model's memorization window, and on that
basis Falcon-H1-Tiny repeated SFT sources a hundred times or more. This
practice says four, and it has 400 runs behind it where that one has one
figure and an argument its own authors call early.

**The two are not quite measuring the same thing, which is the interesting
part.** This sweep repeats a *whole corpus* under a fixed compute budget;
the memorization-window claim is about one high-quality *source inside a
mixture*, where a small share means a long delay between repeats. That
distinction may dissolve the conflict — or it may be the mechanism by which a
100× repetition quietly costs something nobody measured.

[LIT-175](../literature.d/LIT-175.md) is a third position and the most useful of the three, because it
makes the other two falsifiable in the same terms: it says repetition
overfits severely *and* the overfitting is a property of the objective rather
than of repetition, removable with augmentation. If that holds, a recipe
repeating a source a hundred times is either augmenting implicitly or paying
a cost nobody measured.

## Why `Active` while contested

`status:` is this record's editorial position and `consensus:` is the
field's; they are allowed to disagree, which is the whole point of the second
axis. Four epochs from 400 released runs is the best-evidenced number
anybody has published for this question, and a reader who needs a number
today should use it. That it is disputed by two positions with different
methodologies is what `contested` says.

## Reproduced independently, and relocated

Prabhudesai et al., [LIT-tmp5xe2h](../literature.d/LIT-tmp5xe2h.md), re-ran this study — same corpus, same
recipe, same parametric form — with the training objective swapped from
autoregressive to masked diffusion. The autoregressive arm recovers
`R* = 31.93`, which is this practice's four-epoch bound in its source's own
units.

That is a replication, and it changes what the number is a statement about.
The same fit for masked diffusion gives `R* = 512.85`. So the bound is a
property of the autoregressive objective rather than of repetition, and a
reader whose corpus is fixed has a second lever — change the objective —
that this practice's framing does not offer.

Kim et al., [LIT-tmp2udh1](../literature.d/LIT-tmp2udh1.md), point at a third lever from a different
direction: with weight decay tuned rather than inherited, the overfitting
that bounds multi-epoch training largely goes away ([SOTA-tmp9rfqy](SOTA-tmp9rfqy.md)). Neither
result disputes the four epochs. Both say it was measured under conditions
nobody was varying.

## Known implementations

- None reports having used the four-epoch bound as a design rule; the record's
  recipes either repeat far more (Falcon-H1-Tiny) or do not say.
