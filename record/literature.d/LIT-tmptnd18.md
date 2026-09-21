---
status: Active
title: 'Introducing AI to an Online Petition Platform Changed Outputs but not Outcomes'
version: 1
tags:
- deployment-and-society
- analysis-and-evaluation
date: '2026-09-21'
published: '2025-11-01'
arxiv: '2511.13949'
first_author: 'Corpus'
keywords:
- 'ai-writing-tools'
- 'difference-in-differences'
- 'natural-experiment'
- 'homogenization'
- 'platform-effects'
implementations: []
summary: >-
  Corpus et al. (2025), [ARXIV-2511.13949](https://arxiv.org/abs/2511.13949). Change.org's "write with AI"
  tool reached the US, GB and Canada eleven weeks before Australia. Across
  1.5M petitions, access made petitions **49% longer**, more lexically varied,
  1.5 grades harder to read, and rated higher on quality and persuasiveness —
  moving them toward the profile of successful pre-AI petitions — while
  raising inter-petition similarity **23%** and leaving outcomes flat or
  worse. The features that used to predict success stopped predicting it.
---

<!-- inactive-ok-file: SOTA-172 — Proposed, and named to place this paper
     beside the record's synthetic-text homogenization line. The comparison is
     between what the two measured, which does not wait on either being
     settled -->

<!-- inactive-ok-file: SOTA-295 — Proposed, filed earlier the same day and
     cited for the same reason as SOTA-172: it measured collapse in generated
     text, this measures it in text people wrote holding a tool -->

<!-- inactive-ok-file: THEORY-tmp8vfb1 — Proposed, filed in this same
     contribution; named as the account this record files, with its
     unsettledness stated in the theory itself and in the practice -->

# LIT-tmptnd18: Introducing AI to an Online Petition Platform Changed Outputs but not Outcomes

Corpus et al. (2025) — [ARXIV-2511.13949](https://arxiv.org/abs/2511.13949)

## Key takeaways

- **A real natural experiment, which is rare here.** Change.org rolled its
  in-platform AI drafting tool out to the United States, Great Britain and
  Canada eleven weeks before Australia. The authors confirmed the launch dates
  with Change.org staff, verified parallel pre-trends, and analysed 1.5M
  petitions from 2022–2024. The analysis was **preregistered** on AsPredicted.
- **The treatment is *access*, not *use*, and that is a deliberate design
  choice worth taking on its own.** AI detectors are unreliable and biased, so
  defining the treatment as tool availability makes this an intention-to-treat
  estimate that needs no detector to be valid. Their own classifier suggests
  over half of petitions written with access were AI-generated, which sets the
  dilution.
- **Outputs moved a long way.** Median word count **+53.6 (49%)**, Flesch-
  Kincaid grade **+1.49 (19%)**, MATTR **+0.049 (6%)**, all at p < 0.001.
  Qualitatively: the commonest title verbs shifted from monosyllabic Old
  English ("stop", "let") to Latinate ("implement", "establish").
- **And they moved in the direction that used to mean success.** These three
  features were selected precisely because they predicted petition outcomes
  before the tool existed. Independent human raters also scored AI-access
  petitions higher on **writing quality** (Cohen's d = 0.96) and
  **persuasiveness** (d = 0.86). The text did not get worse.
- **Outcomes did not follow.** The share of petitions reaching 10 signatures
  fell **5.33 percentage points** (p = .001); the share reaching one comment
  in 30 days fell 2.51 points, not significant. Participation was flat — a
  Bayesian structural time series counterfactual puts the effect at −354 users
  (95% CrI [−2167, 1263]).
- **The interesting finding is in the appendix and stated once in the
  discussion:** after AI access, lexical features, writing quality and
  persuasiveness became **weaker or negative** predictors of outcomes. The
  proxy did not merely stop working; the relationship inverted.
- **Homogenization is the candidate mechanism.** Mean pairwise cosine
  similarity between petitions rose **0.056 on a 0.240 base — 23%**. This
  analysis was added *after* preregistration and the authors say so.
- **Triangulated rather than argued.** Difference-in-differences (static and
  dynamic), synthetic control with New Zealand and India, Bayesian structural
  time series, interrupted time series, and a within-writer analysis of 4,611
  repeat authors.
- **No benefit to low performers**, contradicting the prior literature the
  authors cite. Among writers whose first petition failed, no cohort with AI
  access did better on their second.
- **Three mechanisms proposed, none tested:** the substance did not improve
  ("AI slop"); readers grew suspicious of AI; authors felt less ownership and
  so promoted their petitions less. The third is the one the authors develop
  most, since off-platform promotion drives petition success.

## Standing in the anthology

The second group for [SOTA-291](../practices.d/SOTA-291.md), and the reason it moves to `Active`. That
practice asked for "a specific-affordance evaluation run at collective scale
with the group-level outcome actually measured", and this is exactly that
shape: one affordance (a drafting tool in one flow), a coherent counterfactual
(the staggered rollout), a long enough window, and outcomes measured **at the
platform level**. The authors reach the design from the same reasoning
independently, and say so — individual-level estimates on an interconnected
platform "may suffer from bias and require internal platform access", so they
estimate the effect of the intervention on the system instead.

It is also the record's first measured instance of a proxy being destroyed by
the tool that optimizes it, which is [THEORY-tmp8vfb1](../theory.d/THEORY-tmp8vfb1.md), and it puts a
human-in-the-loop case beside the record's synthetic-data homogenization line
— [SOTA-172](../practices.d/SOTA-172.md) and [SOTA-295](../practices.d/SOTA-295.md) both concern generated text collapsing
toward itself, and here the text is written by people holding a tool.
