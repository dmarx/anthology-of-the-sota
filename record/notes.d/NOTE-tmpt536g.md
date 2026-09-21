---
status: Read
paper: LIT-tmp36izs
title: 'MIMI: the objective that needs the knowledge it assumes away'
version: 1
date: '2026-09-21'
summary: >-
  Read from the [#180](https://github.com/dmarx/anthology-of-the-sota/issues/180) worklist in rank order. The headline is a
  task-agnostic interface score; the durable finding is its failure case,
  where an assistant doing its job drives the metric *negative* and the fix is
  a horizon hyperparameter that requires exactly the task knowledge the
  objective was built to avoid.
---

<!-- inactive-ok-file: SOTA-tmplzyt9 — Proposed, filed in this same
     contribution; the Recommendations section names it as where R1 went and
     Bearing names what would move it, which is the note's job -->

# NOTE-tmpt536g: MIMI: the objective that needs the knowledge it assumes away

## Contribution

An answer to a genuinely hard problem: how do you fit a human-machine
interface when there is no prior mapping, no action labels, no reward signal,
and no list of what the person is trying to do? The proposal is that
intuitiveness has a task-free signature — a good interface makes a person's
commands informative about what happens — so the mutual information between
command and induced state transition can stand in for a task metric nobody
can observe.

Two uses: ranking existing interfaces offline, and maximizing the score
directly by human-in-the-loop RL to build one from scratch.

## Key insight

You cannot see what the user wants, but you can see whether their inputs
explain the outcomes. A channel the operator cannot use produces commands
uncorrelated with what follows, whatever they were for. That makes interface
quality measurable without ever naming the task — and it makes *what counts
as "what follows"* the whole question, which is where the paper's most useful
result lives.

## Assumptions

- The interface can observe the state `s_t`. The paper notes this fails when
  the user can see things the interface cannot (they look around; it has no
  camera) and calls that an extension.
- A parameterized interface family small enough for Bayesian-optimization RL:
  the largest tested has **8 parameters**.
- The user adapts too — this is *co*-adaptation, and the objective is
  estimated on a moving target.
- A horizon `Δ` is fixed before scoring.

## Key results

- **Offline validation.** 540K examples of keyboard and eye-gaze interfaces
  for typing, simulated robot control and games. In **4 of 5** domains the MI
  score is predictive of ground-truth task reward, average Spearman
  **ρ = 0.43**. The X2T eye-gaze arm alone gives ρ = 0.45 over 36 points
  (12 users × 3 conditions).
- **The inversion.** In the shared-autonomy Lunar Lander (SAvDRL) data, the
  one-step objective gave "a strong negative correlation" with reward. Cause,
  in the authors' words: the assistant prevents crashes, "which necessarily
  involves ignoring a large fraction of the user's commands" — lowering
  `I(x_t, (s_t, s_{t+1}))` while *increasing* the user's influence over later
  states. Generalizing to `I(x_t, (s_t, s_{t+Δ}))` and setting `Δ` to the
  maximum episode length (`10³`) restores a positive correlation.
- **The admission.** "Choosing the value of `Δ` requires prior knowledge of
  the timescale of the user's desired influence over the system... This is the
  primary limitation on the generality of our method." Repeated in §6.1.
- **Online learning.** 12 participants, 2D cursor control through a perturbed
  mouse. MIMI substantially beats randomly parameterized interfaces and
  approaches an oracle that moves straight to the target, in under 30 minutes.
  MI reward and true task reward correlate at **ρ = 0.87**.
- **What it converges to.** The learned perturbation angle `θ` over 12 users
  is sharply bimodal: `θ ≈ 0` (no perturbation) and `θ ≈ π` (exact inversion),
  against a uniform random baseline. Trajectories go from curved and wandering
  to straight after 150 episodes.
- **Lunar Lander by hand gesture**, one expert user: the learned interface
  works, and "does not enable the user to fire the left thruster in isolation"
  — every gesture that fires it also fires the main engine.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | MI between command and induced transition ranks interfaces without task knowledge | moderate | 540K examples, five domains — four of which worked, at ρ = 0.43 |
| C2 | The objective can be maximized to learn an interface from scratch | moderate | 12-participant study, 8-parameter interface, one task family |
| C3 | The correlation's **sign** depends on the horizon `Δ` | strong | the SAvDRL sweep, with a mechanism that explains it |
| C4 | Choosing `Δ` needs task knowledge | strong | stated twice by the authors as the primary limitation |
| C5 | The objective is "completely unsupervised" | weak | true except for `Δ`, and `Δ` is where the task knowledge went |
| C6 | It scales beyond 8 parameters | — | not claimed; named as future work |

## Method

Estimate `I(x_t, (s_t, s_{t+Δ}))` from logged interaction. To learn: randomly
initialize the interface parameters, let the user attempt their own tasks,
estimate the score over the resulting episodes, and update the parameters with
Bayesian-optimization reinforcement learning against that score as reward. No
labels, no reward feedback, no task list — and `Δ` set in advance.

## Concepts

- **MIMI** — the method: mutual information maximizing interfaces.
- **generalized MI objective** — `I(x_t, (s_t, s_{t+Δ}))`, the one-step
  version at `Δ = 1`. The generalization is presented as a fix and is better
  read as the discovery.
- **co-adaptation** — the user learns the interface while the interface learns
  the user. It is why the bimodal convergence to inversion is not simply a
  failure: users adapt to a consistent mapping.
- **infomax** — the older principle the authors connect to in future work.

## Connections

The nearest prior work the paper names is PCA-based unsupervised
co-adaptation, which requires a linear interface and does not optimize
intuitiveness. The record holds neither that line nor anything else on
assistive interfaces, so no relation is declared and none is missing.

## Recommendations

- **R1** — score a control interface by command-to-outcome mutual information
  when labels and rewards are unavailable, and choose the horizon
  deliberately. *Filed* as `SOTA-tmplzyt9`, with the horizon in the title
  because the sign depends on it.
- **R2** — do not read a one-step influence metric as a measure of how well an
  assistant is helping. **Folded into R1's Conditions** rather than filed
  separately: it is the same measurement fact stated from the assistant's side
  rather than the interface's, and one source should not produce two
  practices about one table.

## Bearing on the record

The horizon result joins the four measurement traps the record picked up
today: [SOTA-305](../practices.d/SOTA-305.md) (reconstruction FID needs its rate),
[SOTA-307](../practices.d/SOTA-307.md) (generation FID needs seeds), [SOTA-308](../practices.d/SOTA-308.md)
(recall bought with relevance), and this. It is the sharpest of the set,
because the measurement choice flips the **sign** of the correlation rather
than shifting its magnitude, and because the flip happens exactly when the
system under test is working — an assistant that successfully prevents a crash
looks worst.

Four instances now, from four unrelated fields, all of the form "the reported
number is sensitive to a choice the report does not state". I am recording the
count and not writing the principle: `DP-009`, and the four are not obviously
one mechanism.

## Limitations

- **Four of five domains**, and the abstract says "a variety of domains" with
  the average taken over the four.
- **`Δ` is the load-bearing hyperparameter** and its correct value is task
  knowledge. The paper is admirably direct about this; the abstract's
  "completely unsupervised" is not.
- **`ρ = 0.43` is moderate.** Adequate for ranking, not for close calls. The
  0.87 online figure comes from an easier setting.
- **Eight parameters.** No evidence the objective survives a high-dimensional
  interface, and the data efficiency of the RL is the binding constraint.
- **Small `n` everywhere**: 12 participants in the study, 12 per offline
  evaluation, and a single expert user for the gesture experiment.
- **Consistency versus intuitiveness.** The convergence to `θ ≈ π` shows the
  objective rewarding a mapping the user can learn rather than one they find
  natural. That may be the right target — the paper does not distinguish them.

## Open questions

- **How wrong can `Δ` be?** The measurement that would move this from
  `Proposed`: correlation against a held-out task metric as a *curve* over
  `Δ`, in a second setting, so somebody picking `Δ` blind can see the cost.
  The paper has this curve for SAvDRL (Fig. 2d) and for one domain only.
- **Does it survive a high-dimensional interface?** Named as future work, with
  specific algorithms suggested. Until then the method is demonstrated on
  8 parameters.
- **Is the bimodal convergence a feature?** If the objective reliably finds
  *some* consistent mapping rather than the natural one, then it is a
  learnability score and should be described as one — which would be a
  stronger claim than the paper makes and a different one.
