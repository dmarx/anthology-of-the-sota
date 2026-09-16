---
number: 78
status: Read
formerly:
- NOTE-tmpjskyc
paper: LIT-233
title: 'Neural Thickets'
version: 1
date: '2026-09-15'
summary: >-
  The neighbourhood of a pretrained weight vector is dense with task-improving
  Gaussian perturbations, the density rises monotonically with model scale,
  and the perturbations that help are specialists rather than uniform
  improvements — which together are why a single parallel round of random
  guessing plus majority voting can match PPO, GRPO and ES at equal training
  FLOPs.
---

# NOTE-078: Neural Thickets

## Contribution

Reframes a pretrained checkpoint as a *distribution* over parameter vectors
rather than a point, and measures two properties of that distribution that
nobody had: how often a random Gaussian perturbation improves a downstream
task, and whether the perturbations that improve one task improve the others.
Both rise with model scale. The practical consequence — that a single
parallel round of guess-and-check is a viable post-training method for models
above about 1.5B — is offered as a probe of the measurement rather than as a
method to adopt, and the paper is explicit about that ordering.

## Key insight

**Pretraining does not just move the weights to a good point; it changes what
is nearby.** A small or untrained model sits on a local peak of any
individual task's accuracy, so improvement requires structured search — the
needle in a haystack. A large pretrained model sits in a *valley* of each
individual task's accuracy, surrounded by higher ground in many directions at
once, and the directions are not the same direction: each is an expert at
something different. The aggregate pretraining loss is at a minimum the whole
time, which is why this structure is invisible to the single-objective
landscape analysis the field usually runs. Post-training in that regime is
selection from something already present, not construction of something new.

## Assumptions

The measurements are empirical and carry no formal conditions, but the
setting is narrow in specific ways and they bound everything below:

- **Perturbations are isotropic Gaussian in the full parameter space**, with
  σ ∈ {1, 2, 3}e-3 for the method and σ = 1e-3 for the density study. No
  structure, no layer-wise scaling, no low-rank restriction.
- **"Task expert" means "scores well on the benchmark"**, which the paper
  states and then measures the consequences of (§8). Format and style count
  as expertise under this definition.
- **Density is measured on one model family** — Qwen2.5 instruction-tuned,
  0.5B to 32B — on three reasoning tasks; diversity on seven tasks with 500
  perturbations.
- **The method is evaluated at 8B and below**, on Qwen2.5, OLMo3 and
  Llama-3.1, with baselines matched on *training* FLOPs and not on
  *inference* FLOPs.
- **Scoring uses a held-out set of roughly 200 examples.** The method needs a
  cheap, reliable scalar score per candidate; it inherits every problem a
  verifier has.

## Key results

- **Solution density `δ(m) = P[s(θ+ε) ≥ s(θ)+m]` rises monotonically with
  model size**, at every margin `m` tested. On GSM8K the fraction of
  perturbations at least matching base accuracy goes 0% → 64% across
  0.5B → 32B (Fig. 3, Fig. 12).
- **Spectral discordance rises monotonically with model size** (Fig. 3b) —
  the task rankings of sampled perturbations become *more* orthogonal as
  models grow, supporting specialists over generalists. PCA of the per-seed
  performance vectors over seven tasks separates into clusters with
  complementary strengths (Fig. 4).
- **RandOpt at N=5000, K=50 matches or beats PPO, GRPO and ES at equal
  training FLOPs** across seven tasks (Table 4). Best cells include OLMo3-7B-
  Instruct on Countdown at 85.0% (ES 71.0, GRPO 68.5, PPO 69.0) and
  Qwen2.5-3B-Instruct on GSM8K at 87.1% (GRPO 83.2, ES 85.8).
- **ES + 50-way test-time majority vote takes the best or runner-up cell in
  roughly half of the same table**, beating RandOpt on GSM8K, MATH-500 and
  OlyBench at several scales (Table 4). The paper's §5.4 asks whether
  ensembling helps the baselines and answers yes, and that the gap between
  selection methods shrinks as training proceeds.
- **Wall clock**: one training step against 200 (GRPO), 600 (PPO) and 167
  (ES). OLMo3-7B-Instruct to 70% on Countdown in **3.2 minutes** on 200
  GH200s.
- **The method has a scale threshold.** No gain at GPT-2 0.1B, small gains at
  0.5B, a sharp rise from ~1.5B, then shrinking relative gains as base
  accuracy catches up. From an untrained initialization it is near zero at
  every scale (Fig. 8).
- **Ensembling is load-bearing**: K=1 is substantially worse than K=50,
  though K=1 still beats base (Fig. 11).
- **Population size helps log-linearly** and the optimal selection ratio
  *falls* as N grows; at large N, keeping the top 1% is enough (Fig. 10).
- **Accuracy decomposition on GSM8K** (Qwen2.5-3B-Instruct, N=3000, K=50)
  splits the gain into a "reasoning thicket" (problems the base model got
  wrong) and a "format thicket" (problems it got right and mis-formatted),
  with substantial contributions from both — and reports the same shape for
  GRPO (Fig. 9).
- **Distillation** of the top-50 into one model: 84.3% against the ensemble's
  87.1% on GSM8K at 3B, at ~2% of training cost (Table 2).
- **A minimal replication with no language in it.** An MLP next-value
  predictor over a mixture of 1D signal families shows three regimes: needle
  (no pretraining), thicket (mixture pretraining), and **plateau** (pretrained
  on linear signals only — already at ceiling, guessing buys nothing).

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | The fraction of random Gaussian perturbations that improve a downstream task rises monotonically with model scale | strong | direct measurement, Qwen2.5 0.5B–32B, three tasks, multiple margins (Fig. 3, 12) |
| C2 | Those perturbations are task specialists, not uniform improvements | strong | spectral discordance rising with scale, plus PCA clustering over seven tasks (Fig. 3b, 4) |
| C3 | Thickets require pretraining on a *variety* of tasks, not merely a lot of pretraining | moderate | the 1D signal experiment's three regimes (§3); shown in the toy setting, asserted for LLMs |
| C4 | One parallel round of random guessing plus top-K majority voting is competitive with PPO, GRPO and ES at equal training FLOPs | moderate | Table 4, but the baselines answer with one sample where this answers with fifty |
| C5 | Random guessing is *better* than ES | weak | not supported; ES + TT-MV matches or beats it in about half the table, and the authors do not claim it |
| C6 | The method fails below ~1.5B and from scratch | strong | Fig. 8, including the from-scratch control at every scale |
| C7 | The gains are not an artifact of sandbagging | moderate | OLMo3 base is fully open and improves; §5.3 and App. G argue it, no direct test |
| C8 | A substantial part of the gain is output formatting rather than new capability | strong | the paper's own decomposition, §8 — and it holds for GRPO too |

## Method

RandOpt, in two phases.

**Training (one step, fully parallel).** Sample `N` seeds; assign each a
noise scale `σ_i` drawn uniformly from a small set `Σ`; form
`θ_i = θ + σ_i · ε(seed_i)` with `ε ~ N(0, I_d)`; evaluate each `θ_i` on a
small held-out set; keep the top `K` by score. Workers never communicate
during this phase — scores are gathered once, against `T` times for ES.

**Inference.** Generate from each of the `K` selected models and return the
majority answer.

Only a seed and a scale need to be stored per candidate, so the population is
cheap to represent; the cost is `N` evaluations, which is what "equal
training FLOPs" is buying against the baselines' optimizer steps.

## Concepts

- **Thicket regime** — the state of a parameter vector whose Gaussian
  neighbourhood contains a substantial fraction of task-improving solutions.
  Contrasted with the **needle in a haystack regime** (solutions vanishingly
  rare, structured search required) and the **plateau regime** (the base
  model is already optimal for the task, so nothing nearby helps).
- **Solution density `δ(m)`** — `P[s(θ+ε) ≥ s(θ)+m]` for `ε ~ N(0, σ²I)`.
  The hit rate of random guessing at margin `m`.
- **Spectral discordance** — a scalar read off the spectrum of the
  correlation matrix of per-task percentile ranks across sampled seeds. 0 is
  orthogonal task rankings (specialists); parallel rankings (generalists)
  sit at the other end.
- **Format thicket / reasoning thicket** — the paper's own split of where an
  improvement came from: making an already-correct answer parseable, versus
  answering a question the base model got wrong.

## Connections

Positions itself against three lines. Against **flat-minima** work, its point
is that a flat *aggregate* landscape is compatible with spiky *per-task*
landscapes, and that the per-task structure is what governs adaptation — the
pretrained weights need not minimize any single task. Against the **lottery
ticket hypothesis**, it agrees about random initialization and claims a
qualitatively different regime after pretraining, so the two are about
different starting points rather than in tension. Against **post-training as
reweighting** (KL-regularized PPO and friends), it is the same idea taken
literally into weight space: the behaviours are already in the pretrained
distribution, and post-training selects among them.

Its most direct relative is Qiu et al.'s evolution strategies at LLM scale,
which it cites in the same breath as its own thesis — *it doesn't take much
to obtain good downstream solutions given the right pretrained
representation* — and also runs as a baseline. Machine-readable lineage is on
the LIT.

## Recommendations

- **R1** — If wall-clock time and parallelism matter more than inference
  cost, and your task has a votable answer, one parallel round of scored
  random perturbation plus top-K majority voting is a real option above ~1.5B.
  *Topic:* post-training. *Status:* experimental. *Strength:* moderate.
  *Applies when:* a cheap verifier exists, the answer is discrete, the
  cluster is wide, and `K` forward passes per answer are affordable.
- **R2** — When comparing a post-training method that ensembles at inference
  against one that does not, give both the same test-time budget. This
  paper's own matched arm (ES + TT-MV) changes which method wins in about
  half the table. *Topic:* evaluation. *Status:* standard. *Strength:*
  strong. *Applies when:* any method comparison where the arms differ in
  samples per answer.
- **R3** — Decompose a post-training gain into format-fixing and
  capability before believing it. *Topic:* evaluation. *Status:*
  experimental. *Strength:* moderate. *Applies when:* the benchmark is
  scored by a strict answer checker.
- **R4** — Expect gradient-free post-training to fail on small or untrained
  models, and treat that as a property of the model rather than of the
  method. *Topic:* post-training. *Status:* experimental. *Strength:* strong.

## Bearing on the record

<!-- inactive-ok-block: THEORY-006, SOTA-212 — both Proposed, both
     filed from this reading in this same change; this paragraph is the
     record of that filing, not a reliance on either -->
**Two documents filed from this reading.** [THEORY-006](../theory.d/THEORY-006.md) carries the
density-and-diversity claim, `Proposed`, and [SOTA-212](../practices.d/SOTA-212.md) carries the
method, `Proposed` and `unreplicated`.

**It replicates [SOTA-154](../practices.d/SOTA-154.md), and that is what promoted it.** That practice
rested entirely on [LIT-211](../literature.d/LIT-211.md), whose authors ran it. This paper runs ES as a
baseline across six further tasks and three model families, at matched
training FLOPs, with PPO and GRPO grid-searched over learning rate and batch
or group size while ES ran a single fixed configuration — and finds ES strong
enough that ES plus test-time voting beats the paper's own method in about
half the table.

Arriving as a *baseline* is not a discount on that: a group tuning the rival
harder than the method, in a paper arguing for something else, is a strong
form of evidence.

**What is a discount on it is authorship, and this note missed it twice.** The
first draft called the result "the weaker of the two" for being a baseline and
was corrected; the correction then called it an independent replication, which
is also wrong. **Yulu Gan is the second author of [LIT-211](../literature.d/LIT-211.md)**, the paper this
practice rests on, and this paper cites it as prior work. The tuning asymmetry
still favours the baseline and the six added tasks are still six added tasks —
but `promote_when` excluded "further results from the same group", and an
overlapping group is nearer to that than to what it asked for.

<!-- inactive-ok-block: SOTA-154, THEORY-006 — both Proposed; the
     paragraph says the explanation this reading files is the one that
     practice lacked, which is a claim about both documents' standing -->
**It supplies the explanation [SOTA-154](../practices.d/SOTA-154.md) never had.** Nothing in the record
said why a gradient-free method should find anything in a billion dimensions.
[THEORY-006](../theory.d/THEORY-006.md) now does, and predicts where it stops.

**R2 above is the one thing here the record has no home for.** The anthology
carries evaluation practices — reporting zero-shot and in-distribution
separately, accounting for test-set proximity — and nothing about matching
test-time sample budgets across compared arms. This paper demonstrates the
failure and its fix in its own table, but does not *recommend* anything, so
filing a practice would mean the record inventing a recommendation and
attributing it. Left here deliberately, as a candidate for whoever files the
practice that does recommend it.

## Limitations

The authors state five, and all five are real: the method needs pretraining
and fails from scratch; how far beyond the base model it can reach is
unknown, and the scaling appears to saturate in log resources; inference
costs `K` passes, with distillation as a partial and non-general escape;
majority voting does not extend to structured prediction; and the mechanism
by which pretraining produces a thicket is not explained.

Two more from this reading. **The density and diversity measurements run on
one model family**, so the scaling law is a Qwen2.5 scaling law until someone
repeats it. And **the headline table's asymmetry in test-time budget is
disclosed but not corrected in the figure that carries the argument** — the
matched arm is present in Table 4 and in §5.4, and a reader taking Figure 6
at face value would come away with the wrong conclusion.

## Open questions

- **What about pretraining creates the thicket?** The 1D experiment points at
  variety in the pretraining distribution. What would close it: a controlled
  pretraining sweep on LLMs varying data mixture diversity at fixed token
  count, with `δ` measured at the end of each.
- **Where is the transition, really?** "Around 1.5B" is one family on one
  task. What would close it: the density curve for two more families,
  which would also say whether the threshold tracks parameters, tokens, or
  benchmark headroom.
- **Does the thicket survive a benchmark that cannot be moved by
  formatting?** What would close it: the same decomposition on a task scored
  by a model or an execution harness rather than a string match.
- **Is anisotropic perturbation better?** Everything here is isotropic
  Gaussian over all parameters. Whether density is concentrated in particular
  layers or directions is not asked, and it bears directly on how large `N`
  has to be.
