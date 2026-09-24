---
number: 32
status: Active
title: 'Put the layer normalization inside the residual block, before the sublayer'
version: 4
history:
# inactive-ok: LIT-029 — the retired duplicate, named as what this practice used to cite
- version: 1
  date: '2026-08-24'
  note: >-
    Filed by the migration as "Use pre-norm (RMSNorm) for transformer
    layers", sourced to LIT-029 — a duplicate note whose one-line summary
    attributed RMSNorm to Xiong et al. The practice inherited that
    conflation: it recommended two independent choices and cited a paper
    that supports one of them.
# inactive-ok: LIT-029 — the retired duplicate, named as what the split repointed away from
- version: 2
  date: '2026-09-08'
  note: >-
    Split. This practice is now the placement claim alone, sourced to the
    paper that argues it; the statistic is SOTA-182, sourced to
    Zhang and Sennrich. LIT-029 retired as a duplicate of LIT-114.
- version: 3
  date: '2026-09-18'
  note: >-
    Adds `model-architecture`. Where the layer normalization sits
    relative to the residual block is an architectural choice; that it
    was made for stability is why `model-stability` stays first. It
    does not bind the unbound edge to SOTA-100, which is a real
    crossing between an architectural fix and a schedule one.
- version: 4
  date: '2026-09-24'
  note: >-
    The collapse cost gains a source and a rate (THEORY-096), the
    no-warm-up consequence gains the measurement it lacked, and the
    `universal` reading gains the note it never had. The recommendation is
    unchanged. This practice had been stating the representation-collapse
    argument in its own prose with no citation.
tags:
- model-stability
- model-architecture
consensus: universal
consensus_note: >-
  Not doing it is what needs justifying, and the grounds are adoption rather
  than a survey: every large model in this record is pre-norm, `llama2` is
  listed here and the alternatives that exist — sandwich and peri-layernorm
  placements, and LIT-639's two streams — are rearrangements *of* it
  rather than returns to post-norm. What is not established, and the reason
  this note exists rather than the value standing bare, is that the choice is
  deliberate in each case. LIT-639 is the one paper here that measures
  both sides, and it finds post-norm failing outright at twelve encoder and
  twelve decoder layers even with warm-up — which is a reason the convergence
  is not merely inherited. Read as of 2026-09.
date: '2026-08-24'
source:
- LIT-114
introduced_by:
- LIT-114
implementations:
- llama2
compared_against:
- SOTA-100
summary: >-
  Xiong et al. (2020), [LIT-114](../literature.d/LIT-114.md) — [ARXIV-2002.04745](https://arxiv.org/abs/2002.04745). Pre-LN: normalize the
  input to each sublayer rather than the sum after it, so the gradients near
  the output are well behaved at initialization.
explained_by:
- THEORY-011
- THEORY-096
---
<!-- inactive-ok-file: THEORY-096 — Proposed, filed in this same contribution as the account under SOTA-032's cost. The practice declares explained_by on it, so the citation is the relation itself; the practice stands without the account and the account is the weaker of the two, which is why their statuses differ -->

# SOTA-032: Put the layer normalization inside the residual block, before the sublayer

## Source

Xiong et al. (2020), [LIT-114](../literature.d/LIT-114.md) — [ARXIV-2002.04745](https://arxiv.org/abs/2002.04745).

The original Transformer normalizes *after* the residual addition (Post-LN).
Xiong et al.'s mean-field analysis shows that this leaves the expected
gradients of parameters near the output layer large at initialization, which
is what makes early training fragile under a large learning rate. Moving the
normalization inside the residual branch, applied to the sublayer's input
(Pre-LN), removes that.

The condition worth carrying: the paper's argument is about *initialization*,
and its headline consequence is that Pre-LN models can be trained with no
warmup stage at all and reach comparable results in less time. The record
still recommends warmup in [SOTA-100](SOTA-100.md), which was written against a different
account of why warmup exists. [LIT-114](../literature.d/LIT-114.md) flags that tension; this practice does
not resolve it.

The trade Pre-LN makes is representational rather than numerical: the
residual stream is never renormalized, so later layers see a stream whose
magnitude grows with depth. That is the cost people cite when they revisit
Post-LN or hybrid placements, and it is why this is a placement recommendation
rather than a law.

Independent of the *statistic* — see [SOTA-182](SOTA-182.md). Pre-LN with centered
LayerNorm is what GPT-2 does.

## Known implementations

- llama2

## Pre-norm, and why it changed what training needs

Placing the normalisation inside the residual branch — normalise, then
sublayer, then add — leaves the residual stream itself unnormalised, so
there is a clean additive path from the embedding to the output that nothing
rescales. The original arrangement normalised *after* the addition, which
puts a normalisation on every step of that path.

The consequence is about gradients at initialisation. Post-norm gives
expected gradients at the output layer that grow with depth, which is what
makes a large learning rate diverge early and what a warmup schedule exists
to survive. Pre-norm bounds them, and [LIT-114](../literature.d/LIT-114.md)'s result is that with it the
warmup stage can be removed entirely.

That is why this is one of the few architecture practices whose consequence is
a *training* practice: [SOTA-100](SOTA-100.md)'s warmup-proportional-to-model-size is the
compensation the post-norm arrangement needed, and pre-norm is what made it
optional.

## The cost, which is real and shows up at scale

Pre-norm trades trainability for some final quality: the unnormalised
residual stream grows in magnitude with depth, and deep pre-norm models can
see later blocks contributing proportionally less — the representation
collapse argument. Sandwich and peri-layernorm variants exist because of it.

**That argument now has a source and a rate.** Xie et al.
([LIT-639](../literature.d/LIT-639.md)) derive it: the per-layer change in the normalised hidden
state decays as `O(1/√k)`, and adding a block to an `N−1` block model moves
the output by `O(1/√N)`. [THEORY-096](../theory.d/THEORY-096.md) holds the account, and the
shape worth carrying is that **the benefit and the cost are one mechanism
described twice** — the residual path being unrenormalised is what lets
gradients reach the early blocks, and what lets the stream outgrow any single
block's contribution.

Two qualifications on that rate, both in the theory document: it is derived
under an independence assumption that a trained network does not satisfy, and
`O(1/√k)` is slow — at 24 layers the per-layer change is about a fifth of its
value at the first, not a thousandth. "Collapse" names the direction and
overstates the speed.

Every large model in this record is pre-norm nonetheless, which is the honest
summary: the stability is worth more than the margin, and the alternatives
are refinements of pre-norm rather than returns to post-norm.

## What "warm-up can be removed" costs

The headline consequence above — that Pre-LN models train without a warm-up
stage — is Xiong et al.'s and is stated here without a number. [LIT-639](../literature.d/LIT-639.md)
supplies one, on IWSLT:

| method | warm-up | E6D6 | E12D12 |
| --- | --- | --: | --: |
| Post-LN | yes | 35.37 | **fail** |
| Post-LN | no | fail | fail |
| Pre-LN | yes | 35.12 | 35.18 |
| Pre-LN | **no** | **32.28** | **31.82** |

**Removing warm-up costs 2.84 BLEU at E6D6 and 3.36 at E12D12.** Pre-LN
trains without it, which is what Xiong et al. claimed and what that paper
tested; it does not train *as well*, which nobody had measured here.

That matters for the tension this practice flags with [SOTA-100](SOTA-100.md) and
does not resolve. The tension is not "pre-norm made warm-up unnecessary and
the record still recommends it" — on this evidence warm-up is still paying
for itself under pre-norm, and the thing pre-norm removed is the *requirement*
rather than the benefit. One dataset and one architecture family, so it
narrows the claim rather than settling the question.

Worth noting where the number came from: Xie et al.'s own prose says Pre-LN
"can train effectively without" warm-up, in the paragraph beneath a table
showing a three-point drop. **The table is the finding and the sentence
repeats the received view.**
