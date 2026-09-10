---
status: Skimmed
paper: LIT-021
title: 'Mish: A Self Regularized Non-Monotonic Activation Function'
version: 1
tags:
- model-architecture
date: '2026-09-09'
summary: >-
  Proposes f(x) = x·tanh(softplus(x)), a smooth non-monotonic activation in the Swish family. Reported +2.1 AP50 over Leaky ReLU on YOLOv4/MS-COCO and ~1% top-1 over ReLU on ResNet-50/ImageNet. Read from the abstract only — ar5iv has no rendering for this identifier.
---

# NOTE-tmpmuch0: Mish: A Self Regularized Non-Monotonic Activation Function

**This note is `Skimmed`, not `Read`.** `ar5iv` has no rendering for
`arXiv:1908.08681`, so what follows comes from the abstract and listing
metadata. Under [ADR-025](../decisions.d/ADR-025.md) that is not enough to source a practice from, and
this note deliberately has no claims table.

## Contribution

An activation function:

    f(x) = x · tanh(softplus(x))

described as **self-regularized** and **non-monotonic**, and validated against
"the best combinations of architectures and activation functions" on standard
benchmarks. BMVC 2020.

## Key insight

*(From the abstract; not verified.)* The paper's stated explanation is about
the **first derivative's behaviour acting as a regularizer**, and it positions
Mish explicitly in relation to the **Swish family** — `x·σ(βx)` — rather than
as an unrelated construction. So the claim is not merely that a new curve works
better, but that a property of its derivative is why.

Non-monotonicity means small negative inputs produce a small negative output
rather than zero, which is the shared feature of this whole family and the
usual explanation offered for it.

## Assumptions

Not established from the abstract. Convolutional vision architectures, 2019–20.

## Key results

*(As stated in the abstract.)*

- **+2.1 AP50** over Leaky ReLU on YOLOv4 with a CSP-DarkNet-53 backbone,
  MS-COCO object detection.
- **≈1% top-1** over ReLU on ResNet-50, ImageNet-1k.
- Both "while keeping all other network parameters and hyperparameters
  constant" — which, if it holds, is the right comparison and the one
  activation-function papers most often fail to make.
- The abstract also observes that **data augmentation has a favourable effect**
  on these benchmarks across architectures, which is a separate claim bundled
  into the same sentence and is not obviously about Mish at all.

## Concepts

- **Non-monotonic activations** — the family, including Swish/SiLU and GELU,
  and the axis this paper sits on.
- **The derivative as a regularizer** — the paper's own proposed explanation,
  unverified here.

## Bearing on the record

**Nothing is sourced to this paper and this reading files no practice** — and
in this case that is a conclusion, not a deferral. The record's activation
practice is SwiGLU-shaped, and the gated-linear-unit line is where language
modelling went; Mish is a CNN-vision activation from the pre-gating era, and
holding it at `Active` in the anthology is generous.

Marked `Skimmed` because the full text was unavailable through the route used
for the rest of this pass, and because the two numbers above are the whole of
what the abstract supports. This is the second use of `Skimmed` in the record
and the same reason as the first: recording a gap where the next reader will
find it rather than implying a reading that did not happen.

The document's takeaways — "new activation function", "better gradient flow",
"self-regularizing properties", "improved model performance" — restate the
title and the abstract's own adjective. "Better gradient flow" is not a claim
the abstract makes.

## Limitations

Of this note, not the paper: everything above is the abstract. No method
detail, no assumptions, no ablations, no claims table.

## Open questions

- **Get the full text and upgrade this note to `Read`**, or decide the paper's
  standing without it. Given that the record's activation practices are
  SwiGLU-shaped, the second is defensible and cheaper.
- Is the derivative-as-regularizer argument a real mechanism or a post-hoc
  story? That is the only thing here that would generalise past the curve.
