---
status: Read
paper: LIT-tmpqux2k
title: 'Heads traded for depth, and the five rows where only those two things move'
version: 1
date: '2026-09-22'
summary: >-
  Read on its merits after being triaged past. The headline is an
  architecture recommendation and the interesting part is the mechanism: more
  heads lower the condition number of the attention block, which is the same
  quantity [THEORY-041](../theory.d/THEORY-041.md) says drifts the wrong way when nothing manages it. Half
  the configurations confound the trade by also halving the MLP; the other
  half do not, and those are the result.
---
<!-- inactive-ok-file: SOTA-190 THEORY-041 — both Proposed, and this
     reading's Bearing section is about what each of them does and does not
     settle. Naming them is the subject, not a reliance. -->

# NOTE-tmph5061: Heads traded for depth, and the five rows where only those two things move

## Contribution

Prove that increasing the number of attention heads lowers the condition
number of the attention block, hypothesize that this is part of what depth was
buying, and test the hypothesis by rebuilding twelve published architectures
with more heads and fewer layers.

## Key results

**Theorem 3.2** bounds the condition number `κ(A) = σ₁(A)/σ_k(A)` of the
attention block and shows it improves with head count. The argument runs
through concentration on the sub-blocks; the conclusion is that heads are
doing optimization work, not only representational work.

**The confound, stated first because it decides how to read the tables.** Six
of twelve configurations also change the MLP width — ViT-B and DeiT-B go
3072 → 1536, ViT-L and DeiT-L 4096 → 2048, and both VOLO rows shrink every
MLP dimension. Their parameter savings are not evidence for the trade in the
title.

**The five rows that hold the MLP fixed:**

| model | depth, heads | MLP | Top-1 | params |
|---|---|---|---|---|
| XCiT-M | 24, 8 → **12, 16** | 2048 | 81.4 → **81.7** | 84.4M → 59.0M (−30%) |
| TNT-B | 12, 10 → **8, 16** | 2560 | 82.3 → **82.3** | 65.4M → **30.9M (−53%)** |
| DaViT-B | [1,1,9,1] → **[1,1,5,1]** | unchanged | 83.3 → **83.5** | 88.0M → 62.0M (−30%) |
| XCiT-L | 24, 16 → **12, 24** | 3072 | 82.1 → **82.4** | 189.1M → 103.8M (−45%) |
| DaViT-L | [1,1,9,1] → **[1,1,5,1]** | unchanged | 83.6 → **83.6** | 196.8M → 140.0M (−29%) |

Five for five hold or improve, at 29–53% fewer parameters and correspondingly
less training memory.

**Language.** Crammed BERT on the Pile: 16 layers / 12 heads, 119M, GLUE
average 78.6 → 10 layers / 24 heads, **84M**, GLUE average 78.6, with the
per-task columns essentially unchanged. GPT-2 on TinyStories: 12 layers / 12
heads (89M) → 16 heads and **4 layers**, better validation loss.

**Long-Range Arena** with Nyströmformers, where the models are tiny (160k–470k
parameters): ListOps rises from 36.4% to 37.4% as heads go 2 → 8, and 1-layer
models with ≥4 heads beat the original 2-layer model with fewer parameters.

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | More heads lower the attention block's condition number | strong | proved, and measured empirically on ViTs |
| C2 | Heads can be traded for depth at equal accuracy | strong for vision, moderate elsewhere | five clean configurations plus five confounded ones; GLUE matched exactly |
| C3 | The trade follows from the conditioning improvement | **hypothesis only** | the paper says it lacks a full theoretical explanation |
| C4 | Transformers are over-sized | rhetorical framing | this is the interpretation, not a measured claim |

## Limitations

**C3 is the paper's own admission and it matters.** The theorem establishes
conditioning improves with heads. It does not establish that conditioning is
what the removed layers were providing, so the trade could hold for an
unrelated reason.

**More heads at fixed width means smaller heads.** Every configuration keeps
`d_model` and raises head count, so head dimension falls — XCiT-L goes to 24
heads of `3072/24`. At some point that must break, and no row finds the edge.

**Throughput is not reported.** Parameters and training memory fall; the paper
does not report wall-clock or inference latency, and fewer-but-wider layers
parallelize differently from more-but-narrower ones. That omission is exactly
the axis [SOTA-190](../practices.d/SOTA-190.md)'s source says is its own limit.

**300 epochs, ImageNet-1k, one seed per configuration.**

**The LRA models are 160k–470k parameters** and the effects are fractions of a
percent. They corroborate direction and nothing more.

## Bearing on the record

**It pulls against [SOTA-190](../practices.d/SOTA-190.md), and the pull should be recorded rather
than resolved.** That practice — increase depth before any other dimension —
comes from T5 configurations where the stated limit is model parallelism. This
removes depth and buys it back with heads. The axes differ (depth-vs-width
against depth-vs-heads), neither paper cites the other, and nobody has run the
comparison, so no relation is declared. [ADR-011](../decisions.d/ADR-011.md).

**It is the record's second source on conditioning as a design variable.**
[THEORY-041](../theory.d/THEORY-041.md) says unconstrained matrices drift badly conditioned and
that this correlates with slower training, and is `Proposed` because nothing
intervenes on conditioning alone. This intervenes on conditioning — by head
count — and reports the result. It is not the intervention [THEORY-041](../theory.d/THEORY-041.md)'s
`promote_when` asks for, which wants conditioning separated from norm
constraint, but it is the nearest thing in the record and the two should be
read together.

**It sits oddly beside [SOTA-109](../practices.d/SOTA-109.md).** GQA reduces the number of
distinct key-value heads for memory-bandwidth reasons. This raises head count
for conditioning reasons. They are not in contradiction — GQA shares K/V while
keeping query heads separate — but a reader optimizing both at once has no
guidance here and neither paper considers the other.

## Open questions

- **Where does the trade break?** Every row raises heads and lowers depth and
  nothing reports the configuration where accuracy finally falls.
- **Does it survive at language-model pretraining scale?** The largest
  language result is Crammed BERT at 119M.
- **Throughput.** Fewer, wider layers may be faster or slower; the paper's
  case is parameters and memory, and the deployment case needs latency.
