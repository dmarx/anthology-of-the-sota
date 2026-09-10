---
number: 15
status: Read
formerly:
- NOTE-tmpg746b
paper: LIT-012
title: 'Decoupled Weight Decay Regularization'
version: 1
tags:
- training-optimization
date: '2026-09-09'
summary: >-
  L2 regularization and weight decay are equivalent for SGD and **not** for adaptive methods. Common Adam implementations do L2 while calling it weight decay; decoupling it recovers the real thing, separates the weight-decay and learning-rate choices, and closes Adam's generalization gap to SGD with momentum.
---

# NOTE-015: Decoupled Weight Decay Regularization

## Contribution

Establishes that a widely assumed equivalence is false where it matters. **L2
regularization** (add `λ‖w‖²` to the loss) and **weight decay** (multiply the
weights by `1−λ'` each step) coincide for plain SGD, up to a learning-rate
rescaling. For adaptive methods like Adam they do not, because the adaptive
denominator rescales the L2 gradient along with everything else — so the
regularization a parameter actually receives depends on its gradient history.
Common Adam implementations do L2 "often calling it *weight decay* in what may
be misleading due to the inequivalence we expose". Decoupling recovers the
original formulation.

## Key insight

An optimizer that rescales gradients per-parameter also rescales anything you
smuggled into the gradient. Regularization added to the loss becomes a
gradient term, so it inherits the adaptive scaling and stops being the
uniform pull toward zero it was meant to be — parameters with large
accumulated gradients get *less* decay, which is exactly backwards.

The consequence that made the paper stick is not the accuracy number but the
**hyperparameter geometry**: with L2 the best weight-decay setting moves when
you change the learning rate, so the two must be tuned jointly. Decoupled,
they separate, and a two-dimensional search becomes two one-dimensional ones.

## Assumptions

- Adaptive gradient methods are the regime where the inequivalence bites;
  for standard SGD the two are equivalent when rescaled by the learning rate,
  which the paper states up front.
- Empirical evidence is image classification, where SGD with momentum was the
  incumbent and Adam's generalization gap was the known problem.
- 2017–2019 architectures and scales.

## Key results

- **L2 and weight decay are equivalent for SGD** (rescaled by the learning
  rate) **and not for Adam.**
- Common implementations employ L2 while calling it weight decay.
- **AdamW** decouples the decay from the gradient step.
- **(i) The optimal weight decay decouples from the learning rate**, for both
  SGD and Adam — the hyperparameter-separation result.
- **(ii) Adam's generalization improves substantially**, enough to compete
  with SGD with momentum on image classification, where it previously lost.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | L2 and weight decay are equivalent for SGD, not for adaptive methods | strong | analytic, and the paper's premise |
| C2 | Standard Adam implementations conflate the two | strong | a statement about existing code, verifiable |
| C3 | Decoupling separates the optimal weight decay from the learning rate | strong | measured for both SGD and Adam |
| C4 | Decoupling substantially improves Adam's generalization | moderate | measured on image classification of the period |

## Method

**Algorithm:** AdamW.

Compute the Adam update from the loss gradient as usual, **without** any L2
term. Then apply the weight decay directly to the parameters — multiply by
`1 − ηλ` — outside the adaptive rescaling. The decay is applied to the
weights, not routed through the gradient.

## Concepts

- **Decoupled weight decay** — decay applied to the parameters rather than
  added to the loss, so the adaptive denominator never touches it.
- **The inequivalence** — the paper's own framing. Not that L2 is wrong, but
  that calling it weight decay under an adaptive optimizer is a naming error
  with consequences.

## Connections

A correction to Adam as universally implemented, and the reason "AdamW"
rather than "Adam" is the default everywhere in this record. The
hyperparameter-separation result (C3) is the ancestor of the transfer
arguments µP makes structurally.

## Recommendations

- **R1** — Use decoupled weight decay with any adaptive optimizer. *Topic:*
  optimization. *Status:* standard. *Strength:* strong. *Applies when:*
  always, under Adam or a relative.
- **R2** — Do not assume a regularizer added to the loss survives an adaptive
  optimizer intact. *Topic:* optimization. *Status:* standard. *Strength:*
  strong. *Applies when:* any per-parameter-scaled optimizer; the general form
  of C1.
- **R3** — Expect weight decay and learning rate to be tunable independently
  once decoupled. *Topic:* tuning. *Status:* standard. *Strength:* strong.
  *Applies when:* budgeting a sweep — this is what turns a 2-D search into
  two 1-D ones.

## Bearing on the record

**The one practice sourced to this note is confirmed.**

| practice | disposition |
|---|---|
| [SOTA-120](../practices.d/SOTA-120.md) prefer AdamW's decoupled weight decay to L2 added to the loss | confirmed — C1 through C4 |

`SOTA-120` was `Deferred` when this reading was filed, and the reading did
not change that on its own — correctly, because the deferral was never about
the source. This is among the better-evidenced claims in the corpus: an
analytic argument, two measured consequences, and universal adoption since.
What the deferral waited on was evidence that anyone *states* the choice, and
`LIT-156` and `LIT-122` have since supplied it. The practice is now `Active`,
and this note is why nobody had to re-read the source to get there.

The record has a live tension worth recording here. `SOTA-121`'s line — Muon
with decoupled weight decay — turns on `LIT-153`'s argument that constant
decoupled decay **fixes a layer's equilibrium norm** by hyperparameters rather
than by data, which is a cost of exactly the mechanism this paper introduced.
Both can be true: decoupling is the right way to apply decay, and applying a
*constant* decay has a consequence nobody noticed for years.

## Limitations

- Image classification of the period; no language-model evidence here.
- C4's magnitude is specific to the setting where Adam was losing to SGD,
  which is not the modern situation.
- The paper establishes that decoupling is *correct*; it does not study what
  a constant decoupled decay does to weight norms over a long run, which is
  the thread `LIT-153` later pulls.

## Open questions

- If constant decoupled decay pins the equilibrium norm (`LIT-153`), is there
  a schedule for `λ` that keeps decoupling's benefits without that? Nothing
  in this record answers it.
- C1 is about adaptive denominators generally. Which other regularizers in
  common use are being silently rescaled the same way?
