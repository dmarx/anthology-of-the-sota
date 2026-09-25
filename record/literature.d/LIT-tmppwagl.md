---
status: Active
title: 'Grokked Transformers are Implicit Reasoners: A Mechanistic Journey to the Edge of Generalization'
version: 1
tags:
- capability-thresholds
- analysis-and-evaluation
- data-pipeline
- model-architecture
date: '2026-09-25'
published: '2024-05-23'
arxiv: '2405.15071'
first_author: 'Wang'
keywords:
- 'grokking'
- 'implicit-reasoning'
- 'systematicity'
- 'circuit-analysis'
- 'parametric-memory'
- 'composition'
- 'comparison'
implementations: []
summary: >-
  Wang, Yue, Su and Sun (2024), [ARXIV-2405.15071](https://arxiv.org/abs/2405.15071). Grokking outside
  algorithmic data, on reasoning over stored facts — and a **named correction**
  to the critical-data-size hypothesis the record holds as
  THEORY-071. With the inferred/atomic ratio `φ` held at 9.0, varying
  the training-set size changes nothing; varying `φ` at fixed size moves
  grokking speed monotonically and at `φ = 18.0` all but removes it. Also
  traces the generalizing circuit for two tasks and explains from its layout
  why composition never generalizes out of distribution while comparison does.
---

# LIT-tmppwagl: Grokked Transformers are Implicit Reasoners: A Mechanistic Journey to the Edge of Generalization

<!-- inactive-ok-file: THEORY-071 THEORY-tmp6pl9b SOTA-tmpvsnuz — Proposed, all three, and that is
     what the citations say: THEORY-071 is the account this paper corrects and whose status the
     correction does not change, and the other two are what this note supplied, filed Proposed
     because the evidence is one synthetic study. -->

Wang, Yue, Su and Sun (2024) — [ARXIV-2405.15071](https://arxiv.org/abs/2405.15071)

## Key takeaways

**Grokking, in a domain nobody had reported it in.** An 8-layer GPT-2 (768
hidden, 12 heads, AdamW, weight decay 0.1) is trained from scratch on a
synthetic knowledge graph: *atomic facts* are `(subject, relation, object)`
edges, *inferred facts* are what two latent rule families deduce from them.
On two-hop composition at `|ℰ| = 2000` and `φ = 7.2`, training accuracy passes
99% on both fact types at **~14K steps, with in-distribution test accuracy no
higher than 9.2% at any point before then**, and only reaches near-perfect
after roughly **50× the steps it took to fit the training set**. To the authors' knowledge this is the first report of
grokking on knowledge-based reasoning rather than algorithmic or linguistic
tasks.

**The controlling variable is the data distribution, not the data size —
stated as a correction.** Two sweeps, deliberately separated:

- Vary the inferred/atomic ratio `φ = |train_inferred| / |atomic|` at fixed
  `|ℰ| = 2000`: grokking speed moves monotonically, and at **`φ = 18.0` the
  model reaches 96.7% before training accuracy has even saturated** — the
  delay is gone.
- Vary `|ℰ|` (and so the training-set size, which scales linearly with it) at
  fixed `φ = 9.0`: **nothing qualitatively changes.** Not the gap between the
  train and test curves, not the systematicity level. Scaling the model does
  not change the picture either; larger models just converge in fewer steps.

The paper names the hypothesis this contradicts — *critical data size*, citing
four papers including [LIT-539](LIT-539.md) — and proposes **critical data
*distribution*** in its place.

**Why the separation matters, and is this record's reading rather than the
paper's.** The measurements the critical-data-size hypothesis rests on vary the
training *fraction* of a fixed universe of examples, which moves size and
composition together and cannot tell them apart. This paper has two knobs and
turns them one at a time. It does not follow that the algorithmic results were
measuring a distribution effect — modular addition has no atomic/inferred
split, so `φ` is not defined there — but it does follow that they could not
have told.

**Out-of-distribution generalization splits by task, and the circuit says
why.** Atomic facts are partitioned into an ID and an OOD set; OOD facts appear
in training only in atomic form, never inside an inferred fact.

- **Composition never generalizes OOD.** Training was extended to **2 million
  optimization steps** with no sign of it.
- **Comparison does**, through grokking, on the same protocol.

Causal tracing (activation patching with same-type token replacement) plus
logit lens over checkpoints gives the two circuits. Composition's is
**sequential**: layers 0–5 retrieve the first hop and park the bridge entity
`b` in `S[5, r₁]` while delaying `r₂` to `S[5, r₂]`; layers 5–8 retrieve the
second hop from those two states. Comparison's is **parallel**: both atomic
facts are retrieved in the lower layers into `S[5, e₁]` and `S[5, e₂]`, and the
upper layers only compare them and fetch a label prepared on a separate stream
at `S[7, a]`.

**The OOD failure is localized, not diffuse.** In the OOD setting `S[5, r₁]`
and `S[5, r₂]` still encode `b` and `r₂` exactly as in the ID case — the first
hop works. What is missing is the second-hop fact in the *upper* layers, which
the model had no reason to store there, because that fact never appeared as a
second hop during training. Comparison escapes this because its circuit keeps
one copy of the facts, in the layers where OOD facts were also stored.

**Two predictions derived from the account and then tested.** Larger weight
decay should accelerate grokking, and does (Appendix E.1). Sharing parameters
across the two halves of the stack — layers 0–3 tied to 4–7, after Universal
Transformer — should let the upper layers reach facts they never stored, and
**unlocks OOD generalization on composition**, though "gained much more slowly
than ID generalization" (Appendix E.2; reported as a figure, with no number in
the text).

**Parametric memory against long context and retrieval.** A variant comparison
task expands the search space with (anti-)symmetry and transitivity: each query
entity touches 50+ facts, each bridge entity in the proof touches 900+, and no
surface cue points at the proof. On a 3-way balanced evaluation (**random =
33.3%**):

| | Accuracy (%) |
| --- | --- |
| GPT-4-Turbo, direct + retrieval | 33.3 |
| GPT-4-Turbo, CoT + retrieval | 31.3 |
| Gemini-1.5-Pro, direct (28.2K facts in context) | 28.7 |
| Gemini-1.5-Pro, CoT | 11.3 |
| Gemini-1.5-Pro, direct + retrieval (5.4K facts) | 37.3 |
| Gemini-1.5-Pro, CoT + retrieval | 12.0 |
| grokked transformer | **99.3** |

**Verbalizing made it worse, and the answers that were right were right for the
wrong reasons.** Only one setting clears chance. Eliciting reasoning cost
Gemini 28.7 → 11.3 without retrieval and 37.3 → 12.0 with it, and the
mechanism is legible: **70.7% of its CoT responses conclude the answer cannot
be decided** (58.7% with retrieval) when it can. The paper also reports that
*most* of the CoT rationales that did reach the correct answer are themselves
wrong — hallucinated facts or logical errors — which it establishes by
inspection, without a count. The elicitation is described only as "prompted to
verbalize the reasoning"; the prompt is not given.

## Standing in the anthology

Ranked into [#342](https://github.com/dmarx/anthology-of-the-sota/issues/342)'s
second tier on a count: 41 files in this record say "grokking" and one practice
stood behind them. The count undersold it — the grokking cluster was already
eight notes and six explanations deep — but the paper turned out to matter for
a different reason, which is that it **contradicts a claim two of those
explanations make**.

What it changes here:

- [THEORY-071](../theory.d/THEORY-071.md) had "a critical dataset size" in its title. This is the
  result that says the crossover is not indexed by size, and the document is
  amended rather than merely cited.
- [THEORY-069](../theory.d/THEORY-069.md) is `Active` and lists **training-set size** as the first of
  three knobs that move grokking. It keeps the status — the regime claim is
  what this paper's fourth domain supports — but the knob is now qualified.
- It supplies the account filed as [THEORY-tmp6pl9b](../theory.d/THEORY-tmp6pl9b.md), and the data-mixture
  recommendation filed as [SOTA-tmpvsnuz](../practices.d/SOTA-tmpvsnuz.md).
- The verbalization result is a measured counter-case for [SOTA-279](../practices.d/SOTA-279.md), whose
  consensus note already said its evidence was one 2022 paper plus everything
  built on it since.

**Two things this does not show.** The 99.3% against 37.3% is not a capability
comparison: the grokked transformer was trained to convergence on the exact
fact set the frontier models were handed once, in context. The paper frames it
as parametric against non-parametric memory and says so plainly, and read that
way it is a clean result about what compression buys; read as "a small
transformer beats GPT-4 at reasoning" it is not one.

And every number here comes from synthetic data with unique tokens per entity.
The authors put this in their limitations and defend it: *"we believe that it is
far more important to build solid understandings, even having distances with
practice, than to draw conclusions or make claims that are closer to practice
but questionable due to insufficient control over data and evaluations."* The
record takes that as the right trade and prices the scope in, which is why the
explanation it supplies is `Proposed` and the practice it supplies is
unreplicated.
