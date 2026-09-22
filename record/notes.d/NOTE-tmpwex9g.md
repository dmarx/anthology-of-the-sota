---
status: Read
paper: LIT-tmpgj3s9
title: 'Stage boundaries found without knowing in advance what to look for'
version: 1
date: '2026-09-22'
summary: >-
  Read as the application that makes the LLC matter to this record. Critical
  points of the LLC curve divide two transformers into five stages each, and
  the boundaries land on bigrams, n-grams, previous-token heads and the
  induction circuit — found without a mechanistic hypothesis in hand, which is
  what `LIT-085`'s progress measures require. Its in-context regression model
  acquires in-context learning and then loses it.
---

# NOTE-tmpwex9g: Stage boundaries found without knowing in advance what to look for

## Contribution

It turns a complexity measure into a detector. Rather than proposing a
mechanism and building a measure to track it, this estimates loss-landscape
degeneracy through training, reads stage boundaries off the critical points of
that one curve, and *then* asks independently whether anything structural
changed there. The interesting claim is the direction of inference: the
boundaries are found first and interpreted second.

## Key insight

**A quantity that says nothing about what the network is doing can still say
when it changed.** Every progress measure in the record's possession is
constructed from a hypothesis about the mechanism — `LIT-085`'s restricted and
excluded losses need the five frequencies the network was reverse-engineered to
use. Degeneracy is measured the same way for any model on any data. That buys
detection without a prior hypothesis, at the cost of telling you nothing about
what was detected, and both halves are stated by the authors.

## Assumptions

- The LLC estimator of `LIT-tmp6dook`, with all of its assumptions — SGLD,
  `β* = 1/log n`, a localizing radius, a Bayesian object measured at an
  SGD point.
- Stage boundaries are **critical points of the `λ̂` curve**, a stipulated rule
  rather than a derived one.
- Two models: a 2-layer attention-only language transformer, and a transformer
  trained on synthetic in-context linear regression. Both small.
- Structural and behavioural evidence comes from standard mechanistic probes —
  previous-token matching score, prefix-matching score, composition scores, ICL
  score — each with its own conventions.

## Key results

- **Language model, five stages.** Ends at `t = 900 / 6.5k / 8.5k / 17k / 50k`;
  `Δℓ̂ = −2.33 / −1.22 / −0.18 / −0.40 / −0.34`; `Δλ̂ = +26.4 / +22.5 / −1.57 /
  +8.62 / +1.77`. LM1 bigram statistics; LM2 common n-grams; LM3 previous-token
  heads form and the relevant heads begin composing; LM4 induction heads
  complete the circuit of Olsson et al., with a corresponding drop in ICL score.
  **No significant change was found in LM5.**
- **In-context regression, five stages.** Ends at
  `t = 1k / 40k / 126k / 320k / 500k`; `Δℓ̂ = −0.32 / −2.21 / −0.07 / −0.05 /
  −0.029`; `Δλ̂ = +21.4 / +149 / −12.3 / −44.1 / +3.56`. LR1 learns the
  context-independent optimum `x_k ↦ ŷ_k = 0`; LR2 acquires in-context
  learning; **LR3 and LR4 see in-context ability deteriorate** while the model
  specializes to the pre-training task distribution, with layer-normalization
  weights collapsing to zero.
- **A single run recapitulates a depth ladder.** The 2-layer model passes
  through bigrams and then n-grams before the induction circuit — the same
  progression Olsson et al. found across *fully-developed models of increasing
  depth*.
- **LLC decreases happen, in both models, and are unexplained.**
  Saddle-to-saddle theory for deep linear networks predicts increasing
  complexity; the paper's own §5 transitions are increases. Lowering `λ` at
  constant loss also lowers the free energy, so it is not forbidden — "providing
  a full theoretical account of these stages is an open problem".

## Limitations

**Two case studies, said plainly.** "We do not claim that the structural and
behavioral developments we observed in each setting are universal phenomena."
Also, for both models, "we did not discover significant changes in
[the final stage], and we do not claim that these are the only interesting
developmental stages".

**Coincidence is the evidence.** The abstract calls it "suggestive evidence
that degeneracy and development are linked". Stage boundaries land near
structural changes; nothing here derives one from the other, and the number of
boundaries is small enough that the coincidence is a qualitative argument.

**The stage-boundary rule is a convention.** "Critical points of the LLC curve"
is a reasonable choice and it is a choice; a noisier estimator or a different
smoothing gives different boundaries.

## Bearing on the record

**It is a rival to `LIT-085`, and the paper names it as one.** `SOTA-200`
records that `LIT-085`'s progress measures need the network reverse-engineered
first and calls that the expensive case. This does the same job — reveal
developments invisible in the loss — without the prerequisite, and the record
now holds both approaches with their costs stated.

**The LR3/LR4 finding belongs to the in-context-learning cluster.** An
ICL-objective transformer *acquires and then loses* in-context ability while
its loss keeps falling. Every paper in `THEORY-067`'s cluster measures a
trained model at one point in that trajectory, and none of them reports which
point. Whether the mesa-optimization results were measured before or after LR3
is a question this record can now ask and cannot answer.

**It is also the record's first instance of a model getting simpler.** The
knowledge-acquisition and loss-curve clusters are about what the aggregate
curve hides; this hides a direction, not just a magnitude.

## Open questions

- **What accounts for the LLC decreases?** The authors say nobody knows, and
  the two settings disagree about where they fall.
- **Where in the developmental trajectory were the mesa-optimization results
  measured?** LR3 and LR4 change in-context behaviour substantially; the
  papers in that cluster report a trained model, not a stage.
