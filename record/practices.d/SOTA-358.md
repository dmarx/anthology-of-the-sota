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
version: 2
history:
- version: 2
  date: '2026-09-24'
  note: >-
    The weight shifted off the first measurement and onto the second.
    Beyer et al. (LIT-tmp5t7v1) show the ImageNet-1k recipe those numbers
    came from leaves 13.2 points unclaimed, so "despite tuned
    regularisation" cannot carry the argument. The JFT subset sweep is
    unaffected and the conclusion now rests on it. Status unchanged.
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
  pay. **This measurement has since lost most of its weight** — see below.
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

## What the ImageNet-1k half no longer supports

The first measurement above rests on ViT's ImageNet-1k configuration, and
Beyer et al. ([LIT-tmp5t7v1](../literature.d/LIT-tmp5t7v1.md)) measured what that configuration was worth:
**66.8% top-1 for ViT-S/16, against 80.0% from five changes none of which is
a regulariser.** The original recipe also does not improve with training —
66.8 → 67.2 → 67.1 across 90, 150 and 300 epochs — so it had stopped learning
before any of these comparisons were drawn.

The phrase carrying the argument was *"despite tuned regularisation"*. Beyer
et al.'s abstract names that belief directly and answers it: the lever was
augmentation, and sophisticated regularisation was not what ImageNet-1k-scale
ViT needed.

**What this does not do is refute the crossover.** Beyer et al. ran ViT-S/16
only. Whether ViT-Large would still lose to ViT-Base under their recipe is
**untested**, and nothing here says the ordering flips.

**What it does is move the load.** The second measurement — random JFT subsets
at 9M / 30M / 90M / 300M with hyperparameters and regularisation held fixed —
never depended on anyone having tuned ImageNet-1k well, because it compares
ViT against ResNet inside one protocol across data scales. That is now where
this practice's condition comes from. A reader who wants the threshold should
read the second bullet and treat the first as an illustration whose numbers
are known to be loose.

The general form is worth keeping: **a crossover measured with an
under-tuned configuration on one side is evidence about the tuning as much as
about the crossover**, and which one it is cannot be told from the crossover
alone.

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
