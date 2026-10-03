---
status: Active
promote_when: >-
  Active for the mechanism, which is proved: the learned velocity is the
  average of the conditional velocities through a point, its irreducible
  loss is their spread, and a coupling whose paths do not cross makes it
  straight. Three applications are only illustrated. That straightening is
  what buys few-step quality has controlled evidence at 64 px and below,
  unconditional, in pixel space. That one reflow leaves a flow nearly
  straight is argued from a geometric intuition the authors say they do not
  prove. That a straighter teacher is easier to distil is offered as a
  suggestion by the paper whose controlled comparison it would explain. Each
  would be settled by a run that reports measured straightness beside
  few-step FID for the same model under independent, minibatch-OT and
  reflowed couplings, at 256 px or above with a condition. A new
  few-step result that changes the coupling together with the loss, the
  initialization or the distiller would not settle any of them.
title: "A flow's sampling ODE curves because the noise-data pairs it was trained on cross and the learned velocity averages them, so a coupling whose straight paths do not cross gives a straight flow"
version: 1
tags:
- generative-modeling
- flows-and-transport
- few-step-generation
date: '2026-10-03'
source:
- LIT-tmprjg3i
- LIT-tmpzz36v
- LIT-636
- LIT-tmptpra5
- LIT-tmpyqrl4
extends:
- THEORY-106
explains:
- SOTA-tmphvn35
- SOTA-392
summary: >-
  Pooladian et al. (2023), [LIT-tmprjg3i](../literature.d/LIT-tmprjg3i.md), and Tong et al. (2023),
  [LIT-tmpzz36v](../literature.d/LIT-tmpzz36v.md), with Rectified Flow, [LIT-636](../literature.d/LIT-636.md). Flow matching regresses onto
  the velocity of a straight line between a paired noise and data point, so
  the learned field at (x, t) is the average of the velocities of every
  pair whose line passes through x at t. Under independent pairing many
  lines cross there, and the average turns. A coupling with no crossings,
  the OT plan in the limit or the flow's own map after reflow, leaves one
  line through each point and a straight flow. The mechanism is proved. That
  this is what limits few-step image quality is measured only at 64 px and
  below, and Lee et al. ([LIT-tmptpra5](../literature.d/LIT-tmptpra5.md)) argue, without proof, that one reflow
  is enough.
---

<!-- inactive-ok-file: SOTA-tmphvn35, SOTA-392 — Proposed, and declared in `explains:`; this account underwrites the coupling practice and says why reflow helps a one-step student. Explaining a practice not yet in force is the normal case. -->

# THEORY-tmprwlgq: A flow's sampling ODE curves because the noise-data pairs it was trained on cross and the learned velocity averages them, so a coupling whose straight paths do not cross gives a straight flow

## Source

Pooladian, Ben-Hamu, Domingo-Enrich, Amos, Lipman and Chen (2023),
[LIT-tmprjg3i](../literature.d/LIT-tmprjg3i.md), §3–4, Lemma 3.2, Eqs. 18–19 and Thm. 4.2. Tong, Fatras,
Malkin, Huguet, Zhang, Rector-Brooks, Wolf and Bengio (2023), [LIT-tmpzz36v](../literature.d/LIT-tmpzz36v.md),
§3.2 and the proof of Prop. 3.4. Liu, Gong and Liu (2022), [LIT-636](../literature.d/LIT-636.md),
Thms. 3.3–3.7. Lee, Lin and Fanti (2024), [LIT-tmptpra5](../literature.d/LIT-tmptpra5.md), §2–3. Liu, Zhang,
Ma, Peng and Liu (2023), [LIT-tmpyqrl4](../literature.d/LIT-tmpyqrl4.md), §2.2 and Fig. 6.

## The account

**The learned velocity is an average.** Flow matching draws a pair
(x₀, x₁), places a point on the straight line between them, and regresses
the network onto that line's velocity x₁ − x₀. The minimizer at (x, t) is
the conditional expectation of x₁ − x₀ over all pairs whose line passes
through x at time t. Lee et al. ([LIT-tmptpra5](../literature.d/LIT-tmptpra5.md), Eq. 1) write the same field
through the posterior mean of the data endpoint given x_t.

**Crossings are what make it curve.** If two lines with different
directions pass through the same (x, t), the field there is neither, and a
particle integrating it turns. Multisample Flow Matching ([LIT-tmprjg3i](../literature.d/LIT-tmprjg3i.md))
makes this exact in two places. The joint objective's optimal value is
the spread of the conditional velocities about their mean, and it bounds the
gradient variance at fixed (x, t) (Lemma 3.2). Under independent pairing
it "generally cannot achieve value zero … since there are an infinite number
of pairs (x0, x1) whose conditional path crosses any particular x at a
time t". Its straightness measure S (Eq. 18) can be rewritten as the
variance of the velocity along a trajectory (Eq. 19). It is zero exactly
when every trajectory is a straight line. Lee et al.'s Eq. 4 is the same
fact read as a loss: the training error has a floor, the posterior variance
of the endpoint given x_t, which no network can reduce.

**A coupling without crossings gives a straight flow.** Two constructions
remove the crossings while keeping the endpoint distributions.

- *Optimal transport.* OT-CFM ([LIT-tmpzz36v](../literature.d/LIT-tmpzz36v.md)) proves that with the exact OT
  plan and vanishing path width the learned field solves the dynamic OT
  problem (Prop. 3.4). Its proof turns on the fact that paths from an OT
  map, the gradient of a convex function, cannot cross. So the field at
  each point is that point's own line, T(x) − x. Multisample Flow
  Matching proves the minibatch version in the limit: as the batch size k
  grows, the objective's optimum and S go to zero and the transport cost
  goes to W₂² (Thm. 4.2).
- *Reflow.* Rectified Flow ([LIT-636](../literature.d/LIT-636.md)) pairs each noise with the point the
  current flow carries it to and retrains. Marginals are preserved
  (Thm. 3.3), no convex transport cost increases (Thm. 3.5), and
  straightness improves at rate O(1/K) over K rounds (Thm. 3.7). All three
  are about exact minimizers. InstaFlow ([LIT-tmpyqrl4](../literature.d/LIT-tmpyqrl4.md), §2.2) restates the
  three properties for its text-conditioned reflow.

**Where this sits against [THEORY-106](THEORY-106.md).** That account says a straight
*conditional* path does not make the *marginal* ODE straight, and that
"straight against curved path" comparisons change a weighting, a network
output and a sampling schedule. This one says what does decide the
marginal's shape when the conditional path is held straight: the coupling.
OT-CFM states the premise in §3.2.1: the conditional path is OT, "the
marginal path pt(x) is not in general an OT path".

## What was measured

- **In 2-D the effect is an order of magnitude.** OT-CFM's normalized path
  energy is 0.018–0.087 with minibatch OT against 0.222–2.738 with
  independent pairs, over five seeds. A 2-rectified flow, one reflow on
  the same tasks, reaches 0.069–0.149 ([LIT-tmpzz36v](../literature.d/LIT-tmpzz36v.md), Table 2).
- **On ImageNet at 32 and 64 px it saves Euler steps.** In the controlled
  comparison of Multisample Flow Matching ([LIT-tmprjg3i](../literature.d/LIT-tmprjg3i.md), Table 1, read off
  Fig. 3), FID 20 on ImageNet-64 takes 12 Euler steps with batch OT against
  29 with independent pairing. Likelihood is unchanged. Samples from the
  same noise move less as the step count drops (Table 3).
- **On a diffusion teacher, reflow measurably straightens.** InstaFlow
  ([LIT-tmpyqrl4](../literature.d/LIT-tmpyqrl4.md), Fig. 6) estimates S on Stable Diffusion's probability-flow
  ODE and on the reflowed model, and S falls.

## What it explains

**[SOTA-tmphvn35](../practices.d/SOTA-tmphvn35.md)'s mechanism.** That practice pairs noise and data by exact
minibatch OT before the ordinary regression. This account is why that can
help and why it cannot hurt the target. The marginals are untouched, and
fewer crossings mean a straighter field and a smaller error per coarse
step. It also accounts for the practice's limit. The OT-CFM proof is about
the exact plan, and the minibatch plan's crossings vanish only as k grows
(Thm. 4.2). Nothing bounds them at image dimension and realistic batch
size, which is the practice's own Condition.

**Why reflow helps a one-step student, and when it should matter more.**
[SOTA-392](../practices.d/SOTA-392.md) says to distil a rectified flow and treat reflow as optional, and
InstaFlow contests it from a diffusion teacher. On this account a one-step
distiller must reproduce in one step a map the teacher reaches along a
curved path, and reflow replaces that map with one whose straight-line
pairs barely cross. InstaFlow puts it as a suggestion: "the new coupling
might be easier for the student network to learn" (§2.2). Its matched
comparison fits that reading: from Stable Diffusion, reflow first gives
one-step FID-5k 31.0 against 40.9. So does Rectified Flow's own table from
a straight-path teacher: 4.85 against 6.18. The account predicts a larger
increment from a more curved teacher. That is the direction of the two
results, but they differ in teacher, scale, data and distiller, so it is a
prediction and not a finding.

## Where it stops

- **It does not say reflow is free at many steps.** Rectified Flow's own
  2- and 3-rectified flows lose full-simulation quality, 2.58 to 3.36 and
  3.96 FID. The theorems are about exact minimizers, and each round trains
  on generated pairs with its own error. [SOTA-392](../practices.d/SOTA-392.md)'s last clause, keep the
  pre-reflow model for many steps, rests on that measurement, not on this
  account.
- **"One reflow is enough" is an argument, not a result.** Lee et al.
  ([LIT-tmptpra5](../literature.d/LIT-tmptpra5.md), §3) argue that for two 1-rectified-flow pairs to cross,
  one noise must equal another plus a scaled data difference. Such a noise
  sits off the Gaussian annulus and is autocorrelated, so the optimal
  *2-rectified* flow is nearly straight. It is the 2-rectified flow, after
  one reflow, that they call nearly straight, not the base model. The
  evidence is qualitative (Fig. 2), and the checklist says the claim "is
  intuitive, and we do not prove it". Their follow-on choice of a U-shaped
  timestep density reads the training loss as the reducible error, which is
  sound only if the floor above is near zero.
- **A straighter marginal is not what path comparisons measure.** On
  CIFAR-10, under one recipe, changing the coupling moves 100-step Euler FID
  from 4.461 to 4.443, and changing the conditional path from VP to straight
  moves it from 7.772 to 4.640 ([LIT-tmpzz36v](../literature.d/LIT-tmpzz36v.md), Table 5). So the gain
  [SOTA-266](../practices.d/SOTA-266.md) records for the straight path is not, on this evidence, a gain
  from a straighter marginal ODE. That agrees with [THEORY-106](THEORY-106.md).
- **It does not make a few-step sampler.** Straightening lowers the
  step count of an ODE solve. Four-step Euler FID with batch OT is still
  38.86 on ImageNet-32 ([LIT-tmprjg3i](../literature.d/LIT-tmprjg3i.md), Tables 7–8).
- **Unconditional only.** No paper here pairs under a class or text
  condition. Pairing across a batch makes a noise depend on the other
  images, and whether the conditional marginals survive is not addressed.
- **Straight is necessary for one-step accuracy, not sufficient for
  quality.** Rectified Flow's reflowed model at one undistilled step scores
  12.21 FID, against 4.85 once distilled. Distillation does work that
  straightening does not.
