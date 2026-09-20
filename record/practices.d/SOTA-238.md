---
number: 238
status: 'Active'
formerly:
- SOTA-tmp4n8k9
title: 'Set domain weights with a small proxy model under group DRO on excess loss, then transfer them'
version: 3
history:
- version: 2
  date: '2026-09-18'
  note: >-
    Names what the +6.5 points is measured against. The Pile is now filed;
    its default weights are a judgement call, which is what the gain is
    relative to. Recommendation and consensus unchanged.
- version: 3
  date: '2026-09-20'
  note: >-
    Moved to `contested`, with LIT-451 named. Setting domain weights with
    a small proxy assumes the weight that is right for the proxy is right, or
    nearly right, for the target. That paper finds knowledge acquisition under
    mixing has thresholds in model size, so proxy and target can sit on
    opposite sides of one. The recommendation is unchanged; the method is not
    refuted; the exposure is now named.
tags:
- data-pipeline
consensus: contested
contested_by:
- LIT-451
consensus_note: >-
  The baseline the data-mixing literature measures itself against, and the
  method later work cites when it wants a non-heuristic comparison. Not
  `universal`: most published corpora still ship heuristic weights, and the
  record's own [SOTA-166](SOTA-166.md) is a different instrument for the same decision
  rather than an endorsement of this one.
date: '2026-09-17'
source:
- LIT-391
introduced_by:
- LIT-391
implementations:
- 'DoReMi'
summary: >-
  Xie et al. (2023), [LIT-391](../literature.d/LIT-391.md) — [ARXIV-2305.10429](https://arxiv.org/abs/2305.10429). Train a small proxy under
  group DRO to produce domain weights, then resample and train the real model
  with them. Optimise worst-case EXCESS loss against a reference model, not
  worst-case loss — the naive form upweights whichever domain is noisiest,
  because every domain has a different irreducible entropy.
---

# SOTA-238: Set domain weights with a small proxy model under group DRO on excess loss, then transfer them
<!-- inactive-ok-file: SOTA-268 — Proposed, and filed in this same contribution as the practice drawn from the contesting paper -->

<!-- inactive-ok-file: SOTA-166 — Proposed, and this practice's counterpart; naming it is how the record holds the choice -->

## Source

Xie et al. (2023), [LIT-391](../literature.d/LIT-391.md) — [ARXIV-2305.10429](https://arxiv.org/abs/2305.10429).

## The method

Three steps. Train a small **reference** model on the default mixture. Train a
small **proxy** under Group DRO over domains. Resample the corpus with the
resulting weights and train the model you actually wanted.

In the paper, a 280M proxy sets the weights for an 8B run — a 30x transfer —
for **+6.5 points** average few-shot downstream accuracy over The Pile's
default weights, and baseline accuracy in **2.6x fewer steps**.

Read the denominator. The Pile ([LIT-426](../literature.d/LIT-426.md)) ships 22 named domains and a
default sampling mixture its authors chose by judgement and never claimed
was optimal. So +6.5 points answers *can a learned mixture beat a hand-picked
one*, and the size of the gain is partly a property of the baseline: a corpus
shipped with better-tuned defaults would make this method look worse without
the method changing.

## Optimise excess loss, not loss

This is the part to get right, and the naive version fails in a way that looks
like success:

> a naive worst-case approach would upweight the domains with the most noisy
> data, as every domain has a different optimal loss (aka, the entropy)

Worst-case *loss* selects for whichever domain is hardest, and the hardest
domain is usually the one with the most irreducible noise. So optimise the
**gap against a pretrained reference model** instead. That turns "which domain
is hard" into "which domain has headroom", which is the quantity a mixture
should be chasing.

**The reference model earns its step by supplying that subtraction.** Skipping
it is not a saving; it changes what is being optimised.

The general form is worth carrying past data mixing: *a worst-case objective
over heterogeneous groups selects for irreducible difficulty unless you
subtract a per-group baseline.* Any minimax over domains, tasks, languages or
users has the same failure and the same remedy.

## What it does not require

A downstream task. Weights are produced with no evaluation target in the loop
— and on GLaM they match weights that *were* tuned on downstream tasks. Not
knowing the target cost nothing there, which is the paper's most surprising
result and the reason this is usable before anyone has decided what the model
is for.

## Contested: the proxy and the target may be in different regimes

Gu et al., [LIT-451](../literature.d/LIT-451.md), find that knowledge acquisition from a
knowledge-dense dataset mixed into web text has a **threshold in model
size**: below it the model acquires almost nothing however long it trains,
above it acquisition jumps. The threshold's location depends on the mixing
ratio, through a power law.

A small proxy model can therefore sit below a transition the target model
will sit above. The domain looks worthless to the proxy — little excess loss
to reduce, so little for the group-DRO objective to weight toward — and the
weight it assigns is a fact about the proxy's regime rather than the
target's.

**Not a refutation.** The method's evidence stands, and this is an exposure
rather than a demonstrated failure: nobody has run group DRO across a
transition and watched it choose wrongly. It is worth knowing because the
failure mode is silent — the proxy reports a confident answer either way —
and because it bites hardest on the small knowledge-dense domains where
getting the weight right matters most. [SOTA-268](SOTA-268.md) is the practice drawn
from that finding.

## Conditions

**Downweighting is not free in general.** "Improves perplexity across all
domains, even when it downweights a domain" is reported, and the authors
construct an appendix example of when reweighting has no trade-off — that it
needs constructing is the tell. Expect the no-trade-off case to be a property
of particular domain structures, not a guarantee for an arbitrary corpus.

The proxy must be large enough for its ranking to transfer, and the paper
evidences one gap (280M → 8B) on two corpora. Nothing here says where that
breaks.

## Against the other instrument in this record

[SOTA-166](SOTA-166.md) sets proportions by fitting a **mixing law** on small runs. Both
avoid training a model per candidate mixture, and they answer different
questions:

- A **mixing law** is a *predictor* over mixtures. It costs a set of runs to
  fit, and in exchange you can optimise for any target you can name, and
  compose with scaling laws to extrapolate.
- **This** is a *producer* of one weighting. It costs a reference and a proxy
  run, names no target, and gives you robustness rather than optimality.

Reach for the law when the target is known and worth optimising against;
reach for this when it is not, or when a defensible default is wanted before
the evaluation suite exists.
