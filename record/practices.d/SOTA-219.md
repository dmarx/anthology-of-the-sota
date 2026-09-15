---
number: 219
status: Active
formerly:
- SOTA-tmpth2yj
consensus: emerging
consensus_note: >-
  The original and an independent open reproduction, which is the shape of
  evidence this record asks for. It is one design decision inside one scheme,
  and its generality beyond outer-optimizer training is untested.
title: 'Leave the inner optimizer state unsynchronised in local-update training'
version: 1
tags:
- distributed-optimization
date: '2026-09-15'
source:
- LIT-212
# The independent reproduction, which trains across continents at 90-95%
# compute utilisation and reports the same structure working.
- LIT-252
introduced_by:
- LIT-212
extends:
- SOTA-155
implementations: []
summary: >-
  When workers train independently for hundreds of steps and synchronise by
  exchanging deltas, the Adam moments each worker accumulated are local state
  and should stay local. Synchronising them triples the communication for
  negligible quality gain — which means most of what the scheme saves is not
  saved by communicating rarely, but by communicating less each time.
---

# SOTA-219: Leave the inner optimizer state unsynchronised in local-update training

## What to do

In a local-update scheme — many inner steps per worker, then an outer step
over the accumulated deltas — synchronise the model delta and nothing else.
Each worker keeps its own Adam first and second moments across the
synchronisation boundary and does not reset or exchange them.

## Why

**It is two thirds of the communication.** A model delta is one tensor the
size of the parameters. Adam's moments are two more of the same size, so
synchronising them is a 3x increase in what crosses the slow link — and
[LIT-212](../literature.d/LIT-212.md) reports the quality gain from doing so as negligible.

**It says something about where the saving comes from.** The obvious reading
of local-update training is that it saves by communicating *rarely*. This says
a large part of it is communicating *less*: an outer optimizer that has to be
given consistent inner state is a much more expensive scheme at the same
interval. That distinction is invisible from the practice this one extends,
which states the structure without saying what crosses the boundary.

**It reproduces outside the lab that published it.** [LIT-252](../literature.d/LIT-252.md) is an
independent open implementation trained across continents at 90–95% compute
utilization, and it keeps the same structure.

## What this does not settle

**Why the moments can diverge freely is not explained.** Each worker's
optimizer state drifts toward its own shard's statistics for hundreds of steps
and nothing pulls them back. That this costs nothing measurable is a finding,
not an account, and the record has no theory for it.

**It is a finding about one scheme's design, not a general rule.** SlowMo
([LIT-373](../literature.d/LIT-373.md)) wraps a base optimizer in outer momentum four years earlier and
does not frame this as a decision; whether the result transfers to the other
outer-optimizer schemes in this record is untested.

**Long horizons.** The reproductions are pretraining runs of a size these
papers could afford. Whether unsynchronised moments stay harmless over a much
longer run, where the shards' statistics have more time to separate, is open.
