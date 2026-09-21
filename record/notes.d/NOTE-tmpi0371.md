---
status: Read
paper: LIT-tmpzynnf
title: 'SQ hardness for semiautomata, and the regime it needs'
version: 1
date: '2026-09-21'
summary: >-
  Read from the [#180](https://github.com/dmarx/anthology-of-the-sota/issues/180) worklist. The theorem is clean and the regime it
  needs — an alphabet cubic in the number of states — is what a citing reader
  will drop. Filed for the mental model underneath it, which the record had
  nothing for: longer random sequences carry *less* information about a hidden
  transition structure, not more.
---

<!-- inactive-ok-file: THEORY-tmp38xax — Proposed, filed in this same
     contribution; the Recommendations and Open questions sections name it as
     where R1 went and what would move it, which is the note's job -->

<!-- inactive-ok-file: SOTA-178 — Proposed, cited in "bearing on the record"
     to distinguish expressivity from learnability. The distinction is the
     point of the citation and does not depend on either being settled -->

# NOTE-tmpi0371: SQ hardness for semiautomata, and the regime it needs

## Contribution

The first Statistical Query hardness result for semiautomata, and — more to
the point — the first automaton hardness result that does not smuggle in a
hard language. Every previous SQ lower bound for finite automata works by
embedding parity or a similar function into what the machine accepts, usually
under an input distribution chosen adversarially. A semiautomaton has no
accepting states and no language, so that route is closed. The hardness is
made to come from the transition functions alone, under the uniform
distribution.

The method is the other contribution: reading a random word is a random walk
on `S_N × S_N`, indistinguishability is a mixing question, and one irreducible
representation controls it. That reframing is what makes the calculation
finite, and it is new for automata learning.

## Key insight

Feeding a state machine uniformly random symbols is stirring it. Two different
machines started in the same state drift apart until they agree only as often
as chance — `1/N` — and the approach to chance is exponential in the number of
symbols read. So the quantity that would tell a learner which machine it is
looking at *decays with sequence length*. Longer random inputs are not more
evidence; they are less.

## Assumptions

- Uniform distribution over both the input word **and** the initial state. Not
  adversarial, which strengthens the result, and not a natural data
  distribution either.
- The family is built by matching alphabet letters to **transpositions** and
  assigning them by fair coin flips. Transpositions are what make the walk
  analyzable via Diaconis–Shahshahani; a different generating set is a
  different problem.
- **Alphabet size `Ω(N³ ln N)`**, word length `Ω(N² ln N)`, family size `N!`.
  The bound is asymptotic in `N` with the alphabet growing cubically.
- The learner is an SQ learner. The claim about gradient descent is imported
  from Abbe et al. (2021), whose equivalence holds **with large mini-batches
  or low-precision gradients**.

## Key results

- **Theorem 4.1 (agreement probability)** — for two semiautomata reading the
  same uniformly random word from the same uniformly random start,
  `P_agree(T)` is determined solely by the Fourier transform of the transition
  operator at the irreducible representation `Π₀ = std ⊗ std` of `S_N × S_N`.
  Exponentially many irreducibles collapse to one.
- **Lemma 5.1** — for a randomized `(k, N!)`-shuffle family, the spectral norm
  of `M_{Π₀}` is at most `1 − 1/(2N)` with high probability. Proved by an
  expectation-concentration argument: Schur's lemma for the expectation
  (`1 − 1/(N−1)`), matrix Bernstein for the deviation.
- **Theorem 5.1** — consequently `P_agree(T) = 1/N + error` with
  `|error| ≤ (1 − 1/(2N))^T`, with probability at least `1 − exp(−N ln N)`.
  At `T = O(N² ln N)` and `k = O(N ln N)` — total alphabet `O(N³ ln N)` — the
  error is driven below `1/N!`.
- **Theorem 5.2 (tightness)** — `T = Ω(N² ln N)` is necessary; the mixing time
  of the walk cannot be beaten. *Stated as of independent interest, and it is.*
- **Theorem 6.2 (SQ lower bound)** — SQ dimension at least `N!`, so any SQ
  learner for the class makes super-polynomially many queries or uses
  super-polynomially small tolerance.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Learning semiautomata is SQ-hard under the uniform distribution | strong | Theorems 5.1 and 6.2, proved |
| C2 | The hardness is structural rather than language-based | strong | there is no language in the object; the construction carries the whole argument |
| C3 | Distinct machines become statistically indistinguishable exponentially in word length | strong | Theorem 4.1 with Lemma 5.1 |
| C4 | The mixing time is tight | strong | Theorem 5.2 |
| C5 | This has direct implications for a wide range of practical algorithms | weak | one sentence of related work citing Abbe et al. (2021), with that equivalence's conditions named but not examined, and nothing built on it |

## Method

*(Analytic; no experiments anywhere in the paper.)* Construct `N!`
semiautomata by assigning transpositions to alphabet letters by fair coin
flips. Couple two of them reading the same random word into a single walk on
`S_N × S_N`. Expand the agreement probability in irreducible representations
of that group and show only `std ⊗ std` survives. Bound that block's spectral
norm in expectation by Schur's lemma and in deviation by matrix Bernstein.
Convert the resulting pairwise correlation bound into an SQ dimension via Blum
et al.'s characterization.

## Concepts

- **semiautomaton** — a state set and transition functions, with *no* initial
  state and *no* accepting states. A DFA minus the parts that define a
  language. The distinction is the whole paper: it removes the place previous
  proofs hid their hardness.
- **SQ model** — the learner asks for expectations of bounded functions of the
  data up to a tolerance, rather than reading individual examples. Robust to
  noise by construction, and the reason it matters here is its relation to
  large-batch SGD.
- **SQ dimension** — roughly, how many pairwise-uncorrelated concepts the class
  contains. Large SQ dimension implies an SQ lower bound.
- **`P_agree`** — the probability two machines are in the same state after `T`
  symbols from a common random start. The baseline is `1/N`, which is chance.

## Connections

Directly complements Wang et al. (2025) on `k`-fold composition, which the
paper describes as a restricted subclass of semiautomata with
time-inhomogeneous transitions, proved by recursive algebraic calculation
where this uses representation theory. The open problem it gestures at —
Angluin et al.'s question about learning random DFAs under the uniform
distribution — is explicitly *not* solved here; the authors say they hope it
is a first step.

No machine-readable relation is declared: the record holds neither Wang et al.
nor the DFA hardness line, so there is nothing to relate to.

## Recommendations

- **R1** — when a model fails to learn a state-tracking task, do not conclude
  the architecture cannot represent it. Representability and learnability are
  different limits, and this paper is a case where the object is trivially
  representable and provably hard to learn by a broad class of algorithms.
  **Not filed as a practice**, because the evidence is a proof about a family
  in a regime nobody trains in. Carried as `THEORY-tmp38xax` instead, which is
  the honest shape: a claim about what is true, not an instruction.
- **R2** — do not train on uniformly random sequences when what you want
  learned is a hidden transition structure, and expect longer random contexts
  to make it worse rather than better. **Not filed**, and it is the thing I
  most wanted to file. See Open questions.

## Bearing on the record

Adds an axis the limits cluster did not have. `SOTA-178` recommends
vector-valued gating and in-context learning rates "so it can track state a
softmax layer provably cannot", and `THEORY-038` says a decoder cannot compose
over a long context in few layers. Both are **expressivity** claims: what the
architecture can represent. This is a **learnability** claim: whether gradient
descent finds it. They can disagree in the direction that matters — an
architecture that comfortably represents a machine can still be unable to
learn it — and nothing in the record said so.

`SOTA-278` (rule out the evaluation before reporting a model cannot do
something) is adjacent and about a third thing: measurement. Three different
reasons a capability can look absent, and the record now names all three.

## Limitations

- **The alphabet is cubic in the state count.** `Ω(N³ ln N)` symbols for `N`
  states — about 4.6 million symbols for a hundred-state machine. No realistic
  sequence task has that shape, and the result says nothing about the
  small-alphabet automata that motivate the applications listed in the
  abstract.
- **One constructed family, built from transpositions.** The theorem is an
  existence result: *there is* a hard family. It is not a claim that semiautomata
  encountered in practice are hard, and the authors do not make that claim.
- **No experiments.** Not a criticism of a theory paper, but it means the
  distance between the theorem and any training run is entirely unmeasured.
- **The SGD bridge is one sentence.** "Suggesting our hardness result has
  direct implications for a wide range of practical algorithms" is the most
  quotable line in the related-work section and is the weakest thing in the
  paper — it rests on Abbe et al.'s equivalence, whose conditions (large
  mini-batch **or** low precision) are named and never revisited. How tight
  that equivalence is in the regimes people actually train in is not
  addressed.
- **The open problem stays open.** Learning random DFAs under the uniform
  distribution, Angluin et al.'s question, is not resolved; this is a
  different random model.

## Open questions

- **Does the mixing effect show up at realistic alphabet sizes?** The theorem
  needs `Ω(N³ ln N)`; the interesting question is what happens at, say,
  alphabet 2 to 256. `P_agree` still converges to `1/N`, just more slowly, and
  a measurement of the rate at practical `N` and `k` would say whether the
  mental model transfers at all. This is a cheap experiment — simulate walks,
  no training needed — and nobody has run it.
- **Does a transformer trained on random words actually fail, and does it fail
  worse with longer contexts?** That is R2's missing evidence, and it is the
  result that would turn `THEORY-tmp38xax` into a practice about what
  sequences to train on. A non-uniform curriculum should help by the same
  argument, which makes it jointly testable.
- **How tight is the SQ–SGD equivalence at the batch sizes and precisions in
  use?** Everything practical in this paper passes through that one citation,
  and the record should not treat SQ hardness as gradient-descent hardness
  until somebody quantifies the gap.
