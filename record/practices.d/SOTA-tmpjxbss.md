---
status: Proposed
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
version: 1
tags:
- model-stability
date: '2026-09-15'
source:
# LIT-tmprg45v is primary: it supplies the algorithms and demonstrates the
# barrier closing, where LIT-tmp2m8yx establishes that permutation is what the
# barrier is made of.
- LIT-tmprg45v
- LIT-tmp2m8yx
introduced_by:
- LIT-tmp2m8yx
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
- THEORY-tmpgtvl1
---

# SOTA-tmpjxbss: Align the hidden-unit permutation before averaging weights from separately trained networks

## What to do

Before averaging or interpolating the weights of two networks that were
trained separately — different seeds, different shards, different workers
that have drifted apart — find the per-layer permutation of hidden units that
best matches one to the other, apply it, then average.

Two methods, from [LIT-tmprg45v](../literature.d/LIT-tmprg45v.md). **Weight matching** solves a linear assignment
problem per layer on the weights themselves. **Activation matching** correlates
unit activations on a small reference batch — one to four samples — and is
reported as nearly as good at much lower cost, which is what makes this
affordable inside a training loop rather than only at merge time.

This does not apply to averaging replicas that share an initialization and
have stayed synchronized, which is the ordinary data-parallel case. It applies
wherever the runs could have permuted independently.

## Why

**The barrier between independently trained networks is largely bookkeeping.**
[LIT-tmp2m8yx](../literature.d/LIT-tmp2m8yx.md)'s finding is that if the permutation symmetry is accounted for,
the loss barrier along the linear path between two SGD solutions is small —
the two networks are near each other in function space and far apart in
coordinates. [LIT-tmprg45v](../literature.d/LIT-tmprg45v.md) turns that from a conjecture into a procedure and
reports the barrier closing on real architectures.

**Every averaging scheme in the decentralized literature assumes it away.**
FedAvg averages client weights; local SGD averages worker weights; DiLoCo
averages deltas. All of them work, and all of them work because the workers
start from a common initialization and do not drift far enough to permute. The
practice matters exactly where that assumption weakens — long local phases,
heterogeneous data, workers restarted from different checkpoints — and the
literature in this record measures a penalty in those settings without naming
this as a candidate cause.

<!-- inactive-ok: THEORY-tmpgtvl1 — Proposed, and this practice's own explanation -->
The account of why is [THEORY-tmpgtvl1](../theory.d/THEORY-tmpgtvl1.md).

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
