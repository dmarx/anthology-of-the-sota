---
number: 430
status: Proposed
formerly:
- SOTA-tmpudd8t
promote_when: >-
  A group other than the authors applies both randomization tests to a
  setting where the true dependence of the output on the input is KNOWN by
  construction — a synthetic task or a planted feature — and reports that the
  tests' verdicts agree with that ground truth. That means a method that fails
  is unfaithful there, and a method that passes is not. The verdict should be
  stated as a threshold on a named similarity metric, not read from curves, and
  the setting should include at least one non-image model. What would NOT meet
  it: papers that run the tests on a new method and report that it passes,
  which is adoption (DP-005); more image-classifier sweeps of the same kind,
  which are the result already held; or a critique of the test that the record
  has not read in full (`2106.07475` is the first to read).
consensus: unassessed
consensus_note: >-
  Not judged. captum's README links the source as a critique of methods it
  ships, which is adoption of the test as a reference and not evidence for it.
  A follow-up literature exists that questions the model-randomization test
  (captum also links `2106.07475`). The record holds none of it and has not
  read it. Read as of 2026-09.
title: 'Before using an attribution map to debug a model or explain what it learned, check that the map changes when the weights are randomized and when the labels are permuted — do not validate it by how it looks'
version: 1
tags:
- analysis-and-evaluation
date: '2026-09-25'
source:
- LIT-713
# The same authors stated the parameter-sensitivity check first, in "Local
# explanation methods for deep neural networks lack sensitivity to parameter
# values" (Adebayo, Gilmer, Goodfellow and Kim, 2018; ICLR workshop), which this
# paper cites as [37]. That paper is not held. The two-test form, and the
# instruction to run the tests before deploying a method, are stated here.
introduced_by:
- LIT-713
implementations: []
summary: >-
  Adebayo et al. (2018), [LIT-713](../literature.d/LIT-713.md), read as [NOTE-365](../notes.d/NOTE-365.md). An attribution map
  that survives re-initializing the model's weights, or retraining on permuted
  labels, cannot be telling you about the weights or the labels. Guided
  Backprop and Guided GradCAM survive the first above the lowest layers, and
  their maps look as convincing as ever. A rejection rule, not a certificate:
  passing does not show a method is faithful. The evidence is image
  classifiers only, and pass or fail is read from curves.
---

# SOTA-430: Before using an attribution map to debug a model or explain what it learned, check that the map changes when the weights are randomized and when the labels are permuted — do not validate it by how it looks

## Source

Adebayo, Gilmer, Muelly, Goodfellow, Hardt and Kim (2018; NeurIPS 2018),
[LIT-713](../literature.d/LIT-713.md) — [ARXIV-1810.03292](https://arxiv.org/abs/1810.03292), read in full (v3, November 2020) as
[NOTE-365](../notes.d/NOTE-365.md). The instruction is the paper's own: "our tests can be thought of
as sanity checks to perform before deploying a method in practice."

## Do this

On *your* model, with the attribution method you intend to use:

1. **Model parameter randomization.** Re-initialize the weights from the output
   layer downward, one block at a time, recomputing the maps at each step. Also
   re-initialize one layer at a time with the rest left trained. If the maps
   stay similar while the weights they are supposed to explain are destroyed,
   the method cannot support debugging this model.
2. **Data randomization.** Train the same architecture on permuted labels to
   high training accuracy, and compare its maps with the real model's on the
   same inputs. If they stay similar, the method cannot tell you what the model
   learned about the input–label relationship.
3. **Compare with signed rank correlation as well as absolute or perceptual
   similarity.** The two disagree. On Integrated Gradients and
   gradient⊙input the absolute-value rank correlation and SSIM stay high after
   randomization, while the signed rank correlation drops to about zero at
   once. A single metric can hand you either verdict.

And the negative half, which carries its own evidence: **do not accept a method
because its maps look like the object.** An untrained edge detector produces
maps "strikingly similar" to several methods'. Guided Backprop's maps on a
network randomized above its lowest layers remain "visually and quantitatively
similar" to the trained network's.

## What the source found, which tells you what to expect

| method | weights randomized | labels permuted |
| --- | --- | --- |
| Gradient, SmoothGrad | changes | changes |
| GradCAM | changes once the last conv layer is randomized | changes (disconnected patches) |
| Guided Backprop, Guided GradCAM | **invariant to higher layers**; changes only with the lowest | visible change, still covers the object |
| Integrated Gradients, gradient⊙input | structure persists; sign decorrelates | sign changes; input structure "clearly prevalent" |

The paper names gradients and GradCAM as passing and Guided Backprop and Guided
GradCAM as failing. **It gives Integrated Gradients ([LIT-712](../literature.d/LIT-712.md)) no verdict**,
and neither does this practice.

## What the evidence does not cover

- **A pass is not a certificate.** The tests are necessary conditions. The
  plain gradient passes both, and the paper does not claim it is faithful.
- **Image classifiers only.** Inception v3 on ImageNet, and a small CNN and MLP
  on MNIST and Fashion-MNIST. The tests are defined for any method and any
  model. That they discriminate on a transformer or on token attributions is
  unmeasured.
- **No threshold.** "Similar" is read from curves and figures. There is no
  significance test, and the number of inputs behind the main figures is not
  stated.
- **The paper corrected itself once.** An earlier version said Guided Backprop
  was *entirely* invariant. v3 withdraws that after a bug report (footnote 5).
  The abstract's "independent both of the model and of the data generating
  process" is the pre-correction strength. Cite the body.
- **Whether the model-randomization test measures what it claims is itself
  disputed** in a later literature the record does not hold. That is the reason
  this practice is `Proposed`.

## Where this does not apply

If you only want a map that reflects the architecture's prior, or an
image-processing view of the input, a method that fails these tests can still
serve. The paper says so (§5.1). But then it is not an explanation of what the
model learned, and it should not be presented as one.

## Known implementations

- None recorded in the record. captum links the source; that is a reference,
  not an implementation of the tests.
