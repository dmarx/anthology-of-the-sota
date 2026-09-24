---
number: 384
status: Active
formerly:
- SOTA-tmprlwc2
title: 'Calibrate a trained classifier with a single temperature fitted on held-out data, not with a richer map'
version: 1
tags:
- analysis-and-evaluation
- training-optimization
date: '2026-09-23'
source:
- LIT-616
introduced_by:
- LIT-616
consensus: converged
consensus_note: >-
  Grounds, and their limits, stated rather than assumed. The comparison is
  one group's: Guo et al. across eleven model-dataset pairs in two
  modalities, where temperature scaling beat every alternative on the vision
  tasks and tied on the text ones. What the record adds is downstream
  reliance rather than replication — LIT-514, a different group eight years
  later, builds its whole early-stopping method on temperature scaling
  without re-arguing the choice, and SOTA-315 already tells readers to keep
  the fitted temperature. No survey of the field was run here. `converged`
  rather than `universal` because an uncalibrated classifier still ships
  without comment wherever the probabilities are only ever argmaxed.
implementations: []
summary: >-
  Guo et al. (2017), [LIT-616](../literature.d/LIT-616.md) — rescale the logits by a single learned
  `1/T` fitted for NLL on a held-out set. It cannot change the argmax, so
  accuracy is unchanged by construction, and it beats vector scaling, matrix
  scaling, histogram binning, isotonic regression and BBQ — including the
  two that strictly contain it. Typical uncalibrated ECE is 4–10%.
---
<!-- inactive-ok-file: THEORY-060 — Proposed; named to mark what this paper is NOT a replication of — its decomposition is calibration against refinement, where Guo et al. separate a proper loss from the 0/1 loss -->

# SOTA-384: Calibrate a trained classifier with a single temperature fitted on held-out data, not with a richer map

## Source

Guo, Pleiss, Sun and Weinberger (2017), [LIT-616](../literature.d/LIT-616.md).

## When this applies

Your classifier's output probabilities are used for something other than
taking the argmax — a threshold, a ranking, an abstention rule, a
downstream expected-value calculation, a hand-off to a person — and you have
a held-out set you can spend. Modern architectures are the case that needs
it: typical ECE is **4–10%**, and depth, width, BatchNorm and *reduced*
weight decay each make it worse while improving accuracy.

## Do this

**Fit one scalar.** After training, divide the logits by a temperature `T`
and optimize `T` for NLL on the validation set with the network frozen:

    q̂ᵢ = max_k softmax(zᵢ / T)⁽ᵏ⁾

`T > 1` softens the distribution. It is a one-dimensional convex problem —
about ten conjugate-gradient iterations, a fraction of a second — and in a
framework it is a constant multiplier inserted between the logits and the
softmax, set to 1 during training.

**Note what it cannot do, because that is the reason to prefer it.** A single
positive scalar does not move the argmax, so **accuracy is unchanged by
construction**. Nothing has to be re-validated after applying it. The binning
methods do not have this property: histogram binning, isotonic regression
and BBQ all change class predictions, and cost accuracy for it.

**Do not reach for the more general version.** Vector scaling (a diagonal
matrix) and matrix scaling (a full one) strictly contain temperature scaling
and both do worse. The vector solution comes out with nearly constant
entries — the paper's reading is that **miscalibration is intrinsically low
dimensional**. Matrix scaling is worse still above a few hundred classes,
because its parameter count grows quadratically, and it fails to converge at
all on ImageNet's 1000.

## Why the problem exists at all

Networks overfit to NLL without overfitting to 0/1 loss. On a CIFAR-100
ResNet the test error falls from 29% to 27% **inside the region where NLL is
already rising** — the model buys accuracy with confidence it has not
earned. That is why the four things that worsen calibration are all things
adopted for accuracy, and why the fix is post hoc rather than a change to
training. The paper is explicit that *why* those trends do this is open.

## Limitations

- **It does not fix a model, it fixes a report.** Refinement — how well the
  predictions separate the classes — is untouched, by the same argument that
  makes accuracy untouched. [THEORY-060](../theory.d/THEORY-060.md) is about that other term.
- **It assumes train, validation and test come from one distribution**, which
  is stated in the paper and is the first thing to go in deployment.
- **One dataset in the study was not improved by any method.** Reuters, at
  ECE below 1% before calibration; the authors say post-processing may not
  have been necessary there, and allow that their measurements may be
  affected by the dataset split or the binning scheme.
- **ECE itself is a binned estimate**, which the paper computes at M=15. The
  measure is Naeini et al. (2015), not this paper — this is where it became
  the default.
