---
number: 216
status: Read
formerly:
- NOTE-tmpfcpro
paper: LIT-467
title: 'Chain-of-Thought Prompting'
version: 1
date: '2026-09-21'
summary: >-
  Worked reasoning steps in the few-shot exemplars, nothing else. Reading it:
  the three ablations are the contribution — it is not the equation, not the
  extra tokens, and not knowledge activation — and the effect is absent or
  negative below about 100B parameters.
---

<!-- inactive-ok-file: SOTA-130 — Proposed, and named for the same reason: it extends what this paper established and had no antecedent in the record -->
# NOTE-216: Chain-of-Thought Prompting

## Contribution

Two lines of work existed and each had a fatal cost. Rationale-augmented
training produced models that showed their working, but required a large
corpus of hand-written rationales. Few-shot prompting needed no training at
all, but worked poorly on anything requiring reasoning and — the damning part
— did not improve much with scale. This combines them: put the rationales in
the eight exemplars. The annotation cost collapses to eight examples and the
scaling curve, previously flat, turns sharply upward.

## Key insight

The capability was already in the model and the prompt was the bottleneck.
The paper's own summary is that "standard prompting only provides a lower
bound on the capabilities of large language models" — which is a claim about
measurement, not about training, and it is the reason a method this simple
produced a step change. Nothing about the model was altered.

## Assumptions

- **Sufficiently large models.** The effect is an emergent ability of scale
  in the authors' framing, appearing around 100B parameters. Below that it is
  absent or harmful.
- **Few-shot setting.** Annotation cost is negligible for eight exemplars and
  the paper says explicitly that it would be prohibitive for fine-tuning.
- **Tasks expressible in language.** Arithmetic, commonsense and symbolic
  reasoning; the claim of general applicability is "at least in principle, to
  any task that humans can solve via language", which is a hope rather than a
  result.
- **Three model families** — LaMDA, GPT-3, PaLM — with PaLM 540B carrying the
  headline numbers.

## Key results

- **GSM8K** — PaLM 540B with eight chain-of-thought exemplars reaches state
  of the art, beating a fine-tuned GPT-3 *with a verifier*. Performance more
  than doubles for the largest GPT and PaLM models. *Holds when:* ≥100B
  parameters.
- **Emergence** — no positive effect for small models on the arithmetic
  benchmarks; gains appear only at ~100B. Small models generate fluent but
  illogical chains and do worse than standard prompting.
- **Gain tracks difficulty** — largest on the hardest dataset, negative or
  negligible on SingleOp, the single-step subset of MAWPS.
- **Ablation: equation only** — prompting for just the equation does not
  help on GSM8K, though it does help on one- and two-step problems where the
  equation follows directly from the question.
- **Ablation: variable compute only** — emitting a sequence of dots as long
  as the needed equation performs at baseline. Extra tokens alone buy
  nothing.
- **Ablation: chain of thought after the answer** — performs at baseline, so
  the chain is not merely activating pretraining knowledge; the answer
  depends on it.
- **Robustness** — three independent annotators all beat standard prompting;
  exemplars randomly sampled from the GSM8K training set do as well as
  hand-written ones; robust to exemplar order and count.
- **Commonsense** — gains across five datasets, with StrategyQA at 75.6% vs a
  69.4% prior best and sports understanding beating an unaided sports
  enthusiast (95.4% vs 84%). Minimal on CSQA, which the paper says.
- **Symbolic** — chain of thought lets the model generalize out of
  distribution to longer sequences than the exemplars showed.
- **Error analysis** — of 50 correct answers from LaMDA 137B, all but two had
  correct chains. Of 50 wrong answers, 46% were nearly correct and 54% had
  major errors. Scaling 62B → 540B fixes many one-step-missing and semantic
  errors.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Worked steps in exemplars substantially improve multi-step reasoning | strong | three model families, three task categories, large margins, robust to annotator and exemplar choice |
| C2 | The benefit is not from emitting the equation | strong | direct ablation |
| C3 | The benefit is not from spending more tokens | strong | the dots ablation — the cleanest negative result in the paper |
| C4 | The model's answer depends causally on the chain | moderate | the after-the-answer ablation supports it; "depends causally" is a reading of an accuracy comparison, not a mechanistic result |
| C5 | The ability is emergent at ~100B parameters | moderate | measured on the model sizes available in 2022, and "emergent" is a description of those curves, not a mechanism |
| C6 | Whether the model is "reasoning" | not claimed | the authors explicitly decline this and leave it open |

## Method

Replace each few-shot exemplar's `⟨input, output⟩` with
`⟨input, chain of thought, output⟩`, where the chain is a series of
intermediate natural-language steps. Eight exemplars. Prompt an off-the-shelf
model. That is the entire method.

## Concepts

- **Chain of thought** — a coherent series of intermediate natural-language
  reasoning steps leading to the answer. The authors prefer this to
  "solution" or "explanation" because those conventionally come *after* the
  answer, and the ordering is the point.
- **Emergent ability of scale** — a capability absent in smaller models that
  appears past a threshold.

## Connections

Builds directly on few-shot prompting from GPT-3 ([LIT-035](../literature.d/LIT-035.md)), declared as
`extends`. Positioned against rationale-augmented fine-tuning, whose
annotation cost it avoids, and against neuro-symbolic methods that use formal
languages instead of natural ones.

The relation to [LIT-464](../literature.d/LIT-464.md) is worth stating carefully, because a
fast reading makes them contradict. That paper proves a one-layer decoder
*with* chain of thought can express a composition a constant-depth one
cannot, and describes chain of thought as providing extra computation space.
This paper's dots ablation shows that extra tokens *carrying no information*
buy nothing. Those are consistent: the theoretical benefit comes from writing
intermediate **results** into the context and reading them back, and a row of
dots holds no results. One says the room exists; the other says the room only
helps if you put something in it.

## Bearing on the record

- **It fills the trunk named in the previous contribution.** Before this the
  record held no chain-of-thought practice in 278, and [SOTA-127](../practices.d/SOTA-127.md) —
  filter such traces out of tiny models' training data — was the entire CoT
  presence. That practice now has the paper that explains why small models
  produce bad chains sitting next to it.
- **It produces [SOTA-279](../practices.d/SOTA-279.md).**
- **C5 sits in a live tension the record already holds.** [SOTA-037](../practices.d/SOTA-037.md)
  says in-context learning emerges at scale; [SOTA-200](../practices.d/SOTA-200.md) says to check
  whether an emergent capability is a metric artefact before believing it.
  And this paper's emergence claim is measured on exact-match accuracy over
  multi-step answers — which is, almost word for word, the case BIG-bench
  ([LIT-077](../literature.d/LIT-077.md)) singles out: tasks showing breakthrough behaviour "often
  involve multiple steps or components, or brittle metrics". A chain-of-thought
  answer is scored right only when every step lands. That does not make the
  effect unreal — the *gains* at 540B are enormous and survive three ablations
  — but the **shape** of the curve is the shape `SOTA-200` says to distrust,
  and nobody has re-run this against a continuous score. The record should not
  resolve that from here and should not pretend it is not there.

  Schaeffer et al.'s "Are Emergent Abilities of Large Language Models a
  Mirage?" (`ARXIV-2304.15004`) is the paper that argues this case directly,
  and the record does not hold it. Named here as the obvious next filing.
- **It is the 2022 statement of [SOTA-278](../practices.d/SOTA-278.md).** "Standard
  prompting only provides a lower bound on capabilities" is that practice's
  claim, demonstrated rather than argued, three years before the papers the
  practice is sourced to.
- **Much of what the record already carries assumes it.** [SOTA-130](../practices.d/SOTA-130.md)
  skips reasoning SFT and runs RL with verifiable rewards; the reasoning
  models evaluated in [LIT-466](../literature.d/LIT-466.md) are defined by an extended
  thinking trace. Neither had an antecedent in the record for the thing being
  extended.

## Limitations

The authors list four and they are unusually candid.

- **Whether the model is reasoning is left open**, explicitly.
- **Annotation cost is trivial at eight exemplars and prohibitive for
  fine-tuning**, so the method's cheapness is specific to the few-shot
  setting.
- **No guarantee of correct reasoning paths.** Chains can be wrong and still
  reach the right answer, and vice versa — their own error analysis found two
  of fifty correct answers arrived through incorrect chains.
- **The scale requirement makes it costly to serve.**

And two the record should add:

- **The emergence threshold is a 2022 fact about 2022 models.** Whether ~100B
  is still the boundary for models trained on more data with better recipes
  is not something this can answer, and small-model reasoning distillation
  has moved since.
- **No cost accounting.** Chains of thought are tokens, and on the easiest
  problems the paper reports *negative* gains — so the practice has a
  regime where it loses on both axes, which the paper notes without
  quantifying.

## Open questions

- Is the ~100B threshold a property of scale or of the training data
  distribution of that generation?
- How much of the emergence is the metric? Nobody re-ran this against a
  continuous score.
- The dots ablation is the sharpest negative result here and has never, as
  far as this reading knows, been repeated against modern models that are
  explicitly trained to use thinking tokens — where the answer could easily
  be different.
