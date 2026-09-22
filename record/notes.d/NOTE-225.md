---
number: 225
status: Read
formerly:
- NOTE-tmpw2aa7
paper: LIT-476
title: 'Local Volume'
version: 1
date: '2026-09-21'
summary: >-
  Reading it: the useful result is the audit, not the hypothesis. A network
  trained to generalize badly is detected on clean held-out data where its
  behaviour matches a clean model's, in a small number of forward passes.
  The volume hypothesis itself is left where it was found — "broadly
  consistent", by the authors' own conclusion.
---

<!-- inactive-ok-file: THEORY-006 — Proposed, and named in Connections to say
     this measurement is NOT the one its promotion condition asks for; the
     distinction is the point being made, not a claim resting on it -->

# NOTE-225: Local Volume

## Contribution

An estimator for a quantity people have wanted for thirty years and mostly
approximated by curvature. Flat-minima work asks how fast loss rises as you
step away from a solution; this asks how *much* of parameter space behaves
like the solution, under the distribution the weights were drawn from.

What is true afterwards that was not before: you can put a number on it for a
real model, and the number is a description length rather than a curvature
proxy.

## Key insight

**Measure under the prior, not under Lebesgue, and define the neighbourhood by
behaviour rather than by loss.**

Both choices are doing work. Lebesgue volume of a real neighbourhood can be
*infinite* — they found this empirically — which makes the classical framing
unusable. Using the initialization distribution guarantees finiteness and
gives the quantity its interpretation: it is literally the probability of
drawing a behaviourally-equivalent network at random.

And defining the neighbourhood by KL to the anchor rather than by loss needs
no labels, is exactly zero at the anchor, and is a much stronger constraint —
so the region is compact enough to estimate. The paper's analogy is a Tissot
indicatrix: contours of constant functional similarity in parameter space,
whose size measures how much the architecture stretches or compresses the map
from parameters to functions.

## Assumptions

- **Star-domain neighbourhoods** anchored at the trained weights, with radius
  found by binary search along sampled directions.
- **Gaussian or uniform prior**, with a Gaussian used in practice — which by
  construction cuts off flat directions smoothly, and the authors flag this as
  a possible cause of one of their results differing from the LLC literature.
- **KL cost on held-out inputs**, no labels.
- **Importance sampling with a preconditioner** derived from optimizer state.
- **The aggregate estimate is dominated by the largest sample**, so this is a
  lower bound that improves with better proposals.

## Key results

- P(sampling trained Pythia 31M from its init distribution within a small KL
  ball) ≈ **10⁻³·⁶ˣ¹⁰⁸**.
- **Poisoned ConvNeXt has smaller local volume than clean**, with and without
  preconditioning, measured on clean held-out data.
- Local volume **decreases through training**; for Pythia, smoothly and
  roughly exponentially after an early sharp drop.
- The poisoned model's volume is *larger* for much of training and crosses
  below the clean model's at ~30,000 steps — coinciding with the divergence of
  validation and poison losses.
- Preconditioners: Adam second moment, K-FAC and HesScale all work well and
  similarly; the **full Hessian of the KL does no better than none**.
- Volume vs cutoff follows a power law with log-log slope ≈ `d/2`, unlike LLC
  results where `d/2` is an unattained upper bound.

## Claims

**Measured and clean:** the poisoned/unpoisoned gap on held-out data, and the
downward trend through training. Both were predicted in §4.3 before being
tested, which is worth noting.

**Measured and awkward:** the crossing. The poisoned model is bigger for most
of training. The explanation given — early on the poison term is just making
the network worse everywhere, so it learns less and its volume falls more
slowly — is plausible and post hoc, and it means "smaller volume" is not a
property of a badly-generalizing *run* but of a badly-generalizing *converged*
model.

**Argued, not measured:** that adaptive optimizers generalize worse because
they undo the architecture's volume bias. This is §3.3, it is the paper's most
quotable idea, and no experiment in the paper touches it.

**Explicitly left open:** the volume hypothesis. The conclusion says "broadly
consistent" and "more research is needed to confirm or refute any specific
version".

## Method

Radius-finding along sampled directions, preconditioned importance sampling,
aggregated into a log-volume estimate; run on an MLP, a ConvNeXt and Pythia
31M checkpoints, with poisoned/clean pairs and across training time and KL
cutoff.

## Concepts

*Local volume*; *loss* versus *KL neighbourhoods*; the *volume hypothesis* in
its strong, basin and measure-theoretic forms; the bits-back MDL reading;
the Local Learning Coefficient as the singular-learning-theory neighbour
([LIT-tmp6dook](../literature.d/LIT-tmp6dook.md), filed since; the frame is [THEORY-tmpzuan6](../theory.d/THEORY-tmpzuan6.md)).

## Connections

- [SOTA-012](../practices.d/SOTA-012.md) — sharpness correlates with test error — is the record's
  existing version of this intuition, resting on one 2017 source with
  `consensus` unassessed. This measures a different quantity in the same
  spirit and does not settle it; the paper itself cites Dinh et al. on
  counterexamples to flatness.
- [SOTA-001](../practices.d/SOTA-001.md) recommends Adam. §3.3 offers a reason adaptive optimizers
  might generalize worse — and offers no measurement, so the practice is
  untouched.
- [THEORY-006](../theory.d/THEORY-006.md) says task-improving perturbations are dense around
  pretrained weights and denser at scale. Adjacent and not the same: that is
  about how many nearby points *improve* a task, this is about how many behave
  *identically*. Neither measurement substitutes for the other, and
  `THEORY-006`'s promotion condition asks for its own repeated.

## Bearing on the record

One practice, `Proposed` — the audit use, which is the part with a clean
experiment behind it. One account, `Proposed` — the volume-as-description-length
reading, which the paper itself declines to call settled.

What should not enter the record is the adaptive-optimizer argument. It is an
explanation offered for a known effect with nothing measured, in a paper whose
other claims come with figures.

## Limitations

**The estimator's accuracy is unknown.** Stated plainly in the conclusion.
Everything downstream inherits that, and the structure of the estimate — close
to the largest sample, with one outlier run nearly matching the preconditioned
result on its own — says it is a lower bound whose tightness is the open
question.

**Scale.** 4810 parameters, 3.4M, 31M. The language-model result is at 31M.

**One adversarial pair.** Poisoning produces bad generalization at low
training loss on purpose. Whether ordinary overfitting shrinks volume the same
way is not shown, and the crossing result suggests the relationship is not
simple even here.

**Two numerical artefacts**, both identified: the preconditioner degrading at
high cutoffs, and a low-cutoff collapse confirmed to be floating-point failure
in the binary search rather than a finding. Credit for chasing the second down
rather than plotting it.

**One unexplained result.** The Fisher matrix — the theoretically natural
preconditioner — performs no better than none, and axis-aligned approximations
of it do much better. The authors say they find this surprising and do not
know why.

## Open questions

- Does ordinary overfitting shrink local volume, or only adversarially
  induced bad generalization?
- Why does the full Hessian lose to its own diagonal approximations? The
  authors' guess is a misalignment between locally-flattest directions and the
  neighbourhood's longest ones, and they note it does not explain why
  axis-alignment should help.
- Is the `d/2` slope real or an artefact of the Gaussian prior? The paper
  proposes the test — replace the explicit Gaussian integral with a quadratic
  term in the cost — and does not run it.
- Does any of this survive at a scale where the record's practices live? 31M
  is where the language-model evidence stops.
