---
number: 309
status: Proposed
formerly:
- SOTA-tmplzyt9
promote_when: >-
  The horizon dependence characterized rather than worked around: a second
  setting where the same interface data is scored at several values of `Δ`
  and the correlation with a held-out task metric is reported as a curve, so
  that somebody choosing `Δ` without task knowledge can see how wrong they
  can be. What would not meet it: another system reporting a good correlation
  at a single hand-picked `Δ`, which is what this source's positive results
  already are.
consensus: unreplicated
consensus_note: >-
  One group, one paper, five domains and two user studies — and the closest
  prior work it names (PCA-based co-adaptation) requires a linear interface
  and does not optimize intuitiveness, so there is no competing measurement
  to agree or disagree with. The underlying infomax idea is old; its use as
  an interface score is this.
title: "Score a control interface by the mutual information between the operator's command and the state change it induces, and choose the horizon of that state change deliberately"
version: 1
tags:
- training-optimization
- analysis-and-evaluation
- deployment-and-society
date: '2026-09-21'
source:
- LIT-503
introduced_by:
- LIT-503
implementations: []
summary: >-
  Reddy, Levine and Dragan (2022), [LIT-503](../literature.d/LIT-503.md) — whatever the
  operator is trying to do, a better interface yields less noisy commands, so
  `I(x_t, (s_t, s_{t+Δ}))` scores it with no labels, no reward and no task
  knowledge. Spearman **ρ = 0.43** against true task completion across 540K
  examples in **4 of 5** domains. In the fifth the correlation was **strongly
  negative** at `Δ = 1` and positive at episode length — so the horizon is not
  a detail.
---

# SOTA-309: Score a control interface by the mutual information between the operator's command and the state change it induces, and choose the horizon of that state change deliberately

## Source

Reddy, Levine and Dragan (2022), [LIT-503](../literature.d/LIT-503.md) — read as
[NOTE-250](../notes.d/NOTE-250.md).

## When this applies

A person is steering a system through a learned or configurable mapping — a
prosthesis, a gaze or gesture interface, a shared-autonomy controller, any
assistant that takes a noisy human signal and turns it into an action — and
you cannot obtain labels of what they meant, reward for what they achieved, or
a list of the tasks they will attempt.

## Do this

**Score the mapping by `I(x_t, (s_t, s_{t+Δ}))`** — the mutual information
between the operator's raw command and the state transition that follows. The
argument is task-independent: whatever they are trying to do, an interface
they can use produces commands that explain the outcome, and one they cannot
produces commands that do not.

It ranks existing interfaces offline (Spearman `ρ = 0.43` against ground-truth
task completion across 540K examples), and it can be maximized directly:
randomly initialize the mapping, let the user attempt their own tasks,
estimate the score, and update by reinforcement learning. In a 12-participant
cursor study that learned a usable interface **in under 30 minutes** with no
user feedback, reaching `ρ = 0.87` against true task reward.

**Then choose `Δ` on purpose, because the sign depends on it.** This is the
part to carry:

In the shared-autonomy Lunar Lander data the assistant helps by *overriding*
the user to stop them crashing. Overriding commands is exactly what lowers
one-step mutual information — and it *raises* the user's influence over later
states, because they are still flying. At `Δ = 1` the correlation with true
reward was **strongly negative**. Set `Δ` to the episode length and it turns
positive.

So a one-step influence metric punishes an assistant for assisting. If the
operator's command is a statement about what should happen next, a short
horizon is right; if it is a statement about where they want to end up, only a
long one is.

## Conditions

**The horizon reintroduces the dependency the method removes.** Choosing `Δ`
"requires prior knowledge of the timescale of the user's desired influence
over the system", which the source names as **"the primary limitation on the
generality of our method"**. The abstract calls the objective "completely
unsupervised"; it is unsupervised given a hyperparameter that encodes what the
user is trying to do. That is still a large reduction in what you must know,
and it is not nothing.

**Four of five domains, and the fifth is the informative one.** The average
`ρ = 0.43` is over the four that worked. A reader taking "predictive of the
ground-truth task completion metrics in a variety of domains" from the
abstract will not know that the fifth inverted.

**`ρ = 0.43` is moderate.** It ranks interfaces usefully; it will not
adjudicate between two similar ones. The online figure (0.87) is much better
and is also the easier setting — one user, one task family, interfaces varying
within a parameterized family.

**Eight parameters is the largest interface tested**, limited by user-study
duration and the data efficiency of the Bayesian optimization used for the RL.
Nothing here establishes that the objective survives a high-dimensional
policy, and the source names that as future work.

**What the objective actually rewards is a usable channel, not an intuitive
one.** Over 12 users the learned perturbation angle converges to two modes:
no perturbation and *exact inversion*. Both are consistent mappings a person
can learn. The motivating sentence is about intuitiveness; the measured
quantity is reliability of the command-to-outcome relation, and an inverted
mouse scores well on it.

**Small studies.** Twelve participants in the user study, twelve in each
offline evaluation, one expert user for the gesture-controlled Lunar Lander.

## Related

The horizon result belongs with the record's other measurement traps:
[SOTA-305](../practices.d/SOTA-305.md) (a reconstruction FID needs its token count),
[SOTA-307](../practices.d/SOTA-307.md) (a generation FID needs an error bar over training seeds)
and [SOTA-308](../practices.d/SOTA-308.md) (recall bought with relevance). This is the sharpest
of them, because what changes with the measurement choice is the **sign** of
the correlation rather than its size — and the failure lands precisely on the
system that is working best.
