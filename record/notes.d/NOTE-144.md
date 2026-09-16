---
number: 144
status: Read
formerly:
- NOTE-tmps2205
paper: LIT-058
title: 'Measuring the Effects of Data Parallelism on Neural Network Training'
version: 1
date: '2026-09-15'
summary: >-
  The relationship between batch size and training steps to a goal error
  always follows the same three-regime shape — perfect scaling (b-fold
  benefit), diminishing returns, and a maximum useful batch size beyond which
  adding more parallelism helps nothing — but where these transitions occur is
  workload-specific and cannot be reliably predicted from simple properties of
  the model, data, or optimizer.
---
# NOTE-144: Measuring the Effects of Data Parallelism on Neural Network Training

## Contribution

This paper provides the most rigorous and extensive empirical
characterization of how batch size affects neural network training speed
(measured in steps to reach a goal out-of-sample error) across 6 model
families, 3 optimizers, and 7 datasets, with independent metaparameter
tuning at every batch size. It establishes a universal three-regime
relationship — perfect scaling, diminishing returns, and maximal data
parallelism — and shows that the maximum useful batch size varies
dramatically (from 2^4 to 2^16 across experiments) as a function of the
model, optimizer, and dataset, but not in ways predicted by simple
heuristics. The paper also partially reconciles contradictions in the prior
literature by tracing them to improper metaparameter handling and budget
choices.

## Key insight

The relationship between batch size and training steps to a goal error
always follows the same three-regime shape — perfect scaling (b-fold
benefit), diminishing returns, and a maximum useful batch size beyond which
adding more parallelism helps nothing — but where these transitions occur is
workload-specific and cannot be reliably predicted from simple properties of
the model, data, or optimizer. Most prior apparent "generalization gaps" for
large batch sizes can be traced to (a) learning rate heuristics tuned at a
different batch size, (b) epoch budgets that structurally favor small
batches, or (c) step budgets that structurally favor large batches — rather
than any intrinsic degradation from large batch training.

## Assumptions

- Per-step wall-clock time is independent of batch size (idealized data-
  parallel hardware); steps-to-result is therefore a proxy for wall-clock
  time.
- The best trial from a 100-sample quasi-random search is a reliable
  estimate of the optimally tuned model at each batch size.
- Metaparameter search spaces were chosen to be equally appropriate at all
  batch sizes (best effort; not formally guaranteed).
- The three-regime shape is universal; the paper assumes it holds beyond the
  tested workloads without a mechanistic proof.
- Synchronous data parallelism is the training paradigm; results do not
  directly transfer to asynchronous or gossip-based training.
- Steps-to-result is measured at the best metaparameter setting seen in
  finite search; the true optimum may differ.

## Key results

- **Universal three-regime curve (Figure 2 and throughout).** For every
  tested workload (35 total), steps-to-result vs. log(batch size) follows:
  (1) perfect scaling with slope -1, (2) diminishing returns with slope in
  (-1, 0), (3) a flat plateau at the maximum useful batch size. The
  transition points are workload-specific and span 2^4 to beyond 2^16.
  *Holds when:* Holds across 6 model families, 3 optimizers, 7 datasets,
  with independent metaparameter tuning at every batch size.
- **Momentum extends perfect scaling (Figure 4).** On CIFAR-10 ResNet-8,
  Nesterov momentum extends perfect scaling from batch size 16 (plain SGD)
  to batch size 256 — a 16x extension of the linear speedup regime.
  *Holds when:* Demonstrated on MNIST and CIFAR-10; consistent with Kidambi
  et al. 2018 showing momentum does not harm small-batch performance.
- **Generalization gap is a metaparameter artifact (Section 5).** Five
  specific methodological failures in prior work explain apparent
  generalization gaps: (1) LR heuristics, (2) epoch budgets, (3) step
  budgets, (4) insufficient regularization at large batch, (5) improper goal
  error choices. With correct methodology, no intrinsic generalization
  penalty is observed.
  *Holds when:* Validated for MNIST, Fashion MNIST, and ImageNet (ResNet-50
  with label smoothing).

## Claims

| id | claim | strength | support |
|---|---|---|---|
| C1 | Increasing batch size always produces the same characteristic three-regime curve: perfect b-fold scaling, then diminishing returns, then a maximum useful batch size — across all tested models, optimizers, and datasets. | strong | Validated across 35 workloads, 168,160 individual trained models, 71,638,836 loss measurements. The three-regime shape held consistently when metaparameters were independently tuned at each batch size, for both training error and out-of-sample error, and across different error goal values (which only shift the curve vertically). |
| C2 | The maximum useful batch size varies enormously between workloads (roughly 2^9 to 2^16 in the experiments) and does not depend consistently or predictably on dataset size, model width, or model depth. | strong | Dataset size: subsets of MNIST at different sizes showed negligible change in maximum useful batch size. Model width: narrower Transformer models scaled better than wider ones (opposite of Chen et al. 2018). Depth: inconsistent results across model families. The largest effects came from optimizer choice (momentum vs. plain SGD) and model architecture family (ResNet vs. VGG). |
| C3 | SGD with momentum (and Nesterov momentum) extends the perfect scaling regime to much larger batch sizes than plain SGD, with identical performance to SGD at small batch sizes. | strong | Demonstrated for Simple CNN on MNIST and Transformer on LM1B (Figure 4). On CIFAR-10 with ResNet-8, Masters & Luschi found perfect scaling ends at batch 16 for plain SGD; experiments here show Nesterov momentum extends it to batch 256. The identical performance at small batch sizes is consistent with Kidambi et al. 2018. |
| C4 | There is no evidence that larger batch sizes inherently degrade out-of-sample error when metaparameters are properly tuned; apparent generalization gaps in prior work are artifacts of learning rate heuristics or budget choices. | moderate | For MNIST and Fashion MNIST trained near saturation, differences in maximum performance between batch sizes are very small and within noise. For Transformer on LM1B, performance is budget-limited at all batch sizes. Label smoothing eliminates overfitting at large batch sizes for ResNet-50 on ImageNet. Five specific failure modes in prior literature identified and traced to methodology (Section 5). |
| C5 | The optimal learning rate and momentum do not follow any simple scaling rule with batch size; tuning metaparameters independently at each batch size is essential to measure true scaling behavior. | strong | Across all problems, the optimal effective learning rate generally increases with batch size but does not consistently follow linear or square root scaling. For Transformer, the optimal strategy is to increase momentum while decreasing or holding learning rate constant (Figures 21 and 22). Heuristic scaling is identified as the primary cause of inconsistent results in prior literature. |
| C6 | Solution quality depends on compute budget more than on batch size per se; the relevant question for practitioners is not which batch size gives the best final model, but rather how compute budget varies as a function of batch size. | strong | Figure 11: with a step budget, larger batch sizes achieve better validation error; with an epoch budget, smaller batch sizes achieve better validation error. Both effects are explained mechanically by how many gradient updates are performed, not by intrinsic batch size effects on solution quality. |

## Method

**Systematic steps-to-result measurement with independent metaparameter
tuning at each batch size.**

1. Define a goal out-of-sample error (validation error) for each workload.
2. For each batch size and each workload, perform quasi-random search
(Bousquet et al. 2017) over the training metaparameters: initial learning
rate, momentum (where applicable), and learning rate decay schedule (alpha,
T). Use 100 non-divergent trials per batch size. 3. Measure the number of
training steps required for the best metaparameter configuration to first
reach the goal validation error — this is the "steps to result." 4. Plot
steps-to-result vs. batch size on a log-log scale. Identify the three
regimes: perfect scaling (slope = -1, b-fold benefit), diminishing returns
(slope between -1 and 0), and maximal data parallelism (slope = 0, flat). 5.
Repeat for varied models (architecture, width, depth), optimizers (plain
SGD, SGD with momentum, Nesterov momentum), and datasets. 6. Validate that
the goal error choice only shifts the curve vertically without changing
transition points; validate that training error and out-of-sample error give
similar curves.

- Steps-to-result as the primary measure of training cost (hardware-
  agnostic, equals wall time on ideal data-parallel hardware)
- Quasi-random metaparameter search with equal budgets across all batch
  sizes
- Independent tuning of learning rate, momentum, and learning rate decay
  schedule at every batch size
- Three-regime characterization: perfect scaling / diminishing returns /
  maximal data parallelism
- Comparison of optimizer families (plain SGD vs. momentum vs. Nesterov
  momentum)
- Dataset with 71.6M loss measurements across 168,160 models publicly
  released

## Concepts

- **steps to result** — The number of training steps (gradient updates)
  required for the best-tuned model to first reach a fixed goal out-of-
  sample (validation) error. This is the primary measure of training cost in
  the paper because it is hardware-agnostic and equals wall time on
  idealized data-parallel hardware where per-step time is independent of
  batch size.
- **perfect scaling (b-fold benefit)** — The regime where doubling the batch
  size halves the number of training steps required to reach the goal error.
  Appears as a slope of -1 on a log-log plot of steps vs. batch size. Occurs
  at small batch sizes for all tested workloads.
- **maximal data parallelism** — The regime where increasing batch size no
  longer reduces the number of training steps. Appears as a flat region on
  the steps-to-result vs. batch size curve. The batch size at which this
  plateau begins is called the "maximum useful batch size."
- **workload** — The combination of a dataset, model architecture, and
  training algorithm (optimizer). Used throughout as the unit of analysis
  because scaling behavior is specific to the combination, not to any single
  component.
- **metaparameter** — Any parameter that controls training but is not a
  model weight — including learning rate, momentum, learning rate schedule
  parameters (alpha, T), and regularization strength. The paper's key
  methodological contribution is tuning these independently at every batch
  size rather than using scaling heuristics.
- **epoch budget vs. step budget** — An epoch budget fixes the total number
  of per-example gradient computations; this structurally favors small batch
  sizes because they do more gradient steps per epoch. A step budget fixes
  the number of gradient updates; this structurally favors large batch sizes
  because they process more data per step. Most prior work's "generalization
  gap" results from using epoch budgets.

## Connections

**Builds on.**

- Goyal et al. (2017): Accurate, Large Minibatch SGD — Training ImageNet in
  1 Hour — Prior work popularizing linear LR scaling heuristic; this paper
  shows the heuristic breaks down beyond certain batch sizes
- Keskar et al. (2017): On Large-Batch Training for Deep Learning — Claimed
  large batches degrade generalization; this paper partially refutes this as
  a metaparameter artifact
- Masters & Luschi (2018): Revisiting Small Batch Training for Deep Neural
  Networks — Found critical batch size degradation under epoch budget with
  SGD; this paper shows momentum extends perfect scaling well beyond their
  critical point
- McCandlish et al. (2018): An Empirical Model of Large-Batch Training
  ([LIT-017](../literature.d/LIT-017.md)) — Concurrent work deriving the gradient noise scale as a
  predictor of critical batch size; complementary theoretical framing of the
  same empirical phenomenon

**Related.**

- Follow-on work on optimizer design for large-batch training — Motivates
  search for optimizers (beyond momentum) that extend perfect scaling;
  mentions KFAC as candidate

## Recommendations

- **R1** — Always tune the learning rate, momentum, and learning rate
  schedule independently at every batch size being compared. Never use
  simple scaling heuristics (linear, square root, constant) to transfer
  metaparameters from one batch size to another.
  *Topic:* Metaparameter tuning for batch size experiments · *Strength:*
  strong · *When:* Applies whenever comparing training efficiency across batch
  sizes or whenever changing batch size in a production system. Failure to
  do this is the primary source of incorrect conclusions about large-batch
  training in the literature.
- **R2** — Use SGD with momentum (or Nesterov momentum) rather than plain
  SGD to extend the perfect scaling regime to larger batch sizes. This can
  dramatically reduce training time without changing the out-of-sample
  error.
  *Topic:* Optimizer selection for large-batch training · *Strength:* strong ·
  *When:* Demonstrated clearly on MNIST (Simple CNN) and CIFAR-10
  (ResNet-8). Likely generalizes broadly; consistent with Kidambi et al.
  2018. Other optimizers (KFAC) may extend it further.
- **R3** — Use label smoothing or other regularization techniques at large
  batch sizes to compensate for reduced implicit regularization from small-
  batch gradient noise. Without additional regularization, overfitting may
  prevent reaching the goal error at large batch sizes.
  *Topic:* Regularization at large batch sizes · *Strength:* moderate · *When:*
  Demonstrated for ResNet-50 on ImageNet; label smoothing extended the
  maximum useful batch size above 2^14. L2 regularization and Gaussian
  gradient noise were tried and failed; label smoothing worked. May be
  problem-specific.
- **R4** — Measure steps-to-result vs. batch size empirically for any new
  workload before committing to a hardware configuration, as the maximum
  useful batch size can vary from 2^4 to beyond 2^16 and cannot be reliably
  predicted from workload properties alone.
  *Topic:* Infrastructure planning · *Strength:* strong · *When:* Most important
  for high-value or long-running training jobs. The measurement requires
  training many models at different batch sizes with tuned metaparameters,
  which itself is expensive but less so than running a large cluster with
  suboptimal batch size throughout.
- **R5** — When the training budget is fixed in wall time (step budget),
  prefer larger batch sizes; when fixed in compute (epoch budget), prefer
  smaller batch sizes. The "best" batch size depends entirely on what
  resource is being constrained.
  *Topic:* Budget-aware batch size selection · *Strength:* strong · *When:*
  Applies whenever there is a hard constraint on either wall time or total
  compute (FLOPs). On modern data-parallel hardware where per-step time is
  roughly constant across a range of batch sizes (e.g., TPU pods), the step
  budget framing is most appropriate.

## Bearing on the record

The paper is already `LIT-058`, unread until now. Its first recommendation
contradicts a habit this record has practices for: never transfer learning
rate, momentum or schedule across batch sizes by a scaling heuristic,
because the comparison that heuristic makes is not between batch sizes but
between one tuned configuration and one untuned one. Several existing
practices about batch size and warmup were written against papers that did
exactly that.

## Limitations

- Metaparameter tuning was done by hand-specified quasi-random search
  spaces, which may not be equally appropriate at all batch sizes despite
  the authors' best efforts.
- Only synchronous SGD variants were studied; results may not transfer to
  asynchronous SGD or gossip-style algorithms.
- The maximum useful batch size was only measured up to the limits of
  available hardware (2^16 in most cases); some workloads may scale further.
- The paper cannot determine whether the best trial in a 100-trial search is
  a robust finding or a lucky sample; no percentile statistics are reported.
- Smaller batch sizes got more validation measurement opportunities per
  training run, potentially giving them a structural advantage in the steps-
  to-result measurement.
- The study focuses on synchronous data parallelism only; results do not
  directly apply to model parallelism, pipeline parallelism, or
  decentralized training.
- The exact relationship between maximum useful batch size and model/data
  properties remains unpredictable; the paper describes the phenomenon but
  provides no mechanistic theory.

## Open questions

- Can any optimizer (beyond momentum variants) reliably extend perfect
  scaling across most workloads, and what properties of an optimizer
  determine this?
- Is there a principled way to predict the maximum useful batch size for a
  new workload without exhaustive experiments?
- How do the scaling regimes change for very large models (billions of
  parameters) that require model parallelism in addition to data
  parallelism?
- Does the three-regime shape persist for asynchronous or gossip-style
  distributed training, and if so, where do the transition points occur?
- Why do narrower Transformer models scale better to larger batch sizes than
  wider ones, contrary to intuition and prior work?
- What is the relationship between the gradient noise scale (McCandlish et
  al.) and the empirical transition points observed here? The concurrent
  McCandlish paper predicts B_crit; does it also correctly predict the onset
  of perfect scaling?
- How does decentralized (gossip) SGD's effective batch size compare to its
  nominal batch size, and does it follow the same three-regime curve?
