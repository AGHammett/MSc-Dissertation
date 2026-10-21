# Semi-supervised Reinforcement Learning from Human Feedback for LLM Fine-tuning: Overview

**Supervisor:** Dr Chengchun Shi · **Prepared:** 21 October 2026 · **Sources:** the brief and the 5 supplied papers only

> **Labels.** **[Paper]** a paper states it (with reference) · **[Brief]** the brief states it · **[Interpretation]** my own reading. Check it before relying on it.

## 1. The brief

**[Brief]** Large language models (LLMs) are routinely post-trained with reinforcement learning from human feedback (RLHF): humans say which of two (or more) responses to a prompt they prefer, and the model is fine-tuned towards the preferred behaviour. Human preference labels are expensive, so labelled datasets are small, which the brief says leads to "inefficient training and unpredictable model behavior". The project is to study *semi-supervised RLHF*: use semi-supervised learning (SSL), which combines a small labelled set with a large unlabelled one, to improve existing RLHF algorithms. The brief notes that although LLMs are pre-trained on vast unlabelled text, SSL "has rarely been applied to RLHF". The project should build on recent advances in SSL, is described as "coding-intensive", and is expected to lead to a paper suitable for a top machine-learning conference or a statistics journal.

**Project type:** methodological and computational, with computation dominating. **[Interpretation]** The brief stresses coding. The closest supplied paper (VRPO, §2.5) puts its weight on LLM experiments, with theory in a supporting role. A good dissertation would propose an SSL-style modification of an RLHF loss, back it with a variance or efficiency argument at the level of M-estimation asymptotics, and then show the effect in fine-tuning experiments. A purely theoretical dissertation would fit the brief poorly.

## 2. Paper by paper

**Recommended reading order and why.** (1) InstructGPT sets out the standard RLHF pipeline and the data each stage uses. (2) DPO reduces that pipeline to a single logistic-type loss. That loss is what VRPO modifies, and it is what you would most likely code. (3) The Science version of PPI is the most intuitive statement of "use cheap predictions on unlabelled data, then correct them with a few labels". (4) Xu, Witten and Shojaie give the general efficiency theory, which says *when* unlabelled data can help. (5) VRPO, the supervisor's own paper, combines all of these. It is easiest to understand after the other four, and it is the paper the project most directly extends.

### 2.1 InstructGPT: Training language models to follow instructions with human feedback (Ouyang et al., 2022)

arXiv:2203.02155v1 [cs.CL], 4 March 2022 (OpenAI).

- **Problem.** **[Paper]** Bigger language models are not automatically better at following user intent. They can be untruthful, toxic or unhelpful (Abstract, p. 1). The aim is to align GPT-3 with the intentions of a specific group of people by fine-tuning on human feedback (§1, p. 2).
- **Approach.** **[Paper]** A three-step pipeline (§3.1, p. 6; Fig. 2). (i) *Supervised fine-tuning (SFT)* on labeller-written demonstrations. (ii) A *reward model (RM)* is trained on rankings of model outputs, using the pairwise logistic (Bradley–Terry-type) loss in Eq. (1), p. 8. Labellers rank $K=4$ to $9$ outputs per prompt, and all $\binom{K}{2}$ pairs are treated as one batch element to avoid overfitting. (iii) *PPO* (an RL algorithm) maximises the RM score minus a per-token KL penalty to the SFT model, optionally mixed with pre-training gradients ("PPO-ptx", Eq. (2), p. 9). The data come in three sets (§3.2, p. 6; Table 6, App. A.3): about 13k SFT prompts, 33k RM prompts, and **31k PPO prompts "without any human labels"**.
- **Main findings and results.** **[Paper]** Outputs of the 1.3B InstructGPT model are preferred to those of the 175B GPT-3 (Abstract; Fig. 1, p. 2). The 175B InstructGPT is preferred to 175B GPT-3 85 ± 3% of the time, and to few-shot GPT-3 71 ± 4% of the time (§1, p. 3). Other findings: hallucination on closed-domain tasks falls from 41% to 21% (p. 3); toxicity improves a little (about 25% fewer toxic outputs when prompted to be respectful) but bias does not (p. 3); the "alignment tax" on public NLP benchmarks is mostly removed by PPO-ptx (p. 4). Inter-labeller agreement is about 73% (§3.4, p. 7; §5.2, p. 18).
- **Key assumptions.** **[Paper]** Preferences come from about 40 screened contractors, mostly English-speaking, and most comparisons are labelled by only one contractor "for cost reasons" (§5.3, p. 19). The RM's reward difference is treated as the log-odds of preference (p. 8). Only 6B RMs are used, because 175B RMs were unstable (§3.5, p. 8; App. C.2).
- **Relation to the other papers.** **[Interpretation]** This is the "two-stage" (reward model, then RL) scheme that DPO collapses and that VRPO calls two-stage optimisation (VRPO §2, p. 4). Two things matter for this project. First, it shows that human labels are costly and noisy (one rater per comparison, about 73% agreement), which is the brief's motivation. Second, its PPO stage *already* uses unlabelled prompts: they are needed for policy roll-outs, but they are not used to improve the reward estimate. That gap is the one semi-supervised RLHF would fill.

### 2.2 DPO: Direct Preference Optimization: Your Language Model is Secretly a Reward Model (Rafailov et al., 2023)

arXiv:2305.18290v3 [cs.LG], 29 July 2024; NeurIPS 2023.

- **Problem.** **[Paper]** RLHF with PPO is "complex and often unstable". It involves training several models and sampling from the policy inside the training loop (Abstract; §1, p. 2).
- **Approach.** **[Paper]** The KL-regularised objective $\max_\pi \mathbb{E}[r(x,y)] - \beta\,\mathrm{KL}(\pi\|\pi_{\rm ref})$ (Eq. 3, p. 3) has the closed-form optimum $\pi_r(y|x)\propto \pi_{\rm ref}(y|x)\exp(r(x,y)/\beta)$ (Eq. 4, p. 4; App. A.1). Inverting this gives $r(x,y)=\beta\log\frac{\pi_r(y|x)}{\pi_{\rm ref}(y|x)}+\beta\log Z(x)$ (Eq. 5). Under Bradley–Terry (BT) the partition function $Z(x)$ cancels in reward differences, so the policy can be fitted directly by the logistic loss
$$\mathcal{L}_{\rm DPO}=-\mathbb{E}\Big[\log\sigma\Big(\beta\log\tfrac{\pi_\theta(y_w|x)}{\pi_{\rm ref}(y_w|x)}-\beta\log\tfrac{\pi_\theta(y_l|x)}{\pi_{\rm ref}(y_l|x)}\Big)\Big]$$
(Eq. 7, p. 4). In statistical terms this is maximum likelihood for a reparametrised BT model.
- **Main findings and results.** **[Paper]** Theorem 1 (p. 6) shows that the reparametrisation loses no generality: every reward equivalence class consistent with Plackett–Luce/BT can be written as $\beta\log(\pi/\pi_{\rm ref})$. Empirically, DPO has the best reward–KL frontier on IMDb sentiment, beating PPO even when PPO has the true reward (Fig. 2 left; §6.1, pp. 8–9). On TL;DR summarisation, the GPT-4-judged win rate is about 61% for DPO against 57% for PPO (§6.2, p. 9). On Anthropic-HH, DPO is "the only computationally efficient method that improves over the preferred completions" (p. 9). GPT-4 judgements agree with humans about as often as humans agree with each other (Table 2, §6.4, p. 10).
- **Key assumptions.** **[Paper]** The BT (or Plackett–Luce) preference model, and a reference policy matching the one that generated the data. When no SFT model exists, $\pi_{\rm ref}$ is obtained by fine-tuning on the preferred completions, to "mitigate the distribution shift" (§4, p. 5). Defaults are $\beta=0.1$, batch size 64, RMSprop, learning rate $10^{-6}$ (App. B, p. 20).
- **Relation to the other papers.** **[Paper]** VRPO's experiments follow the DPO training pipeline but swap in its own loss (VRPO §5, p. 8), and VRPO calls DPO-type methods "one-stage optimisation" (VRPO §4, Eq. 5, p. 7). **[Paper]** DPO's own future-work list asks whether "training with self-labeling from the DPO policy [can] similarly make effective use of unlabeled prompts" (§7, p. 10). It also notes in §6.3 (p. 9) that DPO, unlike PPO, does not use the extra unlabelled TL;DR prompts. **[Interpretation]** That is close to an explicit invitation to a semi-supervised DPO.

### 2.3 PPI: Prediction-powered inference (Angelopoulos, Bates, Fannjiang, Jordan & Zrnic, 2023), Science version

*Science* 382, 669–674 (10 November 2023), doi:10.1126/science.adi6000. **This is the short Science article (7 PDF pages: 6 article pages plus a cover/editor's-summary page). It is not the longer arXiv version.** The theorems and algorithms it refers to (Theorem S1, Algorithms S1–S6, Corollary S13, Theorem S3) are in the online Supplementary Materials, which are *not* in the folder. Pages below are the article's "N of 6".

- **Problem.** **[Paper]** A scientist has a few gold-standard labels and many cheap ML predictions. Treating the predictions as truth ("imputation") gives invalid conclusions. Ignoring them ("classical") is valid but wasteful (p. 1 of 6).
- **Approach.** **[Paper]** Choose an estimand $\theta$. Compute a *measure of fit* $m_\theta$ on the unlabelled data with the predictions plugged in, and a *rectifier* $\Delta_\theta$ on the labelled data: the same measure computed with predictions minus that computed with true labels. Then form $\mathcal{C}^{PP}=\{\theta: |m_\theta+\Delta_\theta|\le w_\theta(\alpha)\}$ (p. 1 of 6; Table 1, p. 3 of 6). For the mean this is $\tilde\theta=\frac1N\sum \hat Y'_i-\frac1n\sum(\hat Y_i-Y_i)$. The general version covers any minimiser of a convex objective (p. 2 of 6), and there are variants for covariate shift and label shift (p. 2 of 6).
- **Main findings and results.** **[Paper]** The resulting intervals are valid "for any machine-learning algorithm and any underlying data distribution" (p. 1 of 6). They are narrower than classical intervals in all seven applications (proteomics with AlphaFold, galaxies, gene expression, deforestation, census, plankton; Fig. 2). Table 2 (p. 5 of 6) gives the labels needed to reject a null: for example, 316 against 799 (AlphaFold), 189 against 449 (galaxies) and 21 against 35 (deforestation). The imputation intervals always missed the truth (p. 2 of 6).
- **Key assumptions.** **[Paper]** The labelled and unlabelled data are random samples from the same population (or follow a specified shift), and the predictor is fitted on separate data (p. 1 of 6; Related work, p. 5 of 6). **Limitation:** no gain when the predictions are poor or the unlabelled set is not large enough (Conclusions, p. 5 of 6).
- **Relation to the other papers.** **[Paper]** VRPO cites PPI as the "more general objective functions" member of the semiparametric SSL literature it adapts (VRPO §2, p. 5). Xu et al. show that PPI estimators are a special case of their framework and are not efficient in general (Xu et al. §5). **[Interpretation]** The VRPO loss (Eq. 3) has the same "plug in predictions, then correct with labelled data" shape as the PPI rectifier, with the auxiliary preference model $p_\eta$ playing the role of the predictor.

### 2.4 A Unified Framework for Semiparametrically Efficient Semi-Supervised Learning (Xu, Witten & Shojaie, 2025)

arXiv:2502.17741v2 [math.ST], 18 March 2025.

- **Problem.** **[Paper]** With $n$ labelled pairs $(X,Y)$ and $N$ unlabelled $X$'s, "under what circumstances, and by how much, can incorporating the unlabeled dataset improve upon inference using the labeled data?" (Abstract; §1, p. 1).
- **Approach.** **[Paper]** Semiparametric efficiency theory (§2: tangent spaces, influence functions, efficiency bound, Lemma 2.1). There are three settings: supervised; ideal semi-supervised (ISS), where $P_X$ is known; and ordinary semi-supervised (OSS), with finite unlabelled data and $N/(n+N)\to\gamma$ (§1.1). The key object is the *conditional influence function* $\phi(x)=\mathbb{E}[\varphi(Z)\mid X=x]$ (Eq. 3). Estimators take an initial supervised estimator and subtract a regression-based estimate of $\phi$ evaluated at the labelled points, centred using all the $X$'s (Eq. 9, Eqs. 26–28).
- **Main findings and results.** **[Paper]**
  - Theorem 3.1 (p. 4): the ISS bound is $\mathrm{Var}[\varphi^*]-\mathrm{Var}[\phi^*]$, so knowing $P_X$ helps if and only if $\phi^*(X)$ is non-constant.
  - Theorem 3.2 and Corollary 3.3 (p. 5): if the parameter is *well-specified* (Definition 3.1: changing $P_X$ does not change $\theta$), there is **no gain**.
  - Theorem 4.1 (p. 9): the OSS bound is $\mathrm{Var}[\varphi^*]-\gamma\mathrm{Var}[\phi^*]$, described as the first efficiency bound for this non-i.i.d. setting. Corollary 4.2 (p. 10): again no gain when well-specified.
  - The *safe* estimator (Theorem 4.3, Eq. 31) is never worse than the supervised one, whatever the regressors $g$. The *efficient* estimator (Theorem 4.4) uses a growing sieve basis and attains the bound under Hölder smoothness.
  - §5 (pp. 12–14): PPI-type estimators fall in the OSS class and cannot reach the bound without strong assumptions. Independently trained ML predictors cannot help a well-specified parameter (p. 12; Remark 5.1). Their "safe PPI" estimator (Eq. 41, Proposition 5.2) regresses the influence function on predicted-label influence functions and is optimal within a class that includes PPI and PPI++.
  - Applications cover M-estimation including GLMs, U-statistics and the ATE (§7). Simulations use $n=1000$ (§8).
- **Key assumptions.** **[Paper]** The initial estimator is regular and asymptotically linear (RAL). The influence-function class is Donsker with a Lipschitz condition (Assumption 3.1). The efficient estimator also needs smoothness of $\phi$ with $\alpha>\dim(X)$ (Assumption 3.2), which "cannot be verified in practice" (§7, p. 15). Labelled and unlabelled data come from the same $P_X$.
- **Relation to the other papers.** **[Paper]** It generalises and critiques PPI (§5). **[Interpretation]** It is the theoretical lens for VRPO. VRPO's Table 1 (no asymptotic gain under correct specification, gain under misspecification) is exactly the well-specified/not-well-specified dichotomy of Theorem 3.2 and Corollary 4.2. VRPO's correction term subtracts the conditional expectation of the loss under $p_\eta$ and adds back its average under $\pi_{\rm ref}$, which is a version of Eq. (9) with $\phi$ approximated by a plug-in model rather than a fitted regression. The coefficient is fixed at 1 rather than estimated, so VRPO is not "safe" in Xu et al.'s sense. This is my reading and is not stated in either paper.

### 2.5 VRPO: Robust Reinforcement Learning from Human Feedback for Large Language Models Fine-Tuning (Ye, Zhou, Zhu, Quinzan & Shi, 2025/2026)

arXiv:2504.03784v6 [stat.ML], 10 February 2026. **Chengchun Shi is a corresponding author** (with Quinzan; footnote †, p. 1). The PDF file is named "Robust RLHF for LLM Fine-tuning (VRPO)".

- **Problem.** **[Paper]** Reward-based RLHF assumes $p^*(x,y^{(1)},y^{(2)})=\sigma(r^*(y^{(2)},x)-r^*(y^{(1)},x))$ (Eq. 1, p. 6). This entails transitivity, context-independence and perfect rationality, which real preferences violate (§1, pp. 2–3). Even under BT the parametric reward can be misspecified. Under either kind of misspecification, existing algorithms can give suboptimal policies (§3, p. 6).
- **Approach.** **[Paper]** *Variance-reduced preference optimisation.* First fit a richer *auxiliary* preference model $p_\eta$, for example the general (non-BT) preference model of Zhang et al. 2024a. Then estimate the primary model by minimising
$$\tilde{\mathcal{L}}(\theta)=\mathbb{E}_n\Big[\ell(X,Y^{(1)},Y^{(2)},Z;\theta)-\sum_{u=0}^1\ell(X,Y^{(1)},Y^{(2)},u;\theta)p_\eta(\cdot,u)+\sum_{u=0}^1\mathbb{E}_{y^{(1)*},y^{(2)*}\sim\pi_{\rm ref}(\cdot|X)}\ell(X,y^{(1)*},y^{(2)*},u;\theta)p_\eta(\cdot,u)\Big]$$
(Eq. 3, p. 7). If $\pi_{\rm ref}$ is correct, the last two terms have equal means. If $p_\eta\approx p^*$, they cancel noise (p. 7). The loss plugs into two-stage RLHF (fit the reward, then PPO; Eq. 4) and into one-stage DPO-style training (Eq. 5). The expectation over $\pi_{\rm ref}$ is approximated by Monte Carlo, drawing **one fresh pair** of responses per prompt (§5 Implementation, p. 8).
- **What it says about unlabelled data (relevant to the brief's novelty claim).** **[Paper]** The related-work paragraph headed "Semi-supervised learning" (§2, p. 5) places VRPO in the semiparametric SSL literature (Chakrabortty & Cai; Zhang, Brown & Cai; Angelopoulos et al., i.e. PPI; Zhu et al. 2025 on RL). It states: "we do not develop new semi-supervised learning algorithms. Rather, we adapt ideas from this literature for LLM fine-tuning. Our key observation is that when the reference policy is known, one can generate an abundant amount of responses to each query – albeit without the corresponding human preference labels. This naturally leads to a semi-supervised learning setting … To the best of our knowledge, no prior work has leveraged semi-supervised learning in this way for LLM fine-tuning." **[Interpretation]** So VRPO is itself a semi-supervised RLHF method. In it, "unlabelled data" means *synthetic responses from $\pi_{\rm ref}$ to the already-labelled prompts*, not extra unlabelled prompts. The brief's "rarely applied" is consistent with this paper being one of the few examples. It also means the project almost certainly starts from VRPO, and any novelty has to be measured against it.
- **Main findings and results.** **[Paper]**
  - Theorem 6.1 (double robustness, p. 13): under correct reward and preference models, $\bar\theta$ is identified if *either* $\pi_{\rm ref}$ *or* $p_\eta$ is correct.
  - Theorem 6.2 (p. 14): both estimators have bias $O(d/(n\lambda_{\min}))$, and $\mathrm{Var}(\hat\theta)-\mathrm{Var}(\tilde\theta)=\frac1n A^{-1}HA^{-1}+O(d^{3/2}/(n^{3/2}\lambda_{\min}^2))+O(\|p_\eta-p^*\|_\infty^2/(n\lambda_{\min}^2))$ with $H\succeq0$. A lower bound (Eq. 6) shows the gain vanishes if $\pi_{\rm ref}$ is deterministic or the model is correctly specified.
  - Theorem 6.3 (p. 15): the reduced variance gives a smaller expected suboptimality gap.
  - Experiments (Table 2, p. 8): IMDb sentiment with synthetic BT labels (reward model misspecified); Anthropic-HH dialogue (preference model misspecified); TL;DR summarisation (reference policy misspecified).
  - On HH, VRPO beats nine baselines at every temperature, with win rates of 0.53–0.98 (Table 3, p. 11), about 0.78–0.81 against DPO, and above 0.80 against DPO-hinge (the ablation). On AlpacaEval 2.0 its win rate against SFT is 93.79% (LC 92.95%), against 90.93% for Dr. DPO (Table 4, p. 12). Gains on TL;DR are smaller, which is attributed to the misspecified $\pi_{\rm ref}$ (Fig. 4, pp. 12–13).
  - Two-stage variants: VR-PPO against PPO wins 0.48–0.64; VR-GRPO against GRPO wins 0.52–0.77 (Tables 7–8, supplement p. 29).
- **Key assumptions.** **[Paper]** A known or well-specified reference policy (§3, p. 5, footnote 2). The regularity conditions (A1)–(A4) (supplement §8.2: compact parameter space, bounded second derivatives, non-singular Hessian), and (B1)–(B2) for Theorem 6.3. The authors themselves call (B2) "restrictive" (supplement p. 25). A finite parameter dimension $d$.
- **Relation to the other papers.** **[Interpretation]** It combines InstructGPT/DPO (the base algorithms) with the PPI and Xu et al. idea (correct a plug-in prediction using labelled data, exploit a known marginal). It is the natural baseline for the dissertation.
- **Points I could not fully reconcile.** **[Paper]** The main text refers to "Section S.1.2 / S.2 / S.3 of the Supplementary Material A", but the supplement in this PDF numbers these as Sections 8, 9 and 10. The IMDb set-up says 25,000 prompts in §5.1 (p. 9) but 250,000 in supplement §9.1 (p. 26). Theorem 6.1's proof (supplement §8.1) is brief and labels law-of-large-numbers steps "by central limit theorem". **[Interpretation]** The bounds have terms in $d^{3/2}/n^{3/2}$ with $d$ the parameter dimension. For an LLM, $d$ is in the hundreds of millions, so the theory is best read as heuristic support in that regime. The paper does not discuss this. **No GPU types, run times or total compute are reported.**

## 3. How the papers fit together

**Common thread.** **[Interpretation]** Every paper is about estimating something from **scarce labels plus abundant label-free information**. In InstructGPT and DPO the "something" is a reward or policy fitted from costly human comparisons. PPI and Xu et al. give the statistical recipe: write the estimator via its influence function or loss, then subtract a mean-zero correction built from predictions or a known marginal. VRPO applies that recipe to the RLHF loss, using the fact that $\pi_{\rm ref}$ is known, so unlabelled responses are free to generate.

```
  RLHF pipeline (what is estimated)              SSL / semiparametric toolbox (how to use unlabelled data)
  ---------------------------------              ---------------------------------------------------------
  InstructGPT: SFT -> RM (BT MLE) -> PPO         PPI (Science): predictions + rectifier, valid CIs
          |                                              |
  DPO: RM + RL collapsed into one BT-type loss   Xu-Witten-Shojaie: efficiency bounds, safe/efficient
          |                                      estimators, "no gain if well-specified"
          \______________________  ______________________/
                                 \/
          VRPO (Shi et al.): BT loss + control-variate correction using p_eta and responses from pi_ref
                                 |
                   THIS PROJECT: semi-supervised RLHF, extending VRPO
```

**Axes along which they differ.**

| | InstructGPT | DPO | PPI (Science) | Xu et al. | VRPO |
|---|---|---|---|---|---|
| Goal | aligned LLM | aligned LLM, simpler | valid CIs | efficiency theory | lower-variance RLHF |
| Unlabelled data | prompts for PPO roll-outs only | none (flagged as future work) | unlabelled $X$ + ML predictions | unlabelled $X$ or known $P_X$ | fresh responses from $\pi_{\rm ref}$ |
| Theory | none formal | Thm 1 (reparametrisation) | validity (in SM) | bounds, RAL estimators | DR, variance, regret expansions |
| Inference or prediction | prediction | prediction | inference | inference | estimation then policy quality |
| Scale | 1.3B–175B | up to 6B | tabular/CPU | simulations | 0.5B–1.5B |

**Settled versus unsettled.** **[Paper]** Settled: (i) BT-type losses with a KL anchor work well in practice (InstructGPT, DPO); (ii) in classical settings, unlabelled data help only when the target is not "well-specified" (Xu et al. Thm 3.2, Cor 4.2), which agrees with VRPO's Table 1; (iii) PPI-type corrections keep validity whatever the predictor's quality (PPI p. 1 of 6). **[Interpretation]** Unsettled: (a) which kind of unlabelled data is most useful in RLHF (extra responses, extra prompts, or AI-generated labels); (b) whether a *safe* or *efficient* version of VRPO (estimated coefficients, as in Xu et al. Eq. 28/41) beats the fixed-coefficient VRPO; (c) how classical $\sqrt n$, fixed-$d$ theory transfers to billion-parameter models; (d) how reliable GPT-judged win rates are as the outcome measure (DPO §6.4 and §7; VRPO supplement §9.2 notes GPT-4o-mini's preference for detail).

## 4. Tie-in to the dissertation

### 4.1 What the proposed directions mean in practice

The brief gives one broad direction: "integrate SSL to enhance existing RLHF algorithms using both labeled and unlabeled data", "building on recent advances in SSL". **[Interpretation]** In practice this splits into four concrete choices.

1. **Decide what the unlabelled data are.** Three candidates come from the papers:
   - (a) *Extra responses* sampled from $\pi_{\rm ref}$ for labelled prompts, as in VRPO, which uses only one Monte Carlo pair per prompt (VRPO p. 8). An easy first step is more pairs, or all $\binom{K}{2}$ pairs from $K$ samples.
   - (b) *Extra unlabelled prompts*, as in the PPO dataset of InstructGPT (31k prompts, Table 6) or the unlabelled TL;DR prompts that DPO does not use (DPO §6.3). This is the classical OSS setting of Xu et al. The prompt marginal is unknown but sampled, so the correction has to be centred with empirical means over labelled plus unlabelled prompts (Xu Eq. 26).
   - (c) *AI-labelled comparisons*, where a strong LLM judge (GPT-4-type, as used for evaluation in DPO and VRPO) acts as the "black-box predictor" in PPI. This is a PPI or safe-PPI estimator for the preference loss.

   Doing (a) needs only code changes to VRPO. Doing (b) or (c) requires deriving the corrected loss and its asymptotic variance.

2. **Choose the SSL estimator.** Options: VRPO's fixed control variate; Xu et al.'s *safe* estimator, which regresses the per-example loss gradient (the influence function) on features of $(X,Y^{(1)},Y^{(2)})$ with the coefficient estimated (Eqs. 27–28); or a PPI++-style scalar "power-tuning" weight. In practice you would implement a weighted correction term inside the DPO loss and estimate the weight on a held-out split or by cross-fitting.

3. **Choose the base RLHF algorithm.** One-stage (DPO or its variants) is far cheaper. VRPO's main results are one-stage (p. 8). Two-stage (reward model plus PPO or GRPO) is more expensive but makes the "estimate a reward with lower variance" story cleaner (VRPO Tables 7–8).

4. **Design the evaluation.** Three options:
   - A *synthetic oracle*, as in IMDb with a sentiment classifier as true reward (DPO §6.1; VRPO §5.1). This allows exact reward–KL frontiers and controlled misspecification. It is the best place to show variance reduction across repeated seeds and different labelled-set sizes $n$.
   - *Real preference data* (HH, TL;DR) with LLM-judge win rates.
   - *Label-efficiency curves*: performance against the number of labelled comparisons, mirroring PPI's Table 2 (labels needed to reach a target).

### 4.2 What a dissertation would plausibly involve

**[Interpretation]** The work would contain:

- **Proofs.** Probably modest. Write the new loss and show (i) its population minimiser equals the target (unbiasedness or double robustness, in the style of VRPO Thm 6.1) and (ii) an asymptotic variance comparison via the M-estimation sandwich formula, with "safe" non-inferiority following the argument of Xu et al. Thm 4.3. These are fixed-$d$ arguments built from Taylor expansions, the LLN and the CLT, all within reach of the reader's inference module.
- **New method.** A semi-supervised variant of VRPO or DPO.
- **Simulations.** First low-dimensional BT and logistic-regression simulations (cheap, many replications) to check the variance claims. Then small-LLM simulations with an oracle reward.
- **Real-data experiments.** HH and/or TL;DR with a 0.5B–1.5B model.

**Shape A: "safe VRPO" (lower risk).** Months 1–2: reproduce DPO and VRPO on IMDb with Qwen2-0.5B using the released VRPO code. Month 3: implement an estimated-coefficient (safe) correction and multiple Monte Carlo pairs; derive the variance result for the BT-logistic case and check it on a toy simulation. Months 4–5: IMDb oracle experiments varying $n$ and the quality of $p_\eta$, showing that safe VRPO never loses to DPO when $p_\eta$ is poor, whereas plain VRPO might (Theorem 6.2's $\|p_\eta-p^*\|$ term). Then one HH run. Write-up.

**Shape B: "unlabelled prompts / AI labels" (more novel, riskier).** Extend the VRPO loss to an OSS setting with $N\gg n$ unlabelled prompts, possibly with LLM-judge labels as PPI predictions. Derive the influence-function form, which brings in the $\gamma$ trade-off of Xu Thm 4.1. Show label-efficiency curves on IMDb (oracle) and TL;DR. The risk is that the judge model's preferences become a second source of bias, and LLM-judge calls cost money.

### 4.3 Open questions

- **[Paper]** DPO asks whether self-labelling with the DPO policy can "make effective use of unlabeled prompts" (DPO §7, p. 10). It also flags reward over-optimisation and the effect of the judge prompt on GPT-4 win rates.
- **[Paper]** Xu et al. list two open problems: Donsker conditions fail for high- or infinite-dimensional nuisances, and double/debiased ML may help; and efficient SSL under covariate shift is "relatively open" (§9, p. 22). **[Interpretation]** Both arise directly in RLHF, where $p_\eta$ is a neural network and the prompts in labelled and unlabelled pools may differ.
- **[Paper]** PPI says it gives no gain when predictions are poor or the unlabelled set is small, and that mixed distribution shifts remain open (Conclusions, p. 5 of 6).
- **[Paper]** VRPO: the gain depends on a well-specified $\pi_{\rm ref}$ (§5.3, p. 12) and on $p_\eta$ being close to $p^*$ (Thm 6.2). Assumption (B2) is "restrictive" (supplement p. 25). VRPO has no explicit future-work section; its Conclusion (§7) only summarises. **[Interpretation]** Open questions it leaves: how many Monte Carlo responses to use; whether to estimate the correction coefficient; using unlabelled prompts; and what happens when $\pi_{\rm ref}$ is only approximately known (as in TL;DR).
- **[Paper]** InstructGPT: one rater per comparison, disagreement among labellers, and the question of "who are we aligning to?" (§5.2–5.3, pp. 18–19). It suggests that comparisons may not be the most efficient feedback signal (§5.4, p. 20).

## 5. Background knowledge required

| Area (Maths / Statistics / CS-ML) | Item | Status | Rough effort if not covered | Where it's needed |
|---|---|---|---|---|
| Statistics | Logistic regression, MLE, cross-entropy loss | covered by my modules | n/a | BT reward model (InstructGPT Eq. 1; DPO Eq. 2) |
| Statistics | M-estimation asymptotics: Taylor expansion, sandwich variance, $\sqrt n$-normality | partly covered | 1–2 weeks | VRPO Thm 6.2 proof; any variance result you prove |
| Statistics | Control variates, Monte Carlo variance reduction | partly covered | a few days | VRPO Eq. 3; multiple-sample extensions |
| Statistics | Semiparametric efficiency: influence functions, tangent spaces, efficiency bounds | new to me | 3–4 weeks to read Xu et al. comfortably | Xu et al. §2–4; framing any "efficient" claim |
| Statistics | Doubly robust estimation / missing data (MCAR, AIPW ideas) | new to me | 1–2 weeks | VRPO Thm 6.1; Xu et al. §6 |
| Statistics | Prediction-powered inference, PPI++ | new to me | a few days | PPI-style corrections with LLM-judge labels |
| Maths | Measure-theoretic probability, LLN/CLT, conditional expectation | covered by my modules (this term) | n/a | all proofs |
| Maths | Empirical-process conditions (Donsker classes) | new to me | 2–3 weeks if needed; can mostly be cited | Xu et al. Assumption 3.1 |
| Maths | KL divergence, convex optimisation basics | partly covered | a few days | DPO Eq. 3–4 derivation (App. A.1) |
| CS-ML | RL basics: policies, rewards, policy gradient, PPO, GRPO | new to me | 2–3 weeks for working knowledge | InstructGPT §3.5; VRPO two-stage variant |
| CS-ML | Transformers, autoregressive LMs, tokenisation, sampling temperature | partly covered | 1–2 weeks | all LLM experiments |
| CS-ML | PyTorch and the Hugging Face stack (transformers, TRL, datasets) | new to me | 3–4 weeks to be productive | VRPO code is built on TRL (supplement §9) |
| CS-ML | GPU training practicalities: memory, mixed precision, batching, cluster job scheduling | new to me | 2–3 weeks, ongoing | every fine-tuning run |
| CS-ML | LLM-as-judge evaluation, win rates, AlpacaEval | new to me | a few days | DPO §6.4; VRPO §5.2 |

**Biggest gap.** **[Interpretation]** The statistics is within reach, because the needed results are M-estimation asymptotics that build directly on this term's inference module. The real gap is *engineering*: getting fluent with PyTorch, TRL and GPU cluster workflows, plus enough RL to understand PPO and GRPO. That is a term-length effort if started from scratch, and it should begin before the formal project period, ideally by reproducing a DPO run on a small model.

## 6. Practicalities

### Code

- **[Paper]** VRPO: "The code is available at https://github.com/VRPO/VRPO" (Abstract, p. 1). Baselines use Hugging Face TRL (von Werra et al. 2020); the preference model uses the `general-preference/general-preference-model` framework of Zhang et al. 2024a with a two-dimensional value head; no hyperparameter tuning was done (supplement §9, p. 26).
- **[Paper]** DPO: a PyTorch snippet of the loss is printed in App. B (p. 20). No repository link for DPO itself appears in the PDF. It links third-party models and code: CarperAI's TL;DR SFT model, `reciprocate/ppo_hh_pythia-6B`, and `github.com/CarperAI/trlx` (footnotes, p. 9).
- **[Paper]** PPI: Python package `ppi-py`, Zenodo doi:10.5281/zenodo.8403931 (ref. 5), which also reproduces the experiments (p. 2 of 6).
- **[Paper]** InstructGPT: releases model *samples* at https://github.com/openai/following-instructions-human-feedback (footnote 7, p. 10). The PDF says nothing about releasing training code or models.
- **[Paper]** Xu et al.: the PDF does not mention code.

### Data

- **[Paper]** IMDb reviews (Maas et al. 2011; 50,000 reviews), used with the classifier `siebert/sentiment-roberta-large-english` as an oracle reward (VRPO §5.1; DPO App. C.1).
- **[Paper]** Anthropic Helpful and Harmless (Bai et al. 2022), described in DPO as 170k dialogues (DPO §6, p. 7; VRPO §5.2).
- **[Paper]** Reddit TL;DR (Völske et al. 2017) with human preferences from Stiennon et al. (2020) (VRPO §5.3; DPO §6).
- **[Paper]** AlpacaEval 2.0 for out-of-distribution evaluation (VRPO §5.2).
- **[Paper]** Neither VRPO nor DPO explicitly calls these datasets "public". DPO says "one would like to reuse preference datasets publicly available" (§4, p. 5), and VRPO uses a "public model trained by CleanRL" (p. 12). **[Interpretation]** They are standard benchmarks, but check the licence and access before relying on this.
- **[Paper]** PPI datasets are on Zenodo, doi:10.5281/zenodo.8397451 (ref. 6). InstructGPT's prompts come from OpenAI API customers and labellers (§3.2), and the PDF does not describe releasing them. Xu et al. use simulated data only (§8).

### Compute

**[Paper] What the papers report.**

- **VRPO:**
  - Models: Qwen2-0.5B SFT on IMDb; Qwen2.5-1.5B SFT on HH; `cleanrl/EleutherAI_pythia-1b-deduped__sft__tldr` on TL;DR (supplement §9.1–9.2, pp. 26–27). The auxiliary preference model uses the same base models.
  - Evaluation: GPT-4o-mini (win rates) and a GPT-4-Turbo annotator (AlpacaEval).
  - Training length: DPO 3 epochs, VRPO 1 epoch on IMDb (p. 26).
  - **No GPU type, GPU count or run time is reported.**
- **DPO:**
  - Models: GPT-2-large (IMDb), a GPT-J SFT model (TL;DR), Pythia-2.8B (HH), "up to 6B parameters" (§1, §6).
  - Settings: batch size 64 (App. B). Part of the compute came from Stanford CRFM (Acknowledgements).
  - **No GPU details are given.**
- **InstructGPT:** 1.3B, 6B and 175B policies with a 6B reward model. The 175B SFT model needed 4.9 petaflop/s-days and 175B PPO-ptx 60 petaflop/s-days, against 3,640 for GPT-3 pre-training (§5.1, p. 17). Far beyond MSc scale.
- **PPI and Xu et al.:** statistical computations and simulations ($n=1000$, 1,000 replications in Xu §8). Laptop scale.

**[Interpretation] Feasibility.**

- *Laptop:* enough for all the statistical prototyping, such as BT/logistic simulations of safe versus fixed-coefficient corrections, PPI-style experiments, and perhaps a tiny GPT-2-small debugging run. It is not enough for the LLM experiments the brief implies.
- *University GPU (cluster or cloud):* the realistic target is VRPO's own scale, 0.5B–1.5B models. A VRPO step holds roughly three models (policy, frozen reference and auxiliary preference model) and must *generate* fresh responses from $\pi_{\rm ref}$, which is slow compared with a forward pass. My rough guess is that a 0.5B model is comfortable on one 24–48 GB GPU, while a 1.5B model with full fine-tuning probably wants 40–80 GB, or parameter-efficient methods. These are my estimates, not figures from the papers.
- *Budget:* expect many runs (seeds × labelled-set sizes × methods) and several hours per run. Plan a compute budget of hundreds of GPU-hours, and budget separately for LLM-judge API calls.
- *Where to economise:* the synthetic IMDb set-up gives the most statistical evidence per GPU-hour, because the true reward is cheap to evaluate and no paid judge is needed.

## 7. Questions for the proposal meeting

1. **How should the project position itself relative to VRPO?** VRPO already describes itself as adapting SSL to LLM fine-tuning and claims no prior work does so (VRPO §2, p. 5). Is the dissertation meant to *extend* VRPO (e.g. safe or efficient coefficients, more Monte Carlo samples, unlabelled prompts), or to develop a *different* SSL mechanism? This decides what counts as novel.
2. **What should "unlabelled data" mean here?** Extra $\pi_{\rm ref}$ responses, extra unlabelled prompts, or AI/LLM-judge labels used PPI-style? Each leads to a different estimator, different theory (ISS-like versus OSS with $\gamma$) and different compute cost.
3. **Should the method be "safe"?** Should the extension estimate the correction coefficient so that it is never worse than the base RLHF loss, as in Xu et al. Thm 4.3? VRPO's gain depends on $\|p_\eta-p^*\|$ (Thm 6.2), so this is a natural, well-scoped contribution. Is it enough for a paper?
4. **How much theory is expected?** Is a fixed-dimension variance comparison (sandwich-formula level) enough, or does Dr Shi want efficiency-bound results in the spirit of Xu et al.? This sets how many weeks go to proofs versus code.
5. **One-stage or two-stage?** Focus on DPO-type training (cheaper; VRPO's main results) or also reward model plus PPO/GRPO? Two-stage training roughly doubles the engineering effort.
6. **What compute is available, and on what terms?** Is there access to the group's GPUs or an LSE/university cluster, and with what GPU memory? Who pays for GPT-4o-mini/AlpacaEval judge calls? The answer determines the model sizes (0.5B against 1.5B) and how many seeds are affordable.
7. **Can I build on the VRPO repository and get help with it?** Is https://github.com/VRPO/VRPO the current version, and can I contact the co-authors (e.g. Kai Ye, also at LSE) about set-up? Reproducing the baseline quickly is the biggest schedule risk.
8. **Which benchmarks count as primary evidence?** The IMDb synthetic oracle (clean statistics) or HH/TL;DR with LLM judges (closer to practice)? And how should repeated-seed uncertainty be reported, given that VRPO's tables give point win rates?
9. **What paper is the target, and what is the timeline?** The brief mentions an ML conference *or* a statistics journal. These require different emphases and deadlines. Is the dissertation expected to be paper-ready by submission, or is it a first stage of a longer collaboration?
10. **Two discrepancies in VRPO.** Can Dr Shi clarify the IMDb sample size (25,000 in §5.1 against 250,000 in supplement §9.1)? And how should the $d^{3/2}/n^{3/2}$ terms in Theorem 6.2 be interpreted when $d$ is the size of an LLM? This matters if the dissertation reuses that theoretical template.
