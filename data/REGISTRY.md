# ML Training Recommendations Registry

Last updated: 2026-02-22

## Experimental Recommendations


## Standard Recommendations

### MoE

- Use largest batch that maintains >80% sample efficiency

- Scale batch size with model size but sub-linearly

### attention

- Use flash attention for all attention computations when hardware supports it

- Tiling size should match hardware SRAM size

- Recompute attention during backward pass instead of storing it

- PagedAttention to accelerate batch inference for LLM sampling

- Use flash-attention-2 over original flash-attention when available

- Keep sequence lengths multiple of 128 for best performance

- Pad attention masks to block boundaries for better hardware utilization

- Prefer GQA to MQA or MHA
  - Implementations: llama2

### attention-alternatives

- Consider for very long sequence tasks

- Use for tasks where attention bottlenecks training

- Combine with standard attention for hybrid approaches

### checkpointing

- Checkpoint frequency should increase with training time

- Save optimizer state every N epochs (N ~ sqrt(total_epochs))

- Use async I/O for checkpoint writing

- Implement multi-level checkpoint strategy

### compilation

- Use operator fusion for small operations

- Optimize memory layout for hardware

- Implement custom kernels for critical ops

- Profile-guided optimization for hot paths

### data-loading

- Memory-map large datasets

- Use mixed precision during data loading

- Pin memory for CPU-GPU transfers

- Profile data loading separate from training

- Use tar archives for dataset storage

- Buffer size should be 2-3x batch size

- Pre-fetch next batch during compute

- Use multiple worker processes (num_workers = 4 * num_gpus)

### data-quality

- Use perplexity-based filtering for quality assessment

- Implement dynamic temperature scaling for mixing

- Adjust mixing ratios based on validation performance

- Monitor domain coverage during training

### distributed-training

- Use micro-batch splitting for pipeline parallelism

- Balance pipeline stages to minimize bubble overhead

- Choose pipeline chunks based on memory vs. compute trade-off

- Use hierarchical allreduce for tensors > 1MB

- Overlap communication with backward pass

- Group small tensors before communication

- Set buffer size to network bandwidth-delay product

- Use sequence parallelism for attention layers

- Overlap communication with computation when possible

- Initialize layer norms with smaller variance (0.02) for stability

- Monitor network utilization during training

- Adapt buffer sizes to network conditions

- Use gradient compression for slow networks

- Place replicas to minimize cross-rack traffic

- Use FSDP over DDP when model size exceeds single GPU memory

- Overlap communication with computation using backward prefetch

- Employ mixed precision to reduce memory usage

- Choose sharding factor based on model and GPU memory size

### hardware-optimization

- Fuse small operations into larger kernels

- Align tensor dimensions to hardware boundaries

- Use hardware-specific memory layouts

- Profile and optimize memory access patterns

### initialization

- Scale attention weights by 1/sqrt(head_dim)

- Initialize final layer weights near zero

- Use smaller variance for deep networks

- Special handling for gated architectures

### language-models

- continued pre-training for fine tuning

- gpt training recipe

- LM in-context learning emerges at scale

- ICL permits few-shot task adaptability

- single cycle of cosine decay is sufficient lr schedule

- smaller batch sizes are more sample efficient (i.e., better loss as a function of tokens seen) earlier in training
  - Implementations: PaLM

- larger batch sizes are beneficial later in training due to better gradient estimates
  - Implementations: PaLM

- throughput (energy efficiency) wins out over theoretically optimal sample efficiency
  - Implementations: PaLM

- consider rewinding to earlier checkpoint and skipping a few batches to mitigate unusual loss spikes
  - Implementations: PaLM

### large-batch-training

- linear warmup of LR stabilizes early training with large batch size.

### memory-efficiency

- Stage optimizer states across data parallel ranks (ZeRO-1)

- Partition gradients and optimizer states (ZeRO-2) for larger models

- Use ZeRO-3 only when other strategies insufficient

- Keep micro-batch size per GPU as large as memory allows

### nlp

- BPE tokenization for open vocabulary tasks
  - Implementations: llama2

### normalization

- Place BatchNorm after linear/conv layers but before activation functions

- Use running statistics for inference

- Consider alternatives like LayerNorm for transformers

- Use larger learning rates with batch normalization

- Monitor loss landscape smoothness during training

- Place BN after linear/conv layers but before activation functions

- Initialize LayerNorm weight close to 1 (0.97-1.0)

- Initialize LayerNorm bias to 0

- Use a smaller learning rate for LayerNorm parameters

### optimization

- Default choice for neural network training

- Common hyperparameters: β₁=0.9, β₂=0.999, ε=1e-8

- Learning rate typically 1e-4 to 1e-3 for most tasks

- warmup to a large early lr, anneal throughout training to small final lr

- skip connections promote training stability by smoothing out the loss landscape

- visualizing eigenvalues of hessian (ratio of largest to smallest) over training can be useful diagnostics

- sharpness in loss landscape corerlates with test error

- use gradient clipping

### scaling-laws

- larger models are more sample efficient

- lr tuning less important for larger models

- `num_tokens ~ 20 * num_params`
  - Implementations: chinchilla, llama2

- Optimal batch size scales approximately with compute budget - `B ∝ C^(1/4)`
  - Implementations: chinchilla, llama2

### systems

- Use continuous batching for inference

- Fuse attention operations where possible

- Overlap prefill and decode compute

### training-dynamics

- Warmup needed scales sub-linearly with model size
  - Implementations: vision_transformer, bert

- Initialize layer norm weights closer to 1 for larger models
  - Implementations: vision_transformer, bert

- Can use shorter warmup periods for wider models
  - Implementations: vision_transformer, bert

- Monitor loss specifically during first ~5000 steps for instabilities
  - Implementations: vision_transformer, bert

- Use gradient clipping during early training phase
  - Implementations: vision_transformer, bert

- Monitor validation loss for unexpected spikes during training

- Track gradient norm statistics to detect training instabilities

- Use learning rate warmup proportional to model size

### training-efficiency

- Use dynamic loss scaling that doubles every 2000 successful steps

- Maintain master weights in FP32

- Store optimizer states in FP32

- Perform forward/backward passes in FP16

### training-stability

- Use pre-norm (RMSNorm) for transformer layers
  - Implementations: llama2

- Monitor exp(loss) for stability

- Track gradient norm ratios between layers

- Use gradient clipping with dynamic threshold

- Implement early warning system for NaNs

### transformers

- Use multi-query attention for decoder-only models to reduce memory bandwidth

- Keep key/value projections shared across heads while query projections remain separate

- Use SwiGLU activation for transformers
  - Implementations: llama2

- use RoPE for LLM (1D sequence) positional embeddings


## Deprecated Recommendations


## Statistics

### optimization

- Total recommendations: 8
- Year range: 2014 - 2020

### normalization

- Total recommendations: 9
- Year range: 2015 - 2019

### nlp

- Total recommendations: 1
- Year range: 2015 - 2015

### large-batch-training

- Total recommendations: 1
- Year range: 2017 - 2017

### training-efficiency

- Total recommendations: 4
- Year range: 2017 - 2017

### distributed-training

- Total recommendations: 18
- Year range: 2018 - 2023

### transformers

- Total recommendations: 4
- Year range: 2019 - 2021

### memory-efficiency

- Total recommendations: 4
- Year range: 2020 - 2020

### training-stability

- Total recommendations: 5
- Year range: 2020 - 2021

### language-models

- Total recommendations: 9
- Year range: 2020 - 2022

### scaling-laws

- Total recommendations: 4
- Year range: 2020 - 2022

### data-loading

- Total recommendations: 8
- Year range: 2021 - 2021

### initialization

- Total recommendations: 4
- Year range: 2021 - 2021

### checkpointing

- Total recommendations: 4
- Year range: 2021 - 2021

### MoE

- Total recommendations: 2
- Year range: 2021 - 2021

### training-dynamics

- Total recommendations: 8
- Year range: 2021 - 2023

### compilation

- Total recommendations: 4
- Year range: 2022 - 2022

### attention

- Total recommendations: 8
- Year range: 2022 - 2023

### hardware-optimization

- Total recommendations: 4
- Year range: 2022 - 2022

### data-quality

- Total recommendations: 4
- Year range: 2023 - 2023

### attention-alternatives

- Total recommendations: 3
- Year range: 2023 - 2023

### systems

- Total recommendations: 3
- Year range: 2023 - 2023

