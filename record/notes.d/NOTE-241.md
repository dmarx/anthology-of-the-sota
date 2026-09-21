---
number: 241
status: Read
formerly:
- NOTE-tmpcr9xy
paper: LIT-492
title: 'LLMs raise the opportunity cost of research time'
version: 1
date: '2026-09-21'
summary: >-
  Read for a mechanism `THEORY-051` named and the record could not supply:
  why effort would fall when a writing tool gets better. The answer is that a
  perfect time-saving tool raises the value of time, and the interesting part
  is not the decline but the **phase dependence** — the model predicts
  opposite signs for selectivity, and the opposite sign for thoroughness, from
  properties of the tool you can identify before deploying it.
---

<!-- inactive-ok-file: THEORY-051 — Proposed, cited twice for the same
     reason: this reading exists because that theory named a rival
     explanation it could not account for, and its unsettledness is the
     point of the citation rather than a problem with it -->

# NOTE-241: LLMs raise the opportunity cost of research time

## Contribution

Takes Charnov's marginal value theorem out of behavioral ecology and applies
it to the allocation of research effort, with the discovery phase as the
travel time between patches and discretionary development as the diminishing
harvest within one. The novelty is not the theorem but the decomposition:
splitting the acceleration into three phases — discovery before value is
known, the fixed cost of producing a publishable artifact, and discretionary
improvement after that minimum — and showing the three have different and
partly opposite consequences. Before this, "LLMs will free up time to think"
and "LLMs will flood the literature" were two intuitions with no shared
frame; here they are the same model under different parameters.

## Key insight

A tool that makes you faster makes your time more valuable, and your time
being more valuable is exactly the reason to stop polishing. The long-run
rate of return `λ` is simultaneously the payoff being maximized and the
opportunity cost of every hour, so any acceleration anywhere in the pipeline
feeds back as a higher bar on the marginal hour spent improving the thing in
front of you. The freed time does not return to the work that freed it.

## Assumptions

The formal results need this structure, stated in the appendix:

- Project values `v` are drawn from an atomless distribution `F` with support
  on `[0, v̄]` — values are independent draws, so nothing the researcher
  learns on one project informs the next. This is what makes it foraging.
- `u(t) = 0` for `t ≤ a`; `u' > 0` and `u'' < 0` for `t > a`; `u(t) → 1` from
  below. No payoff at all below the minimum publishable investment, strictly
  diminishing returns above it, and a ceiling at the project's full value.
- Time is the only limiting resource. The authors flag the extension to other
  inputs and do not take it.
- **Institutions and incentives are static.** Peer review capacity, what
  counts as a publishable unit, and hiring norms do not respond. The authors
  defend this only on a short timescale and say a period of mismatch is
  inevitable.
- The tool has no error cost and no financial cost. Stipulated, not derived.

## Key results

- **Prop. 1** — a payoff-optimal policy `τ*(v) ∈ argmax_t {v·u(t) − λ*·t}`
  exists and is unique except at one indifference point, and `λ*` is pinned by
  `λ*·s = E[V·u(τ*(V)) − λ*·τ*(V)]`: the cost of discovery exactly balances
  the expected net benefit of developing. *Holds when:* the structure above.
- **Prop. 3–4** — a unique interior threshold `v₀` exists, and above it both
  development time `τ(v)` and thoroughness `u(τ(v))` strictly increase in `v`.
- **Prop. 5–7 (shortening discovery `s`)** — `λ` strictly decreases in `s`, so
  a faster discovery phase raises `λ`; `v₀` **rises**, so a smaller fraction of
  projects is developed; and `z(β(v))` falls for every developed project. More
  selective, less thorough.
- **Prop. 8–10 (shortening the minimum `a`)** — `dλ/da = −λ/T_d`, where `T_d`
  is the average time between completed projects; `v₀` **falls**, because
  `a + β₀ < T_d` makes the direct effect dominate the opportunity-cost effect
  at the margin; thoroughness falls again. Less selective, less thorough.
- **Prop. 11–12 (accelerating discretionary work by a factor `α`)** —
  thoroughness `z(αβ(v))` **rises** for every developed project, because
  `λ/α` decreases in `α`. And `v₀` falls, *conditional on the elasticity of
  `z` being decreasing in `b`*; the main text says the direction is
  "ambiguous without further structure" absent that condition.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | A perfect time-saving tool raises the opportunity cost of research time | strong | Props. 5, 8 and the `dλ/dα > 0` step in Prop. 12; follows from the renewal-reward structure |
| C2 | Accelerating discovery makes researchers *more* selective about what they develop | moderate | Prop. 6, by the envelope theorem — but the sign depends on `s` entering only as dead time before value is known |
| C3 | Accelerating the fixed cost of publishing makes them *less* selective | moderate | Prop. 9; the dominance argument `a + β₀ < T_d` is exact but holds at the indifference margin only |
| C4 | Projects that are developed get developed less thoroughly | moderate | Props. 7 and 10 — **for two of the three channels**, and reversed by Prop. 12 for the third |
| C5 | Accelerating discretionary improvement raises thoroughness | moderate | Prop. 12 |
| C6 | LLMs will, in practice, do these things to science | weak | no measurement anywhere in the paper; the mapping from LLM capabilities to `s`, `a` and `α` is asserted by example |

## Method

*(Analytic; no experiments.)* Renewal-reward formulation of the long-run rate
`Λ(τ) = E[V·u(τ(V))] / (s + E[τ(V)])`, optimized by the standard shadow-price
argument: define the per-project surplus `m_λ(v) = max_t [v·u(t) − λt]`, show
`Φ(λ) = E[m_λ(V)] − λs` is continuous and strictly decreasing with a sign
change, and take the unique root. Comparative statics are envelope-theorem
derivatives evaluated at the threshold project, which is what lets the sign of
`∂σ(v₀(x), x)/∂x` stand in for the movement of `v₀` itself.

## Concepts

- **discovery phase `s`** — fixed time before the project's value is known.
  Hypothesis generation, experiment design, preliminary data. Dead time in the
  foraging sense: it earns nothing directly and is paid on abandoned projects
  too.
- **minimum development `a`** — the work required to have a publishable
  artifact at all: figures, typesetting, proofreading, submission chores.
  Below it the payoff is exactly zero.
- **discretionary development `b`** — everything above the minimum:
  follow-ups, sensitivity analyses, generalizing a result, polishing prose.
  This is where thoroughness lives.
- **thoroughness** — `u(τ(v))`, the *fraction* of a project's available value
  realized. Not absolute quality: a more valuable project developed to a lower
  fraction can still be a better paper.
- **labor-augmenting** — makes a unit of labor produce more, as opposed to
  replacing it. The distinction matters because the whole argument runs
  through the researcher still choosing.

## Connections

The mathematics is Charnov (1976), the marginal value theorem, unchanged: an
optimal forager leaves a patch when its marginal yield drops to the habitat's
average rate, and enriching the habitat makes it leave sooner. Reading `s` as
travel time and `u` as the within-patch gain function is the whole
translation, and the threshold `v₀` is the one piece of added structure —
foraging models do not usually let the animal inspect a patch and walk away.

Within this record it sits next to [LIT-487](../literature.d/LIT-487.md), which is the empirical case with
no mechanism, where this is the mechanism with no empirical case. The two
were produced independently and neither cites the other.

## Recommendations

- **R1** — before predicting what a time-saving tool does to the quality of
  what people produce with it, identify which phase it accelerates; the sign
  differs by phase. *Topic:* deployment. *Status:* experimental. *Strength:*
  moderate. *Applies when:* the users choose how much effort to spend and are
  rate-limited rather than demand-limited.
- **R2** — do not count the time a tool saves as time that returns to the same
  work. *Topic:* deployment. *Status:* experimental. *Strength:* moderate.
- **R3** — if you want a tool to raise quality rather than volume, put it in
  the discretionary phase. This is the constructive reading of Prop. 12 and
  the paper does not state it as advice.

## Bearing on the record

`THEORY-051` names three candidate explanations for `LIT-487`'s finding that
an AI drafting tool improved petition text and not petition outcomes: reader
suspicion, loss of the features' distinctiveness, and diminished author
effort. The third had no account behind it. This supplies one, and supplies
it in the form that would be testable: Change.org's tool reduces `a` — the
fixed cost of producing a petition at all — and the model's predictions for a
reduction in `a` are *more petitions, each less thoroughly developed*, which
is what that paper observed.

That mapping is this record's reading and not a claim either paper makes.
Petition writers are not researchers, a petition's `v` is not a paper's, and
the model assumes the writer knows `v` before deciding — which for a petition
is doubtful. It is stated here because it is checkable, not because it is
established.

Nothing here bears on `SOTA-291`: that practice is about what an evaluation
design can identify, and this paper runs no evaluation.

## Limitations

- **No data.** Not a single measurement. The paper is honest about being an
  illustration, and its own framing is "a simple mathematical model to
  illustrate".
- **The mapping to real tools is asserted.** Which of `s`, `a` and `α` a given
  LLM workflow touches is given by example — "as in some technical fields",
  "as in fieldwork-based disciplines" — and never operationalized. Since the
  predictions have opposite signs across those cases, the model cannot be
  applied at all without a phase attribution that the paper does not supply a
  method for.
- **Static institutions.** The authors name this and note that submissions are
  already straining peer review, which is an institutional response beginning.
  The model cannot represent it.
- **Independent project values.** If discovery is informative about *future*
  projects rather than only the current one, the foraging analogy weakens; a
  research programme is not a patch chosen at random.
- **The closing sentence overshoots the model.** "Impelling us to do more,
  less well" is stated without qualification in the abstract and again in the
  discussion; Prop. 12 says the third channel does the opposite. §3 states the
  exception. The summary does not carry it.

## Open questions

- **Which phase do real LLM workflows accelerate, and can it be measured?**
  The result that would settle the paper's usefulness is an attribution
  method: some observable that says whether a given tool is acting on `s`,
  `a` or `α` in a given field. Without it the model predicts everything.
- **Does the selectivity prediction hold anywhere?** Prop. 6 and Prop. 9 have
  opposite signs, which makes them jointly falsifiable: find two deployments
  that differ in phase and show the fraction of started work that ships moves
  in opposite directions. A single deployment showing "more output, lower
  quality" confirms nothing — it is consistent with all three channels and
  with plain dilution.
- **What happens when the institutions move?** The paper's own citation to
  rising submissions straining review is the first step of a feedback the
  model holds fixed. Whether the equilibrium restores thoroughness or
  entrenches the shift is not addressed.
