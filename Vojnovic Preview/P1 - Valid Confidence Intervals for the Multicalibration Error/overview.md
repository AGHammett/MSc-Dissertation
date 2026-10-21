# How Multicalibrated Is a Model? Valid Confidence Intervals for the Multicalibration Error: Overview

**Supervisor:** Professor Milan Vojnović · **Prepared:** 21 October 2026 · **Sources:** the brief and the 4 supplied papers only

> **Labels.** **[Paper]** a paper states it (with reference) · **[Brief]** the brief states it · **[Interpretation]** my own reading. Check it before relying on it.

## 1. The brief

**[Brief]** A probabilistic classifier $f$ is *multicalibrated* if it is calibrated within every group in a given, possibly overlapping and possibly very large, collection of subpopulations. Calibrated here means that among cases given probability $v$, about a fraction $v$ have the event happen. The project's target is a single summary number: the **largest calibration gap over groups and over bands of predicted probability**, restricted to groups above a stated minimum size. An extension covers groups defined by a rich function class. Because the largest of many estimated gaps is picked using the same data that estimate it, the naive estimate is biased upwards, and a naive confidence interval can fall short of its stated coverage. The brief describes two existing approaches without naming them. I have checked both against the papers. (i) "Bootstrap-based bounds that hold for every group at once, with asymptotically exact coverage, … for auditing model performance over groups, with multicalibration as an application" is **Cherian & Candès, *Statistical Inference for Fairness Auditing*** (JMLR 2024). It matches their Theorem 4 (simultaneous lower bounds with limiting coverage exactly $1-\alpha$) and their Appendix A (multicalibration as a special case). (ii) "Inference for the largest or smallest value of a collection of estimated quantities … in econometrics, with a selection step that shortens the interval" is **Chernozhukov, Lee & Rosen, *Intersection Bounds: Estimation and Inference*** (arXiv 0907.3503v5). It matches their inference on $\inf_v\theta(v)$ / $\sup_v\theta(v)$ with the "adaptive inequality selection" set estimator $\widehat V_n$ (eq. 3.5). Both guarantees are asymptotic. The research question asks how far an interval for the worst-group gap can be shortened below the one implied by the all-groups bounds while keeping its stated coverage. The shortening would come from using the fact that the target is a *maximum*, and from the structure of the groups (nesting, overlap). The deliverable is **one result**. Either (a) such an interval, with a coverage proof and a width comparison against both the all-groups interval and sample splitting, or (b) a proof that, for a stated group structure, no valid interval is substantially shorter. An open-source implementation is optional. The brief says the work combines proof and simulation.

**Project type:** mainly **theoretical**, with a methodological and computational part. The deliverable is a theorem: a coverage guarantee plus a width comparison, or a lower bound. Simulations are there to check and illustrate that theorem, not to stand as the contribution themselves. Real data is optional.

## 2. Paper by paper

Recommended reading order: **(1) Hébert-Johnson et al.** defines the object. **(2) Guy et al.** shows the "maximum over many groups" summary in practice and how noisy it is. **(3) Cherian & Candès** is the baseline the project must beat. **(4) Chernozhukov, Lee & Rosen** is the heaviest paper and supplies the selection idea the project would borrow. Read 1 and 2 quickly, as they give motivation and vocabulary. Read 3 closely, including Appendix A and the Theorem 4 proof sketch. Read 4's Sections 1–3, 4.1 (Example 1) and 6.1 closely, and leave the series/kernel and strong-approximation material (Sections 4.2–5, Appendices D–J) for reference.

### 2.1 Multicalibration (Hébert-Johnson, Kim, Reingold & Rothblum, 2018)
*Proceedings of the 35th International Conference on Machine Learning (ICML), PMLR 80, 2018. 10-page conference version; full proofs are deferred to supplementary material and an archival version that is not supplied. No printed page numbers, so I cite sections.*

- **Problem.** **[Paper]** Ordinary calibration over a few large protected groups is too coarse. A predictor can be calibrated on a group $S$ while giving every member the group average, which harms its high-risk or high-ability members (§1). Calibration on *every* subset is impossible from a finite sample. The paper wants something in between: calibration on every subpopulation in a collection $\mathcal C$ of "computationally identifiable" sets (§1).
- **Approach.** **[Paper]** Definitions (§2): $f$ is $\alpha$-calibrated on $S$ if, on some $S'\subseteq S$ holding a $(1-\alpha)$ fraction of $S$'s mass, $|\mathbb E_{i\sim S_v\cap S'}[f_i-p^*_i]|\le\alpha$ for every value $v$, where $S_v=\{i:f_i=v\}$. Then $f$ is $(\mathcal C,\alpha)$-multicalibrated if it is $\alpha$-calibrated on every $S\in\mathcal C$. Predictions are discretised into $1/\lambda$ bands $\lambda(v)=[v-\lambda/2,v+\lambda/2)$, which are the brief's "bands of predicted probability". Algorithm 1 (§3.1) is a boosting-like loop. It finds a (set, band) cell whose average prediction is off and shifts predictions there. Cells with mass below $\alpha\lambda\Pr[S]$ are skipped. Statistical queries go through a differential-privacy-style "guess-and-check" oracle so that adaptively chosen queries still generalise.
- **Main findings and results.** **[Paper]** Theorem 1: if every $S\in\mathcal C$ has $\Pr[S]\ge\gamma$ and circuit size $s$, a $(\mathcal C,\alpha)$-multicalibrated predictor exists with circuit size $O(s/(\alpha^4\gamma))$. Theorem 2: Algorithm 1 with $\lambda=\alpha$ learns a $(\mathcal C,2\alpha)$-multicalibrated predictor from $O(\log|\mathcal C|/(\alpha^{11/2}\gamma^{3/2}))$ samples in time $O(|\mathcal C|\,t\,\mathrm{poly}(1/\alpha,1/\gamma))$. Theorems 3–4 (§4) show that learning a multicalibrated predictor is computationally equivalent to weak agnostic learning of $\mathcal C$. Theorem 5 (§5): multicalibrating does not hurt squared error by more than $6\alpha$ relative to a benchmark class. There are no experiments.
- **Key assumptions.** **[Paper]** Binary outcomes $o_i\sim\mathrm{Ber}(p^*_i)$, independent. A lower bound $\gamma$ on group mass, which is the origin of the brief's "minimum size". Footnote 1 in §2 says how much representation is needed in practice is an open empirical question. The theory is in the statistical-query / circuit-complexity tradition. It gives **no confidence intervals** for the multicalibration error.
- **Relation to the other papers.** It supplies the definition that Cherian & Candès audit (their App. A cites "$\gamma$-multicalibration") and that Guy et al. measure. **[Interpretation]** The brief's target, $\max_{S,v}|\text{gap}|$ over groups with $\Pr[S]\ge\gamma$, is essentially the smallest $\alpha$ for which a binned, size-thresholded version of this definition holds. It ignores the "$(1-\alpha)$-fraction" exception, so the brief's target is a simplified version of the definition. That is worth confirming in the meeting (§7).

### 2.2 Measuring multi-calibration (Guy, Haimovich, Linder, Okati, Perini, Tax & Tygert, 2025/26)
*arXiv:2506.11251v2 [stat.ME], 15 April 2026 (Meta). 25 pages.*

- **Problem.** **[Paper]** Practitioners need one scalar that measures distance from perfect multicalibration (§1.1). Binned metrics (ECE, ICI) are statistically unsatisfactory (App. D), and a plain maximum over many subpopulations is dominated by noise from the small ones (§1.2, §3.5).
- **Approach.** **[Paper]** For each subpopulation $k$ (with $k=0$ the full population), sort by score and form cumulative differences $C^k_j$ of responses minus scores (eq. 1). Take the Kuiper range $D_k=\max_j C^k_j-\min_j C^k_j$ (eq. 2–3), which avoids binning. Normalise by $\sigma_k$, the standard deviation of the final cumulative difference *under the null of perfect calibration* (eq. 5). The metric is $M=\max_{0\le k\le \ell} D_k\sigma_0/\sigma_k$ (eq. 4). Scores are treated as fixed and responses as independent Bernoulli (§2.1). Subpopulations come from a randomised algorithm that takes paths in a binary tree of median splits on covariates (§2.3, Algorithm 1). This produces **nested** chains of groups with a minimum size $m$ (default 10).
- **Main findings and results.** **[Paper]** On ACS 2019 (California, Orange County: 10,680 households, 233 covariates) and KDD Cup 1998 (80,796 people, 324 covariates), with $\ell=1000$ subpopulations, $m=10$ and three models (logistic regression, CART, LightGBM) × several calibration methods, there are 72 configurations (§3.1–3.4, App. G). Without the $\sigma_k$ normalisation, the "multi-ablate" metric $\max_k D_k$ is "completely useless". It is large everywhere and only a few times its null expectation, because it locks onto noise in the smallest groups (§3.3 end, §3.5). Isotonic regression is a strong calibration baseline (§3.3, §3.5). $M$ is usually clearly larger than the full-population Kuiper metric, so subgroup miscalibration is real (§3 intro). App. F gives a closed-form synthetic test case.
- **Key assumptions.** **[Paper]** Fixed scores, independent responses, null-calibrated variance used for weighting. The authors say $M$ is most informative when subpopulations are nearly calibrated. When calibration is poor, the weighting suppresses small groups (§3.5). The "±" values in App. G are spreads over three random seeds of the group generator, **not** confidence intervals for the population quantity (App. G).
- **Relation to the other papers.** It is a measurement paper. It uses the HKRR definition but a different, unbinned and normalised, functional. **[Interpretation]** Its "multi-ablate" result is a vivid empirical picture of the upward selection bias the brief describes. Its nested tree groups are a natural example of the "nesting" structure the brief wants to exploit. It offers **no inference** for $M$. Whether the subpopulations are generated on the same test data used to evaluate $M$ is not stated clearly in the text. If they are, that is a further selection effect.

### 2.3 Statistical Inference for Fairness Auditing (Cherian & Candès, 2024)
*Journal of Machine Learning Research 25 (2024) 1–49; submitted 6/23, published 5/24.*

- **Problem.** **[Paper]** Given only a held-out "audit trail" $\{(X_i,Y_i)\}_{i\le n}\overset{iid}\sim P$ and predictions of a fixed black-box $f$, (1) *certify* groups where performance is acceptable and (2) *flag* groups with harmful disparity, with formal error control over a rich, possibly infinite, collection $\mathcal G$ (§1, §2.1). The disparity is $\epsilon(G)=\mathbb E_P[L(f(X),Y)\mid G]-\theta_P$ (Definition 1, eq. 1).
- **Approach.** **[Paper]** *Bound certification* (§3.1.1): a naive constant correction from $\sup_G\{\hat\epsilon(G)-\epsilon(G)\}$ fails, because small groups do not converge uniformly (p. 7). So they bootstrap the stabilised process $\sup_G P(G)P_n(G)(\hat\epsilon(G)-\epsilon(G))$ (eq. 4, Algorithm 1, p. 8) and set $\mathrm{lb}(G)=\hat\epsilon(G)-t^*/P_n(G)^2$ (eq. 5). Because that bound behaves like $|G|^{-1/2}P_n(G)^{-3/2}$ and is vacuous for small groups (p. 8, Fig. 3), they rescale by $\hat s(G)$ (eq. 7–9, Algorithm 2). This interpolates between a Wald-type scaling for groups above a threshold $p^*$ and a pooled variance for tiny groups, with a hyperparameter $w_0$. *Boolean certification* (§3.1.2, Algorithm 3) and *flagging* with BH/FDR (§4, Algorithm 4) are variants. §5 extends from group indicators to non-negative tilts, including the unit ball of an RKHS (Algorithm 5).
- **Main findings and results.** **[Paper]** Theorem 4 (p. 10): if $L$ is bounded and $\mathcal G$ has finite VC dimension, then $\lim_n P(\mathrm{lb}(G)\le\epsilon(G)\ \forall G)=1-\alpha$, i.e. **asymptotically exact simultaneous coverage**. Theorem 7 (p. 12): FWER control for Boolean certificates, exact only when $\epsilon(G)=\varepsilon$ for all $G$. Proposition 8 (p. 18): asymptotic FDR control for disjoint groups or binary $L$. Theorem 9 (p. 22): simultaneous RKHS bounds, with coverage $\ge 1-\alpha$ (conservative). Simulations (Tables 1–2, pp. 14–15; 200 trials, $B=500$, $\alpha=0.1$, $|\mathcal G|=1275$ intervals) show nominal coverage only at larger $n$. Realised simultaneous coverage is 0.81–0.87 for $n\le400$ and 0.88–0.91 at $n=1600$. Real data: COMPAS (PPV and FPR disparities, $n=6781$, 48–58 intersectional groups) and Folktables income prediction (89 groups). **Multicalibration appears only in Appendix A (p. 28).** Set $L=Y-f(X)$, $\theta_P=0$ and $\mathcal G=\{G\cap\{f(X)=v\}\}$. The bound on the multicalibration level $\gamma$ is "the maximum (absolute) value taken over all issued intervals". It is not run in any experiment.
- **Key assumptions.** **[Paper]** i.i.d. holdout data, model fixed. $L$ bounded (or finite variance for finite $\mathcal G$). Finite VC dimension. Asymptotically linear target estimator (Assumption 1). Countability/measurability is assumed for convenience (App. B, after Theorem 12). Groups are not excluded by size, but $p^*$ plays a similar role (App. A).
- **Relation to the other papers.** This is the brief's "all-groups" baseline. **[Interpretation]** Simultaneous coverage of every $\epsilon(G_v)$ automatically gives a valid interval for $\max|\epsilon|$. But it pays for *all* groups, including those nowhere near the maximum. Exactly that slack is what CLR-style selection is designed to remove. Its Algorithm 1 statistic is a sup of a bootstrapped empirical process. That is the same object CLR approximate with Gaussian processes.

### 2.4 Intersection Bounds: Estimation and Inference (Chernozhukov, Lee & Rosen, 2013)
*arXiv:0907.3503v5 [math.ST], 3 May 2013 (dated March 2013; first version December 2007). 110 pages: main text pp. 1–45, Appendices A–D pp. 45–60, references and tables to p. 66, online supplement (Appendices E–L) pp. 67–110. Printed page numbers coincide with PDF pages.*

- **Problem.** **[Paper]** In partial identification a parameter satisfies $\theta^*\le\theta_0:=\inf_{v\in\mathcal V}\theta(v)$ (or a sup lower bound) for a bounding function estimated from data (§1, eq. 1.1; §2, eq. 2.5). The plug-in $\inf_v\hat\theta(v)$ is **downward biased**, and unequal precision across $v$ distorts it further (pp. 3–4, 12; Figs. 1–4). The ordinary bootstrap is not generally consistent here (p. 3). Hirano & Porter (2012), cited on p. 4, show that unbiased estimation is impossible.
- **Approach.** **[Paper]** *Precision correction*: $\hat\theta_{n0}(p)=\inf_{v}[\hat\theta_n(v)+k\,s_n(v)]$ (eq. 2.6, Definition 1/eq. 3.7, p. 19). Here $s_n$ is the pointwise standard error and $k$ a critical value. Taking $p=1-\alpha$ gives a one-sided confidence bound. Taking $p=1/2$ gives a half-median-unbiased point estimator. The critical value is a quantile of $\sup_{v\in V}Z_n^*(v)$, where $Z_n^*$ is a Gaussian "penultimate" process strongly approximating the studentised estimation error (Conditions C.1–C.4, pp. 15–17). The key step is **adaptive inequality selection (AIS)**. It first computes a conservative critical value over all of $\mathcal V$ at level $\gamma_n=1-0.1/\log n$. It then keeps only near-minimisers, $\widehat V_n=\{v:\hat\theta_n(v)\le\inf_{\tilde v}(\hat\theta_n(\tilde v)+k s_n(\tilde v))+2k s_n(v)\}$ (eq. 3.5). The final critical value is the $p$-quantile of the sup over $\widehat V_n$ only (eq. 3.6). Critical values can be analytical (Definition 2) or, preferably, simulated (Definition 3, eq. 3.11).
- **Main findings and results.** **[Paper]** Lemma 1 (p. 17): inference "concentrates" on a shrinking neighbourhood $V_n$ of the argmin set $V_0$. Lemma 2 (p. 21): $V_n\subseteq\widehat V_n\subseteq\overline V_n$ with probability → 1, plus a rate for $\widehat V_n\to V_0$ under an identifiability Condition V. Theorems 1–2 (pp. 20–21): asymptotic level $\ge p$, estimation error $\lesssim\bar\sigma_n\bar a_n$, power against alternatives farther than that. Theorem 3 (p. 22): under Conditions V and S (for example a unique, locally quadratic minimiser) the procedure has **exact** asymptotic size and the critical value tends to the normal quantile (Remark 1, p. 18). **Example 1 (p. 23) is the finite, "saturated" case** $\mathcal V=\{1,\dots,k\}$, $\theta(j)=\beta_j$. Theorem 4 (p. 24) gives validity with $O(n^{-1/2})$ error there, and exact size under Condition V. §6.1 spells out the finite case algorithmically (pp. 38–39). Series (Theorem 5) and kernel (Theorem 6) estimators cover continuous $v$. Theorem 7 (§5) is a new strong approximation for series estimators. Monte Carlo (§7, Tables 1–4): coverage 0.98–0.99 in non-flat designs. The method beats Andrews–Shi's CvM test when the bounding function is peaked and loses when it is flat. "Neither approach dominates" (pp. 43–44, App. K).
- **Key assumptions.** **[Paper]** Strong approximation by Gaussian processes with unit variance (C.2). Concentration of their suprema (C.3, via Talagrand–Samorodnitsky, Lemma 12). Uniformly consistent standard errors (C.4). Anti-concentration from Chernozhukov–Chetverikov–Kato (Lemma 10, p. 46; that paper is not supplied). The framework allows the law $P_n$ to change with $n$ (§3.1). In the parametric case the dimension $k$ is **fixed** (Condition P). Growing dimension is handled only through the series case, with growth restrictions (Condition NS, p. 27).
- **Relation to the other papers.** It supplies the "selection step that shortens the interval". **[Interpretation]** Mapping: the multicalibration error is a supremum over a finite index $v=(G,\text{band},\pm)$ of estimated means, i.e. Example 1 with $\sup$ in place of $\inf$ (§7 footnote 22: "not a substantive difference"). CLR's procedure covers the side of a sup that suffers from selection (the lower confidence bound). It was designed for fixed, moderate $k$, not for thousands of overlapping groups whose number may grow with $n$, and not with the absolute-value or minimum-size features of the multicalibration target.

## 3. How the papers fit together

**Common thread.** Every paper deals with a quantity of the form "worst case over many subpopulations". HKRR *define* it and show it is achievable. Guy et al. *measure* it and show that naive maxima are dominated by noise. Cherian & Candès *bound every component simultaneously*. CLR *do inference directly on the extremum*, using selection to discard irrelevant components.

```
            definition                 point summary            inference
HKRR 2018  ──────────►  Guy et al.  ─────────►  (no CI)
 (target, γ, bands)     (max of normalised
                         Kuiper gaps; noise of
                         small groups)
                                                 ┌─ Cherian & Candès: bound EVERY group
                                                 │   (bootstrap sup-process; exact
  brief's target: max_{G,b} |gap(G,b)| ──────────┤    simultaneous coverage)
                                                 │
                                                 └─ CLR: bound the EXTREMUM only
                                                     (Gaussian sup + adaptive selection;
                                                      exact size only when argmax is
                                                      well identified)
```

| Axis | HKRR | Guy et al. | Cherian & Candès | CLR |
|---|---|---|---|---|
| Goal | learn a multicalibrated $f$ | scalar metric | simultaneous bounds / tests | CI for $\inf$/$\sup$ |
| Gap functional | binned, $\Pr[S]\ge\gamma$ | Kuiper, $\sigma$-normalised | any mean disparity; binned MC in App. A | any estimable $\theta(v)$ |
| Groups | arbitrary $\mathcal C$, large | random nested tree paths | VC class or RKHS tilts | finite or continuum $\mathcal V\subset\mathbb R^d$ |
| Uncertainty | SQ-oracle tolerance | null SD only | bootstrap, asymptotically exact | strong approx., asymptotic, exact only under V+S |
| Uses "target is a max"? | – | yes (definition) | no (all groups) | yes (selection) |

**Settled (within these papers).** Multicalibration is attainable without accuracy cost (HKRR Thm 5). Naive maxima over small groups are noise-dominated (Guy et al. §3.5). Simultaneous bounds over a VC class with asymptotically exact coverage exist and are computable for finite collections (CC Thm 4). For a finite collection of fixed size with a well-separated extremum, one-sided inference on the extremum can have exact size and a normal-quantile critical value (CLR Thm 3–4).

**Unsettled.** **[Interpretation]**
- Nobody in this set gives an interval *for the multicalibration error itself* that is better than "the max of simultaneous intervals".
- CLR's guarantees are for fixed $k$ (or smooth continua), while multicalibration needs very many, overlapping, possibly growing collections.
- When are the gains from selection real? Exactly where CLR are sharp: a unique worst cell. Exactly where they vanish: flat or tied configurations, which includes the important case of a nearly perfectly multicalibrated model.
- No paper here gives a lower bound on the achievable width.

## 4. Tie-in to the dissertation

Notation used below (**[Interpretation]**, my formalisation of the brief). Let $\mathcal V=\{(G,b,s)\}$ index group $G$, probability band $B_b$ and sign $s\in\{\pm1\}$, restricted to cells passing the size threshold. Define $\theta(v)=s\cdot\mathbb E[Y-f(X)\mid X\in G,\ f(X)\in B_b]$. The target is
$$M=\max_{v\in\mathcal V}\theta(v)=\max_{G,b}\big|\mathbb E[Y-f(X)\mid G,B_b]\big|.$$
Each $\hat\theta(v)$ is a ratio of sample means, hence asymptotically linear. That fits CC's Assumption 1 and the "saturated model" of CLR Example 1.

### 4.1 What the proposed directions mean in practice

**Direction 1: use the fact that the target is a maximum.** **[Interpretation]** The two ends of an interval for a maximum behave very differently.
- *Upper end.* $U=\max_v[\hat\theta(v)+c\,s(v)]$ is valid as soon as the single cell $v^{*}$ achieving $M$ is covered, because $U\ge\hat\theta(v^{*})+c\,s(v^{*})$ and the event $\hat\theta(v^{*})+c\,s(v^{*})\ge\theta(v^{*})=M$ involves only one fixed cell. So a *pointwise* critical value $c=z_{1-\alpha_2}$ already suffices asymptotically. The all-groups interval instead uses a simultaneous critical value here.
- *Lower end.* $L=\max_v[\hat\theta(v)-k\,s(v)]$ must hold for *every* $v$, so it needs a max-type critical value. This is the side affected by the upward selection bias, and it is the side CLR's machinery handles: their one-sided bound for an $\inf$ (eq. 3.7), mirrored for a $\sup$ as in §6 (pp. 37–38) and §7 footnote 22. Concretely you would (i) compute the studentised Gaussian or multiplier-bootstrap sup over all cells at level $1-0.1/\log n$; (ii) keep only the near-maximal cells $\widehat V_n$ (eq. 3.5 mirrored); (iii) recompute the critical value over $\widehat V_n$ only.

Doing this means re-deriving CLR's Lemma 1, Lemma 2 and Theorem 2 for the multicalibration index set. Please check the upper-end argument carefully: it is my own, not something any paper states.

**Direction 2: use the group structure (nesting, overlap).** **[Interpretation]** Structure enters in two places. (a) The correlation of $\{\hat\theta(v)\}$. Nested groups (like Guy et al.'s tree paths) share data and are highly correlated, so the effective number of cells, and hence the sup quantile, is smaller than $|\mathcal V|$. A simulated critical value (CLR Definition 3; CC Algorithm 1) uses this automatically. A theorem would need to *quantify* it, e.g. bound $\mathbb E\sup_{v\in\widehat V_n}Z^{*}(v)$ for tree-structured or intersection-structured families. (b) The selection step itself. One could prune whole subtrees whose upper confidence bound is below the current lower bound, possibly iterated as a step-down, which CLR mention but omit (footnote 2, p. 3).

**Direction 3: compare with the all-groups interval and with sample splitting.** **[Brief]** Both comparisons are required. **[Interpretation]**
- *All-groups interval:* take CC's simultaneous intervals (Algorithm 1 unscaled or Algorithm 2 rescaled) for every cell, and set the interval for $M$ to [max of lower ends of $|\cdot|$, max of upper ends].
- *Sample splitting:* pick $\hat v=\arg\max$ on split 1 and form a normal CI for $\theta(\hat v)$ on split 2. Because $\theta(\hat v)\le M$, its lower end is a valid lower bound for $M$, but its upper end is not valid for $M$. Its width carries a $\sqrt2$ penalty from halving the data, plus the risk of picking a sub-maximal cell.
- A width theorem would compare leading constants: simultaneous $\approx q_{1-\alpha}(\max_{v\in\mathcal V}Z_v)\,\sigma/\sqrt{n_{\min}}$ (≈ $\sqrt{2\log|\mathcal V|}$ for weakly correlated cells) versus selected $\approx q_{1-\alpha}(\max_{v\in\widehat V_n}Z_v)$, which tends to $z_{1-\alpha}$ when the argmax is unique and separated (CLR Theorem 3, Remark 1).

**Direction 4 (extension): rich function classes.** **[Brief]** Groups defined by a function class rather than a list. **[Interpretation]** This is where CC's VC-class theory (Theorem 4) and RKHS tilts (§5, Theorem 9) come in. CLR's continuum results need $v\in\mathbb R^d$ with smoothness (Conditions NS/NK), which does not obviously match "all halfspaces" or "all depth-3 trees". Computation also becomes a combinatorial optimisation per bootstrap draw (CC p. 12). I would treat this as optional.

**What each branch of the deliverable would require mathematically.** **[Interpretation]**

*Branch A: a shorter valid interval.*
1. **Model.** i.i.d. holdout data, $f$ fixed. Finite $\mathcal V$ with $|\mathcal V|=k_n$, either fixed or growing. Cell masses bounded below by the threshold (on $P$, not $P_n$).
2. **Linearisation.** $\hat\theta(v)-\theta(v)=n^{-1}\sum_i\psi_v(X_i,Y_i)+r_n(v)$ uniformly in $v$, with $\psi_v=\mathbf 1\{X\in G,f\in B_b\}\,s\,(Y-f-s\theta(v))/P(G\cap B_b)$.
3. **Gaussian approximation of the maximum.** For fixed $k$ this is the multivariate CLT plus Skorohod, as in CLR Example 1 / Lemma 4. For $k_n\to\infty$ (possibly $\gg n$) you need a high-dimensional CLT and anti-concentration for maxima. CLR quote the anti-concentration inequality (Lemma 10), but the high-dimensional CLT is not in the supplied papers. You also need consistency of a Gaussian-multiplier or empirical bootstrap for the sup over a *data-dependent* subset.
4. **Selection lemma.** An analogue of CLR Lemma 2: with probability → 1 the selected set contains a neighbourhood of the argmax set and lies inside a slightly larger deterministic neighbourhood. This must handle the absolute value (cells with $\theta\approx0$ contribute both signs) and the size threshold (cells near the threshold entering or leaving).
5. **Coverage theorem.** $\liminf_n P(L\le M\le U)\ge1-\alpha$, ideally uniformly over a class of $P$ (CLR's $P_n$-sequence framework helps). Exactness holds under a separation condition like CLR Condition V.
6. **Width theorem.** Ratio of expected widths versus CC and versus splitting, as an explicit function of the gap between the best and second-best cells, of $k$, and of the correlation structure. For example: equal to the pointwise width when separated, and never worse than the simultaneous width.
7. **Simulations** confirming coverage at realistic $n$. CC's own coverage at $n\le400$ was 0.81–0.87 for nominal 0.9 (Table 2), so finite-sample behaviour is a real issue.

*Branch B: an impossibility / lower bound.*
1. Fix a structure, e.g. $k$ disjoint groups of equal mass with one band each, or a nested chain, and a class $\mathcal P$ of distributions (Bernoulli outcomes, fixed $f$).
2. Define "valid": $\inf_{P\in\mathcal P}P(M(P)\in C)\ge1-\alpha$. Define "substantially shorter": a constant factor, or a rate in $k$ and $n$.
3. Reduce to testing. If $C$ is valid and $P_0$ has $M=0$ while each $P_j$ has $M=\delta$, then $\mathbb E_{P_0}|C|\ge\delta\,(1-2\alpha-\mathrm{TV}(P_0^n,\bar P^n))$, where $\bar P=\frac1k\sum_jP_j$ is a mixture over *which* group carries the gap.
4. Bound $\mathrm{TV}$ via the $\chi^2$-divergence of the mixture. For disjoint groups this is roughly $\frac1k(e^{n_g\delta^2/\sigma^2}-1)$, which is small when $\delta\lesssim\sigma\sqrt{\log k/n_g}$. That gives a lower bound of the same order as the simultaneous width, so **no rate improvement is possible at the all-gaps-equal configuration**.
5. Show how overlap or nesting changes the $\chi^2$ calculation. Highly correlated nested groups behave like fewer groups.

These tools (Le Cam's two-point/mixture method) are standard but are **not** developed in the supplied papers. CLR only point to the related impossibility of Hirano & Porter (p. 4) and to nonparametric rate lower bounds (footnote 6, p. 6).

*The two branches are probably not exclusive.* **[Interpretation]** Shortening is very likely possible at well-separated configurations and impossible, in rate, at flat or tied ones, including a near-perfectly multicalibrated model. A clean dissertation could prove one side and illustrate the other in simulations. Which side to make the theorem is a choice for the supervisor (§7).

### 4.2 What a dissertation would plausibly involve

**[Interpretation]** Shape 1, "CLR for multicalibration" (Branch A, fixed $k$):
- Weeks 1–4: reproduce CC's Algorithm 1/2 and CLR's §6.1 algorithm on simulated binned-calibration data.
- Then prove a coverage theorem for the selected lower bound plus the pointwise upper bound, for fixed $k$, under a separation condition, largely by adapting CLR Lemmas 1–2 and Theorems 2–4 with $\theta(v)$ = cell gaps.
- Prove a width-comparison proposition.
- Run simulations over three structures (disjoint, nested tree à la Guy et al., intersectional à la CC's COMPAS groups), varying $n$, $k$ and the gap separation, against CC and sample splitting.
- Optional: a real-data illustration on Folktables/ACS or COMPAS, and a small Python package.

Roughly 50% proof, 35% simulation code, 15% writing and context.

**[Interpretation]** Shape 2, "how short can it be?" (Branch B with an A-flavoured complement):
- Prove a minimax lower bound on expected length for disjoint equal groups, then extend to a nested chain, showing the dependence on correlation.
- Show by simulation that CLR-style selection attains the lower bound's order at flat configurations and does much better at separated ones.

This is more purely mathematical: perhaps 65% proof, 25% simulation, 10% writing. It is riskier if the $\chi^2$ calculation for overlapping groups becomes messy.

In both shapes the asymptotic arguments in CLR (strong approximation, concentration, anti-concentration) are the hardest reading. For fixed $k$ most of it collapses to the multivariate CLT, which is why I would start there.

### 4.3 Open questions

From the papers' own limitations and remarks:
- **Small groups.** CC: unscaled bounds are vacuous for small groups (p. 8, Fig. 3). Rescaling is "only one heuristic" (p. 10). Estimating group variances "can harm the finite-sample validity" (pp. 9–10). HKRR: how much representation is needed "remains an interesting question" (§2, footnote 1). Guy et al.: $M$ suppresses small groups when calibration is poor (§3.5).
- **Finite-sample coverage.** CC's simultaneous bounds under-cover at small $n$ (Table 2, pp. 14–15). The RKHS version is conservative (Table 4, p. 23). CLR over-cover (0.98–0.99) in non-flat designs (pp. 43–44).
- **Computation for rich classes.** CC: certification over infinite collections is "tantamount to solving a challenging 0-1 loss optimization problem hundreds of times" (p. 12). The rescaled RKHS bootstrap is "prohibitively expensive" (p. 22).
- **When selection helps.** CLR: exact size needs Conditions V and S (Theorem 3). In flat cases their test lacks $n^{-1/2}$ power where Andrews–Shi has it, and "neither approach dominates" (pp. 6, 44; App. K). A step-down iteration of AIS is mentioned but omitted (footnote 2, p. 3). Non-undersmoothed estimation is not formally covered (p. 14).
- **Error rates beyond the proven cases.** CC expect FDR control to hold outside Proposition 8's assumptions but do not prove it (p. 18). They suggest sample splitting for infinite collections (p. 18).
- **Interpretation of the max metric.** Guy et al. say $M$ "likely is most informative when the subpopulations are calibrated reasonably well" (§3.5). **[Interpretation]** That is exactly the near-tied regime where Branch B suggests selection cannot help.

## 5. Background knowledge required

| Area (Maths / Statistics / CS-ML) | Item | Status | Rough effort if not covered | Where it's needed |
|---|---|---|---|---|
| Maths | Measure-theoretic probability (convergence modes, conditional expectation) | partly covered | in progress this term | Reading all proofs |
| Statistics | Asymptotic statistics: CLT, Slutsky, delta method, asymptotic linearity / influence functions | partly covered | 1–2 weeks to consolidate | CC Assumption 1; ratio estimators of cell gaps; CLR Condition P |
| Statistics | Multiple testing and simultaneous inference (FWER, FDR, BH, Bonferroni, max-t) | partly covered | a few days | CC §3–4; framing of "all-groups" interval |
| Statistics | Bootstrap theory (consistency, multiplier/Gaussian bootstrap, when it fails) | new to me | 1–2 weeks | CC Algorithms 1–3, Thm 4; CLR Definition 3 |
| Maths/Statistics | Empirical processes: Glivenko–Cantelli, Donsker, VC classes | new to me | 2–4 weeks | CC Thm 4 and App. B; rich-class extension |
| Maths | Gaussian processes: suprema, concentration (Borell–TIS / Talagrand), anti-concentration, $\sqrt{2\log k}$ behaviour of maxima | new to me | 2–3 weeks | CLR Conditions C.2–C.3, Lemmas 10–13; width comparisons |
| Maths | Strong approximation / coupling (Skorohod, Yurinskii) | new to me | 1–2 weeks (only to fixed-$k$ depth) | CLR C.2, Lemma 9, §5 |
| Statistics | High-dimensional CLT for maxima of sums (many groups) | new to me | substantial: 3–4 weeks; not in the supplied papers | Branch A with growing $k$ |
| Statistics | Minimax lower bounds (Le Cam, $\chi^2$ of mixtures) | new to me | 2–3 weeks | Branch B |
| Statistics | Partial identification / moment inequalities (context only) | new to me | a few days | Understanding CLR's motivation and §1–2 |
| Statistics | Selective inference / winner's curse, sample splitting | partly covered | a few days | Problem framing; splitting comparison |
| CS-ML | Calibration, reliability diagrams, ECE; multicalibration definition | new to me | a few days | HKRR §2; Guy et al. §1, App. D |
| CS-ML | Algorithmic fairness metrics (group fairness, COMPAS debates) | new to me | a few days | Motivation; CC §2.2, App. A |
| CS-ML | RKHS basics | new to me | 1–2 weeks | Only for the rich-class extension (CC §5) |
| CS-ML | Python simulation (NumPy, scikit-learn, vectorised bootstraps) | partly covered | a week | All simulations; extending `fairaudit` |

The biggest gap is **the probability of suprema**: Gaussian-process maxima, concentration and anti-concentration, and bootstrap consistency for sup-functionals of empirical processes. Every coverage proof in CC and CLR runs on it. A fixed-$k$ version reduces it to the multivariate CLT plus facts about maxima of correlated normals, which is manageable this term. Growing $k$ or rich function classes push it into empirical-process and high-dimensional CLT territory, which would need early, dedicated reading.

## 6. Practicalities

### Code
- **[Paper]** Cherian & Candès: Python package **`fairaudit`**, on PyPI and at `github.com/jjcherian/fairaudit` (§1, p. 2).
- **[Paper]** Guy et al.: code reproducing all results at `https://github.com/facebookresearch/McMetric` (footnotes on pp. 4 and 6). They also mention, without a link, the `mcboost` package by Pfisterer et al. (2021) implementing HKRR-style boosting (§1.5).
- **[Paper]** Chernozhukov, Lee & Rosen: no code link in the paper. Implementation steps are given as Algorithms 1–2 in §6. Timings come from "our implementation" (§7.4, footnote 29).
- **[Paper]** Hébert-Johnson et al.: no code (theory paper).

### Data
- **[Paper]** CC: synthetic linear models (eq. 11–12) and the synthetic CQR data of Romano et al. (2019). COMPAS data "obtained by ProPublica in 2016", $n=6781$ (§2.2.2). Folktables income data from the 2018 ACS PUMS for California, "made available in the Folktables package" (§4.2.1). Public availability is implied for Folktables. For COMPAS it is not stated explicitly.
- **[Paper]** Guy et al.: 2019 American Community Survey microdata, with a Census Bureau URL given, so public (§3.3, footnote). 1998 KDD Cup data, with a UCI URL given, so public (§3.4, footnote). A synthetic set with closed-form answers (App. F).
- **[Paper]** CLR: simulated designs (§7.1). The NLSY79 illustration (Figs. 3–4) belongs to their earlier working paper. Availability is not discussed.
- **[Paper]** HKRR: none.
- **[Interpretation]** The core deliverable needs only simulated data where the true $M$ is known. Folktables/ACS would serve for an optional real-data illustration.

### Compute
- **[Paper]** CC: certification over 1,275 intervals at $n=1600$ with $B=500$ bootstraps takes "under 7 seconds on a 2020 MacBook Pro" (p. 12). COMPAS audits under 1 s (p. 16), flagging under 0.5 s (p. 19), RKHS audit about 1.5 s (p. 23).
- **[Paper]** CLR: 16,000 Monte Carlo replications took about 19–84 minutes depending on the estimator, on a 2011 iMac (2.7 GHz, 8 GB RAM) (§7.4, Table 4, footnote 29).
- **[Paper]** Guy et al. and HKRR report no compute.
- **[Interpretation]** This is a CPU-only project and a laptop is enough. The expensive part is coverage studies: (Monte Carlo replications) × (bootstrap draws) × (number of cells). For example, 1,000 replications × 500 bootstraps × 10⁴ cells is about 5×10⁹ cheap operations per design point. That is vectorisable in NumPy and fine on a laptop overnight, or trivially parallel on the LSE cluster. Rich function classes (searching over halfspaces or trees per bootstrap draw) are the only thing that could become slow.

## 7. Questions for the proposal meeting

1. **Exactly which gap functional?** Is it the binned conditional mean gap $|\mathbb E[Y-f\mid G,B_b]|$ (HKRR / CC App. A style), a mass-weighted version, or something normalised like Guy et al.'s $\sigma$-scaled Kuiper metric? Normalisation changes which cell is the maximiser and hence the whole selection problem.
2. **How is the minimum size defined?** Is it on the population mass $P(G)$ or $P(G\cap B_b)$, or on sample counts? A population threshold estimated from data creates a second selection effect at the boundary. A sample-count threshold makes the target itself random.
3. **Are the bands fixed in advance?** Are they the brief's "bands of predicted probability" with fixed width, and if so how many? Or should unbinned (Kuiper-type) versions be considered? This determines whether CLR's finite-index Example 1 applies directly.
4. **Fixed or growing number of groups?** Is the main theorem for fixed $k$, or must it allow $k_n\to\infty$ (possibly $k\gg n$)? The latter needs high-dimensional Gaussian approximation that is not in the supplied papers and roughly doubles the theoretical load.
5. **Two-sided or one-sided?** Is a two-sided interval required, or is the lower confidence bound (certifying "at least this miscalibrated") or the upper bound (certifying "at most this miscalibrated") the real interest? My reading (§4.1) is that the two ends have very different difficulty.
6. **Which baseline counts as "the all-groups interval"?** CC's unscaled Algorithm 1, or the rescaled Algorithm 2 with which $p^{*}$ and $w_0$? The width comparison depends heavily on this choice.
7. **What does "substantially shorter" mean for Branch B?** A constant factor, or a rate in $k$ and $n$? Should the bound hold at the worst case, at the null of perfect multicalibration, or uniformly? Which group structures are the targets: disjoint, nested chain/tree, or intersections of attributes?
8. **Which branch to aim for first, and when to switch?** Would the supervisor accept a combined result, e.g. "exact and shorter under separation; no rate gain at ties"?
9. **What coverage notion?** Pointwise asymptotic for each fixed $P$, uniform over a class (CLR's $P_n$ framework), or finite-sample? Uniformity is the honest notion for a non-smooth target like a max, but it is harder to prove.
10. **Sample-splitting comparison details.** Which split ratio? Is cross-fitting or repeated splitting allowed as a stronger competitor? Is the splitting interval meant as an interval for $M$ or for the selected group's gap?
11. **Scope of the "rich function class" extension.** Is it in scope, and if so which class (halfspaces, shallow trees, RKHS tilts as in CC §5)? It brings in VC/empirical-process theory and heavy computation.
12. **Is the model treated as fixed,** with inference conditional on $f$ and only holdout data used, as in CC? Or should randomness from training $f$ matter?
13. **Software expectations.** Is the optional open-source release meant to extend `fairaudit` or to be standalone? Is a real-data illustration (Folktables/ACS, COMPAS) expected or optional?
