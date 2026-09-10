---
status: Read
paper: LIT-033
title: 'Longformer: The Long-Document Transformer'
version: 1
tags:
- attention-techniques
date: '2026-09-09'
summary: >-
  Replaces full self-attention with a sliding window plus a small set of task-chosen global positions, giving linear cost in sequence length. The global tokens are the design decision that matters — they are where the task's inductive bias is stated, and they are why the pattern can be adapted per task rather than fixed.
---

# NOTE-tmppu8qj: Longformer: The Long-Document Transformer

## Contribution

Self-attention is quadratic, which caps document length. Longformer combines
two sparse patterns whose union is cheap and, for the tasks considered,
sufficient:

- a **sliding window** of fixed width around each position — local context,
  linear in sequence length;
- **global attention** at a small number of positions chosen per task — those
  positions attend to everything and everything attends to them.

Plus a **dilated** window variant for the language-modelling setting, which
reaches sequences of up to 32K characters at the same cost.

## Key insight

The global tokens are not a patch on the window's limitations; they are
**where the task's inductive bias gets stated**. The paper says so directly:
global attention "encodes inductive bias about the task". For question
answering you make the question tokens global; for classification, the
`[CLS]` token. The pattern is a per-task decision, not an architectural
constant.

That is the durable idea. The window gives you locality for free, and the
handful of global positions is a deliberate, legible, task-specific statement
about which tokens need to see everything — as opposed to learned sparsity,
where the same decision is made invisibly.

Stacking windows also matters: `k` layers of width-`w` windows gives an
effective receptive field of `k·w`, which is why a small window suffices for
documents. The paper varies the window per layer rather than fixing it.

## Assumptions

- **Locality plus a few global anchors is enough.** True for QA, coreference
  and document classification; asserted rather than characterised in general.
- Someone knows which tokens should be global. This is a strength (legible)
  and a limitation (manual).
- Implementation requires custom kernels — the dilated pattern uses 8×8 block
  sparsity from BlockSparse. The complexity is linear; the constant is not
  free.

## Key results

- **Linear scaling in sequence length**, against quadratic.
- **Up to 32K characters** with the dilated pattern in autoregressive language
  modelling.
- Gains on long-document QA, coreference resolution and document
  classification, with ablations on WikiHop.
- **LED (Longformer-Encoder-Decoder):** encoder uses local+global, decoder
  keeps *full* attention over the encoded tokens and previously decoded
  positions. The asymmetry is the point — output sequences are short, so only
  the encoder needs the sparse pattern.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Sliding window plus task-chosen global positions scales linearly and suffices for long-document tasks | strong | measured across three task families |
| C2 | Global positions are where task inductive bias belongs | moderate | argued and demonstrated per task; not compared against learned sparsity |
| C3 | Stacked windows give a `k·w` receptive field | strong | structural |
| C4 | Dilation extends reach at constant cost | moderate | used for LM, requires block-sparse kernels |
| C5 | Only the encoder needs sparsity in seq2seq | moderate | LED's design, justified by output length |

## Method

Attend within a window of width `w` around each position, varying `w` by layer;
add dilation for language modelling; designate a small task-specific set of
positions as global, attending and attended everywhere. Implement with
block-sparse kernels.

## Concepts

- **Global tokens as declared inductive bias** — the transferable idea, and
  the one that outlived the architecture.
- **Receptive field by depth** — `k` layers × window `w`, the same argument
  convolutional stacks make.
- **Asymmetric sparsity in seq2seq** — sparse where the sequence is long, dense
  where it is short.

## Connections

One of the efficient-attention generation — with `LIT-020` in the same
neighbourhood — that the record does not carry as practice, because the field's
answer became exact attention made fast (`SOTA-086`, FlashAttention) rather
than approximate attention made sparse.

But the global-token idea survived the architecture. `SOTA-134`'s
attention-sink neighbourhood is about positions that everything attends to
arising *spontaneously* in a trained model; Longformer is the same structure
<!-- inactive-ok-block: SOTA-176 — Proposed, named as the record's neighbourhood for this question rather than relied on -->
imposed deliberately. Sliding-window-plus-something is also exactly the shape
of `SOTA-176` (long-term slots plus a sliding window under one softmax), where
"something" is learned rather than designated.

## Recommendations

- **R1** — When imposing sparsity, state which positions must see everything as
  a task decision rather than learning it. *Topic:* attention techniques.
  *Strength:* moderate.
- **R2** — Get receptive field from depth × window rather than from a wide
  window. *Strength:* strong.
- **R3** — Make sparsity asymmetric in an encoder-decoder: sparse where the
  sequence is long. *Strength:* moderate.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice.** The
approximate-attention line lost to exact-attention-made-fast, and the record
correctly reflects that.

The reading connects two things the record holds separately: Longformer's
**designated** global tokens and `SOTA-134`'s **emergent** attention sinks are
the same structure — a small number of positions that everything attends to —
arrived at by design in 2020 and by observation later. That the mechanism shows
up unbidden in models nobody designed it into is a stronger argument for its
necessity than Longformer's own results, and the record now has both halves in
view.

The document's takeaways say "efficient attention for long sequences", "linear
complexity attention" and "global-local attention patterns" — three ways of
naming the mechanism without the design decision inside it, which is that
someone chooses the global positions per task.

## Limitations

- 2020; encoder-heavy tasks; the LM result is character-level.
- C1 holds for tasks where locality plus anchors suffices, and the paper does
  not say which tasks those are in general.
- The implementation needs custom block-sparse kernels, so "linear" hides a
  constant that mattered a great deal in practice.
- No comparison against learned sparsity, which is C2's natural control.

## Open questions

- Are Longformer's chosen global tokens and the sinks models learn on their own
  in the same positions? Nobody appears to have checked, and it is checkable.
