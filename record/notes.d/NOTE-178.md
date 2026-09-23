---
number: 178
status: Read
formerly:
- NOTE-tmpei9gn
paper: LIT-401
title: 'Studying Large Language Model Generalization with Influence Functions'
version: 1
date: '2026-09-17'
summary: >-
  Scales influence functions to 52B-parameter language models with an EK-FAC
  approximation to the IHVP and query batching over the gradient bottleneck,
  then uses them as an instrument. Generalization gets more abstract with
  scale; influence is heavy-tailed but not concentrated; and a training
  sequence only counts when the prompt-related phrase comes first.
---

# NOTE-178: Studying Large Language Model Generalization with Influence Functions

<!-- inactive-ok-file: SOTA-245 — the practice this reading files, Proposed on its
     evidence. -->

## Contribution

Training-data attribution existed and did not reach language models. Both of
its costs scale badly: the inverse-Hessian-vector product, and the gradient of
every candidate training sequence you want to score. This paper attacks both
and gets to 52 billion parameters, then spends most of its length using the
result as a scientific instrument rather than presenting it as a method.

## Key insight

**The question "why did the model say that?" can be answered in the currency
of training data, at scale**, and what comes back is not what the mechanistic
reading would predict. Behaviours that look sophisticated are influenced by
sequences that *describe or exemplify the same behaviour* — role-play looks
like imitation — while the influence for any one behaviour is spread across
many sequences rather than traceable to a few, so "the model memorised this"
is usually the wrong description.

The methodological insight is narrower and reusable: **a parametric
approximation to the curvature beats an iterative solver when you need to
reuse it.** EK-FAC is fit once and inverted cheaply, so its cost amortises
across queries in a way LiSSA's per-query iteration cannot.

## Assumptions

- Influence is computed over **MLP parameters only**, treating attention,
  embeddings and layer norm as fixed. Justified by the MLP parameters being
  the majority and by prior localization of factual knowledge to them, and the
  paper says plainly that this probably misses patterns.
- **Pretrained models only.** Nothing here covers preference fine-tuning,
  which the paper names as the important gap.
- The Fisher information matrix is taken as the Gauss-Newton Hessian, valid
  for softmax outputs under autoregressive cross-entropy.
- **Only a fraction of the pretraining corpus is searched**, so "the most
  influential sequence" means the most influential one looked at.
- The estimate targets the PBRF, not leave-one-out retraining — the paper's
  own first limitation, from [LIT-402](../literature.d/LIT-402.md).

## Key results

- **EK-FAC is competitive with LiSSA on estimate accuracy while being
  significantly faster**, validated against the PBRF rather than against
  retraining.
- **Influence is heavy-tailed, with the tail roughly a power law, and is
  nevertheless spread over many sequences.** Typical behaviours are not direct
  memorization of a handful of examples.
- **Abstraction rises with scale.** For a dialogue in which an assistant
  resists shutdown, all top-20 influential sequences at 810M share short token
  sequences with the query and are barely related semantically. At 52B the top
  sequences share little token overlap: an AI named Hal pleading not to be
  left alone, a person surviving in a desert, the daily course of a chronic
  illness. The same pattern holds for programming, mathematical reasoning and
  cross-lingual generalization.
- **Layers differ in kind, not in weight.** Influence is roughly even across
  layers on average, but upper and lower layers stay closer to the tokens and
  middle layers carry the abstract patterns.
- **Word ordering, and this is the concrete finding.** Synthetic training
  sequences were constructed for two queries about fictional entities — the
  first President of the Republic of Astrobia, and the composition of a
  substance called Gleem — and for an English→Mandarin translation query. A
  sequence has high influence **only when the phrase related to the prompt
  precedes the phrase related to the completion.** Reversing the order with
  identical content collapses the score: Mandarin-then-English scores **0.030**
  against a Mandarin-only baseline of **0.020**, where the English-then-Mandarin
  ordering scores far higher. Consistent across model sizes.
- **Role-playing is influenced primarily by examples and descriptions of
  similar behaviour**, which the paper reads as imitation rather than planning.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | EK-FAC gives IHVP estimates competitive with LiSSA, much faster | strong | validated against the PBRF |
| C2 | Influence is heavy-tailed but not concentrated | strong | measured, with power-law goodness-of-fit in an appendix |
| C3 | Larger models generalize more abstractly | moderate | qualitative across several query families, one model series |
| C4 | Influence appears only when prompt-related phrases precede completion-related ones | strong | a controlled synthetic construction with content held fixed |
| C5 | Role-playing behaviour comes from imitation | weak-moderate | qualitative, and "imitation" is an interpretation of the sequences |
| C6 | Middle layers carry abstract patterns, outer layers token-level ones | moderate | layerwise attribution, one model series |

## Method

Fit EK-FAC to the Gauss-Newton Hessian over MLP parameters. For a query,
compute its gradient, apply the approximate inverse, and take dot products
with candidate training-sequence gradients. Cut the candidate-gradient cost
with TF-IDF filtering and with query batching, which shares that cost across
dozens of queries.

## Concepts

- **Attribution as an instrument** — the paper's real posture. The method is a
  means to measure generalization, which is why most of it is experiments
  rather than benchmarks.
- **Abstraction as a measurable property** — token overlap versus thematic
  relation, read off the influence ranking, as a proxy for how a model
  generalizes.
- **Order-dependence of what a sequence teaches** — C4, and the most
  transferable thing here.
- **Spread versus concentration of influence** — the distinction that turns
  "did it memorise this?" into a question with an empirical answer.

## Connections

[LIT-403](../literature.d/LIT-403.md) is the origin; this is that method with the two bottlenecks
solved. [LIT-400](../literature.d/LIT-400.md) is the alternative that avoids the Hessian entirely by
requiring checkpoints; this paper's success is the reason that trade is still
live rather than settled.

[LIT-402](../literature.d/LIT-402.md) is what licenses any of this being informative: the estimate is a
good approximation to the PBRF and a poor one to retraining, and this paper
validates against the PBRF accordingly. It is unusually clean practice — the
method is evaluated against the thing it actually estimates.

C4 sits beside the record's data material rather than its interpretability
material. If a sequence only teaches the direction it was written in, then the
**order of statements inside a document** is a corpus property with
consequences, which none of the twenty-eight `data-pipeline` practices
currently touches.

## Recommendations

- **R1** — If a relation needs to be usable in both directions, put it in the
  corpus in both orders. *Topic:* data pipeline. *Strength:* moderate — strong
  evidence about influence, no evidence about downstream accuracy.
- **R2** — Before calling a behaviour memorization, check whether the
  influence is concentrated or spread. *Strength:* moderate.
- **R3** — Validate an attribution method against the object it estimates,
  not against the object it was motivated by. *Strength:* strong, and general.

## Bearing on the record

Sources [SOTA-245](../practices.d/SOTA-245.md) (R1), `Proposed`. The gap between what C4 measures and
what the practice recommends is real and stated there: influence is not
accuracy, and nobody here trained a model on a reordered corpus and tested it.

R2 is not filed. It is an instruction about how to talk about a result rather
than about what to do, and acting on it requires the apparatus this whole
reading is about — which makes it a condition on attribution work rather than
a practice of its own.

R3 is general and good and belongs to the record's evaluation material rather
than its data material. It is one instance here, and the instance is the
paper's own conduct rather than a result it reports. Named rather than filed,
per [ADR-043](../decisions.d/ADR-043.md): the condition is a second case where validating against the
motivating object rather than the estimated one produced a wrong conclusion.

## Limitations

The paper lists five and leads with the sharpest, which is worth copying:

- Influence functions are a poor match for the counterfactual that motivated
  them and are better read as approximating the PBRF — which is *more local*
  around the trained parameters. The authors therefore expect them to miss
  genuinely nonlinear training phenomena such as circuit formation or
  representational reorganisation, and say explicitly that they do not
  address how well the PBRF captures what one ultimately wants to know.
- Pretrained models only; fine-tuning untouched.
- Up to 52B, which the paper says is far below the state of the art.
- MLP parameters only.
- Only a fraction of the corpus searched, so more influential sequences
  probably exist and were not seen.

## Open questions

- Does the order effect show up in behaviour, not just in influence? A model
  trained on a corpus with one ordering, evaluated in both directions, would
  settle it and nobody here ran it.
- Does any of this survive preference fine-tuning, where the behaviours people
  actually care about are installed?
- The authors flag that a PBRF-targeted estimate should miss circuit formation
  and grokking-like reorganisation. If so, attribution and mechanistic
  interpretability are answering questions that do not compose, and nothing
  currently says where the boundary is.
