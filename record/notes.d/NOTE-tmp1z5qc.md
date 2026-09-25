---
status: Read
paper: LIT-tmpx7oed
title: 'Integrated Gradients'
version: 1
date: '2026-09-25'
summary: >-
  Integrating the gradient along the straight line from a baseline gives the
  unique path attribution that is implementation-invariant, complete and
  symmetry-preserving. The justification is axioms, not a measurement: the
  paper argues that empirical evaluation of attributions is confounded, and
  its one comparison with another method is by eye.
---

# NOTE-tmp1z5qc: Integrated Gradients

## Contribution

Before this, gradient-based and backpropagation-based attribution methods were
compared by how their maps looked. This paper sets out properties an attribution
method should have, shows with counterexamples which existing methods break
them, and derives a method that satisfies them all: the path integral of
gradients along the straight line from a baseline. It also imports the
cost-sharing literature's uniqueness results. After it, "which attribution
method" can be argued from properties rather than from pictures, and completeness
gives a numerical check on the computation.

## Key insight

A gradient is a local derivative, so it reports zero wherever the function is
flat at the input, even if the input's value mattered a great deal relative to
where it started. Attribution is a question about a *difference*,
`F(x) − F(x′)`, and the gradient answers a question about a *point*. Integrating
the gradient along a path from `x′` to `x` answers the right question and keeps
the gradient's independence from how the network is wired. The straight line is
the only path that treats symmetric inputs symmetrically.

## Assumptions

- `F` is continuous everywhere and its partial derivatives are
  Lebesgue-integrable (discontinuities of measure zero). The paper notes that
  sigmoid, ReLU and pooling networks satisfy this.
- A baseline `x′` exists at which the prediction is near zero, so that
  attributions can be read as distributing `F(x)`. Black images for vision and
  the zero embedding for text are the paper's choices. The zero embedding is not
  a valid input, and the paper says so.
- For Proposition 2, the axioms are Friedman's (2004) as stated there, with the
  benchmark fixed. The mapping to deep networks is argued in Remark 4, not
  re-proved.

## Key results

- **Proposition 1 (Completeness).** For `F` differentiable almost everywhere,
  `Σᵢ IG_i(x) = F(x) − F(x′)`. It implies Sensitivity(a) (Remark 2).
- **Remark 3.** Every path method is implementation-invariant, complete and
  sensitive.
- **Proposition 2 (Friedman 2004, Theorem 1).** Path methods are the only
  attribution methods that always satisfy Implementation Invariance,
  Sensitivity(b) (Dummy), Linearity and Completeness.
- **Theorem 1.** IG is the unique symmetry-preserving path method (Appendix A).
  If averages over paths are allowed, Shapley–Shubik also qualifies (Remark 5).
- **Counterexamples (Appendix B, Figure 7).** For two functionally equivalent
  networks at `(3, 1)`, IG gives `(1.5, −0.5)` for both, while DeepLift and LRP
  give `(1.5, −0.5)` and `(2, −1)`. DeconvNet and Guided Backprop give `x₂` zero
  attribution for all inputs, despite the output depending on it.
- **Approximation.** 20–300 Riemann steps are "enough to approximate the
  integral (within 5%)". This is stated without data. The NMT model used
  100–1000.
- **Applications (§6).** These are demonstrations, each on one or a few
  examples:
  - GoogLeNet on ImageNet (Figure 2).
  - A diabetic-retinopathy model, where attributions land on lesion boundaries
    in one image.
  - Question classification, where attributions surface "total number" as a
    numeric trigger and "charles" as a spurious yes/no one.
  - An NMT alignment.
  - A molecular graph convolution: bonded pairs contribute 46% of the score,
    and the method found a W1N2 architecture defect (atoms not fully convolved).

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | IG attributions sum to `F(x) − F(x′)` | strong | Proposition 1, fundamental theorem of calculus for path integrals |
| C2 | Gradients, DeconvNets and Guided Backprop violate Sensitivity(a); DeepLift and LRP violate Implementation Invariance | strong | explicit counterexamples, §2 and Appendix B |
| C3 | Path methods are the only methods satisfying Implementation Invariance, Sensitivity(b), Linearity and Completeness | strong | Friedman (2004), cited; the correspondence to attribution is argued in Remark 4 |
| C4 | IG is the unique symmetry-preserving path method | strong | Theorem 1, proof in Appendix A |
| C5 | IG's maps reflect distinctive features of the input better than gradient×image | weak | visual comparison of a few images, Figure 2; no metric |
| C6 | The axiomatic approach rules out artefacts of the attribution method | weak | argument in §8; the axioms exclude two named failures, not method artefacts in general |
| C7 | 20–300 steps approximate the integral within 5% | weak | stated, no table |
| C8 | IG helps debug networks and extract rules | weak | one example each (§6.3, §6.5); anecdote, not a rate |

## Method

1. Choose a baseline `x′` with `F(x′) ≈ 0` that carries no signal.
2. For `k = 1…m`, compute `∇F(x′ + (k/m)(x − x′))`. The gradients batch.
3. Average them and multiply elementwise by `(x − x′)`.
4. Check that `Σ IG_i ≈ F(x) − F(x′)`. If not, increase `m`.

## Concepts

- **Attribution** — a vector `A_F(x, x′) ∈ ℝⁿ` relative to a baseline. The
  baseline is part of the definition (Definition 1, Remark 1).
- **Sensitivity(a)** — if input and baseline differ in one feature and in
  output, that feature gets non-zero attribution.
- **Sensitivity(b)** (Friedman's *Dummy*) — a variable the function does not
  depend on gets zero attribution.
- **Implementation Invariance** — functionally equivalent networks get
  identical attributions.
- **Completeness** — attributions sum to the output difference. The paper calls
  it "a sanity check that the attribution method is somewhat comprehensive".
  That is a different use of "sanity check" from LIT-tmpzf4pd's.
- **Path method** — attribution by integrating gradients along a monotone path
  from `x′` to `x`.

## Connections

It builds on gradient saliency (Baehrens et al.; Simonyan et al.) and on the
baseline idea of DeepLift and LRP, whose Implementation Invariance it shows
failing. Its theory is Aumann–Shapley cost sharing, via Friedman. It sets
itself apart from LIME (implementation-invariant but not sensitive) and from
attention weights, which are an incomplete account of influence in an LSTM.
LIT-tmpzf4pd later includes IG among the methods it randomizes.

## Recommendations

- **R1** — Use the completeness gap `|Σ IG_i − (F(x) − F(x′))|` as the
  convergence check on the step count, rather than a fixed `m`. *Topic:*
  analysis and evaluation. *Status:* standard. *Strength:* moderate. The
  identity is a theorem; the step counts are anecdote. *Applies when:* any
  Riemann-sum IG.
- **R2** — Report the baseline with every IG attribution, and choose one whose
  score is near zero. *Topic:* analysis and evaluation. *Status:* standard.
  *Strength:* moderate. It follows from the definition, but the paper does not
  measure baseline sensitivity. *Applies when:* always, since attributions are
  relative to it.
- **R3** — Do not take the axioms as evidence that a map is faithful to the
  model. They exclude implementation dependence and dead-gradient zeros, and
  nothing else. *Topic:* analysis and evaluation. *Strength:* moderate, from
  reading the axioms against LIT-tmpzf4pd.

## Bearing on the record

- No practice is sourced from this paper. R1 is sound and cheap, but it rests on
  a theorem plus one unmeasured sentence, and the record has no practice on
  computing attributions for it to belong to.
- SOTA-tmpudd8t (from LIT-tmpzf4pd) is the practice this paper's argument sits
  against. Here, empirical evaluation is set aside as confounded. There, a
  specific empirical evaluation, randomization, is proposed because visual
  evaluation misleads. The two are compatible. This paper's objection is to
  perturbation and bounding-box metrics that cannot separate model artefacts
  from method artefacts. The randomization tests are built to separate exactly
  those.
- The record's other attribution line is training-data attribution
  (LIT-400, LIT-401, LIT-402), which asks a different question. NOTE-178's R3
  and NOTE-179's R1, "validate an attribution method against the object it
  estimates", are the same instinct on that side.

## Limitations

- No quantitative evaluation of faithfulness. By the paper's own argument it
  could not have one it trusted.
- Baseline choice is left to the practitioner and not measured.
- Theorem 1's uniqueness depends on accepting symmetry preservation and
  restricting to single paths. The paper concedes that preferring IG over
  Shapley–Shubik on `min(x₁, x₂)` is "somewhat subjective".
- Interactions between features are explicitly not addressed (§8).

## Open questions

- Is IG faithful to the model in any measurable sense? LIT-tmpzf4pd's result
  suggests its magnitudes are dominated by the input.
- How much do attributions change across reasonable baselines (black, noise,
  blurred)?
