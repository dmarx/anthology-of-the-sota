---
number: 201
status: Read
formerly:
- NOTE-tmpp6ac8
paper: LIT-451
title: 'Data Mixing Can Induce Phase Transitions in Knowledge Acquisition'
version: 1
date: '2026-09-20'
summary: >-
  Linear scaling of acquired knowledge in model size holds when a
  knowledge-dense dataset is trained on alone and breaks once it is mixed
  into web text: below a critical model size, or a critical mixing ratio,
  the model memorises almost nothing. Attributed to capacity allocation as a
  knapsack, with the critical ratio a power law in model size.
---

# NOTE-201: Data Mixing Can Induce Phase Transitions in Knowledge Acquisition
<!-- inactive-ok-file: THEORY-025 — Proposed, and the single-claimant case this reading bounds -->
<!-- inactive-ok-file: SOTA-166 — Proposed, and one of the two practices this reading contests -->

## Contribution

Shows that a scaling law established for knowledge-dense data in isolation
does not survive the condition under which that data is actually used. Real
corpora are over 95% web text; the knowledge-dense fraction is small by
construction, and the question of what a model acquires from a small fraction
had been answered by extrapolating the isolated case. The extrapolation is
wrong in a specific and consequential way: acquisition is not continuous in
either the mixing ratio or the model size, but has thresholds below which
almost nothing is learned however long training runs. The paper supplies a
mechanism — bounded capacity allocated across datasets is a discrete
optimisation, and discrete optima jump — and shows the thresholds are
predictable, the critical ratio following a power law in model size.

## Key insight

**A scaling law measured on one dataset is a statement about a model with
one claimant on its capacity.** The linear law for knowledge acquisition was
measured by training exclusively on biographies, where the only thing
capacity can be spent on is biographies. Put a second dataset in and the
model is solving an allocation problem: given a bounded budget, how much goes
to each corpus to minimise total loss. That problem has a discrete answer,
and a discrete answer moves discontinuously when its inputs move continuously
— so a model just below threshold spends nothing on the small dataset, and a
model just above spends a lot. The smoothness everyone assumed came from
never having more than one claimant.

## Assumptions

- **Synthetic biographies as the knowledge-dense dataset**, following
  Allen-Zhu and Li, mixed into FineWeb-Edu or the Pile. The uniform format is
  what makes knowledge countable — memorised biographies — and is also what
  makes the setting unlike any real knowledge-dense corpus.
- **Pythia models, 14M to 6.9B**, pretrained or continually pretrained on the
  mixture.
- **One knowledge-dense domain at a time.** Real mixtures have many, each
  with its own ratio, and the allocation problem the paper formalises would
  be over all of them.
- The information-theoretic framework assumes capacity is the binding
  constraint and the objective is overall test loss.
- "Knowledge acquired" is memorisation of biographies, not downstream
  capability.

## Key results

- **Phase transition in model size.** At fixed mixing ratio, accuracy stays
  at zero as model size grows, then past a threshold rises rapidly to over
  60%. *Holds when:* 14M–6.9B Pythia, this mixture.
- **Phase transition in mixing ratio.** At fixed model size, accuracy stays at
  zero as the ratio rises, then past a threshold climbs quickly. Below it,
  **extensive further training does not help** — this is not slow learning.
- **The critical mixing ratio follows a power law in model size**, so the
  location of the transition is predictable rather than merely present.
- **Mechanism**: capacity allocation as a knapsack; the optimal allocation
  across datasets can change discontinuously in model size or mixing ratio.
  Formalised information-theoretically.
- **Contrast case**: trained on the knowledge-dense data alone, the same
  setting gives the smooth linear law reported by prior work. The transition
  is a property of mixing, not of the dataset.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Knowledge acquisition under mixing has a phase transition in model size | strong | measured across 14M–6.9B at several ratios, with the isolated-training control giving the smooth law |
| C2 | It has a phase transition in mixing ratio, below which training longer does not help | strong | measured at several model sizes; the "extensive training" control is what rules out slow learning |
| C3 | The critical ratio follows a power law in model size | moderate | fitted over the measured grid; a power law over a limited range |
| C4 | The mechanism is discrete capacity allocation | moderate | an information-theoretic account consistent with the measurements; no intervention isolates it |
| C5 | A mixing recipe optimal for one model size may be wrong for another | strong | follows directly from C1 and C3 and is demonstrated |

## Method

Curate synthetic biographies in the Allen-Zhu and Li format, where each
individual's attributes appear in varied templates so memorisation can be
counted by evaluating recall of the attributes. Mix at a controlled ratio
into a web corpus. Sweep model size and mixing ratio independently,
pretraining or continually pretraining Pythia models at each point, and plot
memorised fraction.

Separately, formalise a model of bounded capacity choosing an allocation
across two datasets to minimise total loss, and derive where the optimum
changes discontinuously. Fit the resulting critical-ratio relationship
against the measured transitions.

## Concepts

- **Knowledge-dense data** — curated corpora with high information density on
  a domain: Wikipedia, Stack Exchange, OpenWebMath, StarCoder. Typically a
  few percent of tokens, often far less.
- **Mixing ratio** — the fraction of the pretraining corpus drawn from the
  knowledge-dense dataset.
- **Capacity allocation** — how a model with bounded capacity divides it
  between datasets. Here, the knapsack whose discreteness produces the
  transitions.
- **Critical mixing ratio** — the ratio, at a given model size, below which
  almost nothing from the dense dataset is memorised.

## Connections

Takes the linear scaling law of Allen-Zhu and Li's biography experiments as
its null hypothesis, and cites [LIT-452](../literature.d/LIT-452.md)'s Wikidata measurement as the
same law reached by a different route, plus a theoretical treatment. All of
these are single-dataset results, which is the paper's point.

The capacity framing is the one [LIT-440](../literature.d/LIT-440.md) uses for a single dataset — a fixed
budget of bits, filled and then substituted for by generalisation. This is
that picture with competition added.

Against the data-mixing-law literature, which fits proportions on small runs
and extrapolates; the paper does not frame itself as a rebuttal to those, and
it is one.

## Recommendations

- **R1** — Do not carry a mixing ratio from a small model to a large one, or
  from a large one to a small one; the threshold where a domain begins being
  learned moves with size. *Topic:* data mixing. *Status:* experimental.
  *Strength:* strong. *Applies when:* any knowledge-dense domain at a small
  share of the corpus.
- **R2** — If a domain shows near-zero acquisition, raise its ratio rather
  than training longer; below the critical ratio more steps do not help.
  *Topic:* data mixing. *Status:* experimental. *Strength:* moderate.
  *Applies when:* the failure looks like slow learning.
- **R3** — Use the power-law relationship to predict where the critical ratio
  sits at target scale rather than measuring at the scale you can afford.
  *Topic:* data mixing. *Status:* experimental. *Strength:* weak. *Applies
  when:* the fitted law can be re-estimated in your own setting; the
  constants are not transferable.

## Bearing on the record

- **Contests [SOTA-166](../practices.d/SOTA-166.md) and [SOTA-238](../practices.d/SOTA-238.md).** Both set data proportions from
  small runs — one by fitting a mixing law and extrapolating, the other with
  a small proxy under group DRO. Both assume the fitted quantity is
  continuous in scale. This names a way for that assumption to fail that
  neither has checked. Neither is refuted; both gain a `contested_by`.
- **Should produce a practice** for R1, and a theory for C4, which is the
  more portable claim: it predicts discontinuity in mixing effects generally,
  not only for factual knowledge.
- **Bounds [THEORY-025](../theory.d/THEORY-025.md)**, whose fixed-bit-budget picture is the
  single-claimant case. The plateau that account measures is smooth because
  nothing is competing for the budget.
- **Does not bear on [SOTA-103](../practices.d/SOTA-103.md)** as directly as it looks. That practice adjusts
  proportions *online from per-domain loss during the run being trained*, so
  it is not extrapolating across scale — though whether an online rule can
  cross a discontinuity it cannot see the far side of is a real question
  nobody has asked.

## Limitations

- Synthetic biographies. The countability that makes the measurement possible
  is exactly what real knowledge-dense corpora lack, and nothing establishes
  that Wikipedia behaves like this.
- One knowledge-dense domain against one web corpus. Real mixtures have many
  domains competing, which is the interesting version of the knapsack and is
  not run.
- Largest model 6.9B. The power law for the critical ratio is fitted over
  that range.
- The knapsack account is consistent with the data and is not isolated by any
  intervention; an alternative explanation in terms of optimisation rather
  than capacity is not ruled out.
- "Memorised biographies" is a memorisation metric, not a capability one. A
  model below threshold might still be usefully better on the domain.

## Open questions

- Does the discontinuity appear for capabilities other than factual
  memorisation? The knapsack argument says it should; nothing tests it.
- What happens with many competing domains? The two-dataset knapsack is the
  simplest case and real mixtures are not it.
- Can an online mixing rule ([SOTA-103](../practices.d/SOTA-103.md)) cross a transition? It adjusts on
  observed per-domain loss, and below the critical ratio there is no loss
  signal to follow.
