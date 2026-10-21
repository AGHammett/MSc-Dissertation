# How Multicalibrated Is a Model? Valid Confidence Intervals for the Multicalibration Error: Plain summary

**Supervisor:** Professor Milan Vojnović

## 1. The domain

This project sits where statistical inference meets the evaluation of machine-learning models. Many models output probabilities, such as "a 70% chance this patient is readmitted". Such a model is *calibrated* if, among all cases given 70%, about 70% actually happen. Calibration over the whole population can hide problems: a model can be right on average but systematically too optimistic for older women and too pessimistic for young men. *Multicalibration* asks for calibration within every group in a specified, possibly huge and overlapping, list of subpopulations. It comes from algorithmic fairness, where the worry is that a model quietly underserves particular groups. In practice people summarise it with one number, the *multicalibration error*: the largest calibration gap found across all the groups and across bands of predicted probability, counting only groups above a minimum size.

## 2. The problem

That number has to be estimated from a finite test set, and it is a maximum over many noisy estimates. The group that looks worst is partly the group that was unluckiest in the sample. So the estimated worst gap is biased upwards: this is the "winner's curse". A naive confidence interval, built as if the worst group had been chosen in advance, can contain the true value much less often than the advertised 95%. Safe methods exist, but they are wasteful because they protect every group at once. Nobody knows how much shorter a valid interval for the *worst* gap can be, or has shown that it cannot be shorter.

## 3. What's been done

- **Hébert-Johnson, Kim, Reingold and Rothblum (2018)** introduced multicalibration. They give an algorithm that achieves it without losing accuracy, but no confidence intervals.
- **Guy and colleagues at Meta (2025/26)** propose a practical multicalibration metric: a maximum over many automatically generated, nested subgroups, with each group's gap scaled by its noise level. Their experiments show the unscaled maximum is mostly noise from tiny groups, which is exactly the bias this project is about.
- **Cherian and Candès (2024)** use the bootstrap to put confidence bounds on a model's performance in every group simultaneously, with coverage that becomes exact in large samples. They note in an appendix that this covers multicalibration. This is the "all groups at once" baseline the brief refers to.
- **Chernozhukov, Lee and Rosen (2013)**, an econometrics paper, show how to do inference on the largest or smallest of many estimated quantities. Their key trick is a data-driven selection step that keeps only the near-worst candidates before computing the margin of error, which makes the interval shorter. Their theory is built for a fixed, modest number of candidates.

## 4. What the project would do

The brief asks for one main result, which can go one of two ways.

1. **A shorter valid interval.** Adapt the econometric selection idea to multicalibration. Prove that the resulting interval still has its stated coverage, at least in large samples. Show how much narrower it is than the all-groups interval and than *sample splitting* (choosing the worst group on half the data and measuring it on the other half). I think the lower end of the interval is where selection really matters; nesting or overlap among groups could tighten things further.
2. **An impossibility result.** For a stated group structure, prove that no valid interval can be substantially shorter than the all-groups one. This would be a "lower bound" argument: some situations with different worst gaps cannot be told apart from data.

I think the honest answer is probably both. Big savings look possible when one group is clearly worst. No saving looks possible when many groups are nearly tied, including when the model is almost perfectly multicalibrated. Simulations would check whatever is proved, and an open-source implementation is a possible extra.

## 5. What working on it would feel like

This is mainly a proof project. I would guess roughly 50–65% theory, 25–35% simulation coding in Python, and about 10–15% reading and writing up. Real data would at most be a short illustration. Early weeks mean working through the asymptotic arguments in the Cherian–Candès and Chernozhukov–Lee–Rosen papers and writing small simulations to see the bias and coverage failures yourself. In the middle you would adapt one proof step at a time (for example, showing the selection step keeps the truly worst group) and check each claim numerically. Towards the end the work shifts to larger simulations, which run fine on a laptop, and write-up. The hardest new material is the probability theory of maxima of many correlated random quantities and of bootstrap approximations to them. It builds on, but goes beyond, this term's probability and inference modules.
