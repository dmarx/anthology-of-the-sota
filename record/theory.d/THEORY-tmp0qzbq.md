---
status: Proposed
promote_when: >-
  The no-follow-is-most-diverse ordering measured on a second platform, by a
  group unconnected to this one. That would make "personalization
  concentrates" a property of the class rather than of one ranking system in
  one six-week window. A further measurement of Twitter/X, or a repeat of the
  same arms on the same platform, is not it.
title: 'Personalizing a feed concentrates what it shows rather than broadening it, and a handful of moderate signals is enough to start'
version: 1
tags:
- deployment-and-society
- analysis-and-evaluation
date: '2026-09-21'
source:
- LIT-tmpq6fna
explains:
- SOTA-tmpxtcgk
summary: >-
  Ye, Luceri and Ferrara (2024), [LIT-tmpq6fna](../literature.d/LIT-tmpq6fna.md) — across four arms of
  an audit, the accounts following **nobody** receive the most diverse
  recommendations and the partisan arms the least. Ten moderate media follows
  and four political accounts are enough to amplify aligned voices more than
  50% above a balanced baseline.
---

<!-- inactive-ok-file: SOTA-tmpxtcgk — Proposed, and the practice this account
     explains; naming it in the `explains` table is the relation, not a claim that
     either is settled -->

# THEORY-tmp0qzbq: Personalizing a feed concentrates what it shows rather than broadening it, and a handful of moderate signals is enough to start

## Source

Ye, Luceri and Ferrara (2024), [LIT-tmpq6fna](../literature.d/LIT-tmpq6fna.md) — read as
[NOTE-tmpz4t8g](../notes.d/NOTE-tmpz4t8g.md).

## What it explains

| practice | what it says to do | what this says it is |
|---|---|---|
| [SOTA-tmpxtcgk](../practices.d/SOTA-tmpxtcgk.md) | include an arm that follows nobody | not a control that reports the null, but the arm that carries the finding — the ordering across arms is the measurement |

## The account

The audit ran four arms: accounts following nobody, accounts following ten
moderate-to-strong media outlets and four political figures on the left, the
same on the right, and a balanced set. Concentration of exposure was measured
by Gini coefficient over the accounts appearing in each timeline.

Every arm is concentrated — Gini above 0.45 throughout, comparable to
published figures of 0.6–0.7 for exposure to one's own friends. The ordering
is the result:

**right-leaning most concentrated > balanced > left-leaning > following
nobody, least concentrated of all.**

All pairwise differences significant at p < 0.001.

So the arm with no personalization signal at all sees the widest range of
sources, and every arm that supplies a signal sees a narrower one. The
direction is the opposite of the intuition that a recommender broadens what
you would otherwise have found: on this measurement personalization is a
narrowing operation, and the baseline it narrows from is the untargeted feed.

**And the amount of signal required is small.** The partisan arms follow ten
media outlets — seven of them moderate — and four political accounts. That is
enough for the top aligned voices to run more than 50% above the balanced
baseline. No interaction, no clicks, no history: only the follows, and only a
fortnight of them before the measurement window.

The source's own reading is that once a new user follows a few partisan
accounts, their recommendations fill with like-minded voices quickly. The
measurement supports the speed as well as the direction, because the arms had
no time to accumulate behaviour — there was none to accumulate.

## Why `Proposed`

**One platform, one six-week window, one election.** The ordering is clean and
significant and it is a photograph. A ranking system is changed continuously,
and this one was changed by its owner during the period it was measured.

**The mechanism for the neutral arm is offered, not tested.** Cold start is
the explanation given for why accounts following nobody see the most diverse
timeline — plausible, and an interpretation. A different explanation, that
untargeted feeds are simply drawn from a broader popularity pool, would
predict the same ordering.

**And the control arm is not clean**, which the source says about its own
design: accounts following nobody still receive trending topics and platform
defaults. The arm that anchors the ordering is the one with a known confound.

The promotion condition therefore asks for a second platform rather than more
of this one. If the ordering holds elsewhere, "personalization concentrates"
is a property of the class; if it does not, it is a fact about Twitter/X in
late 2024.

## What this does not say

**It does not say concentration is caused by personalization.** The arms
differ in what they follow, and following a set of accounts changes both the
personalization signal and the candidate pool. Untangling those needs an arm
that follows many accounts chosen to be uninformative, which was not run.

**It does not say the concentration is harmful.** A concentrated feed of
things a reader wants is a working recommender by most operators' definition.
What the measurement establishes is the direction and the magnitude, and the
record files that without the evaluative step.

**It does not carry the partisan asymmetries.** The finding that default
timelines skew right, and that left-arm amplification is slightly larger in
magnitude, rests on hand-assigned political leanings the authors describe as
possibly inaccurate or stale. That is a separate claim with a separate
evidential basis, and this account does not depend on it.
