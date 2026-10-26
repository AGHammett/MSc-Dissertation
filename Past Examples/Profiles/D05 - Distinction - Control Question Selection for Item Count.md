> **Actual grade:** Distinction · **Source:** `Past Examples/Control Question Selection for the Item Count Method - Distinction.pdf`
> Profile written blind (the reviewer did not know the grade). The blind estimate below is the reviewer's guess, not the real mark.

# D05: Control Question Selection for the Item Count Method
**Length:** 53 pages (41 numbered main-body pages plus front matter, references and 4 appendix pages), ~16,000–17,000 words in the main body (excluding references and appendices; raw extraction gives ~18,700, inflated by tables and equation fragments) · **Area:** Survey methodology / sensitive questions; missing-data likelihood (EM) for list experiments
**Structure:** Intro 15% · ICM method and EM estimation (exposition) 22% · Control-question design and tests 8% · Data (FIDUCIA survey) 5% · Point-estimate results 12% · Item count regression 12% · SEs (analytic vs bootstrap) and control distributions 11% · National estimates 8% · Conclusions 7%

## Research question and project type
Does using control items that are thematically *unrelated* to the sensitive item (illegal downloading of music/TV/films) make the control count Z independent of the sensitive answer Y, which would make EM estimation more efficient, compared with a thematically *related* list? And do the two lists give different prevalence estimates? It uses an existing split-ballot item count experiment in the FIDUCIA survey (UK and Bulgaria, 2014–15, n ≈ 1,940). The project is **applied, with a methodological framing**. The applied side dominates: the work is fitting and testing a published method (Kuha & Jackson 2014) on real data. There is a modest computational element (own R implementation of EM with analytic information matrix, a pooled two-list estimator, and a bootstrap).

## Contribution
- **Original:** the comparison of related and unrelated control lists, using a randomised split-ballot design that, by the author's account, has not been analysed for this purpose before. The author also writes a new R function for pooled estimation across the two lists (shared π_y, list-specific multinomial control models, p. 24). Tests are LR tests of Y* in the control model and Wald tests of π̂_y differences. Further original work: regression with age, conditional-independence tests, a country split, and a bootstrap vs analytic SE comparison.
- **Reproduced/explained:** all of Chapter 2 (moment estimator, pseudo-data EM, multinomial control model, Oakes/Kuha–Jackson information matrix, eqs 1–15) is restated from Kuha & Jackson (2014). The author says so explicitly (p. 7). The rationale for thematic unrelatedness is also taken from Kuha & Jackson.
- **Label:** novel application/data + systematic comparison (two list designs, three control distributions, two variance methods). There is no new method beyond the pooled-estimator adaptation.

## Theory
Depth: **restates known results**. Pages 7–14 set out the EM framework carefully, in consistent notation, including the full observed-information-matrix expressions (eqs 11–15, p. 12–13). Nothing is derived from first principles and nothing new is proved. The weighted-moment estimator in Appendix 3 (eq. 18) is a trivial extension. Section 9 (p. 41) gives a verbal sketch of pseudo-likelihood with survey weights but does not develop it.

## Empirical and simulation work
- **Real data only; no simulation.** A simulation would have been the natural way to check power, or how efficiently the two designs perform under known dependence, but none is done.
- **Design:** a clean randomised 2×2 comparison (list A/B × treatment/control). The analysis builds up sensibly: moment estimator → EM independent/dependent → pooled → regression on age → conditional independence → country split.
- **Baselines/robustness:** compares the moment estimator with EM (Table 4). Checks multinomial against binomial and beta-binomial control models using the `list` package (Tables 11–12). Compares analytic and bootstrap SEs (500 reps, Tables 9–10). Weighted moment estimates in Appendix 3. A reasonable range of checks.
- **Uncertainty:** SEs throughout, Wald and LR tests, AIC. There is no formal power or equivalence analysis, although the main claim is a null result.
- **Problems spotted:** separation (SEs of 179, 634 and 842) is noticed and discussed. There is no remedy (e.g. penalised/Firth or Bayesian priors, or collapsing categories).
- **Reproducibility:** the R code is linked via a hyperlink ("code download", p. 14 and p. 20). An AI-use statement is given (Appendix 1).

## Literature review
There is no separate chapter. The literature is woven into the Intro (~15%) and Ch. 3. It covers randomised response (Warner), the origins of the ICM (Miller), Imai, Blair & Imai, Glynn, Kuha & Jackson, Tourangeau & Yan, and meta-analyses. It is adequate and on point but narrow: ~37 references, and heavily dependent on Kuha & Jackson, which is cited on nearly every paragraph of Ch. 2. It is mostly descriptive. The one critical thread is the tension between efficiency and the "weirdness factor", which the author sets up well as the motivation (p. 4–5, 16).

## Correctness
- **Odds-ratio misinterpretation (p. 36):** UK coefficients of −2.03 to −2.17 are said to mean UK odds are "between 42% and 57%" of Bulgaria's. In fact exp(−2.03) ≈ 0.13 and exp(−2.17) ≈ 0.11, so the odds are about 11–13%.
- **Wald formula (eq. 16, p. 17):** the denominator uses squared variances, var(π̂)², which is wrong. The reported p-values look consistent with the correct formula, so this is a typo.
- **Text/table swap (p. 22–23):** the text attributes the −0.051 difference (p = 0.847) to the dependent models, but Table 3 has −0.051 for the independent models (p = 0.494) and 0.026 for the dependent ones. The AIC values in the text and in Table 7 are similarly swapped (p. 28).
- **Inconsistent SEs:** Table 12 reports a List B dependent 65+ SE of 1.43, while Table 6 gives 842.09 for the same model (p. 35 vs p. 27).
- **Country results don't cohere (p. 36–38):** the country coefficient is "highly significant", yet the Wald test of the UK vs Bulgaria difference gives p = 0.06–0.45. The pooled UK estimate (0.145) lies below both list-specific UK estimates (0.194, 0.203), and the Table 13 intercept implies a UK prevalence of about 6%. None of this is reconciled.
- **Overclaiming from a null (p. 25, 39–41):** a non-significant difference is read as "strong evidence" that the lists are equivalent and "similarly efficient". The thesis then recommends defaulting to related lists. This rests on one item, one survey and no power analysis. Efficiency is never compared directly through the SEs: in the dependent models list B's SE is 0.110 against list A's 0.076, which is evidence that is not discussed.
- **Bootstrap conclusion is shaky (p. 33):** the nonparametric bootstrap blows up when Y* is included, and from this the author concludes that analytic SEs are "more stable under misspecification". But the dependent model is overparameterised and weakly identified, not misspecified. Analytic SEs of 36 and 179 are hardly a sign of stability.
- "p < 0.000" (Table 4 discussion, p. 24). Sloppy notation in eqs 4–5, where p̂_s is conditioned on Y rather than on t.

## Writing and presentation
The prose is clear, fluent and well signposted. Each section opens by recalling its purpose, and the argument is easy to follow. In places it is repetitive and wordy: Kuha & Jackson is cited almost every sentence in Ch. 2, and the "weirdness factor" argument is repeated three times. American spelling throughout. There are a fair number of typos ("overerporting", "Second 3", "Do to so", "ana analytic", "There findings", "coefficinets").

The rendered pages show a clean LaTeX layout: a standard title page, nicely typeset booktabs-style tables with notes (Table 3, Table 6), and well-set block-matrix maths (p. 13). There are **no plots at all**. Every result is a table, and the only figures are screenshots of the questionnaire and of the survey vendors' descriptive tables. Some tables are oddly laid out: Table 6 has a narrow left-aligned panel above a wide one, and Table 2's π̂_y column sits on the "Y = 0" row. Referencing is consistent APA with DOIs.

## Critical reflection
It is reasonably good. The conclusion discusses single-item generalisability, location-specific results, the lack of survey weights (with an appendix check), and future designs such as a pilot survey to select uncorrelated controls. The results are interpreted rather than just reported: the reasons behind separation, the divergence between the moment and EM estimates, and the inadequacy of the binomial model are all explained. However, it does not reflect on statistical power or on "absence of evidence ≠ evidence of absence". This is the most important limitation for its headline claim, and the thesis instead strengthens that claim in the final paragraph.

## Strengths
1. A clear, well-motivated substantive question with a genuinely suitable randomised split-ballot design. The tension between efficiency and the weirdness factor is well framed.
2. A competent own implementation of Kuha–Jackson EM, with analytic information-matrix SEs, extended to a pooled two-list estimator and checked against the `list` package and a bootstrap.
3. A broad set of robustness analyses (control distributions, variance methods, covariate-conditional independence, country splits, weights), with the code linked.

## Weaknesses
1. Theory is entirely restated, and the methodological novelty is thin. A quarter of the text reproduces a single paper's equations.
2. The headline conclusion overreaches from a non-significant result. There is no power, equivalence or simulation study, and efficiency is never compared directly through the SEs.
3. Several numerical/interpretive errors and inconsistencies: the odds-ratio misreading, swapped table and text values, an inconsistent SE in Table 12, incoherent country estimates, and a questionable bootstrap conclusion. Together they suggest the late stages were not proof-checked.

## Scores (1–5, 5 = exceptional for an MSc)
| Originality | Technical depth | Rigour | Empirical work | Literature review | Writing | Presentation | Critical reflection |
|---|---|---|---|---|---|---|---|
| 3 | 3 | 2 | 4 | 3 | 4 | 3 | 3 |

## Blind grade estimate
**Estimate:** Merit · **Mark:** ~66 · **Confidence:** low–medium

The thesis is a solid, well-written applied analysis with a real research question, real experimental data, its own estimation code and a good range of robustness checks. That clearly puts it in the Merit band and could push it towards 70. What holds it back is the lack of technical contribution beyond a faithful restatement of Kuha & Jackson, an overconfident reading of a null result, and a cluster of avoidable numerical and interpretive slips (especially in Ch. 8). A marker who values the substantive design and the breadth of analysis might award a low Distinction.

## Lessons for a future student
1. If your headline finding is "no difference", support it explicitly: give a power calculation, an equivalence test, or a small simulation showing what difference you could have detected. Otherwise "not significant" will be read as weak evidence, not "strong evidence".
2. Proof-check every number in the text against its table, and sanity-check interpretations (exp(β) for odds ratios, whether pooled estimates sit between their components). A handful of such slips undermines trust in otherwise careful work.
3. Keep the restatement of an existing method short. Cite the equations you need, and spend the space you save on something of your own: an extension, a simulation, or a diagnostic plot. Figures would also have made this thesis' results far more digestible than 16 tables.
