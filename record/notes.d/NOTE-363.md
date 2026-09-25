---
number: 363
status: Read
formerly:
- NOTE-tmp3z8n7
paper: LIT-707
title: 'Dropout as ensemble learning'
version: 1
date: '2026-09-25'
summary: >-
  In a teacher-student soft-committee simulation, dropout at p = 0.5 beats a
  fixed two-way split of the same network trained as an ensemble, and
  matches a tuned L2 penalty. That is the whole result: curves averaged over
  10 trials, with no derivation, no numbers, one `p` and one toy model.
---

# NOTE-363: Dropout as ensemble learning

## Contribution

A simulation contrasting dropout with an ensemble built from the same units.
One 100-unit student is trained with dropout at `p = 0.5`. Two 50-unit
students are trained independently and averaged. The finding is that
redrawing which half is trained at every step does better than fixing the
halves.

## Key insight

If dropout is an ensemble of subnetworks, it is not the ensemble you would
build on purpose. Its members share weights and are reshuffled every step,
and in this toy setting that is better than independent members. So "dropout
is an ensemble" cannot by itself explain why dropout helps.

## Assumptions

- Soft-committee machine. Hidden-to-output weights fixed at +1,
  `g(x) = erf(x/√2)`, squared error.
- Inputs i.i.d., zero mean, unit variance. Teacher weights i.i.d. with variance
  `1/N`. The thermodynamic limit is invoked for the setup, but no limit
  equations are used.
- `N = 1000`, teacher 2 hidden units, student 100, `η = 0.01`. A fixed set of
  `N` inputs is reused on-line to make overfitting possible.

## Key results

- **Fig. 4.** Plain SGD overfits: learning and test error diverge. With dropout
  the gap is smaller.
- **Fig. 5.** An ensemble of two 50-unit students beats one 50-unit student.
  Dropout on one 100-unit student reaches a lower test MSE than the ensemble.
  Average of 10 trials, curves only.
- **Fig. 6.** SGD with an L2 penalty reaches "almost the same" residual error as
  dropout.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | At test time a dropout network can be read as an ensemble of trained and untrained half-networks | weak | Informal argument around Eq. 6, stated for `p = 0.5` only |
| C2 | Dropout beats an architecture-matched ensemble of independently trained halves | weak | Fig. 5(a) vs 5(b), a cross-panel visual comparison, one toy model, one `p`, no numbers |
| C3 | Dropout's regularization equals L2's | weak | Fig. 6 vs Fig. 5(b) visually; `α` unreported; i.i.d. unit-variance inputs make a data-scaled penalty and plain L2 hard to tell apart |
| C4 | Dropout has no tuning parameter, unlike L2 | weak | None: `p` is a tuning parameter, and only 0.5 is run |

## Concepts

- **Soft-committee machine** — a two-layer network whose output is the
  unweighted sum of its hidden units.
- **Dropout learning / ensemble learning** — the paper's names for training one
  network with random unit subsets, and for averaging independently trained
  subnetworks.

## Connections

It builds on Hinton et al. 2012 ([LIT-394](../literature.d/LIT-394.md)) for the method and on Hara and
Okada's on-line ensemble-learning theory, which is not in the record. It cites
Wager et al. ([LIT-396](../literature.d/LIT-396.md)) for the L2 comparison but does not engage with that
paper's result that the penalty is data-dependent.

## Recommendations

None that this paper supports.

## Bearing on the record

- **No practice or theory is filed from it**, and it is not added as a
  source anywhere. Its evidence is too thin to carry a claim.
- **[THEORY-016](../theory.d/THEORY-016.md)**: consistent. That account says the ensemble reading explains
  why the test-time rule is cheap, not why dropout generalizes. C2, weak as it
  is, points the same way. The advantage appears exactly where dropout departs
  from an ordinary ensemble.
- **[THEORY-015](../theory.d/THEORY-015.md)**: not contradicted. C3's "same as L2" was measured with
  isotropic unit-variance inputs. There the data-scaled penalties [THEORY-015](../theory.d/THEORY-015.md)
  collects, such as Baldi and Sadowski's `Σ wᵢ² Iᵢ² Var(δ)`, reduce in
  expectation to an isotropic one. The experiment could not have separated
  them.

## Limitations

- No analytic result, despite a setup built for one.
- One `p`, one architecture, one teacher, curves only, and no variability
  shown.
- The printed L2 update subtracts a scalar `α‖J‖²` from a vector, and `α` is
  not given.
- The authors' stated future work is ReLU networks, so the erf setting is
  acknowledged as a limitation.

## Open questions

- Does the dropout-over-ensemble advantage survive at other `p`, and against
  ensembles whose members do not share a training budget?
- An order-parameter analysis of dropout in this model would turn C2 into a
  result. That is what the teacher-student setup is for.
