> **Actual grade:** Merit · **Source:** `Past Examples/Stock Index Forecasting Using Tensor-Values Predictors - Merit.pdf`
> Profile written blind (the reviewer did not know the grade). The blind estimate below is the reviewer's guess, not the real mark.

# D11: Stock Index Forecasting Using Tensor-Values Predictors – Empirical Insights from the STOXX 50 Index
**Length:** 41 pages (29 numbered main-body pages plus front matter and 6 pages of references; no appendices), ~9,500 words in the main body (excluding references and appendices) · **Area:** Matrix/tensor factor models, financial forecasting (MSc Financial Statistics (Research))
**Structure:** Intro 7% · Lit review (including tensor preliminaries) 21% · Method 19% · Simulation 8% · Empirical study 40% · Conclusion 5%

## Research question and project type
Does removing time-varying grand-mean, row and column "main effects" from each matrix slice before a Tucker (matrix-factor) decomposition give better factors, and do those factors help predict 20-day-ahead EURO STOXX 50 index returns from a 50 stocks × 13 characteristics × 838 days tensor? The project is applied and computational: a short simulation, then a single empirical forecasting exercise that compares raw, Tucker-only and main-effects+Tucker predictors fed into a Lasso. The applied empirical part dominates.

## Contribution
The dissertation presents "main effect decomposition" (Eq. 3.1–3.10) as "a novel method" that "addresses a research gap" (abstract, pp. 2, 7, 10). In fact it is the standard two-way ANOVA decomposition of each matrix slice, and the full model (main effects plus a matrix factor model on the interaction term) is the subject of Lam & Cen (2024), "Matrix-valued factor model with time-varying main effects", by the supervisor. That paper is cited only for a null-space property (p. 12) and for the ReMSE metric (p. 16), not as the source of the method. That is a serious over-claim of originality. Everything else is reproduced: Tucker/HOSVD via tensorly, the Lam–Yao eigenvalue-ratio estimator, and the Lasso. The literature-standard stock characteristics (size, volatility, reversal, momentum, turnover, Amihud illiquidity) are built from WRDS data. What is genuinely the student's own is the application: building a stock-characteristic tensor for the EURO STOXX 50 and comparing the forecasts. Label: **novel application/data**, with elements of **replication/exposition**. The claimed **new method** is not justified.

## Theory
Depth: **restates known results**. The only derivation is the closed-form main-effect estimators (pp. 10–11, Eq. 3.4–3.10), obtained by pre- and post-multiplying by vectors of ones under sum-to-zero constraints. This is elementary ANOVA algebra. The eigenvalue-ratio estimator is quoted as "consistent" without stating assumptions (p. 12). The HOSVD algorithm (Table 1, p. 12) and the definitions of tensor products (p. 5) are restated. There are no theorems, no properties of the estimators, and no discussion of identifiability beyond the constraints.

## Empirical and simulation work
- **Simulation (pp. 15–17):** one configuration only (100×100×100, 5×5 core, all N(0,1), 1000 replications), shown as a single boxplot. Path B builds main effects into the data, which Tucker-only with a 5×5 core cannot represent, so Method 2 winning is close to guaranteed by design. There is no variation in dimensions, signal-to-noise ratio or factor strength, and no assessment of how well loadings or factor numbers are estimated. The methods are mislabelled: Method 1 is called "main effect decomposition only" when it is Tucker only (p. 16). It is not stated whether the ReMSE compares against the noiseless signal or the noisy observations.
- **Empirical (pp. 18–27):** real WRDS data, Sept 2020 to Dec 2023, with careful explanation of how the constituents and variables were processed. However:
  - There is no sign that the 13 features were standardised before Tucker/PCA. The author notes magnitudes differing by orders of magnitude (p. 23), and Model B's 1×1 factor "explaining 99.99%" (p. 24) is very likely a scale artefact.
  - Tucker is applied to the training and test sets separately (p. 24), so the test-set loadings are estimated with test data.
  - Daily-sampled 20-day returns overlap, which is not addressed. The Lasso's cross-validation scheme is not specified (it may not be time-series CV).
  - The only baselines are internal (raw, Tucker, C1, C2). There is no zero or historical-mean forecast, so a test MSE of about 10⁻³ for monthly returns cannot be judged.
  - There is one train/test split, with no standard errors, Diebold–Mariano test or rolling evaluation.
  - Factor numbers are chosen partly ad hoc (an 85% variance rule borrowed from a fixed-income textbook, p. 25).
  - No code is provided. Python, SQL and tensorly are mentioned.

## Literature review
About 21% of the main body (pp. 4–9), plus feature-motivation citations in Section 5.2. Breadth is reasonable: classical factor models, CP/Tucker history, matrix factor models (Wang et al., Chen et al., He et al., Chang et al.), factor-number selection (Bartlett through to Lam–Yao, Ahn–Horenstein) and the Lasso. It is almost entirely descriptive, a chronological list of who proposed what. It never engages critically, never positions the work against Lam & Cen (2024), the closest paper, and never explains why main effects should help.

## Correctness
- Overstated novelty and missing attribution of the main-effects matrix factor model to Lam & Cen (2024) (pp. 2, 7, 10, 28).
- The Hadamard product is defined wrongly. Element-wise multiplication of differently sized tensors is said to give a 4-way tensor, which describes an outer product (p. 5).
- "Lasso applies a larger penalty to smaller coefficients" is incorrect (p. 8).
- The eigenvalue-ratio argmin runs over m ∈ [1, M] (Eq. 3.12–3.13, p. 12), so it uses the undefined λ_{M+1}. Because γ̂_t γ̂_tᵀ has 1_M in its null space (stated on p. 12), the smallest eigenvalue is zero and the unrestricted ratio is degenerate. Lam & Yao restrict to m ≤ M/2, which is ignored. Choosing 8 of 13 column factors (p. 25) is suspicious for this reason.
- Says main effect decomposition "involves computing the eigenvalues and eigenvectors of the matrix" (p. 23), which is false: it is only row and column means.
- Inconsistent predictor dimensions. Section 3.3 says the Model C predictors include α_t and β_t (length M+N+d_r d_c), but Section 5.3 gives z_C1 ∈ ℝ⁸ and z_C2 ∈ ℝ²⁴ (p. 26).
- The index is "predict y_{t+1}" in Section 3 but "20 trading days ahead" in Section 5. 670+138 = 808, not 838, and this is not explained. A 36-month (750-day) share-growth feature cannot be computed from data starting in Sept 2020 (p. 21).
- The reported monthly mean and volatility of "-0.05 and 20.86" have unclear units (p. 20).
- The conclusion that main effect decomposition "significantly enhances" accuracy (abstract, p. 28) rests on one split with no significance testing.
- Wrong cross-references: "Figure 1" and "Figure 2" for the CP and Tucker illustrations (p. 6), and "Figure 3.13/3.14" (p. 25).

## Writing and presentation
The prose is fluent but padded and generic ("With the advent of the information age…", p. 1), with frequent signposting and summaries in place of argument. LaTeX typesetting is clean: the rendered maths page (p. 11) is neatly laid out with numbered equations and hyperlinked references. The figures are weak. The simulation boxplot (p. 16) and the eigenvalue plots (pp. 24–26) are small default-matplotlib images whose axis labels and titles are unreadable at normal size, and the illustrative figures (pp. 1, 6, 14) look like imported textbook-style diagrams. Tables are tidy (booktabs, p. 26). There are typos and slips: "Tensor-Values" in the title, "benchmakring", "firtly", "with with", "exratd togdp", and "three variables" listed as "two". Notation drifts (f_t vs F_t, bold vs non-bold γ). Referencing is consistent author–year.

## Critical reflection
Weak. Section 6 promises to "discuss the limitations" but gives only future extensions (more factors, ESG, tensor regression). There is no acknowledgement of the single split, the missing naive benchmark, scaling, overlapping returns, or the data-snooping in choosing factor numbers. Some interpretation is attempted: overfitting in Model A, and why a single row factor might suffice (p. 27). But the discussion of why stocks show little row variation (p. 26) is muddled and partly self-contradictory.

## Strengths
1. A genuine, carefully assembled real dataset: a 50×13×838 tensor of literature-motivated stock characteristics from WRDS, with well-documented currency, corporate-action and total-return adjustments (pp. 19–23).
2. A clear end-to-end pipeline (decompose → choose factor numbers → vectorise → Lasso → out-of-sample MSE) with a sensible comparison set including a raw-data baseline that shows overfitting.
3. Clean LaTeX typesetting and an orderly structure. The main-effect estimators are derived step by step and are easy to follow.

## Weaknesses
1. Originality is misrepresented. A standard two-way decomposition, already developed in the supervisor's paper, is presented as the student's new method.
2. The empirical design is shallow and flawed: no feature standardisation, test-set Tucker fitted separately, a single split, no naive benchmark, no uncertainty or significance testing, and an ad hoc choice of factor numbers. The headline conclusions are therefore unsupported.
3. Theory is minimal and contains errors (Hadamard product, the eigenvalue-ratio range, the Lasso description). The simulation is a single, design-favoured scenario with unreadable figures, and limitations are not discussed.

## Scores (1–5, 5 = exceptional for an MSc)
| Originality | Technical depth | Rigour | Empirical work | Literature review | Writing | Presentation | Critical reflection |
|---|---|---|---|---|---|---|---|
| 2 | 2 | 2 | 3 | 3 | 3 | 3 | 2 |

## Blind grade estimate
**Estimate:** Merit · **Mark:** ~62 · **Confidence:** medium
It is a competent, well-organised applied project with real data work and a full pipeline, which keeps it clear of a Pass. But the technical content is thin: elementary ANOVA algebra plus off-the-shelf tools. There are several methodological errors, and the evaluation (one split, no naive benchmark, no inference) cannot support its "significant improvement" claims. A supervisor-marker would also notice the over-claimed novelty relative to Lam & Cen (2024). Low-to-mid Merit seems most likely. A strong data effort could push it to the upper 60s, and an examiner focused on the errors could put it near 58.

## Lessons for a future student
1. Attribute methods precisely. If your "new" method comes from your supervisor's working paper, say so, and state your own contribution honestly (for example, a new application or extension). Over-claiming novelty is easy to spot and costs credibility.
2. Forecasting comparisons need a naive benchmark (zero or historical mean), honest out-of-sample protocols (no fitting on test data, time-series CV, rolling windows), and some measure of uncertainty or significance. Without these, MSE tables say little.
3. Make simulations informative: vary signal strength, dimensions and misspecification, include cases where your method should not help, and make figures legible with labelled axes at print size.
