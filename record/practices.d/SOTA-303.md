---
number: 303
status: Proposed
formerly:
- SOTA-tmpri5k6
promote_when: >-
  Two deployments of time-saving tools whose phases differ, with the fraction
  of started work that ships measured in both, moving in **opposite**
  directions. That is the prediction no competing story about tools and
  quality makes, and it is jointly falsifiable from the two signs. A single
  deployment would also do it if the phase is attributed by something other
  than the outcome and per-item effort is measured — including, and most
  usefully, a case where effort goes up. What would not meet it: a study
  reporting more output and lower quality after a tool was introduced. That
  is consistent with every channel here and with several explanations that
  are not this one, and it is the reasoning this practice exists to stop.
consensus: unreplicated
consensus_note: >-
  One group, one paper, no data — the model is Charnov's marginal value
  theorem, which is fifty years old and not in dispute, applied to a setting
  nobody has measured. What is unreplicated is not the mathematics but the
  claim that research and writing effort behave this way. Against it: the
  belief this practice contradicts, that saved time returns to the work that
  saved it, is widely held and equally unmeasured.
title: 'Name the phase a time-saving tool accelerates before predicting what it will do to the quality of what people produce with it'
version: 1
tags:
- deployment-and-society
- analysis-and-evaluation
date: '2026-09-21'
source:
- LIT-492
introduced_by:
- LIT-492
implementations: []
explained_by:
- THEORY-055
summary: >-
  Duede, Gross, Crockett and Bergstrom (2026), [LIT-492](../literature.d/LIT-492.md) — in a
  marginal-value-theorem model, accelerating the phase before value is known
  makes producers **more** selective, accelerating the minimum cost of
  shipping makes them **less** selective, and both make each item less
  thoroughly developed — while accelerating discretionary improvement makes
  each item **more** thoroughly developed. Opposite signs from the same tool
  depending on where it acts, so "it saves time" does not determine the
  direction.
---

<!-- inactive-ok-file: THEORY-055 — Proposed, filed in this same
     contribution and declared as this practice's `explained_by:`; the
     citation is the relation -->

<!-- inactive-ok-file: SOTA-298 — Proposed, cited in Related to say what this
     practice is NOT evidence for and to state that neither supports the
     other. A comparison between two open claims does not wait on either -->

# SOTA-303: Name the phase a time-saving tool accelerates before predicting what it will do to the quality of what people produce with it

## Source

Duede, Gross, Crockett and Bergstrom (2026),
[LIT-492](../literature.d/LIT-492.md) — read as [NOTE-241](../notes.d/NOTE-241.md).

## When this applies

You are deploying, evaluating or forecasting a tool that makes people faster
at some part of producing something — a coding assistant, a drafting tool, a
literature-search agent, an automated reviewer, a faster experiment loop. The
people using it choose how much effort to put into each item and how many
items to take on. If they are demand-limited rather than rate-limited — they
have exactly the work they have and no queue behind it — none of this binds.

## Do this

**Attribute the phase before predicting the effect.** There are three, and
they are distinguishable by a question about the tool rather than about its
users:

1. **Before the item's value is known.** The tool helps find out whether the
   thing is worth doing — hypothesis generation, triage, search, a quick
   feasibility check.
2. **The fixed minimum needed to ship at all.** The tool removes required
   overhead — formatting, boilerplate, figure construction, the first draft
   that must exist before anything can be submitted.
3. **Discretionary improvement above that minimum.** The tool makes the
   *improving* faster — the extra experiment, the sensitivity analysis, the
   counter-example search, the revision pass.

Then read the prediction off the phase:

| phase accelerated | fraction of started work that ships | thoroughness of what ships |
|---|---|---|
| 1 — discovery | **falls** (more selective) | falls |
| 2 — minimum to ship | **rises** (less selective) | falls |
| 3 — discretionary improvement | rises, under a regularity condition | **rises** |

[THEORY-055](../theory.d/THEORY-055.md) gives the reason all three share: the producer's own
rate of return is the price of their time, every acceleration raises it, and
the marginal hour of improvement then has to clear a higher bar. Phase 3 is
the case where the hour's value rises faster than the bar.

## The negative this replaces

**Do not treat time saved as time returned to the same work.** "Automating the
tedious parts frees us to think more deeply" is the default forecast, it is
the one the source was written against, and it is the phase-3 prediction
applied to phase-1 and phase-2 tools. If your tool removes overhead, the model
says the freed hour goes to the next item, because the next item is now worth
more per hour than it was.

**And do not run the inference backwards.** Observing more output at lower
quality after a tool lands does not identify this mechanism. Every phase here
predicts lower thoroughness except one, and so do several accounts that have
nothing to do with opportunity cost: newly-enabled producers who are worse
than the incumbents, readers discounting what they suspect was generated, and
skill loss from disuse. The practice is a forecasting discipline, not a
diagnosis.

## Conditions

**This is a model with no measurements in it.** Not underpowered — absent.
Every claim is a proposition with a proof, and the propositions are about a
stylized producer, not about anyone observed. The source's own description is
"a simple mathematical model to illustrate".

**The attribution method does not exist yet, and it is the load-bearing
step.** The source assigns phases by example and gives no procedure. Since the
table above has opposite signs in its first column, a wrong attribution
inverts the prediction, and nothing in the source helps you check one. Treat
the phase as a hypothesis you state in advance and can be wrong about, which
is at least a different epistemic position from having no prediction.

**Most real tools act on more than one phase.** The source says so and studies
them separately anyway. A coding assistant that writes boilerplate (phase 2),
scaffolds an investigation (phase 1) and speeds up a refactor (phase 3) has
all three signs at once, and the model has nothing to say about the net.

**Institutions are held fixed.** Peer review capacity, what counts as a
shippable unit, and what reviewers demand do not respond in the model. The
source notes submissions already straining review as an institutional response
beginning, and cannot represent it. The shorter the horizon, the safer the
assumption.

**The tool is stipulated to be perfect.** No errors, no cost. That is a
strength of the argument — it isolates the consequence of speed — and a limit
on the practice: a real tool's effect on quality is this effect plus whatever
its mistakes do, and this says nothing about the sum.

**The source's own summary overshoots its own result.** "Impelling us to do
more, less well" appears unqualified in the abstract and again as the closing
line, and Proposition 12 proves the opposite for phase 3. The analysis section
states the exception. A reader who takes the memorable sentence has taken the
part the paper disproved, which is why this practice is written around the
table rather than around the conclusion.

## Related

[SOTA-298](../practices.d/SOTA-298.md) says to measure a writing assistant by the outcome it was
deployed to improve rather than by the text features that used to predict it,
on the strength of a deployment where the text improved and the outcomes did
not. This is the complementary half and a different kind of claim: that one is
about what to measure after the fact, this is about what to predict before it.
Neither is evidence for the other — [LIT-487](../literature.d/LIT-487.md) measured outcomes and not
effort, and this source measured nothing — and the two papers do not cite each
other.
