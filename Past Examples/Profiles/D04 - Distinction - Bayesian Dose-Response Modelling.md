> **Actual grade:** Distinction · **Source:** `Past Examples/Bayesian Dose-Response Modeling for Toxicology Risk Assessment with Application - Distinction.pdf`
> Profile written blind (the reviewer did not know the grade). The blind estimate below is the reviewer's guess, not the real mark.

# D04: Bayesian Dose-Response Modeling for Toxicology Risk Assessment with Application to Antimony Trioxide
**Length:** 53 pages, ~15,000 words in the main body (excluding references and appendices) · **Area:** Applied Bayesian statistics / environmental health risk assessment (dose-response modelling, BMA, Gaussian processes)
**Structure:** Intro 14% · Lit review 23% · Methods 25% · Results 12% · Discussion 19% · Conclusion 8% (no appendices)

## Research question and project type
How well do three Bayesian approaches (nine parametric dose-response models fitted individually, Bayesian model averaging over them, and a monotone-constrained GP) estimate the whole cancer risk function from sparse quantal toxicology data, and what do they say about antimony trioxide? Each method is checked on one simulated four-dose design (Log-Probit truth) and then applied to the NTP two-year inhalation study in female mice (lung adenoma/carcinoma). The project is applied and computational, with a light methodological framing. Applied work dominates.

## Contribution
Almost all of the methodology is taken from existing work. The nine models and priors come from the U.S. EPA BMDS 2022 guidance and Fang et al. (2015). Marginal likelihoods for BMA come from the off-the-shelf `bridgesampling` R package. The GP's monotonicity device (cumulative sum of exp(f) passed through a logistic link) follows Guha et al. (2013) and Wood and Kohn (1998). The original parts are: (i) putting all three approaches side by side on one dataset; (ii) the first Bayesian analysis of the antimony trioxide NTP data (a frequentist BMD analysis by Schildroth et al. already exists); (iii) a small number of modelling choices, such as Beta(1,1) priors in place of logit-transformed priors and adapted constraints. The claims of a "novel method for conducting BMA" (p.3) and of "the largest number of toxicology-related parametric models fit to a dose-response dataset in the literature" (p.3) are overstated, since Fang et al. (2015) already used BMA with bridge sampling over eight models. **Label:** novel application/data + (weak) systematic comparison.

## Theory
Depth: restates known results. It writes out the BMA posterior and the Bayes-rule model weights (p.17), sketches the bridge-sampling identity and the Meng–Wong optimal bridge function (pp.18–19), states the standard GP conditional mean and covariance (pp.19–20) and gives the BIC formula (p.21). Nothing is derived beyond algebraic rearrangement, and nothing new is proved. The GP section gives the Gaussian-likelihood conditioning formulas and then switches to a binomial likelihood. That mismatch is never reconciled, and nothing explains how the "marginal likelihood" used to optimise hyperparameters was computed under a non-Gaussian likelihood (pp.20–21).

## Empirical and simulation work
- **Real data:** one well-motivated real dataset (Table 1, p.14) with a sensible choice of endpoint and a discussion of early deaths and the Poly3 correction. It has only four dose groups.
- **Simulation design:** weak. It uses one data-generating model and one dose design. Discrete-uniform(−3, 3) noise is added on top of counts that are already binomial draws, which the author admits is ad hoc (pp.13, 34). There are only 10 replicates, and MSE is reported to three decimals with no Monte Carlo error. BIC and the BMA weights come from a single run, and the BMA weights are not recomputed across replicates (pp.25–26).
- **Baselines:** there is no frequentist baseline, even though the motivation is to improve on frequentist BMD practice; the comparison is deferred to "future work" (p.3). The study never computes BMD or BMDL, although these are the regulatory quantities it discusses at length.
- **Robustness:** prior sensitivity is mentioned only in prose ("shape and model ordering remained consistent", p.31), with no results shown. Kernel alternatives were "tried" with pre-built functions but not reported (p.34). There are no leave-one-dose-out analyses, although the author discusses doing them.
- **Uncertainty and diagnostics:** 95% credible intervals throughout, plus a reasonable account of MCMC diagnostics (R-hat, ACF, trace and pairs plots). The Weibull non-convergence is reported honestly (pp.29–30).
- **Reproducibility:** Stan + R and the MCMC settings are stated, but there is no code, no appendix, and no seeds. Initial values were left to defaults, which the author concedes "may result in poor reproducibility" (p.33).

## Literature review
About 23% of the main body (pp.6–12), with fairly broad coverage of Bayesian BMD (Shao, Fang, Wheeler and others), BMA history (Leamer, Madigan–Raftery, Hoeting) and constrained GPs (Riihimäki–Vehtari, Lin–Dunson, Swiler). The review is well organised and occasionally evaluative: it notes, for example, why BMD reparameterisation was not taken up, the problem of degenerate or double-counted models, and Ren et al.'s lack of monotonicity. Mostly, though, it is a chronological, paper-by-paper description, and it does not build a sharp gap that the dissertation then fills. There are minor slips: the heading "Monotinicty", Swiler et al. (2020) listed twice, and Schildroth cited as 2018, 2020 and 2022 inconsistently.

## Correctness
- **Table 3 (p.24) is internally inconsistent.** Under uniform model priors, posterior probability should be proportional to exp(log marginal likelihood). Yet Dichotomous Hill has the largest log-ML (−57.1) and gets posterior 0.016, while Logistic (−80.3) and Probit (−93.8) get 0.326 and 0.213. Table 5 (p.28) is consistent, which suggests a bug or mislabelling in the simulation weights. This undermines the simulation conclusions about BMA (pp.25, 38).
- **The BMA MSE of 0.259 (Table 4) is implausible.** Every component model has an MSE between 0.001 and 0.010. With fixed weights, a weighted average of the component predictions cannot have a squared error larger than the weighted average of the component squared errors (by convexity). The explanation offered (fixed weights across replicates, pp.25–26) cannot produce this, so there is almost certainly an implementation error. Despite this, BMA is the final recommendation (p.40).
- **Credible intervals are misused.** The 95% credible intervals for the mean risk R(d) are repeatedly judged by whether they "capture" observed proportions (pp.25, 28–29, 38–39), with failure treated as a defect of BMA. A posterior predictive interval is needed for that check.
- **The BMA intervals are suspiciously narrow.** In Table 6 (p.38) they are narrower than those of the Log-Probit component, even though BMA is essentially a 76/24 mixture of Log-Logistic and Log-Probit. A mixture of two posteriors that broadly agree should not be tighter than both components, so intervals or quantiles may have been averaged rather than drawn from the mixture.
- **BIC is computed from the maximum log-likelihood over MCMC draws with n = 4 dose groups (p.21).** This is defensible as a rough approximation, but it is not discussed. Log-models at d = 0 (log 0) are not addressed.
- **Some statements are wrong or loose:** "Yi are realizations of the latent function f" (p.20); the prior θ0 ~ N(−3, 3.3) for a parameter constrained to θ0 ≥ 0 (p.16) is odd and unexplained; the MSE formula omits the sum over doses (p.21).
- **The policy conclusions go beyond the evidence (p.39).** The suggestion that reducing exposure from 6 to 2 mg/kg-bw/day "may not be an efficient" use of resources rests on four dose groups, with known survival bias at the top dose.

## Writing and presentation
The prose is fluent, readable and well signposted, with a clear chapter structure, a full table of contents, and lists of figures and tables. The rendered pages show clean LaTeX typesetting. The Summary page (p.vi) is clear and concise. Table 2 (p.16, landscape) is a neat summary of models, priors and constraints. Tables 3 and 4 (p.24) use clean booktabs style. The figures (for example Fig. 5, p.29) are plain ggplot curves with ribbons, with the observed points in blue, but they are untitled beyond the caption, the axes are labelled only "Dose" and "Response" with no units, and one figure has a visual artefact at the lowest dose that the author admits to (p.28). The writing is verbose and repetitive in places: the Discussion recycles results and lists future work at length. The first-person plural "we" and "our future papers" read as if aimed at a journal series. There are a few typos ("antinomy", "Log-Logisitic", "triode", "Archie"). Referencing is author–year and mostly complete, with some inconsistencies.

## Critical reflection
Fairly strong in volume. Chapter 5 (pp.31–37) honestly discusses prior sensitivity, the arbitrary noise model, model-space choice, the Weibull convergence failure, initialisation, the top-dose survival problem, the monotonicity assumption and even the scope for manipulating results. The author also interprets results rather than just reporting them, for example the contrast between the simulation and antimony fits (pp.32–33). The reflection does not reach the most serious problems, though: it explains away the anomalous BMA MSE instead of recognising it as an error, and never notices the Table 3 inconsistency. The final recommendation of BMA, despite BMA performing worst on both reported criteria, rests on its "theoretically desirable qualities" rather than on evidence (p.40).

## Strengths
1. A real, policy-relevant application (antimony trioxide, NTP data) with careful substantive motivation and a thoughtful choice of endpoint.
2. A broad, well-organised literature review spanning toxicology regulation, BMA and constrained GPs.
3. A clear, readable write-up with good tables (notably Table 2), transparent MCMC diagnostics, and an extensive, candid limitations discussion.

## Weaknesses
1. Implementation errors that go undetected: Table 3's weights are inconsistent with its marginal likelihoods, the BMA MSE of 0.259 is impossible, and the BMA intervals are suspiciously narrow. These problems directly undercut the headline comparison.
2. A thin simulation design: one scenario, 10 replicates, ad hoc uniform noise on binomial counts, no Monte Carlo error, no frequentist baseline, and no BMD/BMDL computed.
3. Little original methodology: everything relies on existing models, priors and packages, while novelty is overclaimed. Statistical concepts are shaky in places (credible versus predictive intervals, the GP likelihood and hyperparameter optimisation).

## Scores (1–5, 5 = exceptional for an MSc)
| Originality | Technical depth | Rigour | Empirical work | Literature review | Writing | Presentation | Critical reflection |
|---|---|---|---|---|---|---|---|
| 3 | 2 | 2 | 3 | 4 | 4 | 3 | 3 |

## Blind grade estimate
**Estimate:** Merit · **Mark:** ~63 · **Confidence:** medium
This is a well-written, well-motivated applied project with a solid literature review and an honest limitations chapter, which would push it into the Merit band. However, the statistical core is shaky. A careful marker would spot the inconsistent simulation BMA table, the impossible BMA MSE and the conflation of credible with predictive intervals. Combined with a minimal simulation study, no code and limited technical depth, these problems keep it well short of a Distinction. The fluent presentation probably protects it from dropping into the Pass band.

## Lessons for a future student
1. Sanity-check your own numbers against theory before writing them up. For example, model weights must match the marginal likelihoods, and an averaged predictor cannot be far worse than every component. A result that "surprises" you is more often a bug than a finding.
2. Design simulations properly: use several scenarios, enough replicates, a realistic noise mechanism and Monte Carlo standard errors, and include the standard baseline (here, frequentist BMD) that your motivation promises to improve on.
3. Do not overclaim novelty, and make your recommendation follow from your evidence. If your preferred method performs worst, either explain this convincingly or change the recommendation. Include code or an appendix so that the results can be checked.
