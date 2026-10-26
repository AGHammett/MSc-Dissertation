> **Actual grade:** Distinction · **Source:** `Past Examples/Forecasting Term Structure Dynamics with Multi-Output Gaussian Process Regression - Distinction.pdf`
> Profile written blind (the reviewer did not know the grade). The blind estimate below is the reviewer's guess, not the real mark.

# D06: Forecasting Term Structure Dynamics with Multi-Output Gaussian Process Regression
**Length:** 41 pages, ~8,100 words in the main body (excluding references and appendices) · **Area:** Financial time series / Bayesian non-parametrics (Gaussian processes)
**Structure:** Intro 6% · Lit review 18% · Data & methodology (incl. kernel exposition, candidate models, evaluation) 45% · Results, robustness & limitations 28% · Conclusion 3%

## Research question and project type
Can multi-output Gaussian process regression (intrinsic/linear model of coregionalisation, IMC/LMC) forecast monthly US Treasury yields (1–10y maturities, 1988–2020) better than standard benchmarks, in terms of both point accuracy and probabilistic accuracy (log score)? Which kernel structures and covariates (time kernels, lagged CPI and Fed funds, Ludvigson–Ng macro factors, an EWMA volatility input) help, and at which horizons? This is an **applied/computational** project with a light methodological element (the volatility-input kernel). The applied side dominates.

## Contribution
Mostly a well-organised **systematic comparison** and **novel application**: nine GP specifications (1A–1F IMC, 2A–2C LMC) compared against a random walk, ARIMA, VAR(1) on 3 PCs, and independent GPs. The forecasts are rolling out-of-sample at 1, 3, 6 and 12 month horizons, scored by RMSE, MAE and log score. The modest **modified method** element is feeding the trace of an EWMA covariance of yield changes into a Brownian (min) kernel, so that predictive variance rises after volatile periods (Model 1E, pp. 9, 18). The GP machinery (LMC, posterior/predictive, marginal likelihood), the kernels and the Diebold–Mariano test are all textbook exposition from Álvarez et al., Rasmussen & Williams, and Diebold & Mariano. The robustness appendices (retraining rule, macros as outputs, identifiability) are small additions.

## Theory
**Restates known results.** It gives the standard GP predictive equations (p. 10–11), the log marginal likelihood (eq. 9), kernel definitions with sample-path plots (pp. 12–15), a heuristic link from AR(1) to OU (pp. 16–17), and the DM statistic (p. 22). The only "derivation" is Appendix D (p. 38), which tries to show that the coregionalisation parameters are non-identifiable. The argument is flawed (see Correctness). There is no new theory.

## Empirical and simulation work
- Real data only: FRED yields, CPI, Fed funds, Ludvigson–Ng factors. No simulation study.
- The design is reasonable. Training runs from 1988 to 2004 with a 200-month rolling window. Hyperparameters are re-estimated every 50 months. Lagged covariates mean no input forecasting is needed. The evaluation spans multiple horizons.
- The baselines are sensible and include the hard-to-beat random walk. The log score is used alongside RMSE and MAE, which is a strength.
- The DM test is described, and its results are cited in the text ("not statistically significant", pp. 23, 27), but **no DM statistics or p-values are reported anywhere**.
- There are no standard errors or intervals on the score differences. Improvements over the random walk at one step are tiny (RMSE 0.221 vs 0.227, Table 2).
- Robustness checks (pp. 32–33, Appendices B–C) are brief. They cover priors/MAP, a linear vs RBF macro kernel, the retraining rule, and macros as outputs. Several are stated in words only, with no numbers.
- The choice of R_q ("cross-validation of each model's marginal likelihood", p. 16) is vague, and the selected values are not reported.
- The EWMA λ = 0.95 is fixed without sensitivity analysis (acknowledged, p. 35).
- Reproducibility: GPy is mentioned (p. 23), but there is no code link or appendix and optimiser settings are not described.

## Literature review
About 18% of the main body (pp. 4–6). On the term-structure side it is reasonably broad: Nelson–Siegel, Diebold–Li, affine models, Duffee, Joslin–Singleton–Zhu, Litterman–Scheinkman, Ludvigson–Ng. The GP side is thinner (kriging, R&W, Álvarez, Roberts, sparse GPs, heteroscedastic GPs). It is moderately critical: it builds a clear motivating thread (parsimony vs no-arbitrage vs non-linearity) that leads to GPs. However, it cites no prior work applying GPs or ML to yield curves, despite the claim "this study joins the few that use GPR" (p. 6), so the novelty is not positioned. The reference list has only about 25 items.

## Correctness
- p. 4: affine term structure models are attributed to "Nelson and Siegel (1987)". This should be Duffie & Kan (1996) or Vasicek-type literature. It is a clear citation error.
- p. 4: eq. (1) uses τ, but the text then says Diebold–Li fix "λ". The notation is inconsistent.
- p. 6: says Titsias "minimiz[es] a lower bound on the marginal likelihood". The ELBO is maximised.
- Appendix D (p. 38): the non-identifiability argument rotates the *outputs* (B̃ = QᵀBQ). This changes the joint distribution of the observed maturities, so the claim that the likelihoods are equivalent is false. The genuine non-identifiability is rotation or sign of the latent mixing weights (A → AR, leaving B = AAᵀ unchanged). The symbol Q also clashes with Q as the number of kernel groups.
- **Table inconsistencies.** Averaging Table 3's per-maturity figures for Model 1D at 12 lags gives LPS ≈ 1.02 and RMSE ≈ 0.67. Table 2 reports 0.922 and 0.600. On Table 3's numbers, Model 1E would beat 1D at 12 lags, which undermines a headline conclusion. Model 3C's figures do match. In Table 2, Model 1E's 6-lag and 12-lag RMSE/MAE are identical (0.621/0.481), which suggests a copy error.
- p. 32: "Model 1D … significantly outperforms the same model with the locally periodic part omitted". That model is not in any table.
- p. 33: the text describes retraining "when predictive accuracy worsens", but Appendix B uses an ADF-test trigger. Appendix C is titled "macro covariates as outputs", yet its table compares VAR models with and without LN factors.
- The Model 1F 1-lag RMSE of 0.362 is a large outlier and is not discussed.
- The Brownian kernel in absolute time with a rolling window depends on the time origin. This is not discussed.
- Minor: duplicate equation numbers ((8)–(11) reused on pp. 13–14). The log score is written as "log p̂ = ½ log σ̂² + …" (sign/naming confusion, p. 21).

## Writing and presentation
The prose is clear and readable, and the argument flows logically from motivation to models to results. LaTeX typesetting is clean (rendered p. 10: well-set equations, hyperlinked citations). The abstract page is concise. Table 2 is a tidy rotated booktabs-style table with bold best entries.

The figures are weaker. The seven-panel forecast grids (pp. 25–29) have tiny, overlapping year labels, and the forecast lines are hard to distinguish from the truth at this size. The residual plot (p. 34) is cluttered with seven overlaid series and small rotated labels. Five full pages of near-identical forecast grids add little. Model labels (1A–3D) force the reader to keep flipping back to Table 1. There are some typos ("Ludvigsson", "less latent functions", a lowercase "we" after a full stop on p. 10), and "Automatic Relevance Detection" should be "Determination". The paper calls itself "this paper", in journal style.

## Critical reflection
The Limitations section (pp. 33–34) is honest. It covers non-convexity and optimiser local optima, the absence of no-arbitrage, cross-correlated residuals violating the diagonal-noise assumption, and volatility clustering not fully captured around 2008. Future work (heteroscedastic multi-output GPs, a low-rank noise covariance, tuning λ) is sensible. The results are interpreted rather than just listed: horizon-dependence of macro factors, shared latent functions possibly favouring short maturities, and lengthscale interpretation (pp. 29–32). However, the interpretation over-reads small differences without reporting their significance. The conclusion ("presents benefits out-of-sample … more accurate estimation", p. 35) is stronger than the evidence, especially at one step, where the random walk is essentially tied.

## Strengths
1. A broad, well-structured model comparison: nine GP variants and four baselines, across four horizons and seven maturities, with genuinely out-of-sample rolling evaluation.
2. Probabilistic evaluation with the log score alongside RMSE and MAE, plus a simple, intuitive volatility-input kernel that measurably improves short-horizon log score.
3. A clear exposition of the LMC/IMC framework and kernel choices, with economically motivated interpretation of the fitted parameters and an honest limitations section.

## Weaknesses
1. Internal numerical inconsistencies between Tables 2 and 3, and an apparent copy error in Table 2, call the headline 12-month conclusion into question.
2. Statistical significance is asserted (DM tests) but never shown. Several robustness claims have no numbers, and there is no code or implementation detail.
3. The few technical or derivational parts contain errors: the faulty Appendix D proof, the ATSM misattribution and the ELBO direction. The method is almost entirely off-the-shelf, and novelty is not positioned against prior GP and yield-curve work.

## Scores (1–5, 5 = exceptional for an MSc)
| Originality | Technical depth | Rigour | Empirical work | Literature review | Writing | Presentation | Critical reflection |
|---|---|---|---|---|---|---|---|
| 3 | 3 | 2 | 3 | 3 | 4 | 3 | 3 |

## Blind grade estimate
**Estimate:** Merit · **Mark:** ~65 · **Confidence:** medium
This is a competent, well-written applied project, with a sensible design and a good range of models and baselines, which puts it securely above Pass. What holds it back from Distinction is mainly rigour. The results tables contradict each other, the significance tests are claimed but not reported, the one proof is wrong, and the methodological novelty is thin. A generous marker who values the breadth of comparison and the volatility idea might push it to the high 60s.

## Lessons for a future student
1. Cross-check every number that appears in more than one place (per-maturity vs averaged tables), and generate tables directly from code. One inconsistency can undermine your main conclusion.
2. If you say a difference is or is not "statistically significant", show the test statistics or p-values in a table. Don't claim improvements over a random walk when the margin is a few basis points without quantifying the uncertainty.
3. Keep proofs minimal but correct, and position your novelty explicitly against the closest prior work. A short paragraph on existing GP or ML yield-curve papers would make "our contribution" credible.
