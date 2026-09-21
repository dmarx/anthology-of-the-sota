---
number: 255
status: Read
formerly:
- NOTE-tmp13fue
paper: LIT-510
title: 'Gemini 1.0: complete disclosure, and an abstract that picks the flattering row'
version: 1
date: '2026-09-21'
summary: >-
  Read from the [#180](https://github.com/dmarx/anthology-of-the-sota/issues/180) worklist for the model and filed for the appendices. The
  headline — first model to exceed human-expert MMLU — holds under one
  inference procedure out of three the report itself publishes, and under the
  other two GPT-4 is ahead. Nothing is concealed. The disambiguating numbers
  are in the same document, which is what makes this the corpus's cleanest
  instance of `DP-010`.
---

<!-- inactive-ok-file: SOTA-309 — Proposed, and named only as one item in
     the tally of five measurement-sensitivity practices this document
     declines to join. Citing a practice in order to say the count does NOT
     extend to it is not citing it as settled. -->

# NOTE-255: Gemini 1.0: complete disclosure, and an abstract that picks the flattering row

## Contribution

A frontier model report. For this record its value is in three evaluation
measurements, all in appendices, all volunteered.

## Key results

**MMLU: the ordering depends on the inference procedure, and the report shows
it.** Uncertainty-routed chain-of-thought draws `k` samples, takes the
majority if consensus clears a threshold, and otherwise falls back to the
greedy no-CoT answer. The threshold is **optimized per model on that model's
validation split**. Appendix 10.2 gives the sweep:

| procedure | Gemini Ultra | GPT-4 | ahead |
|---|---|---|---|
| greedy sample | 84.0% | 84.2% | GPT-4, by 0.2 |
| chain-of-thought @32 only | 85.0% | 87.3% | GPT-4, by 2.3 |
| **uncertainty-routed CoT@32** | **90.0%** | 87.3% | **Gemini, by 2.7** |

Table 2 reports the same shape in the main text: Gemini Ultra **90.04%
CoT@32** and **83.7% 5-shot**, against GPT-4's **87.29% CoT@32 (via API)** and
**86.4% 5-shot (reported)**.

Human-expert performance is 89.8%. So "the first model to exceed human-expert
performance on MMLU" is true under exactly one of the procedures the report
ran, and under the 5-shot protocol that every other model in the table is
scored on, Gemini Ultra is at 83.7% — six points below the threshold and
below GPT-4.

**The mechanism is that the procedure is differentially beneficial**, which
is the part worth keeping. GPT-4 gains 3.1 points from greedy to routed and
gets *all* of it from plain CoT@32 — routing adds nothing on top. Gemini Ultra
gains 6.0, and almost none of it from plain CoT (85.0), so nearly the whole
gain comes from the routing rule itself. Applying the same procedure to both
models is therefore **not sufficient** for a fair comparison: the procedure
interacts with the model, and which one you choose decides who wins.

To the report's credit, it ran the procedure on GPT-4 too, via API, rather
than quoting GPT-4's published number and its own best.

**Contamination, measured.** An extensive post-training leak analysis led them
to drop LAMBADA entirely. On HellaSwag they found that **an additional hundred
fine-tuning steps** on website extracts corresponding to the HellaSwag
*training* set — extracts not in the pretraining data — take validation
accuracy to **89.6% for Pro and 96.0% for Ultra** at 1-shot, against GPT-4's
measured 92.3% 1-shot. They report decontaminated 10-shot results only, and
conclude "there is a need for more robust and nuanced standardized evaluation
benchmarks with no leaked data."

A hundred steps is nothing. That number is the most useful thing in the
report: it prices benchmark inflation, from the inside, in units anyone can
compare against their own training budget.

**A held-out control they did not have to run.** On FLEURS the model
"significantly outperforms" USM and Whisper — and the report immediately says
the gain is large *because the model was trained on the FLEURS training set*,
then reports that retraining without it gives WER **15.8**, still better than
Whisper. That is the ablation the record's [SOTA-311](../practices.d/SOTA-311.md) asks for in a
different setting, done voluntarily and reported against interest.

**Natural2Code** was built from non-web sources specifically to avoid leakage;
Ultra scores 74.9% on it against 74.4% on HumanEval.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | An inference-time decision procedure can be worth more to one model than another and flip a comparison | **strong** | Appendix 10.2's three-procedure sweep, both models, same harness |
| C2 | A benchmark can be inflated past a competitor by a hundred fine-tuning steps on adjacent web text | strong | the HellaSwag measurement, reported against interest |
| C3 | Gemini Ultra is the first model to exceed human-expert MMLU | **conditional** | true at CoT@32 with per-model-tuned routing; false at 5-shot, where it scores 83.7% |
| C4 | Ultra advances the state of the art in 30 of 32 benchmarks | unassessable here | this reading checked MMLU, HellaSwag and FLEURS, not the other 29 |

## Limitations

**Nothing about the models is isolated.** No architecture ablation, no data
mixture, no scaling detail, no training compute. The report is not trying to
be that document and nothing in this record should cite it as one.

**The comparisons are one run each.** No seeds, no intervals, anywhere. After
[SOTA-307](../practices.d/SOTA-307.md), a 2.7-point single-run margin on one benchmark is worth
exactly as much as that practice says it is.

**GPT-4's numbers come from two sources.** Its 5-shot 86.4% is "reported" —
quoted from OpenAI — while its CoT@32 87.29% was measured by Google via API.
Mixing a quoted number and a measured one inside a single row is the thing
this note's own practice is about, in miniature, and the report labels both,
which is the right handling.

**The abstract does not carry any of this.** "Advances the state of the art in
30 of 32" and "first model to achieve human-expert performance" are both
defensible readings of tables that also contain the rows that qualify them.

## Bearing on the record

**One new practice and one strengthened.** [SOTA-313](../practices.d/SOTA-313.md) takes C1:
the inference procedure is part of what is being compared, and reporting the
sweep rather than the best row is what makes a comparison a comparison.
[SOTA-197](../practices.d/SOTA-197.md) — account for test-set proximity and state your exposure —
gains this as a third source and, more usefully, its first *number*: its
`consensus_note` says "what almost nobody does is state their exposure", and
here is a frontier lab doing it and pricing it.

**Sixth instance of the session's running shape, and the one that breaks it.**
The others — [SOTA-305](../practices.d/SOTA-305.md), [SOTA-307](../practices.d/SOTA-307.md), [SOTA-308](../practices.d/SOTA-308.md),
[SOTA-309](../practices.d/SOTA-309.md), [SOTA-312](../practices.d/SOTA-312.md) — are all "a reported number is sensitive to a
choice the report does not state". Here the report states everything: both
protocols in the main table, the full sweep in the appendix, the contamination
price, the FLEURS control. Disclosure was complete and the headline was still
the flattering row. So the remedy cannot be "disclose more", and the count
does not extend — this is [DP-010](../../docs/design-principles.md#dp-10) rather than the others' shape.
Counted, not generalized: [DP-009](../../docs/design-principles.md#dp-9).

## Open questions

- **Does the routing rule generalize or was it fitted?** The threshold is
  tuned per model on the validation split, and no held-out confirmation of the
  threshold's value is reported. Whether 90.0% survives a threshold chosen
  before seeing MMLU validation is unknown and cheap to check.
- **How much of the 30-of-32 rests on procedure choice?** This reading checked
  one benchmark's sweep. The report gives protocol labels throughout, so the
  audit is possible from the published tables alone.
- **What is the price curve on contamination?** A hundred steps was enough.
  Ten? One? The report gives a single point on a curve that would be worth
  having.
