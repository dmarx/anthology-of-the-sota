---
number: 217
status: Proposed
formerly:
- SOTA-tmpjxbss
promote_when: >-
  Permutation alignment demonstrated to improve a real distributed training
  run — federated, gossip, or model-merging — rather than the interpolation
  barrier between two checkpoints. The barrier result is established; that it
  is worth paying for during training is not.
consensus: emerging
consensus_note: >-
  Two groups, one year apart, reaching the same conclusion from opposite
  directions: one conjectured that permutation explains the barrier, the other
  supplied the algorithms and closed it on real networks.
title: 'Align the hidden-unit permutation before averaging weights from separately trained networks'
version: 3
history:
- version: 2
  date: '2026-09-25'
  note: >-
    Adds the scope line this practice was missing: when does the alignment step
    NOT apply. Two papers filed today average weights without aligning anything,
    because their points share an optimization trajectory — SWA along one
    trajectory (LIT-673) and a fine-tuned model with its own initialization
    (LIT-674). The latter states the contrast in one sentence, reporting
    that averaging all layers of unrelated networks gives "no better accuracy
    than a randomly initialized neural network". That is the clearest statement
    of what this practice is for that the record holds, and it also bounds it.
    Recommendation, status and consensus unchanged.
- version: 3
  date: '2026-09-25'
  note: >-
    Adds the third shared-trajectory case, SOTA-tmpchosw, and with it the
    qualification that the scope boundary is a spectrum rather than a dichotomy.
    A shared initialization is not sufficient: the greedy soup recipe exists to
    "avoid adding in models which may lie in a different basin", which can happen
    when sweep members use high learning rates. So a shared start makes averaging
    usually safe, a per-ingredient check makes it reliably safe, and this
    practice's alignment is what is left for networks that share nothing.
    Recommendation, status and consensus unchanged.
tags:
- model-stability
date: '2026-09-15'
source:
# LIT-333 is primary: it supplies the algorithms and demonstrates the
# barrier closing, where LIT-251 establishes that permutation is what the
# barrier is made of.
- LIT-333
- LIT-251
introduced_by:
- LIT-251
implementations: []
summary: >-
  A neural network's hidden units can be permuted without changing the
  function, so two networks trained from different seeds sit in different
  corners of the same symmetry orbit. Averaging their weights directly
  averages across that mismatch and traverses a loss barrier that is mostly an
  artefact of labelling. Match the units first — by weight matching, or by
  activation matching on a handful of samples — and most of the barrier is not
  there.
explained_by:
- THEORY-010
---

# SOTA-217: Align the hidden-unit permutation before averaging weights from separately trained networks


## What to do

Before averaging or interpolating the weights of two networks that were
trained separately — different seeds, different shards, different workers
that have drifted apart — find the per-layer permutation of hidden units that
best matches one to the other, apply it, then average.

Two methods, from [LIT-333](../literature.d/LIT-333.md). **Weight matching** solves a linear assignment
problem per layer on the weights themselves. **Activation matching** correlates
unit activations on a small reference batch — one to four samples — and is
reported as nearly as good at much lower cost, which is what makes this
affordable inside a training loop rather than only at merge time.

This does not apply to averaging replicas that share an initialization and
have stayed synchronized, which is the ordinary data-parallel case. It applies
wherever the runs could have permuted independently.

## Why

**The barrier between independently trained networks is largely bookkeeping.**
[LIT-251](../literature.d/LIT-251.md)'s finding is that if the permutation symmetry is accounted for,
the loss barrier along the linear path between two SGD solutions is small —
the two networks are near each other in function space and far apart in
coordinates. [LIT-333](../literature.d/LIT-333.md) turns that from a conjecture into a procedure and
reports the barrier closing on real architectures.

**Every averaging scheme in the decentralized literature assumes it away.**
FedAvg averages client weights; local SGD averages worker weights; DiLoCo
averages deltas. All of them work, and all of them work because the workers
start from a common initialization and do not drift far enough to permute. The
practice matters exactly where that assumption weakens — long local phases,
heterogeneous data, workers restarted from different checkpoints — and the
literature in this record measures a penalty in those settings without naming
this as a candidate cause.

<!-- inactive-ok: THEORY-010 — Proposed, and this practice's own explanation -->
The account of why is [THEORY-010](../theory.d/THEORY-010.md).

## What this does not settle

**The demonstrations are checkpoint merging, not training.** Both papers
interpolate between two finished networks. Neither runs a distributed training
job with alignment in the averaging step and reports the wall-clock or quality
difference, which is what the promotion condition asks for.

**Cost inside a loop is unmeasured.** Activation matching on four samples is
cheap relative to a training step and not free, and it has to happen at every
averaging event. Nothing here says what that costs at scale.

**Vision architectures, moderate scale.** Whether transformer attention heads
present the same symmetry in the same way — they have more structure to match
and more of it is shared — is not covered by either paper.

## When the alignment step is unnecessary

This practice is about networks that were **trained separately**. If the weight
vectors you want to average share an optimization trajectory, there is no
permutation to undo and no alignment to run.

<!-- inactive-ok: SOTA-408 SOTA-407 SOTA-tmpchosw — Proposed or Active, and named as the cases this practice does not cover. What they do without alignment is the assertion, not their status. -->
Three such cases are filed here. [SOTA-408](SOTA-408.md) averages points visited along one
SGD trajectory. [SOTA-407](SOTA-407.md) interpolates a zero-shot model with the model
obtained by fine-tuning *from* it. [SOTA-tmpchosw](SOTA-tmpchosw.md) averages the members of a
fine-tuning sweep that all started from one pretrained checkpoint. None aligns
anything, and all three work.

The third is the one that shows the boundary is not a clean line. A shared
initialization is **not sufficient**: the greedy recipe exists because some sweep
members land where the average cannot use them, and its own justification is to
"avoid adding in models which may lie in a different basin of the error
landscape", which can happen "if, for example, models are fine-tuned with high
learning rates". So a shared starting point makes averaging *usually* safe and a
per-ingredient check is what makes it reliably safe. Between that and this
practice's alignment step there is a spectrum, not a dichotomy.

[LIT-674](../literature.d/LIT-674.md) puts the contrast in one sentence, which is worth having beside this
practice because it is also the sharpest argument *for* it:

> ensembling all layers—as we do when end-to-end fine-tuning—typically fails,
> achieving no better accuracy than a randomly initialized neural network.
> However, as similarly observed by previous work where part of the optimization
> trajectory is shared, we find that the zero-shot and fine-tuned models are
> connected by a linear path in weight-space along which accuracy remains high.

So the test before averaging is not "are these the same architecture" or "do
these solve the same task", but **did one of these weight vectors come from the
other**. If yes, average. If no, this practice applies and
<!-- inactive-ok: THEORY-010 — Proposed, and cited for the same reason it is cited above: it is the record's account of why the separately-trained case is hard. -->
[THEORY-010](../theory.d/THEORY-010.md) says why.
