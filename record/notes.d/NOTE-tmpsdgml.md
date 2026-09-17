---
status: Read
paper: LIT-tmpd1gpw
title: 'Deep Learning on a Data Diet: Finding Important Examples Early in Training'
version: 1
date: '2026-09-17'
summary: >-
  Two scores that rank training examples by importance from a single early
  checkpoint — GraNd (expected loss-gradient norm) and EL2N (norm of the error
  vector) — averaged over several initializations. They prune half of CIFAR-10
  without loss, transfer across architectures, and come with the finding that
  the very highest-scoring examples should be excluded, more so under label noise.
---

# NOTE-tmpsdgml: Deep Learning on a Data Diet: Finding Important Examples Early in Training

<!-- inactive-ok-file: SOTA-tmp8yskz, SOTA-tmp70sgi — the practice this reading files and the
     one its R3 corrects, both Proposed and both filed here. Cited to say where each
     recommendation landed. -->

## Contribution

Before this, ranking training examples by importance meant watching a whole
training run: forgetting events count how often an example flips from correct
to incorrect over training, AUM integrates margin over the trajectory. Both
cost the run you were hoping to avoid — Toneva et al.'s forgetting scores
stabilise only around epoch 75 of 200 on ResNet18/CIFAR-10.

This paper shows the ranking is available **from local information at a
single early checkpoint**, and that it is good enough to prune on.

## Key insight

The quantity that matters is how much removing an example would change the
loss elsewhere, and after a few epochs a very cheap statistic tracks it.

**GraNd** is the expected loss-gradient norm of an example, which up to a
constant bounds the expected change in loss on an arbitrary other example
caused by removing it. **EL2N** is the norm of the error vector — predicted
class probabilities minus the one-hot label — which approximates GraNd once
per-logit gradients are roughly orthogonal and comparable in size, a condition
the paper argues holds after a few epochs. EL2N is not merely cheaper; the
paper finds it a *stronger* pruning signal than GraNd.

The second insight is about variance. **A score is a property of the example,
and one trajectory is one sample of it.** Scores from a single network perform
materially worse than the same scores averaged over ten independently
initialized ones. The averaging is over initializations, where the earlier
literature averaged over time.

## Assumptions

- Supervised classification with a one-hot target, so that "the error vector"
  is defined. EL2N has no obvious form for next-token prediction over a
  vocabulary, and the paper does not offer one.
- Several independent training runs are affordable, at least for a few epochs.
- The approximation of GraNd by EL2N needs the early-training regime; it is
  argued from prior work on logit-gradient geometry, not proved.

## Key results

- **50% of CIFAR-10 pruned with test accuracy slightly improved**, using EL2N
  computed at epoch 20 from ten ResNet18s.
- **25% of CIFAR-100**, where the abstract says at no cost and the conclusion
  says at about a one-point drop. The conclusion is the figure to quote.
- **The scores transfer across architectures.** EL2N computed on ResNet18
  prunes as well for ResNet50 as ResNet50's own scores do; scores computed
  during hyperparameter search are reusable. The ranking is a property of the
  dataset, not of the network.
- **The optimal subset excludes the very highest scorers.** Keeping only the
  top-scoring examples is not optimal even on clean data, and the window of
  excluded examples widens as label corruption rises — the hardest examples
  and the mislabelled ones are the same examples.
- Averaging over initializations is load-bearing: single-network scores
  underperform.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | GraNd bounds the effect of removing an example on the loss elsewhere | strong | derived, under a continuous-time approximation |
| C2 | EL2N approximates GraNd after a few epochs, and prunes better | moderate | argued from logit-gradient geometry, shown empirically |
| C3 | Early scores identify prunable examples as well as trajectory-integrated ones | strong | CIFAR-10 and CIFAR-100, against forgetting scores |
| C4 | Scores must be averaged over initializations | moderate | ablation; single-network scores underperform |
| C5 | Scores transfer across architectures and hyperparameters | moderate | ResNet18 to ResNet50, plus the HPO reuse experiment |
| C6 | The best subset excludes the very highest scorers, increasingly under noise | moderate | the label-corruption sweep |

## Method

Train `n` independently initialized networks for a small number of epochs
(20, here). For each example compute EL2N — the L2 norm of (predicted class
probabilities − one-hot label) — and average across the `n` networks. Sort.
Discard the lowest-scoring fraction, and optionally the highest-scoring tail.

## Concepts

- **Importance as removal effect** — the definition GraNd formalises: an
  example matters to the extent that deleting it would move the loss on
  others.
- **Early training as a sufficient probe** — the practical claim. What a
  network knows at epoch 20 about which examples are hard is most of what it
  will ever know.
- **The window, not the threshold** — difficulty ranking has two bad ends, and
  the discussion of "keep the hard ones" usually forgets the upper one.
- **Hardest and mislabelled are the same examples** — which is why the upper
  cutoff moves with label noise, and why a corpus's noise rate is a parameter
  of any difficulty-based selection.

## Connections

The natural pair is [LIT-tmpy1abi](../literature.d/LIT-tmpy1abi.md), which uses EL2N as the metric for its
CIFAR-10 confirmation of the abundance inversion and benchmarks it among ten
at ImageNet scale. Read together they say: *which* end to prune from depends
on abundance, and *where* the score comes from can be a cheap early
checkpoint — with C6 adding that the hard end has its own cutoff, which the
abundance story on its own would not tell you.

## Recommendations

- **R1** — Compute example-importance scores a few epochs into training,
  averaged over several initializations, rather than at the end of one run.
  *Topic:* data pipeline. *Strength:* moderate. *Applies when:* the task is
  supervised classification.
- **R2** — Reuse a score across architectures rather than recomputing it.
  *Strength:* moderate.
- **R3** — Exclude the highest-scoring tail as well as the lowest, and widen
  that exclusion when the corpus is noisy. *Strength:* moderate.

## Bearing on the record

Sources [SOTA-tmp8yskz](../practices.d/SOTA-tmp8yskz.md) (R1, with R2 in the body) and corroborates
[SOTA-tmp70sgi](../practices.d/SOTA-tmp70sgi.md), whose conditions carry R3 — the upper cutoff is a correction to
"keep the hard examples", so it belongs where that instruction is read rather
than in a document of its own.

Both practices are `Proposed`, and the binding limitation is the same for
both: EL2N is defined on a one-hot error vector, which pretraining does not
have.

## Limitations

- Vision classification only, and the score's definition does not obviously
  survive the move to next-token prediction.
- Requires several independent runs, which is cheap at CIFAR scale and is not
  obviously cheap anywhere the record's practices operate.
- The GraNd–EL2N approximation is argued rather than proved.
- The paper carries a **retraction of its own earlier claim** about pruning at
  initialization, withdrawn after a framework bug was identified by later
  work. Worth knowing before citing any "prune before training" result.

## Open questions

- What plays the part of the error vector in language-model pretraining?
  Per-token loss is the obvious candidate and nothing here tests it.
- Does the upper cutoff have an analogue in document-level corpus filtering —
  is the "highest-quality" tail of a learned classifier also the tail that
  should be dropped?
