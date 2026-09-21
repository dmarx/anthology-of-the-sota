---
status: Proposed
promote_when: >-
  A second deployment where a text-quality proxy and the outcome it was chosen
  to stand for are both tracked across the rollout and diverge — on a platform
  that is not a petition site, since petition success runs through
  off-platform promotion and that is the channel the rival explanations use.
  What would not move it: a study showing an assistant improved text and
  reporting no outcome measurement, which is the situation this practice
  exists to prevent rather than evidence about it.
consensus: unreplicated
consensus_note: >-
  One platform, one tool, eleven weeks — and an unusually clean natural
  experiment for this kind of question, preregistered and triangulated four
  ways. The underlying worry is old and widely believed; what is new and
  unreplicated is a causal measurement of the proxy and the outcome moving
  apart in the same deployment.
title: 'Measure a writing assistant by the outcome it was deployed to improve, not by the text features that used to predict it'
version: 1
tags:
- deployment-and-society
- analysis-and-evaluation
date: '2026-09-21'
source:
- LIT-tmptnd18
introduced_by:
- LIT-tmptnd18
implementations: []
explained_by:
- THEORY-tmp8vfb1
summary: >-
  Corpus et al. (2025), [LIT-tmptnd18](../literature.d/LIT-tmptnd18.md) — Change.org's AI drafting tool made
  petitions 49% longer, more lexically varied and better rated by human judges
  on quality and persuasiveness, moving them toward the profile of successful
  pre-AI petitions. The share reaching 10 signatures fell **5.33 points**. The
  features had been chosen because they predicted success; afterwards they
  predicted it weakly or negatively.
---

<!-- inactive-ok-file: THEORY-tmp8vfb1 — Proposed, filed in this same
     contribution, and the sentence citing it says so and says the practice
     does not depend on it: all three candidate mechanisms imply the same
     recommendation -->

# SOTA-tmpivc72: Measure a writing assistant by the outcome it was deployed to improve, not by the text features that used to predict it

## Source

Corpus et al. (2025), [LIT-tmptnd18](../literature.d/LIT-tmptnd18.md) — [ARXIV-2511.13949](https://arxiv.org/abs/2511.13949) — read as
[NOTE-tmpge2ux](../notes.d/NOTE-tmpge2ux.md).

## What to do

If you ship a writing assistant to improve some outcome — conversions,
signatures, replies, acceptance, engagement — instrument **that outcome**
across the rollout, and keep instrumenting it. Text-quality measures, judge
scores and human ratings are worth collecting and are not substitutes, however
well they correlated before you shipped.

And if you can, **stagger the rollout** so there is something to compare
against. The entire strength of the source is that one region got the tool
eleven weeks later than the others.

## Why the obvious shortcut fails

The shortcut is reasonable and it is what a careful team would do. Find the
text features that predict the outcome. Ship a tool that produces text with
those features. Verify the text has them. Declare success.

Every step of that worked on Change.org, and the outcome went the other way.

- The features — lexical diversity, readability, length — were chosen
  *because* of their strong predictive relationship to petition outcomes
  before the tool existed.
- The tool moved all three decisively: **+49% length**, **+1.49 reading
  grades**, **+6% MATTR**, all p < 0.001.
- Independent human raters confirmed it was not a hollow shift: writing
  quality **d = 0.96**, persuasiveness **d = 0.86**. The text was genuinely
  better.
- The share of petitions reaching ten signatures fell **5.33 percentage
  points** (p = .001). The share getting a comment within 30 days fell 2.51
  points, not significant. Participation was flat.
- Afterwards, those features — and the rated quality and persuasiveness —
  became **weaker or negative** predictors of outcomes.

[THEORY-tmp8vfb1](../theory.d/THEORY-tmp8vfb1.md) is the account this record files for why, and it is
`Proposed` because two rival explanations predict the same null. But the
practice does not depend on which explanation is right: under all three, the
proxy stopped tracking the outcome, and only the outcome would have told you.

## The corollary about A/B-testing your own tool

Watch what the design does to the comparison. If you ship the assistant to
everyone at once and compare against last quarter, you will see better text
and you will have no counterfactual. If you compare users who used the tool
against users who did not, you have selection. The source's answer —
**treat access as the treatment, not use** — is worth copying: AI detection
is unreliable, so an intention-to-treat estimate over a staggered rollout
needs no detector to be valid. It dilutes the effect by whatever fraction
adopts, which is a price worth paying for an estimate that means something.

## Conditions

**One platform, one tool, eleven weeks.** And petition success runs heavily
through **off-platform promotion**, which is exactly the channel two of the
three proposed mechanisms use, so this may be the setting where the effect is
strongest rather than a typical one.

**Few clusters.** Three treated countries and one control, with inference on
17 degrees of freedom; few-cluster difference-in-differences standard errors
run anti-conservative. The synthetic control with New Zealand and India
mitigates this rather than resolving it.

**The outcomes are floors** — ten signatures, one comment. The study measures
getting off the ground, not succeeding, and the authors argue well for that
choice on a platform spanning hyper-local and global causes.

**The within-writer analysis does not add as much as it appears to.** Repeat
writers' second petitions did worse in every cohort, including those with no
AI access, and the *largest* decline was among writers who had access for
both petitions. Read it as a consistency check that failed to contradict the
main result, not as an individual-level confirmation of it.

**The scope is rivalrous outcomes.** This concerns settings where the
population competes for something scarce — attention, signatures, a slot.
Where the outcome is not rivalrous, an assistant that improves everyone's
draft may simply improve everyone's results, and nothing here argues
otherwise.

**No harm was demonstrated to the writing itself.** The finding is not that
AI-assisted text is worse. It was better and it did not help, which is a
stranger and more useful result.
