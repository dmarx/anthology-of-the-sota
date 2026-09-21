---
number: 226
status: Read
formerly:
- NOTE-tmpbp3dj
paper: LIT-477
title: 'NoProp'
version: 1
date: '2026-09-21'
summary: >-
  Reading it: the interesting number is in the train column, not the test one.
  NoProp matches backprop on test while sitting 8-15 points behind on train,
  which on MNIST and CIFAR costs nothing and would be the whole story anywhere
  fitting is the binding constraint. The paper does not mention it.
---

# NOTE-226: NoProp

## Contribution

A backprop-free training method that is actually competitive, by borrowing
the objective from diffusion models and pointing it at a label embedding
rather than an image. Before this, the local-learning family — forward-forward,
target propagation, forward gradients — was 10 to 30 points behind
backpropagation on CIFAR-10. This closes that gap.

What is true afterwards that was not before: "train each layer independently"
is no longer synonymous with "accept a large accuracy penalty", at least at
this scale.

## Key insight

**Diffuse the label, not the data.** Every other application of this machinery
noises the thing you want to generate. Here the noised object is the target
embedding, the input is a condition held fixed across the whole trajectory,
and the "generative" process produces a classification.

Once framed that way, layer independence falls out: block `t` needs
`(z_{t-1}, x)` and the clean label, and `z_{t-1}` comes from a fixed analytic
noising process rather than from block `t-1`'s learned output. There is
nothing to propagate because there is nothing upstream to wait for.

## Assumptions

- **Every block is conditioned directly on the input.** Stated in §2.1 and
  acknowledged as unlike a standard network. This is the load-bearing
  structural choice, not an implementation detail.
- **A variance-preserving Ornstein-Uhlenbeck forward process** with a fixed
  Gaussian variational posterior, following variational diffusion models.
- **The class embedding matrix** may be fixed (one-hot), learned at dimension
  20, or learned at image dimension ("prototype").
- **No data augmentation** on any dataset.
- **Sequential per-timestep updates each epoch**, chosen for comparability
  with other backprop-free methods rather than out of necessity — timesteps
  could be sampled instead.

## Key results

- Test accuracy, NoProp-DT (prototype) vs best backprop: MNIST **99.54** vs
  99.46; CIFAR-10 **80.54** vs 79.92; CIFAR-100 46.06 vs **47.80**.
- Train accuracy, CIFAR-10: backprop 99.98, NoProp-DT 95.02–97.23.
  CIFAR-100: backprop 98.63–99.19, NoProp-DT 83.25–90.70.
- Prior backprop-free: Forward-Forward 98.63 (MNIST); Local Greedy Forward
  Gradient 69.32 (CIFAR-10); Difference Target Propagation 50.71 (CIFAR-10).
- GPU memory, discrete time: 0.49 / 0.64 / 1.23 GB vs backprop's
  0.87 / 1.17 / 1.73. Continuous: 0.45–1.05 GB vs adjoint's 2.32–6.45.
- NoProp-CT CIFAR-100: 33.66. **NoProp-FM one-hot CIFAR-100: 6.38 ± 4.9.**
- Ablations: no consistent winner between the two class-probability
  parameterisations; orthogonal and prototype embedding initialisations are
  at least as good as random.

## Claims

**Well supported:** that it beats prior backprop-free methods by a wide
margin, and that it uses substantially less memory. Three seeds, five
inference runs, standard errors reported.

**Supported with a caveat the paper supplies itself:** that it matches
backprop. The baseline was constructed to share NoProp's forward structure,
which is the right thing to do — but that structure includes input
connections into every block, so what is matched is a network built for
NoProp's constraint, not a conventional stack.

**Motivational rather than measured:** the distributed-training argument. The
introduction names sequential gradient dependence as an obstacle to
multi-device training. No distributed experiment appears.

## Method

Variational diffusion ELBO over a label embedding, with each block trained by
L2 regression to the clean embedding plus a cross-entropy readout term;
discrete-time, continuous-time and flow-matching variants; compared against a
structure-matched backprop baseline and, in continuous time, against adjoint
sensitivity.

## Concepts

*NoProp-DT / CT / FM*; class embedding as the diffused variable; *prototype*
embeddings, which turn out to be recognisable class-average images; the
signal-to-noise-ratio weighting in the objective.

## Connections

- [SOTA-154](../practices.d/SOTA-154.md) is the record's other answer to "what if not
  backpropagation" — evolution strategies. A different family entirely:
  perturbation-based and black-box, where this is local and analytic. Neither
  cites the other, and the record now holds one of each.
- The activation-memory concern is the one [SOTA-087](../practices.d/SOTA-087.md) addresses by
  *recomputing* what the backward pass needs instead of storing it. This
  addresses the same cost by never incurring it — there is no backward pass
  across blocks to serve — which is a different point on one axis, and the
  memory table is the comparison.
- The diffusion and flow-matching machinery is the record's
  `generative-modeling` cluster used for something that is not generation.

## Bearing on the record

One practice, `Proposed` and tightly conditioned, in a niche the record had
no entry in at all. The honest headline is *"if you need backprop-free, this
is the one that works"* rather than *"backpropagation has an alternative"*.

## Limitations

**The train-accuracy gap is the finding nobody discusses.** Eight to fifteen
points behind backprop on training data while matching on test. On MNIST and
CIFAR, where backprop is at ceiling on train and test scores are set by
generalization, that is free. Anywhere fitting the training data is the
binding constraint — which is essentially every setting this record covers —
it is the whole question, and there is no result here that speaks to it.

**Scale.** Three small image classification benchmarks, no augmentation.

**Two of the three variants are weak and one is broken.** NoProp-FM with
one-hot embeddings on CIFAR-100 scores 6.38 ± 4.9. The paper reports it and
moves on; the family-level claim should not.

**Depth may not be doing what depth usually does.** Every block sees the raw
input, so the layer-wise refinement of representations that motivates deep
networks is not obviously happening. The paper does not investigate what the
intermediate blocks represent, and Figure 2 — learned class embeddings that
look like class-average images — is the only window onto it.

**No limitations section.** The conclusion is a positive summary. Everything
above came from the tables.

## Open questions

- Does the train-accuracy gap close with capacity, or is it structural? This
  is the question that decides whether the method scales, and it is one
  experiment: train both to convergence on something backprop cannot already
  fit perfectly.
- What do the intermediate blocks compute, given each one sees the input? If
  the answer is "roughly the same thing, refined", the method is a deep
  ensemble with a schedule rather than a hierarchy.
- Does the claimed parallelism materialise? Independent blocks should train on
  separate devices without gradient synchronisation. Nobody has run it.
