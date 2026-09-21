---
status: Active
title: Neural networks with late-phase weights
version: 1
tags:
- training-optimization
- model-stability
date: '2026-09-21'
published: '2020-07-01'
arxiv: '2007.12927'
first_author: 'von Oswald'
keywords:
- 'weight-averaging'
- 'ensembles'
- 'batchnorm'
- 'flat-minima'
- 'swa'
implementations: []
summary: >-
  von Oswald, Kobayashi, Meulemans, Henning, Grewe and Sacramento (2020),
  [ARXIV-2007.12927](https://arxiv.org/abs/2007.12927). Late in training, replicate a *small* subset
  of the weights — BatchNorm's scale and shift will do — train `K` copies that
  share everything else, and average them into one model at the end. Inference
  cost unchanged. WRN 28-10 on CIFAR-100: 81.35 → 82.87. Starting the same
  procedure at initialization instead **fails to beat the baseline**.
---

# LIT-tmpledv1: Neural networks with late-phase weights

## Why it's here

The record has **nothing** on weight-space ensembling. No stochastic weight
averaging, no model soups, no snapshot ensembles, no Polyak averaging —
a whole family of cheap generalization gains that is standard practice and
entirely unrepresented. This is the highest-traffic unfiled entry point to it,
and it names SWA as the baseline it improves on.

It also touches [SOTA-012](../practices.d/SOTA-012.md)'s subject from the constructive side. The
method's perturbative initialization is justified by the dense-cluster,
locally-flat picture of SGD solutions — the assumption is that `K` perturbed
copies stay in **one** basin, because if they hopped modes the final average
would be meaningless.

## What it does

Split the weights at some time `T₀` into a **base** set, shared and trained
throughout, and a small **late-phase** set that is replicated `K` times.
From `T₀` onward, train `K` models that differ only in their late-phase
components: update each copy's late-phase weights on every minibatch, and
accumulate the base gradients across copies before taking one base step.

At test time the ensemble is thrown away and the late-phase weights are
**averaged into a single model**. Inference costs exactly what the original
model cost.

Which weights to replicate is the design space, and the answer is
anticlimactic:

- **BatchNorm scale and shift** (`γ`, `β`) — the default, motivated by the
  finding that training only these can reach much lower loss than training a
  random subset of matching size.
- **Rank-1 multiplicative matrices**, for architectures without BatchNorm.
- **Linear hypernetwork weight embeddings**, the general case.
- The **final classification layer**, included by default in classification.

Copies are initialized as Gaussian perturbations of a reference weight, with
the noise scaled layerwise (`σ ∝ √(1/n_in)`) so one hyperparameter governs the
whole network — though on CIFAR the main experiments use **no initialization
noise at all**.

## What was measured

CIFAR-10, WRN 28-10, 5 seeds:

| | test acc. |
|---|---|
| Base (SGD) | 96.16 ± 0.12 |
| Dropout (SGD) | 96.02 ± 0.06 |
| BatchEnsemble (SGD) | 96.19 ± 0.18 |
| **Late-phase (SGD)** | **96.46 ± 0.15** |
| Base (SWA) | 96.48 ± 0.04 |
| **Late-phase (SWA)** | **96.81 ± 0.07** |
| Deep ensemble (SGD), 1 seed | 96.91 |

CIFAR-100, WRN 28-10, 5 seeds: base 81.35 ± 0.16 → **BatchNorm late-phase
82.87 ± 0.22** under SGD; 82.46 ± 0.09 → **83.06 ± 0.08** under SWA. A deep
ensemble reaches 84.09 at full cost.

ImageNet, fine-tuning a pretrained model for 20 epochs, 5 seeds: ResNet-50
76.62 → **76.87**, ResNet-152 78.37 → **78.77**, DenseNet-161 78.17 →
**78.31**. Small margins against standard deviations of 0.01–0.06, so
resolved.

enwik8, a 500-unit LSTM, bits per character: base 1.695, base with the rank-1
multiplicative parameters but no ensembling 1.663, late-phase rank-1 1.633.

## The three results that constrain the recommendation

**"Late" is load-bearing.** Running the same procedure from `T₀ = 0` — the
ensemble present from initialization — **fails to match the base model** on
both CIFAR-10 and CIFAR-100. This is not a minor ablation; it is the
difference between the method working and not.

**The simplest variant wins and the sophisticated one does not.** On CIFAR-100
hypernetwork weight embeddings score 81.55 against BatchNorm's 82.87 and the
base model's 81.35 — essentially nothing under SGD, and under SWA they land at
82.01 against a base of 82.46, which is **worse than doing nothing**.

**Low dimension is doing work.** A late-phase *full* deep ensemble — same
schedule, every weight replicated — lands between the base model and the
low-dimensional version. Replicating more is not better.

## Conditions

**SWA may already be most of it, depending on the setting.** On enwik8 the
three LSTM variants under SWA are 1.626, 1.616 and 1.615 — the late-phase
advantage over plain SWA is 0.011 BPC, against a 0.062 advantage without it.
On CIFAR the interaction is the other way: late-phase plus SWA beats SWA alone
by 0.33 (CIFAR-10) and 0.60 (CIFAR-100). So the two are partly redundant and
the degree depends on the problem. Anyone adopting this should measure SWA
first, because it is simpler.

**Most of the LSTM gain is not the ensemble.** Merely adding the rank-1
multiplicative parameters, with no replication and no averaging, moves 1.695 →
1.663; late-phase adds 1.663 → 1.633. Half the effect is a parameterization
change.

**Deep ensembles are still better**, at `K` times the cost — 96.91 against
96.81 on CIFAR-10, 84.09 against 83.06 on CIFAR-100. The paper says so and
uses them as an upper baseline rather than a comparison.

**Vision, plus one small LSTM.** WRN, PyramidNet, ResNet, DenseNet on
CIFAR-10/100 and ImageNet; a 1.56M-parameter LSTM on enwik8, deliberately
sized so it does not overfit and with no regularization at all. Nothing at
transformer scale, and the paper is from 2020.

**BatchNorm is assumed.** The default and best-performing variant needs it.
The alternatives exist for architectures without it and are the ones that
performed worse.
