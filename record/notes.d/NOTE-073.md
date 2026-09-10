---
number: 73
status: Read
formerly:
- NOTE-tmpz67rs
paper: LIT-018
title: 'On the Convergence of Adam and Beyond'
version: 1
tags:
- training-optimization
date: '2026-09-09'
summary: >-
  Constructs a one-dimensional convex problem on which Adam provably converges to the worst point in the feasible set, locating the error in the original convergence proof and in the exponential moving average itself. Proposes AMSGrad, which keeps the running maximum of the second moment so the effective learning rate is non-increasing. ICLR 2018 best paper; almost nobody runs AMSGrad.
---

# NOTE-073: On the Convergence of Adam and Beyond

## Contribution

A disproof, and a repair. The disproof is the substantial half: an explicit
**one-dimensional convex** online optimisation problem on which Adam converges
to `x = +1` when the minimiser is `x = −1` — not slowly, not approximately,
but to the opposite end of the feasible set. This contradicts the convergence
theorem in the original Adam paper, and the paper identifies exactly where
that proof fails.

The repair is **AMSGrad**: keep `v̂_t = max(v̂_{t−1}, v_t)` instead of `v_t`,
so the denominator never shrinks and the effective per-parameter learning rate
is non-increasing.

## Key insight

The failure is not a subtlety of the analysis; it is what an exponential
moving average *is*. Adam's `v_t` forgets at rate `β₂`, so it is effectively a
window over the recent past. The counterexample exploits this directly:
present a large informative gradient `C` once every three steps and a
misleading gradient `−1` on the other two, with `β₁ = 0` and
`β₂ = 1/(1+C²)`. The rare large gradient is divided down by roughly `C` before
it acts, so the two small wrong-direction steps outweigh the one large right
one, every cycle, forever.

The general statement is the one worth carrying: **any method that scales
updates by a fixed-size window of past gradients has this failure mode.** It is
a property of the forgetting, not of Adam. Adagrad, which accumulates without
forgetting, does not have it — and that is the clue the fix follows.

## Assumptions

- **Online convex optimisation with regret as the criterion.** The
  counterexample and the AMSGrad guarantee both live here, not in the
  non-convex setting where Adam is actually used.
- The counterexample needs `β₁ = 0` and a `β₂` tied to `C`; the paper
  generalises it, but the headline instance is constructed rather than
  observed.
- Bounded feasible set with projection.

## Key results

- **Adam fails on a convex 1-D problem**, by construction and by proof
  (induction on the iterates: `x_{3t+1} = 1` for all `t`).
- **The original convergence proof is wrong**, and the paper says which
  quantity — `Γ_t`, the change in the effective learning rate between steps —
  is assumed to have a sign it need not have.
- **AMSGrad** restores an `O(√T)` regret bound by making the effective step
  size monotonically non-increasing.
- The empirical section is honestly labelled **"a preliminary empirical
  study"** — AMSGrad performs similarly to or somewhat better than Adam on
  logistic regression, a small neural net and CIFARNET.
- **AdamNC** is also offered: Adam with `β₂` increasing toward 1 over training,
  which recovers Adagrad-like accumulation in the limit.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Adam can converge to the worst point of a convex feasible set | strong | explicit construction plus proof |
| C2 | The published convergence proof is incorrect | strong | the faulty step is identified |
| C3 | The cause is the fixed-window forgetting, not Adam's other parts | strong | argued generally; Adagrad's immunity is the control |
| C4 | AMSGrad has `O(√T)` regret | strong | proved |
| C5 | AMSGrad is better in practice | **weak — the authors say so** | "preliminary", small-scale |

## Method

Take Adam. Replace `v̂_t` with the running maximum of `v_t`. Nothing else
changes; the cost is one extra buffer and an elementwise max.

## Concepts

- **The `Γ_t` quantity** — the per-step change in effective learning rate,
  which the original proof assumed positive semi-definite. Naming it is what
  turns "Adam sometimes misbehaves" into a locatable defect.
- **Long-term memory of past gradients** — the paper's own framing of the fix,
  and the axis along which Adagrad, RMSProp, Adam, AMSGrad and AdamNC all sit.

## Connections

<!-- inactive-ok-block: LIT-101 — Proposed, and named as one of the wave this paper licensed, not as evidence -->
Sits between Adagrad/RMSProp and the 2018–2022 wave of Adam variants — RAdam,
AdaBelief, AdaBound, Yogi, and `LIT-101` — nearly all of which cite this paper
as their licence to modify Adam. `LIT-156` is the retrospective on that whole
wave: challengers are tuned less carefully than the baseline and measured too
early, which is a fair description of C5 here.

## Recommendations

- **R1** — Do not treat a published convergence proof as settling anything
  about an optimizer you rely on. *Topic:* analysis and evaluation.
  *Strength:* strong, and the paper's most durable contribution.
- **R2** — If an adaptive method's denominator can shrink, a rare large
  gradient can be permanently outvoted by frequent small ones. *Topic:*
  training optimization. *Strength:* strong — this is the mechanism, and it
  is why sparse-feature and large-output-space settings are where people
  actually hit it.
- **R3** — Use AMSGrad. *Strength:* **weak**, and the field's revealed answer
  is no. Worth stating as the anthology's rule that a proof of correctness is
  not a reason to switch optimizers.

## Bearing on the record

**Nothing is sourced to this paper, and this reading files no practice.** That
is the right outcome and the interesting one: `SOTA-001` says use Adam by
default, and this paper proves Adam can fail on a convex problem. Both stand.
The gap between them is R3 — a correctness result that practice declined to
act on, because the failure mode is constructed and the fix costs memory for
no measured gain.

Worth keeping visible rather than resolving, because it is the cleanest case
in the corpus of the anthology's own premise: **what people do and what is
provably correct are different questions**, and the record tracks the first.

The document's four takeaways — "identifies convergence issues in Adam",
"proposes AMSGrad variant", "provides theoretical convergence guarantees",
"improved adaptive optimization" — are true and empty. The last one is also
the paper's weakest claim stated as fact.

## Limitations

- Convex online optimisation. Every result is in a setting Adam is not used in.
- The counterexample is adversarial, and no one has shown the mechanism firing
  in a real training run at scale.
- C5 is preliminary by the authors' own description, and eight years of
  non-adoption is the field's answer to it.

## Open questions

- Does the mechanism ever fire in practice, or only by construction? Nobody
  seems to have looked, and "rare large gradient outvoted by frequent small
  ones" is a describable thing to instrument.
- AMSGrad costs one extra state buffer per parameter. At current scales, that
  is the reason not to use it — which means the trade was never about
  correctness.
