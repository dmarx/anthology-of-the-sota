---
number: 358
status: Active
formerly:
- SOTA-tmp9k3cq
consensus: converged
consensus_note: >-
  Measured, not assumed, and measured on the wrong half. The field has
  converged on the conclusion — a patch-sequence transformer is the default
  vision backbone, and the `#290` triage found 47 documents in this record
  alone using one as an experimental subject. What has not converged is the
  condition: the threshold gets restated as a preference for the
  architecture, so adopters below it inherit a choice the paper argues
  against. Read as of 2026-09.
title: 'Drop the domain inductive bias once pre-training data is large enough, and keep it when it is not'
version: 1
tags:
- model-architecture
- training-optimization
- vision-and-graphics
date: '2026-09-23'
source:
- LIT-587
introduced_by:
- LIT-587
implementations: []
---

# SOTA-358: Drop the domain inductive bias once pre-training data is large enough, and keep it when it is not

## Source

Dosovitskiy et al. (2020), [LIT-587](../literature.d/LIT-587.md) — [ARXIV-2010.11929](https://arxiv.org/abs/2010.11929).

## The claim

A domain-specific architectural prior — locality and translation equivariance
in vision, and its analogues elsewhere — is a **substitute for data, not a
free improvement**. Above a pre-training scale you can measure, removing it
and letting the model learn the structure wins. Below that scale, keeping it
wins. Both halves are results in the same paper.

The measurements, all with the architecture held fixed:

- **Model size crosses over with data.** Pre-trained on ImageNet-1k,
  ViT-Large is *worse* than ViT-Base despite tuned regularisation. On
  ImageNet-21k (14M) they are level. Only on JFT-300M does the larger model
  pay.
- **The crossover is not a regularisation artefact.** On random 9M/30M/90M/
  300M JFT subsets with hyperparameters and regularisation held fixed,
  ViT-B/32 — slightly cheaper than ResNet-50 — is *much worse* at 9M and
  *better* at 90M and above. Same for ViT-L/16 against ResNet152x2.
- **The prior's value shrinks with budget, it does not invert.** Hybrids
  that feed ResNet feature maps into the transformer beat pure ViT at small
  compute, and the gap vanishes as models grow.

## Why it is stated this way

Because the citable half is "transformers beat CNNs" and the paper does not
say that. It says large-scale training trumps inductive bias, and it measures
where "large" starts. A practitioner who takes the conclusion without the
condition — a patch transformer on a 50k-image dataset — has adopted the
recommendation in the regime where its own source shows the opposite.

The claim is filed under `model-architecture` rather than
`vision-and-graphics` because the domain is the setting, not the subject
(`ADR-046`). Vision is where this was measured; the trade it names —
hand-built prior against data volume — is not about vision.

## Conditions

- **The threshold is measured for image classification with these
  architectures, and the numbers do not transfer.** 9M-vs-90M is a fact
  about ViT-B/32 and ResNet-50 on JFT, not a constant. What transfers is
  that a threshold exists and can be found by the same experiment: hold
  hyperparameters fixed, sweep pre-training set size, and look for the
  crossover.
- **This assumes you get to choose the pre-training scale.** If the data is
  fixed and small, the practice reduces to "keep the prior", which is the
  less-quoted half.
- **Removing a prior costs compute, not just accuracy, below the
  threshold.** The paper's own scaling study is downstream of JFT-300M,
  where data does not bottleneck; the 2–4× compute advantage it reports for
  ViT is a statement about that regime and not about small ones.
- **It is about the architectural prior, not about pre-training being
  optional.** The supervised pre-training this rests on was not replaced by
  the paper's own self-supervised attempt, which landed 4 points behind.

## Known implementations

-
