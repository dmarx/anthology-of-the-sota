---
status: Active
consensus: emerging
consensus_note: >-
  Two independent groups, disagreeing about the object level and demonstrating
  the same thing about the instrument, in opposite directions. Neither states
  it as its own conclusion, which is why `emerging` is a reading of the
  evidence rather than of the field: the record cannot show that anyone has
  adopted this as a reporting standard, and the papers that plot information
  planes mostly still do not say what binning they used. What is established
  is the finding, not the practice's currency.
title: 'State the noise or binning assumption behind any mutual information you report for a deterministic network, and show the conclusion survives changing it'
version: 1
tags:
- analysis-and-evaluation
- representation-and-encoding
date: '2026-09-21'
source:
- LIT-tmpsld21
- LIT-tmpcnvbw
introduced_by:
- LIT-tmpsld21
implementations: []
summary: >-
  Saxe et al. (2018), [LIT-tmpsld21](../literature.d/LIT-tmpsld21.md) — in a deterministic network
  `I(h;X)` is **infinite**, so every finite number on an information plane is
  a property of a noise model the analyst imposed and the network never had.
  The same `tanh` run, binned evenly in net input instead of evenly in
  activity, loses its compression phase entirely; and
  [LIT-tmpcnvbw](../literature.d/LIT-tmpcnvbw.md) makes compression *appear* in ReLU networks by
  changing the binning the other way.
explained_by:
- THEORY-tmppkfku
---

<!-- inactive-ok-file: THEORY-tmppkfku — Proposed, filed in this same
     contribution and carrying the object-level question this practice
     deliberately does not settle. The practice declares `explained_by:` on
     it, so the citation is the relation itself, and the sentence citing it
     says in as many words that it is unsettled. -->

# SOTA-tmpgvchd: State the noise or binning assumption behind any mutual information you report for a deterministic network, and show the conclusion survives changing it

## Source

Saxe, Bansal, Dapello, Advani, Kolchinsky, Tracey and Cox (2018),
[LIT-tmpsld21](../literature.d/LIT-tmpsld21.md) — read as [NOTE-tmp11zjy](../notes.d/NOTE-tmp11zjy.md).

Chelombiev, Houghton and O'Donnell (2019), [LIT-tmpcnvbw](../literature.d/LIT-tmpcnvbw.md) — read as
[NOTE-tmplxznx](../notes.d/NOTE-tmplxznx.md) — which argues against the first and demonstrates the
same point in the opposite direction.

## When this applies

You are reporting mutual information between a network's internal activity and
anything else — an information plane, a compression measurement, a
disentanglement or bottleneck metric, a layer-wise information profile — and
the network's forward pass is deterministic, which is to say almost always.

## Why there is something to state

For a deterministic map `h = f(X)`, the conditional differential entropy
`H(h|X) = -∞`, so

    I(h; X) = H(h) - H(h|X)

is **infinite**. Every finite number anyone has ever plotted on an information
plane is therefore not a measurement of the network. It is a measurement of
the network *plus a noise model the analyst added for the purpose of
measuring*, and which is absent when the network is trained and absent when it
is run.

That would be a technicality if the number were insensitive to the choice. It
is not.

## Do this

**Say which assumption you made, in the paper.** Binning with how many bins,
placed how; or additive noise of what variance; or a kernel density estimator
with what bandwidth. This is one sentence and it is currently missing from
most of the literature it applies to.

**Re-run under a materially different assumption and report both.** Not a
sensitivity sweep over bin *count* — a different *placement*. The two sources
here are the demonstration:

| | changed | result |
|---|---|---|
| [LIT-tmpsld21](../literature.d/LIT-tmpsld21.md) | `tanh` run, bins even in *net input* rather than in *activity* | the compression phase **disappears** |
| [LIT-tmpsld21](../literature.d/LIT-tmpsld21.md) | binning at full machine precision | information pinned at `log₂(P)`, nothing moves |
| [LIT-tmpcnvbw](../literature.d/LIT-tmpcnvbw.md) | ReLU run, adaptive per-layer bins rather than one global range | compression **appears** |

Two groups, arguing against each other, each showing that the conclusion is
the analyst's choice. That is stronger evidence than either intended.

**Prefer a network that actually has the noise.** If the architecture is
stochastic — a variational bottleneck, an explicitly noisy channel — the
mutual information is a property of the model and none of this applies.
[LIT-tmpsld21](../literature.d/LIT-tmpsld21.md) points at exactly this as where the information bottleneck
idea may still pay.

**Do not compare architectures in "the common currency of mutual
information" without checking invertibility.** For a linear network, scaling
one layer by `c` and the next by `1/c` computes an identical function and
generalizes identically, but gives
`I(T;X) = log(w₁²/c² + σ²) − log(σ²)`, which depends on `c`. Mutual
information is invariant to invertible reparameterization; mutual information
*after adding noise for analysis* is not.

**Do not invoke the data processing inequality over these estimates.** The
noise is added per layer for analysis and does not propagate forward, so the
Markov chain the DPI needs is not the one being measured.

## Why `Active` on a dispute

Because the two sources disagree about almost everything else and agree,
without either saying so, about this. The object-level question — whether
`tanh`'s compression is *specifically* a saturation artifact — is open, and
[THEORY-tmppkfku](../theory.d/THEORY-tmppkfku.md) carries it as `Proposed` for that reason. The
instrument-level question is not open: the infinity is analytic, and the
sensitivity is demonstrated twice in opposite directions.

## Conditions

**This is not [SOTA-200](SOTA-200.md), and the difference matters.** That practice says
check whether an emergent capability is a metric artefact — and there the
underlying quantity is real, with a discontinuous scoring rule making a smooth
thing look sharp. Here the underlying quantity is *infinite*, and the reported
number was manufactured in full by a choice. Two arrivals at "the finding was
in the measurement" with different mechanisms is a count, not a
generalization — [DP-009](../../docs/design-principles.md#dp-9).

**It says nothing about whether compression happens.** A reader wanting to
know whether representations discard input information will not find the
answer here or in either source. What the practice claims is that the
published numbers cannot settle it.

**The cost is a rerun, and for a large model that is not free.** The estimators
involved — kernel density over all sample pairs, `k`-nearest-neighbour — scale
badly, and the honest version of this practice on a large network may be
expensive enough to decline. Say so if you decline it.

**Neither source states this as its conclusion.** Both are arguing about
compression. This practice is the record's reading of what their disagreement
jointly establishes, which is why it is worth saying that reading is visible
only from holding both.

## Known implementations

None recorded. [LIT-tmpsld21](../literature.d/LIT-tmpsld21.md) does it to itself — three estimators, two
binning schemes, a machine-precision control — and is the nearest thing to a
worked example.
