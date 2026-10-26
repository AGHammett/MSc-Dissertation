> **Actual grade:** Merit · **Source:** `Past Examples/The Impact of Residential Moves and and Union Dissolutions on Childrens Educational Attainment - Merit.pdf`
> Profile written blind (the reviewer did not know the grade). The blind estimate below is the reviewer's guess, not the real mark.

# D12: The Impact of Residential Moves and Union Dissolutions on Children's Educational Attainment
**Length:** 49 pages (36 numbered body pages plus front matter, a 3-page appendix and 5 pages of references), ~9,500 words of prose in the main body (~11,700 if you include the tables) · **Area:** Applied social statistics: multilevel and multiprocess event-history models, Bayesian MCMC
**Structure:** Intro 3% · Lit review and methodological background 28% · Data 17% · Methodology 15% · Results (including limitations) 35% · Conclusion 2%

## Research question and project type
Does experiencing the mother's residential moves and union dissolutions lower a child's chance of finishing upper secondary education in Denmark, once selection on unobserved mother-level characteristics is accounted for? The dissertation fits a trivariate multiprocess multilevel model to a subsample of Danish administrative register data (11,532 mothers, 19,790 children). There is a logit for the child's outcome, plus discrete-time event-history logits for the mother's moves and her union dissolutions, with correlated mother-level random effects. It is estimated in JAGS. The project is **applied**, with a modest computational component (coding the stacked joint model in BUGS). There is no theoretical work.

## Contribution
- **Novel application/data.** The data are linked Danish registers, and the union definition is broad, so it includes cohabitation as well as marriage (pp. 12–13). It also models moves and dissolutions *jointly* with the outcome. Earlier work, especially Steele et al. (2009) for Norway, mostly modelled one type of disruption.
- **Modest extension of an existing method.** The framework comes straight from Lillard et al. and Steele et al. (2009). The extension is adding a third process. A comparison of four covariance structures (Models 1–4, pp. 25–29) shows which correlation drives the adjustment, and this is the most interesting analytic contribution.
- The methodology chapter (event-history logit, multilevel random effects, Gibbs sampling) is a summary of textbook and lecture material (Allison; Steele and Washbrook; Browne's MLwiN manual).

## Theory
**Restates known results.** It defines the discrete-time hazard, the multilevel logit and the trivariate random-effects covariance with the implied correlations (pp. 6–8, 19–21), and gives a toy description of Gibbs sampling (p. 9). Nothing is derived. Identification is asserted by citing Brien and Lillard (multiple episodes, p. 8) rather than argued. Exclusion restrictions are not discussed.

## Empirical and simulation work
- **Real data, sizeable and hard to obtain:** a random subsample of the population registers. The author says it "showed no significant deviation" from the population (p. 11) but gives no evidence.
- **Baselines:** Model 1 (independent equations) is the naive baseline. Models 2–4 add correlations step by step, which is a sensible design. A further check that drops one set of disruption indicators is reported in words only (p. 30).
- **Model selection** is informal (pp. 24–25). Heterogeneity by age, gender and region, and interactions and move distance, were "explored" but dropped for lack of "substantial evidence". No DIC/WAIC or other criterion and no numbers are given.
- **Uncertainty:** posterior means with 95% credible intervals throughout. MCMC is short: 2 chains × 4,000 iterations with 2,000 burn-in. Gelman–Rubin is "close to 1" but not tabulated. No effective sample sizes are given. The trace plot for σ²_u(E) (Appendix A, p. 37) shows strong autocorrelation and slow mixing, which the text calls "adequate". It is stable across starting values (p. 27).
- **No simulation study** to check that the joint model recovers selection parameters with such small clusters (1.72 children per mother).
- **Reproducibility:** partial. JAGS model and R call snippets are in Appendix B, but the code is not complete (the variable lists are elided) and the data are confidential. There is no repository.

## Literature review
About 28% of the body, including ~1,500 words of method background. The substantive review (pp. 2–5) covers moves, divorce, remarriage and identification strategies (PSM, natural experiments, IV), with ~40 references. It is mostly descriptive, but there is some critical framing: why PSM and IV fall short here, motivating the multiprocess approach. The methods section is exposition rather than review. There is a citation slip: on p. 8, Steele et al. (2013), a paper on employment and mental health, is described as the study of marital dissolution and children's education, which is actually Steele et al. (2009).

## Correctness
- **The headline finding is contradicted by the author's own results.** The Summary (p. iv) and Conclusion (p. 36) say residential moves have the "more substantial" naive effect. Table 5 and the text on p. 27 show union dissolutions have the stronger effect.
- **Table errors.** In Table 6 (p. 29) the "4 moves" row has the mean outside its own CI (−0.16 with (−0.135; 0.207), and −0.18 with (−0.147; 0.210)). The p. 28 text calls the evidence for 3 and 5+ moves "weak" in a way that does not quite match Table 5. The captions of Tables 7 and 8 say "model 1 and model 4" but only Model 4 is shown. Model 1's random-effect variances are discussed (p. 26) but never tabulated.
- **Duplicate and inconsistent descriptive tables.** Table 2 (p. 17) repeats Table 1 with raw, garbled variable names, and gives "parents never married" as 6.1% against 9.10% in Table 1.
- **Prior misstated.** On pp. 21–22, N(0, 0.001) is described as "variance 0.001, representing a non-informative prior". In JAGS the second argument is a precision, and a variance of 0.001 would be highly informative.
- **Loose Bayesian statements.** It claims "the Bayesian framework makes no assumptions about the distribution of the parameters" (p. 10), and says that in latent-variable Gibbs sampling "y_i is updated" (p. 9), although y is observed data.
- **Problems with the ρ(M,U) = 0.92 correlation.** It is very high (p. 27), and the author rightly suspects it is an artefact of unions being defined by shared address. The rebuttal relies on a Statistics Denmark claim that the mother is "only slightly more likely" to move, which sits awkwardly with p. 2's statement that children move with the mother in 80% of cases.
- A "(cite)" placeholder is left in the text (p. 27). The notation in eq. (3) is inconsistent (v_j vs u_j, α^M D^U, stray (p) superscripts, p. 20).
- Disruptions are counted over the child's whole life to age 18. The timing and age of exposure are acknowledged but not modelled.

## Writing and presentation
The structure is clear and the LaTeX layout is clean. The rendered pages show a well-typeset title page, a neat covariance-matrix page (p. 21) and booktabs-style results tables with bold credible intervals (p. 26). Appendix trace plots are legible. There are only four figures, and two are simple diagrams or histograms. There are no coefficient plots, and results appear only as tables. The prose is readable but has a fair number of typos ("sinificant", "adressed", "regressison", "naother", "resdiential", "estimtion"). The introduction's roadmap omits the conclusion chapter. The conclusion is very short (~240 words). Referencing is APA-style and mostly consistent.

## Critical reflection
Good for an applied MSc. Section 5.6 (pp. 32–35) honestly discusses time-varying unobservables, child-specific unobservables, the omitted father's household, endogenous covariates, thin within-mother variation and data limitations. The author interprets results substantively: the selection direction, why the moves equation carries more information than the unions one, and a comparison with Steele et al. (2009). The suspicious 0.92 correlation is flagged rather than ignored. But some defences end in "not a major concern" without evidence, and the short MCMC run and informal model selection are not reflected on.

## Strengths
1. A real, large administrative dataset with careful construction of the event-history episodes and a well-motivated broad definition of unions (pp. 11–13).
2. The step-by-step covariance-structure comparison (Models 1–4) gives an interpretable story about which selection channel matters. Its main finding is that adjusting via the moves equation shrinks both disruption effects.
3. A thoughtful, honest discussion of threats to identification (Section 5.6) and good links to the domain literature.

## Weaknesses
1. Careless errors in the results: the abstract and conclusion contradict the tables, means fall outside their CIs, a garbled duplicate table, a "(cite)" placeholder, and wrong captions.
2. Thin statistical rigour around estimation: short chains with visible autocorrelation, no ESS, no formal model comparison, prior precision misdescribed, and no simulation or sensitivity check on identification with ~1.7 children per mother.
3. Little original methodological depth. The method is reproduced from the supervisor's published framework, the method background is textbook exposition, and the conclusion is underdeveloped.

## Scores (1–5, 5 = exceptional for an MSc)
| Originality | Technical depth | Rigour | Empirical work | Literature review | Writing | Presentation | Critical reflection |
|---|---|---|---|---|---|---|---|
| 3 | 3 | 2 | 4 | 3 | 3 | 3 | 4 |

## Blind grade estimate
**Estimate:** Merit · **Mark:** ~64 · **Confidence:** medium
Ambitious real-data work points towards the upper Merit band: a three-process joint Bayesian model on Danish registers, with a sensible comparative design and honest limitations. A sharp-eyed marker will be held back by the visible sloppiness: the abstract contradicts the results, there are internal table inconsistencies, the prior is misstated, and the MCMC diagnostics are thin. Without those, this could have reached the Distinction boundary.

## Lessons for a future student
1. Check that every claim in the abstract and conclusion is backed by a number in your tables. Then audit the tables themselves (CIs contain means, captions match contents, no leftover "(cite)" or raw variable names). These errors are cheap to fix and costly to leave.
2. If you fit a complex MCMC model, report the diagnostics properly: R-hat and ESS tables, longer chains when the trace plots show autocorrelation, and state correctly what your priors mean in the software's parameterisation.
3. Make model selection explicit and quantitative (DIC/WAIC, or a table of the alternatives you tried). "Explored but found no evidence" is not convincing without numbers. A small simulation showing that your identification strategy works at your cluster sizes would add real rigour.
