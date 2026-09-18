---
number: 179
status: Read
formerly:
- NOTE-tmpiq1um
paper: LIT-402
title: 'If Influence Functions are the Answer, Then What is the Question?'
version: 1
date: '2026-09-17'
summary: >-
  Decomposes the influence-function / leave-one-out gap into five terms and
  finds that the three largest are not approximation errors but a change of
  question. Influence estimates on neural networks closely track the proximal
  Bregman response function, which supports the same use cases — so the method
  is not fragile, it was mislabelled.
---

# NOTE-179: If Influence Functions are the Answer, Then What is the Question?

<!-- inactive-ok-file: THEORY-017, SOTA-246 — the account this paper corrects
     (Rejected, and correctly so) and the practice that survives the correction. -->

## Contribution

It was already known that influence estimates align well with leave-one-out
retraining for linear models and badly for neural networks, and the field had
read that as a failure — influence functions were "fragile". This paper takes
the discrepancy apart term by term and reaches the opposite conclusion.

## Key insight

**A method that reliably fails to answer one question is answering a different
one, and the useful move is to find out which.**

The five-term decomposition separates the discrepancy into pieces that are
*errors* — the estimate is a bad version of the thing it wants — and pieces
that are *gaps* — the estimate is a good version of something else. The errors
turn out to be small. What remains, and dominates, is the distance between
leave-one-out retraining and a different object.

That object is the **proximal Bregman response function**: the effect of
removing a data point *while keeping the model's predictions close to those of
the trained model*. Once named, everything that looked like fragility becomes
a definition.

## Assumptions

- The Gauss-Newton Hessian is used where the loss is convex in the network
  outputs, which covers the standard cases.
- The analysis is of *practical* influence estimates — damped, on
  non-converged parameters — rather than of the idealised quantity, which is
  the point: it characterises what people actually compute.
- The decomposition bounds the parameter (or output) difference by summing the
  per-term differences, so it is an accounting of all approximations and
  assumption violations rather than a tight characterisation of any one.

## Key results

- **Five terms:** the warm-start gap (cold-start versus warm-start response
  functions), the proximity gap (an implicit proximity regularizer),
  the non-convergence gap, linearization error, and solver error.
- **Terms 1–3 dominate; terms 4–5 are at least an order of magnitude smaller**
  for most neural networks. Measured across binary classification, regression,
  image reconstruction, image classification **and language modelling**, and
  studied against network width and depth, weight decay, training time,
  damping, and the number of points removed.
- **Terms 1–3 are exactly the difference between leave-one-out retraining and
  the PBRF.** So the gap between the influence estimate and the PBRF comes only
  from terms 4 and 5 — the small ones. Influence estimates track the PBRF
  closely while failing to track retraining.
- **The uses survive.** The paper states that the PBRF supports the same
  purposes that motivated influence functions: finding influential or
  mislabelled examples, and carrying out data-poisoning attacks.
- **Therefore the PBRF is a better gold standard** for evaluating influence
  estimation than retraining, and influence functions on neural networks are
  not inherently fragile.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | The IF/LOO discrepancy decomposes into exactly those five terms | strong | derived; the decomposition is constructive |
| C2 | Linearization and solver error are an order of magnitude smaller than the rest | strong | measured across five task families |
| C3 | Influence estimates closely approximate the PBRF | strong | Figure 1 and the task sweep |
| C4 | The PBRF supports the mislabelled-example and poisoning use cases | moderate | argued from what the PBRF is; not a fresh benchmark of both |
| C5 | Influence functions are not inherently fragile | strong | follows from C2 and C3, against the prior reading |

## Method

Define the warm-start and cold-start response functions and the PBRF. Insert
each approximation one at a time, measure the parameter or output difference
each introduces, and sum. Then compare influence estimates against retraining
and against the PBRF on the same models.

## Concepts

- **Gap versus error** — the distinction the paper's terminology is built on,
  and the whole argument in one word choice. A gap means the target moved; an
  error means the aim was off.
- **The proximal Bregman response function** — removal, constrained to keep
  predictions near the trained model's.
- **Warm start versus cold start** — retraining from the trained parameters
  versus from scratch, which are not the same counterfactual and are routinely
  conflated.
- **Choosing a gold standard** — retraining is the intuitive one and is the
  wrong one, and a method evaluated against the wrong standard looks broken.

## Connections

This corrects [LIT-403](../literature.d/LIT-403.md)'s account of what an influence estimate measures,
and it is the reason [LIT-401](../literature.d/LIT-401.md) validates against the PBRF rather than
against retraining — a rare case of a correction being absorbed into practice
within a year.

It leaves [LIT-400](../literature.d/LIT-400.md) largely untouched, since TracIn never claimed to
estimate the leave-one-out counterfactual.

## Recommendations

- **R1** — Evaluate an attribution method against the object it estimates.
  *Strength:* strong. Stated here as a consequence rather than as advice.
- **R2** — Do not read an influence estimate as "what would happen if I
  removed this and retrained". *Strength:* strong.
- **R3** — Keep using influence functions for mislabelled-example detection
  and for poisoning analysis; the reinterpretation does not touch those.
  *Strength:* moderate.

## Bearing on the record

Sources [THEORY-018](../theory.d/THEORY-018.md), which corrects [THEORY-017](../theory.d/THEORY-017.md) — the account
[LIT-403](../literature.d/LIT-403.md) published with the method.

R3 is what keeps [SOTA-246](../practices.d/SOTA-246.md) standing. Without this paper the practice would
rest on an explanation the field had abandoned, which is the arrangement
CLAUDE.md warns about in as many words: a technique everybody uses can have
been published with an explanation that was later refuted. Here the refutation
is explicit about which uses it spares, so the practice's conditions can say
so rather than hedging.

R1 and R2 are the theory's content rather than separate practices, and filing
them as practices would duplicate the pair of THEORY documents across schemes.

## Limitations

- The decomposition is an accounting, so the terms are bounded rather than
  characterised exactly.
- C4 is argued from the nature of the PBRF rather than re-benchmarked on both
  use cases.
- The experiments are moderate-scale; nothing is at the size [LIT-401](../literature.d/LIT-401.md)
  works at, and it is that paper that extends the PBRF validation upward.
- The paper says what influence functions *do* estimate. Whether the PBRF is
  the quantity anyone wanted is a separate question it does not take up, and
  [LIT-401](../literature.d/LIT-401.md) explicitly declines to take it up either.

## Open questions

- Is the PBRF the right target? Both this paper and [LIT-401](../literature.d/LIT-401.md) leave it
  open, which means the whole attribution literature is now validated against
  an object nobody has argued is the one of interest.
- Does the warm-start gap have practical consequences for continual training,
  where warm starting is what actually happens?
