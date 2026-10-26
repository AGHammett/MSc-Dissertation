> **Actual grade:** Merit · **Source:** `Past Examples/The Interplay of Intelligence and Education in British Social Class Mobility Insights from Mediation Analysis of Four Categorical Variables - Merit.pdf`
> Profile written blind (the reviewer did not know the grade). The blind estimate below is the reviewer's guess, not the real mark.

# D13: The Interplay of Intelligence and Education in British Social Class Mobility: Insights from Mediation Analysis of Four Categorical Variables
**Length:** 47 pages, ~10,500 words in the main body (excluding references and appendices; about 11,400 if you count table and equation text) · **Area:** Categorical data analysis / mediation analysis applied to social mobility (sociology, using British birth cohort data)
**Structure:** Intro 11% · Data and variables 8% · Methodology (half of it literature review) 33% · Simulation 5% · Empirical analysis 39% · Conclusion 3%

## Research question and project type
How much of the association between class of origin (X) and class of destination (Y) in the 1946, 1958 and 1970 British birth cohorts runs through childhood IQ (M1) and education (M2), on their own and in sequence? The approach extends Kuha, Bukodi and Goldthorpe's (2021) association-based mediation framework for categorical variables (one mediator, education) to two mediators, fitting multinomial logistic models and summarising effects with 441 log odds ratios per table. The project is applied with a light methodological element. The applied side dominates.

## Contribution
- **Reproduced or explained:** the single-mediator framework (equations 1–3, the reference distribution P0, log odds ratio summaries); the ratio-of-indirect-to-total analysis; the bootstrap CIs; and the second-stage linear regression of ratios on white-collar, inheritance and hierarchy indicators (Section 5.3). All of these follow Kuha et al. (2021) closely, including the variable definitions.
- **Original:** (i) adding IQ, merged in by individual ID, as a second categorical mediator (cut into quintiles); (ii) writing down indirect-effect formulas for the X→M1→Y, X→M2→Y and "X→M1→M2→Y" paths (equations 6–8) and a direct effect (equation 10). The thesis calls this "the principal contribution" (p.11), but each formula is a direct substitution into the Kuha template. Nothing is derived or proved about the formulas (identification, decomposition, properties). (iii) Breakdowns by cohort and gender for the new mediator.
- **Label:** novel application/data (main), with a small modified method (an extension to two mediators by analogy).

## Theory
Depth: restates known results. Chapter 3 (pp.8–17) surveys counterfactual mediation (Daniel et al. 2015, with the NDE/NIE decomposition for two ordered mediators, p.12) and Kuha's associational definitions, then *defines* the four-variable quantities (pp.13–16) without derivation. The multinomial logit (equations 12–14, pp.16–17) is textbook material. Appendix C (pp.38–39) swaps sums for integrals for a continuous IQ, a notational change that is never estimated. No proofs, and no formal argument that the new quantities mean what they are claimed to mean.

## Empirical and simulation work
- **Real data:** three NSHD/NCDS/BCS70 cohorts, 7×7 class tables, analysed for the whole cohort and by gender. Tables of fitted "total" and "indirect" probabilities (Table 2, Appendix A), 21 diagonal log ORs plotted by path and gender (Figs 6 and 8), ratio summaries with bootstrap percentile intervals (Fig 7, Table 3), and 18 second-stage regressions (Tables 4–6).
- **Simulation (pp.18–20):** very weak. X, M1, M2 and Y are drawn independently and uniformly, so every effect is null. The simulation only shows that estimated probabilities sit near 1/7 and log ORs near 0. It cannot check that the path-specific formulas recover non-zero indirect effects, yet it is described as having "reinforced the robustness of the model and the accuracy of its predictions".
- **Missing data:** IQ is missing for 33.6% of cases (44.6% in 1958). The analysis is complete-case and never discusses whether the missingness is related to class.
- **Uncertainty:** bootstrap with 1,000 resamples (Appendix B) and a Wald-test filter at p<0.1. No baselines or robustness checks: the IQ cut-points and the reference distribution are not varied, and the reference distribution is justified only by citing Kuha.
- **Reproducibility:** the thesis mentions "nested for loops in R", but the plots look like matplotlib. No code is provided or linked.

## Literature review
Spread across the Introduction (~1.5 pages on IQ, education and mobility) and the first half of Chapter 3 (~4 pages on mediation methods): roughly 15–18% in total. The breadth is reasonable (Bukodi & Goldthorpe, Deary, Forrest, Connelly & Gayle, Daniel, VanderWeele, Imai, Steen). The review is mostly descriptive ("X did Y"). There are some errors and oddities: Niles (1922) is credited with introducing path coefficients (that was Wright) and is cited before Galton (1889) "further developed" mediators (p.8); "Vemuri (2015)" is a book review of Imbens & Rubin, cited as if it were a source of methods (p.9); the law of total expectation is called the "Power Property" (p.12).

## Correctness
- **Sequential path conflated (eq. 8, p.15):** the "X→M1→M2→Y" effect uses the marginal P(M2|X=x) = Σ P(M2|m1,x)P(m1|x), which includes the direct X→M2 path as well as X→M1→M2 (the text admits "path a+b+c"). So it is really the total effect through M2. Its being the largest effect is therefore partly built in, and the conclusion that IQ has a "facilitative effect on educational attainment" (p.34) does not follow.
- **Table 3 counts (p.29):** the number of significant log ORs is identical in all three cohorts (88/100/115), and identical for men and women (168/169/179). The counts also differ by path, even though the filter applies to the total log OR, which is the same for every path. This looks like a tabulation error.
- **"Below 50%" claim:** the text says the maximum contribution does not exceed 50% (p.31; also the abstract). Table 3 shows 95th percentiles of 0.56–0.62 for IE3, and Fig 7 shows upper limits above 0.7.
- **Implausible values:** women in 1946 are said to have "total ORs above 10" for "2 vs 5" and "4 vs 7" (p.26). This is not checked, and probably reflects sparse cells.
- **Overstated significance:** in Tables 4–6 the 441 ratios are highly dependent, yet many coefficients carry "***, p≈0". The significance codes themselves are non-standard (* means p<0.01, · means p<0.05).
- **Untested comparisons:** "significantly higher" claims about IQ means across cohorts (p.28) and gender gaps are made without tests. IQ was standardised, so differences in cohort means mostly reflect sample composition. Reading quintile shares as men having "lower cognitive development" (p.7) is careless.
- **Unused quantity:** the direct effect is defined (equation 10) but never estimated.
- **Wrong cross-reference:** p.3 says the associations are defined "in Section 5"; they are in Section 3.

## Writing and presentation
- **Rendered pages:** a LaTeX document with a clean LSE-crest title page and a clear table of contents and list of figures. Equations are typeset properly but awkwardly broken across lines (p.14). The results figures (p.25) are default matplotlib scatter plots with small axis labels and readable legends, plus italic captions. Fig 7 (p.28) is small and dense. The regression tables (p.31) use booktabs and look tidy.
- **Prose:** generally readable, with grammatical slips ("The educational qualifications is provided", "classifictions", "zrelate", "between between", "X1 → M2 → Y" in the Table 3 note).
- **Interpretation passages:** these lean towards long runs of numbers (pp.26–27).
- **Referencing:** author–year and consistent, though some entries are lower-cased ("b ritain").

## Critical reflection
Limited. The conclusion lists four future directions: continuous IQ, multiple imputation, more mediators, later cohorts. It does not engage with the substantive weaknesses: complete-case bias, the arbitrary quintile cut, the meaning of the sequential path, the non-additivity of the effects, or causal confounding of IQ. The results are partly interpreted (hierarchy and inheritance effects, gender patterns), but often simply read off the tables. Some interpretations go beyond the evidence, for example IQ's growing importance for women.

## Strengths
1. A genuinely interesting substantive extension: adding childhood IQ to the established education-mediation analysis of British mobility, with data linked across three cohorts.
2. A complete, coherent pipeline that mirrors a published AoAS framework: fitted probability tables, diagonal log ORs, bootstrap ratio intervals, and second-stage regressions on mobility-type indicators.
3. Breakdowns by cohort and gender, with plenty of tables and figures and a clear organisational outline.

## Weaknesses
1. The methodological "contribution" is formula substitution with no derivation or validation. The sequential-path definition actually captures all mediation through education, so the headline ranking of paths is partly an artefact.
2. The simulation study is trivial: an all-null, independent uniform design that cannot test whether the path effects are recovered. There are also internal inconsistencies (Table 3 counts, the "<50%" claim against the CIs).
3. Complete-case analysis with 33–45% missing IQ and no sensitivity analysis. Significance is overstated in the second-stage regressions, and the reflection on limitations is thin.

## Scores (1–5, 5 = exceptional for an MSc)
| Originality | Technical depth | Rigour | Empirical work | Literature review | Writing | Presentation | Critical reflection |
|---|---|---|---|---|---|---|---|
| 3 | 2 | 2 | 3 | 3 | 3 | 3 | 2 |

## Blind grade estimate
**Estimate:** Merit · **Mark:** ~63 · **Confidence:** medium
This is a competent, well-scoped applied project that sensibly extends a supervisor-style published framework to a new mediator, using real cohort data and a full analysis pipeline. That puts it solidly in Merit territory. It falls short of Distinction because the methodological extension is shallow and partly mis-specified (the sequential path), the simulation validates nothing meaningful, and there are internal numerical inconsistencies, unaddressed missing data and overclaimed significance. A lenient marker who values the data linkage and the volume of output could push it to the high 60s.

## Lessons for a future student
1. If you claim a new estimand or extension as your contribution, show it works: derive its properties, or simulate from a data-generating process with *known non-zero* effects and check you recover them. A null simulation only shows your code produces zeros.
2. Check every path definition against what it actually conditions on or marginalises over, and make sure each headline interpretation follows from the estimand rather than from how it was constructed.
3. Cross-check your tables against your text (counts, maxima, CIs) and handle substantial missingness explicitly, at minimum with a sensitivity analysis. Examiners notice inconsistencies quickly.
