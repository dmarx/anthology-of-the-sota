---
number: 91
status: Proposed
formerly:
- THEORY-tmp1aw1p
promote_when: >-
  The consistency reading tested against the intuitiveness reading directly:
  interfaces that are equally consistent but differ in how natural they are
  (an identity mapping against an inversion or a fixed rotation) scored by
  command-to-outcome mutual information and by a held-out usability measure
  taken before users have adapted. If the score cannot tell them apart and
  the early-use measure can, the account holds. The source's bimodal
  convergence is suggestive and was not designed as that test.
title: 'Command-to-outcome mutual information scores an interface because it measures how reliably the operator''s input determines what happens at the chosen horizon, which rewards a learnable channel rather than an intuitive one'
version: 1
tags:
- analysis-and-evaluation
- deployment-and-society
date: '2026-09-23'
source:
- LIT-503
explains:
- SOTA-309
summary: >-
  Reddy, Levine and Dragan (2022), [LIT-503](../literature.d/LIT-503.md). The paper's reason is that an
  intuitive interface makes commands less noisy. Its own results fit a
  narrower account: the score measures how much the operator's input
  determines the state Δ steps later. Users adapt, so any consistent mapping
  scores well, and learned interfaces converge on both no perturbation and
  exact inversion. The account also explains the one failure: an assistant
  that overrides commands to prevent crashes lowers one-step influence and
  raises long-horizon influence.
---

# THEORY-091: Command-to-outcome mutual information scores an interface because it measures how reliably the operator's input determines what happens at the chosen horizon, which rewards a learnable channel rather than an intuitive one

## Source

Reddy, Levine and Dragan (2022), [LIT-503](../literature.d/LIT-503.md), read as [NOTE-250](../notes.d/NOTE-250.md).

## The account

**The paper's version.** Whatever the user is trying to do, an intuitive
interface produces less noisy commands, so the mutual information
`I(x_t, (s_t, s_{t+Δ}))` between command and induced state change rises with
interface quality and needs no knowledge of the task.

**The version its results support.** The quantity measured is how much the
operator's input determines the state `Δ` steps later: how reliable the
channel from what they do to what happens is. That tracks task success
whenever success requires the operator to steer, which is why it ranks
interfaces without labels. It is not a measure of intuitiveness, because the
operator adapts. A mapping they find unnatural but consistent becomes one
they can steer through, and it scores as well as a natural one.

## What it explains

- **The bimodal convergence.** Over 12 users, learned cursor interfaces
  settle on no perturbation (`θ ≈ 0`) and on exact inversion (`θ ≈ π`).
  Both are consistent. Only one is intuitive. The score cannot prefer it,
  and the result shows it does not.
- **The sign flip.** In shared-autonomy Lunar Lander the assistant overrides
  commands to prevent crashes. Commands then determine less of the next
  state and more of the states that follow, because the lander is still
  flying. One-step influence falls and long-horizon influence rises, so the
  correlation with reward is strongly negative at `Δ = 1` and positive at
  episode length. The paper's version does not predict this: the interface
  did not become less intuitive.
- **Why online beats offline** (ρ = 0.87 against 0.43). In the online study
  one user adapts to one interface family on one task, so steerability and
  success are close to the same thing. Across heterogeneous offline domains
  they come apart more.

## Where it is weak

- **It is a reading of one paper's results, not something the paper tests.**
  The bimodal convergence is the evidence for it, and it comes from one
  8-parameter cursor task with 12 users.
- **Consistency and intuitiveness were not separated by design.** No
  condition compares an equally consistent but unnatural mapping against a
  natural one before adaptation, which is the test in `promote_when`.
- **"Determines the outcome" hides the choice of `Δ`.** The account says why
  the horizon matters. It does not say how to pick one without knowing the
  user's timescale, which the source names as its main limitation.

## What it does not say

It does not say the score is wrong to prefer a consistent channel. For a
prosthesis used every day, a mapping the user can learn may be the right
target. The claim is that the score measures learnability, and a reader who
takes it as a measure of intuitiveness will be surprised by an inverted
mouse.
