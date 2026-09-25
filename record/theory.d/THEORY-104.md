---
number: 104
status: Proposed
formerly:
- THEORY-tmp8i6gq
promote_when: >-
  The convergence radius is measured rather than inferred — a sweep of step size
  against guidance scale showing where each solver order starts to converge, or a
  direct measurement of the derivative magnitudes the argument turns on. The FID
  table this rests on is the *consequence* and is not in doubt; what is asserted
  and unmeasured is that a narrowed convergence radius is why. A fourth solver
  family failing the same way would add another consequence, not the mechanism.
title: "A large guidance scale amplifies the model's derivatives, which narrows a high-order solver's convergence radius"
version: 1
tags:
- analysis-and-evaluation
- generative-modeling
- numerics-and-precision
date: '2026-09-25'
source:
- LIT-676
explains:
- SOTA-410
summary: >-
  Lu et al. (2022), [LIT-676](../literature.d/LIT-676.md). Why the fast diffusion samplers invert under
  guidance. Classifier-free guidance scales the difference between conditional
  and unconditional predictions, which amplifies the model's **derivatives** as
  well as its output; a `k`-th order solver is built from `k`-th order
  derivatives, so its convergence radius shrinks fastest for the largest `k`. At
  a fixed evaluation budget the higher-order method is then worse than the lower,
  which is what the measured FIDs show — 13.04, 114.62 and 164.74 at 10
  evaluations for orders 1, 2 and 3.
---

# THEORY-104: A large guidance scale amplifies the model's derivatives, which narrows a high-order solver's convergence radius

## Source

Lu, Zhou, Bao, Chen, Li and Zhu (2022), [LIT-676](../literature.d/LIT-676.md).

## The account

A high-order ODE solver buys accuracy by using derivative information: a
`k`-th order method is a Taylor-style construction whose error term involves
`k`-th order derivatives of the integrand. That is a bargain with a condition
attached — the construction only converges when the step size is inside a radius
set by how large those derivatives are.

Guided sampling breaks the condition. The guided prediction is the unconditional
prediction plus `s` times the difference between conditional and unconditional,
so a large `s` amplifies the function *and everything derived from it*. The
paper's statement:

> large guidance scales may amplify both the output and the derivatives of the
> model … The derivatives of the model affect the convergence range of ODE
> solvers, and the amplification may cause high-order ODE solvers to need much
> smaller step sizes to converge, and thus the higher-order solvers may perform
> worse than the first-order solver. Moreover, high-order solvers require
> high-order derivatives, which are generally more sensitive to the
> amplifications. This further narrows the convergence radius.

Two consequences follow, and both are what make this worth filing rather than
noting in passing.

**The ordering by order inverts, rather than degrading.** If high order merely
helped less under guidance, the ladder would flatten. Instead it reverses,
because the sensitivity to amplification grows with the order — so the method
that is most accurate inside its radius is the one thrown furthest outside it.

**Fixed budget is the whole story.** Nothing here says a high-order solver
cannot reach a good sample under guidance; it says it needs a step size small
enough that the evaluation count is no longer competitive. A claim about solver
order is always a claim at a budget.

## What was actually shown

The consequence, measured. ImageNet 256×256, guidance scale 8.0, no
thresholding, FID at 10 function evaluations: **13.04** for first-order DDIM,
**114.62** for DPM-Solver-2, **164.74** for DPM-Solver-3. The same ordering
persists at 15, 20 and 25 evaluations, with DPM-Solver-3 still at 29.40 where
DDIM is at 9.87. Two other solver families fail the same way — PNDM at order 2
scores 99.80 at 10 evaluations and DEIS at order 3 scores 66.86 — which is what
makes this a property of order under guidance rather than of one implementation.

And the remedy the account predicts is the one that works: reduce the effective
step size by going multistep, and stop raising the order. DPM-Solver++(2M)
reaches 9.10 at 20 evaluations, and the authors decline to go past order 2 at
all — "high-order solvers may be unsuitable for large guidance scales, thus we
mainly consider `k = 2`".

## What this does not say

**The mechanism is argued, not measured.** The paper says "intuitively" and
"may", and the derivative magnitudes are never reported. What is measured is the
FID inversion; the convergence-radius explanation is the reason offered for it,
and the `promote_when` asks for the step-size-against-guidance sweep that would
turn it into a finding.

**It is not the boundedness problem, which is separate and already filed.** The
same paper identifies a second failure — large guidance pushes the converged
`x₀` outside the training data's range — and that is [SOTA-202](../practices.d/SOTA-202.md)'s mechanism,
from Imagen. Thresholding fixes that one and does **not** fix this one; going
multistep fixes this one and does not fix that one. A reader who collapses the
two will expect thresholding to rescue a third-order solver, and it does not.

**It is not an argument against high-order solvers.** Unguided, the ladder runs
the right way up and [SOTA-203](../practices.d/SOTA-203.md) stands — which is the point of bounding that
practice rather than retiring it.
