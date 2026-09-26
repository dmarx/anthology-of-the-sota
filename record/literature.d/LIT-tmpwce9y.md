---
status: Active
title: 'Visualizing and Understanding Convolutional Networks'
version: 1
tags:
- analysis-and-evaluation
- vision-and-graphics
- model-architecture
date: '2026-09-26'
published: '2013-11-12'
arxiv: '1311.2901'
first_author: 'Zeiler'
keywords:
- deconvolutional network
- feature visualization
- occlusion sensitivity
- ablation study
implementations:
- 'captum (Deconvolution, Occlusion)'
- ZFNet
summary: >-
  Zeiler and Fergus (2013), [ARXIV-1311.2901](https://arxiv.org/abs/1311.2901). Two attribution families start
  here and the record depends on both. The **deconvnet** is the approach guided
  backprop ([LIT-tmpw88iy](LIT-tmpw88iy.md)) is explicitly "a new variant of", and so is the
  antecedent of [SOTA-430](../practices.d/SOTA-430.md)'s headline failure case. **Occlusion sensitivity** —
  slide a grey square, watch the class probability — is the perturbation-based
  family [LIT-725](LIT-725.md) names as its own origin, and [LIT-725](LIT-725.md)'s infidelity is its
  quantitative descendant. Also an early depth-against-parameters ablation:
  removing the fully connected layers costs little, removing them *and* two
  middle conv layers is "dramatically worse".
---

<!-- inactive-ok-file: SOTA-430 — Proposed, and cited twice for the same reason: this paper's deconvnet is the antecedent of the method in that practice's failing row, and its occlusion test is the positive-validation move the practice explicitly cannot make. Neither depends on the recommendation being in force. -->

# LIT-tmpwce9y: Visualizing and Understanding Convolutional Networks

Zeiler and Fergus (2013) — [ARXIV-1311.2901](https://arxiv.org/abs/1311.2901)

## Key takeaways

- **The deconvnet, and the switches that make it work.** Given a high-level
  feature map, leave one neuron non-zero and invert the data flow back to
  image space. Max-pooling is not invertible, so the method "requires first to
  perform a forward pass of the network to compute 'switches' — positions of
  maxima within each pooling region". Those switches are what condition the
  reconstruction on the image, and the paper is explicit that because of them
  the deconvnet "is hence conditioned on an image and does not directly
  visualize learned features".
- **Occlusion sensitivity.** Slide a grey square over the input and watch two
  things: the classifier's probability for the correct class, and the summed
  activity of the strongest feature map in the top conv layer. Both drop when
  the occluder covers the region the visualization highlights.
- **And the paper uses the second to validate the first**, in its own words:
  "This shows that the visualization genuinely corresponds to the image
  structure that stimulates that feature map, hence validating the other
  visualizations." A perturbation that moves the model is offered as evidence
  that a visualization is about the model. Three test examples, qualitative.
- **The visualizations are used diagnostically, not decoratively.** They
  motivate architecture changes that beat Krizhevsky et al. on ImageNet:
  14.8% test error with multiple models, against 16.4%, described as "almost
  half" the best non-convnet result (26.2%).
- **An early depth-against-parameters ablation.** Removing the fully connected
  layers 6 and 7 "only gives a slight increase in error ... surprising, given
  that they contain the majority of model parameters"; removing two middle
  convolutional layers is also small; removing **both** gives a four-layer
  model that is "dramatically worse". Widening the middle conv layers helps;
  widening them and the FC layers together overfits.

## Standing in the anthology

Filed with [LIT-tmpw88iy](LIT-tmpw88iy.md) as a pair, because guided backpropagation is
defined in that paper as a variant of this one's deconvnet, and the record
already holds the verdict on both without holding either.

**Two families begin here and the record leans on each.**

| what | where the record depends on it |
| --- | --- |
| deconvnet → guided backprop | [SOTA-430](../practices.d/SOTA-430.md)'s verdict table; its **headline failure case** is guided backprop's maps surviving weight randomization |
| occlusion sensitivity | [LIT-725](LIT-725.md) names it as the origin of perturbation-based attribution, and its infidelity measure is a perturbation-based fidelity criterion |

The second is the one a dependence count would miss. `LIT-725` says it
plainly — "perturbation-based attributions measure the prediction difference
after perturbing a set of features. Zeiler & Fergus 2014 use such perturbations
with grey patch occlusions on CNNs" — and its "Square" perturbation, uniform
over square patches, is a grey square with a distribution over it. The record
acquired a perturbation-based metric yesterday and did not hold the
perturbation-based method it descends from.

**No practice is filed for occlusion sensitivity.** The positive-validation
move it makes — perturb what the attribution highlights and check the output
moves — is worth having, and the record already has it in quantitative form
as `LIT-725`'s infidelity, under [SOTA-435](../practices.d/SOTA-435.md). Filing the 2013 qualitative
version separately would be filing on antecedence rather than on a defect,
which is the call [LIT-722](LIT-722.md) got two units ago. What this note adds is the
lineage: the modern metric's family has a named origin and a three-example
qualitative start.

**The ablation is out of scope and worth a line anyway.** "Most of the
parameters are in the layers that matter least, and depth is what matters" is
a 2013 result in a record with a large scaling cluster, and nothing here cites
it. It is not this unit's subject and is not a defect in anything held.

## Limitations

- **2013, AlexNet-scale, ImageNet classification.** The deconvnet is defined
  against a max-pooling architecture and needs it.
- **The occlusion validation is three examples and a figure.** No metric, no
  threshold, no baseline for what an unfaithful visualization would have
  looked like under the same test — which is the gap [LIT-713](LIT-713.md) closes five
  years later, in the rejecting direction.
- **The visualizations are qualitative throughout**, and the paper's own
  argument for them is that they led to a better architecture. That is
  evidence the *process* worked, not that the maps are faithful.
