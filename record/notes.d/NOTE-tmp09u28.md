---
status: Read
paper: LIT-tmpz0ivc
title: 'Informative and Actionable Social Media Research'
version: 1
date: '2026-09-21'
summary: >-
  Reading it: the power-grid example is the whole paper and it is worth the
  space. Treat too few substations and the grid absorbs it; treat enough and
  the controls black out too. Both give "no effect", both are wrong, and
  nothing about that argument is specific to social media.
---

# NOTE-tmp09u28: Informative and Actionable Social Media Research

## Contribution

A precise account of why a literature keeps failing to reach consensus, and a
replacement question. Before it, conflicting trial results looked like a
measurement problem to be solved with better trials. After it, they look like
what you should expect when the estimand and the estimate are different
quantities.

What is true afterwards that was not before: "individual-level RCT finds no
effect" has a known set of reasons to be uninformative, each nameable, rather
than a vague sense that complexity is hard.

## Key insight

**The power grid, run twice.** Randomize substations to demand spikes. Treat
few and the grid compensates — no difference. Treat many and the grid fails,
**including the controls** — no difference. The same null appears from
opposite sides of the real effect.

That single example carries non-linearity and SUTVA violation together, and it
transfers without modification to any system where units are coupled and the
aggregate has a threshold. It is the best short argument I have read for why a
clean experimental design can still answer the wrong question.

## Assumptions

- **The estimand of interest is collective and long-run** — polarization,
  mental-health trends, vaccine uptake. If your question genuinely is the
  individual short-run effect, the critique does not bind.
- **Social systems are complex in the technical sense**: interactions produce
  emergence, and estimates are not independent of the system's history or the
  moment of observation.
- **Recommendation algorithms learn from behaviour**, so the system under
  study changes during the study.
- **No new data.** This is a review; the four mechanisms are imported and the
  application is argued.

## Key results

Four named failure modes, each with a physical and a social illustration:

- **Non-linearity across scale** — global outcomes are not the sum of
  individual components. Power grid, both directions.
- **Hysteresis** — the system depends on its history, so removal is not the
  inverse of addition. Duolingo withdrawn for a week; fluency retained. "This
  problem of interpretation besets all withdrawal studies."
- **Feedback in time** — effects are non-monotonic and depend on when you
  look. Two-week smoking cessation would establish smoking as a way to lose
  weight and reduce irritability.
- **SUTVA violation** — units interact. Someone assigned a chronological feed
  still receives algorithmically-ranked content through their neighbours.
  Avoidable only by randomizing whole subnetworks, and **no existing trial
  does**.

The positive recommendation: evaluate specific interventions on specific
affordances, because the counterfactual is coherent, small treatments can run
longer than deactivation studies, and the answer maps to a decision. Evaluate
continuously, because effects are time- and state-dependent. Triangulate,
because no modality here is a gold standard.

## Claims

**Correct and not really contestable:** the SUTVA argument and the hysteresis
argument. Both are structural. A trial that violates SUTVA is not estimating
what its design says it estimates, and a withdrawal study assumes a symmetry
that path-dependent systems do not have.

**Reasoned and a judgement:** that such trials are therefore "bound to be of
limited value". How much value remains is not quantified for any specific
study, and a reader who wants individual-level trials for narrower estimands
is not answered.

**A recommendation rather than a finding:** the intervention-evaluation
programme. Argued from three advantages, not demonstrated.

## Method

Review and argument, organised around one worked physical analogy and four
mechanisms, with re-readings of published large-scale experiments.

## Concepts

*Estimand* versus estimated quantity; *hysteresis* and path-dependence;
*SUTVA*; the distinction between net-effect questions and
specific-affordance questions; continuous rather than one-shot evaluation.

## Connections

- [SOTA-200](../practices.d/SOTA-200.md) and [SOTA-278](../practices.d/SOTA-278.md) are the same concern aimed at models:
  a measurement can fail to be about the thing you care about, and the failure
  is structural rather than noisy. This is that concern aimed at deployed
  systems, and the mechanisms are different — metric deformation there,
  estimand mismatch here.
- [LIT-tmpvcocw](../literature.d/LIT-tmpvcocw.md), filed alongside, finds that industry-tied research
  is sparse in exactly the platform-dynamics cluster this paper says the
  effects live in. Same first author, so not an independent corroboration —
  but the two halves fit.
- The record's `analysis-and-evaluation` practices are all about models under
  test. This is the first material it holds about systems under deployment,
  which is what `ADR-052` made room for.

## Bearing on the record

One account and one practice, both general beyond the domain. The argument is
about randomizing individuals and asking about collectives; it applies to any
deployed system whose users interact, which is most of them.

What should not be taken from it is "RCTs are bad". The paper's claim is about
a mismatch between a design and an estimand, and it names the conditions under
which the mismatch bites.

## Limitations

**No measurement of the size of any distortion.** The mechanisms are real and
their magnitude in any published study is not estimated. That is the gap
between "this design cannot cleanly identify the effect" and "this specific
published null is wrong".

**The positive programme is untested.** Evaluating specific affordances
continuously is a good argument and not yet a demonstrated one; the paper
notes that two Facebook studies did test realistic ranking interventions but
did not assess collective outcomes.

**Shared authorship with its companion.** Filed as a pair, same first author,
complementary halves. Not two groups agreeing.

## Open questions

- Does anything in the ML-evaluation literature have this structure? An
  offline benchmark is an individual-level measurement of a system that will
  be deployed into a population that interacts — the estimand mismatch may not
  stop at social media.
- Is there a case where randomizing whole subnetworks has been done? The paper
  says none exists in this literature; if one exists elsewhere, its cost is
  the number that decides whether the prescription is practical.
