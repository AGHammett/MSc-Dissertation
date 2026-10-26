> **Actual grade:** Distinction · **Source:** `Past Examples/Two-step Maximum Likelihood and Bayesian Estimation of Structural Equation Modelling - Distinction.pdf`
> Profile written blind (the reviewer did not know the grade). The blind estimate below is the reviewer's guess, not the real mark.

# D14: Two-step Maximum Likelihood and Bayesian Estimation of Structural Equation Modelling
**Length:** 50 pages, ~10,500 words in the main body (excluding references and appendices; ~15,400 raw tokens including tables and maths) · **Area:** Latent variable models / SEM, psychometrics and social statistics
**Structure:** Intro 9% · Lit review 9% · Models and variables 9% · Methodology 26% · Simulation study 27% · Empirical study (ESS Round 10) 16% · Conclusion 5%

## Research question and project type
The dissertation asks whether a two-step "structural-after-measurement" (SAM) estimator for continuous SEMs (fit the measurement model first, then fix its parameters and fit the structural model) performs comparably to one-step joint estimation. It also asks whether hybrid variants that mix ML and Bayesian estimation across the two steps ("ML + draws + ML", "Bayesian + ML") are workable alternatives. It is mainly a computational and methodological comparison (a 27-cell simulation), with an applied illustration on European Social Survey data. The simulation comparison dominates.

## Contribution
Most of the framework is reproduced from existing work. The SAM / pseudo-ML idea and its corrected variance formula come from Rosseel and Loh (2022), Bakk and Kuha (2018) and Xue and Bandeen-Roche (2002). Bayesian two-step SEM comes from Levy (2023), and the Gibbs sampler and conjugate posteriors from Lee (2007), reproduced in Table 2. The student's own additions are modest:
- combining ML and Bayesian estimation across the steps;
- a resampling way to carry step-1 uncertainty into step 2: draw θ₁ from N(θ̂₁, se²) or from its posterior, refit, and combine the results with the law of total variance (pp. 17–18);
- the simulation grid (measurement R², structural R², n);
- a cross-national ESS application, including a timing comparison (12.96 min joint vs 1.16 min two-step).

Labels: **systematic comparison** (main), a minor **new or modified method** (the draws-based variance), and **novel application/data**.

## Theory
Depth: **restates known results**. The model-implied moments (eqs 5–8), the ML discrepancy function (eq 11), the full conditionals for the Gibbs sampler (eq 13, Table 2), the two-step corrected variance (eq 18) and the consistency of pseudo-ML (citing Gourieroux and Monfort, p. 16) are all stated with citations, not derived. The total-variance combination on p. 17 is a straightforward application of a standard identity. No new results are proved. The Bayesian step-2 variants are set out (p. 18) but then dropped without being implemented.

## Empirical and simulation work
- **Design.** The design looks sensible on paper: 3 latent factors with 4 indicators each, a mediation structure, 27 settings, 2,000 replications, five estimators, blavaan default priors, and 2 chains of 10,000 draws.
- **The results are not credible.**
  - The reported biases and RMSEs are of order 10⁻⁸ to 10⁻¹⁷ for joint ML and SAM (Tables 4, 5 and 13). Yet Tables 6 and 7 report Monte Carlo standard deviations of about 0.03–0.15 for the same estimators. RMSE cannot be smaller than the s.d., so something in the computation is badly wrong.
  - All 95% intervals reportedly cover the true value in 100% of replications for almost every method and setting (p. 26, Table 8 note). That is impossible for calibrated 95% intervals over 2,000 replications.
  - These anomalies are reported as findings rather than flagged as bugs. For example, "RMSE ... decreases by approximately 12 decimal places" (p. 22).
- **Other weaknesses.**
  - The measurement-parameter density comparison uses a single "typical dataset" per setting (p. 28).
  - The empirical study treats ordinal 1–5 items as continuous and assumes MCAR, neither with justification.
  - Step-1 uncertainty is ignored in the cross-national analysis. The large-n rationale for this is reasonable.
- **Reproducibility.** lavaan and blavaan are named, but no code is provided or described in any detail.

## Literature review
About 9% of the main body (pp. 5–7), plus background in the introduction. Breadth is reasonable: Burt on interpretational confounding, three-step bias correction, 2SLS, Bakk and Kuha, Rosseel and Loh, and the Bayesian SEM literature. It is mostly descriptive and chronological. There is a little positioning (2SLS "offers limited help" with confounding; Bayesian two-step work is "relatively rare"), but no critical comparison of the methods' assumptions or results.

## Correctness
- **Tables 4, 5 and 13:** bias and RMSE values of ~10⁻¹⁶ are inconsistent with the s.d. values of ~0.05–0.1 in Tables 6 and 7. The simulation summaries were almost certainly computed wrongly, for example on the averaged estimate or on the wrong object. The text interprets these numbers at face value (pp. 20–22), e.g. joint Bayesian is "the most stable".
- **p. 26:** 100% coverage everywhere is implausible. It is explained away as continuous variables being "less traceable".
- **Table 6, R²ₘ = 0.9, R²ₛ = 0.4, n = 200 row:** reads 0.03250 / 0.03250, which looks like a copy-paste error against the neighbouring rows and Table 7 (0.08776).
- **p. 17:** V₁ and V₂ are swapped in the prose. The "naive" estimator is called V̂₁/n, but eq 18 defines it as V₂.
- **p. 20:** the joint Bayesian positive bias is attributed to the prior, and the growing Bayesian + ML bias with n is attributed to the prior "becoming more pronounced with larger sample sizes". The second claim is backwards: prior influence shrinks as n grows.
- **p. 32:** "In SAM, the structural model is estimated first" should read "measurement model".
- **p. 34:** mcinter and mccoord are both glossed as "Makes work and life interrupt each other". "Australia" should be Austria.
- **pp. 35–36:** confidence-interval width is interpreted as how dispersed respondents' attitudes are. In fact it reflects estimation uncertainty.
- **p. 36:** a spatial-correlation claim is made from a choropleth map with no test.
- **Table 11:** the SAM loadings (e.g. mcclose 1.287) differ more from all four joint fits than the joint fits differ from each other. This is weak evidence of the interpretational confounding it is used to "confirm".

## Writing and presentation
The prose is generally clear and well organised, with a logical flow from the general framework to specific estimators and then to studies. There are some non-native phrasings ("double sword", "the affection by") and occasional typos ("mdoel", "approches", "imparct", "blavvan"). Notation is mostly consistent, with bold vectors.

From the rendered pages:
- The LaTeX typesetting is clean, with numbered equations, booktabs-style tables, and a contents page with lists of figures and tables.
- The density-plot figures (p. 29) have no axis tick labels or scales, so they cannot be read quantitatively.
- The forest plot (p. 36) is legible but small.
- Several tables run over two pages.

Referencing is in APA style with DOIs, and is thorough and consistent.

## Critical reflection
Limited. Section 7.2 lists future work: covariates in the simulation, Bayesian step 2, and informative priors. It does not seriously confront the study's own weaknesses: the anomalous simulation numbers, treating ordinal data as continuous, MCAR, or the single-dataset density comparison. Results are mostly described cell by cell. Where interpretation is offered, it is often speculative or wrong, for example on prior influence, attitude dispersion and spatial effects.

## Strengths
1. A clear, well-structured exposition of joint ML, joint Bayesian (Gibbs) and two-step SAM estimation, including the corrected two-step variance.
2. An ambitious simulation design (27 settings × 5 estimators × 2,000 replications) plus a real cross-national application with a concrete computational-time comparison.
3. A neat, practical idea: propagate step-1 uncertainty by resampling θ₁, using posterior draws in the Bayesian case, and combine with the law of total variance. The s.d. and m(se) results for ML + draws + ML closely track SAM.

## Weaknesses
1. The core simulation results (bias, RMSE, coverage) are numerically implausible, and the student did not notice. This undermines the main comparative conclusions.
2. Little original theory, and the "proposed" method is essentially existing SAM. The Bayesian step-2 variants are proposed and then not implemented.
3. Weak interpretation in the empirical section: confidence intervals read as attitude dispersion, unsupported spatial claims, and ordinal data treated as continuous without discussion. No code is provided.

## Scores (1–5, 5 = exceptional for an MSc)
| Originality | Technical depth | Rigour | Empirical work | Literature review | Writing | Presentation | Critical reflection |
|---|---|---|---|---|---|---|---|
| 3 | 3 | 2 | 2 | 3 | 3 | 4 | 2 |

## Blind grade estimate
**Estimate:** Merit · **Mark:** ~60 · **Confidence:** low

The dissertation looks polished. It has a sound grasp of the SEM and SAM literature and a substantial simulation-plus-application structure, all of which would push it into Merit. But a careful marker would see that the bias and RMSE tables (~10⁻¹⁶) contradict the Monte Carlo s.d. tables, and that 100% coverage is impossible. Those are the central results, and the conclusions rest on them. Together with the misinterpretations in the empirical section, this should keep it well short of Distinction and could pull it towards the Merit/Pass boundary.

## Lessons for a future student
1. Check your simulation outputs against each other before you write them up. RMSE² = bias² + variance, and 95% intervals should cover about 95% of the time. A bias of 10⁻¹⁷ or 100% coverage means a bug, not a finding.
2. If you call a method "proposed", be clear about what is genuinely yours compared with existing work (here, SAM by Rosseel and Loh), and implement every variant you introduce or explain why you dropped it.
3. In applied sections, interpret statistics correctly and cautiously. A confidence interval measures estimation uncertainty, not population heterogeneity. Back up claims such as "spatial effects" with an analysis, and justify modelling shortcuts such as treating ordinal items as continuous.
