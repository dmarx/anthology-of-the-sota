# Theory

Why the things in the [practice registry](../practices/README.md) work — one
document per claim, each citing the paper it came from.

A theory is a **finding**, where a practice is an instruction. "Use batch
normalization" is a practice; "batch normalization helps by smoothing the
optimization landscape" is a theory, and the two are held apart because they
can be true and false independently. That is not a hypothetical: batch
normalization's practices are `Active`, the paper that introduced it is worth
reading, and the explanation in that paper's own title is `Rejected` here.
Three facts, three statuses, three documents.

`Active` means this is the best account the record holds. `Rejected` means
the account is disbelieved — **and the thing it explained may still work
perfectly well**, which is the word's whole reason for meaning something
different here than it does on a practice. Nothing is deleted: an explanation
that stops being believed keeps its body, because how a plausible mechanism
survived a decade of correct predictions is the interesting part.

Every theory names a `source:`, on the same rule as a practice — an
explanation with no paper behind it is a hunch. Where one underwrites a
recommendation it says so with `explains:`, and the practice reads it back as
`explained_by:`. That field is optional, because a finding that underwrites
nothing yet is still a finding.

File one with `luria new theory`. Never hand-write a link target: write the
bare code and run `luria link --fix`.

<!-- GENERATED below this line by `luria index` — edit README.stub instead. -->

## By topic

**[Training optimization](tags/training-optimization.md)** (0) — optimizers, learning-rate schedules, batch size, training dynamics, scaling laws and scaling strategies.

**[Systems optimization](tags/systems-optimization.md)** (0) — hardware utilization, kernels, compilation, memory access patterns, numerical precision.

**[Model stability](tags/model-stability.md)** (4) — initialization, normalization, gradient handling, regularization, loss-landscape behaviour:
[001](../../record/theory.d/THEORY-001.md) · [003](../../record/theory.d/THEORY-003.md) · [010](../../record/theory.d/THEORY-010.md) · [011](../../record/theory.d/THEORY-011.md)

**[Distributed optimization](tags/distributed-optimization.md)** (0) — parallelism and sharding, communication, memory management, checkpointing.

**[Data pipeline](tags/data-pipeline.md)** (0) — loading, quality assessment and selection, preprocessing, batch preparation.

**[Attention techniques](tags/attention-techniques.md)** (0) — attention variants and alternative mechanisms, implementation optimizations, context length.

**[Model architecture](tags/model-architecture.md)** (1) — architecture patterns, component design, structural choices, model families, multi-modal designs:
[005](../../record/theory.d/THEORY-005.md)

**[Inference optimization](tags/inference-optimization.md)** (0) — serving-time decisions — batching, cache layout, quantization, compression, sparsity, distillation, sampling algorithms.

**[Adaptation and tuning](tags/adaptation-and-tuning.md)** (0) — taking a trained model somewhere new — fine-tuning and transfer, preference training and alignment, parameter-efficient adaptation, context extension.

**[Representation and encoding](tags/representation-and-encoding.md)** (0) — how the signal is encoded before the expensive network sees it — tokenizers and learned latents, positional encoding, and the frequency or basis choices that go with them.

**[Analysis and evaluation](tags/analysis-and-evaluation.md)** (6) — how to find out whether something worked — what to measure, what a measurement cannot tell you, and which comparisons are unsound; theory, interpretability and debugging belong here too:
[002](../../record/theory.d/THEORY-002.md) · [004](../../record/theory.d/THEORY-004.md) · [006](../../record/theory.d/THEORY-006.md) · [007](../../record/theory.d/THEORY-007.md) · [008](../../record/theory.d/THEORY-008.md) · [009](../../record/theory.d/THEORY-009.md)

**[Generative modeling](tags/generative-modeling.md)** (0) — diffusion, samplers, text-to-image, conditioning and control.

**[Vision and graphics](tags/vision-and-graphics.md)** (0) — neural rendering, reconstruction, perception, visual foundation models.

**[Tiny models](tags/tiny-models.md)** (0) — claims that hold at the small end and not in general — sub-billion-parameter training, where the usual scaling advice inverts.

**By status:** [The current account](status/Active.md) (5) · [Offered](status/Proposed.md) (5) · [Not yet judged](status/Deferred.md) (0) · [Disbelieved](status/Rejected.md) (1) · [Replaced](status/Superseded.md) (0)

## Chronological

What the status column means in this scheme — the words are luria's, the meanings are this project's.

| Status | | Means |
|---|---|---|
| `Active` | The current account | The best explanation the record holds for why this happens |
| `Proposed` | Offered | Stated and plausible, on evidence that is suggestive rather than settling — the document says what would settle it |
| `Deferred` | Not yet judged | Filed because the question is real; no position taken on the answer |
| `Rejected` | Disbelieved | Tested and failed, or contradicted by later work — and the thing it explained may still work perfectly well |
| `Superseded` | Replaced | A later account covers the same ground better, and this one names it |

| # | Title | Summary | Status |
|---|---|---|---|
| [THEORY-001](../../record/theory.d/THEORY-001.md) | Batch normalization works by reducing internal covariate shift | Ioffe and Szegedy (2015), [LIT-002](../../record/literature.d/LIT-002.md) — the explanation batch normalization was named after and introduced with: that training is slowed by each layer's input distribution shifting as the layers below it update, and that holding those distributions steady is what buys the speed. Refuted in 2018; the technique was not. | Rejected — the experiment that would have confirmed it was eventually run, and the benefit survived the shift being put back |
| [THEORY-002](../../record/theory.d/THEORY-002.md) | A dense network contains a sparse subnetwork that matches its accuracy when trained from the same initialization | Frankle and Carbin (2018), [LIT-019](../../record/literature.d/LIT-019.md) — the lottery ticket hypothesis. A randomly-initialized dense network contains a subnetwork that, trained alone from the same initial values, matches the full network in at most the same number of steps. The reset is the claim; the same structure re-initialized randomly does not do it. | Proposed |
| [THEORY-003](../../record/theory.d/THEORY-003.md) | Batch normalization helps by smoothing the optimization landscape, not by reducing internal covariate shift | Santurkar et al. (2018), [LIT-223](../../record/literature.d/LIT-223.md) — the distributional stability batch normalization was named after turns out not to be what it does. Injecting covariate shift back in after the BN layer costs nothing; what BN changes is the smoothness of the loss surface, and other normalisations that do nothing for covariate shift change it comparably. | Active |
| [THEORY-004](../../record/theory.d/THEORY-004.md) | A lottery ticket wins by re-learning the solution its dense run already found | Evci et al. (2020), [LIT-039](../../record/literature.d/LIT-039.md) — sparse networks trained from scratch do worse because gradient flow at initialization is poor, and a rewound ticket does not escape that by having found a good sparse architecture: it lands back in the basin the dense pruning run reached. The hypothesis survives as a claim about initialization, not about architecture. | Active |
| [THEORY-005](../../record/theory.d/THEORY-005.md) | Dense feed-forward layers are already mixtures of experts, and pre-training settles the partition before the neurons | Zhang et al. (2021, 2023), [LIT-226](../../record/literature.d/LIT-226.md) and [LIT-228](../../record/literature.d/LIT-228.md) — a trained dense FFN uses a tiny fraction of its neurons per input, the co-activating neurons partition into functional experts that can be recovered post hoc with the same parameters, and through pre-training the partition stabilizes earlier than the neurons in it. A mixture of experts makes explicit a structure dense training arrives at anyway. | Proposed |
| [THEORY-006](../../record/theory.d/THEORY-006.md) | Task-improving weight perturbations are dense around pretrained weights, and denser the larger the model | Gan and Isola (2026), [LIT-233](../../record/literature.d/LIT-233.md), with a prediction of it independently confirmed by [LIT-230](../../record/literature.d/LIT-230.md) — the fraction of random Gaussian weight perturbations that improve a downstream task rises monotonically with model scale, from 0% at 0.5B to 64% at 32B on GSM8K, and the perturbations that help are task specialists rather than uniform improvements. It is the record's account of why gradient-free post-training works at all, measured on one model family by one group. | Proposed |
| [THEORY-007](../../record/theory.d/THEORY-007.md) | Fine-tuning landscapes are low-dimensional in curvature, and improving directions are degenerate rather than unique | Liang et al. (2026), [LIT-236](../../record/literature.d/LIT-236.md) — a small set of stiff directions carries the improvement in a fine-tuning landscape and their number does not grow with the model. Because improvement depends only on a perturbation's projection onto that subspace, many ambient perturbations share a useful component, so a fixed population of about thirty keeps working as dimension grows. The same heterogeneity gives rise-then-decay: stiff modes saturate while variance keeps accumulating in the flat bulk. | Proposed |
| [THEORY-008](../../record/theory.d/THEORY-008.md) | An evolution-strategies update is mostly a loss-invariant random walk whose size grows with steps and shrinks with population | Hoy et al. (2026), [LIT-235](../../record/literature.d/LIT-235.md), confirmed by [LIT-238](../../record/literature.d/LIT-238.md) — an ES weight update splits into an on-manifold part that changes the loss and an off-manifold part that does not, and in a landscape with many flat directions the second dominates. Its squared norm grows as sigma^2 d T / N, so the drift that three papers in this record read as evidence of forgetting, of functional sparsity, and of a failing search is mostly a random walk that the loss cannot see. | Active |
| [THEORY-009](../../record/theory.d/THEORY-009.md) | A wide two-layer network's training dynamics are a gradient flow on the distribution of its neurons, and that flow is convex | Scale a two-layer network's output by 1/N and the object that moves under SGD stops being the weights and becomes their empirical distribution, which follows a Wasserstein gradient flow of the population risk. The risk is convex as a functional of that distribution — so the non-convexity of the finite-width landscape, and the permutation symmetry that produces most of its apparent local minima, are both artefacts of the coordinates. Four groups reached this within about a year by four routes. | Active |
| [THEORY-010](../../record/theory.d/THEORY-010.md) | Most of the loss barrier between two independently trained networks is permutation, not disagreement | Two networks trained from different seeds land far apart in weight space and close together in function space, and the linear path between them crosses a loss barrier. The account is that the barrier is mostly an artefact of unit labelling: permute the hidden units of one to match the other and the barrier largely disappears. What looked like two different solutions was one solution written in two orders. | Proposed |
| [THEORY-011](../../record/theory.d/THEORY-011.md) | Skip connections make a deep network trainable by smoothing the loss surface, not by making it more expressive | Li et al. (2017), [LIT-014](../../record/literature.d/LIT-014.md) — the same deep network plotted with and without skip connections gives a chaotic surface with visible barriers between nearby points, and a smooth near-convex one. The claim is about *trainability* rather than capacity: the residual network is not a larger function class, it is a reachable one. It is the reason depth stopped being the barrier it had been, and the reason every practice in this record about residual streams is about what to do with them rather than whether to have them. | Active |

