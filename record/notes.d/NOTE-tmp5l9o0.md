---
status: Read
paper: LIT-tmpitbks
title: 'ParScale'
version: 1
date: '2026-09-21'
summary: >-
  Read as a candidate third scaling axis. The scaling law is fitted honestly
  and the inference-cost analysis is better instrumented than most; the claim
  that carries furthest is the *asymmetry* — code benefits more than general
  text, on two independent measurements — and it is the claim the paper
  labels a conjecture.
---

<!-- inactive-ok-file: SOTA-257 — Proposed, and cited in Connections as the
     nearest neighbour whose cost profile is the opposite one. The comparison
     is to its content, not its standing -->

<!-- inactive-ok-file: SOTA-256 — Proposed, and cited for the question it
     poses — judge a monotone recipe by its asymptote — which this reading
     then reports nobody has answered here. Citing an open question as open
     is the correct use of an unsettled document -->

<!-- inactive-ok-file: THEORY-tmprktkw — Proposed, filed in this same
     contribution, and the sentence citing it says it is a conjecture the
     authors labelled as one. Its unsettledness is the content of the
     citation -->

# NOTE-tmp5l9o0: ParScale

## Contribution

Parameter scaling and inference-time scaling were the two known ways to spend
more on a model. This proposes a third that is orthogonal to both: hold the
parameters, run the network `P` times over learnably-transformed copies of the
input, and learn how to combine the results — during **training** as well as
inference.

What is true afterwards that was not before: there is a fitted, two-corpus
scaling law relating parallel computation to parameter count, `P` streams
behaving like `O(log P)` more parameters, and therefore a quantitative answer
to "is capacity parameters or computation?" rather than a rhetorical one.

## Key insight

**Classifier-free guidance works because of the second forward pass, not
because of what is in it.** That is the hinge of the paper and it is a good
observation. CFG's second stream is a *degraded* input — strictly less
information than the first — and the two-pass output still beats the one-pass
output. So the benefit cannot be the information; it must be the computation.

Remove the hand-designed degradation, make the transformations learnable,
make the aggregation learnable, let `P` be a free parameter, and train the
whole thing end to end. The paper's own pivot experiments then confirm the
hinge: the *particular* transformation and aggregation barely matter, and `P`
does.

## Assumptions

- **Trained to convergence** — the theory (Proposition 1) assumes the
  Chinchilla form per stream and ignores data and step limits.
- **The fitted form assumes `ρ` is constant in `P`.** The theoretical result
  says the equivalent parameter multiplier is a function of stream diversity;
  the practical law substitutes `log P` because the observed gains from
  1→2, 2→4 and 4→8 were roughly equal. Diversity is never measured.
- **42B tokens, no repetition**, for the scaling-law fit. The data axis is
  held fixed and explicitly deferred.
- **Same layer count across all models**, varying only width and `P`, which
  is what makes the latency comparison fair.
- Inference cost is **modelled** with the `llm-analysis` framework, not timed
  on hardware.

## Key results

- **`P` streams ≈ `O(log P)` more parameters.** Coefficient **0.39** on
  Stack-V2-Python, **0.33** on the Pile.
- **Larger models gain more.** The loss contours flatten as parameters grow,
  so the return on `P` rises with model size.
- **Downstream, asymmetrically:** 1.6B at `P = 8` matches 4.4B on coding
  (39.1 vs 39.2) and 2.8B on general tasks (55.7 vs 55.2).
- **Inference cost at batch size 1:** 22× less added memory, 6× less added
  latency than the equivalent parameter scaling. Still ahead at batch size 8;
  the advantage narrows as decoding becomes compute-bound.
- **Two-stage training:** 1T tokens plain, then 20B tokens (2%) with streams
  on. At 1.8B, `P = 1 → 8` gives **+2.6%** general, **+4.3%** code, **+7.3%**
  math, and **+10 points on GSM8K** (34% relative). Stage-2 loss spike
  recovers within 0.0002T tokens.
- **Retrofit:** continual pretraining on Qwen-2.5-3B improves loss on corpora
  that 18T tokens of pretraining had probably already covered. With the
  backbone **frozen** and only prefixes and aggregator trained, code
  generation still improves — so `P` can be switched at deployment.
- **Composes with chain of thought:** the GSM8K gain persists with CoT
  applied on top.

## Claims

**Well supported:** that increasing `P` improves loss and downstream
performance, monotonically, across six model sizes, two corpora, and again at
1T tokens. This is a lot of compute spent on one question.

**Well supported and the most useful thing in the paper:** the inference-cost
comparison. Measuring memory and latency instead of FLOPs is the right call
for decode and the authors argue it properly, and the batch-size sweep shows
where the advantage ends rather than quoting the best case alone — though the
headline 22×/6× is the batch-size-1 number.

**Fitted, not derived.** The `log P` form is an empirical choice made after
looking at the curve, substituted into a theoretical result whose actual
content is "the multiplier depends on diversity". The theory does not predict
`log P`; it permits anything from `log` to a power law depending on `ρ`, and
`ρ` is never measured. Calling the result a *law* is doing some work.

**Labelled a conjecture by the authors and likely to be cited as a finding:**
that parameters carry memorization while computation carries reasoning. The
evidence is real and indirect — two corpora with different fitted
coefficients, plus the 4.4B-vs-2.8B downstream asymmetry. It is also a clean
two-way agreement between a fitted constant and a benchmark, which is more
than most conjectures get. Filed as [THEORY-tmprktkw](../theory.d/THEORY-tmprktkw.md), `Proposed`.

**Asserted with an ablation behind it:** that the specific input
transformation does not matter. This is load-bearing — it is what makes the
paper about computation rather than about prefix tuning — and it lives in an
appendix.

## Method

Pre-train Qwen-2.5-architecture models from 0.5B to 4.4B at `P = 1…8` on 42B
tokens of two corpora, fit a scaling law, evaluate downstream. Then a 1T-token
two-stage run at 1.8B, instruction tuning on top, and two retrofit settings on
Qwen-2.5-3B. Model inference memory and latency across batch sizes 1–8.

## Connections

- [SOTA-280](../practices.d/SOTA-280.md) — sample several reasoning paths and take the majority.
  Also parallel, and the differences are the point: untrained, applied only at
  inference, restricted to tasks with an answer to vote on.
- [SOTA-227](../practices.d/SOTA-227.md) — speculative decoding — spends parallel computation to
  save latency at *identical* output. This spends it to change the output.
- [SOTA-257](../practices.d/SOTA-257.md) — ensemble independently seeded models and distil.
  Nearest neighbour in spirit, opposite in memory: that ensemble's members do
  not share weights, which is exactly the cost ParScale avoids.
- [SOTA-150](../practices.d/SOTA-150.md) — mixture-of-experts — is the complementary trade, and the
  paper says so: MoE is parameter-heavy and latency-friendly, this is
  computation-heavy and memory-friendly. Nobody has combined them.
- [SOTA-184](../practices.d/SOTA-184.md) — LoRA — is the technique the frozen-backbone variant most
  resembles operationally, and the object being adapted is different: here
  the adapter buys *capacity*, not task specialization.

## Bearing on the record

Two practices and a theory. The practices split along a real decision
boundary: whether to use parallel scaling at all (which turns on the
inference profile, and the paper measures it) and how to pay for it (the
two-stage schedule, which is what makes the first affordable).

It also puts a number on something the record has only had qualitatively.
[SOTA-256](../practices.d/SOTA-256.md) says to judge a monotone scaling recipe by its asymptote;
this is a monotone scaling recipe whose asymptote in `P` is not established
— the fit is logarithmic and stops at `P = 8`, and the authors name "is
there a performance upper bound for `P`" as open.

## Limitations

**One group, one architecture family, one tokenizer.** Everything is Qwen-2.5
dense architecture. The paper claims applicability to "any model structure"
and tests one.

**`P = 8` is where the evidence stops**, and a logarithmic fit is exactly the
shape that flatters an extrapolation nobody ran.

**Inference cost is modelled, not measured.** `llm-analysis` is a reasonable
instrument and it is not a stopwatch, and the batch-size-1 headline is the
most favourable point on the curve.

**Training cost is the honest objection** and the two-stage strategy is a
mitigation, not an answer: `P`× FLOPs during the ParScale phase is real, the
1T/20B split point is unjustified beyond "it worked", and the paper says so.

**The scaling law holds the data axis fixed.** Data-constrained parallel
scaling is deferred, with a footnote reporting that `P` seemed to *reduce*
overfitting on repeated data — an interesting aside with no experiment
attached.

## Open questions

- Does the logarithmic form survive past `P = 8`, and is there a ceiling?
  The authors ask this themselves.
- Is diversity `ρ` measurable? If it is, the theoretical law becomes
  predictive instead of descriptive, and the `log P` assumption becomes
  testable rather than fitted.
- Does the memorization/reasoning split hold on a corpus that is neither code
  nor general web text?
- What happens with a mixture-of-experts backbone? The paper names it as the
  complementary trade and leaves it.
