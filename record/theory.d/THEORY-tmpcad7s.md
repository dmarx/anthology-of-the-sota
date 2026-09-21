---
status: Proposed
promote_when: >-
  The opportunity-cost channel identified against its rivals in a real
  deployment, not just observed alongside them: a population of producers
  given a time-saving tool whose phase can be attributed, with per-item
  effort and the fraction of started work that ships both measured, moving in
  the directions that phase predicts — and in particular one case where
  thoroughness goes **up**, since that is the prediction no rival account
  makes. What would not move it: more output at lower quality after any tool.
  That is the observation this is one of several accounts of, and dilution of
  the marginal producer, reader-side effects and simple skill loss all predict
  it too.
title: "A producer's own rate of return is the price of their time, so making them faster raises the bar on every marginal hour of improvement"
version: 1
tags:
- deployment-and-society
- analysis-and-evaluation
date: '2026-09-21'
source:
- LIT-tmpfa3d0
explains:
- SOTA-tmpri5k6
summary: >-
  Duede, Gross, Crockett and Bergstrom (2026), [LIT-tmpfa3d0](../literature.d/LIT-tmpfa3d0.md) — in a
  marginal-value-theorem model of effort allocation, the long-run rate of
  return is simultaneously the objective and the opportunity cost of the
  marginal hour. Any acceleration raises it, so the marginal hour of
  improvement has to clear a higher bar. Whether quality then falls is a race
  between that bar and the value of the hour, which is why the sign depends on
  **which phase** was accelerated rather than on how much time was saved.
---

<!-- inactive-ok-file: SOTA-tmpri5k6 — Proposed, filed in this same
     contribution; this theory declares `explains:` on it, so the citation is
     the relation itself -->

<!-- inactive-ok-file: THEORY-051 — Proposed, cited in "what this does not
     say" precisely to record that the two accounts are rivals and neither is
     settled -->

# THEORY-tmpcad7s: A producer's own rate of return is the price of their time, so making them faster raises the bar on every marginal hour of improvement

## Source

Duede, Gross, Crockett and Bergstrom (2026),
[LIT-tmpfa3d0](../literature.d/LIT-tmpfa3d0.md) — read as [NOTE-tmpcr9xy](../notes.d/NOTE-tmpcr9xy.md).

## What it explains

| practice | what it says to do | what this says it is |
|---|---|---|
| [SOTA-tmpri5k6](../practices.d/SOTA-tmpri5k6.md) | attribute the phase a tool accelerates before predicting its effect on quality | not a caveat about tool quality but a consequence of the producer re-optimizing against a price that the tool itself moved |

## The account

Consider anyone who works through a queue of items of varying value: they
spend a fixed period finding out what an item is worth, then decide whether to
finish it, then choose how much to invest beyond the minimum that makes it
shippable. Their payoff over the long haul is a rate — total value produced
divided by total time — and the optimal policy maximizes that rate.

The structural fact is that **this rate is also the shadow price of an hour**.
An hour spent improving the item in hand is an hour not spent starting the
next one, and the next one is worth the rate. So the policy is: keep improving
until the marginal value of another hour falls to the rate, then stop. That is
Charnov's marginal value theorem, and nothing about it is specific to science
or to language models.

Now give this producer a tool that makes some part of the work faster. The
rate goes up — that is what the tool is for. But the rate is the price of an
hour, so the bar every marginal hour of improvement must clear goes up with
it. This is the whole mechanism, and it does not require the tool to be
inaccurate, to homogenize anything, or to be used badly. It requires only that
the producer is choosing.

**The sign of the effect on quality is a race, and the race is won by phase.**

- Accelerate the *finding out what it is worth* phase and the marginal hour of
  improvement is unchanged in value while the bar rose. Improvement falls. And
  because starting over got cheaper, the threshold for bothering at all rises:
  **fewer items finished, each less finished**.
- Accelerate the *minimum needed to ship* phase and improvement falls for the
  same reason, but the threshold moves the other way — the cheapest possible
  item is now cheap enough to be worth doing. **More items finished, each less
  finished.** These two are not variations of one prediction; they have
  opposite signs on the first quantity.
- Accelerate *improvement itself* and the marginal hour is worth more, by the
  same factor that raised the rate and then some. This one **raises**
  thoroughness. It is the case the paper proves and its own closing sentence
  forgets.

The third case is why the account is worth having rather than replacing with
"tools make people sloppy". The mechanism predicts its own exception, from a
property of the tool you can state before deploying it.

## Why `Proposed`

Because it is derived and not measured. Every proposition in the source is
proved, and none of them is tested; there is no data in the paper at all. A
proof establishes that the conclusion follows from the assumptions, and the
assumptions here include that the producer optimizes a long-run rate, that
item values are independent draws, that the payoff curve is concave above a
hard minimum, and that institutions do not respond. Each is an idealization
somebody could reasonably reject.

The status is about the account, not about the algebra. The algebra is fine.

## What this does not say

**It does not say a time-saving tool lowers quality.** It says the bar on the
marginal hour rises, and that two of three channels lose the race while the
third wins it. A summary that keeps the conclusion and drops the phase has
kept the part that is not determined.

**It does not identify the phase for any real tool.** The source assigns
phases by example — discovery-like in "some technical fields", publication-like
in "fieldwork-based disciplines" — and gives no method for the attribution.
Since the predictions have opposite signs across phases, an account that
cannot attribute the phase predicts nothing in particular. That gap is the
reason [SOTA-tmpri5k6](../practices.d/SOTA-tmpri5k6.md) is phrased as an instruction to do the
attribution rather than as a prediction to apply.

**It is not a claim about LLMs specifically, and the record should not file it
as though it were.** Any labor-augmenting tool has this shape. Compilers,
autocomplete, automated experiment runners, faster training clusters and
evaluation harnesses all remove time from an identifiable phase of somebody's
pipeline, and the argument reaches all of them. The source's framing is
scientific research because that is its authors' field.

**It is one of several accounts of an observation the record already holds.**
[LIT-487](../literature.d/LIT-487.md) found an AI drafting tool that improved petition text on
every measured feature while outcomes stayed flat or fell, and
[THEORY-051](../theory.d/THEORY-051.md) offered feature-distinctiveness as one explanation while
naming diminished author effort as a rival it could not account for. This is
an account of that rival. It does not adjudicate between them — both predict
the same null — and the two papers were written independently of each other.
The mapping of a petition tool onto this model's minimum-publishable phase is
a reading this record makes, and neither paper makes it.
