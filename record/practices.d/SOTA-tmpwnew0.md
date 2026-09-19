---
status: Active
consensus: unreplicated
consensus_note: >-
  One paper. The record holds no second instance of the pattern, and the
  claim is about how a system is factored rather than about a measured
  quantity — which is worth watching rather than discounting, since the
  same factoring shows up wherever a model is asked to memorise instances.
title: 'Add a new instance by reconstructing it, not by training on it'
version: 1
tags:
- vision-and-graphics
- model-architecture
date: '2026-09-19'
source:
- LIT-111
introduced_by:
- LIT-111
implementations:
- OnePose
summary: >-
  Sun et al. (2022), [LIT-111](../literature.d/LIT-111.md) — [ARXIV-2205.12257](https://arxiv.org/abs/2205.12257). Split what the
  system knows about a specific object from what it has learned in general.
  Build the object's structure once by reconstruction; match against it with a
  network that never saw the object or its category. Adding an object is then
  a scan, not a training run.
---

# SOTA-tmpwnew0: Add a new instance by reconstructing it, not by training on it

## Source

Sun et al. (2022), [LIT-111](../literature.d/LIT-111.md) — [ARXIV-2205.12257](https://arxiv.org/abs/2205.12257).

## The rule

Two kinds of knowledge get conflated whenever a model is asked to handle a
specific thing: **what is true of this instance** and **what is true in
general**. Factor them.

The instance's structure is built once by reconstruction — in the source's
case an SfM point cloud from a scanned video. The general capability is a
network that matches 2D interest points to 3D points and *"can handle objects
in arbitrary categories without instance- or category-specific network
training"*.

**The operational consequence is the point of the practice.** Supporting a new
object becomes a scan rather than a training run: no labels for it, no
fine-tune, no risk to anything the network already does. "One-shot" here
means one *construction*, not one example.

## When it applies

- **When the instance has stable structure that can be reconstructed.** A
  rigid object does; a deformable or featureless one does not
- **When the set of instances grows after deployment.** If the instance set is
  fixed and known at training time, the factoring buys nothing
- **When retraining is the expensive part** — because a team cannot retrain,
  or because retraining risks regressions elsewhere

## Why it is filed outside its domain's frame

The source is an object-pose paper and the recommendation is not about pose.
It is about where instance knowledge lives, and the same question is asked
whenever a system is expected to know about particular entities: retrieval
against an index instead of memorisation in weights is the same factoring,
reached from a different direction.

Filed under `ADR-026`'s rule — the claim takes its kind rather than the domain
it was discovered in — and `model-architecture` is its second tag for that
reason.

## Conditions

- **One paper, no replication in this record.** See `consensus_note`
- **Reconstruction quality bounds it.** The matcher can only be as good as the
  point cloud, and the paper's setting is a scanned video under reasonable
  conditions
- **The generic matcher is doing real work**, and is the part that would need
  re-training if the *class* of instances changed rather than the instance
