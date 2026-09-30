---
number: 13
status: Rejected
formerly:
- THEORY-tmp0a1gz
title: 'The SGD noise scale g = eps*N/B sets generalization, so the optimal batch size grows with the training set'
version: 1
tags:
- training-optimization
date: '2026-09-16'
source:
- LIT-305
- LIT-058
- LIT-017
summary: >-
  Smith and Le (2017), [LIT-305](../literature.d/LIT-305.md), read SGD as a stochastic differential equation
  with noise scale g = eps*N/B, argued that minibatch noise is what drives the
  optimizer toward minima that generalize, and derived that the optimal batch
  size is proportional to the learning rate and to the training set size.
  Filed `Rejected` and kept: [LIT-058](../literature.d/LIT-058.md) swept 35 workloads thirteen months later,
  found no evidence that larger batches degrade out-of-sample performance once
  the metaparameters are retuned, and reviewed this paper by name as one that
  did not retune. The phenomenon the account explains is, on the larger
  measurement, mostly an artefact of holding the learning rate fixed.
---

# THEORY-013: The SGD noise scale g = eps*N/B sets generalization, so the optimal batch size grows with the training set

## The claim, as it was made

Treat an SGD step as the discretisation of a stochastic differential equation.
The scale of the random fluctuations is then

    g = eps*(N/B - 1) ~= eps*N/B

for learning rate `eps`, training set size `N` and batch size `B`; with
momentum `m` it becomes `eps*N/(B*(1 - m))`. Because the gradient drives the
optimizer toward deep minima and the noise drives it toward broad ones, and
because breadth is what the Bayesian evidence rewards, there is a batch size
that maximises test accuracy rather than merely maximising speed. Holding `g`
fixed as anything else moves gives three scaling rules, the headline one being

    B_opt ~ eps*N

— the optimal batch size is proportional to the learning rate **and to the
size of the training set**. [LIT-305](../literature.d/LIT-305.md) verifies all three empirically.

## Why it is `Rejected`

**The `N` half is contradicted by name, twice, by two different groups.**

[LIT-017](../literature.d/LIT-017.md), two months later, says it outright: it cites this paper, notes that
it "predict[s] a dependence on dataset size", and adds — *"which we do not
observe"*. Its own noise scale is "independent of the size of the full
training set" by construction, and its measurements across MNIST, SVHN,
CIFAR-10, ImageNet, Billion Word, Atari, Dota and an autoencoder find that
more complex datasets have larger noise scales "in a way that is not directly
determined by dataset size".

[LIT-058](../literature.d/LIT-058.md), thirteen months later, tested the dependence the other way — by
subsampling MNIST and ImageNet and re-running — and reports that the effect of
the data set "does not depend on data set size in any consistent way", and is
smaller than the effects of the model and the optimizer.

This record briefly held [LIT-305](../literature.d/LIT-305.md) and [LIT-017](../literature.d/LIT-017.md) as two routes to one statistic.
They are two papers, one of which rebuts the other on the point that
distinguishes them.

**The phenomenon it explains is mostly an artefact of the design.** The whole
account rests on a generalization peak observed "if one holds the other SGD
hyper-parameters constant" — [LIT-305](../literature.d/LIT-305.md)'s own words. [LIT-058](../literature.d/LIT-058.md)'s central finding is
that disagreements in this literature "can largely be explained by differences
in metaparameter tuning", and it finds *no* evidence that larger batches
degrade out-of-sample performance once each batch size is tuned. It reviews
[LIT-305](../literature.d/LIT-305.md) by name and notes that it trained on 1,000 MNIST examples with two
batch sizes "without changing the learning rate between batch sizes".

**[LIT-305](../literature.d/LIT-305.md)'s own figures are consistent with the artefact reading.** Figure 5a
shows the accuracy peak sliding right as `eps` rises. Read as the paper reads
it, that confirms `B_opt ~ eps`. Read the other way, it says the location of
the peak is a fact about the `(eps, B)` pairing rather than about `B` — which
is the same observation, and is why the rule is not wrong so much as not about
what it claims to be about.

## What survives, and it is not nothing

**`g = eps*N/B` held fixed is linear scaling.** Double `B`, double `eps`. The
Bayesian derivation is an independent route to the heuristic Goyal et al.
popularised empirically — which is a real contribution, and also the reason
this is a `Rejected` account rather than a refuted measurement: [SOTA-218](../practices.d/SOTA-218.md) is
the record's position on scaling heuristics, and it says no such rule held
across [LIT-058](../literature.d/LIT-058.md)'s workloads. The derivation predicts a rule; the sweep says the
rule does not transfer.

**The momentum rule is the least tested and the most interesting.**
`B_opt ~ 1/(1 - m)` is the one of the three that [LIT-058](../literature.d/LIT-058.md) indirectly supports:
it found that SGD with momentum extends perfect scaling to larger batch sizes
than plain SGD, which is the same direction. Nobody has checked whether the
coefficient matches.

**And the two "noise scales" in this record are different quantities.** This
is the confusion that filed [LIT-305](../literature.d/LIT-305.md) as a duplicate of the gradient noise scale
in the first place. [LIT-305](../literature.d/LIT-305.md)'s `g` is a property of the *configuration* — three
numbers you chose — and you set it. [LIT-017](../literature.d/LIT-017.md)'s `B_simple = tr(Sigma)/|G|^2` is a
property of the *gradient distribution*, and you measure it. They answer
different questions: what pairing of learning rate and batch size to hold, and
where increasing the batch stops buying speed. [SOTA-198](../practices.d/SOTA-198.md) is about the second.

## What `Rejected` does not mean here

It does not mean the technique fails. Coupling the learning rate to the batch
size works over some range for some workloads, which is why people do it, and
[LIT-305](../literature.d/LIT-305.md) is the cleanest derivation of why it might. It does not mean the
Bayesian-evidence argument about sharp and broad minima is wrong; that is a
separate claim and this record takes no position on it. What is rejected is
the specific account of the generalization gap as a noise-scale effect with a
batch optimum proportional to `N`, on the grounds that the gap it explains
largely disappears under retuning.
