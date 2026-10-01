---
status: Proposed
promote_when: >-
  An arm that separates the two readings on a pretrained decoder, with no
  training under a separator mask: keep the separators' keys and drop or zero
  their values. If separators are only where idle attention lands, keeping
  the keys preserves the softmax denominator and the score should stay near
  SepLLM's; if they carry the segment, it should fall toward StreamingLLM's.
  A probe that reads segment content back out of separator hidden states,
  against a matched probe on non-separator tokens, or a measurement of value
  norms at separators in a decoder (LIT-414 measured them small in BERT),
  would also settle it. What would NOT meet it: another KV-eviction method
  that keeps separators and scores well, which both readings predict; or
  results from a model trained under the separator mask, where the
  condensation is forced by construction.
title: 'A separator token condenses the content of the segment it closes, rather than only receiving attention a head has nowhere else to put'
version: 1
tags:
- attention-techniques
- inference-optimization
date: '2026-10-01'
source:
- LIT-tmp8tr17
explains: []
contested_by:
- LIT-414
summary: >-
  Chen et al. (2024), [LIT-tmp8tr17](../literature.d/LIT-tmp8tr17.md) — SepLLM. Attention in Llama-3-8B-Instruct
  concentrates on punctuation and whitespace, and the paper reads that as each
  segment's content being condensed into its closing separator. Its
  evidence is what masking costs: keeping only separators, a window and
  three initial tokens holds GSM8K-CoT at 77.18 against 77.79 with 47% of the
  KV, where StreamingLLM at the same budget gets 70.89 and keeping every
  fourth token instead gets 72.71. The record already holds the opposite
  reading — [LIT-414](../literature.d/LIT-414.md) found heads parking no-op attention on `[SEP]`, periods
  and commas, whose values are small, and [THEORY-019](THEORY-019.md) is the sink account it
  belongs to. No experiment in either paper separates the two.
---

# THEORY-tmp7q4tl: A separator token condenses the content of the segment it closes, rather than only receiving attention a head has nowhere else to put

## Source

Chen et al. (2024), [LIT-tmp8tr17](../literature.d/LIT-tmp8tr17.md) — SepLLM, §3, Table 1, Tables 2–3,
Appendix F (needle in a haystack), Appendix H and Appendix I (FixLLM,
Table 17).

## The two readings

Attention in trained transformers lands disproportionately on punctuation.
The record holds two accounts of why, and they predict different things
about what a separator's key-value pair *contains*.

**The summary reading (this document).** [LIT-tmp8tr17](../literature.d/LIT-tmp8tr17.md) sees separators such as
`,` and `.` receiving more attention than nouns and verbs in
Llama-3-8B-Instruct and hypothesizes that "information of the segments
between these separator tokens can be effectively condensed into the
separator tokens". Its argument for why: separators are the most frequent
context in pretraining, so they attend broadly and are attended to broadly,
and "generating a separator serves as a summarization of the current
segment". On this reading a separator's value vector carries what came
before it, and evicting it loses content.

**The no-op reading (already held).** [LIT-414](../literature.d/LIT-414.md) found, in BERT, that heads with
nothing to do assign "almost all of its probability mass to `[SEP]` tokens,
and other less informative tokens like dots/commas, while these tokens also
have small values" — so the product is near zero and the head performs a
no-op. That is [THEORY-019](THEORY-019.md)'s account of the attention sink — softmax mass
must land somewhere — with the landing site chosen for low information
rather than for position. On this reading the separator's value carries
little, and evicting it hurts because it removes mass from the softmax
denominator, exactly as evicting the initial tokens does in StreamingLLM
(perplexity 5.40 to 5158 in [THEORY-019](THEORY-019.md)).

The two are not exclusive — [LIT-414](../literature.d/LIT-414.md) itself shows heads putting only part of
their mass on delimiters as a soft gate, and a separator could be a sink for
some heads and a summary for others. But they disagree about what a
separator is *for*, and this document is the claim that the summary function
is real.

## What the source shows, and what each result can distinguish

**Training-free masking** (Table 1, Llama-3-8B-Instruct). Each query sees
three initial tokens, every earlier separator, and the 256 nearest tokens:
GSM8K-CoT **77.18** against 77.79 for full attention, with 47.36% of the KV;
MMLU 64.68 against 65.72 with 44.61%. StreamingLLM, with the window widened to
380 to match the budget, gets **70.89** on GSM8K-CoT. The separators are worth
six points at a matched budget. Both readings predict that: if heads park
mass on separators, evicting them perturbs the denominator whether or not
they carry anything.

**Separators against arbitrary tokens** (Table 17). FixLLM keeps one token
every Δ positions instead of the separators. At Δ = 4, with 49.08% of the KV —
slightly *more* than SepLLM — GSM8K-CoT is **72.71** against 77.18, and MMLU
62.91 against 64.68. This is the paper's best evidence: it is not the
sparsity pattern but *which* tokens. It still does not separate the readings,
because the no-op reading also says the specific tokens matter — heads learned
to park on punctuation, not on every fourth token.

**Needle in a haystack** (Appendix F). SepLLM retrieves needles StreamingLLM
cannot, which the paper reads as the needle's content surviving in nearby
separators after its own KV is discarded. That would discriminate — a sink
carries no needle — but every configuration shown keeps full attention in
some layers (the first and last at 160M, the first two and last two at 8B),
and in those layers the needle's KV is not discarded. The result is
confounded by the hybrid.

**Training from scratch** (Pythia-160M, 300B tokens, Tables 2–3). Under the
separator mask the model reaches lower loss than full attention at equal
FLOPs, and roughly on par at equal steps (LAMBADA perplexity 30.16 against
34.83 at n = 128, ARC-c 19.97 against 20.14). This shows that a model *can*
be trained to route segment content through separators. It is not evidence
that a model trained without the mask does so, because the mask forces it:
the paper says as much, that under training "the information within
segments is forced to be condensed into the separators". It is at 160M only.

## What this does not say

- **It does not say separators carry no sink function.** Nothing here
  measures that, and [THEORY-019](THEORY-019.md) is unaffected: its evidence is about the
  initial tokens, which SepLLM keeps.
- **It is not measured on a representation.** There is no probe, no value-norm
  measurement, no ablation that keeps the keys and removes the values. Every
  result is the cost of masking, which both readings explain.
- **[LIT-414](../literature.d/LIT-414.md)'s evidence is from a different model family.** Bidirectional
  BERT with an explicit `[SEP]`, OPT-125M and ViT; SepLLM's is causal
  decoders. A separator in a causal model sees only the segment before it,
  which is the condition the summary reading needs and an encoder does not
  provide — so the two papers may each be right about their own models.
