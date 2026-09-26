---
number: 365
status: Read
formerly:
- NOTE-tmp5d8h0
paper: LIT-713
title: 'Sanity Checks for Saliency Maps'
version: 2
history:
- version: 2
  date: '2026-09-26'
  note: >-
    One of this reading's open questions is answered by a paper the reading
    itself named as unheld. LIT-tmp5z3a0 runs the parameter-randomization test
    on a BERT text classifier and the verdict on global Integrated Gradients
    reverses. The two bare-id mentions of that paper now name a document, and
    the answered question is struck through rather than deleted, because what
    the reading did not know is part of what it recorded.
date: '2026-09-25'
summary: >-
  Randomize the model's weights, or train it on permuted labels, and see
  whether the saliency map changes. Gradients and GradCAM change. Guided
  Backprop is invariant to the higher layers. Integrated Gradients keeps the
  input's structure while its sign decorrelates. Visual inspection cannot tell
  these cases apart, and that is the paper's point.
---

<!-- inactive-ok-file: SOTA-430 — Proposed; the practice filed from this reading's R1 -->
<!-- inactive-ok-file: THEORY-tmp4cch6 — Proposed, and filed from the critique this document pointed at; named to say where the mechanism behind its own headline failure is now written down. -->

# NOTE-365: Sanity Checks for Saliency Maps

## Contribution

Before this, saliency methods were chosen mostly by how plausible their maps
looked, and assessed with perturbation or localization metrics. This paper
adds a necessary condition that any explanation method can be tested against:
if the explanation is meant to be about the model or the data, destroying the
model or the data must change it. Several popular methods fail that condition
in part, and a map that looks right is no evidence of passing it.

## Key insight

Every explanation method has invariances, transformations of model and data
that leave its output unchanged. If one of them is incompatible with the task,
the method is ruled out for that task, however good its maps look. Guided
Backprop's maps look like the object because they are close to an edge map of
the input. An untrained edge detector produces something similar, and a human
reads either as an explanation.

## Assumptions

- The task the explanation serves depends on the learned parameters (model
  debugging) or on the input–label relationship (explaining what was learned,
  finding outliers). The paper says a method insensitive to both may still say
  something about the architecture as a prior (§5.1).
- A randomized model, re-initialized from a truncated normal (std 0.01 for the
  CNN) or a uniform, is far enough from the trained one that a
  parameter-dependent explanation must change. Truncated normal and uniform
  gave "identical results".
- The similarity metrics measure what matters. They are Spearman with and
  without absolute values, SSIM and HOG correlation. The paper concedes that
  "quantifying human visual perception is still an active area of research".
- Settings: Inception v3 on ImageNet (93.9 top-5), a 2-conv CNN (99.2% on MNIST)
  and a 4-layer MLP (98.7%) on MNIST and Fashion-MNIST. There is also a figure on
  an Inception v4 bone-age model and AlexNet with a perturbation method
  (Figure 36). All are image classifiers.

## Key results

- **Cascading randomization (Figures 2, 4, 5).**
  - Gradient and SmoothGrad maps change as soon as the top layers go.
  - GradCAM changes once the randomization reaches the last convolutional layer.
  - Guided Backprop and Guided GradCAM stay "visually and quantitatively
    similar" until the lower layers are randomized.
  - IG and gradient⊙input keep high SSIM and absolute-value rank correlation.
    Their no-absolute-value rank correlation drops to about zero at the first
    randomized block.
- **Independent randomization (Figure 3).** The same pattern appears: Guided
  Backprop is sensitive only to the lower layers, and even then stays
  "dominated by the input structure".
- **Data randomization (Figure 6).** Models are trained to above 95% training
  accuracy on permuted labels.
  - Gradient and SmoothGrad change substantially.
  - GradCAM fragments into disconnected patches.
  - Guided Backprop changes visibly but still covers the digit.
  - IG and gradient⊙input change sign, with the input's structure "clearly
    prevalent".
- **Input × random vectors (Figure 19).** `x⊙u` and `x⊙v` for independent
  random `u` and `v` stay similar on every metric. The input dominates the
  product.
- **1-layer conv + ReLU + sum-pool (§5.3).**
  `∂l/∂x_ij = Σ_{k,l∈{−1,0,1}} a_{i+k,j+l} w_{kl}`. The local activation pattern
  alone sets the gradient, so edges show.
- **Calibration (Appendix B).** Over 50 ImageNet images, a map against a random
  mask scores about 0 (|·| < 0.005) on all four metrics.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Guided Backprop and Guided GradCAM are invariant to the weights of the higher layers | strong | cascading and independent randomization on three architectures and four datasets, four metrics; corrected in v3 from "entirely invariant" |
| C2 | Gradients and GradCAM are sensitive to model parameters and training labels | strong | same experiments |
| C3 | Visual inspection of saliency maps can make a model-insensitive method look valid | strong | the IG/gradient⊙input SSIM-versus-signed-rank split; the edge-detector comparison |
| C4 | Methods that approximate input⊙gradient mostly return the input when gradients are noisy | moderate | Figure 19 random-vector experiment; an argument by construction, not a measurement on trained models |
| C5 | Convolutional structure makes some saliency methods act as edge detectors | moderate | closed-form gradient for one conv layer (§5.3); for deep networks only "perhaps a similar principle applies" |
| C6 | Some saliency methods are independent of both model and data | weak as worded (abstract) | the body shows dependence on lower layers and a visible change on random labels |
| C7 | The tests apply to any explanation method | moderate | true of the tests' definition; the evidence is image classifiers only |
| C8 | On a linear model IG is `(x − x̄)⊙w/2` | wrong by a factor of 2 | §5.3 integrates `wα` where the gradient is `w`; the qualitative point (IG ≈ gradient⊙input) holds |

## Method

- **Model parameter randomization.** Re-initialize the weights top-down
  (cascading) or one layer at a time (independent). Recompute the maps and
  compare them with the trained model's maps on four similarity metrics.
- **Data randomization.** Permute the training labels, retrain to high
  training accuracy, and compare the maps on the same test inputs.

## Concepts

- **Sanity check** — a necessary condition an explanation method must meet
  before being used for a task that depends on what the check destroys. It is
  not a sufficient test of faithfulness.
- **Invariance of an explanation method** — a transformation of model or data
  under which its output does not change.
- **ABS / diverging visualization** — the absolute value of a normalized map,
  versus the signed map. The two give opposite verdicts on IG, which is why
  both are reported.

## Connections

The data-randomization test borrows Zhang et al.'s random-label training,
which is not held. Nie et al. had shown theoretically that Guided Backprop and
DeconvNet do partial input recovery; this paper adds a test that anyone can run.
It cites Ancona et al. for the equivalence of ε-LRP and DeepLift(Rescale) to
input⊙gradient in bias-free ReLU networks, which is why it treats them as one
family. IG ([LIT-712](../literature.d/LIT-712.md)) is one of the eight methods tested, and no lineage
relation is declared (see [LIT-713](../literature.d/LIT-713.md)).

## Recommendations

- **R1** — Before using an attribution method for model debugging or to explain
  what a model learned, run both randomization tests on your model and reject
  the method for that purpose if its maps survive. *Topic:* analysis and
  evaluation. *Status:* experimental. *Strength:* moderate. It is strong as a
  rejection rule and says nothing about sufficiency. *Applies when:* the task
  depends on parameters or labels. Filed as [SOTA-430](../practices.d/SOTA-430.md).
- **R2** — Report signed rank correlation alongside any absolute-value or
  perceptual similarity when comparing maps. The absolute-value measures hide
  the sign change that distinguishes IG on a trained model from IG on a random
  one. *Strength:* moderate.
- **R3** — Do not judge a saliency method by how its maps look. Compare it with
  an edge detector on the same input. *Strength:* strong for the negative claim.

## Bearing on the record

- **[SOTA-430](../practices.d/SOTA-430.md) is filed from R1**, `Proposed`. The paper states the instruction
  outright ("sanity checks to perform before deploying a method in practice") and
  backs it with a broad sweep. It is one group, all image classifiers, and pass
  and fail are read from curves without thresholds. The practice says all three.
- **Integrated Gradients ([LIT-712](../literature.d/LIT-712.md)).** This reading should stop the record
  citing either "IG passes" or "IG fails" the sanity checks. The paper puts IG
  in neither list, and the metrics disagree about it.
- The four methods the paper gives verdicts on (gradient, GradCAM, Guided
  Backprop, Guided GradCAM) are not held as notes. The follow-up captum links
  now is: [LIT-tmp5z3a0](../literature.d/LIT-tmp5z3a0.md).

## Limitations

- Image classifiers only. No language model, no text attribution.
- No thresholds or significance tests. Pass and fail are read from figures.
- The number of inputs behind the main curves is not stated. The calibration
  used 50.
- The tests are necessary conditions. A method that passes, like the plain
  gradient, is not thereby shown to be faithful.
- Randomizing the weights also changes the scale of activations and gradients,
  and the paper does not separate that from "the learned parameters".

## Open questions

- ~~Do the verdicts hold for transformers and for token attributions?~~
  **Answered, and the answer is no.** [LIT-tmp5z3a0](../literature.d/LIT-tmp5z3a0.md) runs the
  parameter-randomization test on a BERT classifier on SST-2: global
  Integrated Gradients, which fails here, becomes parameter-sensitive there,
  because token scores are summed over embedding dimensions and the input
  multiplier's structure does not survive the sum.
- Can a threshold be set so that "passes" is a statistic rather than a
  judgement, and does IG pass it?
- The later literature questions whether the randomization test measures what
  it claims. One of it is now held — [LIT-tmp5z3a0](../literature.d/LIT-tmp5z3a0.md), which traces this paper's
  own headline failure to the input multiplier ([THEORY-tmp4cch6](../theory.d/THEORY-tmp4cch6.md)) and finds a
  smoothness confound in the test. The rest is not.
