# NOTE documents

<!-- GENERATED below this line by `luria index` — edit README.stub instead. -->

**[Adaptation-And-Tuning](tags/adaptation-and-tuning.md)** (1):
[020](../../record/notes.d/NOTE-020.md)

**[Attention-Techniques](tags/attention-techniques.md)** (5):
[005](../../record/notes.d/NOTE-005.md) · [007](../../record/notes.d/NOTE-007.md) · [014](../../record/notes.d/NOTE-014.md) · [016](../../record/notes.d/NOTE-016.md) · [021](../../record/notes.d/NOTE-021.md)

**[Data-Pipeline](tags/data-pipeline.md)** (2):
[002](../../record/notes.d/NOTE-002.md) · [018](../../record/notes.d/NOTE-018.md)

**[Distributed-Optimization](tags/distributed-optimization.md)** (2):
[003](../../record/notes.d/NOTE-003.md) · [006](../../record/notes.d/NOTE-006.md)

**[Generative-Modeling](tags/generative-modeling.md)** (2):
[009](../../record/notes.d/NOTE-009.md) · [019](../../record/notes.d/NOTE-019.md)

**[Inference-Optimization](tags/inference-optimization.md)** (1):
[023](../../record/notes.d/NOTE-023.md)

**[Model-Architecture](tags/model-architecture.md)** (2):
[004](../../record/notes.d/NOTE-004.md) · [011](../../record/notes.d/NOTE-011.md)

**[Model-Stability](tags/model-stability.md)** (4):
[001](../../record/notes.d/NOTE-001.md) · [008](../../record/notes.d/NOTE-008.md) · [013](../../record/notes.d/NOTE-013.md) · [022](../../record/notes.d/NOTE-022.md)

**[Representation-And-Encoding](tags/representation-and-encoding.md)** (1):
[010](../../record/notes.d/NOTE-010.md)

**[Training-Optimization](tags/training-optimization.md)** (5):
[012](../../record/notes.d/NOTE-012.md) · [015](../../record/notes.d/NOTE-015.md) · [017](../../record/notes.d/NOTE-017.md) · [024](../../record/notes.d/NOTE-024.md) · [025](../../record/notes.d/NOTE-025.md)

**By status:** [Read](statuses/Read.md) (25) · [Skimmed](statuses/Skimmed.md) (0) · [Unread](statuses/Unread.md) (0) · [Re-read](statuses/Superseded.md) (0)

What the status column means in this scheme — the words are luria's, the meanings are this project's.

| Status | | Means |
|---|---|---|
| `Read` | Read | The full text, closely enough to state its assumptions and results exactly — the only status that licenses a claims table |
| `Skimmed` | Skimmed | Abstract, figures and selected sections; honest, useful, and explicitly not enough to source a practice from |
| `Unread` | Unread | Looked at and deliberately set aside — a human judgement, not a backlog entry. A paper nobody has reached simply has no note (ADR-025) |
| `Superseded` | Re-read | A later reading replaced this one, and names it |

| # | Title | Summary | Status |
|---|---|---|---|
| [NOTE-001](../../record/notes.d/NOTE-001.md) | Understanding and Improving Layer Normalization | LayerNorm's benefit is in the backward pass — the derivatives of the mean and variance re-center and re-scale the gradients — not in forward normalization. Its bias and gain increase overfitting risk and "do not work in most cases". | Read |
| [NOTE-002](../../record/notes.d/NOTE-002.md) | Efficient Online Data Mixing | An Exp3 bandit over data domains, rewarded by per-domain training loss on the batches the run is already taking, revising the mixture during training. 19% fewer iterations to the next best method's final perplexity, at negligible wall-clock cost. | Read |
| [NOTE-003](../../record/notes.d/NOTE-003.md) | PyTorch FSDP | Fully Sharded Data Parallel as an industry-grade PyTorch component: a sharding factor F generalising replication through full sharding, communication overlapped by backward prefetching, and a rate limiter over the CUDA caching allocator. The first cluster in [#114](https://github.com/dmarx/anthology-of-the-sota/issues/114) whose practices its paper actually supports. | Read |
| [NOTE-004](../../record/notes.d/NOTE-004.md) | Scale Efficiently | Model shape, not only model size, determines downstream fine-tuning quality — and the widely adopted T5-Base and T5-Large configurations are Pareto-inefficient. Read in full for [#114](https://github.com/dmarx/anthology-of-the-sota/issues/114) after its LIT note was found to describe a different paper. | Read |
| [NOTE-005](../../record/notes.d/NOTE-005.md) | FlashAttention | Attention is bounded by HBM traffic rather than FLOPs. Tiling to on-chip SRAM and recomputing the attention matrix in the backward pass gives exact attention in Θ(N²d²M⁻¹) HBM accesses against standard attention's Θ(Nd + N²) — and Proposition 3 proves no exact algorithm beats that across all SRAM sizes. | Read |
| [NOTE-006](../../record/notes.d/NOTE-006.md) | GPipe | Pipeline parallelism by splitting a mini-batch into micro-batches. Bubble overhead is O((K−1)/(M+K−1)) and negligible once M ≥ 4K; re-materialization plus partitioning cuts peak activation memory from O(N×L) to O(N + (L/K)(N/M)). | Read |
| [NOTE-007](../../record/notes.d/NOTE-007.md) | FlashAttention-2 | FlashAttention reached only 25–40% of peak FLOPs/s; the loss was work partitioning between thread blocks and warps, not the algorithm. Three changes — fewer non-matmul FLOPs, parallelism over sequence length, better warp partitioning — give ~2× and 50–73% of peak. | Read |
| [NOTE-008](../../record/notes.d/NOTE-008.md) | Visualizing the Loss Landscape of Neural Nets | Filter normalization makes loss-surface plots comparable across architectures, and under it sharpness correlates with generalization error. Deep networks transition from nearly convex to chaotic; skip connections prevent that transition, which is why they are needed at depth. | Read |
| [NOTE-009](../../record/notes.d/NOTE-009.md) | Latent Diffusion Models | Train the diffusion model in the latent space of a pretrained autoencoder rather than in pixels. The autoencoder removes imperceptible detail; the diffusion model then spends its capacity on semantics instead of on high-frequency content nobody sees. | Read |
| [NOTE-010](../../record/notes.d/NOTE-010.md) | Neural Machine Translation of Rare Words with Subword Units | Translation was open-vocabulary and NMT models were not, backing off to a dictionary for unknown words. Encoding rare and unknown words as subword units — byte pair encoding adapted to segmentation — makes the model open-vocabulary itself. | Read |
| [NOTE-011](../../record/notes.d/NOTE-011.md) | Attention Is All You Need | Dispenses with recurrence and convolution entirely. The 1/√d_k scaling has a stated reason: with unit-variance components, q·k has variance d_k, and unscaled dot products push the softmax into regions of extremely small gradients. | Read |
| [NOTE-012](../../record/notes.d/NOTE-012.md) | LARS: Large Batch Training of Convolutional Networks | Linear LR scaling with warm-up is "not general enough and training may diverge". Layer-wise Adaptive Rate Scaling sets a per-layer rate from the ratio of weight norm to gradient norm, reaching AlexNet at batch 8K and ResNet-50 at batch 32K without accuracy loss. | Read |
| [NOTE-013](../../record/notes.d/NOTE-013.md) | DeepNet | Scale the residual by α and initialise the residual branch with gain β, both constants determined only by depth. Bounds the model update theoretically, combines Post-LN's quality with Pre-LN's stability, and reaches 1,000 layers. | Read |
| [NOTE-014](../../record/notes.d/NOTE-014.md) | Monarch Mixer | One sub-quadratic primitive — Monarch matrices — along both sequence length and model dimension. Matches BERT-base/large on GLUE with up to 27% fewer parameters and 9.1× throughput at 4K, and beats ViT-b by 1% at half the parameters. Attention-free, not hybrid. | Read |
| [NOTE-015](../../record/notes.d/NOTE-015.md) | Decoupled Weight Decay Regularization | L2 regularization and weight decay are equivalent for SGD and **not** for adaptive methods. Common Adam implementations do L2 while calling it weight decay; decoupling it recovers the real thing, separates the weight-decay and learning-rate choices, and closes Adam's generalization gap to SGD with momentum. | Read |
| [NOTE-016](../../record/notes.d/NOTE-016.md) | Fast Transformer Decoding: multi-query attention | Incremental decoding is bounded by the memory bandwidth of reloading the keys and values, not by arithmetic. Share one key/value head across all query heads: much faster decoding, "only minor quality degradation". | Read |
| [NOTE-017](../../record/notes.d/NOTE-017.md) | Scaling Laws for Neural Language Models | Loss is a power law in model size, dataset size and compute over seven orders of magnitude, and shape barely matters. Its learning-rate finding is the opposite of what the record recorded: larger models require a *smaller* rate to avoid divergence, and the paper carries an explicit LR(N) rule. | Read |
| [NOTE-018](../../record/notes.d/NOTE-018.md) | Segment Anything | The data engine is the transferable part. Three stages — assisted-manual, semi-automatic, fully automatic — each stage's labels training the model that produces the next stage's, ending in 1.1B masks. The model and the dataset are built together. | Read |
| [NOTE-019](../../record/notes.d/NOTE-019.md) v2 | Elucidating the Design Space of Diffusion-Based Generative Models | Pulls diffusion's tangled formulations apart into independent axes — sampler, training noise distribution, and preconditioning — and derives the preconditioning coefficients from a unit-variance requirement rather than choosing them. FID 1.79 on class-conditional CIFAR-10 at 35 network evaluations; a pretrained ImageNet-64 model improves 2.07 to 1.55 from the sampler alone. | Read |
| [NOTE-020](../../record/notes.d/NOTE-020.md) | Don't Stop Pretraining | Two adaptive-pretraining stages, and the second is the surprise. Domain-adaptive pretraining (DAPT) on a large in-domain corpus helps; task-adaptive pretraining (TAPT) on the task's own small unlabelled set also helps, and the two are complementary rather than alternatives. | Read |
| [NOTE-021](../../record/notes.d/NOTE-021.md) | Grouped-Query Attention | MQA is fast and costs quality, and training a separate model for inference is undesirable. Two results: uptrain an existing multi-head checkpoint with 5% of pretraining compute, and use an intermediate number of key-value heads — quality near multi-head at speed near MQA. | Read |
| [NOTE-022](../../record/notes.d/NOTE-022.md) | RMSNorm | LayerNorm gives re-centering and re-scaling invariance; the hypothesis is that re-centering is dispensable. Normalize by root mean square alone — re-scaling invariance and implicit learning-rate adaptation kept, 7–64% less time per step. | Read |
| [NOTE-023](../../record/notes.d/NOTE-023.md) | PagedAttention and vLLM | KV cache memory is huge, grows and shrinks dynamically, and was managed as one contiguous block — so fragmentation and duplication capped the batch size. PagedAttention borrows OS paging: near-zero waste, sharing within and across requests, 2–4× throughput at equal latency. | Read |
| [NOTE-024](../../record/notes.d/NOTE-024.md) | ReLoRA: High-Rank Training Through Low-Rank Updates | Restart LoRA repeatedly during pretraining — merge the adapter, reinitialise it, prune the optimizer state, re-warm the learning rate — so a sequence of low-rank updates sums to a high-rank one. The ablation is the finding: the full-rank warm start it also requires accounts for most of the measured gain, and the restart machinery adds 0.42 perplexity on top of it. | Read |
| [NOTE-025](../../record/notes.d/NOTE-025.md) | AdaNorm: Adaptive Gradient Norm Correction based Optimizer for CNNs | Keeps an EMA of the gradient's scalar L2 norm and, when the current gradient is smaller than that history, scales it up to match — a floor under the gradient norm, applied to Adam's first moment only. The exact mirror image of gradient clipping. Evidence is VGG/ResNet on CIFAR-10, CIFAR-100 and TinyImageNet; there is no transformer and no language result. | Read |

