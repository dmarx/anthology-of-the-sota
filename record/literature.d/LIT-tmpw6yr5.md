---
status: Active
title: 'On the distance between two neural networks and the stability of learning'
version: 1
tags:
- training-optimization
- model-stability
date: '2026-09-25'
published: '2020-02-09'
arxiv: '2002.03432'
first_author: 'Bernstein'
keywords:
- 'deep-relative-trust'
- 'fromage'
- 'layerwise-relative-update'
- 'descent-lemma'
- 'frobenius-norm'
- 'lars'
implementations:
- 'fromage (github.com/jxbz/fromage)'
extends:
- LIT-009
extended_by:
- LIT-436
corrected_by:
- LIT-437
compared_against:
- LIT-001
summary: >-
  Bernstein, Vahdat, Yue and Liu (NeurIPS 2020), [ARXIV-2002.03432](https://arxiv.org/abs/2002.03432). A deep
  network's trust region is not quadratic. The change in its function and
  Jacobian is bounded by a *product* of per-layer relative perturbations
  ("deep relative trust"), and Figure 1 shows loss and gradient breaking down
  quasi-exponentially in that quantity at depth 16. The optimizer it derives,
  Fromage, is LARS plus a norm-correcting prefactor. It is the Frobenius
  antecedent of the modular-norm line. LIT-437, which shares an author,
  names its conditioning assumption as the flaw and replaces Frobenius with
  spectral.
---

<!-- inactive-ok-file: THEORY-024 THEORY-012 — both Proposed; named as the account this
     paper is the corrected antecedent of, and the account it adds a small,
     confounded data point to. Neither is relied on here -->

# LIT-tmpw6yr5: On the distance between two neural networks and the stability of learning

Bernstein, Vahdat, Yue and Liu (2020; NeurIPS 2020) — [ARXIV-2002.03432](https://arxiv.org/abs/2002.03432)

## Key takeaways

**The argument.** Gradient descent minimizes a first-order model plus a
quadratic trust penalty. "Since a quadratic trust region does not capture the
compositional structure of a neural network, it is difficult to choose the
learning rate η in practice." The proposal is to replace the penalty with a
distance made of per-layer *relative* changes.

**Theorem 1 (MLPs), and the step that is not a theorem.** Under a
transmission bound on the nonlinearity and a **conditioning** assumption, that
all weights *and their perturbations* have condition number at most κ, the
relative change in output and in each layer-to-output Jacobian is bounded by
`(βκ²/α)^L [Π_k (1 + ‖ΔW_k‖_F/‖W_k‖_F) − 1]`. Extending this to the loss
gradient is "a modelling assumption", deep relative trust. It sets `κ = 1`
and neglects `∂L/∂f`.

**The measured part is Figure 1.** For 2- and 16-layer MLPs on MNIST, the
weights are perturbed along the full-batch gradient at relative size up to
0.1. "For the depth 16 network, … the loss and gradient did break down
quasi-exponentially in the layerwise relative size of a parameter
perturbation. For the depth 2 network, the breakdown was much milder." This
is direct evidence against assuming Lipschitz-smooth gradients in deep
networks.

**Fromage.** `W ← (1/√(1+η²)) · [W − η (‖W‖_F/‖g‖_F) g]` per layer, with no
momentum and "a good default η = 0.01". The prefactor is the difference from
LARS. In scale-invariant layers the gradient is orthogonal to `W`, so without
it the norm grows by `√(1+η²)` per step: "compounding growth … numerical
overflow". Figure 2 shows this as a clean lesion on a spectrally normalized
GAN.

**Results, three seeds, test set:**

| benchmark | SGD | Fromage | Adam |
| --- | --- | --- | --- |
| CIFAR-10 (loss) | 0.545 | **0.31** | 0.76 |
| ImageNet (loss) | **1.091** | 1.126 | 1.184 |
| GAN (FID) | 34 | **16** | 23.9 |
| Transformer, Wikitext-2 (ppl) | **169.6** | 171.1 | 172.7 |

On training perplexity, the paper's own primary metric ("all results are
reported on the training set"), the transformer row is Fromage 66.1 against
Adam **36.8**. Deep MLPs without batch norm or skips train to "at least
depth 50" with Fromage, against about 25 for SGD and Adam.

## Traps

- **"Little to no learning rate tuning" is weaker than it reads.** η was
  grid-searched over powers of ten for the GAN and for ImageNet. The finding
  is that the same grid point won. On deep MLPs "a smaller value of η was
  needed", and the Discussion concedes "Fromage's optimal learning rate should
  depend on network depth."
- **The CIFAR-10 and transformer rows carry a Fromage-specific fix.** "Fromage
  would heavily overfit the training set. We were able to correct this … by
  constraining the neural architecture": each layer's norm is capped at its
  initial value. The text does not say the baselines got the same cap.
- **The Frobenius norm is the part that was retracted.** [LIT-437](LIT-437.md)
  names this paper's Condition 2 as "the flaw in that analysis": weights have
  high stable rank and updates low. It says the paper "obtained the wrong
  scaling relation with network width". `κ = 1` in deep relative trust is
  exactly that condition.
- **It is not where Muon comes from.** It has no spectral norm, no
  orthogonalization and no duality map, and [LIT-438](LIT-438.md) does not cite it.
  The route runs this paper → (corrected by) [LIT-437](LIT-437.md) → [LIT-436](LIT-436.md) → [LIT-438](LIT-438.md).

## Standing in the anthology

Filed from the reading-time triage of 2026-09-25, which called it "the 2020
paper between" signSGD and Modular Duality. That was right about the order
and wrong about the lineage. The later line builds on the *per-layer
relative* idea and explicitly replaces this paper's norm. So what it gives
the record is the thing [THEORY-024](../theory.d/THEORY-024.md)'s supporting line
contrasts against: "not from Frobenius or entry-size heuristics". It is
filed as that corrected antecedent, not as a source.

**A third data point for [THEORY-012](../theory.d/THEORY-012.md) and
[SOTA-221](../practices.d/SOTA-221.md).** Those say a layerwise ratio with no
per-coordinate term is not enough for an attention stack. LARS fails on BERT.
Fromage, layerwise-only, wins on ResNets and the GAN and loses the
transformer's training perplexity to Adam by a wide margin. The comparison is
small and confounded, so it belongs here in prose, not in a `source:` list.

**It challenges an assumption of the same author's earlier paper.**
[LIT-280](LIT-280.md) (signSGD) rests on coordinate-wise Lipschitz smoothness, and
Figure 1 argues that deep networks violate it. That challenges an assumption,
not a result, so no relation is declared.
