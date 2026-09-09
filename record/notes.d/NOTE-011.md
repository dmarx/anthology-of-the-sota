---
number: 11
status: Read
formerly:
- NOTE-tmpct2nt
paper: LIT-008
title: 'Attention Is All You Need'
version: 1
tags:
- model-architecture
date: '2026-09-09'
summary: >-
  Dispenses with recurrence and convolution entirely. The 1/√d_k scaling has a stated reason: with unit-variance components, q·k has variance d_k, and unscaled dot products push the softmax into regions of extremely small gradients.
---

# NOTE-011: Attention Is All You Need

## Contribution

Prior sequence architectures reduced sequential computation by stacking
convolutions, and paid for it: the operations needed to relate two positions
grew with their distance — linearly for ConvS2S, logarithmically for ByteNet
— which "makes it more difficult to learn dependencies between distant
positions". The Transformer reduces that to a **constant** number of
operations for any pair, at the cost of "reduced effective resolution due to
averaging attention-weighted positions", which is what **multi-head
attention** exists to counteract.

## Key insight

Distance between positions should not be a cost. Once relating any two
positions is `O(1)` operations, depth stops being the mechanism for
long-range dependency and becomes free for other work. The trade this
introduces — averaging over attention-weighted positions blurs resolution —
is real and is answered structurally rather than by adding capacity: several
heads attend in parallel to different subspaces.

## Assumptions

- Machine translation is the evaluation domain (WMT En-De, En-Fr), 2017
  scales, trained on eight P100 GPUs.
- The scaling argument assumes **components of `q` and `k` are independent
  random variables with mean 0 and variance 1** — stated explicitly in the
  paper's footnote, and true at initialization rather than throughout
  training.
- Dot-product attention is chosen over additive on a *practical* argument —
  "much faster and more space-efficient, since it can be implemented using
  highly optimized matrix multiplication code" — not a quality one.

## Key results

- **`O(1)` operations to relate any two positions**, against ConvS2S's linear
  and ByteNet's logarithmic growth in distance.
- **The `1/√d_k` scaling, and why.** Additive attention outperforms unscaled
  dot-product attention at larger `d_k`. The paper's explanation: for large
  `d_k` the dot products "grow large in magnitude, pushing the softmax
  function into regions where it has extremely small gradients". The footnote
  gives the arithmetic — with `q` and `k` components independent, mean 0,
  variance 1, then `q·k = Σᵢ qᵢkᵢ` has **mean 0 and variance `d_k`**. Scaling
  by `1/√d_k` returns it to unit variance.
- **Multi-head attention** counteracts the resolution loss from averaging
  attention-weighted positions.
- No recurrence, no convolution.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Attention alone suffices for sequence transduction | strong | the results, and everything since |
| C2 | Relating two positions in `O(1)` operations helps long-range dependency | strong | the complexity argument, plus measured quality |
| C3 | Unscaled dot products saturate the softmax at large `d_k` | moderate | "we suspect", supported by the variance argument and by additive attention's known advantage there |
| C4 | `1/√d_k` is the right scale | strong | follows directly from the variance being `d_k` |
| C5 | Multi-head attention recovers resolution lost to averaging | moderate | argued and ablated, not isolated analytically |

## Method

Scaled dot-product attention: `softmax(QKᵀ/√d_k)V`. Several heads in
parallel over projected subspaces, concatenated and projected out.

## Concepts

- **Scaled dot-product attention** — the paper's name for its compatibility
  function. The scaling is part of the definition, not a trick applied to it.
- **Effective resolution** — what averaging attention-weighted positions
  costs, and the thing multi-head attention is introduced to counteract. A
  framing the record does not otherwise carry.

## Connections

Positioned against ConvS2S, ByteNet and the Extended Neural GPU — all
reducing sequential computation with convolutions — and against additive
attention, which it beats on speed rather than on quality. It is the parent
of essentially everything else in this record.

## Recommendations

- **R1** — Scale dot-product attention by `1/√d_k`. *Topic:* attention.
  *Status:* standard. *Strength:* strong. *Applies when:* always; it is part
  of the operation's definition.
- **R2** — When a compatibility function's magnitude grows with a dimension,
  check what that does to the softmax's gradients. *Topic:* architecture.
  *Status:* standard. *Strength:* moderate. *Applies when:* designing any
  scoring function feeding a softmax — the general form of C3.
- **R3** — Prefer the operation that maps to optimized matmul. *Topic:*
  kernels. *Status:* standard. *Strength:* moderate. *Applies when:* two
  formulations are of similar quality; this paper chose on that basis and was
  right, and `LIT-115` makes the same argument fifteen years of hardware
  later.

## Bearing on the record

**The one practice sourced to this note is confirmed.**

| practice | disposition |
|---|---|
| [SOTA-050](../practices.d/SOTA-050.md) scale attention weights by `1/sqrt(head_dim)` | confirmed — C3, C4 |

The reading supplies the *reason*, which the practice states as a formula.
The variance argument is a footnote in the original and is the whole
justification: `q·k` has variance `d_k`, so an unscaled score grows with the
dimension and saturates the softmax. A reader who knows only the formula
cannot tell whether it generalises; a reader who knows the argument can, and
`R2` is that generalisation.

Worth noting the paper's own hedge — "we **suspect** that for large values of
`d_k`" — which is weaker than the record's flat statement, and honest about
being an explanation offered rather than isolated.

## Limitations

- 2017 translation benchmarks.
- C3 is stated as a suspicion with a supporting argument, not a measurement
  of softmax gradient magnitudes.
- The variance argument holds at initialization, where components are
  plausibly independent with unit variance. Whether it holds after training
  is not addressed, and is the assumption everything downstream inherits.

## Open questions

- The `1/√d_k` scaling assumes unit-variance, independent components. Modern
  models normalise queries and keys explicitly (QK-norm) — is that fixing the
  same problem the scaling was fixing, and does the scaling still earn its
  place alongside it?
- "Reduced effective resolution due to averaging" is a cost this paper names
  and the record does not otherwise discuss. Is it what the attention-sink
  and entropy-collapse literature is measuring?
