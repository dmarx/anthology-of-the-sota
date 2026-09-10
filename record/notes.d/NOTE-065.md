---
number: 65
status: Read
formerly:
- NOTE-tmps3e9a
paper: LIT-020
title: 'Pay Less Attention with Lightweight and Dynamic Convolutions'
version: 1
tags:
- attention-techniques
date: '2026-09-09'
summary: >-
  Shows a depthwise convolution with softmax-normalized weights, shared across channel groups and with a kernel fixed at 31 or less, matches self-attention on translation — 29.7 BLEU on WMT En-De. Dynamic convolution predicts the kernel from the current token alone, so the mixing weights depend on position rather than on the pair of positions being mixed.
---

# NOTE-065: Pay Less Attention with Lightweight and Dynamic Convolutions

## Contribution

An ablation of self-attention dressed as an architecture paper, and the more
useful reading is the ablation. Two components:

- **LightConv** — a depthwise separable convolution that additionally
  **shares weights across channel groups** and **softmax-normalizes the kernel
  over its temporal extent**. A depthwise kernel `W ∈ ℝ^{d×k}` with `d=1024`,
  `k=3` has 7,168 weights; sharing collapses that by the group factor.
- **DynamicConv** — the same, but the kernel is **predicted from the current
  token's representation**, so it varies by position while remaining a fixed
  finite window.

## Key insight

Self-attention computes a mixing weight for every *pair* of positions.
DynamicConv computes mixing weights from **one** position — the current one —
and applies them over a fixed window. It cannot condition on what it is
attending to.

That it nonetheless matches self-attention on translation is the finding, and
it is a claim about the task: for machine translation at these lengths, the
content of the *other* token is apparently not what determines how much it
should be mixed in. Position and the current token suffice.

The softmax over the kernel is the other quiet decision. Normalising the
kernel's temporal extent makes it a weighted average rather than a free linear
map, which is the structural property self-attention has and an ordinary
convolution does not.

## Assumptions

- **A fixed, small window suffices.** Kernel sizes are 3, 7, 15 and 31 across
  encoder blocks — the largest is 31 tokens, and there is no mechanism for
  anything further.
- Translation-scale sequences and 2019 model sizes.
- Weight sharing across channels does not cost representational capacity in a
  way these tasks detect.

## Key results

- **29.7 BLEU on WMT English–German**, matching the best reported
  self-attention results at the time; matches the best on English–French.
- Also evaluated on language modelling and abstractive summarisation.
- Ablations isolate the softmax normalisation and the weight sharing as the
  parts that matter.
- Kernel schedule **3, 7, 15, 31** per block — the receptive field is grown by
  depth, not by one wide kernel.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | A softmax-normalized shared depthwise convolution matches self-attention on translation | strong | 29.7 BLEU, multiple language pairs |
| C2 | Content-based pairwise weighting is not necessary for these tasks | moderate | C1 implies it; not isolated directly |
| C3 | Softmax-normalizing the kernel is load-bearing | moderate | ablated |
| C4 | A window of ≤31 with depth suffices | moderate | the configuration works; no study of where it fails |
| C5 | Predicting the kernel from the current token beats a static kernel | moderate | LightConv vs DynamicConv comparison |

## Method

Replace self-attention with a depthwise convolution whose weights are shared
across channel groups and softmax-normalized over the kernel window; optionally
predict those weights from the current token. Grow the kernel with depth.

## Concepts

- **Softmax over a kernel** — turning a convolution into a weighted average,
  which is the property being borrowed from attention.
- **Position-conditioned rather than pair-conditioned mixing** — the precise
  thing DynamicConv gives up, and the axis on which to read every
attention-replacement paper since.
- **Kernel growth with depth** — the same receptive-field-by-depth argument
  `LIT-033` makes with windows.

## Connections

Sits with `LIT-033` and the rest of the attention-replacement wave that lost to
exact attention made fast (`SOTA-086`). Its precise question — *does mixing
need to be conditioned on both positions or only one?* — is the question the
<!-- inactive-ok-block: SOTA-167, SOTA-177, SOTA-178 — Proposed, named as the record's neighbourhood for this question rather than relied on -->
modern linear-attention and state-space line (`SOTA-167`, `SOTA-177`,
`SOTA-178`) re-asks with different machinery: a recurrent state is also a way
of mixing without a pairwise score.

<!-- inactive-ok-block: SOTA-167, SOTA-177, SOTA-178 — Proposed, named as the record's neighbourhood for this question rather than relied on -->
`SOTA-178`'s framing — vector-valued gating and in-context learning rates so a
recurrence can track state a softmax layer provably cannot — is the modern,
sharper version of the same axis, running in the opposite direction.

## Recommendations

- **R1** — Before assuming pairwise content-based attention is necessary, test
  whether position-conditioned mixing suffices for the task. *Topic:*
  attention techniques. *Strength:* moderate — established for translation at
  2019 scale.
- **R2** — Softmax-normalize a mixing kernel so it is an average rather than a
  free linear map. *Strength:* moderate.
- **R3** — Grow the kernel with depth rather than widening one. *Strength:*
  strong; the same argument holds for windows and for convolutional stacks.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice.**

The reading's value is that it dates a question the record treats as new. The
<!-- inactive-ok-block: SOTA-167, SOTA-177, SOTA-178 — Proposed, named as the record's neighbourhood for this question rather than relied on -->
linear-attention and state-space practices (`SOTA-167`, `SOTA-177`, `SOTA-178`)
are all, at bottom, about how much of attention's pairwise content-conditioning
is actually load-bearing. This 2019 paper answers "for translation, none of
it", with a fixed 31-token window. That answer did not survive the move to long
contexts and general language modelling, and *why* it did not is the more
interesting question than the practices currently make it look — the record
carries the modern attempts without the earlier negative result they are
implicitly answering.

The document's takeaways — "alternative to self-attention", "dynamic parameter
generation", "reduced computational complexity", "competitive performance with
transformers" — are accurate and would fit forty other papers.

## Limitations

- 2019, translation-scale sequences, no long context.
- The 31-token ceiling is structural, and the paper does not test where it
  breaks.
- C2 is inferred from parity rather than isolated.
- Whether the result survives decoder-only language modelling at scale is
  exactly what nobody re-ran, and the field moved on instead.

## Open questions

- Where does position-conditioned mixing actually fail? The record has a
  generation of papers reintroducing content conditioning by other means and no
  statement of what the earlier approach could not do.
