> **Actual grade:** Distinction · **Source:** `Past Examples/Variable Selection for Gaussian - Distinction.pdf`
> Profile written blind (the reviewer did not know the grade). The blind estimate below is the reviewer's guess, not the real mark.

# D15: Variable Selection for Gaussian Process Regression
**Length:** 42 pages (7 front matter + 30 main body + 2 appendix + 3 references), ~7,000 words in the main body (excluding references and appendices; raw extraction gives ~8,100 including tables and equations) · **Area:** Bayesian variable selection / Gaussian processes / MCMC, with a sports-analytics application
**Structure:** Intro 11% · Lit review 19% · Methodology 39% · Empirical analysis (simulation + real data) 27% · Conclusion 4%

## Research question and project type
Can spike-and-slab priors on the inverse length-scales of an ARD (squared-exponential) kernel give direct, probabilistic variable selection in GP regression, and can the posterior be sampled with a Metropolis independence sampler whose proposal is a Laplace approximation? The approach is tested on a small simulation and on football data (328 forwards from the top five European leagues, 14 match statistics plus their squares, response = transfer value). It is a mix of methodological and applied work, with a computational slant. The methodology chapter dominates the page count, but the "method" is largely an assembly of existing pieces.

## Contribution
- **Reproduced or explained:** GP regression and ML-II (Rasmussen & Williams), the ARD kernel family and spike-and-slab on inverse length-scales (taken directly from Dance & Paige 2022, eqs 2.3–2.4 and 3.4–3.6), the standard George–McCulloch spike-and-slab linear regression Gibbs sampler (the LR-SS baseline, pp. 24–25), and textbook Metropolis–Hastings and Laplace approximation (pp. 15–18).
- **Claimed as original:** using a Metropolis independence sampler with a Laplace-approximation proposal for GPR with spike-and-slab priors ("to the best of our knowledge … not yet applied", p. 8). It is a standard MCMC device, so this is a modest, implementation-level novelty. The use of half-normal (truncated) spike and slab components on λ is a small modelling tweak. The self-scraped football dataset (whoscored + transfermarkt) is a novel application.
- **Label:** new or modified method (minor), novel application/data, and a small comparison (OLS, LR-SS, GPR, GPR-SS).

## Theory
Depth: **restates known results**, with some routine derivations. It derives full conditionals for f, λ and γ (eqs 3.17–3.21, p. 14) and the marginalised λ posterior (3.22, p. 15). The LR-SS Gibbs conditionals are derived on p. 25. All are standard Gaussian/inverse-gamma algebra. The Bayesian CLT justification for the Laplace proposal (p. 17) is only asserted. There are no new results and no analysis of the sampler (e.g. ergodicity under the truncated proposal).

## Empirical and simulation work
- **Simulation (pp. 21–23):** the response is generated from a linear model using the 4 OLS-significant football covariates. Six "non-significant variables, which are all zeros" are then added. Constant zero columns contribute nothing to any kernel, so excluding them is trivial and the selection test is close to meaningless. There are 25 random 75/25 splits, and GPR-SS beats GPR in 20/25, with mean MSE 4.09 vs 4.19 (×10⁻³). The difference is tiny, with no standard errors and no paired test. Chains are only 500 iterations, with no burn-in stated.
- **Real data (pp. 25–28):** 4-fold CV MSE is reported for OLS 0.581, LR-SS 0.502, GPR 0.494, GPR-SS 0.477. There is no variability across folds, so calling it a "clear difference" (p. 27) is unsupported. Inclusion probabilities are reported (Table 4.6, 11 variables selected), along with posterior summaries of λ (Table 4.5) and trace plots.
- **Baselines:** reasonable (OLS, LR-SS, ML-II GPR). There is no LASSO and no comparison with Dance & Paige's SSVGP or a sensitivity-based method.
- **Robustness and uncertainty:** no sensitivity analysis for ψ, π_γ, r or the fixed σ² (whose values are never stated). Convergence diagnostics are trace plots only, with no ESS or R-hat and no multiple chains.
- **Reproducibility:** no code is provided or linked. Key hyperparameter values are missing, and sklearn is mentioned only in passing.

## Literature review
About 19% of the main body (pp. 4–8), with roughly 30 references. The breadth is adequate: filter, wrapper and embedded methods, spike-and-slab, GP variable selection (Linkletter, Andersen, Dance & Paige) and VB vs MCMC. It is mostly descriptive, one paper per sentence, with brief critique (e.g. why Gibbs and HMC do not apply, pp. 7–8). It ends usefully by explaining that RWM and adaptive MCMC were tried and got stuck, which motivates the sampler. Mitchell & Beauchamp (1988) is cited on p. 11 but missing from the bibliography.

## Correctness
- **Acceptance step in Algorithm 2 (p. 19, lines 12–15):** it compares only log π(λ*|y) − log π(λ_t|y) and omits the q(λ_t)/q(λ*) ratio. That ratio is required for an independence sampler, and the text itself states it in eq. 3.24 (p. 16). As written, the chain does not target the posterior. Rejection-resampling until λ* > 0 also makes the proposal a truncated normal, which is not accounted for.
- **Simulation design (p. 21):** the all-zero "irrelevant" variables make the selection result uninformative. Standardising a zero column is also undefined, yet p. 20 says all variables are standardised. The claim that the four variables were "proven to be significant in the GPR models" is circular.
- **λ as coefficients:** λ is repeatedly called "regression coefficients" (pp. 23, 27, Table 4.5), although λ are inverse length-scales.
- **Laplace proposal (p. 18):** the proposal N(λ_M, σ²H*⁻¹) is scaled by an unexplained σ², and H* is called "the covariance matrix of λ", which conflates the Hessian with its inverse. Independence of the λ is "assumed" (diagonal), with no justification.
- **γ update (p. 19):** the notation "N(λ_t, rψ)" should be a density evaluated at λ_t with mean 0. There is also a ψ vs ψ² inconsistency.
- **σ² and ρ fixed:** σ² is fixed with an overstated rationale ("prevents overfitting", p. 13). ρ = 1 is fixed because it is sklearn's default (p. 10).
- **IG parameters:** inconsistent, (n−1)/2 on p. 24 vs n/2 on p. 25.
- **Convergence:** "ensures the convergence" is claimed from a single trace plot that shows long sticky flat stretches (Fig. 4.2, p. 28).
- **Conclusion (p. 29):** it lists "goals, assists, dribbleWon" as selected and validates them by "common sense". It ignores oddities in Table 4.6, such as age excluded while age² is included, and accurateCross excluded.

## Writing and presentation
Typeset cleanly in LaTeX with a standard LSE title page. It has a contents page, list of figures and list of tables, numbered equations and properly boxed algorithms (rendered p. 19 looks professional). The rendered maths page (p. 14) is neat and readable. The results pages are weaker. Table 4.5 is a long, unlabelled list of λ₁…λ₂₈ with no variable names and a "95% Percentile" column instead of an interval. Figure 4.1 is a bare bar chart indexed 0–28, with no variable labels. The trace plots (p. 28) are legible but titled "Plot of the First Coordinate in Dimension 28". The English is generally clear but has slips: "can also treated" (p. 1), "makes GPs be able to complex" (p. 2), "approach method" (p. 7), a missing bracket in eq. 4.2, and a reference to Table 4.6 where 4.1 is meant (p. 20). Some passages are generic padding (e.g. explaining Bayes' theorem, p. 12). Citations are mostly sound, with one missing reference.

## Critical reflection
Limited. The conclusion (one page) names sensible extensions: a prior on σ², dependence between length-scales, and scalability to high dimensions via SSVGP. It does not acknowledge the weaknesses that matter: the trivial nulls in the simulation, the tiny MSE gains without uncertainty, the threshold sensitivity, the short chains, and the lack of hyperparameter sensitivity. Results are mostly reported and then declared "superior". The one genuine interpretive passage is the discussion of age² hovering around the 0.5 threshold (p. 23).

## Strengths
1. A coherent, well-motivated pipeline: spike-and-slab on ARD inverse length-scales, marginalising f to improve mixing (p. 15), and a clearly presented sampling algorithm.
2. Honest account of failed attempts (RWM and adaptive MCMC getting stuck, p. 8), used to motivate the method choice.
3. Self-collected real dataset (web-scraped), with a sensible set of baselines including a fully derived LR-SS Gibbs sampler.

## Weaknesses
1. Methodological errors in the core algorithm: the q-ratio is missing from the independence-sampler acceptance, and the truncation of the proposal is ignored.
2. The simulation is uninformative (all-zero nulls), and performance claims rest on small MSE differences with no uncertainty quantification.
3. Thin theory and modest originality: most of the model is taken from Dance & Paige (2022), the "novel" sampler is standard, and there is no sensitivity or diagnostic analysis.

## Scores (1–5, 5 = exceptional for an MSc)
| Originality | Technical depth | Rigour | Empirical work | Literature review | Writing | Presentation | Critical reflection |
|---|---|---|---|---|---|---|---|
| 2 | 2 | 2 | 2 | 3 | 3 | 3 | 2 |

## Blind grade estimate
**Estimate:** Merit (borderline Pass) · **Mark:** ~60 · **Confidence:** low
It is competently assembled and neatly typeset, with a real dataset and a clear algorithm, which should place it around the Merit/Pass boundary. Several things hold it back: it is short, well under 10k words of prose; the simulation is weak; the gains are tiny and lack uncertainty; and the core MCMC step has an error a statistically literate marker would likely spot. A marker who reads it mainly as a sensible applied project could give low-to-mid 60s. One who examines the sampler and simulation closely could put it in the 50s.

## Lessons for a future student
1. Make simulations genuinely test your claim. Irrelevant variables should be real noise covariates, ideally correlated with the signal, and you should report selection rates (TPR/FPR) over many replications with standard errors.
2. When you implement a textbook algorithm, check that the code matches the maths (here, the proposal ratio and the truncation). Report hyperparameter values and proper MCMC diagnostics (ESS, multiple chains, burn-in), and include or link your code.
3. Don't overclaim. A 2–3% MSE improvement from one CV run needs fold-level variability before it can be called "clearly superior", and a limitations section should name the weaknesses that actually matter.
