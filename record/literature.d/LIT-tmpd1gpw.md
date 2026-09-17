---
status: Active
title: 'Deep Learning on a Data Diet: Finding Important Examples Early in Training'
version: 1
tags:
- data-pipeline
date: '2026-09-17'
published: '2021-07-15'
arxiv: '2107.07075'
first_author: 'Paul'
keywords:
- 'data-pruning'
- 'example-difficulty'
- 'training-dynamics'
- 'label-noise'
implementations: []
summary: >-
  Paul et al. (2021), [ARXIV-2107.07075](https://arxiv.org/abs/2107.07075). Two scores — GraNd and EL2N — that rank
  training examples by importance a few epochs into training rather than at
  the end of it, and transfer across architectures. Also the finding that the
  very highest-scoring examples should be excluded, more so under label noise.
---

# LIT-tmpd1gpw: Deep Learning on a Data Diet: Finding Important Examples Early in Training

Paul et al. (2021) — [ARXIV-2107.07075](https://arxiv.org/abs/2107.07075)

## Key takeaways

- **The ranking is available long before the model is.** Prior difficulty
  measures — forgetting events, AUM — integrate over a whole training run, so
  they cost the run you were trying to avoid. The **GraNd** score (expected
  loss-gradient norm, which up to a constant bounds the change in loss from
  removing that example) and its cheap approximation **EL2N** (the norm of
  the error vector: predicted class probabilities minus the one-hot label)
  are computed from local information at a single early checkpoint
- **EL2N at epoch 20 prunes 50% of CIFAR-10 with test accuracy slightly
  improved**, and 25% of the harder CIFAR-100. The paper's abstract says that
  second figure costs nothing and its conclusion says it costs about a point;
  the conclusion is the one to quote
- **Average over initializations, not over time.** Scores from a single
  network perform materially worse; the paper's protocol averages over ten
  independently initialized networks. What is being estimated is a property
  of the example, and one trajectory is one sample of it
- **The scores transfer.** EL2N computed on a ResNet18 prunes just as well for
  a ResNet50, and scores calculated during hyperparameter search are reusable.
  The ranking is a property of the dataset rather than of the network
- **The top of the ranking is not safe.** Excluding a small subset of the
  very highest-scoring examples *improves* performance, and the optimal window
  widens as label corruption rises — the hardest examples and the mislabelled
  ones are the same examples. Without a validation set, the paper says to be
  cautious about keeping them
- An earlier version of this paper reported striking results for pruning *at
  initialization*; those were retracted after a framework bug was found. The
  surviving claim is specifically about early training, not about zero steps

<!-- inactive-ok-block: SOTA-tmp8yskz, SOTA-tmp70sgi — both Proposed, and both filed from
     this note in the same contribution. Named to say what this paper sources and what it
     corroborates; there is no Active practice on either claim to name instead. -->
## Standing in the anthology

Read — [NOTE-tmpsdgml](../notes.d/NOTE-tmpsdgml.md). Sources [SOTA-tmp8yskz](../practices.d/SOTA-tmp8yskz.md), and corroborates [SOTA-tmp70sgi](../practices.d/SOTA-tmp70sgi.md).
