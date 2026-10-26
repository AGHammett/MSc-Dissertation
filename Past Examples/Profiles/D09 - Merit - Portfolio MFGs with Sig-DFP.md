> **Actual grade:** Merit · **Source:** `Past Examples/Portfolio Optimisation via Mean Field Games with Common Noise using Signatured Deep Fictitious Play, and Learning Rate Tuned Neural Networks - Merit.pdf`
> Profile written blind (the reviewer did not know the grade). The blind estimate below is the reviewer's guess, not the real mark.

# D09: Portfolio Optimisation via Mean Field Games with Common Noise using Signatured Deep Fictitious Play, and Learning Rate Tuned Neural Networks
**Length:** 48 pages (42 numbered), ~9,000 words in the main body (excluding references and appendices) · **Area:** Mean field games / stochastic control / deep learning for finance
**Structure:** Intro 7% · Background and lit review (game theory, MFGs, Itô, fictitious play) 23% · Signatures and Sig-DFP (incl. second lit review) 18% · Problem statement 10% · Methodology 10% · Stage I results, Stage II set-up and two propositions 16% · Stage II results 10% · Conclusions and future work 6%

## Research question and project type
The dissertation asks whether Signatured Deep Fictitious Play (Min and Hu, 2021) for MFGs with common noise can be made more stable by replacing its linear signature-regression step for the conditional mean field with other estimators: a path-to-value regressor, a GAN-style pushforward, or Nadaraya–Watson kernel regression. It then asks which policy network (FFN, LSTM or Transformer, each with and without learning-rate tuning) works best in a portfolio MFG. The project is mainly computational, with an applied finance framing and a thin theoretical layer.

## Contribution
- Reproduced or explained: the MFG framework, the HJB/Fokker–Planck system, Itô's lemma, fictitious play, signatures and the Sig-DFP algorithm, all taken from Min and Hu and textbooks.
- Claimed as original: (i) stability changes (stop-gradient "detachment" and EMA smoothing of the mean field); (ii) three alternative conditional-law estimators on signature features; (iii) a "portfolio-aware loss"; (iv) a "corrected theoretical foundation" for Min and Hu's Lemma 4.1; (v) an architecture comparison.
- In practice, (ii) and (v) are the real content. The custom loss is never written down. The "correction" is a standard Nadaraya–Watson consistency result plus a one-line Banach contraction argument that simply assumes the property it needs (Lipschitz constant L < 1). Several claims in the Introduction and §4.2.1 are not delivered: "six different neural architectures" (only three appear), "baselines include naïve nested-loop FP" (never run), and "we document failure modes".
- Label: **new or modified method** (modest) + **systematic comparison**.

## Theory
Depth: **restates known results**, with a light attempt at deriving more. Pp. 5–13 restate textbook material: the Nash equilibrium, the HJB equation (eq. 2), Fokker–Planck (eq. 3), Itô's lemma (eq. 5) and the signature definition (eqs. 7–10). Lemma 1 (p. 28–29) is standard Nadaraya–Watson L²-consistency, with a "proof sketch" that only cites Györfi et al. and Tsybakov. Proposition 1 (p. 29) shows that EMA smoothing is a contraction *if* the population operator is already a contraction (L < 1), which assumes away the substantive question. Nothing connects these results back to the Wasserstein gap in Min and Hu's lemma that the author says is broken (p. 19).

## Empirical and simulation work
- **Stage I** (pp. 25–28) shows four 2×2 diagnostic panels (loss, surrogate error, mean-field residuals, wealth histogram) and a summary table (Table 1). There is a baseline (the unfixed method), which is good.
- **The Stage I evidence is internally inconsistent.** Fig. 1 reports finite residuals for the baseline (Δ≈0.58) and a loss that visibly *decreases*, yet the caption calls it "oscillatory" and Table 1 says the baseline "Diverges". Table 1's MF-gap values (2.1–3.8) are on a different scale from the residuals in the figures (0.007–0.07), and no explanation is given. Table 1 is described as an "LSTM, stress regime" experiment that appears nowhere else. The 5,000-iteration runs are "not shown".
- **Stage II** (pp. 33–36) computes annualised Sharpe, drawdown, VaR/ES and Calmar from "exported wealth series". The equity-curve figure (Fig. 6) has a 0–1000 x-axis matching the 1,000 training iterations, and its curves are noisy, non-cumulative levels between 1.00 and 1.06. That strongly suggests per-iteration terminal wealth was treated as a daily return series with 252-day annualisation, which makes the finance metrics essentially meaningless.
- **The data source is never stated.** The AI appendix mentions downloading the VIX, and §8.1 calls the common noise "a VIX-style proxy", but the dissertation never says whether the data are simulated or real. Model parameters (μ, ν, σ_c, T, the number of agents) are never given.
- The only benchmark is a 0% cash line, so there is no Merton closed-form or analytic LQ solution to check accuracy against.
- **Uncertainty is quantified, but the results contradict each other.** Table 2 contains duplicated rows (identical metrics under different run IDs). Table 3, described as the "top Sharpe per arch/tune", contradicts Table 2: Transformer base is 0.031 vs 0.122, and LSTM bo is 0.074 vs 0.121. Table 4's bootstrap intervals (±1.4 on Sharpe differences of about 0.03) are labelled CI0.05/CI0.95 but called 95%. The author honestly reads Table 4 as showing no tuning effect.
- Reproducibility: the GitHub link is promised "after submission". Hyperparameter grids are listed (p. 32), but the seeds, the number of runs and the data are not.

## Literature review
Roughly 30–35% of the body, spread across Chapter 2 and §3.1–3.2. The coverage of the core sources is reasonable (Lasry–Lions, Carmona–Delarue–Lacker, Cardaliaguet–Hadikhanloo, Perrin et al., Min and Hu, Lyons, Kidger). A lot of space goes on padding, though: the history of Brownian motion (Wiener 1923, Kolmogorov 1931), the applications of Itô's lemma, and von Neumann–Morgenstern. The review is mostly descriptive. The "Critical analysis" paragraph on Sig-DFP (p. 16) and the discussion of nested FP costs (p. 15) are the only genuinely critical parts. There are only around 35 references, and there is no engagement with recent deep-learning MFG solvers beyond Min and Hu.

## Correctness
- **p. 17:** broken cross-reference ("see Sec. ??") for the training loss. The custom loss is never defined, and p. 14 instead says the objective is −E[ln X_T].
- **Inconsistent dynamics.** The SDE is written dX = πX(μdt + νdW + σdB) on pp. 3, 6 and 17, but step 3 on p. 17 drops X. The running cost ℓ = ηπ² + β(x−m)² (p. 7) never reappears.
- **p. 22:** the "raw mean-field update" averages X over *all* trajectories. That gives an unconditional mean, not E[X_t | F^B_t], so it undercuts the stated motivation.
- **p. 24:** the bandwidth conditions are stated for a softmax temperature γ ("γ_N ↓ 0"). Because γ is an inverse bandwidth, this is the wrong direction, and it is also mixed with Silverman's rule.
- **p. 18:** the complexity O(NLp + Np²) is attributed to Min and Hu without justification.
- **p. 27–28:** the claim that the baseline's failure is "confirming the theoretical instability of the original lemma" is not supported.
- **pp. 34–36:** the Stage II metrics appear to be computed on training-iteration series (see above). Tables 2 and 3 contradict each other, and Table 2 has duplicate rows.
- **p. 37:** the conclusions say FFN's edge is "steady and reproducible, not just luck", but Table 4 and the rolling Sharpe (Fig. 8, where leadership swaps) do not support this.

## Writing and presentation
The LaTeX typesetting is clean: a proper title page, contents, lists of figures and tables, booktabs-style tables, and proof boxes on the theory page (p. 29). The figures are matplotlib defaults. Fig. 1's 2×2 panel is readable, but Fig. 6 (equity curves) is an unreadable tangle of six overlapping noisy lines. The prose is fluent but chatty and journalistic: "despite all the hype around attention models", "Think of it less as an upper bound", "For a relatively cheap trick, this fix works surprisingly well". The structure is muddled:
- "Stage I" headings appear twice (§5.1 and §5.2).
- §6.1 is an empty heading.
- The Stage II set-up sits inside the Stage I results chapter.
- "Code Repository" is numbered Chapter 9, after the bibliography.
- The literature review is split across two chapters, and the contributions are listed twice (§1.0.1 and §4.2.1) with different content.

Notation is mostly consistent (σ_c is introduced deliberately), though σ and σ_c drift. Citations are author–date, but spaces are often missing ("1950Nash (1950)", "PDEsGuéant"). Generative AI use is acknowledged in an appendix.

## Critical reflection
There is some. The conclusions note that the results depend on the tight 1,000-iteration budget, and that LSTMs and Transformers might do better with more compute. Table 4 is read correctly as showing no tuning effect. But the internal inconsistencies, the missing data description and the meaning of the "backtest" are never examined. The analysis paragraphs mostly restate numbers with upbeat spin rather than interrogating them. The future-work section (DCC-GARCH common noise) is sensible but brief.

## Strengths
1. Ambitious, current topic (Sig-DFP for common-noise MFGs) with a clear two-stage design: fix the mean-field step, then apply it to the portfolio problem.
2. A genuine implementation that compares three distinct conditional-law estimators against an unfixed baseline, with a consistent four-panel diagnostic layout.
3. Clean LaTeX presentation, a full set of risk metrics defined precisely (p. 30), and a bootstrap comparison of tuning effects.

## Weaknesses
1. Claims that are overstated or never delivered: a "corrected proof" that is really an assumed contraction, a custom loss that is never specified, six architectures and a nested-FP baseline that never appear.
2. Empirical results that contradict each other (Fig. 1 vs Table 1, Table 2 vs Table 3, duplicate rows), with no data description and apparently meaningless annualised metrics computed over training iterations.
3. A padded, largely descriptive background (history of stochastic calculus, Itô's lemma), messy chapter organisation and an informal tone.

## Scores (1–5, 5 = exceptional for an MSc)
| Originality | Technical depth | Rigour | Empirical work | Literature review | Writing | Presentation | Critical reflection |
|---|---|---|---|---|---|---|---|
| 3 | 3 | 2 | 2 | 2 | 3 | 3 | 2 |

## Blind grade estimate
**Estimate:** Merit (borderline Pass) · **Mark:** ~60 · **Confidence:** low
The topic is demanding, and the student clearly built a working Sig-DFP pipeline with several estimators and architectures, which a supervisor in this area would credit. Against that, the theory adds little, many headline contributions are asserted rather than shown, and the empirical section has visible inconsistencies and a questionable evaluation protocol that an attentive marker would penalise. The polished typesetting probably keeps it at the Merit/Pass boundary rather than lower.

## Lessons for a future student
1. Make the contributions list match exactly what the dissertation delivers. Promising six architectures, a nested-FP baseline or a "corrected proof" and then not providing them invites the marker to check every claim.
2. Cross-check every number between figures, tables and text before submitting, and state plainly what the data are (simulated parameters or a real series). One inconsistent table damages trust in all the others.
3. Cut textbook background (the history of Brownian motion, generic Itô's lemma) in favour of a critical review of the closest papers. Benchmark against a known solution (for example, Merton's closed form) so that "better" has a meaning beyond beating cash.
