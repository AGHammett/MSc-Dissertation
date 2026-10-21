# Improving Statistical Inference Using External Predictions: Overview

**Supervisor:** Dr Oliver Feng · **Prepared:** 21 October 2026 · **Sources:** the brief and the 3 supplied papers only

> **Labels.** **[Paper]** a paper states it (with reference) · **[Brief]** the brief states it · **[Interpretation]** my own reading. Check it before relying on it.

*Page references.* For PPI and PAST, printed page numbers coincide with PDF page indices. For CARE, the title/abstract page is unnumbered, so printed page = PDF page − 1; I mostly cite CARE by section, theorem and equation number.

## 1. The brief

**[Brief]** In many supervised problems, fully observed data (covariates *and* responses) are scarce because labelling is slow or expensive (e.g. expert image labelling). At the same time we may have a black-box ML system or external estimator that produces predictions (e.g. artificial labels) from covariates, plus a much larger dataset in which responses (and possibly covariates) are missing. The question is whether external predictions can be combined with the labelled data to improve estimation and inference. The aim is specifically to find approaches that give significant gains *even when the predictions are inaccurate*, so they should not simply be plugged in as extra covariates or as surrogate responses. The suggested starting point is a comprehensive literature review. After that, the student may compare and/or modify existing methods, with theoretical and/or empirical analysis, or may implement and refine these procedures in a specific application area such as imaging or biostatistics.

**Project type:** methodological, with a theoretical and a computational component. Which one dominates is left open by the brief ("theoretical and/or empirical"). **[Interpretation]** The common core is methodological: understanding, comparing and modifying estimators that combine scarce labels with external predictions. The supervisor's own paper (CARE) is heavy on theory (non-asymptotic rates, minimax lower bound, oracle inequalities for cross-validation), so a theory-leaning project would fit his angle. An applied/computational dissertation is equally allowed by the brief's "specific application area" direction.

## 2. Paper by paper

**Recommended reading order: PPI → PAST → CARE.** PPI is the simplest and most self-contained. Its warm-up (mean estimation, §1.3) gives the key debiasing idea in one line of algebra, and it is the paper the brief's wording most closely echoes ("valid inference", "inaccurate predictions"). PAST moves from inference to *prediction*. It treats external predictions as "helper covariates" rather than as responses, and it introduces the non-asymptotic, empirical-process style of guarantee. CARE is the supervisor's paper and by far the most technical: survival analysis, reproducing kernel Hilbert spaces and a 106-page appendix. It is easiest to read once the "combine external predictions safely" theme is clear from the other two. **[Interpretation]** Read CARE §1 and §3.3 early anyway, because they show what the supervisor cares about.

### 2.1 Prediction-Powered Inference (Angelopoulos, Bates, Fannjiang, Jordan, Zrnic, 2023)

arXiv:2301.09633v4 [stat.ML], 9 Nov 2023 (UC Berkeley). PAST cites the published version as *Science* 382 (2023).

- **Problem.** **[Paper]** We have a small gold-standard labelled set $(X_i,Y_i)_{i=1}^n$, a large unlabelled set $(\tilde X_i)_{i=1}^N$ with $N\gg n$, and a prediction rule $f$ trained on independent data. The aim is to build *provably valid* confidence intervals for a population quantity $\theta^*$ (mean, quantile, regression coefficient, …) that are narrower than the "classical" intervals that use labelled data only. The "imputation" approach (treat $f(\tilde X_i)$ as truth) is cheap but generally biased (§1, p. 1; §1.1, p. 2).
- **Approach.** **[Paper]** Define a *rectifier* $\Delta$ that measures how prediction errors bias the imputed estimate. Build a confidence set for $\Delta$ from labelled data, then correct the imputed estimate by every plausible value of $\Delta$ (§1.1, p. 2). For the mean (§1.3, p. 3),
  $$\hat\theta^{PP}=\underbrace{\tfrac1N\textstyle\sum_{i=1}^N f(\tilde X_i)}_{\tilde\theta^f}-\underbrace{\tfrac1n\textstyle\sum_{i=1}^n\big(f(X_i)-Y_i\big)}_{\hat\Delta},\qquad \hat\theta^{PP}\pm z_{1-\alpha/2}\sqrt{\hat\sigma^2_{f-Y}/n+\hat\sigma^2_f/N}.$$
  This estimator is unbiased, and its interval is narrower than the classical one when $\mathrm{Var}(f(X)-Y)<\mathrm{Var}(Y)$ and $N\gg n$. More generally, for $\theta^*=\arg\min_\theta E[\ell_\theta(X,Y)]$ with convex $\ell_\theta$ and subgradient $g_\theta$, the rectifier is $\Delta_\theta=E[g_\theta(X,Y)-g_\theta(X,f(X))]$ (eq. (2), p. 5). The paper also notes the "rectified loss" $L^{PP}(\theta)$ whose minimiser is a prediction-powered point estimate (§4.3, p. 16). The authors say the mean estimator is the *difference estimator* from model-assisted survey sampling and relate it to AIPW and the semiparametric missing-data literature (§1.4, p. 4).
- **Main findings and results.**
  - **[Paper]** **Theorem 1** (p. 5): for any nondegenerate convex estimation problem, $C^{PP}_\alpha=\{\theta:0\in\mathcal R_\delta(\theta)+\mathcal T_{\alpha-\delta}(\theta)\}$ has coverage $\ge1-\alpha$, with no assumptions on $f$ or on the data distribution beyond the ability to build intervals for two means. Theorem C.1 (App. C.1, p. 25) is the CLT-based asymptotic version.
  - **[Paper]** Algorithms 1–5 and Propositions 1–4 (pp. 6–8) give intervals for the mean, quantiles, logistic regression, linear regression (sandwich variance) and general convex M-estimators (Table 1, p. 8). Nonasymptotic variants are in App. C.2.
  - **[Paper]** Extensions (§4): nonconvex/constrained risk minimisation through a one-dimensional loss rectifier and data splitting (**Theorem 2**, p. 14; e.g. mode, Tukey biweight, best-subset). Covariate shift with a *known* Radon–Nikodym weight (**Corollary 1**, p. 15). Label shift through a confusion-matrix inversion (**Theorem 3**, p. 16). Finite populations (App. B). p-values (App. A).
  - **[Paper]** Experiments (§3, Fig. 1, Table 2): seven applications (AlphaFold proteomics, Galaxy Zoo, gene expression with a transformer, Amazon deforestation, census health insurance, census income under covariate shift, plankton counting under label shift). In all of them, imputation intervals fail to cover, and PPI intervals are valid and narrower than classical ones. Labels needed to reject a null, PPI vs classical: e.g. 316 vs 799 (AlphaFold), 189 vs 449 (galaxies), 21 vs 35 (deforestation), 5569 vs 6653 (health insurance) (Table 2, p. 10).
  - **[Paper]** **Appendix G** (pp. 35–37) is directly relevant to the brief. PPI can be *worse* than classical inference when the model is inaccurate (deforestation with a linear model: 40 vs 35 labels needed, App. G.2) or when $N$ is not large relative to $n$ (App. G.3). For binary $Y$ with $p=0.5$ the model's error rate must be below 25%, and for $p=0.1$ below about 9.5%, for PPI to help (App. G.1).
  - **[Paper]** App. F: PPI beats Wang et al.'s post-prediction inference (which fails to cover) and Zhang & Bradic's semi-supervised mean estimator in a census experiment.
- **Key assumptions.** **[Paper]** Labelled and unlabelled data are i.i.d. from the same distribution (relaxed in §4.2 and App. B). $f$ is independent of the observed data (§1.2, p. 3). The estimand is a convex M-estimand satisfying the first-order condition (1), and §2.1 additionally needs CLT regularity conditions (App. C.3). For covariate shift, the density ratio $w(x)$ must be known (§4.2.1).
- **Relation to the other papers.** **[Interpretation]** PPI is the "inference" pole of the area. Its rectifier is the same debiasing device that turns up implicitly in PAST's pseudo-response step. PAST explicitly calls PPI "related in spirit (but distinct in goals)" (PAST §1.2, p. 4). PPI gives no mechanism for *downweighting* poor predictions, and App. G shows the cost of that gap. CARE (cross-validated convex weighting) and PAST (a learned recalibration $\tilde g$) both address the same gap in different ways. CARE does not cite PPI.

### 2.2 Prediction Aided by Surrogate Training (Xia, Wainwright, 2024)

arXiv:2412.09364v1 [math.ST], 12 Dec 2024 (MIT).

- **Problem.** **[Paper]** This is semi-supervised *prediction* in which every observation also carries "helper" (surrogate) covariates $W$ that may be used in training but are not available at prediction time. The labelled data are $(X_i,W_i,Y_i)_{i\le n}$ and the unlabelled data are $(X_i,W_i)_{i=n+1}^{N}$. The goal is a predictor $\hat f(x)$ close to $f^*=\arg\min_f E\,L(f(X),Y)$ (eq. (1)–(2), §2.1, p. 5). Sources of $W$ include noisy or mis-calibrated predictions from pre-trained/foundation models, future covariates in forecasting, and outputs of models from related tasks (§1.1, pp. 2–4).
- **Approach.** **[Paper]** PAST is a three-stage meta-procedure (Algorithm 1, p. 6): (i) fit $\tilde g(x,w)$ to predict $Y$ from $(X,W)$ on the labelled data; (ii) impute pseudo-responses $\tilde Y_i=\tilde g(X_i,W_i)$ on the unlabelled data; (iii) run ERM over a class $\mathcal F$ on all $N$ points (eq. (3)). The "ideal proxy" is $g^*(x,w)=E[Y\mid X=x,W=w]$ (eq. (4)). **[Interpretation]** This is exactly the brief's point that inaccurate predictions should not be used directly as responses: they enter as an input to a recalibration model, so bias or label flipping in $W$ is learned and corrected.
- **Main findings and results.**
  - **[Paper]** **Theorem 1** (square loss, p. 9): with probability $\ge1-\delta$,
    $$\|\hat f-f^*\|_2\le(11+10\sigma)r_N+3\|\tilde f-f^*\|_m+2\tau_N(\delta),$$
    where $r_N$ is the oracle rate with $N$ *labelled* points, defined through localised Rademacher complexity (eq. (5a)–(5b)). Here $\tilde f(x)=E[\tilde g(X,W)\mid X=x]$ is the *W-smoothed* auxiliary fit (eq. (7b)) and $\tau_N$ is a higher-order term (eq. (8)). The paper stresses that the bound depends on $\tilde f-f^*$ rather than $\tilde g-g^*$, which is smaller by Jensen's inequality (p. 9).
  - **[Paper]** **Theorem 2** (p. 14): analogous bounds for Lipschitz, strongly convex losses that are "$g^*$-compatible" (eq. (16)), covering GLM-type losses (eq. (17b)) such as logistic/cross-entropy.
  - **[Paper]** Synthetic ensembles (§2.4): when $\lambda$ (the helper's usefulness) is close enough to 1 relative to $\sqrt{n/N}$, PAST attains the oracle rate (eq. (12), Fig. 1(a)). With a high-dimensional nuisance helper, PAST can be **worse than the labelled-only baseline** for small $\lambda$ (eq. (14), Fig. 1(b), $\lambda\in[0,0.4]$).
  - **[Paper]** Classification (§2.6): stochastic soft labels $\tilde Y\sim\mathrm{Ber}(\tilde g)$ give calibrated $\tilde f$, while hard labels can be mis-calibrated (eq. (21b), Fig. 2(a)). With label-flipping noise, PAST stays stable while treating $W$ as the label degrades (eq. (22b), Fig. 2(b)).
  - **[Paper]** Real data (§3): $R^2$ gains in forecasting societal ills (e.g. alcoholism 0.147 → 0.216, Table 1, p. 20). Small accuracy gains for post-MI cardiovascular risk on MIMIC-IV at low labelled fractions, where hard labels were slightly better (Fig. 3, §3.2). NLSY income $R^2$ 4.6% → 6.5% (§3.3). Pneumonia from chest X-rays with NegBio noisy labels as helpers: AUC 0.55 → 0.66 (§3.4).
- **Key assumptions.** **[Paper]** i.i.d. sampling with responses missing completely at random (MCAR) (§2.1, p. 5). $\mathcal F$ and $g^*$ uniformly bounded, noise $Y-g^*$ bounded in $[-\sigma,\sigma]$ (p. 8). A monotonicity condition on $r_N$ (eq. (6)). Loss compatibility (eq. (16)) for Theorem 2.
- **Relation to the other papers.** **[Interpretation]** PAST shares the setting with PPI (few labels, many unlabelled points, external predictions), but its target is prediction risk rather than confidence intervals, and it treats predictions as covariates to be recalibrated rather than as responses to be debiased. It shares with CARE a non-asymptotic "oracle rate + overhead" style of bound. Unlike CARE it has no built-in protection when the helper is harmful (§2.4.2), and the authors list automatic detection of this as future work (§4, p. 25), which is essentially what CARE's cross-validated weighting does in its own setting.

### 2.3 Upgrading survival models with CARE (Underwood, Reeve, Feng, Lambert, Mukherjee, Samworth, 2026)

arXiv:2506.23870v3 [stat.ME], 23 Sep 2026. **[Paper]** The first page lists **Oliver Y. Feng (Department of Statistics, LSE) as a co-author** (third author). Python package `care-survival` (Abstract; §6).

- **Problem.** **[Paper]** Clinical risk models (e.g. SCORE2 for 10-year cardiovascular risk) are periodically updated as new covariates become available, often from a different data source. The original training data are often unavailable (confidentiality, proprietary reasons), so the existing model can only be *queried*. The question is how to combine one or more such "external" relative-risk estimators with a new censored time-to-event dataset that has an expanded covariate set (§1, pp. 1–2). The standard practice of importing published hazard ratios assumes they stay valid when covariates are added, which is a strong assumption (§1, p. 1).
- **Approach.** **[Paper]**
  1. A proportional hazards model $h(t\mid x)=\lambda_0(t)e^{f_0(x)}$ with relative risk $f_0$ in an RKHS $\mathcal H$ and $P_X(f_0)=0$ (eq. (1), §2.2–2.3).
  2. A kernel estimator $\hat f_{n,\gamma}$ that minimises the negative log-partial likelihood plus $\gamma\|f\|^2_{\mathcal H}$ subject to empirical centring (eqs. (2)–(4)). A representer result (**Proposition 3**) reduces this to a strongly convex problem in at most $n$ dimensions. A linear kernel gives a regularised Cox model (§1, p. 1).
  3. **CARE**: form convex combinations $\check f_{n,\gamma,\theta}=(1-\sum_m\theta_m)\hat f_{n,\gamma}+\sum_m\theta_m\tilde f_m$ of the kernel estimator and the (centred) external estimators, and choose $(\gamma,\theta)$ *jointly* by partial-likelihood cross-validation on an independent validation set of size $n$ (§3.3, eq. (6)). External models need not use the same covariates; one only needs to be able to evaluate the validation likelihood at them (§3.3).
- **Main findings and results.**
  - **[Paper]** **Theorem 4** (§4.1): with high probability, $\|\hat f_{n,\gamma}-f_0\|_{L^2}\le C_0\big(\sqrt{(H_{2,\gamma}+s)/n}+\sqrt\gamma\big)$ (eq. (7)), where $H_{2,\gamma}$ is the kernel's effective dimension. This gives rates $n^{-1/2}$ for polynomial kernels, $n^{-1/3}$ for the first-order Sobolev kernel, and $n^{-b/(2+2b)}$ for eigenvalue decay $\nu_r\le r^{-b}$ (Examples 5–7, §4.1.1).
  - **[Paper]** **Theorem 8** (§4.2): a matching minimax lower bound (in a simplified uncensored, constant-baseline sub-model), so the rate is optimal.
  - **[Paper]** **Theorem 9** (§4.3): cross-validated $\hat\gamma$ is within a constant factor of the best $\gamma\in\Gamma$, up to an additive $\sqrt{(s+\log n)/n}$.
  - **[Paper]** **Theorem 10** (§4.4) and eq. (8): CARE is within a constant of the oracle convex combination, so it converges at least as fast as *both* the optimal kernel estimator and the best external model, $\min\{\sqrt{H_{2,\gamma^\star}/n}+\sqrt{\gamma^\star},\ \|\tilde f_{m^\star}-f_0\|_{L^2}\}$, plus $\sqrt{(s+|\mathcal M|+\log n)/n}$. Poor external models therefore do not significantly degrade CARE. The paper calls this a "double regularisation" (shrinkage towards 0 via $\gamma$ and towards the external models via $\theta$). Some covariate shift between the external and new populations is tolerated if the density ratio is bounded (§4.4).
  - **[Paper]** Simulations (§6.1, App. D.1): the oracle and cross-validated weight $\theta$ decrease as $n$ grows. CARE beats the kernel-only estimator throughout and beats the external model once $n$ is moderate (Figs 4, 6). The results are robust to heavy or no censoring (App. D.1).
  - **[Paper]** UK Biobank (§6.2): SCORE2 (trained on 173,438 people from an independent cohort) is upgraded with deprivation (imd) and two polygenic scores, using a quadratic polynomial kernel. CARE improves on SCORE2 once $n\ge10{,}000$. With all data, the concordance index improves by 0.51%/0.44% (F/M) for Model 1 (same covariates) and by 1.52%/2.26% for Model 2 (new covariates) (§6.2.1–6.2.2). Linear-kernel (Cox) and Sobolev-kernel variants are reported in App. D.2.4–D.2.5.
- **Key assumptions.** **[Paper]** Conditionally independent censoring. $\inf_x P(T\ge1\mid X=x)>0$ (§2.2). Correct specification $f_0\in\mathcal H$ (§2.3). Kernel regularity conditions (App. B). External estimators computed on data independent of the training and validation sets, and uniformly bounded (§3.3). Finite grids $\Gamma\subseteq[n^{-\xi},n^\xi]$ and $\Theta$ in the simplex (§4.3, §3.3).
- **Relation to the other papers.** **[Interpretation]** CARE is the supervisor's take on "external predictions". The external information is a whole *fitted function* (a risk score) whose training data are gone, rather than labels for an unlabelled sample. It contributes the idea most relevant to the brief's "even when inaccurate" clause: *learn how much to trust the external predictor* by cross-validation, with a guarantee that the result is never much worse than ignoring it or using it alone. PPI and PAST lack this, and both papers contain explicit examples where they lose to the labelled-only baseline (PPI App. G; PAST §2.4.2). CARE's targets are estimation and prediction ($L^2$ error, concordance) rather than confidence intervals, and it uses no unlabelled covariate sample.

## 3. How the papers fit together

**Common thread.** **[Interpretation]** All three papers combine a small, trusted dataset with a cheap but untrusted external predictor. All three insist that the result must not inherit the predictor's errors uncritically. They differ in *how* trust is controlled: debiasing (PPI), recalibration (PAST) and data-driven weighting (CARE).

| | PPI | PAST | CARE |
|---|---|---|---|
| Goal | Valid CIs / p-values for $\theta^*$ | Low prediction risk for $\hat f(x)$ | Low $L^2$ error for relative risk $f_0$ |
| External info | Predictions $f(X)$ on labelled + unlabelled data | Helper covariates $W$ (incl. ML predictions) on all data | Fitted external risk functions $\hat f_m$ (data unavailable) |
| Unlabelled sample? | Yes, $N\gg n$ | Yes, $m$ points | No (new labelled data split train/validation) |
| How errors in predictions are handled | Rectifier $\Delta$ estimated on labelled data | Learn $\tilde g(x,w)\approx E[Y\mid X,W]$, then pseudo-label | Cross-validated convex weight $\theta$ |
| Protection if predictions are bad? | No (App. G: can lose to classical) | No (§2.4.2: can lose to naive) | Yes, oracle inequality (Thm 10, eq. (8)) |
| Theory style | Exact/asymptotic coverage (Thm 1, C.1) | Non-asymptotic risk bounds via localised Rademacher complexity (Thms 1–2) | Non-asymptotic rates, minimax lower bound, CV oracle inequalities (Thms 4, 8–10) |
| Data model | i.i.d. (+ shift extensions) | i.i.d., MCAR | Censored survival, proportional hazards, RKHS |

```
            trusted labels (scarce)                  external predictor (cheap, possibly wrong)
                      \                                   /
                       \------ how much to trust it? ----/
                              |            |            |
                     debias (PPI)   recalibrate (PAST)   weight by CV (CARE)
                        |                 |                    |
                    valid CIs       prediction risk      L2 risk, adaptive
```

**Axes of difference.** (i) Inference vs prediction/estimation. (ii) Whether an unlabelled covariate pool exists. (iii) Whether the external object is a set of predictions or a fitted function. (iv) Parametric/convex M-estimands vs nonparametric function estimation. (v) i.i.d. regression vs censored survival data.

**Settled vs unsettled (as these papers present it).**
- **[Paper]** Settled: valid inference with an arbitrary black-box predictor for convex M-estimands (PPI Thm 1). Oracle-type prediction rates when helpers make $Y$ easier to predict (PAST Thm 1). Minimax-optimal kernel relative-risk estimation and adaptive aggregation with external survival models (CARE Thms 4, 8, 10).
- **[Interpretation]** Unsettled within these papers: (a) inference that is *both* valid *and* guaranteed no worse than classical when predictions are poor (PPI has validity without the guarantee, CARE has adaptivity but no confidence intervals); (b) prediction-powered methods for survival data, where the partial likelihood couples observations through risk sets, so PPI's i.i.d. mean-of-gradients rectifier does not apply directly; (c) relaxing MCAR / independence assumptions; (d) automatic detection of harmful helpers (PAST §4).

## 4. Tie-in to the dissertation

### 4.1 What the proposed directions mean in practice

1. **Comprehensive literature review [Brief].** In practice: master the three supplied papers, then the literature they point to. PPI §1.4 lists survey-sampling difference/GREG estimators, AIPW and semiparametric missing data, semi-supervised inference (Zhang–Brown–Cai, Chakrabortty–Cai, Zhang–Bradic, Song et al.) and Wang et al.'s post-prediction inference. PAST §1.2 adds weak supervision, noisy labels and surrogate indices. CARE §1 adds data fusion and aggregation (Goldenshluger, Dalalyan–Salmon), external-information Cox models (Huang et al. 2016; Ding et al.; Wang et al. 2025) and pseudo-labelling under covariate shift (Wang 2026). **[Interpretation]** A good review would organise these along the axes in §3 rather than paper by paper.
2. **Compare existing methodology [Brief].** **[Interpretation]** Implement classical, imputation, PPI, PAST-style pseudo-labelling and a CARE-style cross-validated convex combination on a common simulation design. Vary predictor accuracy (e.g. PPI App. G's flip rate $\eta$), the ratio $N/n$, and helper dimension (PAST eq. (13)). Report coverage, interval width, and $L^2$/prediction error. The aim is to map out *when* each method helps or hurts, which is the regime the brief cares about.
3. **Modify existing methodology, theory and/or simulations [Brief].** **[Interpretation]** Natural modifications suggested by the papers:
   - (a) A *weighted* PPI estimator, e.g. $\frac1N\sum\lambda f(\tilde X_i)-\frac1n\sum(\lambda f(X_i)-Y_i)$, with $\lambda$ chosen from data (analogous to CARE's $\theta$). Prove that the variance is never above classical, and check that coverage survives the data-driven choice.
   - (b) A CARE-style safeguard for PAST: cross-validate between PAST and the naive fit, or over a convex weight between them, as PAST §4 suggests.
   - (c) Prediction-powered *inference* for Cox regression coefficients or for relative risks, using an external risk score such as SCORE2 as the "prediction".
   - (d) Confidence intervals or uncertainty quantification for CARE itself, which the paper does not provide.
4. **Application area, e.g. imaging or biostatistics [Brief].** **[Interpretation]** Biostatistics aligns with CARE (risk-score upgrading, censored outcomes). Imaging aligns with PPI (galaxy, plankton) and PAST (chest X-rays with NLP labels). In practice: get a dataset with ground truth, simulate scarce labels by subsampling (as all three papers do), use a pre-trained model's outputs as the external predictions, and evaluate the methods.

### 4.2 What a dissertation would plausibly involve

- **Proofs:** at least reproducing PPI's mean and linear-regression validity arguments (App. D). Possibly a new variance/efficiency comparison or an oracle inequality in a simple model.
- **New methods:** a modest modification (weighting, safeguarding, survival extension) rather than a whole new framework.
- **Simulations:** almost certainly central, because all three papers use them to illustrate theory.
- **Real data:** optional. Public options exist through the PPI code release; CARE's UK Biobank data are access-controlled (§6 below).

**[Interpretation] Shape A: "Safe prediction-powered inference" (theory + simulation).** Study a power-tuned/weighted PPI estimator for means and linear/logistic regression with the weight chosen by a CARE-like criterion. Prove (i) asymptotic validity with an estimated weight and (ii) that the asymptotic variance is at most the classical variance. Compare by simulation across predictor quality, reproducing PPI App. G's failure cases and showing the fix. Write-up: review, theory chapter, simulation chapter, one real-data illustration (e.g. census data via the PPI notebooks).

**[Interpretation] Shape B: "External risk scores in survival analysis" (methodological/applied, closest to the supervisor).** Use CARE as the base. Either (i) compare CARE against simpler ways of using an external risk score (offset in a Cox model, the score as a covariate, PPI-style debiasing of a Cox coefficient) in simulations under misspecified or shifted external models; or (ii) explore a PPI-style extension in which unlabelled covariates (people with covariates but no follow-up) are also available, combining CARE's weighting with PPI's use of unlabelled data. This needs survival-analysis background and would use `care-survival` and synthetic data unless UK Biobank access is possible.

### 4.3 Open questions

- **[Paper]** PAST §4 (pp. 24–25): model the full conditional distribution of $Y$ given $(X,W)$, e.g. via EM, to exploit heterogeneous imputation difficulty. Relax MCAR to missing-at-random ($Y\perp Z\mid(X,W)$, footnote 8). Develop automated (hold-out/CV-guided) procedures that detect when the auxiliary error dominates and PAST would be worse than naive.
- **[Paper]** PPI App. G: PPI is underpowered when the predictor is inaccurate or $N$ is not $\gg n$. The paper only advises not to use it then, and gives no corrective mechanism. **[Interpretation]** This is the clearest opening for the brief's "even when inaccurate" aim.
- **[Paper]** PPI §4.1, p. 13: the general (nonconvex) method does not reduce to the convex one and is expected to be less powerful. §4.2.2, p. 16: label-shift intervals become conservative as the number of classes grows. §4.2.1: covariate shift requires a *known* density ratio. **[Interpretation]** Each of these is a candidate refinement. Note that this version of PPI has no dedicated limitations/future-work section.
- **[Paper]** CARE §3.3: removing a covariate used by an external model requires marginalising over its conditional distribution, which "may be challenging" without the original data. CARE §6.2: the method and theory "could be adapted" to the Fine–Gray competing-risks setting. CARE §1: landmark analysis is not addressed. CARE §4.4: covariate shift is handled only via a bounded density ratio. App. C: details of automatic kernel selection are "omitted for brevity". CARE has no separate discussion or future-work section, so these are drawn from remarks in the main text.
- **[Interpretation]** Neither CARE nor PAST provides confidence intervals. Neither PPI nor PAST adapts automatically to bad predictions. Bridging these gaps is the shared open problem across the three papers.

## 5. Background knowledge required

| Area (Maths / Statistics / CS-ML) | Item | Status | Rough effort if not covered | Where it's needed |
|---|---|---|---|---|
| Statistics | CLT, delta method, confidence intervals, hypothesis tests/p-values | covered by my modules | n/a | PPI throughout |
| Statistics | M-/Z-estimation, sandwich variance, misspecified (projection) regression | partly covered | a week | PPI §2, Alg. 4, App. C.3 |
| Statistics | Missing data (MCAR/MAR), semi-supervised inference, AIPW/difference estimators | new to me | 1–2 weeks | PPI §1.4; PAST §2.1, §4; literature review |
| Maths | Measure-theoretic probability (Radon–Nikodym, conditional expectation) | covered by my modules (this term) | n/a | PPI §4.2.1; PAST eq. (7b); CARE §4.4, App. B |
| Maths | Concentration inequalities (Hoeffding, Bernstein), union bounds | partly covered | a few days | PPI Thm 2, App. C.2/E; PAST eq. (8); CARE proofs |
| Maths | Empirical process theory: Rademacher complexity, localisation, peeling | new to me | substantial: 3–4 weeks to read proofs, more to write new ones | PAST Thms 1–2, App. C–F; CARE App. E |
| Statistics | Nonparametric regression rates, minimax lower bounds | new to me | 2–3 weeks | PAST §2.3 examples; CARE Thms 4, 8 |
| Maths/CS-ML | Reproducing kernel Hilbert spaces, Mercer's theorem, representer theorem, Nyström | new to me | 2–3 weeks | CARE §2.3, §3.1, §5, App. A–B |
| Statistics | Survival analysis: censoring, hazards, Cox PH, partial likelihood, Breslow estimator | new to me | 2–3 weeks | CARE throughout; Shape B |
| Maths | Counting processes and martingales in survival analysis | partly covered (martingales this term) | 1–2 weeks to connect | CARE §2.2 (event process $N_i(t)$), App. E |
| Statistics | Model aggregation, cross-validation oracle inequalities | new to me | 1–2 weeks | CARE Thms 9–10; PAST §4 |
| Statistics | Risk-model evaluation: concordance index, integrated Brier score, calibration | new to me | a few days | CARE §6.2; PAST §2.6.1 |
| Statistics | Distribution shift (covariate/label shift, importance weighting) | partly covered | a week | PPI §4.2; CARE §4.4 |
| Maths | Convex analysis (subgradients, strong convexity), quasi-Newton optimisation | partly covered | a week | PPI §2; PAST §2.5.1; CARE Prop. 3, §5.3 |
| CS-ML | Random forests, gradient boosting, fine-tuning pre-trained CNNs | partly covered | a few days to a week | PPI §3, App. H; PAST §3 |
| CS-ML | Python scientific stack, reproducible simulation studies | partly covered | a few days | All implementation work |

**Biggest gap.** For a theory-leaning project, the main gap is empirical process theory together with nonparametric minimax arguments. These drive both PAST's and CARE's proofs and are a term-length topic. For a CARE-based project, survival analysis (partial likelihood, censoring) is a second substantial new area, though this term's martingale material connects to its counting-process formulation. A PPI-centred project needs much less: the core arguments use only CLTs, sandwich variances and union bounds, which is why it is the most accessible entry point.

## 6. Practicalities

### Code
- **[Paper]** PPI: points to the Python package `ppi-py` [38] "which contains code for reproducing the experiments", with a Jupyter notebook per application (§3, p. 10). The printed reference [38] gives no URL. The PDF's embedded notebook links point to `https://github.com/aangelopoulos/ppi_py` (e.g. `examples/alphafold.ipynb`, `galaxies.ipynb`, `forest.ipynb`, `census_healthcare.ipynb`, `census_income_covshift.ipynb`, `gene_expression.ipynb`, `plankton.ipynb`). These are hyperlinks behind icons rather than printed text.
- **[Paper]** PAST: no code release is mentioned.
- **[Paper]** CARE: Python package `care-survival` (Abstract; §6), cited as v0.1.2 at `https://pypi.org/project/care-survival/` (reference list, Underwood et al. 2025).

### Data
- **[Paper]** PPI: AlphaFold/PTM data from Bludau et al. (10,803 points), Galaxy Zoo 2, yeast promoter gene expression (Vaishnav et al.), Amazon deforestation labels plus satellite forest-cover predictions, US census (California 2018–2019) via the Folktables interface, and WHOI plankton imagery (§3, App. H). The authors "packaged the data" so the notebooks run locally without downloading large datasets (§3, p. 10). They do not otherwise comment on licences.
- **[Paper]** PAST: American Community Survey 2010 and 2017–2021 (via IPUMS NHGIS) plus CDC BRFSS SMART (§3.1). MIMIC-IV, "available at PhysioNet" (§3.2). NLSY 1997 cohort (§3.3). MIMIC-CXR with NegBio labels and features from a TorchXRayVision foundation model (§3.4). The paper does not discuss access conditions. **[Interpretation]** MIMIC datasets usually require credentialed access, so check before planning around them.
- **[Paper]** CARE: simulated data (§6.1) and UK Biobank (N = 162,682 females, 121,333 males after removing about 15% with missing covariates), used "under application 608471" (§6.2, §7). Polygenic scores come from the PGS Catalog. The SCORE2 external model was trained on Emerging Risk Factors Collaboration data. UK Biobank is not described as public. **[Interpretation]** It is access-controlled, so whether a student could use it under the supervisor's application is a question for the meeting.

### Compute
- **[Paper]** PPI: fine-tunes ResNet50 (galaxies) and ResNet152 (plankton) with Adam/AdamW, batch size 32 (App. H.2, H.7). Other predictors are gradient-boosted trees or small logistic models. No hardware or run times are reported. PAST: random forests and a 3-layer network on 1024-dimensional pre-computed X-ray features (§3.4). No hardware is reported. CARE: BFGS optimisation, Nyström subsampling ($m=n\wedge100$) and 200 simulation repetitions (§5.3, §6.1). The UK Biobank analysis uses a quadratic polynomial kernel through a finite feature map for efficiency (§6.2, App. A.1). No hardware or run times are reported.
- **[Interpretation]** Everything a dissertation would plausibly do is laptop-feasible: PPI/PAST simulations, the PPI notebooks with their pre-computed predictions, and CARE simulations with Nyström. Only re-training deep image models from scratch, or kernel methods on hundreds of thousands of survival records without approximations, would call for the LSE cluster or a GPU. Pre-computed predictions avoid that entirely.

## 7. Questions for the proposal meeting

1. **Inference or prediction?** The brief says "estimation and inference", but only PPI produces confidence intervals; PAST and CARE target prediction/$L^2$ error. Which should the dissertation's main deliverable be: valid intervals, better point estimates, or both? This determines which theory and metrics matter.
2. **How central should CARE and survival analysis be?** Would you like the project to build on CARE (e.g. external risk scores in survival models), or is a general i.i.d. PPI/PAST setting fine? Survival analysis is a large new area for me, so this affects the time budget.
3. **What does "significant gains even when predictions are inaccurate" mean formally?** Is the target a guarantee of never doing worse than labelled-only methods (as in CARE's Theorem 10), or gains under a specific model of prediction error? This fixes the success criterion.
4. **Theory/empirics balance.** What level of proof is expected: reproducing known arguments, proving a new result in a simple model (e.g. a weighted PPI estimator), or something closer to CARE's non-asymptotic analysis? The empirical-process tools needed for the last option are a substantial investment.
5. **"Responses and possibly covariates missing".** Which setting did you have in mind for missing covariates: CARE's situation (external data entirely unavailable, only the model), or partially observed covariates in the new sample? They lead to different methods.
6. **Unlabelled data in survival settings.** Is there interest in combining CARE's weighting with a PPI-style unlabelled sample (people with covariates but no outcome or follow-up)? Does the partial likelihood's risk-set structure make PPI's rectifier argument break down, and is that a worthwhile question for an MSc?
7. **Data access.** Could I use UK Biobank under your application 608471, or should I plan on simulations plus public data (e.g. the PPI notebooks' census or galaxy data)? Access timelines can be long.
8. **Missingness mechanism.** All three papers assume MCAR-type sampling or independence of external estimators. Is relaxing this (MAR, label selection depending on covariates) in scope, or a distraction?
9. **Literature beyond the supplied papers.** Which strands should the review prioritise: semiparametric efficiency / semi-supervised inference (PPI §1.4), aggregation and data fusion (CARE §1), or weak supervision and noisy labels (PAST §1.2)? Are there specific follow-ups to PPI you consider essential?
10. **Software.** Is building on `ppi-py` and `care-survival` acceptable, or do you prefer independent implementations for transparency? This affects how much coding time goes to infrastructure.
11. **Application area.** If an applied component is wanted, do you prefer biostatistics (risk scores) or imaging (pre-trained classifier labels)? This decides which data and predictors I need early on.
12. **Distribution shift.** External models are often trained on different populations (CARE §4.4; PPI §4.2). Should robustness to shift between the external model's population and the new data be part of the project?
