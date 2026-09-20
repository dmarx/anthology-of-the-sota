---
number: 190
status: Read
formerly:
- NOTE-tmpbxl0o
paper: LIT-440
title: 'How much do language models memorize?'
version: 1
date: '2026-09-19'
summary: >-
  Defines memorization as compression rate against the model, separates it
  from generalization by training on uniform random bitstrings, and measures
  GPT-style transformer capacity at ~3.6 bits per parameter, linear in
  parameter count and nearly indifferent to precision. Double descent begins
  exactly where the data's information content crosses that capacity.
---

# NOTE-190: How much do language models memorize?
<!-- inactive-ok-file: SOTA-124 — Proposed, and the practice this reading half-settles; saying which half is the point -->
<!-- inactive-ok-file: SOTA-173 — Proposed, and named as one of the two positions this reading supplies a quantity for -->

## Contribution

Supplies a definition of memorization that is measurable on a single trained
model, at the level of a single datapoint, and that does not depend on
getting the model to emit anything. With it, the paper puts a number on
transformer storage capacity — ~3.6 bits per parameter — and shows the number
is stable across widths, depths, sequence lengths, vocabulary sizes and, most
surprisingly, precision. It then locates the onset of double descent at the
point where the dataset's information content exceeds that capacity, which is
the first account of double descent with both quantities measured rather
than proxied by parameter and sample counts.

## Key insight

**A model has a fixed budget of bits, and generalization is what it does when
the budget runs out.** Below capacity it is cheaper to store datapoints
separately, so it does; past capacity it cannot, so it is forced to find
structure that lets several datapoints share representation — and structure
that several datapoints share is exactly what generalization is. Double
descent is then not a curiosity of over-parameterization but the visible
moment of that switch. The corollary that matters for practice: the question
"is this model memorizing my data" has a units answer, and the units are bits
against parameters, not tokens against samples.

## Assumptions

- **Capacity is measured by gradient descent**, so every number is a *lower
  bound* on what the architecture could hold. The authors are explicit.
- **The synthetic setting assumes generalization is impossible.** Uniform
  i.i.d. bitstrings have exactly computable Shannon information and no
  structure, which is what makes total memorization equal to capacity. Any
  residual structure would inflate the estimate.
- **The text setting requires an oracle reference model** trained on the full
  data distribution, against which "generalization" is defined. The estimate
  of unintended memorization is relative to that oracle's quality.
- Compression rate under the model is used as a practical stand-in for
  Kolmogorov complexity; the paper is clear this is an approximation with
  Shannon-information machinery, not the real quantity.
- **GPT-family decoder-only transformers**, ~500K to 1.5B parameters,
  bfloat16 unless stated. Hundreds of models.

## Key results

- **Capacity ≈ 3.6 bits per parameter.** Measurements across widths and
  depths span 3.61–3.68; the average estimate in bfloat16 is 3.51 and in
  float32 is 3.83. *Holds when:* trained to saturation on synthetic uniform
  data, capacity read as the maximum memorization over all dataset sizes.
- **Precision buys almost nothing.** Doubling the bits per weight moves
  capacity by ~9%, not ~100% — so most of the extra representational range is
  not used for storage.
- **Capacity is linear in parameter count**, smoothly, across the full range
  tested. Consistent with prior fact-storage results; somewhat above
  Allen-Zhu and Li's ~2 bits/parameter quantization estimate.
- **Memorization plateaus at capacity** regardless of how much more data is
  supplied; past that point per-sample memorization *decreases* as the model
  substitutes shared structure.
- **Double descent begins where dataset information exceeds model capacity**,
  shown on both synthetic bitstrings and real text with both quantities
  computed rather than estimated by counting.
- **Membership inference follows a sigmoid in the dataset-to-capacity
  ratio**, extrapolating to the prediction that modern models are trained on
  far too much data for reliable membership inference on an average point.
- **The most-memorized text is the text with the rarest words** (measured
  against TF-IDF), in a model trained past capacity.
- Capacity predictions hold across sequence length and vocabulary size with
  ~1.8% average error.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | GPT-style transformers store ~3.6 bits of information per parameter | strong | direct measurement on synthetic uniform data across many model shapes, §3 |
| C2 | Capacity scales linearly with parameter count | strong | smooth fit across three orders of magnitude, §3.2 |
| C3 | Capacity is nearly independent of weight precision | moderate | one bfloat16-vs-float32 comparison, consistent across model sizes |
| C4 | Double descent begins exactly when data information exceeds model capacity | moderate | co-located onset on synthetic and text data, §4; a mechanism is proposed but not isolated |
| C5 | Membership inference becomes unreliable as dataset size grows past capacity | moderate | fitted scaling law validated on larger models, §5 |
| C6 | Extraction and membership inference are neither necessary nor sufficient as definitions of memorization | strong | argued, with counterexamples from the literature, §1–2 |

## Method

Define per-sample unintended memorization as the reduction in the codelength
of a datapoint when the model is available, minus what a reference model
capturing the true data distribution would already provide. Sum over the
dataset to get total unintended memorization.

To measure capacity, remove the reference-model term by removing the
possibility of generalization: build datasets of uniformly sampled tokens
whose total entropy is `N · L · log2(V)` exactly, train to saturation at many
dataset sizes, and take the maximum total memorization over all of them.

Repeat on real text with an oracle model trained on the full distribution
standing in for the true distribution, which permits the memorization and
generalization components to be tracked separately as dataset size grows.

## Concepts

- **Unintended memorization** — the information a model contains about a
  specific dataset, over and above what a model of the true data-generating
  process would contain.
- **Generalization (intended memorization)** — the information a model
  contains about the data-generating process itself. Deliberately named as a
  component of memorization rather than its opposite.
- **Capacity `L(θ)`** — the maximum total unintended memorization a learning
  algorithm and architecture can reach, taken over dataset sizes. An
  empirical quantity with a training procedure inside it, not an
  architectural constant.
- **Dataset-to-capacity ratio** — the information content of the training set
  divided by the model's capacity. The axis along which double descent and
  membership inference both organize.

## Connections

Sits downstream of the fact-storage literature (Roberts et al.,
Allen-Zhu and Li) which found storage linear in parameters for *facts*; this
generalizes the finding to arbitrary information and gives a tighter number
by removing the need to define a fact. Against the extraction and
membership-inference traditions it is a critique: both are argued to measure
something other than what they are used to claim.

The double-descent result connects to Belkin et al. and Nakkiran et al.,
whose accounts are in terms of parameter and sample counts. Replacing those
with measured information content is what makes the onset predictable rather
than observed.

## Recommendations

- **R1** — When asking whether a model has memorized a dataset, compare the
  dataset's information content to the model's capacity in bits rather than
  comparing sample count to parameter count. *Topic:* measurement. *Status:*
  experimental. *Strength:* moderate. *Applies when:* a reference model for
  the distribution is available, or the data is synthetic.
- **R2** — Do not treat successful extraction as evidence of memorization, or
  failed extraction as evidence of its absence. *Topic:* evaluation.
  *Status:* standard. *Strength:* strong. *Applies when:* always.
- **R3** — Budget roughly 3.6 bits per parameter when reasoning about what a
  model can hold. *Topic:* capacity. *Status:* experimental. *Strength:*
  moderate. *Applies when:* GPT-style decoder-only transformers; the number
  is a gradient-descent lower bound.

## Bearing on the record

- **Half-settles [SOTA-124](../practices.d/SOTA-124.md)'s conjecture.** That practice rests on a
  memorization window "scaling linearly" in parameters, from one figure, and
  its `promote_when:` asks for a second measurement. The linear scaling is
  measured here across three orders of magnitude. The *window* — a token
  count — is not, and converting between the two is the step nobody has
  taken. [SOTA-124](../practices.d/SOTA-124.md) should record the partial check without being promoted on
  it.
- **Supplies the missing quantity in the [SOTA-171](../practices.d/SOTA-171.md) / [SOTA-173](../practices.d/SOTA-173.md)
  disagreement.** Those two disagree about whether repeated data overfits.
  This predicts where the turn should happen — at the capacity crossing —
  which is a testable bridge nobody has run in the multi-epoch setting.
- **Should produce a theory document**, not a practice. The capacity number
  and the double-descent account are claims about what is true, and the
  instructions they carry (R1, R2) are about how to measure rather than what
  to train.

## Limitations

- Every capacity figure is a gradient-descent lower bound; nothing here
  characterizes what the architecture could store under a better optimizer.
- The largest model is 1.5B, and capacity is the quantity most likely to
  behave differently once mixture-of-experts, tied embeddings or heavy
  quantization enter — none of which is tested.
- The text-side measurements inherit the oracle model's errors, and the
  oracle is itself a trained model of finite capacity.
- Double descent is *located* at the capacity crossing; the sharing mechanism
  offered for why is called a theory by the authors and is not isolated.
- All of this is uniform-random or English text under one tokenizer.

## Open questions

- What is the capacity of an MoE model per *active* parameter, and per total
  parameter? The linear law is the kind of thing sparsity should break.
- Does the capacity crossing predict the onset of overfitting under *repeated*
  data, as it does under increasing unique data? That is the experiment that
  would turn this into a settlement of the repetition dispute.
- Why is capacity nearly precision-independent? If the extra bits are not
  storage, the question of what they are for is wide open, and it bears
  directly on how far quantization can go.
