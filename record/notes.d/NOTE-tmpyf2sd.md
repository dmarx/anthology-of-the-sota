---
status: Read
paper: LIT-tmpj6eqy
title: 'Non-identifiability of mechanistic explanations'
version: 1
date: '2026-09-21'
summary: >-
  Read from the [#180](https://github.com/dmarx/anthology-of-the-sota/issues/180) worklist, the strongest of the remaining
  candidates. Asks whether mechanistic interpretability's criteria pick out a
  unique explanation and answers no at all four stages by exhaustive
  enumeration — no network had exactly one circuit interpretation — with both
  counts lower bounds by construction.
---

<!-- inactive-ok-file: SOTA-309 — Proposed, named in a tally of five
     documents filed the same day. The citation counts it; it does not rely
     on it, and the tally's own point is that no principle is being drawn -->

<!-- inactive-ok-file: SOTA-286 — Proposed, cited as one of the two existing
     practices this one completes a set with. The citation is about what the
     three are severally about, which does not wait on any of them being
     settled -->

# NOTE-tmpyf2sd: Non-identifiability of mechanistic explanations

## Contribution

Asks a question the field had left tacit and answers it with a construction
rather than an argument. A mechanistic explanation has two components — *what*
algorithm, and *where* it lives in the network — and two dominant strategies
find them in opposite orders. The paper borrows identifiability from
statistics, poses one question per component per strategy, and settles all
four by enumerating the complete space on models small enough to enumerate.

The value is in the methodology as much as the answer: by shrinking the
problem until exhaustive search is possible, a claim that would otherwise be
an intuition ("there are probably other circuits") becomes a count.

## Key insight

Circuit error and interchange-intervention accuracy are **satisfiability
tests, not selection rules**. They tell you an explanation is admissible. They
are silent about how many other explanations are equally admissible, and the
answer turns out to be "very many, growing fast with width". The criteria were
doing less work than their use implies, and nobody had checked because
checking requires a model small enough to exhaust.

## Assumptions

- The explanatory goal is fixed — explain the input-output behaviour of a
  trained MLP — and so is the simplification strategy. The paper deliberately
  excludes the explanatory pluralism that would make multiple explanations
  unsurprising, and searches for *conflicting* ones under matched goals.
- Two explanations conflict if they posit different algorithms for the same
  behaviour, or embed the same algorithm in different subspaces.
- Training stops at mean squared loss below `n × 10⁻³` rather than zero; §4.2
  probes whether that slack explains the counts.
- Circuit enumeration is restricted to sparsity above 0.3 and to
  two-input/one-output circuits per target gate, "the smallest sparsity that
  remains manageable".

## Key results

- **All four identifiability questions answered negatively.** Multiple circuits
  reach circuit error zero; a given circuit admits multiple valid
  interpretations; several algorithms reach IIA of one; and a given aligned
  algorithm admits multiple equally-aligned subspaces.
- **Counts by width** (`k` from 2 to 5, median): circuit-first **38 →
  910,000**; algorithm-first **8 → 3,700**.
- **Uniqueness is essentially absent.** Under **2%** of trained networks have
  exactly one valid minimal mapping; **no network** has exactly one circuit
  interpretation.
- **Both are lower bounds**, stated by the authors: the sparsity cap and the
  circuit shape restriction bound the circuit count, and interpretations are
  counted only for the sparser circuits while "the number of potential
  interpretations for a single circuit grows exponentially with its size".
- **Multi-task training reduces it.** Fixing `k = 3` and varying `n` from 1 to
  6 gates trained in parallel, the number of interpretations decreases
  significantly (`p = 0.05`) up to 4 tasks; past that the variation is not
  significant.
- **Training slack is not the explanation.** Varying the loss cutoff and the
  input noise moves the counts — noise decreases circuits while increasing
  interpretations in the circuit-first method, and has no significant effect
  algorithm-first — but "this effect alone is unlikely to mitigate the issue
  entirely".
- **Scale demonstration.** MLP `(784, 128, 128, 3, 3, 3, 1)` on MNIST digits
  0/1, split at the width-3 bottleneck; the tail enumerated against the head's
  partial computations gives **3,209 valid circuits**, and any valid circuit
  in the head extends through one of them.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | MI criteria do not identify a unique explanation at any of the four stages | strong | exhaustive enumeration; the counts are lower bounds |
| C2 | The problem grows with network width | strong | 38 → 910,000 and 8 → 3,700 across `k` = 2…5 |
| C3 | It does not vanish at larger scale | moderate | one MNIST network, one partial enumeration, plus a burden-shifting argument |
| C4 | Multi-task training reduces the count | weak | `p = 0.05`, one width, plateaus after 4 tasks |
| C5 | Training slack does not explain the counts | moderate | loss-cutoff and noise sweeps in the appendices, reported as directions |
| C6 | Sparsity cannot break the tie | moderate | argued, and supported by the enumerations not singling anything out |

## Method

Train MLPs of shape `(2, k, k, n)` to implement `n` two-input logic gates on
noisy binary inputs. For the **circuit-first** (where-then-what) strategy:
enumerate sub-networks, test which compute the target independently, and for
each search feature interpretations that map intermediate logic-gate values
consistently onto neuron activations. For the **algorithm-first**
(what-then-where) strategy: enumerate subsets of neurons and test causal
alignment by IIA against candidate algorithms' intermediate variables. Repeat
across seeds, widths and task counts.

## Concepts

- **computational abstraction** — the paper's term for a mechanistic
  explanation: a simpler algorithm that tracks the network's internal
  computation, with a *what* and a *where*.
- **where-then-what / what-then-where** — the two strategies. Useful
  vocabulary the field lacked, and the reason the paper can ask four questions
  instead of one.
- **identifiability of explanation** — uniqueness of the valid explanation
  under fixed standards of validity. The import from statistics is the move
  that makes the question precise.
- **IIA** — interchange-intervention accuracy: how well an algorithm's states
  stay aligned with the network's under counterfactual manipulation. An IIA of
  one is the strongest thing the field currently asks for, and many
  explanations achieve it.
- **contrastive underdetermination** — §5.3's framing: Lagrangian and
  Hamiltonian mechanics posit different entities and predict identically. The
  paper raises the possibility that MI is like that, without asserting it.

## Connections

No machine-readable relation is declared: the record holds none of the
circuit-discovery or causal-abstraction line this extends, and it does not
correct or measure itself against a specific paper the corpus has. It is the
first interpretability-methodology document here.

## Recommendations

- **R1** — treat an explanation that passes the criteria as one of many, and
  report what was done to rule out the rest. *Filed* as `SOTA-tmp2f1hx`.
- **R2** — state the epistemic goal the explanation serves. *Folded into R1*,
  because it is the source's own constructive proposal and it is the sentence
  that makes R1 actionable rather than merely deflating.
- **R3** — train on several tasks if you want fewer valid abstractions. **Not
  filed.** `p = 0.05` at one width with a plateau after four tasks is not a
  recommendation, and the reader who acts on it would be changing how they
  train a model in order to make it easier to explain, which is a bigger
  decision than the evidence carries.

## Bearing on the record

Completes a set the record had two thirds of. [SOTA-278](../practices.d/SOTA-278.md) says rule
out the evaluation before reporting a model cannot do something;
[SOTA-286](../practices.d/SOTA-286.md) says measure how much of parameter space behaves like the
part you sampled. Both are about the gap between a demonstration and the claim
it is taken to support. This is that gap at the explanation end, and it is the
sharpest of the three because the criterion is *passed* — nothing looks wrong.

It is also the fifth document today about a reported number being sensitive to
something the report does not state, after `SOTA-305`, `SOTA-307`, `SOTA-308`
and `SOTA-309`. I flagged four as a count rather than a pattern this
afternoon; this is the fifth, and I am still counting rather than concluding.
What would change that is a mechanism, and I do not have one: seed variance in
FID and circuit non-identifiability are not the same phenomenon in any sense I
can defend.

## Limitations

- **Toy models.** `(2, k, k, n)` MLPs on logic gates, with `k ≤ 5` for the
  enumerations. The paper's own §5.4 is about exactly this.
- **One partial demonstration at scale.** The MNIST result enumerates a
  `(3, 3, 3, 1)` tail, not a network anyone would call large, and its
  extension to the full model is an argument rather than an enumeration.
- **The scale defence is burden-shifting.** "If this is true, why the problems
  would disappear at larger scales must be demonstrated" is a good argument
  and is not evidence about large models.
- **The multi-task lever is thin** — `p = 0.05`, one width, plateau at four.
- **Boolean tasks may be unusually degenerate.** A network computing XOR has a
  small, highly symmetric solution space, and whether symmetry is doing the
  work is not separated from whether the criteria are weak.

## Open questions

- **How many circuits satisfy the criteria in a transformer doing a real
  task?** Not enumerable, but samplable: find `k` circuits passing the
  threshold by independent search rather than asserting the first. That is the
  measurement the field could run tomorrow and nobody reports.
- **Does faithfulness in the causal-abstraction sense narrow it?** §5.2 names
  this as the promising direction — requiring excluded components to be
  causally justified rather than merely absent — and does not test it.
- **Is the Boolean setting representative?** The enumeration needs tiny
  models; tiny models may be the unusual case. Establishing that the count
  scales the way §4.1 suggests in a non-Boolean setting would settle whether
  this is a property of the criteria or of the toy.
