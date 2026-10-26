> **Actual grade:** Merit · **Source:** `Past Examples/Multivariate Ranks Using Optimal Transport - Merit.pdf`
> Profile written blind (the reviewer did not know the grade). The blind estimate below is the reviewer's guess, not the real mark.

# D08: Multivariate Ranks Using Optimal Transport
**Length:** 53 pages (41 numbered main-body pages plus 7 front-matter pages and 5 of references; no appendices), ~11,000 words in the main body (excluding references and appendices; raw count ~12,900 including maths and captions) · **Area:** Nonparametric statistics / optimal transport (multivariate rank-based two-sample testing)
**Structure:** Intro 5% · Related work / lit review 20% · Methodology (OT theory, OT ranks, existing OT tests) 27% · Proposed tests 15% · Simulation study 22% · Empirical study 7% · Conclusions and limitations 5%

## Research question and project type
How can ranks be defined in R^d so that they are distribution-free, and can such optimal-transport (OT) ranks be plugged into classical two-sample tests to build new multivariate nonparametric tests? The thesis explains OT-based ranks (Hallin et al., Chernozhukov et al., Ghosal and Sen, Deb and Sen). It then proposes three rank tests: a Rank MST test, a Rank Anderson–Darling test and a multivariate Wald–Wolfowitz runs test. Only the Rank MST test is evaluated, by simulation and on two real datasets. It is a mix of methodological and computational work. Methodology (mostly exposition) dominates, with a moderate simulation component.

## Contribution
- **Reproduced or explained:** the survey of component-wise, spatial and depth-based ranks (pp. 3–6). OT preliminaries and the Brenier–McCann theorem (pp. 11–12). Population and sample OT ranks via cell decomposition and power diagrams, following Ghosal and Sen (pp. 13–16). Halton-sequence plus Hungarian-algorithm ranks, following Deb and Sen (pp. 17–19). Rank Hotelling and rank energy tests (pp. 20–21).
- **Claimed as original:** (i) the Rank MST test (p. 22–24). This is the Friedman–Rafsky MST test applied to OT ranks, an application of the general "replace X_i by its rank" recipe the author states on p. 20. Friedman and Rafsky (1979) are never cited. (ii) The Rank AD test (p. 25–26): rank energy statistic with each pair weighted by a product of coordinate-wise R(1−R) terms. This is a heuristic analogue of Anderson–Darling with no theory and no simulations. (iii) The multivariate runs test (p. 26–27): only three loosely sketched options (PCA projection, clustering, Hilbert sorting), with no statistic actually defined. (iv) A data-dependent switch between a Unif[0,1]^d and a unit-ball reference distribution (p. 28).
- **Label:** new or modified method (modest, mostly plug-in) plus replication/exposition, with a small systematic comparison (Rank MST against Energy Distance).

## Theory
Depth: **restates known results.** Definitions (Borel measure, measurable function, subdifferential, Legendre–Fenchel dual, pp. 11) and theorems (Brenier–McCann, Alexandrov, the empirical rank map theorem 3.3 on p. 15–16) are stated without proof. The univariate rank-as-assignment argument via the rearrangement inequality (p. 7) is the only derivation. The distribution-freeness claim for Rank AD (p. 25–26) is a one-line argument, correct in spirit because under H0 the pooled ranks are a uniform permutation of fixed reference points. There are no new propositions, no consistency results and no power analysis for any proposed test.

## Empirical and simulation work
- **Design:** 2-D tests with independent components, correlated components and contaminated mixtures (pp. 28–35), plus intermediate dimensions d = 10–50 (pp. 35–36). B = 1000 permutations. Tables report the *average p-value* over only 50 replications (or 10 replications for n = 1000), not rejection rates. Most entries sit at the floor of 0.0010, so the tables carry little information. Two power-curve figures (Figs 9–10, 1000 replications) are the most informative results and show Rank MST doing better than Energy Distance under weak dependence changes.
- **Baselines:** only Energy Distance on raw data. There is no raw-data MST (Friedman–Rafsky) test, so the effect of the rank transform is never isolated, and no comparison with the existing OT-rank tests reviewed in §3.3 (rank Hotelling, rank energy).
- **Size control:** not checked properly. Under H0 only average p-values of about 0.5 are shown. In Fig. 9 the Energy Distance power is about 0 at small ρ, below the nominal 0.05 for an alternative. This suggests something odd in the implementation or setup, and it goes unremarked.
- **Real data:** red versus white wine (d = 11) and benign versus malignant breast cancer (d = 30). Both are trivially separable, so p = 0.001 is uninformative.
- **Reproducibility:** the summary says "Codes … can be viewed here: CODES-LINK". The placeholder was never filled in. SciPy functions are named and pseudocode is given (Algorithms 1–3). The runtime study (Fig. 7) confirms O(n³) empirically.

## Literature review
About 20% as a dedicated chapter, plus a further literature section in §3.3. It is reasonably broad, covering depth notions, spatial ranks, OT computation, recent OT-rank tests (Deb, Sen, Hallin, Shi et al. 2025) and applications of OT in ML. It is mostly descriptive, though it does compare: it explains distribution-dependence, the convex-contour limitation of Tukey depth (with a banana example, Figs 1 and 4) and computational cost. A key omission is the original graph-based two-sample literature (Friedman–Rafsky 1979, Henze, Rosenbaum's cross-match, Chen–Friedman), which the main proposed test builds directly on.

## Correctness
- **p. 34 (Table 3) and p. 36 (Table 4), serious:** the sample with 4% contamination from N(24,24) genuinely comes from a different distribution. Rank MST failing to reject is a Type II error, yet the text calls it "correctly concluding that the two samples are drawn from the same distribution". Energy Distance's rejection is called "incorrect". This interpretation is backwards, unless robustness to contamination is explicitly made the target, and the thesis does not do that.
- **p. 24:** complexity stated as O(B·n³). The ranks and the MST do not depend on the labels, so they are computed once and each permutation costs O(n). The test is O(n³ + Bn).
- **p. 28:** the reference distribution is chosen according to whether the samples "are normal-like". This is a data-dependent choice that undermines the distribution-free claim, and in practice the answer is unknown.
- **p. 31 vs p. 32:** the text uses "ρ = 1.9" (a covariance, not a correlation), but the Fig. 10 caption says ρ = 0.9. "ρ" labels a covariance throughout.
- **p. 4:** the spatial median is said to use the "L1 norm". It is the Euclidean norm. The Halton empirical quantile (p. 18) also uses an "L1 norm" without justification.
- **p. 6:** the Mahalanobis distance is missing a transpose, and the depth 1/(1+d_M) is mislabelled as "the Mahalanobis distance".
- **p. 16:** "ŵ is calculated in (5)" should refer to (6). Definition 3.2 switches between F and f. The hypothesis is written "H0: µνX = µνY" (pp. 23, 25).
- **p. 39:** Table 6 (breast cancer) is captioned "Wine Quality dataset".
- **Conclusions (p. 40):** the claim of "extensive simulation studies" and of good handling of "tail differences" and "nonlinear patterns" is overstated given the evidence.

## Writing and presentation
The English is readable but non-native and sometimes awkward: "cases are that…", "Codes running time", "goodness-of-fitness", "performe", "distinguishs", "diffference", "Tudey depth". Argument flow is logical and well signposted. The LaTeX is clean and standard: the title page is plain and tidy, and the dense maths page (p. 16) is neatly typeset with numbered displays and boldface definitions. The power-curve page (p. 32) shows two clean matplotlib line plots with legends and descriptive italic captions. The MST scatter plots (pp. 30, 35) are cluttered, with tiny axis text at the rendered size, though they do help intuition. Tables are simple and uniform. The acknowledgements run to a full, very personal page. Referencing is consistent author–year, but many entries lack venue details and capitalisation is broken ("monge–kantorovitch", "hotelling's t2").

## Critical reflection
There is a dedicated limitations section (p. 41). It honestly admits O(n³) cost, the lack of a principled choice of reference distribution, that only the Rank MST test was evaluated, and that average p-values should have been empirical power. It does not see the outlier misinterpretation, the trivial real-data examples or the missing raw-MST baseline. Interpretation goes beyond reporting in places (the explanation of why Rank MST gains power under weak dependence, p. 33), but the explanations are intuitive and untested.

## Strengths
1. An ambitious, current topic (OT-based multivariate ranks). The exposition of the population and sample definitions, including both the cell-decomposition and Halton/Hungarian routes, is coherent and well illustrated (Figs 3–6).
2. The power curves (Figs 9–10) are a genuine, properly replicated comparison showing a regime where Rank MST beats Energy Distance.
3. A clear structure, with pseudocode for every algorithm, an empirical runtime check and an honest limitations list.

## Weaknesses
1. The "three new tests" are thin. One is a plug-in of a classical test that is not cited (Friedman–Rafsky), one is an untested heuristic, and one is only a sketch. There is no theory for any of them.
2. The simulation design is weak: average p-values from 10–50 replications, floor effects, no proper size study, a single baseline that does not isolate the rank transform, and trivially separable real datasets.
3. The outlier/contamination results are misread (a missed detection is called "correct"), and there are several technical slips (complexity, norms, a data-dependent reference choice, caption and cross-reference errors). The code link is a placeholder.

## Scores (1–5, 5 = exceptional for an MSc)
| Originality | Technical depth | Rigour | Empirical work | Literature review | Writing | Presentation | Critical reflection |
|---|---|---|---|---|---|---|---|
| 3 | 3 | 2 | 2 | 3 | 3 | 3 | 3 |

## Blind grade estimate
**Estimate:** Merit · **Mark:** ~65 · **Confidence:** low
The topic is ambitious and the mathematical exposition is competent, which pushes it towards the upper Merit band; a lenient marker who rewards the "three new tests" framing could go to Distinction. Holding it back: the original content is shallow (one of the three tests is properly evaluated), the empirical evaluation is underpowered and lacks the obvious baselines, and there are clear interpretive and technical errors. Overall it reads as a good literature-driven project with a modest plug-in extension, not a rigorous methodological contribution.

## Lessons for a future student
1. If you call something a "new test", cite and compare against its closest ancestor. Here that is the raw-data MST test, which would show what the rank transform actually adds. Also evaluate every method you propose, or drop it: it is better to present one well-studied method than three half-studied ones.
2. Report rejection rates (size under H0 and power under H1) over enough replications, not average p-values stuck at 1/(B+1). Use real datasets where the answer is not obvious.
3. Think carefully about what "correct" means in each simulation scenario. Failing to detect a real distributional difference is a Type II error, not robustness, unless you have set up robustness as the explicit goal beforehand.
