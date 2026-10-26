> **Actual grade:** Distinction · **Source:** `Past Examples/Aggregating Preferences for AI Alignment - Distinction.pdf`
> Profile written blind (the reviewer did not know the grade). The blind estimate below is the reviewer's guess, not the real mark.

# D01: Aggregating Preferences for AI Alignment
**Length:** 54 pages (38 numbered main-body pages plus front matter, a 6-page bibliography and a 3-page appendix), ~11,000 words in the main body (excluding references and appendices) · **Area:** Reinforcement learning for LLM fine-tuning (RLHF/RLAIF, policy optimisation)
**Structure:** Intro 7% · Related work 29% · Methodology 21% · Experiments (set-up) 14% · Results and interpretation 25% · Conclusion 4%

## Research question and project type
Can the training–inference mismatch in GRPO-style fine-tuning (training optimises average group reward, while deployment uses best-of-N selection) be reduced by redefining each completion's advantage as its *marginal utility*, i.e. the set utility minus the leave-one-out utility? The student proposes "MUBPO", instantiates it with a max-utility aggregator, and tests it against sequence-level GRPO on TL;DR Reddit summarisation, using Qwen2-0.5B-Instruct as the policy and Gemini-2.0-Flash as an LLM-judge reward. It is a methodological project with a computational/empirical evaluation. The methodological framing dominates, but most of the substantive effort is computational.

## Contribution
- **Original:** the MUBPO framing (pp. 13–19). Advantage = standardised leave-one-out marginal utility of a permutation-invariant set function f, averaged over m stochastic judge rounds. The student shows that sum-utility recovers GRPO (eq. 3.11–3.12), proposes max-utility for BoN, and specifies (but does not implement) a win-rate utility borrowed from InfAlign (pp. 15–16). Also original: a full training pipeline with an LLM judge, 3 configurations × 5 seeds, and an ablation on n = 4 vs 8.
- **Reproduced or explained:** policy-gradient/REINFORCE, baselines, GAE, PPO, token- and sequence-level GRPO, the BoN order-statistic distribution (eq. 2.16, matched to Balashankar et al.), k1/k3 KL estimators, and the chain-rule decomposition of sequence KL (Appendix II).
- In substance the max-utility variant gives the argmax completion an advantage proportional to (best − second best) and gives zero to everyone else, then standardises. That is close to existing "BoN-aware" or pass@k-style training ideas, and the related literature is not engaged with beyond InfAlign.
- **Labels:** new or modified method (main) · novel application/data (secondary).

## Theory
**Depth:** restates known results, with light derivations of known results.
- Appendix I (pp. 45–46) derives the policy-gradient theorem, and Appendix II (p. 47) gives the sequence-KL decomposition. Both are textbook derivations.
- p. 11 states the BoN density N·π(y)·F(y)^{N−1}, and Fig. 2.1 illustrates it for a normal base distribution.
- pp. 28 and 33 compute the standardised advantages (√3, −1/√3; √7, −1/√7) for one-hot reward vectors. This is simple, but it is a nice check on the logged plots.
- There is no analysis of the new estimator itself. The student never shows that the leave-one-out difference is an unbiased gradient for E[max], never asks what the subsequent standardisation does to that property, and gives no variance or convergence argument. Claims such as "mitigates distribution shift" and "eliminates granularity mismatches" (p. 2) are asserted rather than proved.

## Empirical and simulation work
- **Data:** real data (trl-lib/tldr train/validation splits). The validation set size is not stated.
- **Design:** standard GRPO (sum, m = 1, n = 4) vs max_m3 (max, m = 3, n = 4) vs max_m3_n8. Batch size 1 and 500 steps on a single RTX 6000. Hyperparameters, seeds, prompts and hardware are tabulated well (Tables 4.1–4.7, pp. 22–24). A ROUGE-L pilot motivates the LLM judge (Fig. 4.1).
- **Baseline:** GRPO is a sensible baseline. However, the "ablation" in comparison 1 changes two things at once (the utility *and* m = 1 → 3), so the effect of the utility is not isolated.
- **Uncertainty:** 5 seeds, with means and 95% CIs (Fig. 5.4, 5.9) and per-seed tables. The student correctly notes that the CIs overlap for the score difference (p. 30). No paired test is used, even though max_m3 wins on every seed, which a sign or paired test could have exploited.
- **Robustness:** a single task, a single small model, a single judge prompt, no judge-reliability check, and no human evaluation. The "sanity check" (§5.1) rests on one example, scored by the same judge.
- **Reproducibility:** the set-up is well described, but no code repository is mentioned.

## Literature review
Around 29% of the main body (Ch. 2, ~9 pages), which is heavy for the length. It is a competent, textbook-style tour of RLHF, MDPs, policy gradients, PPO, GRPO, DPO/NLHF/InfAlign, LLM-as-a-judge, BoN and marginal utility. It is mostly descriptive. The only critical thread is the critique of GRPO's token/sequence granularity and its average-case objective, which is well tied to the motivation. Directly competing work on inference-aware or BoN-aware fine-tuning (beyond InfAlign) and on leave-one-out baselines (e.g. RLOO) is missing. The marginal-utility economics section is thin (1 page).

## Correctness
- **Major confound (pp. 33–36):** the n = 8 model is evaluated by the max over 8 completions and the n = 4 model by the max over 4 (§3.5). A higher best-of-8 score is expected even from an *identical* policy, so the "+3%" gain cannot be attributed to training. The student even justifies the result this way (p. 33), and calls it "little additional computational cost" (p. 35), although it doubles generation and judge calls.
- The KL reduction of "about 4 per sequence" (abstract, p. 37) is driven largely by one outlier seed (15.6, Table 5.2b). The +1% score gain is not significant (p. 30), yet the abstract and conclusion say MUBPO "consistently outperforms" and is "empirically validated".
- "Minimal overlap of CIs → likely significant" (p. 35) is not a valid test.
- Interpreting KL as "exploration" and score as "exploitation", and the claim that too high a score signals overfitting (pp. 31–32), is loose reasoning.
- The sanity check (§5.1) claims the judge "reflects human judgment" on the basis of one example. The max_m3 summary contains a factual error yet still scored 90, which arguably undercuts the claim.
- Minor errors: equation cross-references are wrong on p. 5 ("Equation 2.1 to Equation 2.3" should be 2.2). The heading "Loss vs. Step" sits over KL plots (pp. 29, 34). The bibliography lists the same Ouyang et al. paper twice (2022a/b), and a citation reads "Ng & updated by Tengyu Ma".

## Writing and presentation
The rendered pages show a clean LaTeX layout: a proper LSE title page, numbered equations, a well-typeset Algorithm 1 (p. 21) and tidy booktabs-style tables. The figures are a weak point. Figs 5.1 and 5.2 (p. 28) are raw Weights & Biases screenshots of very noisy, unsmoothed per-step traces with tiny legends. The CI plots (p. 31) are matplotlib error bars, each based on only 5 points. The prose is fluent and well signposted (each chapter opens with a roadmap), but it is padded with promotional language ("extensive contribution", "solid foundation", applicability to robotics and resource allocation, all untested). There are a few typos ("especiall", "to to", "From an technical"). Notation is mostly consistent, but the superscripts get heavy in §3.4 and in the algorithm.

## Critical reflection
Partial. The conclusion lists sensible limitations: one dataset, five seeds, and the tension between exploitation and exploration. The student also concedes that the score CIs overlap. However, the interpretation consistently leans towards the favourable reading. The confounds (n at evaluation, m differing between arms), the dependence on one judge, and the tiny training budget are not acknowledged as threats to the main conclusions. Results are interpreted rather than just reported, but with motivated framing.

## Strengths
1. A clear, well-motivated idea: framing best-of-N alignment through leave-one-out marginal utility, with GRPO recovered as the sum-utility special case (pp. 13–15).
2. An ambitious end-to-end implementation: a real LLM policy trained with RL and an API-based LLM judge, three configurations across five seeds, with thorough tabulation of settings.
3. Polished typesetting, including a complete pseudo-code algorithm, and small analytical checks that tie the logged advantage values to the theory (pp. 28, 33).

## Weaknesses
1. Confounded comparisons: the n = 4 vs n = 8 evaluation uses different best-of-N sizes, and the GRPO vs MUBPO comparison also changes m. The headline effects are not cleanly identified.
2. The claims outrun the evidence: a non-significant +1%, a KL gain driven by an outlier, a one-example "human judgment" check, and very small-scale training (batch 1, 500 steps).
3. No theory for the proposed estimator (bias, variance, effect of standardisation), and a largely descriptive literature review that misses the closest prior work.

## Scores (1–5, 5 = exceptional for an MSc)
| Originality | Technical depth | Rigour | Empirical work | Literature review | Writing | Presentation | Critical reflection |
|---|---|---|---|---|---|---|---|
| 4 | 3 | 2 | 3 | 3 | 3 | 4 | 2 |

## Blind grade estimate
**Estimate:** Merit · **Mark:** ~66 · **Confidence:** low
The originality, ambition and polish of the implementation push it towards the top of the Merit band, and a marker who values a working novel method on a current topic could reach 70. What holds it back is the statistical and design weaknesses: the n = 8 evaluation confound, two variables changed at once, significance overstated, and a single outlier driving the KL result. Together with the lack of any theory for the estimator and the overclaiming, these are what a statistics department would penalise.

## Lessons for a future student
1. Design ablations that change one thing at a time, and evaluate every arm under an identical inference protocol. Otherwise your headline effect may be an artefact of the evaluation.
2. Match claim strength to the evidence. If the CIs overlap, say "no significant difference" in the abstract too, and use a proper paired test when the runs share seeds. Check whether one outlier is driving a mean.
3. If you propose a new estimator, add at least a short theoretical property, such as unbiasedness or a variance argument. In a statistics MSc this does more for the mark than extra literature exposition.
