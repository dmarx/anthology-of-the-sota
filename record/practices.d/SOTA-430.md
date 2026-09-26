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
  which is adoption (DP-005); or more image-classifier sweeps of the same kind,
  which are the result already held. The critique this field named first is now
  held as LIT-724, and it does not meet this bar — it supplies the
  non-image model and shows the verdict is metric- and modality-dependent,
  without ever putting a known dependence in front of the tests.
consensus: contested
consensus_note: >-
  Two groups, and the fork is clean. Both run the tests and neither validates a
  map by eye, so the trunk — check before you trust — is agreed. What they
  differ on is what a failure means. LIT-713 reads it as evidence that
  gradient-based methods are "inadequate tools for model explanation";
  Kokhlikyan et al. (LIT-724, the captum maintainers) read the same
  failure as an artefact of the input multiplier, a model-independent factor
  you can switch off, and show that the verdict reverses on text and depends on
  whether you score with SSIM or Spearman. LIT-724 is both `source:` and
  `contested_by:` here, which is not a contradiction: it supplies step 4 and
  two of the conditions while disputing what its co-source concludes from a
  failure. Moved off `unassessed` because somebody has now looked, not because
  the field agreed. Read as of 2026-09.
title: 'Before using an attribution map to debug a model or explain what it learned, check that the map changes when the weights are randomized and when the labels are permuted — do not validate it by how it looks'
version: 2
history:
- version: 2
  date: '2026-09-26'
  note: >-
    Reads the critique this practice named twice as unread. LIT-724 adds a
    fourth step — when a method fails, re-run it without the input multiplier,
    because that is where the failure has been traced — and two conditions: the
    verdict does not transfer from image to text, and the paper independently
    reproduces the metric split step 3 already warned about, on a different
    model. Consensus moves from `unassessed` to `contested`, because somebody
    has now looked and the two groups differ on what a failure means. The
    recommendation and the status are unchanged.
tags:
- analysis-and-evaluation
date: '2026-09-25'
source:
- LIT-713
- LIT-724
contested_by:
- LIT-724
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
explained_by:
- THEORY-113
---

<!-- inactive-ok-file: THEORY-113 — Proposed, and it is the account filed alongside this amendment; step 4 points at it for the mechanism, and the practice says in the same breath that it does not rehabilitate the method. -->

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
4. **If a method fails, re-run it without the input multiplier before
   concluding anything about the method.** Integrated Gradients,
   InputXGradient, DeepLift and Gradient SHAP all multiply a model-dependent
   quantity by `(x − x₀)`, which does not depend on the model at all.
   [LIT-724](../literature.d/LIT-724.md) traced the failure to that factor: drop it and the
   maps become parameter-sensitive, with SSIM for the local variant about half
   the global variant's on Inception. Their recommendation is to "compare
   their explanations with and without this multiplier in order to understand
   the magnitude of these structural effects", and [THEORY-113](../theory.d/THEORY-113.md) is the
   account. This does **not** rehabilitate the method — a pass is still not a
   certificate — but it tells you whether you have learned something about
   the attribution or about the picture.

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
- **The verdict does not transfer across modality, which is now measured
  rather than suspected.** [LIT-724](../literature.d/LIT-724.md) runs the parameter-randomization
  test on a BERT classifier fine-tuned on SST-2 and finds that global
  Integrated Gradients — which fails on images — becomes parameter-sensitive
  there, because token scores are summed over embedding dimensions and the
  multiplier's structure does not survive the sum. So "run these tests" means
  run them **in your modality**: a verdict imported from an image classifier
  can be the wrong sign.

- **A failure can be a fact about the similarity metric.** Step 3 above says
  the metrics disagree, on this source's own data. A second group reproduces
  the split on a different model: SSIM reports global IG insensitive to
  cascading randomization while Spearman rank correlation reports both
  variants sensitive, in the same experiment. That is the strongest
  corroboration any part of this practice has, and it is corroboration of the
  caveat rather than of the headline.

- **Part of what the test moves is numerical, not explanatory.** Randomizing
  weights makes the network less smooth, which makes gradients noisier and an
  integral-based attribution's approximation worse. Infidelity on Inception
  goes from 2.84 at the trained model to 1.27 × 10⁷ partway down the
  randomization cascade. If you score a randomization test with a
  faithfulness metric rather than a similarity metric, some of the movement is
  quadrature error.

- **Whether the model-randomization test measures what it claims is disputed,
  and the practice stays `Proposed` for it.** The dispute is now held rather
  than gestured at: see the `consensus_note` and
  [LIT-724](../literature.d/LIT-724.md)'s standing section. What neither group has done —
  and what the `promote_when` asks for — is run the tests where the true
  dependence of output on input is known by construction.

## Where this does not apply

If you only want a map that reflects the architecture's prior, or an
image-processing view of the input, a method that fails these tests can still
serve. The paper says so (§5.1). But then it is not an explanation of what the
model learned, and it should not be presented as one.

## Known implementations

- None recorded in the record. captum links the source; that is a reference,
  not an implementation of the tests.
