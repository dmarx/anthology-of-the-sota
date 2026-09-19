---
status: Read
paper: LIT-218
title: 'Video models are zero-shot learners and reasoners'
version: 1
date: '2026-09-19'
summary: >-
  The argument by analogy: LLMs became generalist from three primitives —
  large, generative, web-scale — and video models now have all three. The
  evidence is a catalogue of tasks Veo 3 was never trained for and can do
  anyway, from segmentation and edge detection through affordances and tool
  use to maze and symmetry solving. It is a position paper with
  demonstrations, and the demonstrations are of one proprietary model.
---

# NOTE-tmpygxgb: Video models are zero-shot learners and reasoners

## Contribution

A claim about trajectory, supported by breadth rather than depth. The authors
argue that generative video models are where LLMs were before the generalist
turn, and demonstrate that Veo 3 solves a wide range of vision tasks with no
task-specific training: segmenting objects, detecting edges, editing images,
understanding physical properties, recognising affordances, simulating tool
use — and then early visual *reasoning*, maze solving and symmetry.

## Key insight

The primitives are the argument. Large + generative + web-scale produced
general-purpose language understanding; the same three now describe video
models; therefore expect the same outcome. Everything else in the paper is
existence proof that the capabilities are already appearing.

## Concepts

- **Zero-shot capability** here means prompting a video model to produce a
  video whose *content* solves the task — the output is a video, not a label
- **Chain-of-frames**, the visual analogue the framing implies: reasoning laid
  out across frames the way chain-of-thought is laid out across tokens

## Assumptions

- **The LLM analogy holds.** This is the load-bearing assumption and it is an
  analogy, not a result
- **Veo 3 is representative of generative video models**, rather than of
  Google's data and scale
- **Task success is readable from generated video.** Evaluation runs through
  what the video shows, which is softer than a benchmark number
- **Emergence continues with scale**, which the paper projects rather than
  measures

## Key results

- **A broad catalogue of tasks solved without task-specific training**,
  spanning perception (segmentation, edges), physical understanding
  (properties, affordances), manipulation of the image, and early reasoning
  (mazes, symmetry). *Holds when:* Veo 3, prompted; qualitative and
  quantitative results on the project page.
- **The reasoning tasks are the novel part.** Segmentation-by-video is
  striking; maze solving is the claim that something beyond perception is
  happening.

## Limitations

- **One model, and it is closed.** No recipe, no weights, no ablation of what
  in the training produced any of it. Nothing here is reproducible or
  attributable to a technique
- **Zero-shot capability is not efficiency.** A specialist segmentation model
  is orders of magnitude cheaper than generating video
- **The analogy is doing the work.** LLM generality emerged alongside
  instruction tuning and RLHF, neither of which has an obvious video analogue
  and neither of which this paper addresses
- **No comparison against the joint-embedding line**, which is the live rival
  and which the record now holds (`LIT-216`, `LIT-215`)

## Connections

The opposing bet to `LIT-216` and `LIT-215`, and the reason all three were
filed as a cluster. Both lines aim at general visual understanding from
unlabelled video; one predicts representations and explicitly refuses to
generate, the other generates and gets representations as a side effect.
`LIT-216`'s own Figure 2 taxonomy names the distinction — generative versus
joint-embedding-predictive — years before this paper made the generative side
of it look like a winning bet.

## Bearing on the record

**No practice, and this one is not close.** `DP-006` asks whether the work
contains an instruction. The nearest candidate — "use a generative video
model zero-shot instead of a task-specific model" — rests on one proprietary
system with no recipe, and `DP-005` puts that in the adoption column rather
than the evidence column.

What it is here for is that the record now holds **both** answers to the same
question, and can say that the field has two live bets rather than one. A
corpus holding only the joint-embedding line would read as though the
question were settled.
