---
status: Read
paper: LIT-tmpbm5j4
title: 'Estimating Training Data Influence by Tracing Gradient Descent'
version: 1
date: '2026-09-17'
summary: >-
  Defines a training example's influence as the total change it caused in a
  test point's loss over the iterations where it was used, and approximates
  that by step-size-weighted gradient dot products at saved checkpoints. No
  Hessian, no convexity. Self-influence ranks mislabelled examples to the top.
---

# NOTE-tmppmv7l: Estimating Training Data Influence by Tracing Gradient Descent

<!-- inactive-ok-file: SOTA-tmp8ornu — Proposed, the practice this reading corroborates,
     filed in the same contribution. -->

## Contribution

Influence functions answer the attribution question from an **optimality
condition**: assume the parameters minimize the empirical risk, and ask what
the minimizer would have been without this point. The price is an inverse
Hessian, quadratic in the parameter count, which in practice forces everyone
to freeze all but the last layer.

TracIn answers it from the **trajectory** instead. The training run already
contains the answer: on every step where example `z` was used, the loss on the
test point moved by some amount, and the total of those movements over the run
*is* the influence of `z` on that prediction.

## Key insight

**The counterfactual you want was already executed.** Nobody needs to model
what would have happened without the example, because the optimizer visited
the example and its effect on the test loss at that moment is measurable.

The first-order approximation follows from step sizes being small: on
iteration `t` the loss on `z'` changes by about `η_t ∇L(w_t, z) · ∇L(w_t, z')`,
so summing over the iterations that used `z` approximates the idealized
quantity. The correction term is `O(η_t²)`.

That the formula is a step-weighted gradient dot product is what makes it
general: no second derivative appears, so no convexity is needed, and the
whole thing works for any architecture, domain or task trained with SGD or a
variant.

## Assumptions

- **Step sizes small enough** that the first-order approximation holds. The
  formula itself changes for AdaGrad, Adam or Newton, and the argument does
  not.
- **Checkpoints exist** at useful points in the run. This is the real
  precondition, and it is a precondition on how the training was operated
  rather than on the model.
- For the mislabel result: that mislabelled examples are outliers with respect
  to their own labels — a property of the corruption, not a theorem.

## Key results

- **TracInCP**: sampling checkpoints rather than every iteration is enough. On
  CIFAR-10 the experiments use every 30th checkpoint from the 30th, each at an
  epoch boundary, with the last layer only.
- **Self-influence surfaces mislabelled examples.** A mislabelled point is a
  strong proponent of *itself*: strong because it is an outlier, and a
  proponent because it reduces the loss with respect to its own wrong label.
  Sorting by decreasing self-influence puts the errors at the front.
- On CIFAR-10 with 10% of labels changed to the highest-scoring incorrect
  label — which cost test accuracy 93.4% → 87.0% at 99.6% train
  accuracy — **TracInCP recovered more of the mislabelled data than influence
  functions or representer-point selection** at the same inspection budget.
  The influence-function baseline was restricted to the last layer, because
  the full Hessian is not computable; the inverse was then formed exactly,
  which 50,000 examples permit.
- Ablations cover the choice of checkpoints, the first-order approximation
  itself, and the random-projection compression.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Idealized influence is the summed change in test loss over steps using the example | strong | it is a definition, and a defensible one |
| C2 | A step-weighted gradient dot product approximates it to `O(η²)` | strong | derived, given small steps |
| C3 | Checkpoints suffice in place of every iteration | moderate | ablated on CIFAR-10 and MNIST |
| C4 | Self-influence ranks mislabelled examples highly | moderate | CIFAR-10 and MNIST, one corruption model |
| C5 | TracInCP beats influence functions and representer points at recovering mislabels | moderate | one comparison, with the baselines last-layer-restricted |

## Method

Save checkpoints. For a query `z'`, compute `∇L(w_t, z')` at each checkpoint;
for each candidate `z`, accumulate `η_t ∇L(w_t, z) · ∇L(w_t, z')`. Optionally
restrict to a subset of layers and compress the gradients with random
projections. For self-influence set `z' = z`.

## Concepts

- **Attribution as trajectory accounting** — the reframing. Influence is a
  fact about a training run, not a property of a converged model.
- **Proponents and opponents** — replacing "helpful" and "harmful" because a
  negative contribution is not automatically a defect. Small, and it changes
  how the output reads.
- **Self-influence** — the diagonal of the influence matrix, and the cheapest
  useful thing in this literature.
- **Requirements as a design axis** — what a method *needs* (gradients,
  checkpoints, a loss) is as much its specification as what it computes.

## Connections

The straight comparison is with [LIT-tmpz6v6v](../literature.d/LIT-tmpz6v6v.md), whose method this is explicitly
positioned against, and with [LIT-tmpmgsal](../literature.d/LIT-tmpmgsal.md), which does not concede the point:
it keeps the Hessian formulation and gets to 52B parameters with a parametric
approximation instead. The record should hold both, because they need
different things — a trajectory versus a final model — and which you have is
usually not a choice.

Worth noting against [LIT-tmpyirk2](../literature.d/LIT-tmpyirk2.md): because TracIn never claims to estimate the
leave-one-out counterfactual, the correction that reframes influence functions
does not land on it in the same way. What TracIn estimates is what it defines,
and the open question is whether that definition is the useful one.

## Recommendations

- **R1** — Find mislabelled training data by self-influence. *Topic:* data
  pipeline. *Strength:* moderate.
- **R2** — Prefer an attribution method whose requirements you can meet:
  checkpoints and gradients if you have the run, a Hessian approximation if
  you have only the model. *Strength:* moderate.
- **R3** — Save checkpoints during training even when you have no immediate
  use for them, because attribution needs them afterwards and cannot
  reconstruct them. *Strength:* weak here — the paper assumes checkpoints
  rather than arguing for keeping them.

## Bearing on the record

Corroborates [SOTA-tmp8ornu](../practices.d/SOTA-tmp8ornu.md), whose primary source is [LIT-tmpz6v6v](../literature.d/LIT-tmpz6v6v.md). R1 is the
same recommendation from a different method, with a mechanism that says *why*
self-influence should work at all — which is the part the earlier paper's
version lacked.

R2 is not filed. It is a true and useful statement and it is a description of
a choice rather than an instruction to make one; a practice reading "use the
method you can afford" would carry nothing a reader does not already have.

R3 is not filed either, and it is the closer call. If it were supported it
would be a genuine operational instruction with a cost attached. It is not
supported here — the paper assumes checkpoints exist rather than arguing for
retaining them, and its own evidence is CIFAR-scale. The condition that would
file it: a report of attribution being run on a production model where the
retained checkpoints were what made it possible, or the reverse.

## Limitations

- CIFAR-10, MNIST, and small application studies. Nothing at language-model
  scale.
- The mislabel evaluation uses a synthetic corruption — labels flipped to the
  highest-scoring incorrect class — which is a *particular* kind of error and
  a fairly adversarial one.
- The influence-function baseline is handicapped by being last-layer only,
  which is an honest reflection of what was affordable in 2020 and is no
  longer the state of the art ([LIT-tmpmgsal](../literature.d/LIT-tmpmgsal.md)).
- Storage and compute scale with the number of checkpoints retained, and the
  paper does not characterise how few is too few beyond its ablation.

## Open questions

- Does self-influence still separate errors when the corruption is natural
  noise rather than a confident wrong label?
- At language-model scale, is the checkpoint requirement or the Hessian
  approximation the cheaper constraint in practice? Both papers are optimistic
  about their own side and neither runs the comparison.
