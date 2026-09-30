---
number: 425
status: Active
formerly:
- SOTA-tmpyc66w
consensus: emerging
consensus_note: >-
  The instrument is standard and the reporting discipline is not. Precision and
  recall for generative models are Kynkäänniemi et al.'s (2019) definitions,
  LIT-703, and the diffusion literature does report them in comparison
  tables — this paper, its successors, DiT. What is not routine is using them the way this practice
  asks: to say which side of a fidelity/diversity trade a model sits on, rather
  than as two more columns beside the FID that decides the ranking. `emerging`
  rather than `converged` because the record has one paper whose own table
  contradicts its title and one (LIT-563) that shows FID's ranking can be
  manufactured; it does not have a survey of how often the columns are read.
  Per DP-005, the columns appearing in tables is adoption of the metric, not of
  the practice. Read as of 2026-09.
title: "Report precision and recall beside FID whenever the generator has a fidelity-diversity knob, because FID's best value sits in the interior of that trade"
version: 2
history:
- version: 2
  date: '2026-09-25'
  note: >-
    Corrects a false claim about the instrument this practice recommends. v1 said
    precision and recall are "computed with the same ImageNet network FID uses".
    They are not: LIT-703 uses VGG-16 activations after the second fully
    connected layer, FID uses Inception-v3. The hazard SOTA-337 names survives
    because both are ImageNet classifiers, but the sentence did not, and it took
    filing the defining paper to see it. Adds the source, a better demonstration
    than v1 had (two StyleGAN setups 0.2 FID apart and perceptually opposite),
    and two conditions v1 lacked: `k` and the sample count have to be fixed, and
    two metrics make model selection multi-objective. Recommendation, status and
    consensus unchanged.
tags:
- analysis-and-evaluation
- generative-modeling
date: '2026-09-25'
source:
- LIT-699
- LIT-703
introduced_by:
- LIT-699
implementations: []
summary: >-
  Dhariwal and Nichol (2021), [LIT-699](../literature.d/LIT-699.md). FID mixes fidelity and diversity,
  so on any knob that trades one for the other its optimum is interior and a
  single FID cannot say which side of the trade you are on. Their own Table 5 is
  the demonstration: ADM-G beats BigGAN-deep on FID at ImageNet 128, 256 and 512
  while **losing precision at all three** (0.78/0.86, 0.82/0.87, 0.87/0.88) and
  winning recall by 0.24, 0.24 and 0.13. Report precision and recall, state the
  knob's value, and never read a single FID as "better samples".
---

# SOTA-425: Report precision and recall beside FID whenever the generator has a fidelity-diversity knob, because FID's best value sits in the interior of that trade

## Source

Dhariwal and Nichol (2021), [LIT-699](../literature.d/LIT-699.md) —
[ARXIV-2105.05233](https://arxiv.org/abs/2105.05233). The recommendation comes
from that paper's tables, not from the metric's definition.

**The metric's own paper is not held here.** Precision and recall for generative
models are Kynkäänniemi et al.'s (2019) definitions — the fraction of samples
falling in the data manifold, and the fraction of data falling in the sample
manifold — and `1904.06991` was looked at in the 2026-09-23 metric-definition
sweep and **declined on the grounds that it was "not load-bearing on
anything"**. This practice is what makes it load-bearing, so that decline has
expired and the paper is the next thing this line wants.

## What to do

**If your generator has a knob that trades fidelity for diversity** — a
guidance scale, a truncation level, a sampling temperature, a rejection
threshold — then:

1. **Report precision and recall beside FID**, at the knob value you are
   reporting.
2. **State the knob's value.** A number without it is unreproducible, because
   the knob moves FID more than most contributions do.
3. **Do not read a single FID as a fidelity claim.** FID is a distance between
   distributions; it falls both when samples get better and when coverage gets
   better, and rises when either does at the other's expense.

## Why a single FID cannot answer the question

FID depends on fidelity and diversity together. On a knob that trades them, it
is therefore **non-monotonic**: it improves while the cheaper of the two is
still being bought and worsens once the trade starts costing more than it
returns. The paper states this directly — "since FID and sFID depend on both
diversity and fidelity, their best values are obtained at an intermediate
point" — and the interior optimum is why a model tuned to its best FID is
neither the highest-fidelity nor the most diverse version of itself.

The consequence is that **two models can be ranked oppositely by FID and by
precision**, and that is not a pathological case. It is what the paper's own
headline comparison does, at all three resolutions it ran:

| ImageNet | model | FID ↓ | Prec ↑ | Rec ↑ |
| --- | --- | --- | --- | --- |
| 128 | BigGAN-deep | 6.02 | **0.86** | 0.35 |
| 128 | ADM-G | **2.97** | 0.78 | **0.59** |
| 256 | BigGAN-deep | 6.95 | **0.87** | 0.28 |
| 256 | ADM-G | **4.59** | 0.82 | **0.52** |
| 512 | BigGAN-deep | 8.43 | **0.88** | 0.29 |
| 512 | ADM-G | **7.72** | 0.87 | **0.42** |

A paper titled *Diffusion Models Beat GANs on Image Synthesis* reports, in its
main table, that GANs have higher precision at every resolution it tested. The
title is a claim about FID and coverage. Both readings are defensible and the
three columns are what tells them apart; the one column does not.

## Conditions

**The knob has to exist for this to bite.** Comparing two models with no
fidelity/diversity control is the ordinary case, and there FID's error bar and
sample count matter more — [SOTA-307](SOTA-307.md) for the seed variance, [SOTA-383](SOTA-383.md) for the
sample count.

**Precision and recall do not escape the feature space, and they are not
computed in FID's.** Two separate facts, and v1 of this practice collapsed them
into a false one. The metric's features are **VGG-16 activations after the second
fully connected layer** ([LIT-703](../literature.d/LIT-703.md)); FID's are Inception-v3. So it is a
*different* ImageNet classifier, not the same one — and it is still not a second
opinion on FID's feature space, because that paper's Figure 3c finds Inception-v3
features give "substantially similar" results. Two ImageNet classifiers agreeing
is what [SOTA-337](SOTA-337.md) exists to warn about. This practice answers "which side of the
trade"; [SOTA-337](SOTA-337.md) answers "is the measurement trustworthy", and it covers all
three metrics.

**Fix `k` and the sample count, and do not compare across them.** `k = 3` and
50 000 samples are the conventional defaults, and `k` is not innocuous: higher
values raise *both* precision and recall "in a fairly consistent fashion" until
they saturate at 1.0 and 0.0. A precision of 0.86 at one `k` against 0.82 at
another is not a comparison, for the same reason two FIDs at different guidance
weights are not one.

**Two metrics make model selection multi-objective, so "the best checkpoint"
stops being defined.** With FID alone you take the best snapshot. With precision
and recall, snapshots of one run span a range of tradeoffs, so [LIT-703](../literature.d/LIT-703.md)
reports the **Pareto frontier** — the minimal subset guaranteed to contain the
optimum for whatever tradeoff you turn out to want — rather than assuming one.
Do that instead of picking a snapshot by either column. This is where the
practice costs something real, and it interacts with [SOTA-307](SOTA-307.md): that practice
asks for an error bar over seeds, and a frontier over two objectives is what an
error bar becomes when there are two of them.

**Low on both is a third outcome, not a middle.** Appendix G lowers the
sampling temperature two different ways and gets **low precision and low
recall together**, with blurry samples — a knob that is not on the trade curve
at all. Two columns detect that; FID alone reports it as a worse model without
saying why.

**Upsampling is the counter-example that makes the practice useful.** It raises
precision at roughly constant recall (0.69→0.72 and 0.73→0.75 at 256 and 512),
which guidance cannot do at any scale. A single FID cannot distinguish "moved
along the trade" from "moved off it"; that distinction is the reason the paper
combines the two techniques rather than choosing between them.

## Relation to what the record already says

- [SOTA-307](SOTA-307.md) — FID's **variance** across seeds. This practice is about what FID
  measures, not how noisy it is.
- [SOTA-383](SOTA-383.md) — fix the sample count before comparing. Orthogonal and both apply.
- [SOTA-337](SOTA-337.md) — when an ImageNet network is in the loop, confirm in another
  feature space. That is about FID's **bias**; this is about its **composition**.
- [THEORY-095](../theory.d/THEORY-095.md) — no unbiased estimator of FID exists. Also about the estimator,
  not the quantity.
- [SOTA-424](SOTA-424.md) — choose the guidance weight by which metric you are willing to
  lose. That practice names FID and IS because its source's sweep reports those
  two; precision and recall are the pair that name the trade's two ends
  directly, and this is where they come from.
