---
number: 2
status: Read
formerly:
- NOTE-tmp9vhnf
paper: LIT-117
title: 'Efficient Online Data Mixing'
version: 1
tags:
- data-pipeline
date: '2026-09-09'
summary: >-
  An Exp3 bandit over data domains, rewarded by per-domain training loss on the batches the run is already taking, revising the mixture during training. 19% fewer iterations to the next best method's final perplexity, at negligible wall-clock cost.
---

# NOTE-002: Efficient Online Data Mixing

## Contribution

Data *selection* chooses individual documents and is too expensive to run
during training; data *mixing* chooses proportions over groups and is cheap
but fixes them before training starts, so it cannot respond to what the model
has already learned. ODM takes the grouping from mixing and the adaptivity
from selection: the domains are fixed, the proportions are a bandit policy
revised at every step, and the reward is a quantity training already computes.
The result is adaptivity at essentially no wall-clock cost.

## Key insight

The reason online data selection is expensive is that people reach for a
signal that requires extra work — a proxy model, a held-out validation pass,
a quality classifier. But the training loss on the batch you just took is
already an estimate of how much there is left to learn in that domain, and
it costs nothing because you computed it to take the step. Reframing "which
data should I train on next" as a bandit whose reward is the loss turns an
expensive question into a free one.

The information-theoretic gloss the authors give is worth keeping: perplexity
is expected information gain from the next token, so a domain with high loss
is a domain with more to teach. That is *learnability*, not quality — and
those diverge, since noise also has high loss.

## Assumptions

Not a theoretical paper; Exp3's own regret guarantees are inherited and not
re-derived here. What bounds the conclusions:

- **The domains are given.** ODM optimises proportions *over a partition
  someone else chose* — the 22 Pile domains. It says nothing about how to
  cut the corpus into groups, and the quality of the partition bounds what
  the method can do.
- **The reward is stationary enough for a bandit.** Exp3 assumes an
  adversarial but bounded reward; per-domain loss drifts as training
  proceeds, which is the point, and the exploration term is what keeps the
  policy tracking it.
- **One scale, one corpus.** 1B parameters, 50B tokens, The Pile. Not the
  multi-trillion-token regime the record's contemporary practices assume,
  and the paper does not claim it transfers.

## Key results

- **The policy.** Exp3's Gibbs distribution mixed with uniform exploration at
  rate `ℰₜ`:

      πₜ(Dᵢ) = (1 − K·ℰₜ) · exp(ℰₜ₋₁·R̂ᵢ) / Σⱼ exp(ℰₜ₋₁·R̂ⱼ)  +  ℰₜ

  where `R̂ᵢ` is the importance-weighted reward for domain `i` and `K` the
  number of domains.
- **The reward** is the per-domain training loss `L_Dᵢ`, computed on the
  batch already drawn.
- **19% fewer training iterations** to reach the final perplexity of the next
  best method.
- **+1.9% relative accuracy** on 5-shot MMLU.
- **Negligible added wall-clock time**, which is the claim the whole design
  serves.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Mixing proportions fixed before training cannot adapt to training dynamics, and adapting them helps | strong | the 19% iteration saving against fixed-proportion baselines |
| C2 | Per-domain training loss is an adequate reward signal for choosing proportions | moderate | works at 1B/50B on The Pile; no ablation against a validation-based reward |
| C3 | The method's cost is negligible | strong | follows from the design — the reward is already computed — and is measured |
| C4 | Higher loss means more information left to learn in a domain | weak | an information-theoretic argument, not a measurement; noise also has high loss |
| C5 | The gains transfer to downstream tasks, not just perplexity | moderate | +1.9% relative on 5-shot MMLU, a single benchmark |

## Method

**Algorithm:** Online Data Mixing (ODM), an Exp3 multi-armed bandit.

At each training step `t`, sample a domain `Dᵢ` from the current policy `π`,
take the batch, compute the loss, use it to update the model *and* as the
reward to update `π` for step `t+1`. Arms are domains; the policy is the
Gibbs-plus-uniform mixture above.

**Key components**

- The domain partition (given, not learned)
- Per-domain training loss as reward — the efficiency claim lives here
- Importance weighting, so a domain sampled rarely still contributes an
  unbiased reward estimate
- The exploration rate `ℰₜ`, which both mixes in the uniform distribution and
  scales the Gibbs exponent

## Concepts

- **Online data mixing** — revising the sampling distribution over data
  groups *during* training, as opposed to fixing it beforehand.
- **Exploration rate `ℰₜ`** — Exp3's parameter. It does two jobs here, and
  the second is easy to miss: it sets how much uniform distribution is mixed
  in, *and* it multiplies the reward inside the Gibbs exponent, where it acts
  as an inverse temperature controlling how sharply the policy concentrates.
- **Learnability** (implicit) — the quantity the reward proxies. Not quality:
  a domain can have high loss because it is rare and valuable or because it
  is noise, and this reward cannot tell them apart.

## Connections

Positioned explicitly between two lines of prior work — data selection
(expensive, per-document, adaptive) and data mixing (cheap, per-group,
static) — and claims the useful corner of both. The Pile provides the domain
partition it optimises over.

## Recommendations

- **R1** — Adjust data mixing proportions online from a signal you are
  already computing. *Topic:* data mixing. *Status:* experimental.
  *Strength:* moderate. *Applies when:* the corpus has a usable domain
  partition and the mixture is currently fixed by hand.
- **R2** — Use the per-domain training loss rather than validation
  performance as that signal. *Topic:* data mixing. *Status:* experimental.
  *Strength:* moderate. *Applies when:* always, within R1 — a validation pass
  per domain per update is the cost this method exists to avoid.
- **R3** — Do not read a loss-derived sampling signal as a quality signal.
  *Topic:* data quality. *Status:* standard. *Strength:* strong. *Applies
  when:* any loss- or perplexity-driven data decision; noise and rare
  valuable text are indistinguishable to it.

## Bearing on the record

**Contradicted all four practices that cited it.** The paper contains
`filter`, `temperature`, `domain coverage` and `validation performance`
**zero times each**.

<!-- inactive-ok-block: SOTA-101, SOTA-102, SOTA-104 — retired in #114; this table is the record of why -->
| practice | disposition |
|---|---|
| [SOTA-101](../practices.d/SOTA-101.md) perplexity-based filtering | `Rejected` — ODM does no filtering; it reweights, and filtering has the opposite failure mode |
| [SOTA-102](../practices.d/SOTA-102.md) dynamic temperature scaling | `Superseded by SOTA-103` — see below |
| [SOTA-103](../practices.d/SOTA-103.md) adjust ratios from validation performance | **survives, restated** from R1 and R2 |
| [SOTA-104](../practices.d/SOTA-104.md) monitor domain coverage | `Rejected` — no signal, no action, and in tension with the method |

<!-- inactive-ok-block: SOTA-102 — Superseded in this same change; the paragraph is about why it superseded rather than retired -->
**`SOTA-102` is the interesting disposition and it corrects an earlier
reading of mine.** Its body, written for [#107](https://github.com/dmarx/anthology-of-the-sota/issues/107) without the paper open, said a
temperature and a bandit are different things — "a temperature reshapes a
distribution somebody already chose; a bandit discovers the distribution".
That is wrong about this bandit. Exp3's policy *is* a tempered softmax, and
`ℰₜ` is the inverse temperature, varying over training. So "dynamic
temperature scaling for mixing" names a real component of ODM imprecisely,
rather than naming something the paper does not do. It is `Superseded` into
the practice describing the whole method, not `Rejected`.

## Limitations

- The domain partition is an input, and a bad one caps the method. Nothing
  here says how to choose it.
- C4 is the load-bearing intuition and the weakest claim: high loss means
  "more to learn" only if the data is worth learning.
- 1B parameters and 50B tokens on The Pile. Whether an online mixture still
  pays when the corpus is 100× larger and already curated is untested.
- No ablation isolating the reward choice — training loss is never compared
  against a validation-based reward, so C2 rests on the method working
  overall.

## Open questions

- Does this survive contact with a modern curated mixture, where the
  hand-set proportions encode a lot of prior work the bandit would discard?
- What happens when a domain is noise? C4 predicts ODM over-samples it, and
  nobody has run that experiment.
- Is the domain partition itself learnable, or does the grouping have to
  come from outside?
