---
number: 205
status: Read
formerly:
- NOTE-tmp72c2z
paper: LIT-461
title: 'Edge of Stability'
version: 1
date: '2026-09-20'
summary: >-
  Full-batch gradient descent raises the loss Hessian's top eigenvalue until
  it hits `2/eta` and then trains there. Reading it: the three standard
  analytical assumptions fail at every reasonable step size, and the
  curvature-based step-size rule loses to the fixed step size it forbids.
---

<!-- inactive-ok-file: THEORY-030 SOTA-272 — THEORY-030 is Proposed and is cited for what its own promote_when says, which is the gap this reading fills; SOTA-272 is Proposed and filed here from this reading -->
# NOTE-205: Edge of Stability

## Contribution

Before this paper the dynamics of gradient descent on neural objectives had
no simple characterization. It gives one, and the characterization is
uncomfortable: at any step size a practitioner would actually use, the
sharpness rises to `2/eta` and stays, and the training loss becomes
non-monotone over short timescales while continuing to fall over long ones.
What is new is not that oscillation happens — several prior papers saw pieces
of it — but that the resting value is *predictable from the hyperparameter*,
and that this holds across architectures and tasks rather than in one setting.

## Key insight

Gradient descent does not find a step size that suits the landscape; it
*changes the landscape until the landscape suits the step size*, and then
stops there. Progressive sharpening pushes curvature up, instability pushes
it back down at `2/eta`, and the balance is where training lives. The
oscillation this produces is not a malfunction to be damped out: it is the
mechanism by which a fixed step size keeps working.

## Assumptions

- **Full-batch gradient descent.** The characterization is for deterministic
  GD. §6 is explicit that under SGD the sharpness does not settle at any
  fixed value, let alone one predictable from the hyperparameters.
- **Sharpness means the maximum eigenvalue of the training-loss Hessian**, and
  the paper adds a footnote declining any connection to generalization —
  which is the opposite of how the word is used in the flat-minima literature.
- **Reasonable step sizes.** Step sizes small enough to avoid the regime
  exist. The claim that the regime is the rule is an empirical claim about
  what is reasonable on standard architectures and CIFAR-10, not a theorem.
- **Scale.** Small vision architectures on CIFAR-10, plus a Transformer on
  WikiText-2. This record's practices assume decoder-only transformers at
  large batch; nothing here was run at that scale.

## Key results

Empirical rather than theorem-level, which is the paper's own framing.

- **Progressive sharpening** — while sharpness `< 2/eta` it rises, across the
  architectures and tasks tested. *Holds when:* full-batch GD at a step size
  that is not vanishingly small.
- **The `2/eta` ceiling** — once reached, sharpness hovers at or just above
  it for the rest of training, and the loss is non-monotone over short
  timescales. *Holds when:* the same.
- **`L`-smoothness cannot be assumed along the trajectory** — it would require
  sharpness `< 2/eta`, and sharpness sits just above. This is a direct
  consequence of the ceiling, and it applies to *local* `L`-smoothness too.
- **Fixed step size beats the `1/sharpness` rule** (Appendix F) — the
  textbook-optimal adaptive rule is outperformed by `eta = 2/S0`, the fixed
  step the rule calls impermissible. *Holds when:* full-batch GD; the
  experiment is a direct head-to-head.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Sharpness rises to `2/eta` and stays there under full-batch GD | strong | the paper's central experiment, run across architectures, tasks and step sizes |
| C2 | The regime obtains at every reasonable step size on standard vision architectures | moderate | §4 and Figure 7.3 on CIFAR-10; "reasonable" is an empirical judgement, and the architecture set is narrow |
| C3 | Convergence analyses assuming `L`-smoothness or monotone descent do not apply to GD on neural objectives | strong | follows from C1 by the definition of the assumptions |
| C4 | The `eta = 1/sharpness` step-size rule is outperformed by a fixed step size | moderate | one head-to-head in Appendix F, in the full-batch setting only |
| C5 | An analogue holds for SGD | weak | the authors' own suggestion, with an "acclimation" experiment in Appendix H; §6 states the precise characterization does not carry |

## Concepts

- **Sharpness** — the maximum eigenvalue of the training-loss Hessian, and
  nothing else. Explicitly not asserted to relate to generalization.
- **Progressive sharpening** — the tendency of sharpness to rise while it is
  below `2/eta`.
- **Edge of stability** — the regime in which sharpness hovers at or just
  above `2/eta` and the loss falls non-monotonically.

## Connections

The name is borrowed from Giladi et al. (2020). Pieces were seen earlier:
Xing et al. (2018) on non-monotone valley-bouncing, Wu et al. (2018) on
sharpness at convergent solutions being near `2/eta`, Kopitkov and Indelman
(2020) on the NTK eigenvalue flatlining. The paper is candid that
Jastrzębski et al. (2020) conjectured both phenomena for full-batch GD
without running full-batch experiments. [LIT-453](../literature.d/LIT-453.md) is the same first
author carrying this into a quantitative model of the time-averaged
trajectory.

## Bearing on the record

- **[THEORY-030](../theory.d/THEORY-030.md) named this as established premise and the record did not
  hold it.** Its `promote_when` says more evidence for the edge of stability
  "is established and is the premise rather than the claim". That was true of
  the literature and not of the record, which is the gap this fills.
- **It qualifies [THEORY-030](../theory.d/THEORY-030.md)'s own `promote_when` in one direction.**
  The step from full-batch to stochastic that `THEORY-030` says would settle
  it is precisely the step §6 of this paper says has not been taken, five
  years earlier. The gap is old.
- **It produces [SOTA-272](../practices.d/SOTA-272.md)**, on not reading short-timescale
  non-monotonicity as instability and not setting the step size from a
  curvature bound.
- **It is the converse of [SOTA-270](../practices.d/SOTA-270.md)**, which warns against reading a
  smooth curve as smooth training. This warns against reading a rough curve
  as broken training. Both are about the curve being a poor instrument.

## Limitations

- Full-batch only, stated by the authors as the first limitation. Nobody
  trains this way.
- Small scale: CIFAR-10-class vision models and a WikiText-2 Transformer.
- No claim that sharpness relates to generalization, so nothing here licenses
  the flat-minima inferences a reader may be primed to make.
- The `1/sharpness` comparison is one experiment, not a study.
- Explanatory rather than predictive: the paper says what happens, and is
  explicit that it hopes others will explain why.

## Open questions

- What is the stochastic analogue, and is there a resting value predictable
  from `eta` and batch size? Five years on, [THEORY-030](../theory.d/THEORY-030.md) still names
  this as the open step.
- Does the ceiling hold at frontier scale, where nothing in this paper was
  run?
- Why does progressive sharpening happen at all? The paper reports it and
  does not account for it.
