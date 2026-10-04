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
  supplied the algorithms and closed it on real networks wide enough to
  allow it.
title: 'Align the hidden-unit permutation before averaging weights from separately trained networks'
version: 4
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
    Adds the third shared-trajectory case, SOTA-409, and with it the
    qualification that the scope boundary is a spectrum rather than a dichotomy.
    A shared initialization is not sufficient: the greedy soup recipe exists to
    "avoid adding in models which may lie in a different basin", which can happen
    when sweep members use high learning rates. So a shared start makes averaging
    usually safe, a per-ingredient check makes it reliably safe, and this
    practice's alignment is what is left for networks that share nothing.
    Recommendation, status and consensus unchanged.
- version: 4
  date: '2026-10-03'
  note: >-
    Corrected after LIT-251 and LIT-333 were re-read against their texts. The
    claim that activation matching on "one to four samples" is nearly as good
    as weight matching "at much lower cost" was backwards, and it appeared in
    the summary, What to do and What this does not settle. In LIT-333,
    activation matching uses activations over the training data (§3.1).
    Weight matching is the fast, data-free method: the two "perform
    similarly, although weight matching is orders of magnitude faster and
    does not rely on the input data distribution" (Figure 2). Its measured
    cost is 3 s to 194 s per merge on one V100 (A.5). LIT-251 is reworded
    from a finding to the conjecture it states (§1, §3.2). Its own search did
    not reduce the barrier for VGG or ResNet (§4). A width condition is
    added: zero barrier needs large width. 1× models "did not seem to exhibit
    linear mode connectivity" (LIT-333 §5.3), and on ImageNet a barrier
    remains after a 67% reduction (§5.1). Recommendation, status, consensus
    and introduced_by unchanged.
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
  artefact of labelling. Match the units first — by weight matching, which
  needs no data and takes seconds to minutes — and for wide enough networks
  the barrier is gone. At standard width, and on ImageNet, it shrinks but
  does not vanish.
explained_by:
- THEORY-010
---

# SOTA-217: Align the hidden-unit permutation before averaging weights from separately trained networks


## What to do

Before averaging or interpolating the weights of two networks that were
trained separately — different seeds, different shards, different workers
that have drifted apart — find the per-layer permutation of hidden units that
best matches one to the other, apply it, then average.

Two methods, from [LIT-333](../literature.d/LIT-333.md). **Weight matching** works on the weights
themselves. It is coordinate descent over all layers, each step a linear
assignment problem, repeated until no permutation changes. It needs no data
and took 3 s to 194 s per merge on one V100 (A.5). Run it to convergence: A.7
shows that a single greedy pass over the layers collapses an ImageNet merge
from 51.01% to about 7% top-1. **Activation matching** solves the same kind
of assignment on unit activations over the training data. It "perform[s]
similarly" to weight matching but is orders of magnitude slower and needs the
data (Figure 2). Weight matching is the method that could be affordable
inside a training loop, and federated settings that cannot share data
need it.

Expect the barrier to vanish only for networks wide enough. In [LIT-333](../literature.d/LIT-333.md), 1×
models "did not seem to exhibit linear mode connectivity", and wider ones
reached zero barrier (§5.3, Figure 4). On ImageNet, ResNet50 at 1× width kept
a barrier after a 67% reduction (§5.1). At ordinary width, alignment makes
averaging much less bad. It does not make it free.

This does not apply to averaging replicas that share an initialization and
have stayed synchronized, which is the ordinary data-parallel case. It applies
wherever the runs could have permuted independently.

## Why

**The barrier between independently trained networks is largely bookkeeping.**
[LIT-251](../literature.d/LIT-251.md) first stated this, as a conjecture. It proposes that if the
permutation symmetry is accounted for, there will likely be no barrier along
the linear path between two SGD solutions, and that the permutation could
then be used "to do weight averaging and build ensembles more efficiently"
(§5). Its evidence is indirect: barriers between independently trained
networks look like barriers between random permutations of one network. Its
own permutation search did not reduce the barrier for VGG or ResNet.
[LIT-333](../literature.d/LIT-333.md) turns the conjecture into a procedure and reports the barrier
closing on real architectures. It reaches zero on MNIST and for wide ResNet20
on CIFAR-10, but not at 1× width or on ImageNet.

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
interpolate between finished networks. [LIT-333](../literature.d/LIT-333.md)'s MergeMany merges up to 32
at once, but still after training. Neither runs a distributed training job
with alignment in the averaging step and reports the wall-clock or quality
difference, which is what the promotion condition asks for.

**Cost inside a loop is unmeasured.** Weight matching's one-off cost is
measured: 3 s for an MLP, 33 s for ResNet50 and 194 s for a 32×-wide
ResNet20 on one V100 ([LIT-333](../literature.d/LIT-333.md) A.5). That is cheap for a merge and not free
at every averaging event. Nothing here says what it costs per event at
scale.

**Standard width is where it works least.** The zero-barrier results are at
large width. At 1× width the barrier after alignment does not reach zero,
and on ImageNet a barrier remains ([LIT-333](../literature.d/LIT-333.md) §5.1, §5.3). How much of the
penalty alignment would remove at the widths distributed training actually
uses is not shown.

**Vision architectures, moderate scale.** Whether transformer attention heads
present the same symmetry in the same way — they have more structure to match
and more of it is shared — is not covered by either paper.

## When the alignment step is unnecessary

This practice is about networks that were **trained separately**. If the weight
vectors you want to average share an optimization trajectory, there is no
permutation to undo and no alignment to run.

<!-- inactive-ok: SOTA-408 SOTA-407 SOTA-409 — Proposed or Active, and named as the cases this practice does not cover. What they do without alignment is the assertion, not their status. -->
Three such cases are filed here. [SOTA-408](SOTA-408.md) averages points visited along one
SGD trajectory. [SOTA-407](SOTA-407.md) interpolates a zero-shot model with the model
obtained by fine-tuning *from* it. [SOTA-409](SOTA-409.md) averages the members of a
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
