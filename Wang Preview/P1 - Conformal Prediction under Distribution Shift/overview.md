# Conformal Prediction under Distribution Shift: Overview

**Supervisor:** Professor Tengyao Wang · **Prepared:** 21 October 2026 · **Sources:** the brief and the 4 supplied papers only, plus clearly labelled background knowledge on one unsupplied book

> **Labels.** **[Paper]** a paper states it (with reference) · **[Brief]** the brief states it · **[Background]** from my own general knowledge, not from the supplied papers and not checked against the source · **[Interpretation]** my own reading. Check it before relying on it.

Page numbers are the printed page numbers. For all four PDFs these match the PDF page index. References such as "Tibshirani §2.3" refer to sections of the supplied papers.

## 1. The brief

**[Brief]** Conformal prediction gives prediction sets that are distribution-free and have a finite-sample *marginal* coverage guarantee, but only when the data are exchangeable (Vovk et al., 2005). After a model is deployed, the population it meets may differ from the one used to train and calibrate it, and then standard conformal intervals can lose their coverage. Recent methods deal with this under different assumptions about the shift. Under *covariate shift*, importance-weighted conformal prediction reweights the calibration points so that they represent the target population (Tibshirani et al., 2019). Other methods give guarantees for non-exchangeable data (Barber et al., 2023), use doubly robust calibration (Yang et al., 2024), or protect against every distribution in a stated neighbourhood of the training distribution (Cauchois et al., 2024). The brief flags three practical issues: how to estimate the importance weights, what happens when the source and target populations overlap only partly, and the trade-off between coverage and interval width. The student would review the area, then implement and compare standard, importance-weighted and robust methods on simulated and real data. The simulations may vary shift severity, sample size, heteroscedasticity and source–target overlap. Stronger students may look at weight truncation, doubly robust calibration, or departures from the covariate-shift assumption. Prerequisites are mathematical statistics (regression, testing, asymptotics) and good R or Python skills. Exposure to statistical learning, importance sampling or semiparametric methods is desirable but optional.

**Project type:** mainly **computational**, with a **methodological** component. **[Interpretation]** The required core is a review followed by implementation and a designed simulation study plus real-data comparisons, which is computational. The optional extensions (truncation, doubly robust calibration, departures from covariate shift) add method development and possibly some light theory. The brief never asks for new theorems, but the papers' proofs are short enough that a small original result is realistic for a strong student (see 4.2).

## 2. Paper by paper

**Recommended reading order and why.** (0) Background on the conformal foundations, which you can take from Tibshirani §1 and Barber §2 and §6.1 without the book. (1) **Tibshirani et al.** It is short and sets up the covariate-shift problem and the weighted method that everything else compares against. (2) **Barber et al.** It has the same authors and notation as Tibshirani, its proofs are elementary (ranks plus total variation), and it explains how far coverage degrades when exchangeability fails. (3) **Cauchois et al.** This is the "robust" class of methods in the brief's core comparison. It uses a different idea (worst case over an f-divergence ball) and needs some convex analysis. (4) **Yang et al.** It addresses the same problem as Tibshirani, but its tools (semiparametric efficiency, influence functions, empirical processes) are the least familiar to you, and in the brief it is an optional extension.

### 2.0 Background: Vovk, Gammerman & Shafer (2005), not supplied

The book is not in the folder. Everything in this subsection marked **[Background]** comes from my general knowledge and **has not been checked against the book**. Where a supplied paper restates the same point, I cite the paper instead.

- **What the book is.** **[Paper]** *Algorithmic Learning in a Random World* (Springer, 2005) is described as "the definitive reference" for conformal prediction (Tibshirani p. 1) and "a critical resource" (Barber p. 8). Barber (pp. 9–10) says it contains chapters on going beyond exchangeability, including Mondrian conformal prediction and online compression models. **[Background]** The book collects Vovk and co-authors' work from the late 1990s and early 2000s. Its setting is mainly *online* prediction: examples arrive one at a time and the predictor issues a set before each label is revealed. The title refers to algorithmic randomness (Kolmogorov-style), which was the original motivation. Beyond conformal predictors the book also covers Venn predictors (calibrated probabilistic prediction), Mondrian (category-conditional) conformal predictors, and efficiency of conformal predictors. I believe there is a second edition (2022), but I have not verified this.
- **Exchangeability.** **[Paper]** Variables $Z_1,\dots,Z_{n+1}$ are exchangeable if their joint law is invariant under permutation. This is "(significantly) weaker" than i.i.d. (Tibshirani Remark 1, p. 3), and it is the only distributional assumption that standard conformal prediction needs (Tibshirani p. 1; Barber pp. 2–3). **[Background]** The book works under what it calls the randomness assumption (i.i.d.) and the exchangeability assumption, and much of the theory needs only the latter.
- **Nonconformity scores.** **[Paper]** A score $S((x,y),\mathcal Z)$ measures how unusual $(x,y)$ is relative to a multiset $\mathcal Z$. The standard example is the absolute residual $|y-\hat\mu(x)|$ (Tibshirani eq. (3), p. 2; Barber eq. (9), p. 8). Barber (p. 7) attributes the general nonconformity-score formulation to the book. **[Background]** In the book a *nonconformity measure* is any function of this kind that treats the bag of other examples symmetrically. For each candidate label it produces a conformal p-value, roughly the proportion of scores at least as large as the test score, and the prediction set at level $\varepsilon$ collects the labels whose p-value exceeds $\varepsilon$. The book also uses the related terms *confidence* and *credibility*.
- **Full (transductive) versus split (inductive) conformal.** **[Paper]** Full conformal refits the model on the training data augmented with $(X_{n+1},y)$ for every candidate $y$ and keeps the $y$ values whose score is not too extreme (Tibshirani eqs. (4)–(5); Barber §2, eq. (8)). This is statistically efficient but computationally heavy. Split, or inductive, conformal fits $\hat\mu$ once on a separate split and calibrates residuals on a hold-out set, giving $\hat\mu(x)\pm$ the $\lceil(1-\alpha)(n+1)\rceil$-th smallest hold-out residual (Barber eq. (5), p. 6; Tibshirani eq. (9), p. 5). Yang et al. (§2.1, p. 3) credit the transductive method to Vovk et al. (2005) and the inductive method to Papadopoulos et al. (2002). Barber (p. 6) attributes both to the book. **[Background]** In the book, inductive conformal predictors are a computationally cheap special case.
- **The finite-sample marginal coverage guarantee and why it holds.** **[Paper]** If the data are exchangeable and the algorithm treats points symmetrically, then $P\{Y_{n+1}\in\hat C_n(X_{n+1})\}\ge 1-\alpha$ for every distribution (Tibshirani Theorem 1, p. 3, attributed to Vovk et al. 2005; Barber Theorem 1, p. 7). There is also an upper bound $1-\alpha+1/(n+1)$ when there are no ties, attributed to Lei et al. (2018), not to the book (Tibshirani p. 2). The proof is a rank argument. Symmetric construction makes the $n+1$ scores exchangeable, so the test score is equally likely to occupy any rank, and the probability that it lies among the $\lceil(1-\alpha)(n+1)\rceil$ smallest is at least $1-\alpha$ (Tibshirani Lemma 1 and proof, p. 2). Barber §6.1 (pp. 28–29) gives an equivalent "strange points" proof: at most $\alpha(n+1)$ points can be strange, and by exchangeability the test point is no more likely than any other to be strange. **[Paper]** The guarantee is marginal. It averages over the training data and the test point, and it does not give conditional coverage given $X_{n+1}=x$. Exact conditional coverage at almost every $x$ for every distribution forces infinite expected length (Tibshirani p. 15, citing Vovk 2012 and Lei & Wasserman 2014). **[Background]** In the online setting the book proves something stronger for smoothed (randomised) conformal predictors: the error indicators are independent Bernoulli($\varepsilon$), so the long-run error frequency is $\varepsilon$ almost surely. The supplied papers use only the batch (single test point) version.

### 2.1 Conformal Prediction Under Covariate Shift (Tibshirani, Barber, Candès & Ramdas, 2019)

arXiv:1904.06019v3 [stat.ME], 6 July 2020. Barber et al. cite it as NeurIPS 32 (2019).

- **Problem.** Training data are i.i.d. from $P_X\times P_{Y|X}$, but the test point comes from $\tilde P_X\times P_{Y|X}$. The covariate law changes while the conditional law of $Y$ given $X$ stays the same (model (6), p. 3). Standard conformal prediction then loses its guarantee (§2).
- **Approach.** Each calibration score is weighted in proportion to the likelihood ratio $w(x)=d\tilde P_X/dP_X(x)$, and the test point's own weight is placed on $+\infty$ (eqs. (7)–(8), p. 4):
  $$p_i^w(x)=\frac{w(X_i)}{\sum_{j=1}^n w(X_j)+w(x)},\quad p_{n+1}^w(x)=\frac{w(x)}{\sum_{j=1}^n w(X_j)+w(x)},$$
  $$\hat C_n(x)=\Big\{y:\ V^{(x,y)}_{n+1}\le \mathrm{Quantile}\Big(1-\alpha;\ \textstyle\sum_{i=1}^n p_i^w(x)\delta_{V_i^{(x,y)}}+p^w_{n+1}(x)\delta_\infty\Big)\Big\}.$$
  The split version is $\mu_0(x)\pm$ a weighted quantile of hold-out residuals (eq. (10), p. 5). $w$ only needs to be known up to a constant (Remark 3). When $w$ is unknown, it is estimated with a probabilistic classifier that separates training covariates ($C=0$) from unlabelled test covariates ($C=1$), using $\hat w(x)=\hat p(x)/(1-\hat p(x))$ (eq. (12), p. 8). The general theory introduces *weighted exchangeability*: the joint density factorises as $\prod_i w_i(v_i)\,g(v_1,\dots,v_n)$ with $g$ symmetric (Definition 1, p. 12).
- **Main findings and results.**
  - **[Paper]** Corollary 1 (p. 4): with $\tilde P_X\ll P_X$ and the true $w$, the weighted band has coverage at least $1-\alpha$ in finite samples.
  - Lemma 2 (p. 12): independent non-identical draws are weighted exchangeable with weights $dP_i/dP_1$. Lemma 3, the weighted quantile lemma (p. 12), and Theorem 2, weighted conformal (p. 13), generalise Lemma 1 and Theorem 1. The proof conditions on the unordered multiset of data and computes the probability that the test point takes each value (§3.1–3.3).
  - Remark 5 (p. 13): no general upper bound on coverage, because one weight can be very large. This matters for over-coverage and width.
  - The weights depend on the test point $x$, so the weighted quantile has to be recomputed for each test point. Under covariate shift this is still as cheap as ordinary conformal (§4, p. 14). Yang et al. (p. 6) call it computationally intensive.
  - **Airfoil experiment** (§2.3, pp. 5–10). UCI data, $N=1503$, $d=5$, 5000 random splits (25% pre-fit, 25% calibration, 50% test). The shift is induced by resampling with probability proportional to $\exp(x^\top\beta)$, $\beta=(-1,0,0,0,1)$ (eq. (11)). Results at nominal 90%: ordinary split conformal covers 90.2% with no shift but only **82.2%** under shift. Oracle weighting restores **90.8%**. Estimated weights give **91.0%** for both logistic regression (well-specified here) and random forests (pp. 6–8, Fig. 2).
  - The weighted coverage histogram is more dispersed. The authors explain this with the effective sample size $\hat n=\|w(X_{1:n})\|_1^2/\|w(X_{1:n})\|_2^2$ (p. 6): unweighted conformal using only $\hat n$ points matches the dispersion (p. 8).
  - Weighted intervals are longer, partly because $\mu_0$ was not refitted for the shift (p. 8, Fig. 3). Random-forest weights sometimes give much longer intervals. Random-forest probabilities were **clipped to [0.01, 0.99]** because unclipped weights were infinite in about 2% of cases (footnote 3, p. 8). With no actual shift, estimated weights cost little, though random-forest weights add dispersion (Fig. 4, p. 10).
- **Key assumptions.** Covariate shift with $P_{Y|X}$ unchanged. Absolute continuity $\tilde P_X\ll P_X$. The likelihood ratio is **known**. The finite-sample guarantee does not cover estimated weights, and the paper gives no theory on the error from estimating weights (Yang p. 6 makes the same point). The score or algorithm treats points symmetrically.
- **Relation to the other papers.** This is the baseline the other three papers position themselves against. Barber generalises in a different direction (fixed weights, any non-exchangeability, with a coverage-gap bound) and argues that neither paper subsumes the other (Barber p. 8). Yang keeps the same covariate-shift problem but replaces the known-weight finite-sample guarantee with an asymptotic, doubly robust one that allows estimated nuisances. Cauchois drops the covariate-shift structure and protects against all score distributions within an f-divergence ball, arguing that the likelihood ratio is hard to estimate in high dimensions (Cauchois p. 6).

### 2.2 Conformal Prediction Beyond Exchangeability (Barber, Candès, Ramdas & Tibshirani, 2023)

arXiv:2202.13415v5 [stat.ME], 17 March 2023.

- **Problem.** Conformal validity rests on two kinds of symmetry: exchangeable data, and an algorithm that treats points symmetrically. Both fail under drift, changepoints or dependence, and under drift one may also want an algorithm that favours recent data (§1.1, p. 3). Before this paper there was no bound on how much coverage is lost when exchangeability fails (p. 4).
- **Approach.** "Nonexchangeable conformal" (NexCP) uses **fixed, pre-specified** weights $w_i\in[0,1]$, normalised as $\tilde w_i=w_i/(\sum_j w_j+1)$ and $\tilde w_{n+1}=1/(\sum_j w_j+1)$ (eq. (10)), and replaces the quantile with a weighted quantile (split: eq. (11); full: eq. (12)). For non-symmetric algorithms, which take tagged points $(X_i,Y_i,t_i)$ such as weighted least squares or autoregressive fits (§3.2), a random index $K\sim\sum_i\tilde w_i\delta_i$ is drawn and the test point's tag is swapped with point $K$'s before fitting (eqs. (17)–(18)). Split conformal needs no swap (p. 13). The paper also gives extensions to general scores (App. A), jackknife+ (App. B) and cross-conformal (App. D).
- **Main findings and results.**
  - **[Paper]** Theorem 2 (p. 15), the coverage-gap bound, holds with no assumption on the joint distribution:
    $$P\{Y_{n+1}\in\hat C_n(X_{n+1})\}\ \ge\ 1-\alpha-\sum_{i=1}^n\tilde w_i\, d_{TV}\big(R(Z),R(Z^i)\big),$$
    where $Z^i$ swaps the test point with point $i$ and $R(\cdot)$ is the residual vector. This is at most $\sum_i\tilde w_i\, d_{TV}(Z,Z^i)$, and for independent data it is at most $2\sum_i\tilde w_i\, d_{TV}(Z_i,Z_{n+1})$ (Lemma 1, p. 4; p. 16).
  - Theorem 3 (p. 16) gives an upper bound: coverage $<1-\alpha+\tilde w_{n+1}+$ the same TV sum, so the method does not over-cover much when the effective sample size is large.
  - Implications (§4.3, pp. 17–18). (i) Under exchangeability, fixed weights cost **no** coverage. (ii) Setting $w_i\equiv 1$ gives a new robustness result for *standard* split and full conformal: the gap is at most $\frac{1}{n+1}\sum_i d_{TV}(R(Z),R(Z^i))$. (iii) There is a trade-off: low weights reduce the effective sample size and widen intervals, and how to choose weights optimally is left open.
  - Worked examples (§4.4). Under bounded drift with $d_{TV}(Z_i,Z_{n+1})\le\epsilon(n+1-i)$ and $w_i=\rho^{n+1-i}$, the gap is at most $2\epsilon/(1-\rho)$. With a changepoint $k$ steps ago the gap is at most $\rho^k$. In an AR covariate example, the residual-based TV can be tiny while the raw-data TV is near 1 (eq. (19), pp. 19–20).
  - Appendix C (pp. 41–42, Theorem 6) gives a **multiplicative** bound under Huber contamination: non-coverage is at most $\alpha/(1-\epsilon)$, for independent data and symmetric algorithms.
  - **Experiments** (§5, nominal 90%).
    - Simulations with $N=2000$ and $X\sim N(0,I_4)$, linear $Y$, 200 replications, for i.i.d., changepoint and drift settings (Table 1, p. 24). CP+LS covers 0.900 / 0.835 / 0.838. NexCP+LS covers 0.907 / 0.884 / 0.888 with wider intervals. NexCP+WLS covers 0.907 / 0.906 / 0.907 with *narrower* intervals under shift (width 4.13 against 5.99 for CP+LS at the changepoint).
    - ELEC2 electricity data, $N=3444$ (Table 2, p. 26): CP+LS covers 0.852, NexCP covers about 0.89, and all methods are near 0.90 on randomly permuted data.
    - 2020 US election, with a biased split (Eastern time zone as training, 1119 training counties and 1957 test counties). Weights are $w_i=e^{-\gamma\|X^{\text{prev}}_i-X^{\text{prev}}_{n+1}\|_2}$ built from 2016 covariates and tuned to an effective sample size of 100 (pp. 26–28). CP+LS covers 0.743 against 0.820–0.840 for NexCP. With a CQR score, CP+QR covers 0.782 against about 0.835 (Table 3).
    - Split conformal and jackknife+ versions behave similarly (App. F, Tables 4–5).
- **Key assumptions.** Weights and tags must be **fixed**, i.e. independent of the data. Data-dependent weights need a conditional-TV version of the bound (§4.5, pp. 20–21), which the paper does not develop. The bound is useful only if you have qualitative prior knowledge that makes the weighted TV terms small (p. 18). There are no assumptions on the joint distribution.
- **Relation to the other papers.** It shares authors and the weighted-quantile construction with Tibshirani. However, Tibshirani's weights are data-dependent ($w(X_i)$), exact, and need covariate shift plus a known likelihood ratio, while Barber's are fixed and approximate and need no model of the shift (p. 8). **[Paper]** Barber claims that if there is no shift, Tibshirani's weighted algorithm "does not have any coverage guarantee, while ours retains exact coverage" (p. 8). **[Interpretation]** I read this as referring to running the weighted method with non-constant weights when the data are in fact exchangeable. With correct weights, which would then be constant, Tibshirani's guarantee still holds. Worth confirming. It is the natural tool for "departures from covariate shift" because its bound needs no structural assumption. Cauchois is mentioned as an alternative based on f-divergences (p. 9).

### 2.3 Robust Validation: Confident Predictions Even When Distributions Shift (Cauchois, Gupta, Ali & Duchi, 2024)

arXiv:2008.04267v3 [stat.ML], 4 July 2024. The brief cites it as 2024.

- **Problem.** Give prediction sets that keep $1-\alpha$ coverage uniformly over a set of plausible test distributions, without assuming a particular shift structure such as covariate shift. The authors argue that covariate shift is "no more plausible than other (more general) shifts" and that likelihood ratios are hard to estimate in high dimensions (p. 6). A second goal is to estimate how much shift to protect against (pp. 2–3).
- **Approach.** The uncertainty set is an f-divergence ball around the calibration *score* distribution $P_0$, namely $\{P: D_f(P\|P_0)\le\rho\}$ (eq. (6)). By the data processing inequality this covers every joint shift of $(X,Y)$ with $D_f(Q\|Q_0)\le\rho$ (p. 10). The worst-case quantile over the ball turns out to be an ordinary quantile at an inflated level:
  $$\sup_{D_f(P_1\|P)\le\rho}\mathrm{Quantile}(\beta;P_1)=\mathrm{Quantile}\big(g^{-1}_{f,\rho}(\beta);P\big),$$
  where $g_{f,\rho}$ comes from a one-dimensional convex problem (Proposition 1, pp. 10–11). In closed form, $g^{-1}_{f,\rho}(\tau)=\min\{\tau+\rho/2,1\}$ for total variation (Example 1), and $\chi^2$ gives $g_{f,\rho}(\beta)=[\beta-2\rho\beta(1-\beta)]_+$. The prediction set therefore thresholds the score at a higher empirical quantile (eq. (8)). The radius $\rho$ is chosen by looking for covariate regions with poor coverage: the worst coverage over subsets $R$ with $Q_0(X\in R)\ge\delta$ (eq. (10)), searched over sampled slab directions (Algorithm 1) or over an estimated "worst direction" fitted by regression or SVM on the scores (Algorithm 2). §4 and Algorithm 3 give a cross-fitted, debiased estimator of how sensitive coverage is to covariate shift in chosen covariates, using Rényi-∞ balls.
- **Main findings and results.**
  - **[Paper]** Theorem 1 (p. 12): if the test score has law $P_{\text{test}}$ with $\rho^\star=D_f(P_{\text{test}}\|P_0)$, coverage is at least $g_{f,\rho^\star}\big(\tfrac{n}{n+1}g^{-1}_{f,\rho}(1-\alpha)\big)$. If $\rho\ge\rho^\star$, coverage is at least $1-\alpha-c_{\alpha,\rho,f}/(n+1)$ (Corollary 2.1). A level-corrected version achieves exactly $\ge1-\alpha$ (Corollary 2.2). For TV, use the empirical quantile at $1-\alpha+\rho/2$ (Corollary 2.3). Coverage "degrades gracefully" if $\rho<\rho^\star$ (p. 13).
  - Theorem 2 (App. A.1, p. 31): Algorithm 1 approaches uniform coverage over the region class when that class has finite VC dimension. Consistency of the worst direction needs a strong stochastic-order condition (Assumption A2). The condition holds for linear shifts in a **heteroscedastic** regression $Y=\mu^\star(X)+h(v_{\text{var}}^\top X)\varepsilon$ (Example 4, p. 18; Lemma A.3, p. 33). Theorem 4 (App. B.2) gives $\sqrt n$ asymptotic normality of the sensitivity estimator.
  - **Experiments.**
    - Nine UCI regression datasets with exponential tilting along the top principal component, $w(x)=\exp(a v^\top(x-\bar x))$ with $a\in\pm\{0,\dots,0.64\}$. Standard conformal under-covers even for small tilts (Fig. 1, §1.3). With $\rho=0.01$ for $\chi^2$, the robust method clearly improves on standard conformal on 5 of the 9 datasets (abalone, delta ailerons, kinematics, puma, airfoil), with average coverage above nominal. Ailerons "still covers". The remaining datasets have roughly twice the divergence and lose coverage (App. C.1, pp. 41–43).
    - CIFAR-10.1, QMNIST and ImageNetV2 with a ResNet-50. Standard conformal covers 0.88 (target 0.95) on CIFAR and 0.80 (target 0.90) on ImageNet. The robust sets reach about nominal coverage and are "not substantially larger" (pp. 27–30).
    - COVID-19 county positivity time series (App. C.2).
    - Covariate-sensitivity checks on three UCI datasets (App. C.3).
- **Key assumptions.** The validation scores are i.i.d. (exchangeable) from $P_0$, and the test score is independent with law $P_{\text{test}}$ within divergence $\rho$. The guarantee is only as good as the choice of $\rho$, and the paper describes its methods for choosing $\rho$ as "well-motivated, but still heuristic" (p. 3). The model is held fixed: the method validates the model and does not adapt it (p. 9).
- **Relation to the other papers.** This is the "protect against a neighbourhood" approach named in the brief. It does not use target covariates, unlike Tibshirani and Yang, which makes it more general but potentially conservative. **[Interpretation]** A covariate shift with a large likelihood ratio can have a large divergence, so $\rho$ would have to be large. Note also that the robust set is a constant-width inflation of the usual set: it raises one quantile level and does not reweight. In its discussion it names Tibshirani-style reweighting as an alternative that is "likely impossible in high-dimensional scenarios" (§6, p. 30). Like Barber, it gives coverage under shifts that are not covariate shifts.

### 2.4 Doubly Robust Calibration of Prediction Sets under Covariate Shift (Yang, Kuchibhotla & Tchetgen Tchetgen, 2024)

arXiv:2203.01761v3 [stat.ME], 13 December 2022. The brief cites it as 2024, presumably the journal version, which is not supplied.

- **Problem.** The covariate-shift prediction problem of Tibshirani, but with the likelihood ratio unknown. Labelled source data are $\{(X_i,Y_i)\}_{i\le n}$, unlabelled target covariates are $\{X_i\}_{n<i\le N}$, and $P_{Y|X}$ is shared (eq. (2), §3.1). The authors call this "explainable covariate shift" and show that it is equivalent to **missing at random** (MAR) with indicator $T$ (§3.2, eqs. (6)–(7)).
- **Approach.** Fix a score $R(x,y)$, for example the absolute residual or the CQR score, trained on a separate split. Estimate the $(1-\alpha)$ quantile of $R$ in the target population by solving an estimating equation based on its **efficient influence function** (Lemma 1, eq. (13), p. 9):
  $$\mathrm{IF}(\theta;\pi,m)=\mathbb 1\{t=0\}\,\pi(x)\,[\mathbb 1\{r\le\theta\}-m(\theta,x)]+\mathbb 1\{t=1\}\,[m(\theta,x)-(1-\alpha)],$$
  with nuisances $\pi^\star(x)=P(T=1|x)/P(T=0|x)$ (the density ratio, up to a constant) and $m^\star(\theta,x)=P(R\le\theta|X=x)$ (the conditional CDF of the score). $\hat r_\alpha$ is the smallest $\theta$ at which the empirical mean of IF is $\ge 0$, and the set is $\{y:R(x,y)\le\hat r_\alpha\}$. Algorithm 1 ("split DRP", p. 12) estimates nuisances on one split and solves the equation on another. Algorithm 2 ("full DRP", p. 14) avoids splitting. Algorithm 3 (p. 20) picks the narrowest set over several learners. §9 adds a sensitivity parameter $\gamma(x,y)$ for departures from MAR.
- **Main findings and results.**
  - **[Paper]** Theorem 1 (p. 8), an impossibility result: without knowing either the shift or $P_{Y|X}$, any prediction set with finite-sample coverage under all such distributions must have **infinite expected Lebesgue measure**. The proof goes via the impossibility of conditional-independence testing (Shah & Peters). This is why the paper aims only for asymptotic coverage.
  - Lemma 2 (p. 10): coverage equals $1-\alpha+P[\mathrm{IF}]/P(T=1)$ whenever *either* $\pi$ or $m$ is correct (double robustness). Theorem 2 (p. 11) bounds the bias by the product $\|\hat\pi-\pi^\star\|_2\cdot\sup_\theta\|\hat m(\theta,\cdot)-m^\star(\theta,\cdot)\|_2$.
  - Theorem 4 (p. 13): for split DRP, with probability $1-\delta$ the coverage is at least $1-\alpha-\frac{\|\hat\pi-\pi^\star\|_2\sup_\theta\|\hat m-m^\star\|_2}{P(T=1)}-C\sqrt{\frac{(m_0+\pi_0+1)\log(1/\delta)+1}{P(T=1)|I_2|}}$. Here $\pi_0$ bounds the estimated weights (assumption A2). Theorem 6 (p. 15) gives the full-data version, which needs entropy (covering-number) conditions (A4).
  - **Simulations** (§7). Kang–Schafer design: $n=2000$, $X\sim N(0,I_4)$, linear $Y$ with $N(0,1)$ noise, logistic propensity (eq. (21), p. 16). The airfoil data are also used with Tibshirani-style missingness. Nuisances are fitted with SuperLearner (random forest + GLM), and the propensity is **clipped at 0.99** (pp. 15–16). Over 500 runs (Table 1, p. 18), DRP variants cover 0.90 with width about 3.3 on synthetic data and cover 0.88–0.94 with width about 25–28 on airfoil. Weighted conformal (WCP) covers 0.97 / 0.99 with width 7.41 / 47.71, and gave **infinite intervals more than 50% (synthetic) and 90% (real) of the time**, which the authors truncated at 10 and 50 for plotting (p. 16).
  - In a conditional-coverage check with the CQR score, DRP is similar in coverage and narrower (Fig. 3). Efficient DRP beats choosing the tuning parameter by cross-validation in width while keeping coverage (Table 2, p. 20).
- **Key assumptions.** MAR, i.e. covariate shift (eq. (7)). Absolute continuity $Q_X\ll P_X$ (eq. (8)). Bounded nuisance estimates (A2). $\hat m$ monotone in $\theta$ (A3). At least one nuisance must be consistent. For the efficiency interpretation, $E[\pi^{\star2}]<\infty$ and a positive density at $r_\alpha$ (Lemma 1). The guarantees are asymptotic only.
- **Relation to the other papers.** It solves Tibshirani's problem with estimated weights and compares directly against WCP. **[Interpretation]** Its frequent infinite WCP intervals are the brief's "limited overlap" problem in concrete form: when one test weight $p^w_{n+1}(x)$ exceeds $\alpha$, Tibshirani's quantile is $+\infty$. Its §9 sensitivity model and Cauchois's f-divergence approach are two different ways to relax covariate shift. Yang (p. 22) contrasts its sensitivity parameterisation with Jin et al. (2021), which is not supplied.

## 3. How the papers fit together

**Common thread.** **[Paper]** All four start from split or full conformal and its rank-based guarantee, and all four replace the uniform empirical quantile of calibration scores with a *modified* quantile: weighted by a likelihood ratio (Tibshirani), weighted by fixed trust weights (Barber), taken at an inflated level (Cauchois), or defined as the root of an influence-function estimating equation (Yang). **[Interpretation]** One way to see it: each paper changes the calibration quantile so that it targets the right $(1-\alpha)$ quantile of the *test* score distribution, and they differ in what they assume about how the test distribution relates to the calibration one.

| | Tibshirani (WCP) | Barber (NexCP) | Cauchois (robust) | Yang (DRP) |
|---|---|---|---|---|
| Shift assumed | covariate shift, $P_{Y\mid X}$ fixed | none (bound in TV) | test score law in f-divergence ball | covariate shift (MAR) |
| Needs target covariates? | yes (to estimate $w$) | no (fixed weights from prior knowledge) | no (uses validation data to pick $\rho$) | yes |
| Weights | $w(X_i)$, data-dependent | fixed $w_i\in[0,1]$ | none (level inflation) | estimated $\hat\pi$ inside IF |
| Guarantee type | exact finite-sample (known $w$) | finite-sample, $1-\alpha-$gap | finite-sample if $\rho\ge\rho^\star$ | asymptotic, product-form bias |
| Behaviour under poor overlap | infinite intervals when $p^w_{n+1}>\alpha$ | n/a | n/a | bias slack grows with weight bound $\pi_0$ |
| Main tool | weighted exchangeability | swap + TV coupling | convex duality, DRO | semiparametric efficiency |

```
            exchangeable conformal (Vovk et al. 2005)
                         |
      +------------------+--------------------+
      | know HOW the shift happens?           | don't model the shift
      |                                       |
 covariate shift                      bounded "distance" to test law
      |                                       |
  known w  -> Tibshirani (exact)       fixed weights, TV  -> Barber
  unknown w-> Yang (DR, asymptotic)    f-divergence ball  -> Cauchois
```

**Axes of difference.** (i) How specific the shift assumption is (covariate shift versus general). (ii) Finite-sample versus asymptotic guarantees. (iii) Whether unlabelled target data are used. (iv) Whether the guarantee degrades gracefully when the assumption is wrong. Barber and Cauchois both give explicit degradation bounds, while for Tibshirani and Yang degradation is covered only by Yang's §9 sensitivity sketch.

**Settled.** **[Paper]** Exact finite-sample validity is achievable under covariate shift if $w$ is known (Tibshirani Cor. 1). It is *impossible* non-trivially if neither $w$ nor $P_{Y|X}$ is known (Yang Thm 1). Standard conformal is robust to mild non-exchangeability, with an explicit TV bound (Barber §4.3). Worst-case quantiles over f-divergence balls reduce to a single inflated quantile level (Cauchois Prop. 1).

**Unsettled.** **[Paper]** How to choose weights optimally (Barber p. 18). How to choose $\rho$, "the most glaring" open problem (Cauchois §6). How errors in estimated weights affect finite-sample WCP (raised by Yang p. 6). Whether efficient DRP is near-oracle (Yang §10). **[Interpretation]** Also unsettled, as far as these papers go: a systematic empirical comparison across shift severity and overlap, and principled weight truncation. These are exactly the gaps the brief targets.

## 4. Tie-in to the dissertation

### 4.1 What the proposed directions mean in practice

1. **Review conformal prediction under shift.** **[Interpretation]** A literature chapter organised around the table in §3, with the coverage proofs written out in your own notation: Tibshirani Lemma 1 and Lemma 3, Barber Thm 2 (a one-page proof, pp. 30–32), and Cauchois Prop. 1 at least in the TV case. Yang's influence-function machinery can be stated without proof.

2. **Implement and compare standard, importance-weighted and robust methods.** **[Interpretation]** Concretely, the following methods. Splitting the data three ways (model fit / weight fit / calibration) is the cleanest design and mirrors Yang's "three splits" recommendation (p. 17).
   - split conformal (Barber eq. (5));
   - weighted split conformal with oracle weights and with weights estimated by logistic regression and by a flexible classifier (Tibshirani eqs. (10), (12));
   - Cauchois's robust split conformal with $\chi^2$ or TV balls, with $\rho$ either fixed or chosen by Algorithm 1 or 2;
   - possibly NexCP with fixed similarity weights, as in Barber's election example;
   - for the extension, split DRP (Yang Alg. 1).

   Metrics should include:
   - marginal coverage and its spread across replications. The spread matters because Tibshirani (p. 6) shows weighting increases dispersion via the effective sample size;
   - mean and median width;
   - the fraction of infinite intervals. Yang reports more than 50% for WCP, so how infinite intervals are summarised must be decided up front;
   - coverage within covariate regions, as a conditional-coverage proxy (Yang Fig. 3; Cauchois's worst-slab coverage, eq. (10)).

3. **Simulation factors named in the brief, mapped to the papers.**
   - **Severity of covariate shift.** Use an exponential tilt $w(x)\propto\exp(a\,v^\top x)$ with severity $a$. This is exactly Tibshirani eq. (11) (airfoil) and Cauchois §1.3 ($a\in\pm\{0,\dots,0.64\}$ along the top principal component). Report severity as the effective sample size $\hat n$ (Tibshirani p. 6), a $\chi^2$ divergence (Cauchois App. C.1) or TV (Barber Thm 2) as well as $a$, so that results are comparable across designs. **[Interpretation]** With $X\sim N(0,I_d)$ and $\|v\|=1$ the tilted law is $N(av,I_d)$, and $E[w^2]/E[w]^2=e^{a^2}$, so the population effective sample size fraction is roughly $e^{-a^2}$. That gives a clean single dial (my own calculation; check it).
   - **Sample size.** Vary the calibration size $n$ and, for the estimated-weight methods, the number of unlabelled target points $m$. The theory predicts specific effects. The upper-bound slack is $1/(n+1)$ (Tibshirani Thm 1) or $\tilde w_{n+1}$ (Barber Thm 3). The Cauchois correction is $c/(n+1)$ (Cor. 2.1). Yang's slack is $O(|I_2|^{-1/2})$ plus the product bias (Thm 4). The dispersion of weighted coverage tracks $\hat n$, not $n$ (Tibshirani p. 8).
   - **Heteroscedasticity.** Use $Y=\mu(X)+\sigma(X)\varepsilon$ with $\sigma$ increasing along the tilt direction. This is the scenario where unweighted conformal fails, because the shift moves mass to high-noise regions. Tibshirani motivates the airfoil example by heteroscedasticity (p. 5). Cauchois's Example 4 and Lemma A.3 make the shift direction coincide with the variance direction. Barber §4.2 notes that changing $\mathrm{Var}(Y|X)$ can cause under- or over-coverage. Comparing the absolute-residual score with the CQR score (used in Yang §7 and Barber §5.3) is a natural second factor, because the CQR score adapts to heteroscedasticity.
   - **Source–target overlap.** Control overlap through the tail of $w$: larger tilts, or a target whose support sits at the edge of the source. The relevant papers say:
     - $\tilde P_X\ll P_X$ is required (Tibshirani Cor. 1; Yang eq. (8));
     - Yang's efficiency claim needs $E[\pi^{\star 2}]<\infty$ (Lemma 1), and its slack grows with the weight bound $\pi_0$ (Thm 4);
     - poor overlap produces infinite WCP intervals (Yang p. 16) and wide, highly variable intervals with random-forest weights (Tibshirani p. 8, footnote 3).

4. **Weight truncation.** **[Paper]** The only truncation in the papers is ad hoc clipping: classifier probabilities to [0.01, 0.99] (Tibshirani footnote 3) and the propensity at 0.99 (Yang p. 15), plus Yang's boundedness assumption A2. None of them analyses its effect. **[Interpretation]** In practice this means running WCP with $w_\tau=\min(w,\tau)$, or capping at a quantile of the estimated weights, and tracing coverage and width as functions of $\tau$. A clean result seems within reach. By Tibshirani Cor. 1 and Remark 3, WCP with $w_\tau$ is *exactly* valid for the tilted target $Q_\tau$ with $dQ_\tau\propto w_\tau\,dP_X$. Since the coverage event depends on the test point only through $(X_{n+1},Y_{n+1})$ and $P_{Y|X}$ is shared, coverage under the true target is at least $1-\alpha-d_{TV}(Q_\tau,\tilde P_X)$. That gives a bias–variance-style trade-off in $\tau$ that could be estimated and tested. This argument is mine, so check it with the supervisor. Barber's TV coupling (Thm 2) is the same flavour of argument.

5. **Doubly robust calibration.** Implement Yang's Algorithm 1. You need $\hat\pi$, which is the same classifier odds as Tibshirani eq. (12), and $\hat m(\theta,x)$, a conditional CDF of the score. **[Interpretation]** $\hat m$ is the fiddly part: one option is a binary regression of $\mathbb 1\{R\le\theta\}$ on $X$ over a grid of $\theta$ values with monotone rearrangement (Yang p. 12 cites Chernozhukov et al. 2009 for this); another is quantile regression forests. Then solve the one-dimensional equation by bisection. Experiments should deliberately misspecify one nuisance at a time to show double robustness. Kang–Schafer is the standard design for that (Yang §7.2).

6. **Departures from the covariate-shift assumption.** Let $P_{Y|X}$ change in the target as well, for example by inflating the noise or shifting the mean in a region, and measure how WCP and DRP break. Compare them with methods that do not assume covariate shift: Cauchois (valid if $D_f\le\rho$) and Barber (coverage gap bounded in TV). **[Paper]** Yang §9 gives the efficient influence function under an MNAR-style sensitivity model with known $\gamma(x,y)$ (Thm 7) but leaves nuisance estimation for future work. Barber p. 9 mentions label shift (Podkopaev & Ramdas, not supplied) as a reweighting variant.

### 4.2 What a dissertation would plausibly involve

**[Interpretation]** Roughly: no heavy proofs are required, implementation is substantial but standard (R or Python, small models), there is a large designed simulation, and one or two real datasets are needed. Two plausible shapes:

- **Shape A, a careful comparative study (safest).**
  - Chapter 1: conformal foundations with proofs.
  - Chapter 2: the four approaches, with proofs of Tibshirani Cor. 1 and Barber Thm 2.
  - Chapter 3: a factorial simulation (severity × $n$ × heteroscedasticity × overlap × score type) comparing split CP, oracle and estimated WCP, Cauchois-robust and split DRP.
  - Chapter 4: real data, for example airfoil with induced tilting (as in Tibshirani and Yang) plus one dataset with natural shift, such as ELEC2 (Barber) or a UCI set split on a covariate.
  - Chapter 5: practical recommendations, for example when WCP returns infinite intervals and when the robust method is too conservative.

- **Shape B, a methodological focus on overlap and truncation (more ambitious).**
  - Do the same review and core comparison, but make weight truncation the centrepiece.
  - State and prove a coverage bound for truncated WCP, for example the TV argument in 4.1(4).
  - Propose a data-driven choice of $\tau$, for example by estimating $d_{TV}(Q_\tau,\tilde P_X)$ from target covariates or by targeting a minimum effective sample size, as Barber does with its effective-size-100 tuning on p. 27.
  - Compare truncated WCP with DRP, whose bias slack also depends on the weight bound, under decreasing overlap.
  - A shorter real-data section.

### 4.3 Open questions

From the papers' own limitations and future-work remarks:

- **Choosing the robustness level $\rho$** is "the most glaring" open question (Cauchois §6, p. 30). The paper suggests matching projected covariate statistics on new test data to calibrate it. A related open problem is identifying sensitive *directions* rather than single covariates (Cauchois App. C.3, p. 49).
- **Optimal weights for NexCP**, and even how to define optimality (Barber §4.3, p. 18). Barber also asks whether one can tell adaptively, from the data, whether the coverage gap is likely to be large (p. 18).
- **Data-dependent weights** in Barber's framework, which would unify it with WCP and localised conformal prediction, are left for future work (Barber §4.5, pp. 20–21).
- **Non-symmetric algorithms that are sensitive to the swap step**, for example autoregressive models (Barber §3.2, p. 15).
- **The effect of estimating $w$** on WCP's finite-sample coverage is not analysed by Tibshirani (raised by Yang p. 6). Estimating high-dimensional density ratios is hard. Tibshirani §4 suggests exploiting low-dimensional structure ($Z\to X\to Y$) as future work.
- **No upper bound on WCP coverage** without conditions on the weights (Tibshirani Remark 5), which relates to over-coverage and width.
- **Local or conditional coverage.** Tibshirani's kernel-weighted construction needs the centre point fixed in advance, and "many important practical and philosophical problems … remain open" (p. 15).
- **DRP open items:**
  - prove that efficient DRP is nearly oracle-efficient (Yang §10);
  - estimate nuisances in the latent-shift sensitivity model (Yang §§9–10);
  - use higher-order influence functions to shrink the product bias (Yang p. 23);
  - the finite-sample impossibility result (Yang Thm 1) means any DRP-type guarantee will be asymptotic.

## 5. Background knowledge required

| Area | Item | Status | Rough effort if not covered | Where it's needed |
|---|---|---|---|---|
| Statistics | Quantiles, order statistics, ranks under exchangeability | partly covered | a few days | All coverage proofs (Tibshirani Lemma 1; Barber §6.1) |
| Maths | Exchangeability and permutation invariance | partly covered | a few days | Foundations, Tibshirani §3 |
| Maths | Radon–Nikodym derivatives, likelihood ratios, absolute continuity | covered by my modules (measure-theoretic probability) | – | Tibshirani Cor. 1, Lemma 2; Yang eq. (8) |
| Maths | Total variation distance, coupling | partly covered | a few days | Barber Thm 2, Lemma 1 |
| Maths | f-divergences (KL, $\chi^2$, Rényi), convex duality | new to me | 1–2 weeks | Cauchois §2, §4 |
| Statistics | Importance sampling and effective sample size | partly covered | a few days | Tibshirani p. 6; weight truncation |
| CS-ML | Density-ratio estimation by probabilistic classification | partly covered (logistic regression yes; framing new) | a few days | Tibshirani eq. (12); Yang $\hat\pi$ |
| CS-ML | Random forests, gradient boosting, SuperLearner-style stacking | partly covered | about a week | Weight and nuisance estimation (Tibshirani §2.3; Yang §7) |
| Statistics | Quantile regression and conformalised quantile regression (CQR) | partly covered | about a week | Heteroscedastic designs; Yang §7, Barber §5.3 |
| Statistics | Missing data (MAR / MNAR), propensity scores | new to me (some econometrics exposure helps) | about a week | Yang §3.2, §9 |
| Statistics | Semiparametric efficiency, influence functions, double robustness | new to me | substantial: 3–4 weeks to use, a term-length topic to master | Yang §5 throughout |
| Maths | Empirical processes (DKW, covering numbers, VC dimension) | new to me | 2–3 weeks (to read proofs); not needed to apply methods | Yang Thms 3, 5; Cauchois Thm 2 |
| Statistics | Causal inference basics (potential outcomes, unconfoundedness) | partly covered (econometrics) | a few days | Yang App. S.2; context only |
| CS-ML | RKHS methods | new to me | about a week; optional | Cauchois §3.2, App. A.2 only |
| CS-ML | Simulation design and reproducible R/Python (parallel replications) | partly covered | 1–2 weeks | Whole project |
| CS-ML | Deep classifiers (ResNet) | covered by my modules (basics) | – | Only to reproduce Cauchois §5.1; not necessary |

**Biggest gap.** **[Interpretation]** Semiparametric theory is the biggest gap: influence functions, double robustness and the empirical-process arguments behind Yang's theorems are new to you and are a substantial topic on their own. The good news is that the brief makes doubly robust calibration optional, and implementing Yang's Algorithm 1 needs only the estimating equation (eq. (13)) and two ordinary regressions, not the theory. The f-divergence material for Cauchois is the second gap, but the TV and $\chi^2$ closed forms (Example 1, p. 11) keep it manageable.

## 6. Practicalities

### Code
- **[Paper]** Tibshirani: "R code to reproduce these simulation results can be found at http://www.github.com/ryantibs/conformal/" (p. 5).
- **[Paper]** Barber: code for §5.1–5.2 and App. F at https://rinafb.github.io/code/nonexchangeable_conformal.zip (p. 22 footnote; p. 60).
- **[Paper]** Cauchois: no code link appears in the supplied PDF.
- **[Paper]** Yang: no code link appears in the supplied PDF. It mentions R's SuperLearner (Polley & van der Laan) for nuisance fitting and R's `smooth.spline` (pp. 15–16).
- **[Interpretation]** Everything core (split CP, WCP, TV/$\chi^2$ robust CP) takes a few dozen lines in R or Python. I have not checked whether the cited links still work.

### Data
- **[Paper]** **Airfoil** (UCI repository; cited with URL; used by Tibshirani §2.3 and Yang §7.1). Shift is induced artificially by tilting.
- **[Paper]** **Kang–Schafer synthetic design** (Yang §7.2).
- **[Paper]** **ELEC2 electricity** (Barber §5.2; obtained from a Kaggle URL given on p. 24).
- **[Paper]** **2020 US election county data** (Barber §5.3, App. G; built from US Census Bureau and USDA ERS downloads, MIT Election Data and Science Lab, and Dave Leip's Atlas).
- **[Paper]** **Nine UCI regression sets**: abalone, ailerons, airfoil, banking, Boston and California housing, delta ailerons, kinematics, puma (Cauchois §1.3, App. C.1). Also real-estate, weather-history and wine-quality UCI sets (App. C.3).
- **[Paper]** **CIFAR-10 / CIFAR-10.1 v4, MNIST / QMNIST50K, ImageNet / ImageNetV2** (Cauchois §5.1).
- **[Paper]** **COVID-19 county positivity** from CMU DELPHI (Cauchois App. C.2).
- **[Paper]** None of the papers explicitly calls these datasets "public". They give repository names or URLs (UCI, Kaggle, Census) from which the data were obtained.
- **[Interpretation]** UCI and ELEC2 look straightforward to get. I cannot tell from the papers whether all election sources (for example Leip's Atlas) are freely available.

### Compute
- **[Paper]** None of the papers reports hardware or run times.
- **[Paper]** Scale of the experiments:
  - Tibshirani: 5000 replications of linear-regression split conformal on 1503 points;
  - Barber: full conformal with least squares at about 1900 time points × 200 replications, with $N=2000$;
  - Yang: 500 Monte Carlo runs with SuperLearner (random forest + GLM) at $n=2000$;
  - Cauchois: ResNet-50 models trained on CIFAR-10, MNIST and ImageNet (the paper gives no GPU details).
- **[Interpretation]** Everything except Cauchois's image experiments is laptop-scale. Split-conformal simulations with thousands of replications take minutes. DRP with random-forest nuisances over a factorial design may take hours, which is easily parallelised or run on the LSE cluster. Full conformal is only cheap for least squares or ridge (Barber p. 7), so I would use split conformal throughout. If an image example is wanted, use a pretrained classifier and conformalise only, but this is not needed for the brief.

## 7. Questions for the proposal meeting

1. **Which "robust" methods are in scope: Cauchois's f-divergence sets, Barber's NexCP, or both?** The brief lists both under "other approaches". This decides whether the core comparison has three or four arms, and how much new theory (TV coupling versus convex duality) you need to learn.
2. **Is the target marginal coverage only, or should conditional or local coverage be evaluated (for example coverage in covariate regions)?** All the guarantees are marginal, but heteroscedastic designs reveal big conditional failures (Cauchois Ex. 4; Yang Fig. 3). The answer shapes the evaluation metrics.
3. **How should infinite WCP intervals be reported and compared?** Yang found them in more than 50–90% of cases and truncated widths at an arbitrary value for plotting. The choice (median width, fraction infinite, capped mean) can change which method looks best.
4. **What exactly does "weight truncation" mean here: clipping classifier probabilities, capping $w$ at a fixed value, or capping at a weight quantile? Is a theoretical justification expected or just empirical?** The papers only clip ad hoc (Tibshirani fn. 3; Yang p. 15). A coverage bound like the TV argument in 4.1(4) is possible, but it changes the project's character.
5. **Is any original theory expected, or is a well-designed empirical study enough for a distinction?** The brief says only "capable students may explore". Knowing this up front determines how much reading time goes to Yang's semiparametric proofs.
6. **Which score functions should be used: the absolute residual only, or also CQR / locally weighted residuals?** The score interacts strongly with heteroscedasticity and therefore with how badly unweighted conformal fails under shift.
7. **For estimated weights, how many unlabelled target covariates should be assumed, and which classifiers?** Tibshirani's well-specified logistic case is optimistic. Misspecified or flexible classifiers are where overlap problems show up (random-forest weights, Tibshirani p. 8).
8. **How should $\rho$ be set for Cauchois in a fair comparison: oracle divergence, a fixed grid, or the paper's data-driven Algorithms 1 and 2?** The robust method's coverage and width depend entirely on $\rho$, and the paper admits its selection rules are heuristic.
9. **Which real datasets: induced shift on a standard set (airfoil-style tilting, where truth is known), or natural shift (ELEC2, election), or both?** With induced shift you can compute the oracle weights and divergences. With natural shift covariate shift may not hold, which links to the "departures" extension.
10. **For "departures from covariate shift", which kind of departure: concept shift in $P_{Y|X}$, label shift, or latent confounding as in Yang §9?** Each points to a different comparator (Cauchois/Barber versus a Yang-style sensitivity analysis), and Yang leaves nuisance estimation in §9 unsolved.
11. **R or Python, and is it acceptable to build on the authors' released code (Tibshirani's R package, Barber's zip)?** This affects time spent on implementation versus experiments.
12. **The brief cites Yang et al. (2024) and Cauchois et al. (2024); the supplied Yang PDF is arXiv v3 (Dec 2022). Are there important differences in the published versions?** I can only vouch for what is in the supplied versions.
