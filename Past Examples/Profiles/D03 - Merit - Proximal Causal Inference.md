> **Actual grade:** Merit · **Source:** `Past Examples/A Proximal Causal Inference approach to study the influence of Proxy-Confounder Associations on Treatment Effects - Merit.pdf`
> Profile written blind (the reviewer did not know the grade). The blind estimate below is the reviewer's guess, not the real mark.

# D03: A Proximal Causal Inference approach to study the influence of Proxy-Confounder Associations on Treatment Effects
**Length:** 52 pages (5 front matter + 47 numbered), ~13,500 words in the main body (excluding references; there are no appendices) · **Area:** Causal inference (proximal causal inference / negative controls), simulation study
**Structure:** Intro 6% · Lit review 8% · Data 10% · Empirical approach 7% · Continuous-proxy simulations 38% · Binary-proxy simulations 28% · Conclusion 3%

## Research question and project type
The project asks how strongly the treatment proxy Z and the outcome proxy W must be associated with an unmeasured confounder U for the two-stage regression-based proximal causal inference (PCI) estimator of Liu, Park, Li and Tchetgen Tchetgen (2024) to give reliable average causal effect estimates. It also asks how this changes with noise in Z and with Z being continuous or binary. The data are a European Quality of Life Survey extract: cost barriers to seeing a doctor (A), mental well-being (Y), household economic situation (U). Because the real variables violate the PCI assumptions (p. 13), everything is simulated from coefficients fitted to the real data. This is a **computational/simulation study** with a thin applied wrapper. Simulation dominates.

## Contribution
- **Original:** a grid-based sensitivity study. It varies the Z–U coefficient (7 levels), the W–U coefficient (7 levels), the noise SD in Z (0.5, 1, 2.5, 5), and the binarisation of Z (75th or 25th percentile). It reports single-run tables (Tables 5.1–5.8) and 20-replicate strip plots (Figs 5.1–6.8), then condenses them into "minimum W–U threshold" tables (Tables 5.9, 6.1).
- **Reproduced:** the PCI assumptions, the DAGs and the two-stage GLM procedure, all taken from Tchetgen Tchetgen et al. (2020) and Liu et al. (2024) (pp. 3–6). Figures 2.1 and 2.2 appear to be lifted from those sources.
- The "novel application to social science data" is mostly nominal: the real data only supply simulation coefficients.
- Label: **systematic comparison** (a simulation sensitivity analysis), with an element of **novel application/data** in name only.

## Theory
**Restates known results.** The only formal content is the three conditional independence assumptions (eqs 2.1–2.3, p. 4) and a verbal two-step description of the estimator (p. 5). The estimator is never written out, there is no identification argument, and the dissertation never explains *why* weak proxies make estimates blow up. That is a weak-instrument-type phenomenon: the first-stage relevance condition fails. Making that link would have given the results a theoretical spine.

## Empirical and simulation work
- **Design:** a reasonable factorial idea. Execution is weak:
  - Tables 5.1–5.8 interpret single Monte Carlo draws cell by cell (p. 19 admits this).
  - The plots use only 20 replications.
  - There are no summary metrics such as bias, RMSE, empirical SE, coverage or Monte Carlo error. "Reliable" means eyeballing whether estimates fall in a 24–28 band (p. 19), which is then "relaxed".
  - Plots have fixed y-limits that silently drop extreme points (pp. 19, 21). The author admits this makes some cases look better than they are.
- **Real versus simulated:** real data are used only for descriptive boxplots (pp. 8–12) and to calibrate coefficients. The true effect (27.02) comes from regressing simulated Y on simulated A and U (p. 13).
- **Baselines:** there is no naive (unadjusted) estimator to show how much PCI actually de-biases, and no comparison with other PCI estimators.
- **Robustness:** a second design (Z–U decreasing, W–U increasing; §5.2) is called a check, but it is the same grid read in a different order.
- **Uncertainty:** none, apart from one CI for the true effect.
- **Reproducibility:** one line of R code (p. 13) and verbal descriptions. No code appendix or repository, and no seeds.

## Literature review
About 4 pages (~8%) and 8 references, all from the Tchetgen Tchetgen group or the negative-control literature. It is **descriptive**. It summarises the PCI framework and assumptions but does not engage critically. It misses obvious neighbours: weak-instrument and IV literature, sensitivity analysis for unmeasured confounding, measurement-error proxies, and other PCI estimators such as the doubly robust or kernel methods. It describes an arXiv paper as "bioRxiv". In-text citations list every author's full name ("Jiewen Liu, Chan Park, Kendrick Li, and Eric J. Tchetgen Tchetgen (2024)"), which is non-standard.

## Correctness
- **Practical advice confuses Monte Carlo variability with what an analyst can do (pp. 20, 22, 23, 28, 36–43).** The recommendation to "obtain at least 5 [or 7] estimates of beta and use the median" is repeated throughout. A researcher with one real dataset cannot redraw the data. This is a conceptual error that runs through the whole results discussion.
- **PCI bias dismissed (p. 14).** The PCI estimate of 25.48 lies far outside the true-effect 95% CI (26.995, 27.036). This bias is waved away because "an increase of 25 units or 30 units does not make much of a difference". It is not investigated, even though it comes from a single realisation.
- **"Association" is not on comparable scales.** It means a log-odds coefficient for binary W but a linear coefficient for continuous Z, with no intercepts used (p. 16). Comparing Z–U strengths across noise SDs ignores signal-to-noise. The headline thresholds (e.g. "W–U > 0.75 works for any Z with SD ≤ 1", p. 46) are therefore specific to the design and eyeballed.
- **"Robust to more 0s or 1s" (p. 44) is overstated.** Table 6.1 shows the thresholds differ between the two cases in most rows.
- **Reasoning:** the claim that the real data violate the assumptions "obviously" (p. 13) is asserted with little evidence. Saying the CI is tight "because" other variables are absent (p. 14) is muddled reasoning.
- **Labelling errors:**
  - "true causal effect of A on Z" (p. 13) should be A on Y.
  - "treatment proxy (U)" (p. 14).
  - The Fig 3.4 caption says "Outcome Proxy Z".
  - The Fig 6.4 caption says SD = 2.5 but the figure shows SD = 5.
  - The Table 5.8 caption says SD = 0.5 but the table shows SD = 5.
  - "Table X" appears on p. 18.

## Writing and presentation
- **Typesetting:** LaTeX, with clean title, contents and lists of figures and tables. Rendered p. 4 is tidy: the DAG figure and displayed equations are properly numbered. Rendered p. 21 shows a ggplot strip chart of 20 replicates per W–U level, faceted by Z–U level. The legend ("zv Value") and axis labels ("wv", "Beta Coefficient") are raw variable names, and the caption is generic.
- **Prose:** clear enough sentence by sentence, but very repetitive. Sections 5–6 (about two-thirds of the body) are a long cell-by-cell narration of plots with the same phrasing ("robust", "highly variable and unreliable", "if the researcher does not mind slightly biased estimates") rather than synthesis.
- **Encoding and typos:** "¿" and "¡" appear in place of > and < (pp. 21, 35). Other typos include "metal well-being", "defers from", "casual effect" and "guaranties".
- **Notation and terminology:** notation is light but inconsistent. The text says "Graph 5.1" while the captions say "Figure". There is no abstract-style quantitative summary beyond the Summary page.

## Critical reflection
Limited. The conclusion lists three limitations (pp. 46): only binary and continuous proxies, thresholds may not transfer, and GLM adequacy. These are generic. The real methodological limitations are not acknowledged: few replications, no performance metrics, single-run tables, eyeballed thresholds, and clipped plots. The dissertation does interpret results, through the trade-off that a weaker or noisier Z needs a stronger W. But much of the "interpretation" is speculative practical advice rather than analysis of why the patterns occur.

## Strengths
1. A clear, well-defined question about a very recent method (2024), with a sensible factorial grid over proxy strength, proxy noise and proxy type.
2. Calibrating the simulation to real survey data is a reasonable idea, and the trade-off finding (stronger W compensates for weaker or noisier Z) is plausible and clearly stated in summary Tables 5.9 and 6.1.
3. Competent LaTeX layout, a correctly stated set of PCI assumptions with DAGs, and an easy-to-follow overall structure.

## Weaknesses
1. Statistically thin simulation methodology: single-draw tables, 20 replicates, no bias/RMSE/coverage, eyeballed "reliable" bands, and plots clipped at fixed limits.
2. No theoretical engagement: the estimator is never written down and there is no explanation (e.g. weak relevance) for the instability. The literature review is short and descriptive.
3. A recurring conceptual error ("take the median of 5–7 estimates") and dismissal of the PCI estimator's bias. On top of this there are many caption, labelling and typo errors, and long repetitive narration in place of synthesis.

## Scores (1–5, 5 = exceptional for an MSc)
| Originality | Technical depth | Rigour | Empirical work | Literature review | Writing | Presentation | Critical reflection |
|---|---|---|---|---|---|---|---|
| 2 | 1 | 2 | 2 | 2 | 2 | 3 | 2 |

## Blind grade estimate
**Estimate:** Pass · **Mark:** ~56 · **Confidence:** medium
The project is coherent and complete, and it addresses a genuine, current question, which keeps it safely above a fail. But it has almost no theory, only a descriptive literature review, and an informal simulation analysis with no performance metrics or Monte Carlo uncertainty. It also misreads what its own replications mean in practice (the median-of-estimates advice). If a marker valued the topical choice and the volume of simulation work, it might reach a low Merit (~60). It falls well short of Distinction.

## Lessons for a future student
1. **Run simulations properly.** Use enough replications (hundreds or more). Report bias, empirical SE, RMSE and coverage with Monte Carlo error, and summarise in compact tables or plots instead of narrating single draws cell by cell.
2. **Write the estimator down and explain your results theoretically.** A short derivation of why weak proxies cause instability (here, the link to weak instruments) turns "we observed X" into understanding and lifts the technical depth considerably.
3. **Keep the results' practical meaning straight, and proofread captions.** Distinguish sampling variability across simulated datasets from what an analyst with one dataset can do. Never dismiss a bias that falls outside your own confidence interval without investigating it. Check that every figure and table caption matches its content.
