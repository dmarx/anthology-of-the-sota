---
number: 282
status: Read
formerly:
- NOTE-tmpi8cjd
paper: LIT-540
title: 'Induced on images, text and molecules, and eliminated on demand'
version: 1
date: '2026-09-22'
summary: >-
  Read to settle whether grokking is specific to algorithmic data. It is not —
  but producing it on MNIST, IMDb and QM9 takes two deliberate departures from
  standard practice: a much smaller training set and an inflated initialization
  scale. At standard initialization there is no grokking on any of them. The
  control runs both ways: constraining the weight norm nearly eliminates
  grokking on algorithmic data.
---

# NOTE-282: Induced on images, text and molecules, and eliminated on demand

## Contribution

It converts grokking from a curiosity of one data family into a dial. By
analysing loss as a function of weight norm rather than of time, it identifies
a mismatch between the training and test landscapes, and then uses that picture
to *produce* grokking on three ordinary supervised tasks and to *remove* it on
the algorithmic ones. Whatever one thinks of the mechanism, the
induce-and-eliminate result is the answer to a question the founding paper
left open.

## Key insight

**Plot loss against weight norm instead of against step, and the puzzle turns
into a geometry problem.** Reduced training loss is L-shaped — it falls and
then stays near zero for all larger norms, because a big network can fit a
small training set many ways. Reduced test loss is U-shaped, with a minimum at
some `w_c`. Above `w_c` the two disagree, so the model can sit at zero training
loss and high test loss indefinitely, and only regularization's slow walk down
the norm axis gets it to the generalizing shell. The time scale of grokking is
then the time scale of that walk.

## Assumptions

- **Reduced losses** are defined by minimizing over angular directions at fixed
  norm: `w*(w) ≡ argmin_{‖w‖=w} l_train(w)`. The landscape picture is about
  this reduced function, not about the trajectory the optimizer actually takes.
- The analysis applies to **large initializations** `w > w_c`; the paper states
  that small initializations `w < w_c` always generalize fast.
- The toy derivation is a **teacher–student** regression, with classification
  imitated by thresholding prediction error at `θ = 0.01`.
- The real-data results use **non-standard setups**, named as such by the
  authors.
- The paper notes that reduced training loss should in principle be
  non-increasing, and that optimization issues can break this for very large
  initializations.

## Key results

- **Teacher–student, `α = 2.0` (large init).** Time to 95% *training* accuracy
  is independent of weight decay `γ`; time to 95% *test* accuracy is
  **inversely proportional to `γ`**, as the LU picture predicts. At `α = 0.5`,
  fast generalization regardless of `γ`. At `α = 2.0`: `γ = 0` fails to
  generalize, small `γ` groks, large `γ` generalizes quickly.
- **MNIST.** Depth-3 width-200 ReLU MLP, AdamW, MSE on one-hot targets, with
  two deliberate changes: training set cut from 60k to **1k**, and
  Kaiming-uniform initial weights multiplied by `α > 1`. Grokking appears.
  At the standard initialization (`α = 1`, point A in their Figure 3) there is
  none. Time to generalize rises rapidly near a critical training-set size,
  matching Power et al.
- **IMDb**, LSTM, 1k examples: a weak grokking signal at `α = 6`, none at
  `α = 1`. **QM9**, GCNN: grokking at `α = 3`, none at standard init. Both
  signals are described by the authors as less sharp than on algorithmic data.
- **De-grokking by data.** Larger training sets broaden the Goldilocks zone and
  reduce or remove grokking even at large initialization; below a critical size
  generalization does not happen at all.
- **De-grokking by constraint.** Training on a small-weight-norm sphere nearly
  eliminates grokking on algorithmic datasets.
- **Why algorithmic data is dramatic.** Representation quality there decides
  between chance and 100%; on MNIST between 95% and 100%. So overfitting under
  a bad representation is visible in one case and nearly invisible in the other.

## Limitations

**"Grokking beyond algorithmic data" is true and the setups are not ordinary.**
Every positive result outside algorithmic data needs both a shrunken training
set and an inflated initialization, and the paper says so plainly in the
sentence introducing the MNIST experiment. A reader who takes the title alone
will over-generalize; a reader who reads §4 will not.

**The mechanism is contested and the experiments are not.**
[ARXIV-2310.06110](https://arxiv.org/abs/2310.06110) exhibits grokking with no weight decay and a *rising* weight
norm, which the LU walk cannot produce. That is a counterexample to the
account, not to the induce-and-eliminate demonstrations.

**Reduced landscapes are not trajectories.** Minimizing over angular directions
at each norm is a well-defined object and is not what the optimizer does; the
inference from landscape shape to dynamics is the step doing the work.

## Bearing on the record

**This is the paper that should be carrying `SOTA-200`'s third check**, and it
changes what the check should say. The record currently reads "a
data-starved-regime phenomenon, not a fundamental one", on one paper's
data-fraction number. Data fraction is one axis. Initialization scale relative
to the generalizing norm is a second, it is the one that turns MNIST into a
grokking task, and it is not in the practice at all.

**It also gives the practice something it lacked: a positive control.** Nothing
in `SOTA-200` currently says what to do if you want to know whether an apparent
discontinuity is a regime effect. Here there is an answer — move the regime and
see whether the discontinuity moves with it.

## Open questions

- **Is there a version of the induce experiment at standard initialization?**
  Every non-algorithmic positive result here changes two things at once, so the
  relative contribution of data size and initialization scale is not separated.
- **Does the LU picture survive being made dynamic?** The paper argues from a
  reduced landscape; the counterexample that undoes it is a trajectory
  observation, and nobody has reconciled the two.
