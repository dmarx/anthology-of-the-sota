---
number: 261
status: Read
formerly:
- NOTE-tmpg1l16
paper: LIT-520
title: 'The singular distribution stops moving long before the weights do'
version: 1
date: '2026-09-22'
summary: >-
  Read for one question: is the spectral shape that three other papers measure
  a stable property or a snapshot? It is stable, and early. The empirical
  section was read and the theory that derives the stability bound was not,
  which is stated rather than implied.
---
<!-- inactive-ok-file: THEORY-041 — Proposed, named as an adjacent account
     that this reading says is NOT the same claim. A use that requires it to
     be unsettled rather than one that leans on it. -->

# NOTE-261: The singular distribution stops moving long before the weights do

## Contribution

Name and measure a phenomenon: during pretraining the *shape* of the singular
spectrum reaches stationarity well before the weight matrices do, and the
moment it does coincides with the loss curve's transition from fast to slow
descent.

## Key results

**The definition.** The Singular Distribution is the trace-normalized
spectrum `Σ̂ₜ = Σₜ/tr(Σₜ)`. Because cosine similarity is scale-invariant,
`cos⟨Σₜ, Σ_T⟩` saturating is equivalent to `Σ̂ₜ` stabilizing. Measured against
the *final* state, so it is a statement about arriving early rather than about
changing slowly.

**The two phases.** With `ΔΣₜ = ‖Σ̂ₜ₊₁ − Σ̂ₜ‖_F`:

| phase | steps | `ΔΣ` | validation loss |
|---|---|---|---|
| I — restructuring | `t < 1000` | transient peak near `10⁻²` | ~10 → ~4.0 |
| II — metastability | `t > 1000` | floor near `10⁻⁴` | long slow descent |

The spectral shape settles and the fast descent ends at the same point.

**MLP layers vary less than attention layers**, consistently, and both enter
the stable regime together.

**It survives the recipe.** GPT-2 Small and Medium, LLaMA 0.5B and 2B;
step-wise, WSD and cosine-decay schedules; different weight decays; AdamW and
Muon.

**The offered account** is a stability bound `ε ∝ η/‖W‖`: learning-rate
schedules tighten it, weight decay relaxes it by suppressing norm growth, and
the paper reads WSD and Muon through that lens.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | The singular distribution stabilizes before the weights | strong | four models, direct measurement against the final state |
| C2 | Stabilization coincides with the loss-curve elbow | strong as correlation | synchronization shown, causation argued in the theory section |
| C3 | It is robust to schedule, weight decay and optimizer | moderate-to-strong | the sweep is real but each cell is one run |
| C4 | `ε ∝ η/‖W‖` explains the strategies | not assessed here | section 4, not read |

## Limitations

**Read in part, and the unread part is the explanatory one.** Sections 1–3
were worked through; the theorems in section 4 that derive the bound and
couple loss descent to spectral variation were not. C4 is recorded as the
paper's claim, not as something this record checked.

**Correlation is what is measured.** Two curves elbow together across many
settings. That is a strong pattern and it is not an intervention: nothing
here forces the spectrum to keep moving and shows the loss keeps falling.

**Small models.** The largest is LLaMA 2B.

**Single runs.** The robustness sweep varies the setting, not the seed.

## Bearing on the record

**It is why a one-shot spectral reading means anything.**
[SOTA-318](../practices.d/SOTA-318.md) reads a per-matrix spectrum once and picks a rank
from it; [SOTA-314](../practices.d/SOTA-314.md) peels a fixed number of directions from a finished
checkpoint. Both assume the shape they are reading is the shape the model has.
This says it is — fixed within the first thousand steps or so and held
thereafter, across two architectures, three schedules and two optimizers.

**It also bounds a tempting inference.** Stability of the *distribution* is
not stability of the matrix: the weights keep moving, so which directions the
mass sits in can change even while how concentrated it is does not. Nothing
in this record should read SoSD as saying a rank chosen early stays the right
rank.

**Adjacent to [THEORY-041](../theory.d/THEORY-041.md), and not the same claim.** That account says
unconstrained transformer matrices drift into a badly conditioned,
rank-deficient shape. This says the normalized spectrum stops changing early.
Drift in conditioning and stability of shape are compatible — the first is
about where the mass is, the second about how spread it is — and neither
paper cites the other.

## Open questions

- **Does the bound survive an intervention?** Forcing continued spectral
  variation late in training — and seeing whether the loss falls faster — is
  the experiment the correlation asks for.
- **Does SoSD hold at 7B and beyond?** Every model here is 2B or smaller, and
  the two-phase loss curve it explains is most consequential at the scales
  where a pretraining run is expensive.
