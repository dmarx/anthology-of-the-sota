---
number: 242
status: Read
formerly:
- NOTE-tmpavng3
paper: LIT-493
title: 'Genesys and what survives its own controls'
version: 1
date: '2026-09-21'
summary: >-
  Read from the [#180](https://github.com/dmarx/anthology-of-the-sota/issues/180) worklist for the architecture-discovery claim and
  filed for the code-generation one. Unit-by-unit generation with an
  execution-based checker takes valid output from 6% to 92% on the same
  proposals, with a stated mechanism that has nothing to do with
  architectures. The discovered architectures are a wash against their own
  seeds, by the paper's own table.
---

<!-- inactive-ok-file: SOTA-304 — Proposed, filed in this same
     contribution; the Recommendations section names it as where R1 went,
     which is the note's job rather than a claim that it is settled -->

# NOTE-242: Genesys and what survives its own controls

## Contribution

The first automated-discovery experiment in this area large enough to be
informative about the *system* rather than about a handful of cherry-picked
outputs: 1,062 designs verified by actual pretraining, at 14M–350M parameters,
with every artifact, agent dialogue and training run published. Previous
LLM-driven "AI scientist" systems chose open-ended research tasks where
success cannot be checked; this one picks a task with an executable success
criterion and then measures its own components against each other. The durable
contribution is the component analysis, not the artifacts.

## Key insight

Getting a long, constrained artifact out of a fixed model is a search whose
difficulty is multiplicative, and the fix is to stop paying for the whole
artifact each time you fail. One-shot generation with retries needs
`E[calls] = 1/p`, where `p` is the probability that *everything* is
simultaneously right; decompose the artifact into units, check each one, and
freeze the ones that pass, and a joint probability becomes a product of local
ones you pay for separately. The checker is what makes freezing meaningful —
without a test that can fail a unit, there is nothing to freeze against.

## Assumptions

- **The artifact must be decomposable into typed units that can be checked in
  isolation.** The paper proves that any composition of `Σ → Σ` functions
  admits the tree factorization it uses, and sketches type-lifting for the
  general case. Architecture blocks are `(X, Z) → (X, Z)`; not every program
  is.
- **A checker must exist and must be cheap.** Genesys's runs static AST
  analysis plus initialization, forward, backward, causality,
  differentiability and a short training run for gradient stability and FLOPs.
  Where no executable check exists, the mechanism has nothing to act on.
- **Fitness is average downstream accuracy across tasks and scales**,
  `F = (1/MK) ΣᵢΣⱼ Perf(B, Dᵢ, Sⱼ)`. Everything selection does runs through
  this number.
- **Performance is assumed to correlate across scales**, which is what makes
  the Ladder-of-Scales budget legitimate. Cited to scaling-law work, carried
  from the small-LM literature, not tested here.

## Key results

- **Table 4 — code generation, 100 held-out proposals.** Valid-implementation
  rate: **Full 92%**, No Planner 91%, No Observer 89%, No unit-based
  generation **73%**, No symbolic checker **30%**, Direct prompting **6%**.
  Function-body lines: Full 181 (±44), No UG 75 (±29), Direct 49 (±15),
  against a human reference library at 220. Token cost: Full 15.0 (±18.5),
  Direct 0.3 (±0.3) — roughly **50×**. *Holds when:* the artifact is a
  GAB-conformant PyTorch block and the checker in Table 1 is available.
- **Table 3 — error rate downstream.** 8.61% with the full system, 27.31%
  without experiment verification, 21–24% for the memory-only and base
  variants. Removing the pretraining feedback roughly triples later failures.
- **Table 2 — evolution ablations, first 300 designs.** End fitness gain
  `Δ`: Full 4.10%, w/o Literature 3.37%, w/o Experiment 2.20%, Base w/ Memory
  2.81%, **Base 0.01%**. Sharpe ratio 69.0 / 56.7 / 26.3 / 19.6 / 0.2. At 1000
  designs the full system reaches peak fitness 0.633 and shows signs of
  converging.
- **Table 5 — discovered designs at 350M, 50B tokens.** Averages: seeds GPT
  **61.78**, Mamba2 61.45, RWKV7 61.14, RetNet 59.78, TTT 59.71; discovered
  Geogate **61.81**, HMamba 60.61, Hippovq 59.80, SRN 59.57, VQH 59.05. Best
  discovered beats best seed by **0.03**; the five discovered average
  **60.17** against the seeds' **60.77**.
- **Table 16 — spread across the whole search.** Per-benchmark standard
  deviation over all verified designs: mrpc 0.1465, wnli 0.0593, blimp 0.0566,
  rte 0.0288, wsc273 0.0179, inverse_scaling 0.0141, cola 0.0138, sst2 0.0138,
  winogrande 0.0103. Random baselines sit at 0.49 on six of the nine.
- **Appendix A.1** — the Viterbi-style argument: unit-wise generation with
  freezing reduces expected calls and billable tokens exponentially in the
  number of units, relative to one-shot-with-retry, under i.i.d. per-unit
  success.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Unit-by-unit generation with a per-step checker massively raises the rate of valid long programs | strong | Table 4, 100 held-out proposals, five ablated arms plus a direct-prompting control |
| C2 | Of the two, the checker matters more than the decomposition | strong | Table 4: 30% without the checker vs 73% without unit-based generation |
| C3 | The advantage is exponential in artifact complexity | moderate | Appendix A.1, proved under i.i.d. per-unit success — an assumption the paper does not test and which correlated failures would break |
| C4 | Real pretraining feedback in the selection loop improves both fitness and downstream code correctness | moderate | Tables 2 and 3; the fitness half runs through a noisy metric, the error-rate half does not |
| C5 | The discovered architectures are competitive with GPT2 and Mamba2 | weak | Table 5, as a maximum over five designs selected from 1,062 by the same metric family, on benchmarks chosen from the search's own statistics |
| C6 | This shows the feasibility of LLM-driven discovery for competitive ML research | weak | rests on C5 |

## Method

Two agent subsystems over a shared evolution tree. **Proposal:** a proposer
agent picks one or two parent designs plus references from a 297-paper library
and writes a research proposal for a mutation, crossover or from-scratch
design; an adversarial reviewer scores it against past proposals and the loop
repeats until the score clears a threshold. **Implementation:** a planner picks
an unimplemented unit and plans it, a coder writes it and may declare child
units, and a symbolic checker plus an observer agent accept or revert the
unit; the tree state rolls back on failure, so only the failing unit is redone.
**Verification:** a Ladder of Scales — about 1,000 models at 14M on 0.7B
tokens down to 5 models at 350M on 50B tokens, budgets released upward as
lower-scale budgets are spent. **Selection:** designs are placed in quadrants
by fitness and by confidence (number of scales verified); designers exploit
Good-and-Confident and explore Poor-and-Confident, verifiers exploit
Good-and-Unconfident.

## Concepts

- **GAB / GAU** — the generalized autoregressive block, a PyTorch module
  contract `(X, Z) → (X, Z)`, and the unit tree a block factors into. The
  contract is what makes a partial artifact checkable, which is the whole
  trick.
- **Fitness `F`** — average downstream task accuracy over tasks and scales.
  Not loss, not held out.
- **Confidence** — how many scales a design has been verified at. Orthogonal
  to fitness and used to direct verification rather than design.
- **Ladder of Scales** — pyramidal verification budget, many trials small, few
  large.
- **Viterbi-style search** — here, generating a structured artifact left to
  right while committing to each validated piece, rather than resampling the
  whole.

## Connections

The lineage is neural architecture search with the fixed operator inventory
removed: instead of searching a predefined space of kernels and head counts,
an LLM writes new operators as code. That is the same move as FunSearch and
the LLM-genetic-programming line the paper cites, applied to a much larger
artifact. The seeds are the record's own architecture trunk — GPT, Mamba2,
RetNet, RWKV6, TTT — which is why the tags put this under
`model-architecture` as well as where its usable advice lives.

No machine-readable relation is declared. The record holds the seed
architectures, but this paper does not extend, correct or measure itself
against any single one of them; it uses five of them as starting points, which
is not a relation the vocabulary has a word for.

## Recommendations

- **R1** — generate long constrained programs unit by unit, freezing each unit
  that passes an executable check, rather than regenerating the artifact and
  retrying. *Topic:* code generation with a fixed model. *Status:*
  experimental. *Strength:* strong. *Applies when:* the artifact decomposes
  into independently checkable pieces and a cheap checker exists. Filed as
  `SOTA-304`.
- **R2** — if you can only build one of the two, build the checker. *Same
  source, same table*; carried as a paragraph inside R1's practice rather than
  as its own document, because it is a refinement of the same instruction.
- **R3** — put real execution feedback, not a model's judgement of the
  artifact, in the selection loop. *Strength:* moderate. **Not filed.** The
  fitness half of the evidence runs through the noisy benchmark average
  criticized below, and the error-rate half (27.31% → 8.61%) is one
  measurement in one system. It is a candidate, not a recommendation.
- **R4** — evaluate a design search on tasks held out of its fitness function,
  and compare a winner's margin against the spread of that metric across the
  search population. **Not filed as a practice**, because this paper is an
  instance of the problem rather than evidence about it: nobody here ran the
  held-out comparison and measured the difference. Filed as an issue instead.

## Bearing on the record

Adds a practice the corpus had no coverage of at all: seven documents carry
`in-context-learning` and none of them is about getting a long, constrained
artifact out of a fixed model. `SOTA-279`, `SOTA-280` and `SOTA-281` are about
reasoning traces; this is about structured generation under a checker, which
is a different lever.

It does **not** bear on the record's architecture practices. Nothing here
recommends any of VQH, HMamba, Geogate, HippoVQ or SRN, and the record should
not file a discovered design as a practice on this evidence.

## Limitations

- **The final evaluation is not held out of the search.** Fitness is average
  downstream accuracy; the nine tasks in Table 5 are drawn from the same
  verification pool, selected by Table 16's standard — largest standard
  deviation across designs, best design beating random by over 5%, enough
  samples — which are statistics of the search population itself. The paper
  states this; it still means the headline comparison shares a metric with the
  selection.
- **The margins are inside the noise the paper publishes.** CoLA and SST2 have
  a design-to-design standard deviation of 0.0138 across all verified designs,
  and the Table 5 margins on them run from half a point to two and a half. Six
  of the nine tasks have a random baseline at about 0.49 and every model within
  a few points of it.
- **Five designs against five seeds, one run each.** No seeds, no error bars,
  no repeated training runs anywhere in Table 5.
- **The exponential advantage assumes independent per-unit success.** Failures
  in generated code are plausibly correlated — a bad plan makes several units
  wrong together — and the appendix does not treat that case.
- **Cost is real and reported.** The full designer spends about 50× the tokens
  of direct prompting per artifact. The paper reports this in the same table as
  the win, which is the right place for it.
- **The authors name their own two:** efficiency-focused innovations such as
  FlashAttention cannot be discovered because the hardware-specific evaluation
  is not in the loop, and billion-parameter discovery was out of budget.

## Open questions

- **Does the unit-plus-checker result hold outside architecture code?** The
  mechanism is stated in terms of any decomposable artifact under any checker,
  and was measured on exactly one artifact type with one checker. The
  replication that would settle it is the same model and budget generating
  long artifacts of another kind under both strategies, with validity judged
  by a checker written before either run.
- **How much of the 92% is the GAB contract rather than the loop?** A
  well-specified module interface is itself a large constraint on what the
  model can write, and no arm removes it.
- **Would the discovered designs survive a held-out evaluation?** The artifacts
  and training runs are public, so this is answerable by someone with the
  compute: take the five designs and score them on tasks the fitness function
  never saw. Until that exists, "competitive with known architectures" is a
  statement about a selected maximum.
