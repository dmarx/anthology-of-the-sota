---
status: Active
title: 'InfoNCE maximizes a lower bound on mutual information that cannot exceed log N'
version: 1
tags:
- analysis-and-evaluation
- representation-and-encoding
date: '2026-09-23'
source:
- LIT-tmp5vq8g
explains:
- SOTA-tmp6lc4c
---

# THEORY-tmpptbj9: InfoNCE maximizes a lower bound on mutual information that cannot exceed log N

## Source

Oord et al. (2018), [LIT-tmp5vq8g](../literature.d/LIT-tmp5vq8g.md) — [ARXIV-1807.03748](https://arxiv.org/abs/1807.03748), §2.3.

## The claim

The paper derives

> `I(x_{t+k}; c_t) ≥ log(N) − L_N`

where `L_N` is the InfoNCE loss over `N` candidates, and says the bound
"becomes tighter as N becomes larger". Two consequences follow from that one
line, and they point in opposite directions:

1. **Minimising the loss maximises a lower bound on mutual information.**
   This is the sense in which contrastive pretraining "maximises
   information", and it is what the objective is usually justified by.
2. **The bound cannot exceed `log N`.** `L_N` is a cross-entropy over `N`
   classes and so is non-negative; setting it to zero leaves `I ≥ log N`.
   With a batch of 32,768 — CLIP's, `LIT-588` — the certificate tops out at
   about **10.4 nats**, however much information the pair actually shares.

The second is arithmetic on the paper's own inequality, not a later result,
and the paper does not draw it.

## Why it matters, and what it does not license

A representation can be excellent while the bound is saturated, because a
saturated bound is a statement about what the estimator can *certify*, not
about what the encoder has *learned*. So:

- **"Contrastive learning maximises mutual information" is true of a bound
  and not of the quantity.** Once `L_N` is near zero the gradient signal is
  near zero too, and further training is optimising something the inequality
  has stopped measuring.
- **A reported InfoNCE value is not comparable across batch sizes**, since
  the achievable range is set by `log N`.
- **It does not follow that large batches are pointless.** They make the
  discrimination harder and the certificate larger. It follows only that the
  information framing cannot be the reason, past `log N`.

## Standing

Filed as the account behind [SOTA-tmp6lc4c](../practices.d/SOTA-tmp6lc4c.md), and filed separately from it
because it is the kind of claim `ADR-031` splits out: the practice can be
right while this explanation is the wrong reason for it. A subsequent
literature argues exactly that — that the MI framing is a poor account of why
contrastive pretraining works, and that what the objective really selects for
is better described in terms of alignment and uniformity on the sphere. The
record does not hold those papers yet; `#304` lists them.

The status is `Active` because the narrow claim here is arithmetic on the
paper's own inequality — `L_N` is a cross-entropy and so non-negative — and
not a mechanism anyone has to believe. That dispute is about whether the
bound is the right *explanation* for contrastive pretraining's success. This
document says only that the bound exists and where it stops, which stands
either way, and a result overturning the MI account would leave it intact
while removing most of the reason to care.
