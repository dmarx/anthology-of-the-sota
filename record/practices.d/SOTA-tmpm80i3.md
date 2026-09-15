---
status: Proposed
promote_when: >-
  An independent group running it against a policy-gradient or ES baseline
  that gets the same test-time ensemble budget, on a model above 8B — or a
  released model whose post-training recipe used it. What would not satisfy
  this: a further result from these authors, or a comparison in which the
  baseline answers with one sample while this answers with fifty.
consensus: unreplicated
consensus_note: >-
  One group, one paper, models at 8B and below. It is the second entry in the
  record's gradient-free post-training line and the first independent
  evaluation of the first (SOTA-154), which is corroboration of the paradigm
  rather than of this method.
title: 'Post-train by scoring many random weight perturbations in one parallel pass and majority-voting the best of them'
version: 1
tags:
- adaptation-and-tuning
date: '2026-09-15'
# The paper ran the comparison itself against PPO, GRPO and ES at matched
# training FLOPs. One source: no replication exists, which is what
# promote_when is about.
source:
- LIT-tmphm6g2
# inactive-ok-block: ADR-030 — Proposed, and cited for what it says the field
# is FOR, not as a settled decision; `introduced_by:` is required in
# luria.yaml today whatever becomes of the decision that asked for it
# NOT the same code as `source:`, and this is the case the field exists for
# (ADR-030). LIT-tmphm6g2 produced the evidence and explicitly declines to
# make the recommendation — "our goal is not to promote RandOpt as superior
# to alternative methods. Rather, we use it as a probe." The work that first
# stated the instruction "post-train by perturbing the weights and selecting,
# rather than by gradient" is LIT-211, and RandOpt is that instruction with
# the iteration count set to one and an ensemble on the end.
introduced_by:
- LIT-211
# The lineage, not a rivalry: this is the one-shot ensembled form of SOTA-154
# and sits on the same line. The paper did also measure the two against each
# other and the result was a tie; that fact is in the body rather than in a
# second relation over the same pair.
extends:
- SOTA-154
# The comparison the paper ran against the other paradigm: the group baseline
# inside GRPO. Stated here, on the practice that ran it; the fixer writes the
# other side.
compared_against:
- SOTA-145
implementations: []
summary: >-
  Qiu et al. introduced it ([LIT-211](../literature.d/LIT-211.md)); Gan and Isola (2026),
  [LIT-tmphm6g2](../literature.d/LIT-tmphm6g2.md) — [ARXIV-2603.12228](https://arxiv.org/abs/2603.12228) — measured this form of it. Sample N Gaussian
  weight perturbations, score them on a few hundred held-out examples, keep
  the top K and majority-vote at inference. At equal training FLOPs it
  matches or beats PPO, GRPO and ES across seven tasks at 0.5B–8B, in one
  parallel step instead of hundreds of sequential ones — 3.2 minutes for
  OLMo3-7B on Countdown across 200 GH200s. Filed Proposed: one group, K
  forward passes per answer, and discrete answers only.
explained_by:
- THEORY-tmp38myz
---

# SOTA-tmpm80i3: Post-train by scoring many random weight perturbations in one parallel pass and majority-voting the best of them

## Source, and who is recommending this

The evidence is Gan and Isola (2026), [LIT-tmphm6g2](../literature.d/LIT-tmphm6g2.md) —
[ARXIV-2603.12228](https://arxiv.org/abs/2603.12228). **The recommendation is not theirs.** That paper
measures the method and declines to promote it, in as many words: "our goal
is not to promote RandOpt as superior to alternative methods. Rather, we use
it as a probe." The instruction — post-train by perturbing the weights and
selecting among the results, rather than by following a gradient — was
<!-- inactive-ok-block: ADR-030 — Proposed, and cited for the distinction it
     draws rather than as a settled decision; the field is required in
     luria.yaml today either way -->
stated by Qiu et al. ([LIT-211](../literature.d/LIT-211.md)), and this is that instruction with the
iteration count set to one and an ensemble on the end. `introduced_by:` says
so, which is the distinction [ADR-030](../decisions.d/ADR-030.md) requires every practice to make.

The procedure, called RandOpt, is four lines:

1. Draw `N` seeds. Give each a noise scale `σ` drawn from a small set — the
   paper uses `Σ = {1, 2, 3}e-3` — and form `θ_i = θ + σ_i · ε(seed_i)` with
   `ε ~ N(0, I)`.
2. Score every `θ_i` on a small held-out set (~200 examples).
3. Keep the top `K`.
4. At inference, generate from all `K` and majority-vote the answers.

`N = 5000, K = 50` throughout the paper. Nothing is sequential: the workers
never communicate during training and the scores are gathered once, against
`O(T)` rounds of communication for ES and `O(T)` optimizer steps for PPO and
GRPO.

## Why this is a recommendation and not just a result

The claim that carries it is the **wall-clock and parallelism** one, not the
accuracy one. Matched on training FLOPs, RandOpt wins or ties most cells of a
seven-task table across Qwen2.5 0.5B–3B, OLMo3-7B base and instruct, and
Llama-3.1-8B-Instruct. But it does that in **one step**: OLMo3-7B-Instruct
reaches 70% on Countdown in 3.2 minutes on 200 GH200s. Where nodes are cheap,
interconnect is expensive and time-to-result is what binds — and in federated
or otherwise decentralized settings, where communicating gradients is the
problem — that is a different trade from the one every other post-training
method offers, and it is the reason to reach for this rather than a margin on
a benchmark.

## Conditions, and they are severe

<!-- inactive-ok-block: THEORY-tmp38myz — Proposed, filed from the same paper
     in this same change, and held no more firmly than this practice is -->
**The base model has to be big enough.** Below roughly 1.5B parameters the
gains are small; at GPT-2 scale there are none; applied to un-pretrained
weights the method returns near zero at every scale tested. This is not a
tuning failure — [THEORY-tmp38myz](../theory.d/THEORY-tmp38myz.md) is the account of it, and the practice
inherits its boundary. As base accuracy rises the relative gain also shrinks,
so the window is real on both sides.

**The answer has to be votable.** Majority voting is the whole of the
inference step. For a story, a molecule or an image there is no obvious vote;
the paper offers mean-ensembling a diffusion model's denoising steps as a
proof of concept and claims nothing more.

**Inference costs `K` forward passes.** `K = 1` is substantially worse than
`K = 50`, so the ensemble is not optional. Distilling the top-`K` into one
model recovers most of it — 84.3% against 87.1% on GSM8K for
Qwen2.5-3B-Instruct, at about 2% of training cost — but that reintroduces the
sequential training the method exists to avoid.

**Part of what you are buying is formatting.** The paper's own decomposition
of the GSM8K gain finds a substantial share is answers the base model already
had, emitted in a form a strict checker rejects. It reports the same of GRPO,
so this is not a reason to prefer the baseline — it is a reason to check what
moved before believing a number.

## Against the record's post-training spine

<!-- inactive-ok-block: SOTA-146 — Proposed, and named as one of the three
     practices that assume the paradigm this steps outside of -->
[SOTA-129](SOTA-129.md) makes reinforcement learning with verifiable rewards the third stage
of the reasoning recipe, [SOTA-145](SOTA-145.md) recommends the group baseline inside it and
[SOTA-146](SOTA-146.md) corrects the objective. All three assume the paradigm. This is the
second practice in the record to reach the same goal from outside it, after
[SOTA-154](SOTA-154.md) — which it `extends:` rather than rivals. Both are gradient-free,
both perturb the full parameter space with Gaussian noise, and this one is ES
with the iteration count set to one and an ensemble on the end.

**The honest comparison against [SOTA-154](SOTA-154.md) is a tie, not a win.** The paper's
headline gives this method a 50-way ensemble and the RL baselines a single
sample, which it says plainly "disadvantages the baseline but reflects
current standard usage". It also runs the matched version — ES plus 50-way
test-time majority vote — and that arm takes the best or runner-up cell in
roughly half the table, beating this one on GSM8K, MATH-500 and OlyBench at
several scales. The paper's own conclusion is that once you ensemble, the
selection method matters less and less. **What this practice is evidence for
is the paradigm and the parallelism; a practitioner choosing between it and
[SOTA-154](SOTA-154.md) on accuracy alone has no result to choose on.**

That tie is also the most useful thing here for a reader evaluating anyone
else's post-training numbers: an ensembled method compared against a
one-sample baseline is a comparison about ensembling.

## Known implementations

- None in a released model. The authors publish code at
  `github.com/sunrainyg/RandOpt`.
