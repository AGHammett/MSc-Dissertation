# Variance-reduced Alignment for Large Language Models: Overview

**Supervisor:** Dr Chengchun Shi · **Prepared:** 21 October 2026 · **Sources:** the brief and the 3 supplied papers only

> **Labels.** **[Paper]** a paper states it (with reference) · **[Brief]** the brief states it · **[Interpretation]** my own reading. Check it before relying on it.

Paper shorthands used below: **InstructGPT** = Ouyang et al. (2022); **DPO** = Rafailov et al. (2023/2024); **VRPO** = Ye, Zhou, Zhu, Quinzan and Shi, arXiv v6 (2026). Page numbers are the printed ones. VRPO's main text points to "Section S.1.2", "S.2", "S.3.1" and so on of its supplement, but the supplement in the supplied PDF is actually numbered Sections 8–10 (proofs = 8, implementation = 9, extra results = 10). I cite the printed numbering (8, 9, 10).

## 1. The brief

**[Brief]** Reinforcement learning from human feedback (RLHF) is the standard way to align large language models (LLMs) with human preferences, but most RLHF algorithms rely on the Bradley–Terry (BT) model of preferences, whose assumptions often fail to capture how complex and variable real human preferences are. Ye et al. (2025) proposed variance-reduced preference optimisation (VRPO), which is meant to improve the sample efficiency and robustness of existing RLHF methods when the model is misspecified, and they showed strong results on the IMDb, Helpful–Harmless (HH) and TL;DR datasets. The project aims to push VRPO further in two ways: (i) improve its *computational and statistical efficiency*, and (ii) extend it to the *UltraFeedback* dataset, which the brief describes as more complex than the other three in both data scale and response complexity. The brief says the project "will be coding intensive" and that, if it succeeds, it should lead to a paper suitable for a top-tier ML conference or a statistics journal.

**Project type:** a mix of computational and methodological, with **computational dominant**. The brief explicitly says it is coding intensive, and one of its two concrete deliverables (UltraFeedback) is an empirical scaling exercise. The "statistical efficiency" direction leaves room for a methodological, and possibly theoretical, contribution, but the brief does not ask for proofs.

## 2. Paper by paper

Recommended reading order: **InstructGPT → DPO → VRPO.** InstructGPT sets up the three-step RLHF pipeline (supervised fine-tuning, reward model, policy optimisation with PPO) that both later papers take as given. DPO removes the separate reward model and RL loop, and its training pipeline is the one VRPO's implementation "parallels" (**[Paper]** VRPO §5, p. 8). VRPO is the centrepiece and only makes sense once you know what the BT loss, the reference policy $\pi_{\text{ref}}$ and the DPO loss are. If time is short, read InstructGPT §1, §3 and §5.3–5.4, DPO §3–5 and §6.1–6.2, then VRPO in full.

### 2.1 InstructGPT (Ouyang et al., 2022)
arXiv:2203.02155v1 [cs.CL], 4 March 2022 (OpenAI). The PDF does not print a venue. VRPO's bibliography cites it as NeurIPS 35.

- **Problem.** Larger language models are not automatically better at following a user's intent. They can be untruthful, toxic or unhelpful, which the paper calls "misaligned" (**[Paper]** abstract; §1, pp. 1–2).
- **Approach.** A three-step pipeline (**[Paper]** §3.1, p. 6; Fig. 2, p. 3):
  1. *Supervised fine-tuning (SFT)*: GPT-3 is fine-tuned on about 13k labeller-written demonstrations.
  2. *Reward model (RM)*: a 6B-parameter model is trained on labeller rankings of $K=4$–$9$ responses per prompt (about 33k prompts) using the BT-type pairwise loss $-\binom{K}{2}^{-1}\mathbb{E}\,[\log\sigma(r_\theta(x,y_w)-r_\theta(x,y_l))]$ (**[Paper]** §3.5, eq. (1), p. 8).
  3. *RL*: the SFT model is optimised with PPO against the RM, plus a per-token KL penalty to the SFT model with coefficient $\beta$ and optionally a pretraining log-likelihood term with coefficient $\gamma$ ("PPO-ptx") (**[Paper]** §3.5, eq. (2), p. 9). Dataset sizes are in Table 6. Hyperparameters ($\beta=0.02$, 256k episodes, $\gamma=27.8$) are in Appendix C.4, p. 41.
- **Main findings and results.**
  - Labellers prefer outputs of the 1.3B InstructGPT to those of the 175B GPT-3 (**[Paper]** abstract; Fig. 1, p. 2). The 175B InstructGPT is preferred to 175B GPT-3 85 ± 3% of the time, and to few-shot GPT-3 71 ± 4% of the time (**[Paper]** §4.1, p. 11).
  - Truthfulness improves (TruthfulQA, and closed-domain hallucination rate of 21% vs 41%), toxicity improves a little, and bias does not improve (**[Paper]** §1, p. 3; §4.2).
  - There is an "alignment tax" on public NLP benchmarks, and PPO-ptx largely removes it (**[Paper]** §1, pp. 3–4).
  - Inter-labeller agreement is about 72.6 ± 1.5% (**[Paper]** §3.4, p. 8). Reward models predict held-out labellers' preferences with 69.6 ± 0.9% accuracy (**[Paper]** §4.1, p. 12). For this project, the point is that the human preference labels are themselves very noisy.
  - Alignment is cheap relative to pretraining: 4.9 petaflop/s-days for the 175B SFT model and 60 for 175B PPO-ptx, against 3,640 for GPT-3 (**[Paper]** §5.1, p. 17).
- **Key assumptions.** Preferences follow a reward-difference (BT-type) model. The preferences being aligned to are those of about 40 contractors and the researchers, not "human values" in general (**[Paper]** §5.2, p. 18). Most comparisons are labelled by only one contractor (**[Paper]** §5.3, p. 19).
- **Relation to the other papers.** This is the "two-stage" reward-then-RL approach that VRPO calls two-stage optimisation (**[Paper]** VRPO §2, p. 4). DPO's §3 restates exactly this pipeline before replacing steps 2–3. **[Interpretation]** It also supplies the empirical motivation for VRPO: noisy, inconsistent labellers (agreement of about 73%) suggest that the BT model is misspecified.

### 2.2 DPO (Rafailov et al., 2023)
arXiv:2305.18290v3 [cs.LG], 29 July 2024. Footer: 37th Conference on Neural Information Processing Systems (NeurIPS 2023).

- **Problem.** The RLHF pipeline (fit a reward model, then run PPO) is complex, unstable and expensive, because it needs several LMs and sampling from the policy inside the training loop (**[Paper]** abstract; §1, p. 2).
- **Approach.** Start from the KL-regularised objective $\max_\pi \mathbb{E}[r(x,y)] - \beta\,\mathrm{KL}(\pi\|\pi_{\text{ref}})$ (**[Paper]** eq. (3), p. 3). Its optimiser is $\pi_r(y|x)=\pi_{\text{ref}}(y|x)\exp(r(x,y)/\beta)/Z(x)$ (eq. (4), p. 4). Inverting gives $r(x,y)=\beta\log\frac{\pi_r(y|x)}{\pi_{\text{ref}}(y|x)}+\beta\log Z(x)$ (eq. (5)). Under BT only reward *differences* matter, so $Z(x)$ cancels, and the reward-model likelihood becomes a likelihood in the policy itself:
  $$\mathcal{L}_{\text{DPO}}(\pi_\theta;\pi_{\text{ref}})=-\mathbb{E}\Big[\log\sigma\Big(\beta\log\tfrac{\pi_\theta(y_w|x)}{\pi_{\text{ref}}(y_w|x)}-\beta\log\tfrac{\pi_\theta(y_l|x)}{\pi_{\text{ref}}(y_l|x)}\Big)\Big]$$
  (**[Paper]** eq. (7), p. 4). This is plain binary cross-entropy, with no RL loop and no sampling during training.
- **Main findings and results.**
  - *Theory*: Theorem 1 (p. 6, proof in App. A.6) says that, under "mild assumptions", every reward equivalence class consistent with Plackett–Luce/BT can be written as $\beta\log(\pi/\pi_{\text{ref}})$, so the reparameterisation loses no generality. Lemmas 1–2 (p. 5) show that rewards differing by a function of $x$ give the same preferences and the same optimal policy. §5.2 (p. 6) argues that PPO's instability comes from the normalising term (a soft value function), which DPO avoids.
  - *Experiments*: On IMDb with a ground-truth sentiment reward, DPO's reward–KL frontier dominates PPO's, even PPO with access to the true reward (**[Paper]** §6.1, Fig. 2 left, pp. 7–8). On TL;DR, the GPT-4 win rate against reference summaries is about 61% at temperature 0, versus 57% for PPO (§6.2, p. 9). On single-turn HH, DPO is the only computationally efficient method that beats the chosen responses (Fig. 3, p. 8). Out of distribution (CNN/DailyMail), the win rate is 0.36 vs 0.26 for PPO (Table 1, p. 9). GPT-4 judgements agree with humans about as often as humans agree with each other (Table 2, p. 10).
  - Models go up to 6B parameters: GPT-2-large (IMDb), a GPT-J SFT model (TL;DR) and Pythia-2.8B (HH) (**[Paper]** §6, pp. 7–9; App. C.1, p. 19). Defaults are $\beta=0.1$ ($0.5$ for TL;DR), batch size 64, RMSprop, learning rate $10^{-6}$ (App. B, p. 19).
- **Key assumptions.** A BT (or Plackett–Luce) preference model. A reference policy that matches the policy which generated the preference data: when no SFT model is available, $\pi_{\text{ref}}$ is fitted by maximum likelihood on the preferred completions "to mitigate the distribution shift" (**[Paper]** §4, p. 5). For HH, the responses were "generated by a large (although unknown) language model" (§6, p. 7).
- **Relation to the other papers.** DPO is VRPO's main base algorithm. VRPO's "one-stage optimisation" is DPO-style reparameterisation (**[Paper]** VRPO eq. (5), p. 7), and VRPO's main HH experiment uses DPO-hinge as the base loss (VRPO §5.2, p. 11). **[Interpretation]** DPO's reliance on the BT model and on a correctly specified $\pi_{\text{ref}}$ is exactly what VRPO targets. DPO treats BT as given, while VRPO asks what happens when it is wrong.

### 2.3 VRPO (Ye, Zhou, Zhu, Quinzan and Shi, 2025/2026)
Title on PDF: "Robust Reinforcement Learning from Human Feedback for Large Language Models Fine-Tuning". arXiv:2504.03784v6 [stat.ML], 10 February 2026. No venue is printed. Shi and Quinzan are corresponding authors. Main text pp. 1–20, supplement pp. 21–33.

- **Problem.** Reward-based RLHF assumes $p^*(x,y^{(1)},y^{(2)})=\sigma\big(r^*(y^{(2)},x)-r^*(y^{(1)},x)\big)$ (**[Paper]** eq. (1), p. 6). This implies transitivity, context-independence and perfect rationality, all of which are empirically doubtful (§1, pp. 2–3). Misspecification can enter in two ways: (a) eq. (1) fails, or (b) the parametric reward class $r_\theta$ does not contain $r^*$ (§3, p. 6). The paper does not try to build a better preference model. It asks how to estimate *the same target* $\bar\theta=\arg\min_\theta\mathbb{E}[\mathcal{L}(\theta)]$ more efficiently when the model is misspecified (§1, p. 3; §6, p. 13).
- **Approach.** The key observation is that the reference policy that generated the response pairs is usually known, or can be well specified. So one can generate unlimited *unlabelled* response pairs from $\pi_{\text{ref}}$, which turns RLHF into a semi-supervised problem (**[Paper]** §2 "Semi-supervised learning", p. 5). Fit an auxiliary, more flexible preference model $p_\eta$ first (either non-reward-based, e.g. the general preference model of Zhang et al. 2024a, or a larger reward model). Then estimate the primary model $\theta$ by minimising
  $$\tilde{\mathcal{L}}(\theta)=\mathbb{E}_n\Big[\ell(X,Y^{(1)},Y^{(2)},Z;\theta)-\sum_{u=0}^{1}\ell(X,Y^{(1)},Y^{(2)},u;\theta)\,p_\eta(X,Y^{(1)},Y^{(2)},u)+\sum_{u=0}^{1}\mathbb{E}_{y^{(1)*},y^{(2)*}\sim\pi_{\text{ref}}(\cdot|X)}\,\ell(X,y^{(1)*},y^{(2)*},u;\theta)\,p_\eta(X,y^{(1)*},y^{(2)*},u)\Big]$$
  (**[Paper]** eq. (3), p. 7). The first term is the usual loss (e.g. cross-entropy, eq. (2)). The second subtracts the loss *predicted* by $p_\eta$ on the observed pair. The third adds back the same predicted loss averaged over fresh pairs drawn from $\pi_{\text{ref}}$. If $\pi_{\text{ref}}$ is correct, terms 2 and 3 have the same mean, so the target is unchanged. If $p_\eta\approx p^*$, they cancel most of the label noise (p. 7). **[Interpretation]** This is a control-variate / augmented-estimating-equation construction, the same idea as semi-supervised mean estimation or prediction-powered inference, which the paper cites as related (§2, p. 5), applied to the gradient of a misspecified M-estimator. It plugs into two-stage RLHF (fit $r_{\tilde\theta}$, then PPO on eq. (4)) or one-stage RLHF (DPO parameterisation, eq. (5)) (pp. 7).
- **Implementation (**[Paper]** §5, p. 8; §9, pp. 26–27).**
  - $\pi_{\text{ref}}$ is an SFT model.
  - The inner expectation is approximated by Monte Carlo using **a single sampled pair per prompt**.
  - $p_\eta$ is the BT model in §5.1 and the general preference model of Zhang et al. (2024a), "two-dimensional value head", in §5.2–5.3. All preference models are trained on the same base model and the same dataset as the primary model.
  - The code builds on Hugging Face TRL. There was "no hyperparameter-level fine-tuning" (§9, p. 26).
- **Main findings and results.**
  - *Theorem 6.1 (double robustness, p. 13).* In the correctly specified setting, $\bar\theta$ minimises $\mathbb{E}[\tilde{\mathcal{L}}]$ if *either* $\pi_{\text{ref}}$ *or* $p_\eta$ is correct. The proof (§8.1, pp. 21–22) is a short law-of-large-numbers argument.
  - *Theorem 6.2 (variance and MSE reduction, p. 14).* With $\pi_{\text{ref}}$ known and under conditions (A1)–(A4) (§8.2, p. 22: compact parameter space, interior $\bar\theta$, bounded first and second derivatives, non-singular Hessian $A(\bar\theta)$), and *whether or not the model is misspecified*, both estimators have bias $O(d/(n\lambda_{\min}))$ and
    $$\mathrm{Var}(\hat\theta)-\mathrm{Var}(\tilde\theta)=\underbrace{\tfrac1n A^{-1}HA^{-1}}_{\text{variance reduction}}+O\!\Big(\tfrac{d^{3/2}}{n^{3/2}\lambda_{\min}^2}\Big)+O\!\Big(\tfrac{\|p_\eta-p^*\|_\infty^2}{n\lambda_{\min}^2}\Big),$$
    where $H\succeq 0$. Its minimum eigenvalue is bounded below by a term proportional to how much the conditional expected gradient $\mathbb{E}_z[\nabla_\theta\mathcal{L}]$ varies across response pairs drawn from $\pi_{\text{ref}}$ (eq. (6), p. 14). From the proof (§8.2, p. 24), $H=\mathbb{E}\big[\mathbb{E}_z\nabla\mathcal{L}-\mathbb{E}_{z,y}\nabla\mathcal{L}\big]^2$, i.e. the between-response-pair variance of the score that the augmentation removes. The gain is zero if $\pi_{\text{ref}}$ is deterministic or if the model is correctly specified (expected gradient zero) (p. 14). This matches Table 1, p. 4: there is no asymptotic gain under correct specification.
  - *Theorem 6.3 (suboptimality gap, p. 15).* $\mathbb{E}R(\theta)=R(\bar\theta)+\mathrm{tr}\{\mathrm{Var}(\theta)(-\nabla^2_\theta J(\bar\theta))\}+O(d^{3/2}/(n^{3/2}\lambda_{\min}^3))$ for both estimators, so lower variance gives lower expected regret. The proof requires (B2) that $\bar\theta$ optimises $J$ over $\Theta$ (p. 24). The authors call this "restrictive" and give a weaker Theorem 3′ with a bias term $b(\cdot)$ satisfying $|b(\tilde\theta)|\le|b(\hat\theta)|$ (pp. 25–26).
  - *IMDb, synthetic BT labels (§5.1, pp. 8–10; Fig. 3).* The preference model is correct and the reward model is misspecified. VRPO, with an auxiliary model built from DPO's own estimated reward, beats DPO in expected reward and in the reward–KL frontier (VRPO uses $\beta=0.1$; DPO uses $\beta\in\{0.02,0.05,0.1\}$). Varying which of $\pi_{\text{ref}}$ and $p_\eta$ is correct gives expected reward of about 0.95 when both are correct, 0.8–0.95 when one is, and below 0.8 when neither is (empirical double robustness). A misspecified $p_\eta$ is simulated as $1-p_{\text{true}}$, and a misspecified $\pi_{\text{ref}}$ as the base Qwen2-0.5B (§9.1, p. 26).
  - *Anthropic HH (§5.2, pp. 10–12).* The preference model is argued to be misspecified, because earlier work found label-flip noise with $\epsilon\approx0.1$ (p. 10). VRPO (on DPO-hinge) beats nine baselines at all five sampling temperatures, with win rates of 0.53–0.98 (Table 3, p. 11). That is 0.77–0.81 against DPO and 0.81–0.84 against DPO-hinge, which the authors present as an ablation showing the gain is not due to the hinge loss. On AlpacaEval 2.0 against SFT, VRPO scores 93.79% (92.95% length-controlled) against 90.93% (92.16%) for the best baseline, Dr. DPO (Table 4, p. 12).
  - *TL;DR (§5.3, pp. 12–13; Fig. 4).* The reference policy is deliberately misspecified (a public CleanRL Pythia-1B SFT model trained on a filtered version of the data). VRPO still beats SFT and DPO, but by less than on HH.
  - *Two-stage (§10.2, pp. 29–30).* VR-PPO vs PPO has win rates of 0.48–0.64 (Table 7). VR-GRPO vs GRPO peaks at 0.77 (Table 8).
- **Key assumptions.** $\pi_{\text{ref}}$ is known or "well-specified" ("very close to the ground truth", footnote 2, p. 5). This is assumed to hold for HH because the SFT model was trained on HH (p. 6). $p_\eta$ is treated as fixed when analysing $\tilde\theta$. Regularity conditions (A1)–(A4) and (B1)–(B2) (pp. 22, 24) hold. The parameter dimension $d$ is finite and fixed. Response pairs are i.i.d. draws from $\pi_{\text{ref}}$ given $X$ (§3 DGP, p. 5).
- **Relation to the other papers.** It sits on top of both: two-stage (InstructGPT-style PPO) and one-stage (DPO). It inherits DPO's experimental tasks (IMDb, TL;DR, HH) and its GPT-judge evaluation, but its models are smaller: Qwen2-0.5B, Qwen2.5-1.5B and Pythia-1B (§9, pp. 26–27), against up to 6B in DPO. **[Interpretation]** Things to raise with the supervisor:
  1. DPO says HH responses came from an *unknown* LM (DPO p. 7), whereas VRPO treats an SFT model fitted to HH as a well-specified $\pi_{\text{ref}}$ (Table 2, p. 8). That is an approximation, not a known policy.
  2. The theory is classical fixed-$d$ M-estimation. With $d\sim10^9$ parameters, the $O(d^{3/2}/n^{3/2})$ remainders are not small, so the theory is best read as a guide to the mechanism.
  3. There are some internal inconsistencies. The prompt count is 25,000 on p. 9 but 250,000 in §9.1, p. 26. (B2) says "minimizer" of $J$ but the proof uses it as a maximiser (pp. 24–25). Table 8 is headed "GRPO vs. VR-GRPO" while the text reads it as VR-GRPO's win rate (p. 29). The supplement section labels do not match (see the note at the top).

## 3. How the papers fit together

**Common thread.** All three learn a policy from pairwise human preferences $(X,Y^{(1)},Y^{(2)},Z)$ under a KL constraint to a reference/SFT policy, and all three assume, at least as a working model, that preferences come from reward differences through a link $\sigma$.

```
 InstructGPT (2022)              DPO (2023)                       VRPO (2025/26)
 SFT -> RM (BT loss) -> PPO  ==> reparametrise r = β log π/πref ==> keep the same loss/target θ̄,
 "two-stage"                     closed-form, "one-stage"          add control-variate terms using
 assumes BT, big compute         assumes BT, πref matched          auxiliary p_η + fresh πref samples
                                                                   -> lower variance when BT/reward
                                                                      is misspecified; plugs into both
```

| Axis | InstructGPT | DPO | VRPO |
|---|---|---|---|
| Uses explicit reward model? | yes | implicit | either (both variants) |
| Uses RL in the loop? | PPO | no | optional (PPO/GRPO) or no (DPO-style) |
| Attitude to BT misspecification | not addressed (noted noisy labellers) | assumed correct | central concern |
| Role of $\pi_{\text{ref}}$ | KL anchor | KL anchor + reparametrisation | KL anchor + **source of unlabelled samples** |
| Theory | none formal | identifiability (Thm 1) | double robustness, variance/MSE, regret (Thms 6.1–6.3) |
| Largest policy model | 175B | ~6B | ~1.5B |
| Evaluation | human labellers | GPT-4 judge + small human study | GPT-4o-mini judge, AlpacaEval 2.0 |

**Settled (within these papers).** DPO-style one-stage training is a workable and much cheaper substitute for PPO at the sizes tested (DPO §6). Given a known $\pi_{\text{ref}}$, the VRPO augmentation leaves the target $\bar\theta$ unchanged and cannot increase the leading-order variance (VRPO Thm 6.2).

**Unsettled.**
- How large the gain is in practice, and how it depends on the quality of $p_\eta$ and on how well $\pi_{\text{ref}}$ is specified. VRPO §5.3 shows the gain shrinking under $\pi_{\text{ref}}$ misspecification but gives no theory for that case beyond double robustness in the correctly specified setting.
- Whether gains persist at larger scale, on richer data, or under human rather than GPT evaluation. DPO's limitations section raises scaling and dependence on the evaluator prompt (DPO §7, p. 10).
- What "the right preferences" are in the first place (InstructGPT §5.2–5.4).

## 4. Tie-in to the dissertation

### 4.1 What the proposed directions mean in practice

**(a) Improve VRPO's computational efficiency.** **[Interpretation]** Compared with DPO, each VRPO step also needs:
- response pairs sampled from $\pi_{\text{ref}}$ for every prompt (generation is the slow part of LLM work);
- $p_\eta$ evaluated on both the observed and the sampled pairs;
- forward and backward passes of $\pi_\theta$ on the extra pair.

Because $p_\eta$ and $\pi_{\text{ref}}$ are fixed before the primary fit (**[Paper]** §4, p. 6), much of this can be done once, offline: pre-generate the pairs, cache $\pi_{\text{ref}}$ log-probabilities and cache $p_\eta$ outputs. Note too that the loss for $u=0$ and $u=1$ on the same pair uses a single forward pass. Concrete projects would be:
- profile VRPO against DPO in wall-clock time and memory;
- design a cached or offline variant;
- use a cheaper $p_\eta$ (a smaller model, or a LoRA head sharing the policy backbone) and measure the loss in variance reduction;
- sample the augmentation term less often than every step.

None of these are proposed in the paper. They are my reading of where the cost lies.

**(b) Improve VRPO's statistical efficiency.** **[Interpretation]** Natural levers that fall straight out of eq. (3) and Theorem 6.2:
1. *More Monte Carlo pairs per prompt.* The paper uses one (**[Paper]** §5, p. 8). Averaging over $M>1$ pairs reduces the extra noise that the third term adds, at a cost in compute that is linear in $M$. This links (a) and (b).
2. *A tuned control-variate coefficient.* Eq. (3) gives the augmentation a weight of 1. Classical control-variate reasoning suggests an optimal weight that shrinks towards 0 when $p_\eta$ is poor, and estimating that weight could protect against a bad auxiliary model.
3. *Sample splitting / cross-fitting for $p_\eta$.* The paper trains $p_\eta$ on the same data as the primary model (**[Paper]** §9, p. 26), while the theory treats $p_\eta$ as fixed. Cross-fitting is the standard semiparametric fix and could be tested empirically and justified theoretically.
4. *Better auxiliary models.* Theorem 6.2's remainder depends on $\|p_\eta-p^*\|_\infty$, so a better $p_\eta$ (larger, or trained on more data) should help.
5. *Relaxing "known $\pi_{\text{ref}}$".* For example, estimate $\pi_{\text{ref}}$ and quantify the bias. This is directly relevant to (c).

**(c) Extend to UltraFeedback.** **[Paper]** None of the three supplied papers mentions UltraFeedback, so everything about the dataset (its size, how its responses were generated, how its labels were produced) has to come from outside the supplied material, presumably from the supervisor or the dataset's own documentation. **[Brief]** The brief says only that it is larger and has more complex responses. **[Interpretation]** Practically, this means:
- choosing a base model and SFT procedure;
- deciding what $\pi_{\text{ref}}$ is (VRPO needs the policy that generated the responses to be known or well specified, footnote 2, p. 5, and §5.3 shows the gains shrink when it is not);
- training a $p_\eta$ on UltraFeedback;
- running DPO and a few baselines plus VRPO;
- evaluating, probably with an LLM judge and/or AlpacaEval 2.0 as in VRPO §5.2.

Scale is the main risk. Longer responses mean more memory per example, and a bigger dataset means more GPU-hours.

### 4.2 What a dissertation would plausibly involve

**[Interpretation]** Two plausible shapes:

- **Shape A, "Efficient VRPO at scale" (mostly computational).**
  1. Reproduce VRPO vs DPO on HH with the released code (Qwen2.5-1.5B, or a smaller model if compute is tight).
  2. Implement an offline/cached VRPO and profile cost.
  3. Run an ablation over the number of Monte Carlo pairs $M$ and the size of the auxiliary model.
  4. Port the best variant to UltraFeedback and compare with DPO and one or two robust baselines under a fixed compute budget.

  Deliverables: code, a cost–accuracy trade-off study, and UltraFeedback results.

- **Shape B, "Statistically efficient VRPO" (methodological plus small-scale experiments).**
  1. Propose a weighted / cross-fitted VRPO estimator.
  2. Derive its asymptotic variance in the fixed-$d$ setting of Theorem 6.2, which is within reach using M-estimation and sandwich-variance arguments.
  3. Verify the theory in a cheap simulation where the truth is known: a small parametric "policy" with intransitive or noisy preferences, or the IMDb synthetic-label setting of §5.1.
  4. Show one real-data experiment, on HH or a subset of UltraFeedback.

  Deliverables: a new estimator, a proposition with proof, simulations, and one LLM experiment.

In both shapes, expect most of the time to go on engineering (data pipelines, GPU jobs, evaluation harnesses) rather than on mathematics.

### 4.3 Open questions

VRPO has no explicit limitations or future-work section; its conclusion (§7, p. 15) only summarises. The open questions below are therefore partly drawn from what the paper concedes elsewhere, and are labelled accordingly.

1. **Reference-policy misspecification.** **[Paper]** "Effective variance reduction in VRPO relies on a well-specified behavior policy" (VRPO §5.3, p. 12). Gains are "more modest" on TL;DR, where $\pi_{\text{ref}}$ is wrong (p. 12). **[Interpretation]** There is no theory for the misspecified-$\pi_{\text{ref}}$ case, and this matters for any external dataset, UltraFeedback included.
2. **The regret theorem's restrictive assumption.** **[Paper]** The authors acknowledge that (B2) is "restrictive" (VRPO p. 25). Theorem 3′ relaxes it only partially.
3. **No hyperparameter tuning, single MC sample.** **[Paper]** VRPO §9, p. 26 and §5, p. 8. **[Interpretation]** Both leave room for efficiency gains.
4. **Two-stage implementation issues.** **[Paper]** "GRPO encounters an implementation issue under fully deterministic sampling" (VRPO p. 30), and VR-PPO loses at temperature 0 (Table 7, 0.48).
5. **Scaling and out-of-distribution generalisation.** **[Paper]** DPO lists scaling to models "orders of magnitude larger", out-of-distribution generalisation, reward over-optimisation, and evaluator-prompt sensitivity as open (DPO §7, p. 10).
6. **Whose preferences, and label noise.** **[Paper]** InstructGPT notes single-labeller comparisons, labeller disagreement, and the question of whether aligning to the average labeller is desirable (InstructGPT §5.3, p. 19; §5.2, p. 18). It also notes that comparisons may not be the most efficient feedback signal (§5.4, p. 20). **[Interpretation]** These are exactly the sources of BT misspecification that VRPO exploits.
7. **Evaluation by LLM judge.** **[Paper]** DPO found that GPT-4 prefers longer, more repetitive summaries under one prompt (DPO §6.4, p. 10). VRPO reports the same verbosity bias in GPT-4o-mini (VRPO §9.2, p. 27). **[Interpretation]** Any UltraFeedback result will inherit this concern.

## 5. Background knowledge required

| Area (Maths / Statistics / CS-ML) | Item | Status | Rough effort if not covered | Where it's needed |
|---|---|---|---|---|
| Statistics | MLE, cross-entropy / logistic loss, Bradley–Terry model | partly covered | a few days (BT specifically) | Eq. (1)–(2) of VRPO; DPO eq. (1)–(2) |
| Statistics | M-estimation under misspecification (pseudo-true parameter, sandwich variance $A^{-1}BA^{-1}$) | partly covered | 1–2 weeks | VRPO Thm 6.2 and proof §8.2 |
| Statistics | Control variates, semi-supervised / augmented estimators, double robustness | new to me | 2–3 weeks | VRPO §4, Thm 6.1; any "statistical efficiency" extension |
| Statistics | Sample splitting / cross-fitting | new to me | a week | Extension (b)(3) |
| Maths | Taylor expansions with $O_p$ / $o_p$, LLN/CLT for estimators | covered by my modules | — | VRPO proofs §8 |
| Maths | KL divergence, constrained optimisation, Gibbs/softmax form of optimum | partly covered | a few days | DPO eq. (3)–(5), App. A.1 |
| CS-ML | Transformers, autoregressive LMs, tokenisation, sampling temperature | partly covered | 1–2 weeks | All experiments |
| CS-ML | RL basics: policies, reward, policy gradient, PPO / GRPO | new to me | 2–3 weeks (enough to run, not to research) | InstructGPT §3.5; VRPO two-stage §10.2 |
| CS-ML | SFT, DPO and variants (IPO, cDPO, rDPO, hinge) | new to me | 1–2 weeks | VRPO baselines §5.2 |
| CS-ML | PyTorch + Hugging Face Transformers/TRL, mixed precision, gradient checkpointing, LoRA, multi-GPU jobs on a cluster (SLURM) | new to me | substantial: 3–6 weeks of hands-on practice | Every experiment; the brief's "coding intensive" |
| CS-ML | LLM evaluation: LLM-as-judge win rates, AlpacaEval, length control | new to me | a week | VRPO §5.2, Tables 3–4 |

**Biggest gap.** The largest gap is practical LLM engineering: fine-tuning billion-parameter models with TRL on GPUs, managing memory, generating samples, and running judge-based evaluation. The reader profile covers basic deep learning but not this, and the brief explicitly calls the project coding intensive. The statistics (M-estimation, control variates, double robustness) is the second gap. It sits much closer to the MSc statistical inference material and can be learned in a few weeks.

## 6. Practicalities

### Code
- **[Paper]** VRPO: "The code is available at https://github.com/VRPO/VRPO" (abstract, p. 1). The implementation follows Hugging Face TRL (von Werra et al., cited as https://github.com/huggingface/trl in VRPO's references), with Dr. DPO implemented by modifying TRL's DPO trainer. The preference model $p_\eta$ uses "the framework of general-preference/general-preference-model proposed by Zhang et al. (2024a)" (§9, p. 26). No URL is printed for that framework.
- **[Paper]** DPO gives PyTorch code for the loss in Appendix B (p. 19). No repository URL for DPO itself is printed in the supplied PDF. It references TRLX (https://github.com/CarperAI/trlx, footnote 6, p. 9) and Hugging Face checkpoints used as baselines.
- **[Paper]** InstructGPT releases model *samples* only: https://github.com/openai/following-instructions-human-feedback (footnote 7, p. 10). It releases no training code and no models.

### Data
- **IMDb** (Maas et al., 2011): 50,000 movie reviews (VRPO p. 8). Used by DPO and VRPO with synthetic labels from the public classifier `siebert/sentiment-roberta-large-english`.
- **Anthropic HH** (Bai et al., 2022): about 170k dialogues ending in a chosen/rejected pair (DPO p. 7). Used by DPO and VRPO.
- **Reddit TL;DR** with the preference annotations of Stiennon et al. (2020): used by DPO and VRPO. VRPO uses the public CleanRL SFT model `cleanrl/EleutherAI_pythia-1b-deduped__sft__tldr` (p. 27).
- **AlpacaEval 2.0** benchmark: VRPO's out-of-distribution evaluation (p. 11).
- **InstructGPT data**: OpenAI API prompts plus labeller-written prompts (SFT about 13k, RM about 33k, PPO about 31k prompts; §3.2, p. 7). These are proprietary, filtered for personal information, and not released.
- **Public?** **[Paper]** The papers refer to HH, TL;DR and IMDb by citation and use public Hugging Face model checkpoints. DPO says "one would like to reuse preference datasets publicly available" (p. 5). VRPO calls the CleanRL model "public" (p. 12), but neither paper explicitly states the licence or availability of the datasets themselves. **UltraFeedback** is not mentioned in any supplied paper.

### Compute
**[Paper] What is reported.**
- **VRPO:** policy sizes are Qwen2-0.5B (IMDb SFT, 3 epochs), Qwen2.5-1.5B (HH SFT, 3 epochs) and Pythia-1B (TL;DR, CleanRL SFT) (§9.1–9.2, pp. 26–27). DPO was trained for 3 epochs and VRPO for 1 on IMDb (p. 26). The auxiliary $p_\eta$ uses the same base model (p. 26). Evaluation uses the GPT-4o-mini API and AlpacaEval 2.0 with a GPT-4-Turbo annotator. **VRPO reports no GPU type, GPU count or run time.**
- **DPO:** policies up to about 6B (GPT-2-large, GPT-J SFT, Pythia-2.8B). Batch size 64, RMSprop, learning rate $10^{-6}$ (App. B, p. 19). The IMDb PPO baseline uses 1024 samples per PPO step (App. C.1). **No GPU type, count or run time is reported**, beyond acknowledging Stanford CRFM compute (p. 10).
- **InstructGPT:** 1.3B, 6B and 175B policies, with a 6B reward model and value function (§3.5, p. 8; App. C.2, p. 41). Compute is given only in aggregate: 4.9 petaflop/s-days for 175B SFT and 60 for 175B PPO-ptx (§5.1, p. 17). No GPU details are given.

**[Interpretation] What is feasible.**
- *Laptop:* only toy versions, such as a simulation study with a small parametric model, or GPT-2-small-scale experiments on IMDb. That is useful for checking variance-reduction claims, but it will not reproduce the paper.
- *Single GPU:* a rough memory calculation for full fine-tuning of a 1.5B model with Adam in mixed precision is about 16 bytes/parameter, so roughly 24 GB for the trainable policy alone. On top of that come a frozen $\pi_{\text{ref}}$ and $p_\eta$ (about 3 GB each in bf16) and activations, which grow with response length. So reproducing the HH experiment realistically needs one 40–80 GB data-centre GPU (A100/H100 class), or LoRA / gradient checkpointing on a 24 GB card.
- *UltraFeedback:* longer responses and more data plausibly mean several such GPUs for days rather than hours.
- *Hidden costs:* generating $\pi_{\text{ref}}$ samples for every prompt (offline, but slow) and paying for an API judge (GPT-4o-mini) for thousands of comparisons.

The amount of GPU time available through LSE or Dr Shi's group is the deciding practical question. The supplied papers say nothing about it.

## 7. Questions for the proposal meeting

1. **Which direction leads: efficiency or UltraFeedback?** The brief lists both. They point towards rather different dissertations (Shape A vs Shape B, §4.2), and doing both thoroughly may not fit an MSc timeline.
2. **What GPU resources can I use (type, count, hours), and is there an API budget for GPT-4o-mini / AlpacaEval judging?** Neither VRPO nor DPO reports hardware, and feasibility at 1.5B+ parameters depends on this entirely.
3. **What exactly does "computational efficiency" mean to you: wall-clock time, memory, number of $\pi_{\text{ref}}$ samples, or the cost of training $p_\eta$?** Each needs a different design, e.g. caching versus a lighter auxiliary model.
4. **What does "statistical efficiency" mean beyond Theorem 6.2: an optimally weighted augmentation term, cross-fitting $p_\eta$, more Monte Carlo pairs, or a semiparametric efficiency bound?** This sets how much theory is expected.
5. **For UltraFeedback, what plays the role of $\pi_{\text{ref}}$?** VRPO needs a known or well-specified reference policy (footnote 2, p. 5), and none of the supplied papers describes how UltraFeedback's responses were generated. If the generating policy is unknown, the variance reduction may weaken, as on TL;DR (§5.3).
6. **Which base model and size for UltraFeedback (e.g. reuse Qwen2.5-1.5B as in VRPO §9.2)?** Comparability with the paper versus feasibility.
7. **Which auxiliary model $p_\eta$ should I use: the general preference model of Zhang et al. (2024a), as in the paper, or something cheaper?** It drives both the cost and the size of the gain (Theorem 6.2's $\|p_\eta-p^*\|_\infty$ term).
8. **Should I work from the released repo (github.com/VRPO/VRPO), and is there internal code or checkpoints from the paper (SFT models, trained $p_\eta$) I can reuse?** Reuse could save weeks of setup.
9. **Can you clarify the inconsistencies I noticed: 25,000 vs 250,000 IMDb prompts (p. 9 vs p. 26), the "minimizer" in (B2), the Table 8 header, and the S.x vs 8–10 section labels?** These matter if I am reproducing or extending the paper.
10. **Which baselines and evaluation protocol count as convincing for a paper submission (LLM judge, AlpacaEval, human evaluation, number of seeds)?** VRPO reports single runs without error bars in Tables 3–4, so deciding on seeds and uncertainty quantification early affects the compute budget.
11. **One-stage (DPO-style) only, or also two-stage (PPO/GRPO)?** Two-stage is far more expensive and fragile (VRPO §10.2), and it changes which RL background I need.
12. **What is the target venue and timeline, and what would count as a successful MSc outcome if the paper-level result does not materialise?** The brief aims at a top venue, and I want a fallback scope agreed in advance.
