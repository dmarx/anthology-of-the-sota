---
status: Read
paper: LIT-tmptnd18
title: 'AI on Change.org'
version: 1
date: '2026-09-21'
summary: >-
  Read to test it against `SOTA-291`'s promotion condition, which it satisfies.
  The platform-level difference-in-differences is the strong evidence; the
  repeat-writer analysis reads stronger than it is; and the finding with the
  longest reach — that the text features stopped predicting outcomes — is in
  the appendix.
---

<!-- inactive-ok-file: SOTA-172 — Proposed, cited in Connections to contrast
     two causal paths to the same statistical place -->

<!-- inactive-ok-file: SOTA-295 — Proposed, cited alongside SOTA-172 for the
     same contrast -->

<!-- inactive-ok-file: SOTA-292 — Proposed, and applied rather than relied on:
     this reading runs its check against the present paper and reports the
     result. A practice being unsettled does not stop it being usable -->

# NOTE-tmpge2ux: AI on Change.org

## Contribution

A causal estimate of what happens when a platform puts an AI drafting tool
into its own writing flow, from a natural experiment rather than a survey or
a lab study. Before this, the literature had off-platform AI use, which is
hard to detect and idiosyncratic in how it is invoked; here the usage runs
through one model, one backend prompt and one interface, and the rollout was
staggered by country.

What is true afterwards that was not before: an AI writing tool can make text
substantially better by every measure that used to matter and leave the thing
the text was for **unchanged or worse**, at scale, causally, on a real
platform.

## Key insight

**The features were chosen because they predicted success, and after the tool
they stopped predicting it.**

That sentence is the paper, and it is not the sentence in the abstract.
Lexical diversity, readability and length were selected as outcome variables
*because* they had a strong predictive relationship to petition outcomes
before the tool existed. The tool pushed all three in the successful
direction, and human raters confirmed the text really was better written and
more persuasive. Outcomes went flat-to-down. And then — in the appendix —
the predictive strength of those features, and of rated quality and
persuasiveness, is reported as having **weakened or reversed**.

So the correct reading is not "AI writing did not help". It is that the
measurement the platform would have used to tell whether it helped was
destroyed by the thing it was measuring.

## Assumptions

- **Parallel trends**, verified pre-period and observed to resume after all
  countries had access.
- **Treatment = access, not use.** An intention-to-treat estimate. Their
  classifier puts AI-generated content at over half of petitions written with
  access, which sets how much the true per-user effect is diluted.
- **Off-platform AI use is assumed similar across countries**, so it
  differences out. Supported by pre-period detection rates being similar, not
  proven.
- **Minimum thresholds as outcomes** — 10 signatures, one comment in 30 days
  — rather than raw counts, on the argument that Change.org spans
  hyper-local and global causes and raw engagement would weight by community
  size.
- Australia is the control; New Zealand and India enter through a synthetic
  control robustness check.

## Key results

- **Lexical:** word count +53.63 (49% over a 110-word base), FKGL +1.49
  grades (19% over grade 8), MATTR +0.049 (6% over 0.8). All p < 0.001.
- **Homogeneity:** mean pairwise cosine similarity +0.056 on a 0.240 base,
  **+23%**, p < 0.001. Not preregistered; the authors flag it as an
  augmentation.
- **Outcomes:** 10-signature share **−5.33 pp** (95% CI [−8.21, −2.45],
  p = .001); one-comment-in-30-days share −2.51 pp (95% CI [−6.36, 1.34],
  p = .187, not significant).
- **Quality went up, not down:** writing quality d = 0.96, persuasiveness
  d = 0.86, both p < 0.001, by independent raters.
- **Participation flat:** BSTS counterfactual, −354 users (s.d. 901), 95%
  CrI [−2167, 1263].
- **Repeat writers (N = 4,611):** Pre/Post cohort's second petitions 39%
  longer and at 25% lower odds of a positive outcome (OR = 0.754).
- **No low-performer benefit**, against the cited prior literature.

## Claims

**Well supported:** that access to the tool changed the text, a lot, in the
direction of the previously-successful profile, and that platform-level
outcomes did not improve. Preregistered, parallel trends checked,
triangulated four ways, and the effect sizes are large relative to their
intervals.

**Well supported and the most useful thing here:** that the text was
genuinely better. Without the human-rater result, "outcomes did not improve"
would be explained by the tool simply being bad, and the paper would be much
less interesting. The raters close that door.

**Reported once, in an appendix, and carrying the most weight of anything in
the paper:** that the predictive relationship between text features and
outcomes weakened or reversed. Everything that makes this a general lesson
rather than a fact about petitions rests on it, and it is not in the abstract,
not preregistered, and given a sentence.

**Weaker than its prose suggests — the repeat-writer analysis.** The paper
says the decline in second-petition outcomes "was greater when users had AI
access for their second petition". The three cohorts' odds ratios are
Pre/Pre 0.825 (ns), Pre/Post 0.754 (p < .001), Post/Post **0.662**
(p < .001). The largest decline is in the cohort that had access for *both*
petitions, so "gaining access" is not what separates them, and the three
confidence intervals overlap heavily — Pre/Pre [0.648, 1.050] contains both
other point estimates. The honest reading is that all repeat writers decline,
consistent with the regression to the mean the authors themselves name, and
this analysis does not isolate an AI effect. It is a consistency check that
did not contradict the main result, which is worth something and is less than
it reads as.

**Explicitly untested:** all three proposed mechanisms — thin substance,
reader suspicion of AI, and diminished author ownership reducing off-platform
promotion. The third is the most developed and the most plausible given that
promotion drives petition success, and the paper offers no evidence for it.

## Method

Difference-in-differences, static and dynamic, on weekly country-level series
over an eleven-week window of differential access, with a 65-week pre-period.
Synthetic control, Bayesian structural time series and interrupted time
series as robustness. Human rating of quality and persuasiveness. A
mixed-effects within-writer analysis of repeat authors.

## Connections

- [SOTA-291](../practices.d/SOTA-291.md) — evaluate a specific intervention on a specific
  affordance and measure the group-level outcome. This is the second group
  and the design its promotion condition named; it moves to `Active` on it.
- [THEORY-048](../theory.d/THEORY-048.md) — individual randomization estimates an individual
  quantity and the collective effect is not its sum. The authors reach the
  same conclusion independently, in their limitations, as their reason for
  not estimating individual effects at all.
- [SOTA-172](../practices.d/SOTA-172.md) and [SOTA-295](../practices.d/SOTA-295.md) are the record's synthetic-text
  homogenization line — generated corpora collapsing toward themselves,
  measured by n-gram over-concentration. This is the same collapse measured by
  embedding similarity, in text written by **people using a tool**, which is a
  different causal path to the same statistical place.
- [SOTA-292](../practices.d/SOTA-292.md) — check industry ties when reading this literature. Worth
  applying here and it comes out clean: the authors are academics, they
  obtained launch dates from Change.org staff, used only publicly accessible
  data, and the conclusion is unflattering to the platform.

## Bearing on the record

It promotes `SOTA-291`, which is the outcome a `promote_when` exists to
produce, and it does so from a genuinely independent direction — different
group, different platform, different intervention, and the design arrived at
by the same reasoning rather than by following the source.

It also supplies a practice and a theory of its own about proxy collapse,
which is a claim the record has had no instance of.

## Limitations

**Four countries is few clusters.** Three treated and one control, with
inference on 17 degrees of freedom from weekly observations. Few-cluster
difference-in-differences standard errors are anti-conservative, and the
synthetic control with two extra countries mitigates this rather than
resolving it.

**Eleven weeks.** Long enough to see the lexical shift, short for anything
that propagates through a community, and the homogenization trend was still
moving at the end of the window.

**Access, not use, dilutes everything.** If half of petitions with access used
the tool, the per-user effect is roughly twice the reported one — which makes
the outcome null *stronger* and the "did not help" reading safer, but it also
means no number here describes what happens to a person who uses it.

**The outcome metrics are floors.** One comment, ten signatures. A petition
that would have got 500 signatures and got 400 is invisible. The authors
justify the choice well and it still means the study measures getting off the
ground, not succeeding.

**Publicly accessible data only**, so platform amplification (home-page
features) and off-platform amplification (social ranking) are unobserved.

## Open questions

- Which of the three mechanisms is it? Author ownership is testable — does
  AI-assisted petition writing reduce off-platform sharing? — and nobody has.
- Does the proxy inversion recover? If it is a novelty effect in readers it
  should decay; if it is homogenization it should not.
- Would friction in the writing flow restore the effect? The authors suggest
  requiring longer input or forcing an edit pass, and this is a concrete,
  cheap, A/B-testable design change nobody has run.
