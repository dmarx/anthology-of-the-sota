---
status: Read
paper: LIT-tmpbtdlg
title: 'How do language models learn facts?'
version: 1
date: '2026-09-20'
summary: >-
  Factual recall is learned in three phases, and the plateau between generic
  statistics and individual knowledge is the attention recall circuit being
  built — patching in a trained model's attention patterns removes the
  plateau. Imbalanced data shortens the plateau and slows acquisition after
  it, so a schedule from imbalanced to uniform beats either fixed choice.
---

# NOTE-tmp7om7u: How do language models learn facts?
<!-- inactive-ok-file: SOTA-130 — Proposed, and named among the task-stage curricula this reading distinguishes itself from -->

## Contribution

Identifies what a specific and common loss plateau *is*, by intervention
rather than inference. Factual recall training passes through three phases,
and the long flat middle one coincides with the formation of the
attention-based circuit that recall depends on; patching a reference model's
attention patterns into a training model removes the plateau entirely, and
patterns drawn from progressively later in the plateau work progressively
better. From that mechanism the paper derives a data-distribution trade-off
with opposite signs on either side of the plateau, and turns it into a
schedule that beats every fixed distribution tested. It also reports that
hallucinations begin at the same moment knowledge does, and that fine-tuning
absorbs new facts slowly while corrupting old ones quickly.

## Key insight

**A plateau can be a prerequisite being built, and while it is being built
the gradient cannot reach the thing that needs to learn.** Factual recall in
a transformer runs through a known circuit: early attention assembles the
name into a representation, MLPs act as a key-value store, and a late
attention layer selects the right value given the attribute type. Until that
last piece exists, the error at the attribute token is spread across
irrelevant positions instead of flowing back to the name tokens — so the
key-value store cannot learn, and the loss sits still. The plateau is not the
model failing to make progress; it is the model making the only progress that
is available, on a component whose value is invisible in the loss until it is
finished.

## Assumptions

- **A synthetic biography task**, with information about the individual and
  attribute type placed before the attribute value so that every prediction
  is a recall problem. This is what makes knowledge countable and directly
  measurable as loss, rather than requiring question-answering fine-tunes at
  every checkpoint.
- **Attribute loss** is the main metric, chosen over accuracy for
  interpretive power and smoother progression across scales.
- The three-phase structure and the circuit account are for **this recall
  task**; the paper offers the mechanism as likely general and does not show
  it elsewhere.
- The patching experiment assumes attention patterns can be transplanted
  meaningfully between a reference and a modified model — which is what makes
  its result an intervention rather than a correlation, and is also its main
  methodological commitment.
- Biographies are never repeated, which the authors note distinguishes their
  setup from Allen-Zhu and Li's "celebrities" result.

## Key results

- **Three phases**: generic attribute-value statistics (short), plateau at
  exactly the no-knowledge baseline, then individual-specific knowledge.
  **Plateau length grows almost linearly with population size**, which
  supports a statistical account — the model must see an individual several
  times to learn that values are individual-specific — over a pure
  saddle-point account.
- **Attention patching removes the plateau.** Patterns from later reference
  checkpoints are better; patterns from *very early* training are worse than
  the untrained ones, because the model is then attending to attribute-type
  tokens to predict the generic distribution.
- **Attention to name tokens rises through the plateau**, measured at the
  position that tests recall — the direct signature of the extraction circuit
  forming.
- **The trade-off**: plateau length is governed by the frequency of the most
  common individuals; post-plateau acquisition speed by the frequency of the
  least common. So imbalance shortens the plateau and slows what follows.
- **Optimal fixed imbalance** is an inverse power law with exponent between
  1 and 2, roughly independent of population size, and the optimum shifts
  toward more imbalance as the plateau takes a larger share of the budget —
  larger populations or shorter runs.
- **A dynamic schedule beats the best fixed distribution**, minimising
  plateau length and maximising acquisition rate in turn.
- **Hallucinations emerge simultaneously with knowledge** — overconfident
  predictions on unseen individuals begin exactly when individual-specific
  knowledge does.
- **Fine-tuning is a poor knowledge-insertion mechanism**: slow to absorb,
  fast to corrupt existing parametric memories.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Knowledge acquisition has three phases with a plateau whose length scales with population | strong | measured across population sizes, five seeds |
| C2 | The plateau is the attention recall circuit forming | strong | patching intervention removes the plateau; attention-to-name rises through it; two independent signatures |
| C3 | Imbalanced distributions shorten the plateau and slow subsequent acquisition | strong | swept over an inverse-power-law exponent at several population sizes |
| C4 | A dynamic data schedule beats any fixed distribution | moderate | demonstrated for this task; the schedule is tuned in the same setting it is evaluated in |
| C5 | Hallucinations arrive with knowledge rather than after it | moderate | co-occurrence in this synthetic setting, where "unseen individual" is exactly definable |
| C6 | Fine-tuning corrupts existing knowledge faster than it adds new | moderate | measured here; a familiar phenomenon given a quantitative form in a controlled setting |

## Method

Construct biographies for a controlled population, with attributes embedded
in varied templates and the individual and attribute type always preceding
the value, so that attribute-value prediction is factual recall and its loss
is a knowledge measure.

Train, and track the attribute loss against a computed no-knowledge baseline
to locate the phases.

For the circuit claim: snapshot a reference model at various points in its
training, and replace a second model's attention patterns with the reference's
throughout that second model's training. Measure how easily the task is
learned as a function of when the reference snapshot was taken. Separately,
track attention paid to name tokens at the recall position across training.

For the distribution results: set individual occurrence probability to an
inverse power law with exponent `a`, sweep `a` at several population sizes
under a fixed step budget, and then schedule `a` over training.

## Concepts

- **Attribute loss / attribute accuracy** — loss and accuracy on predicting
  the attribute value token; the knowledge metric.
- **No-knowledge baseline** — the loss an ideal model with no
  individual-specific knowledge would achieve. The plateau sits on it exactly,
  which is what makes the plateau interpretable.
- **Extraction circuit** — the late attention operation selecting the value
  matching the attribute type from the individual's representation.
- **Attention patching** — transplanting a reference model's attention
  patterns into a training model, to test whether those patterns are the
  bottleneck.

## Connections

Builds on the mechanistic account of factual recall in transformers — first
attention assembling the name, MLPs as key-value store, final attention
selecting by attribute type — and asks when each piece appears rather than
what it does once trained.

Relates to three prior findings the paper names: Allen-Zhu and Li's
"celebrities" benefit, which it partly explains; Charton and Kempe on
repetition helping arithmetic training, whose learning curves show many
plateaus; and Park et al. on low task diversity shortening plateaus at a cost
in out-of-distribution generalisation. The last is the warning attached to
the schedule.

## Recommendations

- **R1** — Start the training distribution imbalanced and flatten it, rather
  than holding it uniform. *Topic:* data schedule. *Status:* experimental.
  *Strength:* moderate. *Applies when:* the knowledge to be acquired is
  spread over many rarely-occurring entities, which is the pretraining case.
- **R2** — Expect a plateau proportional to the number of entities, and do not
  read it as the run having failed. *Topic:* training dynamics. *Status:*
  experimental. *Strength:* strong. *Applies when:* training on factual
  recall.
- **R3** — Do not add knowledge by fine-tuning. It is absorbed slowly and it
  corrupts what is already there quickly. *Topic:* adaptation. *Status:*
  experimental. *Strength:* moderate. *Applies when:* the goal is new facts
  rather than new behaviour.
- **R4** — Expect hallucination to arrive with knowledge, not as a later
  defect to be trained out. *Topic:* evaluation. *Status:* experimental.
  *Strength:* moderate. *Applies when:* measuring factual reliability during
  training.

## Bearing on the record

- **Should produce a practice** for R1 and a theory for C2. The record holds
  several curriculum practices ([SOTA-129](../practices.d/SOTA-129.md), [SOTA-130](../practices.d/SOTA-130.md), [SOTA-123](../practices.d/SOTA-123.md)) and all of
  them are curricula over *task stages*. This is a curriculum over the
  distribution within a stage, with two measured quantities moving in
  opposite directions as its justification.
- **Gives the record a mechanism for plateaus.** Loss plateaus appear
  throughout its training material as phenomena to schedule around; this is
  the first account of one as a component under construction, with an
  intervention behind it.
- **R3 sits beside [SOTA-199](../practices.d/SOTA-199.md)**, which regularises a narrow fine-tune against
  the base model's own samples. That practice treats drift as containable;
  this says that for knowledge the exchange rate is bad before any
  regulariser is applied.
- **R4 bears on the record's hallucination material** and is uncomfortable
  for any framing of hallucination as a training defect: here it is the
  shadow of the same mechanism that produces the knowledge.

## Limitations

- Synthetic biographies throughout. The tractability is the point, and it is
  also the limit: nothing here is measured on a natural corpus.
- The schedule is tuned and evaluated in the same setting, so C4's margin is
  optimistic.
- The paper's own cited neighbour (Park et al.) reports that low diversity
  shortens plateaus *and* costs out-of-distribution generalisation. The
  schedule is proposed as mitigating the overfitting cost, and the
  out-of-distribution question is not measured here.
- "Fine-tuning corrupts knowledge" is measured on this task with this
  population; the record already holds better-instrumented work on
  fine-tuning drift in general.
- Model scales are small, as the controlled-population design requires.

## Open questions

- Do natural corpora have this plateau? Population size is exactly defined
  here and is not a quantity a real corpus exposes.
- Is the circuit account general to other plateaus, or specific to recall?
  The patching method would transfer; nobody has run it elsewhere.
- What does the schedule cost in out-of-distribution generalisation? The
  neighbouring literature says there is a cost and this setting does not
  measure it.
