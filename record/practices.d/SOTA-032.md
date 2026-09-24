---
number: 32
status: Active
title: 'Put the layer normalization inside the residual block, before the sublayer'
version: 5
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
- version: 5
  date: '2026-09-24'
  note: >-
    Three changes, recommendation unchanged. `introduced_by` was LIT-114
    (Xiong et al., Feb 2020); LIT-tmprikl1 (Oct 2019) predates it and
    disowns the origin itself, crediting Chen et al. 2018, Wang et al. 2019
    and three toolkits. So the field goes EMPTY under ADR-053 rather than
    repointing — pre-norm was in the toolkits before anyone argued for it.
    LIT-tmprikl1 joins `source:` as the first systematic evaluation. The body
    gains the high-resource counter-result it never had — post-norm beats
    pre-norm 27.58 to 26.83 on WMT'14 English-German — and the qualification
    that smaller initialization recovers most of post-norm's stability. The
    `universal` note is amended to say what the convergence does and does not
    rest on.
tags:
- model-stability
- model-architecture
consensus: universal
consensus_note: >-
  Not doing it is what needs justifying **at the scales this record is about**,
  and the grounds are adoption rather than a survey: every large model in this record is pre-norm, `llama2` is
  listed here and the alternatives that exist — sandwich and peri-layernorm
  placements, and LIT-639's two streams — are rearrangements *of* it
  rather than returns to post-norm. What is not established, and the reason
  this note exists rather than the value standing bare, is that the choice is
  deliberate in each case. LIT-639 is the one paper here that measures
  both sides, and it finds post-norm failing outright at twelve encoder and
  twelve decoder layers even with warm-up — which is a reason the convergence
  is not merely inherited. The bound on the reading: LIT-tmprikl1 measured both
  placements on high-resource WMT'14 English-German in the base regime and
  **post-norm won**, 27.58 to 26.83, so `universal` is a statement about the
  regime the record files for and not about transformers in general. Read as of
  2026-09.
date: '2026-08-24'
source:
- LIT-114
- LIT-tmprikl1
# Searched and not found: no document this record can name FIRST MADE this
# recommendation. LIT-tmprikl1 (Oct 2019) is the earliest systematic evaluation
# and explicitly attributes pre-norm to others — Chen et al. 2018
# (1804.09849), who found it instrumental inside a larger system, and Wang et
# al. 2019 (1906.01787), who first compared the placements at depth — while
# noting it was "already implemented in popular toolkits (Vaswani et al. 2018;
# Ott et al. 2019; Hieber et al. 2018), though not necessarily used by their
# default recipes." The origin is code, not a paper. Naming a paper that argued
# for it before Oct 2019 is how a reader refutes this (ADR-053 §2).
introduced_by: []
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

Xiong et al. (2020), [LIT-114](../literature.d/LIT-114.md) — [ARXIV-2002.04745](https://arxiv.org/abs/2002.04745), the mean-field
analysis. Nguyen and Salazar (2019), `LIT-tmprikl1`, the first systematic
evaluation, four months earlier.

<!-- inactive-ok-block: ADR-029 — Superseded by ADR-030, cited beside it
     because the pair is what defines the field this paragraph is about:
     ADR-029 drew the origin/evidence distinction, ADR-030 refined it, and
     ADR-053 (Active) is the one being exercised here. -->
**This practice has no `introduced_by`, and the emptiness is a claim.**
Pre-norm was in OpenNMT, tensor2tensor and Sockeye, and was used inside larger
systems, before anybody published an argument for it; the two earliest papers
that argue for it both attribute it to others. So there is no work that *first
made this recommendation* in the sense `ADR-029` and `ADR-030` mean, and
`ADR-053` is what lets the record say so instead of promoting its best
citation into the slot. The frontmatter comment names what was searched, which
is how a reader refutes it.

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

## The regime where post-norm wins, and how much of the rest is initialisation

Everything above is about stability and about low-resource or deep settings.
`LIT-tmprikl1` ran the comparison at **high resource** — base Transformer,
WMT'14 English-German, `newstest2014`, tokenized BLEU — and the result goes
the other way:

| | BLEU |
| --- | --: |
| PostNorm + LayerNorm | **27.58** |
| PostNorm + FixNorm + ScaleNorm | 27.57 |
| PreNorm + FixNorm + ScaleNorm | 27.07 |
| PreNorm + LayerNorm | **26.83** |

**Post-norm by 0.75 BLEU**, which the paper flags as surprising and reports
Wang et al. (2019) observing too. Their summary is the one to carry: *"while
PostNorm performs better for high-resource NMT in the original base
Transformer regime, PreNorm is both more stable and more competent in
low-resource settings."*

Their speculation about the mechanism is **not** the collapse argument above —
they suggest identity residual networks act like shallow ensembles and thereby
*"undermine the learning of the longest path"*, and say further study is
required. Two accounts of the same cost, neither adjudicated here.

The second qualification is sharper, because it is about the headline failure.
On low-resource en→vi, post-norm with the default Xavier initialization
**fails to converge** at 4k and 8k warm-up steps and reaches 5.76 BLEU at 16k.
Reduce the attention layers' initialization (`SmallInit`) and the same
post-norm model reaches **28.17** at 4k, against pre-norm's 28.52.

So the dramatic version of this practice's motivation — post-norm diverges,
pre-norm does not — is **partly an initialization artefact**. The paper's own
phrasing is the accurate one: smaller initialization *"partly reclaims
PostNorm's stability"*, and pre-norm is *"less sensitive to this magnitude"*.
Less sensitive is a real advantage and a smaller one than "does not diverge".

What survives all of this unchanged is depth without warm-up, where the
placement difference is categorical rather than marginal: at five and six
encoder/decoder layers with no warm-up, post-norm **fails** and pre-norm sits
at 28.13 and 28.32.
