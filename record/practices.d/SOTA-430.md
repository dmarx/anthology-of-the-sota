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
  LIT-725 comes closest and still misses, in a way worth naming: it builds
  the planted feature — a caption in one half of the image, with one model
  verified to use it and one verified not to — and it runs the randomization
  test, and the two are different experiments. The planted feature validates
  infidelity against human judgement; the randomization test runs on ImageNet
  with no ground truth. The experiment asked for here is a table-join away
  inside a published paper.
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
version: 7
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
- version: 3
  date: '2026-09-26'
  note: >-
    Step 3's metric split gets a third independent source and the promote_when
    gets sharper. LIT-725 reproduces the split on ResNet-50 — signed rank
    correlation 0.10–0.18 against absolute-value 0.57–0.62, same explanations,
    same randomization — so three groups on three model families now agree that
    the metric choice flips the verdict. The same paper builds the
    planted-feature setting this promote_when asks for and points it at
    infidelity rather than at the randomization tests, so the bar is not met
    and the reason it is not met is now specific. Its infidelity figures also
    have a definition behind them at last. Recommendation, status and consensus
    unchanged.
- version: 4
  date: '2026-09-26'
  note: >-
    The two methods in the failing row get their defining papers. Guided
    backprop is LIT-727 §4.2 and the deconvnet it varies is
    LIT-728, so the verdict table's headline failure can now be followed
    to a masking rule instead of stopping at a name. Nothing about the verdict
    or the recommendation changes. Third amendment today, and each was driven
    by a source arriving rather than by a rereading: v2 the critique, v3 the
    metric definitions, v4 the two referents. The churn is a fact about how
    fast this cluster filled, not about the practice being unstable.
- version: 5
  date: '2026-09-26'
  note: >-
    Corrects a false sentence v4 added hours earlier, and files the account for a
    family this table does not cover. v4 said 1912.09818 "is the paper that
    argues" why guided backprop fails; it is not — it measures guided backprop
    and hands the explanation to Nie, Zhang and Patel (2018), 1805.07039, because
    a ReLU on the gradient makes the backward pass non-linear. What 1912.09818
    does supply is THEORY-114, the rank-1 convergence account for the z+
    family. So the cluster's failures now partition into three mechanisms, two
    held and one not, and this table's headline failure is the unheld one.
    Recommendation, status and consensus unchanged.
- version: 6
  date: '2026-09-26'
  note: >-
    The third row is held, so the partition is complete. LIT-730 proves that
    guided backpropagation recovers the input in a RANDOM three-layer CNN,
    regardless of the class, and that the saliency map and DeconvNet in the same
    network are noise — so the headline failure in the table below is a method
    that was never about the weights. THEORY-115 is the account. It also
    supplies the mechanism behind this practice's own do-not-validate-by-eye
    argument: the untrained edge detector matches these maps because partial
    image recovery is what an edge detector approximates. Recommendation, status
    and consensus unchanged.
- version: 7
  date: '2026-09-26'
  note: >-
    Fixes the summary, which the six amendments above never read. "The evidence
    is image classifiers only" was true at v1 and false from v2, when LIT-724
    supplied a BERT text classifier and a Condition saying the verdict does not
    transfer; and the summary still credited one source where `source:` now
    names two. The index renders this field, so it is the most-read line in the
    document and the only one an amendment never touches.

    Also strengthens the negative half, which now has three groups and a
    mechanism behind it rather than one paper's phrasing. And a correction of my
    own reporting rather than of the practice: three earlier units described this
    example as "leaning on a figure both Adebayo and Sixt amended". Re-reading
    shows the practice was correctly scoped throughout — summary, verdict table
    and negative half all state the narrowed "above the lowest layers" claim, not
    the "entirely invariant" form LIT-713's footnote 5 withdrew. The defect was
    smaller than three reports of it said. Recommendation, status and consensus
    unchanged.
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
  Adebayo et al. (2018), [LIT-713](../literature.d/LIT-713.md), read as [NOTE-365](../notes.d/NOTE-365.md), with
  Kokhlikyan et al. (2021), [LIT-724](../literature.d/LIT-724.md). An attribution map that survives
  re-initializing the model's weights, or retraining on permuted labels, cannot
  be telling you about the weights or the labels. Guided Backprop and Guided
  GradCAM survive the first above the lowest layers, and their maps look as
  convincing as ever. A rejection rule, not a certificate: passing does not show
  a method is faithful. **The verdict is per-modality** — the same test on a BERT
  text classifier reverses it for global Integrated Gradients — and pass or fail
  is read from curves with no threshold anywhere.
explained_by:
- THEORY-113
- THEORY-114
- THEORY-115
extended_by:
- SOTA-435
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

   **Three groups have now found this, on three model families.** `LIT-713`
   on Inception and MNIST; [LIT-724](../literature.d/LIT-724.md) on Inception and BERT, where SSIM
   calls global Integrated Gradients insensitive to randomization and Spearman
   calls it sensitive; and [LIT-725](../literature.d/LIT-725.md) on ResNet-50, where signed rank
   correlation runs 0.10–0.18 across five explanations and the absolute-value
   correlation on the same explanations runs 0.57–0.62. This step is the
   best-supported thing in the practice.
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
maps "strikingly similar" to several methods' — and [THEORY-115](../theory.d/THEORY-115.md) now says why,
because partial image recovery is what an edge detector approximates.

Guided Backprop's maps survive randomizing the weights above the lowest layers,
and **that verdict has three groups behind it and does not rest on anyone's
figures**: [LIT-713](../literature.d/LIT-713.md) on Inception and MNIST, [LIT-724](../literature.d/LIT-724.md) on Inception and
BERT, [LIT-729](../literature.d/LIT-729.md) on VGG-16 and ResNet-50, each by a similarity curve rather
than by eye. Worth knowing while reading the first of them: its published
Figure 2 for Guided Backprop is wrong, `LIT-729`'s authors confirmed the
implementation bug, and `LIT-713`'s own footnote 5 withdrew the stronger
"entirely invariant" claim. **The narrowed claim above is the one all three
support**, and it is the one this practice has always stated.

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

**The failing row's methods are now held, and its rule is one sentence.**
Guided backpropagation ([LIT-727](../literature.d/LIT-727.md), §4.2) zeroes the gradient at each
ReLU wherever *either* the top gradient or the bottom activation is negative —
both masks at once, where plain backprop applies the second and the deconvnet
([LIT-728](../literature.d/LIT-728.md)) applies the first. Its authors' stated reason is to
"prevent backward flow of negative gradients".

That is the rule, not the explanation, and the explanation is still not held.
The cluster's failures partition into three mechanisms:

| family | mechanism | held as |
| --- | --- | --- |
| Integrated Gradients, gradient⊙input, DeepLIFT | the model-independent input multiplier | [THEORY-113](../theory.d/THEORY-113.md) |
| DTD, LRP-α1β0, Excitation BP, PatternAttribution | rank-1 convergence of a non-negative chain | [THEORY-114](../theory.d/THEORY-114.md) |
| **Guided Backprop, Deconv, Guided GradCAM** | **partial image recovery** — the map is an approximate reconstruction of the input, unrelated to the decision | [THEORY-115](../theory.d/THEORY-115.md) |

The middle row covers no method in this table. **The bottom row is this table's
headline failure and is now explained**: [LIT-730](../literature.d/LIT-730.md) proves
`s_k^GBP(x) ≈ x` in a *random* three-layer CNN, regardless of the class, so the
map's invariance to the weights is not a defect in an attribution — it is what an
approximate image reconstruction looks like. That also explains the edge-detector
comparison in this practice's negative half. The
`1912.09818` reading is what settled which is which: it measures guided
backprop and explicitly hands the explanation to Nie et al., because applying a
ReLU to the gradient makes the backward pass non-linear so its own theorem does
not reach. **v4 of this practice said `1912.09818` was the paper that argues it.
That was wrong**, written from [LIT-725](../literature.d/LIT-725.md)'s citation rather than from the
paper.

It also rules out the intuitive story by name: "Other than argued in (Gu et al.
2018), the class insensitivity is not caused by missing ReLU masks and Pooling
switches."

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
  quadrature error — and infidelity is a squared error between `Iᵀ Φ` and the
  function difference ([LIT-725](../literature.d/LIT-725.md), Definition 2.1), so a degraded
  approximation raises it by construction. [SOTA-435](SOTA-435.md) is the hygiene that
  goes with reporting either measure.

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
