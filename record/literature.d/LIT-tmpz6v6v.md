---
status: Active
title: 'Understanding Black-box Predictions via Influence Functions'
version: 1
tags:
- analysis-and-evaluation
- data-pipeline
date: '2026-09-17'
published: '2017-03-14'
arxiv: '1703.04730'
first_author: 'Koh'
keywords:
- 'influence-functions'
- 'data-attribution'
- 'dataset-debugging'
- 'data-poisoning'
implementations: []
summary: >-
  Koh and Liang (2017), [ARXIV-1703.04730](https://arxiv.org/abs/1703.04730). Traces a prediction back through the
  learning algorithm to the training points responsible for it, using a
  classical technique from robust statistics made tractable by needing only
  gradients and Hessian-vector products. The origin of training-data
  attribution in deep learning.
---

# LIT-tmpz6v6v: Understanding Black-box Predictions via Influence Functions

Koh and Liang (2017) — [ARXIV-1703.04730](https://arxiv.org/abs/1703.04730)

## Key takeaways

- **Asks a counterfactual and answers it without running it.** How would this
  prediction change if this training point were not in the training set?
  Answering by retraining is prohibitive; the influence function answers it
  analytically by upweighting the point infinitesimally and differentiating
- **Made practical by never forming the Hessian.** Both routes — conjugate
  gradients, and the stochastic estimator of Agarwal et al. — need only
  Hessian-vector products, which cost about a gradient each. The stochastic
  version estimated `H⁻¹v` on MNIST *without looking at every training point*,
  and even a single repeat still identified the most influential examples
- **The theory assumes a twice-differentiable, strictly convex risk and the
  paper then breaks both assumptions on purpose.** Under non-convergence and
  non-convexity a damped quadratic approximation around the actual parameters
  still gives meaningful results. Under non-differentiability it does **not**:
  setting the derivative at an SVM hinge to zero gave inaccurate influences,
  and a smooth surrogate loss was needed
- **Four uses, and they are still the four.** Understanding what a model
  relies on; quantifying vulnerability to training-set attacks; debugging
  domain mismatch; and finding mislabelled examples
- **Two models, same predictions, different mechanism.** An Inception v3 with
  frozen lower layers and an RBF-SVM agree on a dog-versus-fish task. The
  SVM's influences vary inversely with raw pixel distance — a soft nearest
  neighbour — while Inception's barely correlate with it, and its **fifth most
  helpful image for classifying a fish was a dog**
- **The attack is the same computation as the explanation.** Constructing
  visually indistinguishable training-set perturbations is mathematically the
  same gradient step, which is why the method also measures how exposed a
  model is to data poisoning
- **Dataset repair, quantified.** On Enron1 spam (4,147 train, logistic
  regression on bag-of-words) with 10% of labels flipped, prioritising
  inspection by influence repaired the dataset after checking fewer points
  than either the highest-training-loss baseline or random, over 40 repeats,
  with no access to test data

<!-- inactive-ok-block: SOTA-tmp8ornu, THEORY-tmp7738v — the practice this paper sources
     (Proposed) and the account it published with the method (Rejected). The Rejected one
     is the point: this paper is where that explanation comes from, so naming its successor
     instead would misattribute it. -->
## Standing in the anthology

Read — [NOTE-tmptzfh5](../notes.d/NOTE-tmptzfh5.md). Sources [SOTA-tmp8ornu](../practices.d/SOTA-tmp8ornu.md), and states [THEORY-tmp7738v](../theory.d/THEORY-tmp7738v.md) —
the account of what an influence estimate measures that [LIT-tmpyirk2](LIT-tmpyirk2.md) later
corrected for neural networks.
