> **Actual grade:** Distinction (Winton Prize) · **Source:** `Past Examples/Reinforcement Learning for Market Making-Distinction(Winner of the Winton Prize for Best Dissertation 2023-24.pdf`
> Profile written blind (the reviewer did not know the grade). The blind estimate below is the reviewer's guess, not the real mark.

# D10: Reinforcement Learning for Market Making: Leveraging Behavioral Cloning and Dynamic Weights for Optimal Trading Strategies
**Length:** 45 pages (3 front matter + 40 body + 2 references; no appendix), ~10,500 words in the main body (excluding references and appendices) · **Area:** Reinforcement learning / quantitative finance (market microstructure)
**Structure:** Intro 6% · Related work 17% · Preliminaries (LOB, state, actions, reward) 16% · Methodology (DQN, A2C, behaviour cloning, dynamic weights) 17% · Experiment set-up 23% · Results 16% · Conclusion 4% (word shares; results take up more pages, about 12 of 40, because they are mostly full-page figures)

## Research question and project type
Can deep RL agents (DQN and A2C) learn market-making quoting policies that beat a fixed-spread rule, and does adding behaviour cloning (BC) from an "expert", plus a heuristic schedule that changes the RL and BC loss weights during training ("dynamic weights", DW), make them more stable and profitable? Agents are tested on replayed Nasdaq LOB data (MSFT, NVDA) and on a Glosten–Milgrom-style simulated market. The project is **computational/applied** with a light methodological element (the DW heuristic and the reward shaping). Computational/applied work dominates. There is no theory.

## Contribution
- **Reproduced or explained:** the LOB basics, the PnL reward (adapted from Spooner et al. 2018), DQN and A2C (textbook equations), and BC as an auxiliary loss (cited to Ross & Bagnell 2010, and close in form to Liu et al. 2020's imitative RL for trading).
- **Claimed as original:** (i) a decay factor β on unrealised PnL and a linear or power inventory penalty in the reward (pp. 10–11). These are standard reward-shaping devices, close to Spooner et al.'s dampened PnL, so the claimed novelty is overstated. (ii) "Dynamic weights": a multiplicative 1.05/0.95 update of λ1 and λ2, triggered by whether the change in BC loss passes a threshold (Table 4, p. 24). This is an ad hoc schedule. (iii) A dual environment, historical replay plus a simulation.
- **Label:** new or modified method (minor, heuristic) plus systematic comparison (7 models × 2 environments).

## Theory
**Depth: restates known results.** Chapter 4 (pp. 12–17) restates the DQN Bellman target and loss, the n-step A2C advantage and policy gradient, and the BC loss. Nothing is derived. The DW scheme comes with no justification beyond words, such as a link to curriculum or annealing schedules or any convergence argument. The equations themselves contain slips (see Correctness).

## Empirical and simulation work
- **Data:** real Databento Nasdaq LOB data for MSFT and NVDA ("several months" according to p. 19, but only one day is plotted and no date range, split or sample size is given). The simulated Glosten–Milgrom market is described only in prose (p. 21), with no parameters, trader proportions or price process. The text says code is "available in the appendix or upon request", but there is no appendix.
- **Design:** a fixed-spread benchmark (0.5 × spread) against DQN and A2C, each with and without BC and BC+DW. Hyperparameters are tabulated (Tables 1–6) and said to come from a grid search, but the grid is not reported. Training is 300 iterations of 500 steps. There is no description of a train/test separation in time. "Best model identified during training" is then evaluated on 100 episodes (p. 25), which brings in selection bias.
- **Expert:** the "Prophet" expert uses knowledge of future prices (pp. 14–15). Cloning an oracle with look-ahead is a questionable design choice, and the thesis never discusses whether it leaks future information into the policy.
- **Uncertainty and robustness:** Tables 7–8 report means and standard deviations over 100 episodes, but there are no confidence intervals, significance tests or multiple seeds. Differences between RL variants are tiny relative to the SDs (PnL means 1.95–2.00 with SDs of about 0.9). There is no ablation of β or α, no transaction-cost sensitivity, and no comparison against Avellaneda–Stoikov even though it is cited.
- **Reproducibility:** poor. There is no code, no simulator specification and no data window.

## Literature review
About 17% of the body (pp. 3–6), covering about 16 references. It reasonably spans Glosten–Milgrom and its extensions, RL market making (Chan & Shelton, Lim & Gorse, Spooner et al., Gašperov & Kostanjčar, Sadighian) and BC (Bain & Sammut, Daftry et al., Liu et al.). It is **mostly descriptive**: one paragraph per paper and little synthesis. The only critical thread is the simulation vs historical-replay trade-off (market impact ignored). There is no engagement with the stochastic-control literature beyond a mention, nor with RL-from-demonstrations work such as DQfD.

## Correctness
- **Sharpe ratio is wrongly defined** as (realised + unrealised PnL) / *variance* of PnL (p. 25). The reported values also cannot be reproduced from the tables: for DQN, 1.96/0.95² ≈ 2.2 and 1.96/0.95 ≈ 2.1, yet the table gives 4.42.
- **Results contradict the narrative.** The text says BC lowers inventory mean and SD (p. 38), but A2C_BC has inventory SD 0.65 against 0.09 for plain A2C, and a higher mean (0.21 vs 0.20). DQN_BC_DW has a *higher* inventory SD than DQN_BC. "Significantly outperformed" is claimed without any test.
- **Units are inconsistent.** Trades are 50 units, and Figure 2 shows inventory around 100–250, yet Table 7 reports inventory means of about 0.18. Training plots show episode PnL of 0–800 and rewards down to −15,000, which have no clear relation to the table values. The simulated-environment numbers in Table 8 look suspiciously round.
- **The DW direction is described inconsistently.** P. 12 says that as performance improves the weights shift "to place greater emphasis on behavior cloning". P. 16 says λ2 (BC) decreases. In Table 4, a small change in BC loss *increases* λ2.
- **Equation slips:** the BC loss (eq. 17, p. 14) has a leading minus sign but is meant to be minimised. Eq. 12 is labelled ∇θL but shows the loss itself. P. 13 says "k is the discount factor" (k is the n-step horizon). Eq. 16 mixes θ and θ′.
- **Placeholder reference:** Gašperov & Kostanjčar (2021a) is cited as "IEEE Transactions on Something, xx(yy):zz–aa" (p. 41). Author names are garbled throughout ("Gavsperov & Kostanjvcar"). Sadighian (2020) is "available at" an email address.
- The "Efficient Market Hypothesis" is misused to mean only that bid < ask (p. 18).

## Writing and presentation
The prose is fluent but generic and repetitive. Many paragraphs restate the obvious, for example the state-space bullet points on p. 8 and repeated "robust and adaptive" phrasing, and there is some marketing tone ("meticulously designed", "invaluable tool"). Claims are often stronger than the evidence. The LaTeX looks professional (Palatino, booktabs tables). The title page is clean, and the maths page (p. 14) is tidy. However:
- Figure 2 (p. 15) and Figures 4–11 are full-page matplotlib stacks with small axis labels. Some pages carry nothing but figures, and two figures appear on otherwise blank page sequences.
- From §5.1.2 onwards (p. 19 to the end), the body text is visibly indented, which looks like an unclosed list environment. This is clear on the rendered p. 37.
- Table 8 has a duplicated "PnL Mean" header where "PnL Std" is meant. Figure 3 labels NVDA as "INDV".
- Spelling switches between "behavior cloning" and "behavioral cloning". Referencing is in author–year style, but the entries are of poor quality (see above).

## Critical reflection
Weak. The conclusion restates the claimed wins and lists generic future work: market impact, multi-agent settings, other reward structures, other assets. Limitations such as zero transaction costs and no market impact are listed as assumptions (p. 18) but are not revisited when interpreting results. Several issues go unacknowledged: the look-ahead expert, the tiny and noisy differences between variants, the inventory-SD reversals that contradict the claims, and the thin simulator. The results chapter mostly describes curves ("more stable", "smoother") rather than quantifying or explaining them.

## Strengths
1. A complete, working pipeline: LOB replay on real Nasdaq data plus a simulated market, with 7 agent variants trained and compared under a common protocol.
2. Sensible reward design discussion (pp. 9–11), which motivates the inventory penalty and unrealised-PnL damping from clear failure modes of naive PnL rewards.
3. A clear, well-organised structure, a reasonably broad literature review of RL market making, and complete hyperparameter tables.

## Weaknesses
1. Statistical rigour is lacking: Sharpe ratio is misdefined and its values cannot be reproduced, there are no significance tests or seeds, differences are within noise, and the stated conclusions contradict parts of the tables.
2. Reproducibility and specification are thin: the simulator is described only in prose, there is no data window or train/test split, the promised appendix and code are missing, and the expert uses future prices without discussion.
3. Careless finishing: a placeholder citation ("IEEE Transactions on Something"), garbled author names, an internally inconsistent description of dynamic weights, equation slips, and layout and indentation faults.

## Scores (1–5, 5 = exceptional for an MSc)
| Originality | Technical depth | Rigour | Empirical work | Literature review | Writing | Presentation | Critical reflection |
|---|---|---|---|---|---|---|---|
| 3 | 2 | 1 | 3 | 3 | 3 | 3 | 2 |

## Blind grade estimate
**Estimate:** Merit (borderline Pass) · **Mark:** ~60 · **Confidence:** low
The project is ambitious in scope and implementation (real LOB data, two environments, seven models), and it reads fluently, which pulls it towards Merit. Against that, a statistics department would penalise the misdefined and irreproducible Sharpe ratio, the absence of any uncertainty quantification or testing, conclusions that the tables partly contradict, the inconsistent DW description and the placeholder reference. These problems undermine trust in the results. It could plausibly fall in the high 50s.

## Lessons for a future student
1. In a statistics dissertation, the claim "method A beats method B" needs inferential support: multiple seeds, confidence intervals or paired tests, and an honest statement when differences are within noise. Check that every sentence in the results matches the numbers in your tables.
2. Define metrics correctly and make them reproducible: give the formula, units and sample. A reader should be able to recompute a headline number (like a Sharpe ratio) from what you report.
3. Fully specify your data and simulator (time window, train/test split, simulation parameters), and if you promise code or an appendix, include it. Proofread references: one placeholder entry signals carelessness to the examiner.
