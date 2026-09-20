---
status: Proposed
promote_when: >-
  A second group measuring knowledge acquisition against both model size and
  mixing ratio and reporting a threshold, on a natural knowledge-dense corpus
  rather than a synthetic one; or a pretraining report that says it raised a
  domain's share because the smaller run showed nothing. What would not move
  it: a mixing-law paper reporting that its fitted proportions transferred
  well, which is consistent with being on the same side of a transition at
  both scales.
consensus: unreplicated
consensus_note: >-
  One group, synthetic biographies mixed into web text, Pythia models to
  6.9B. The transitions are unambiguous in that setting and nobody has looked
  for them in another.
title: 'Do not transfer a data mixing ratio across model scales; the threshold where a domain starts being learned moves with size'
version: 1
tags:
- data-pipeline
date: '2026-09-20'
source:
- LIT-tmphrxdn
introduced_by:
- LIT-tmphrxdn
implementations: []
summary: >-
  Gu et al. (2025), [LIT-tmphrxdn](../literature.d/LIT-tmphrxdn.md) — knowledge acquisition from a
  knowledge-dense dataset mixed into web text has thresholds, not a smooth
  curve. Below a critical model size, or a critical mixing ratio, the model
  memorises almost nothing however long it trains; past it, accuracy jumps
  to over 60%. The critical ratio follows a power law in model size, so a
  ratio chosen at one scale can be on the wrong side of a transition at
  another.
explained_by:
- THEORY-tmpijbl9
---

# SOTA-tmphckqj: Do not transfer a data mixing ratio across model scales; the threshold where a domain starts being learned moves with size
<!-- inactive-ok-file: SOTA-166 — Proposed, and one of the two practices this contests; the contest is declared on those practices -->
<!-- inactive-ok-file: THEORY-tmpijbl9 — Proposed, and filed in this same contribution as this practice's explanation -->

## Source

Gu et al. (2025), [LIT-tmphrxdn](../literature.d/LIT-tmphrxdn.md) — [ARXIV-2505.18091](https://arxiv.org/abs/2505.18091).

## What breaks

Knowledge acquired from a knowledge-dense dataset scales linearly with model
size — when that dataset is trained on **alone**. That law is well
established, from synthetic biographies and independently from Wikidata
triples ([LIT-tmpvt6e3](../literature.d/LIT-tmpvt6e3.md)).

Mix the same dataset into web text at a realistic share and the law is gone.
Two thresholds appear:

- **In model size.** At a fixed mixing ratio, accuracy sits at zero as the
  model grows, then past a threshold jumps to over 60%.
- **In mixing ratio.** At a fixed model size, accuracy sits at zero as the
  ratio rises, then past a threshold climbs rapidly.

**Below the ratio threshold, training longer does not help.** That control is
what makes this a different phenomenon from slow learning, and it is the one
a practitioner is most likely to misdiagnose.

## Why the ratio has to be re-chosen

The critical mixing ratio follows a **power law in model size**. So the
proportion that works at your proxy scale is not a noisy estimate of the
proportion that works at target scale; it can be an estimate of a different
regime's answer. The paper states the consequence directly: a good mixing
recipe for large models may not be optimal for small models, and vice versa.

The practical form of the advice is asymmetric and worth stating both ways.
A domain that shows nothing at small scale may be fine at target scale — so
do not drop it. A domain that works at small scale may be over-weighted at
target scale — so do not assume the share carries.

## What this contests

[SOTA-166](SOTA-166.md) fits a mixing law on small runs and extrapolates. [SOTA-238](SOTA-238.md) sets
domain weights with a small proxy model under group DRO. Both assume the
quantity being fitted moves continuously with scale.

Neither is refuted. Both were measured, both work where they were measured,
and a mixture whose domains all sit on the same side of their transitions at
both scales will transfer fine — which may well be the common case for the
large web domains those methods were validated on. What this adds is a named
failure mode that neither has checked for, and it bites hardest exactly where
those methods are most useful: small, high-value, knowledge-dense domains at
low share.

[SOTA-103](SOTA-103.md) is differently exposed. It adjusts proportions online from
per-domain loss *during the run being trained*, so it is not extrapolating
across scale at all. Whether an online rule can cross a discontinuity is a
separate question and an open one: below the critical ratio there is not much
loss signal to follow.

## The mechanism, and why it matters beyond this

[THEORY-tmpijbl9](../theory.d/THEORY-tmpijbl9.md) is the account: a model of bounded capacity allocating it
across datasets is solving a discrete problem, and a discrete optimum moves
discontinuously when its inputs move continuously. If that is right, the
discontinuity should show up for things other than factual memorisation,
which nobody has tested.

## Conditions, and why this is `Proposed`

**Synthetic biographies.** The countability that makes the measurement
possible is exactly what a real knowledge-dense corpus lacks. Nothing
establishes that Wikipedia behaves this way, and it is the obvious next
experiment.

One knowledge-dense domain against one web corpus, Pythia models to 6.9B. The
interesting case — many domains competing for one budget — is the one the
knapsack framing is actually about and is not run.

The power law for the critical ratio is fitted over that range, and its
constants are not transferable. What is reusable is the shape of the problem,
not the numbers.

The metric is memorised biographies. A model below threshold might still be
usefully better on the domain in ways this does not measure.

## Known implementations

- None. No pretraining report in the record says it chose a domain's share
  with a threshold in mind.
