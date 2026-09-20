---
number: 196
status: Read
formerly:
- NOTE-tmp31z9k
paper: LIT-449
title: 'Scaling Rectified Flow Transformers'
version: 1
date: '2026-09-20'
summary: >-
  A 61-way sweep over diffusion and rectified-flow formulations settles on a
  straight-line path with logit-normal timestep sampling — rectified flow
  with uniform timesteps does not win. Adds a resolution-dependent timestep
  shift, MMDiT's per-modality weights with joint attention, and QK-RMSNorm
  for high-resolution stability. 8B, weights released.
---

# NOTE-196: Scaling Rectified Flow Transformers

## Contribution

Takes rectified flow from "better theory, unproven in practice" to a released
8B text-to-image model, and does it by way of a comparison broad enough to be
worth trusting: 61 formulations swept at matched settings, covering the
standard diffusion parameterizations and schedules alongside rectified flow
under several timestep distributions. The winning entry is not rectified flow
as usually written but rectified flow with the training timesteps drawn from
a logit-normal. Two further contributions are separable from the transport
question: a correction to the timestep schedule when resolution changes, and
a transformer that gives each modality its own weights while letting the
streams attend jointly.

## Key insight

**A formulation's advantage can be hidden by the sampling distribution it is
usually written with.** Rectified flow's straight-line path had better
theory and mixed empirics, and the sweep shows why: `rf/uniform` — rectified
flow with uniformly sampled timesteps, the way the prior literature wrote it
— does not beat well-tuned epsilon-prediction, while `rf/lognorm` does. The
path and the distribution over where you train along it are separate
decisions, and conflating them had made a real advantage look absent. The
same structure explains the resolution result: a timestep is not a fixed
amount of corruption, because destroying the signal in more pixels takes more
noise, so a schedule transferred between resolutions is systematically wrong
in a direction nobody had named.

## Assumptions

- **Latent diffusion**, with an autoencoder whose channel count the paper
  raises to 16 after finding it improves reconstruction and scales better.
- **Text-to-image**, evaluated by validation loss, GenEval, automated metrics
  and human preference; the sweep itself is ranked on validation loss, and
  the paper's own justification for that is the correlation it measures
  between loss and the downstream metrics.
- **The sweep is at a fixed, smaller scale**; the 8B run applies its winner
  rather than re-running the comparison there.
- Pretraining at 256×256, then finetuning at higher resolution with mixed
  aspect ratios through bucketed sampling.
- The resolution-shift derivation assumes corruption should be matched in
  terms of signal destroyed per pixel count.

## Key results

- **The 61-way ranking.** Rectified flow with logit-normal timestep sampling
  ranks first. Rectified flow with **uniform** timesteps does not — a
  distinction the headline claim would erase.
- **Rectified flows are most advantaged at few sampling steps.** At 25 steps
  and above only `rf/lognorm(0.00, 1.00)` stays competitive with
  `eps/linear`; below that the gap is wider. The benefit lands where
  inference cost binds.
- **Resolution-dependent timestep shifting**: map a timestep at one resolution
  to the one producing equivalent corruption at another. Without it, a
  schedule tuned at low resolution is wrong at high resolution.
- **MMDiT**: separate projections and MLPs per modality, attention over the
  concatenated sequence. Beats UViT and DiT at matched budget, with the gains
  concentrated in text comprehension, typography and human preference.
- **Predictable scaling**, with validation loss correlating to human
  preference and automated metrics — which is what licenses selecting a
  configuration before the expensive run.
- **QK-RMSNorm** with learnable scale in both streams, adopted after
  mixed-precision training diverged at high resolution; the diagnosis
  (attention entropy growing uncontrollably) is taken from the discriminative
  ViT literature.
- **16 latent channels** in the autoencoder: better reconstruction, and better
  FID scaling because the harder prediction task rewards capacity.
- 8B parameters, outperforming the state of the art at the time; code,
  weights and experimental data released.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Rectified flow with logit-normal timestep sampling beats established diffusion formulations | strong | 61-way sweep at matched settings, with the negative control (uniform timesteps) reported |
| C2 | The advantage survives to 8B and to text-to-image | moderate | one 8B run applying the sweep's winner; the sweep was not repeated at that scale |
| C3 | Timestep schedules must be shifted with resolution | moderate | derivation from signal-per-pixel plus a qualitative comparison; no ablation isolating its contribution to the final model |
| C4 | Per-modality weights with joint attention beat a shared-weight backbone | moderate | comparison against UViT and DiT at matched budget, single architecture family |
| C5 | Validation loss predicts human preference well enough to select on | moderate | measured correlation over the scaling study; a correlation, not a guarantee, and measured within one family |
| C6 | Rectified flows are more sample-efficient at few steps | strong | direct measurement across step counts |

## Method

Sweep 61 formulations — epsilon and v prediction across several schedules,
and rectified flow across several timestep distributions including uniform,
mode-weighted and logit-normal — at matched settings, ranking on validation
loss.

For the architecture, embed text and image as separate token streams with
their own projections and MLPs, concatenate for attention so information
flows both ways, and compare against UViT and DiT backbones at matched
compute.

Pretrain at 256×256, then shift the timestep schedule for the target
resolution before finetuning with mixed aspect ratios via bucketed sampling.
Apply RMSNorm to Q and K in both streams to keep mixed-precision training
from diverging. Scale, and check that validation loss tracks the downstream
metrics before committing to 8B.

## Concepts

- **Rectified flow** — a forward process connecting data and noise along a
  straight line, as against diffusion's curved path.
- **Logit-normal timestep sampling** — draw `t` so that its logit is normal;
  the density vanishes at both endpoints, concentrating training in the
  middle of the range.
- **Resolution-dependent shift** — the map from a timestep at one resolution
  to the timestep at another producing the same degree of corruption.
- **MMDiT** — a transformer with modality-specific weights and a shared
  attention operation over the concatenated streams.

## Connections

Extends [LIT-447](../literature.d/LIT-447.md), which it names as the prior evidence for the
straight-line path and whose limitation it states precisely: small and medium
scale, class-conditional only.

The logit-normal timestep distribution is the rectified-flow expression of
what EDM ([LIT-075](../literature.d/LIT-075.md)) reached as a log-normal over noise levels — concentrate
training where there is something to learn. Two formulations, two
coordinates, one recommendation; the record holds it as [SOTA-188](../practices.d/SOTA-188.md).

The QK-normalization arrives from the ViT literature's attention-entropy
diagnosis, independently of the language-model line where the record already
holds it.

## Recommendations

- **R1** — Use a rectified-flow (straight-line) forward process with
  logit-normal timestep sampling, not uniform. *Topic:* forward process.
  *Status:* standard. *Strength:* strong. *Applies when:* latent diffusion
  for image synthesis; most valuable where sampling steps are few.
- **R2** — Shift the timestep schedule when changing resolution, by the
  signal-per-pixel correspondence. *Topic:* noise schedule. *Status:*
  experimental. *Strength:* moderate. *Applies when:* training or finetuning
  at a resolution different from where the schedule was set.
- **R3** — Give each modality its own weights and let the streams attend
  jointly. *Topic:* architecture. *Status:* experimental. *Strength:*
  moderate. *Applies when:* a multimodal generative backbone.
- **R4** — Normalize Q and K before attention when training at high resolution
  in mixed precision. *Topic:* stability. *Status:* standard. *Strength:*
  strong. *Applies when:* the failure mode is loss divergence with growing
  attention entropy.
- **R5** — Select a formulation on validation loss before the expensive run,
  having first checked that loss tracks the downstream metric you care about.
  *Topic:* evaluation. *Status:* experimental. *Strength:* moderate.
  *Applies when:* a scaling study is affordable at small scale.

## Bearing on the record

- **Should produce practices** for R1 (with [LIT-447](../literature.d/LIT-447.md) supplying the
  controlled attribution), R2 and R3. None has an equivalent in the record.
- **Confirms half of [SOTA-188](../practices.d/SOTA-188.md) at 8B in a formulation EDM did not test.**
  That practice already lists Stable Diffusion 3 as an implementation and the
  record did not hold the paper; the listing turns out to be correct, and
  saying *why* it is correct — logit-normal over `t` is log-normal over noise
  level in the other coordinate system — is worth more than the listing.
- **R4 is a rediscovery of [SOTA-131](../practices.d/SOTA-131.md), [SOTA-192](../practices.d/SOTA-192.md) and [SOTA-050](../practices.d/SOTA-050.md)** from the
  other side of the field, reached from a different failure. Worth recording
  in those practices as independent arrival rather than filing again.
- **R5 bears on the record's evaluation material** and is weaker than it
  looks: the correlation is measured within one model family, which is
  exactly the condition under which such correlations usually hold and stop
  being informative.

## Limitations

- The sweep and the 8B run are different experiments. C1 is well supported at
  the sweep's scale; C2 is one run applying its winner.
- No mechanism. The study ranks formulations and does not isolate why the
  straight path helps; the nearest account is [LIT-447](../literature.d/LIT-447.md)'s transport-cost
  observation, which is itself correlational.
- The resolution shift is derived and demonstrated qualitatively; its
  contribution to the final model is not ablated against not doing it.
- MMDiT is compared against UViT and DiT, not against other per-modality
  designs, so "separate weights help" is established against shared-weight
  baselines only.
- Human preference is the headline quality metric on a text-to-image task,
  with all the population and prompt-distribution dependence that carries.
- The 16-channel autoencoder change is entangled with everything downstream
  of it.

## Open questions

- Would the 61-way ranking hold if repeated at 8B? The paper's own scaling
  argument says probably, and probably is what is established.
- Is the logit-normal's benefit the same benefit as EDM's log-normal, or does
  the straight path change where the useful region is? Nobody has mapped one
  onto the other.
- How much of MMDiT's gain is the separate weights and how much the joint
  attention? The two arrive together.
