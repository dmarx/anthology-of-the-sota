---
status: Read
paper: LIT-tmp069e7
title: 'A counterexample with no weight decay and a rising weight norm'
version: 1
date: '2026-09-22'
summary: >-
  Read because it is the reason this cluster cannot be filed as a single
  account. A two-layer MLP groks on modular arithmetic with no weight decay and
  a parameter norm that goes up through the transition — which neither the LU
  mechanism nor circuit efficiency can produce, since both turn on the norm
  coming down. The replacement offered is a transition out of lazy dynamics,
  with two measurable knobs; what it does not address is ungrokking.
---

# NOTE-tmpvrr0d: A counterexample with no weight decay and a rising weight norm

## Contribution

Two things, and the first is the more durable. It exhibits grokking in a
setting the standing explanations forbid — no regularization, weight norm
increasing — which converts a field with two competing mechanisms into a field
with two incomplete ones. Then it proposes a third account: early training is
close to linearised, the network fits the training set with its initial
features, and grokking is the late onset of feature learning as the linear
approximation breaks down.

## Key insight

**A memorising solution and a lazy one look the same from outside.** Both fit
the training set fast and generalize badly; both are followed by a long
plateau. The difference is whether the network is storing examples or fitting
them in a fixed feature basis it has not yet updated. If it is the latter, the
delay is the time it takes to leave the kernel regime — and that is set by the
output scale and by how badly the initial kernel is aligned to the task, not by
anything about norm.

## Assumptions

- The analysable case is **polynomial regression with a two-layer network**,
  where sufficient statistics for the test loss can be written down and tracked.
- **Laziness is controlled by an output-scale parameter `α`**, and the paper
  notes the same regime is reachable by label rescaling.
- Alignment is `ε` in the toy model, generalised to arbitrary tasks as
  **centered kernel alignment** between the initial NTK and the labels.
- **Loss, not accuracy**, throughout: the paper argues loss is what drives the
  dynamics and shows in its appendix that accuracy curves on regression tasks
  can be gamed by the choice of metric.
- The counterexample uses MSE loss on a classification task, following the
  convention of the papers it is arguing with.

## Key results

- **The counterexample (§3).** Modular arithmetic, two-layer MLP, **no weight
  decay**: grokking occurs and the parameter weight norm **increases** through
  it. Since [ARXIV-2210.01117](https://arxiv.org/abs/2210.01117) and [ARXIV-2309.02390](https://arxiv.org/abs/2309.02390) both explain grokking by a
  late *decrease* in norm, "grokking cannot in general be explained by theories
  of weight decay". The polynomial-regression task shows the same rising norm.
- **`α` controls grokking continuously.** A sweep over the laziness parameter
  makes the gap more dramatic or removes it entirely.
- **Alignment controls it too.** Worse initial NTK–task alignment gives more
  intense grokking *and a lower final test loss*, because poor alignment is
  exactly the case where feature learning is necessary rather than optional.
  "Lazy, misaligned networks grok the most intensely."
- **Three stated conditions.** The top eigenvectors of the initial NTK are
  misaligned with `y(x)`; the dataset is large enough that generalization is
  eventually possible but not so large that training loss tracks test loss
  throughout; and the network begins lazy.
- **Carried beyond the toy model** to MNIST, one-layer transformers and
  student–teacher networks, and reported as consistent across architectures,
  optimizers and datasets.

## Limitations

**It does not explain ungrokking or semi-grokking.** [ARXIV-2309.02390](https://arxiv.org/abs/2309.02390) derived
both before observing them, and nothing in this account speaks to a grokked
network *regressing* at a sharp threshold in dataset size. A replacement theory
that leaves its predecessor's two confirmed novel predictions unexplained has
not replaced it.

**The analysable setting is a two-layer network on polynomial regression.**
The transformer and MNIST results are reported as consistent rather than
derived.

**Its second condition is a data-size condition.** So the paper that most
directly attacks the weight-norm accounts still agrees with them, and with
Power et al. and `LIT-085`, that the dataset size has to be in a window. That
agreement across three mutually incompatible mechanisms is the most robust
thing in the cluster.

## Bearing on the record

**It is why this unit files three accounts rather than one.** Filing circuit
efficiency alone — which on evidential shape is the most impressive of the
three — would have put a mechanism in the record that a published
counterexample contradicts.

**And it supplies `SOTA-200`'s third knob.** Data fraction is the first;
initialization scale relative to the generalizing norm is the second, from
[ARXIV-2210.01117](https://arxiv.org/abs/2210.01117); initial kernel–task alignment is the third, and it is
measurable on any task by centered kernel alignment, which makes it the one a
practitioner could actually check.

**The methodological aside is worth keeping.** Working in loss rather than
accuracy, on the grounds that accuracy curves on regression tasks can be gamed
by the metric, is `SOTA-200`'s own argument arriving from a different
direction — and it is a nice instance of `DP-004`, since the grokking
literature's query was shaped like an accuracy curve.

## Open questions

- **Can the counterexample be reconciled with ungrokking?** One account
  explains a phenomenon the other cannot produce, and the other exhibits a
  setting the first cannot cover. Nobody has a theory covering both, and that
  is the state this record is filing.
- **Does low NTK–task alignment predict grokking prospectively?** Centered
  kernel alignment is computable before training. Whether it forecasts a
  delayed-generalization run in a realistic setting is not tested here.
