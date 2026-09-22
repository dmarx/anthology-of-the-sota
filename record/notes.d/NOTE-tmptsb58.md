---
status: Read
paper: LIT-tmpf6jxc
title: 'The setup that made the mechanism question answerable'
version: 1
date: '2026-09-22'
summary: >-
  Read because every later claim about what in-context learning *is*
  measures in this setup. A 9.5M-parameter GPT-2 trained from scratch on
  `(x, f(x))` sequences matches ordinary least squares on unseen linear
  functions and Lasso on sparse ones, in a single forward pass. The training
  objective is the setup's power and, later, the ground of the main objection
  to everything built on it.
---

# NOTE-tmptsb58: The setup that made the mechanism question answerable

## Contribution

It converts an observation about GPT-3 into an experiment. Instead of asking
why a text model can do arithmetic from three examples, train a model on
nothing but sequences of `(x, f(x))` pairs drawn from a known function class,
and ask whether it learns unseen members of that class from its context. The
answer is yes, at the accuracy of the class's optimal estimator, and the
setup is what the mechanism papers then argue inside.

## Key insight

**If you want to know what algorithm a forward pass is running, pick a task
where the optimal algorithm is known.** Linear regression has a closed-form
optimum, a well-understood iterative solver, and a sharp underdetermined
regime. Everything the record now holds about mesa-optimization exists
because this paper chose a problem whose answer key was already written.

## Assumptions

- **Trained from scratch on the ICL objective.** No text, no pretrained
  initialization: the model sees only prompts from the target function class.
  This is the condition [ARXIV-2310.08540](https://arxiv.org/abs/2310.08540) later argues makes the setup
  non-representative of pretrained language models, and it is stated plainly
  here.
- Inputs `x_i ~ N(0, I_d)`, `d = 20`; weight vectors from the corresponding
  natural distribution per class.
- Decoder-only GPT-2 family: 12 layers, 8 heads, 256-dimensional embeddings,
  9.5M parameters; batch 64, 500k steps, squared error.
- Curriculum learning over function complexity — reported as necessary for
  tractable training cost, not for the result.

## Key results

- **Linear functions.** The trained model's error curve as a function of the
  number of in-context examples tracks the least-squares estimator, which is
  optimal here.
- **Robust to two distribution shifts.** Between the training prompt
  distribution and the inference one, and between the in-context examples and
  the query input.
- **Sparse linear functions** (`d = 20`, `s = 3`): squared error **0.58** at
  `k = 5` and **0.09** at `k = 10`, against Lasso's **0.62** and **0.08**.
  Lasso has no closed form and solves an ℓ₁-regularized objective iteratively;
  the transformer matches it in one forward pass.
- **Two-layer ReLU networks** (100 hidden units) and **depth-4 decision
  trees**: performance matching or exceeding the algorithm built for each.

## Limitations

**The trained model is trained for the task it is tested on.** That is what
makes the experiment clean and it is also the whole of the later objection.
The paper is explicit about it; the literature that grew on top was less so.

**`d = 20` and one architecture.** No scaling study across model size in the
sense a language-model paper would mean.

**It establishes capability, not mechanism.** "Matches least squares" is
consistent with running least squares, with running enough gradient steps to
get there, and with running a second-order method. Distinguishing those is
what [ARXIV-2212.07677](https://arxiv.org/abs/2212.07677), [ARXIV-2211.15661](https://arxiv.org/abs/2211.15661) and [ARXIV-2310.17086](https://arxiv.org/abs/2310.17086) are for, and
[DP-005](../../docs/design-principles.md#dp-5) applies to reading this one as if it had already done it.

## Bearing on the record

The record held [SOTA-037](../practices.d/SOTA-037.md) (in-context learning emerges at scale) and [SOTA-038](../practices.d/SOTA-038.md)
(it permits few-shot adaptation) from Brown et al., and [THEORY-038](../theory.d/THEORY-038.md) on what a
decoder cannot compose in few layers. It held nothing about *what the forward
pass does* when it does in-context learning. This is the substrate under that
question.

## Open questions

- **Does the function-class result survive a model pretrained on text?** The
  natural experiment — present linear-regression prompts to a language model
  never trained on them and measure against least squares — is adjacent to
  [ARXIV-2310.08540](https://arxiv.org/abs/2310.08540)'s setting but is not the experiment it ran.
