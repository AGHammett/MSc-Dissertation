# Semi-supervised RLHF — dissertation brief review

Oct 15, 2026 · @Alex

## How to read this

The one-line verdict: your supervisor's group has already published one semi-supervised RLHF method (VRPO, paper 4), so the dissertation has to be a *next step* beyond it, and Xu–Witten–Shojaie (paper 5) hands you the theory to say exactly what that step is.

Every claim is labelled:

- **\[Paper\]** — what the paper states, with section, theorem or equation numbers so you can check.
- **\[Inference\]** — my own reading, derivation or speculation. Treat as a hypothesis to verify.
- **\[Search\]** — from a literature search run on 15 October 2026 (cited in Sources).

Papers are numbered by the order I recommend reading them in Stage 3, not by attachment order: (1) Ouyang et al. 2022, InstructGPT; (2) Rafailov et al. 2023, DPO; (3) Angelopoulos et al. 2023, Prediction-powered inference (PPI); (4) Ye, Zhou, Zhu, Quinzan & Shi, Robust RLHF / VRPO (arXiv v6, Feb 2026); (5) Xu, Witten & Shojaie 2025, Unified framework for semiparametrically efficient semi-supervised learning.

Assumptions I had to make, because the placeholders in your message were unfilled:

- Supervisor: Chengchun Shi (named on the brief).
- Winter modules: ST418 Advanced Time Series, ST451 Bayesian ML, ST455 Reinforcement Learning.
- Time budget: submission around mid-to-late August 2027 (typical for LSE MSc dissertations; not verified for ST499), about 8–10 hours a week in term and full-time from June. Every feasibility verdict in Stage 4 is conditional on this; correct it and the verdicts shift.

The brief cites no papers, so I can't confirm these five are the full set it relies on. Material the attached papers lean on but which isn't attached is listed under Sources; I describe it only as far as the attached papers do.

## Stage 1 — The brief

### The question, in my words

Human preference labels are the expensive input to RLHF; unlabeled inputs are nearly free. The brief asks: can you use unlabeled data to estimate the reward model, or the aligned policy, more efficiently than from the labeled comparisons alone, and with what guarantees? Statistically this is semi-supervised M-estimation where the label is a binary preference Z and the covariate is the triple (prompt X, response Y⁽¹⁾, response Y⁽²⁾).

### What a successful dissertation would deliver

- **A method**: a loss or estimator that uses unlabeled data and plugs into an existing RLHF pipeline (DPO-style one-stage, or reward-model-then-policy two-stage).
- **A guarantee**: at minimum, that it is never worse than the labeled-only baseline; ideally, an efficiency result saying how much it gains and when.
- **Evidence**: experiments where the gain can be measured against a known truth (a synthetic or oracle-reward setting), plus at least one real preference dataset.
- **Packaging** that could become a paper. The brief says "coding-intensive" and names top ML venues or statistics journals, so it expects both theory and code.

### Ambiguities to clarify

1. **What counts as "unlabeled data".** These are different problems with different theory:
   - (a) response pairs (X, Y⁽¹⁾, Y⁽²⁾) sampled from the reference policy for *labeled* prompts — free whenever π\_ref is known; this is what VRPO uses;
   - (b) extra *prompts* with no responses or labels (InstructGPT's 31k PPO prompts, Table 6);
   - (c) AI-judge or reward-model pseudo-labels on unlabeled pairs (a PPI-style surrogate);
   - (d) the raw pretraining corpus, which the brief alludes to ("LLMs are typically trained with massive amounts of unlabeled text") but which I can't see a clean statistical role for.
2. **How this differs from VRPO.** Paper 4 already calls itself semi-supervised (its Section 2, last paragraph) and is your supervisor's own work. Is the dissertation meant to extend VRPO, re-derive it, or take a separate route?
3. **The estimand.** Reward-model parameters, policy parameters, the policy's value or win rate, or a confidence interval for any of these? "Improve alignment" doesn't pick one.
4. **One-stage or two-stage.** They lead to very different compute bills and different statistical objects (Stage 4 argues for a two-stage, low-dimensional testbed).
5. **Compute and evaluation budget.** VRPO trained 0.5–1.5B models and judged with GPT-4o-mini (its Supplement Section 9). Is there GPU access, and who pays for judge API calls?
6. **Theory versus empirics.** How much proof is expected in an MSc dissertation versus a working method plus experiments?
7. **Paper expectations.** Does "suitable for submission" mean a target venue and deadline, and who would co-author?
8. **Starting code.** VRPO's repository (github.com/VRPO/VRPO) exists; is building on it expected or allowed?

## Stage 2 — Paper by paper

### Paper 1 · Ouyang et al. (2022), *Training language models to follow instructions with human feedback* (InstructGPT)

**Problem and contribution \[Paper\].** Next-token pretraining is misaligned with "follow the user's instructions helpfully and safely" (Section 1). The contribution is an empirical demonstration, at scale, that the three-step pipeline — supervised fine-tuning (SFT), reward model (RM), then PPO against the RM — makes GPT-3 much more preferred by human raters (Figure 2, Section 3.1).

**Setup and assumptions \[Paper\].**

- RM loss, Eq. (1): loss(θ) = −(1/C(K,2)) · E\_{(x, y\_w, y\_l)∼D}\[log σ(r\_θ(x, y\_w) − r\_θ(x, y\_l))\]. Labelers rank K = 4 to 9 outputs; all C(K,2) pairs from one prompt go in as a single batch element because shuffling them separately overfit (Section 3.5, footnote 5).
- RL objective, Eq. (2): maximise E\[r\_θ(x, y) − β log(π^RL\_φ(y | x) / π^SFT(y | x))\] + γ E\_{x∼D\_pretrain}\[log π^RL\_φ(x)\], with β = 0.02 and γ = 27.8 (Appendix C.4). γ = 0 is "PPO"; γ > 0 is "PPO-ptx".
- One 6B RM serves every policy size (Appendix C.2). RM rewards are shifted so demonstrations score 0 on average (Section 3.5).
- Data, Table 6: SFT about 13k prompts, RM about 33k prompts, PPO about 31k prompts **with no labels** (Section 3.2).

**Assumptions doing the heavy lifting.**

- &#91;Paper\] The Bradley–Terry (BT) link in Eq. (1): preference probability = σ of a reward difference. Everything downstream inherits it.
- &#91;Inference\] That the RM, trained on outputs from mostly SFT policies, stays accurate on PPO-policy outputs. The per-token KL penalty is the only guard against this distribution shift.
- &#91;Inference\] That labeler preferences are the target. Section 5.2 is explicit that they align to this specific group, not to "human values".

**Results.**

- Proved: nothing. This is an empirical paper.
- Shown empirically \[Paper\]: the 1.3B PPO-ptx model is preferred to the 175B GPT-3 (Figure 1). The 175B model is preferred 85 ± 3% of the time over GPT-3 and 71 ± 4% over few-shot GPT-3 (Section 4.1). Hallucination on closed-domain tasks falls from 41% to 21% (Section 1). The "alignment tax" on public NLP benchmarks is largely removed by the pretraining mix, and raising β alone does not fix it (Appendix E.6, Figures 33–34).
- RM generalisation \[Paper\]: accuracy 72.4 ± 0.4% on training labelers, 69.6 ± 0.9% on held-out labelers (Section 4.1). Inter-annotator agreement is about 73% (Section 3.4).

**Limitations.**

- &#91;Paper\] About 40 contractors, mostly one labeler per comparison (Section 5.3). Training prioritised helpfulness while final evaluation prioritised truthfulness and harmlessness (Section 3.4, Appendix B.2), so the labels and the evaluation target differ. The model hedges and accepts false premises (Section 4.3, Figure 9).
- &#91;Inference\] A roughly 73% agreement ceiling means a large share of the label noise is irreducible. That is the regime in which BT is plausibly misspecified, which matters for papers 4 and 5.
- &#91;Inference\] Comparisons within a prompt are correlated (the authors' own overfitting finding). The i.i.d.-tuple assumption used by papers 4 and 5 does not hold for K-wise rankings; it is closer to clustered data.

**Things that look wrong \[Inference, check them\].**

- Appendix E.2 says the "inter- and intra-group validation accuracies" are 72.4% and 69.6% "respectively", which reads the opposite way round to Section 4.1. The numbers agree; the labels look swapped.
- In Table 14 the CNN/DM and TLDR ROUGE-L rows are identical to three decimals across all 12 models, which suggests a copying error.
- Figures 26 and 27 (summarisation tasks) say "15 additional French / English pairs", apparently pasted from the translation figure.

**Role in the brief: foundational.** It defines the pipeline, the BT reward model, the KL-regularised objective and — the point for you — a natural split into labeled comparisons (RM data) and unlabeled prompts (PPO data). Read Sections 1, 3.1–3.5, 4.1 and 5.2–5.3; skim the rest.

## Stage 3 — The literature as a whole

The five papers form two lineages that meet in VRPO: an alignment lineage (InstructGPT → DPO → VRPO) and an inference lineage (PPI → Xu–Witten–Shojaie). The single most useful thing you can do early is see VRPO through the lens of paper 5, because that tells you exactly what VRPO does and doesn't already cover.

&#91;embedded content: literature map · 5 attached papers + 1 missing sibling\]

Read down each column, then across: PPI's rectifier and paper 5's theory both describe VRPO, though VRPO and paper 5 don't cite each other (VRPO does cite PPI).

### The unifying calculation \[Inference — my derivation, check it\]

Map RLHF onto paper 5's notation. The SSL "covariate" is the triple W = (X, Y⁽¹⁾, Y⁽²⁾); the "label" is Z. With the BT log-loss and Δ\_θ(W) = r\_θ(X, Y⁽²⁾) − r\_θ(X, Y⁽¹⁾), the score is (σ(Δ\_θ) − Z)∇Δ\_θ, so the supervised influence function and its conditional mean (paper 5, Eq. 3) are:

```latex
\varphi(W,Z)=-A^{-1}\big(\sigma(\Delta_{\bar\theta}(W))-Z\big)\nabla\Delta_{\bar\theta}(W),\qquad \phi(W)=\mathbb E[\varphi\mid W]=-A^{-1}\big(\sigma(\Delta_{\bar\theta}(W))-p^*(W)\big)\nabla\Delta_{\bar\theta}(W)
```

Three consequences follow.

1. **Gain exists only under misspecification.** ϕ ≡ 0 exactly when σ(Δ\_θ̄) = p\* wherever ∇Δ ≠ 0, i.e. when BT with that reward class is correct. That is paper 5's Theorem 3.2 and paper 4's Table 1 saying the same thing in different languages.
2. **VRPO is PPI with soft labels.** Differentiating Eq. (3) of paper 4 gives the estimating equation E\_n\[(p\_η − Z)∇Δ\_θ\] + E\_n\[E\_{π\_ref}{(σ(Δ\_θ) − p\_η)∇Δ\_θ | X}\] = 0. That is PPI's convex-minimiser rectifier (paper 3, Table 1, row 6) with the prediction replaced by the soft label p\_η, unit weight, and infinitely many unlabeled pairs per prompt. If p\_η = p\*, the correction equals ϕ exactly, which makes VRPO the efficient estimator for the variation *within* each prompt.
3. **VRPO leaves two things on the table.**
   - It resamples responses only for the *labeled* prompts, so it removes E\[Var(ϕ | X)\] but not Var(E\[ϕ | X\]). Paper 4's H (Supplement 8.2, Step 3) is exactly E\[Var(·| X)\], which is consistent with this reading. Extra unlabeled prompts could capture part of the second piece.
   - With p\_η ≠ p\*, a unit weight is "original PPI", which paper 5 shows is not safe. Paper 5's safe estimator fits the weight instead.

DPO enters this picture only as the base M-estimator with r\_θ = β log(π\_θ/π\_ref), so everything above applies to its implicit reward.

### Who builds on whom \[Paper\]

- DPO builds on InstructGPT's pipeline and objective (DPO Section 3 restates InstructGPT's RM and RL phases).
- VRPO builds on DPO for the one-stage variant (Eq. 5) and on InstructGPT-style PPO for the two-stage one, and cites the semiparametric SSL literature and PPI (Section 2, "Semi-supervised learning").
- Paper 5 builds on PPI, absorbs it as a special case, and proves PPI's variants sub-optimal (Section 5, Appendix C). It does not cite VRPO, and VRPO does not cite it.

### Shared assumptions

| Assumption | Where it appears | Status in practice \[Inference\] |
| --- | --- | --- |
| BT link between reward and preference | InstructGPT Eq. 1; DPO Eq. 1; VRPO's primary model | Questionable: about 73% inter-annotator agreement; VRPO assumes it may fail |
| i.i.d. labeled tuples | All five | Violated by K-wise rankings (InstructGPT Section 3.5) |
| Pairs sampled from a known π\_ref | DPO Section 4; VRPO Section 3 | Only true when you generate the pairs yourself; false for HH as released |
| Auxiliary model independent of the data | PPI; paper 5 Section 5 | VRPO's p\_η is trained on the same data |
| Fixed, low-dimensional parameter | PPI; paper 5; VRPO's theorems | False for LLM policy weights; true for a reward head |
| Same distribution for labeled and unlabeled inputs | PPI main protocol; paper 5 | Plausible if you control sampling; covariate shift is open (paper 5, Section 9) |

### Where they disagree or pull against each other

- **Does unlabeled data help a correct model?** Paper 5 and VRPO say no, asymptotically. DPO's Section 7 and the brief implicitly hope it does. \[Search\] Empirical SSL reward-modelling papers report gains (see Sources). \[Inference\] Those gains must come from finite-sample regularisation, misspecification or shift, not first-order efficiency. Being precise about which is itself a contribution.
- **Validity versus efficiency.** PPI stresses validity for *any* predictor; paper 5 shows the same estimator can be less efficient than ignoring the predictor. Both are true.
- **The reference policy.** DPO treats a mis-matched π\_ref as a mild nuisance (Section 4). VRPO needs it to be right for its correction to be unbiased, and its own TL;DR experiment shows gains shrink when it isn't (Section 5.3).

### Reading order

This order goes from concrete to general and makes VRPO's theory recognisable when you reach it. Hours are rough, for a careful first pass.

1. **Prerequisite refresh (ST460 covers most):** MLE and M-estimation asymptotics, the sandwich covariance A⁻¹BA⁻¹, delta method. Then influence functions and semiparametric efficiency, which ST460 probably won't reach: Tsiatis (2006) Chapters 2–4, or van der Vaart (2000) Chapter 25. About 15 hours.
2. **InstructGPT** — Sections 1, 3, 4.1, 5. Read for the pipeline, not the numbers. About 3 hours.
3. **DPO** — Sections 3–5 and Appendix A. Re-derive Eqs. (4)–(7) by hand. About 6 hours.
4. **PPI** — the main text, then its supplement (Theorem S1, the convex case). About 5 hours. Then PPI++, which isn't attached.
5. **Paper 5** — Sections 1–4, then Section 5 and Appendix C. Skip Appendix E.3 on a first pass; the non-i.i.d. efficiency theory there is the hardest wall in the set. Reproduce the mean-estimation simulation of Section 8.1 in Python. About 20 hours.
6. **VRPO** — all of it. Re-derive Theorem 6.2's H using paper 5's tools, and check my unifying calculation above. About 12 hours.
7. **Positioning** — the doubly robust preference optimisation paper from the same group (NeurIPS 2025; not attached), then the recent related work in Sources.

## Stage 4 — Gaps and candidate research questions

My recommendation is direction A, with B as its first chapter and C as an experimental arm. Together they make a dissertation that is clearly beyond VRPO, has a theorem you can realistically prove, and can be tested cheaply. Everything in this section is **\[Inference\]** unless marked **\[Search\]**; the novelty checks are a one-afternoon search, not a systematic review.

| Rank | Direction | Type | Novelty | Feasibility in about 600 hours |
| --- | --- | --- | --- | --- |
| 1 | A · Prompt-augmented, safe, cross-fitted VRPO | Theory + method + experiments | Medium–high | Good |
| 2 | B · Diagnose before you augment: estimating the achievable gain | Method + empirical | Medium | Very good |
| 3 | C · An external LLM judge as the auxiliary model | Method + empirical | Medium (close prior work) | Good, if API budget exists |
| 4 | D · Choosing which pairs humans label | Theory + method | Medium, crowded field | Fair |
| 5 | E · Does unlabeled data help in the overparameterised regime? | Theory | High | PhD-scale; avoid |

The time budget assumes submission in mid-to-late August 2027, about 8–10 hours a week through term (about 200 hours) and full-time from June (about 350 hours). The hour estimates under each direction are rough.

### A · Prompt-augmented, safe, cross-fitted VRPO (rank 1)

**The question.** How much efficiency can a semi-supervised preference estimator gain when π\_ref is known *and* extra unlabeled prompts are available, and can that gain be had with a guarantee of never doing worse than the labeled-only estimator?

**What's novel.** Three gaps in VRPO, each grounded in Stages 2–3:

1. **A two-level efficiency bound.** Responses come from a known π\_ref; prompts from an unknown distribution, with N extra unlabeled prompts. My conjecture for the bound is Var φ − E\[Var(ϕ | X)\] − γ·Var(E\[ϕ | X\]). It sits between paper 5's ISS and OSS cases and neither paper states it.
2. **Safety.** Replace VRPO's unit weight with an estimated weight — a scalar à la PPI++, or a block-diagonal matrix on a reward head — so the estimator is asymptotically never worse than the base, even with a bad p\_η (paper 5, Theorem 4.3).
3. **Cross-fitting p\_η.** Train p\_η on held-out folds so the theory's "fixed p\_η" assumption actually holds. Because π\_ref is known, I expect consistency of p\_η to be enough for efficiency — no product-rate condition, as in a randomised trial with known propensity.

&#91;Search\] Semi-supervised reward modelling by iterative pseudo-labelling exists (SSRM, 2024) without statistical guarantees. A debiased semi-supervised DPO exists for diffusion models (DeDPO, Feb 2026). A preference-distillation method (DP3O, Sep 2026) cites VRPO and claims variance reduction. None that I found addresses unlabeled prompts, safety or cross-fitting for VRPO-type estimators. Read your supervisor's NeurIPS 2025 doubly robust paper before claiming novelty.

**How to make it tractable.** Make the statistical object a *reward model with a small trainable head on frozen LLM embeddings* (d in the low thousands). The fixed-d theory then really applies, A⁻¹ is computable, and training is cheap. Evaluate downstream with best-of-N sampling against an oracle reward rather than PPO. Run a one-stage DPO version on a 0.5B model only as a bonus.

**Experiments, in order.**

- Synthetic, where p\* is known and BT is deliberately wrong (e.g. intransitive or context-dependent preferences on low-dimensional features). Check that coverage and variance match the bound.
- IMDb with the sentiment-classifier oracle (paper 4's Section 5.1 design), where π\_ref is your own model, so you control the misspecification.
- HH as the realistic case.

**Maths and tools.**

- ST460: M-estimation, the sandwich covariance, asymptotic normality — the core.
- MA411: conditional expectation as L² projection — exactly what ϕ = E\[φ | W\] is; also modes of convergence.
- Self-study: semiparametric efficiency (Tsiatis Chapters 2–4), cross-fitting (Chernozhukov et al. 2018 — close to your econometrics background), and empirical-process basics (van der Vaart Chapter 19) only if a proof needs a Donsker step.
- ST455: the KL-regularised RL framing and PPO, for the policy side.
- Code: PyTorch, Hugging Face TRL, the VRPO repository.

**Feasibility: good.** Roughly 120 hours on theory, 80 on simulations, 150 on LLM experiments and 120 on writing. The main risk is that the between-prompt term Var(E\[ϕ | X\]) is small in real data, making unlabeled prompts add little. A well-measured null result with a proof of why is still a dissertation; direction B is the hedge.

### B · Diagnose before you augment (rank 2)

**The question.** Before spending compute on semi-supervised RLHF, can you estimate from the labeled data how much it could possibly gain — i.e. estimate Var ϕ relative to Var φ — and test whether BT is misspecified enough to matter?

**What's novel.** The gain formula in Stage 3 makes this a calibration question: is the residual Z − σ(Δ\_θ̂(W)) predictable from W? A cross-fitted estimate of that predictability doubles as a goodness-of-fit test for BT and an estimate of the attainable variance reduction. \[Search\] I found statistical surveys flagging misspecification and uncertainty quantification as open in RLHF, but not this specific diagnostic. Confidence: moderate.

**Type.** Methodological and empirical, with light theory (asymptotic validity of the test).

**Tools.** ST460 (score and specification tests), plus classification-calibration ideas. Your econometrics background helps — it is a conditional-moment test.

**Feasibility: very good** as a self-contained chapter. Too thin alone for a "paper" ambition, which is why it sits inside A.

### C · An external LLM judge as the auxiliary model (rank 3)

**The question.** Use a strong external LLM judge's soft preference as p\_η in a safe VRPO/PPI estimator. Because the judge is trained elsewhere, the independence assumption holds for free and no cross-fitting is needed.

**What's novel.** A clean theoretical point most applied work misses: by paper 5's Remark 5.1, even a perfect judge cannot help a *correctly specified* reward model asymptotically; it helps only by giving a better estimate of p\* where BT fails. \[Search\] DeDPO (diffusion models, Feb 2026) already debiases DPO with AI-feedback labels; LLM-judge *evaluation* with PPI and efficient influence functions is well covered (Chen et al., ICML 2026; stratified PPI). Novelty would rest on LLMs, safety and the theory, so it is moderate.

**Feasibility: good,** but API costs scale with the number of unlabeled pairs; a mid-size open judge model on a GPU avoids that. Works best as an experimental arm of A (p\_η = judge versus p\_η = trained model).

### D · Choosing which pairs humans label (rank 4)

**The question.** Given the efficient estimator, which pairs should go to humans? Theory suggests sampling where the conditional residual variance times the gradient norm is largest, then correcting by inverse-probability weighting (the "active statistical inference" idea of Zrnic and Candès, cited by paper 5).

**Novelty and risk.** \[Search\] Active learning for RLHF is crowded: active preference optimisation, an ICML 2026 active preference-data pipeline, optimal-design work, and a 2026 paper on budget-constrained semiparametric learning with human judgments. Your supervisor also has a dual active learning paper (cited in VRPO, Section 2). The combination with semi-supervised efficiency might be new, but proving that would take real reading.

**Tools.** ST409's martingale CLT would matter if labelling is adaptive.

**Feasibility: fair.** Adaptive sampling theory is a step up, and experiments need a simulated labeller.

### E · Unlabeled data in the overparameterised regime (rank 5 — avoid)

All the theory here is fixed-d asymptotics, but the parameters people actually train are billions of LLM weights with singular Hessians. Whether and how unlabeled data help when d is comparable to or exceeds n — proportional asymptotics, kernel or neural-tangent limits — is the deep open question behind the brief. **Verdict:** PhD-scale. Worth one paragraph in your discussion section, not a dissertation.

## Stage 5 — Questions for the first supervisor meeting

Lead with scope; the technical questions about VRPO are best asked as "I tried to re-derive this and got stuck here" rather than as criticisms.

**Scope**

1. VRPO already uses unlabeled π\_ref samples. Is this project meant to extend VRPO, or to take a different route to "semi-supervised RLHF"?
2. Which unlabeled data do you have in mind: fresh response pairs, extra prompts, LLM-judge labels, or something else?
3. Would extending VRPO with unlabeled prompts, a safe (estimated) weight and cross-fitted p\_η count as a sensible core? Is anything like it already underway in the group?
4. How does this sit relative to your doubly robust preference optimisation paper (NeurIPS 2025)? Should I read it before VRPO?

**What "done" looks like**

5. What balance of theory and experiments do you expect for an MSc dissertation? Is one new theorem plus a careful empirical study the right shape?
6. Is a reward model with a small head on frozen embeddings an acceptable main testbed, with one-stage DPO experiments as a bonus?
7. If it might become a paper, what venue and timeline do you have in mind, and who else (e.g. a PhD student) would be involved?

**Resources**

8. What GPU access can I get, and roughly how much? Is there a budget for judge API calls, or should I use an open-weight judge?
9. May I build on the VRPO repository directly?

**Technical (VRPO)**

10. In VRPO's experiments, is p\_η trained on the same labeled data as the primary model? Would sample splitting change the theory or results?
11. In the IMDb experiment where p\_η is DPO's own fitted model, θ̂\_DPO looks like a stationary point of the VRPO loss to me. Where does the gain come from — the 3 versus 1 epochs, or something I'm missing?
12. On HH, π\_ref is an SFT fit to the released responses, not the generating policy. How much does the variance-reduction argument rely on that being accurate?
13. Is Theorem 6.2's H equal to E\[Var(E\_z∇L | W) | X\] — the within-prompt part only? If so, are unlabeled prompts the natural next lever?

**Logistics**

14. How often will we meet, and what should I bring each time?
15. Confirm the ST499 submission date and any interim milestones (proposal, literature review, progress report).
16. Which of the missing references (Sources section) should I prioritise?

## Sources and missing references

The most important missing item is your supervisor's NeurIPS 2025 doubly robust paper; get it before the meeting. Nothing below was used to describe content beyond what the attached papers or the opened pages say.

**Attached (reviewed in Stage 2)**

- [Ouyang et al. 2022, InstructGPT](https://arxiv.org/abs/2203.02155)
- [Rafailov et al. 2023, DPO](https://arxiv.org/abs/2305.18290)
- [Angelopoulos et al. 2023, Prediction-powered inference, Science 382](https://doi.org/10.1126/science.adi6000)
- [Ye, Zhou, Zhu, Quinzan & Shi, Robust RLHF / VRPO](https://arxiv.org/abs/2504.03784)
- [Xu, Witten & Shojaie 2025, Unified semi-supervised efficiency](https://arxiv.org/abs/2502.17741)

**Missing but relied on (identifiers from the attached reference lists)**

- PPI supplementary material — Theorem S1, Algorithms S1–S6, Corollary S13 hold the actual guarantees.
- [PPI++, Angelopoulos, Duchi & Zrnic 2023](https://arxiv.org/abs/2311.01453) — the tuned, "safe" PPI that paper 5 compares against.
- [Xu, Ye, Zhou, Zhu, Quinzan & Shi 2025, Doubly robust alignment for LLMs](https://arxiv.org/abs/2506.01183), [NeurIPS 2025 version](https://proceedings.neurips.cc/paper_files/paper/2025/hash/0a226473989931ec6f6ced7343542f86-Abstract-Conference.html) — same group; from its abstract, it targets consistency when either the preference model or π\_ref is right.
- [Zhang et al. 2024a, General preference modeling](https://arxiv.org/abs/2410.02197) — VRPO's p\_η in Sections 5.2–5.3.
- [Liu, Shi & Sun 2024, Dual active learning for RLHF](https://arxiv.org/abs/2410.02504) — relevant to direction D.
- [Zhu et al. 2025, Semi-pessimistic RL](https://arxiv.org/abs/2505.19002) — semi-supervised RL from the same group.
- [Zrnic & Candès 2024, Active statistical inference](https://arxiv.org/abs/2403.03208).
- [Bai et al. 2022, the Anthropic HH dataset paper](https://arxiv.org/abs/2204.05862).
- Textbooks: Tsiatis (2006) *Semiparametric Theory and Missing Data*; van der Vaart (2000) *Asymptotic Statistics*; Chernozhukov et al. (2018) on double/debiased ML.

**Found in the 15 October 2026 search (for novelty checks)**

- [Semi-supervised reward modeling via iterative self-training (SSRM), 2024](https://arxiv.org/abs/2409.06903)
- [SURF: semi-supervised reward learning for preference-based RL, 2022](https://arxiv.org/abs/2203.10050)
- [DeDPO: debiased DPO for diffusion models, Feb 2026](https://arxiv.org/abs/2602.06195)
- [Preference distillation (DP3O), Sep 2026](https://arxiv.org/abs/2609.06893) — full text not retrievable; described from its search listing only.
- [Semi-DPO: noisy preferences as unlabeled data, 2026](https://arxiv.org/abs/2604.24952)
- [Semiparametric preference optimization (single-index), 2025](https://arxiv.org/abs/2512.21917)
- [Chen et al., Efficient inference for noisy LLM-as-a-judge evaluation, ICML 2026](https://proceedings.mlr.press/v306/chen26cq.html)
- [Stratified prediction-powered inference for LM evaluation, 2024](https://arxiv.org/abs/2406.04291)
- [ActiveUltraFeedback, ICML 2026](https://arxiv.org/abs/2603.09692)
- [Towards optimality in active preference learning, 2026](https://arxiv.org/abs/2602.01581)
- [Labels or preferences? Budget-constrained learning with human judgments, 2026](https://arxiv.org/abs/2601.13458)
- [RLHF: a statistical perspective (survey), 2026](https://arxiv.org/abs/2604.02507)

### Paper 2 · Rafailov et al. (2023), *Direct Preference Optimization* (DPO)

**Problem and contribution \[Paper\].** RLHF needs a separate RM plus unstable on-policy RL. DPO shows that the KL-regularised reward-maximisation problem can be solved with a single classification loss on the policy, so no explicit RM or RL loop is needed (Section 4).

**Setup \[Paper\].**

- Eq. (1): BT model, p\*(y₁ ≻ y₂ | x) = exp r\*(x, y₁) / \[exp r\*(x, y₁) + exp r\*(x, y₂)\].
- Eq. (3): max over π\_θ of E\[r\_φ(x, y)\] − β · D\_KL(π\_θ(· | x) ‖ π\_ref(· | x)).
- Eq. (4): its solution is π\_r(y | x) = π\_ref(y | x) exp(r(x, y)/β) / Z(x); derivation in Appendix A.1.
- Eq. (5): invert to r(x, y) = β log\[π\_r(y | x)/π\_ref(y | x)\] + β log Z(x). Z(x) cancels in the BT difference, giving Eq. (6).
- Eq. (7), the DPO loss: −E log σ(β log\[π\_θ(y\_w | x)/π\_ref(y\_w | x)\] − β log\[π\_θ(y\_l | x)/π\_ref(y\_l | x)\]).

**Assumptions doing the heavy lifting.**

- &#91;Paper\] BT (or Plackett–Luce) is the true preference model. If it isn't, DPO is fitting a misspecified likelihood. Paper 4 is built on this point.
- &#91;Paper\] π\_ref(y | x) > 0 for every response (Appendix A.6), and Eq. (4) is solved over an unrestricted policy class (Appendix A.1).
- &#91;Paper\] The preference pairs are sampled from π\_ref (the "DPO outline", Section 4). When the generating policy is unknown, as with Anthropic HH, they set π\_ref to a model fine-tuned on the preferred completions — an approximation they say mitigates the shift (Section 4; Section 6, "single-turn dialogue").

**Results.**

- Proved \[Paper\]: the closed form, Eq. (4); Lemmas 1–2 (rewards that differ by a function of x give the same preferences and the same optimal policy); Theorem 1 and Proposition 1 (every reward equivalence class has exactly one representative of the form β log π/π\_ref). These are identification results about population optima.
- Not proved: consistency, rates or any finite-sample property of the DPO estimator; they point to Bong and Rinaldo for MLE consistency under BT (Section 4).
- Shown empirically \[Paper\]: on IMDb with a known sentiment reward, DPO's reward–KL frontier dominates PPO, even PPO with the true reward (Figure 2 left, Section 6.1). On TL;DR, about 61% win rate against reference summaries at T = 0 versus PPO's 57% (Section 6.2). On HH it is the only efficient method that beats the chosen responses (Figure 3). Out of distribution on CNN/DailyMail, 0.36 versus PPO's 0.26 (Table 1). GPT-4 agrees with humans about as often as humans agree with each other (Table 2).

**Limitations.**

- &#91;Paper\] Section 7 lists out-of-distribution generalisation, reward over-optimisation, scale (up to 6B only) and judge-prompt sensitivity. Two remarks are directly on-brief: DPO "does not use the additional unlabeled Reddit TL;DR prompts that PPO uses" (Section 6.3), and Section 7 asks whether self-labeling "from the DPO policy" can "make effective use of unlabeled prompts". DPO's own authors flag unlabeled prompts as an open question.
- &#91;Inference\] Theorem 1 says the reparameterisation loses no reward class *when the policy class is unrestricted*. With a finite network π\_θ, the implied reward class {β log π\_θ/π\_ref} is restricted, so DPO can be reward-misspecified even when BT holds. Paper 4 makes this argument in its Section 5.1.
- &#91;Inference\] The loss only constrains log-ratio differences on the observed pairs. It says nothing direct about probability on responses outside the data. That is one reason fresh π\_ref samples — the unlabeled data of paper 4 — might add information.

**Things that look wrong \[Inference\].** Section 5.2 says "π\* is the optimal policy from Eq. 7 induced by the reward function"; the optimal policy is Eq. (4), and Eq. (7) is the loss. Probably a typo.

**Role in the brief: the method to extend.** Paper 4's one-stage variant is a modified DPO loss, and DPO (or its hinge variant) is the baseline you would beat. Read Sections 3–5 and Appendix A closely; Section 6 for the experimental template.

### Paper 3 · Angelopoulos, Bates, Fannjiang, Jordan & Zrnic (2023), *Prediction-powered inference* (Science 382)

**Problem and contribution \[Paper\].** Scientists have a few gold-standard labels and many cheap ML predictions. Imputing predictions as if they were labels gives invalid inference; ignoring them wastes power. PPI combines the two into confidence intervals that are valid for any predictor and narrower when the predictor is good (abstract, Section "Protocol").

**Setup \[Paper\].**

- Labeled data (X₁, Y₁), …, (X\_n, Y\_n); unlabeled features X′₁, …, X′\_N with N typically much larger than n. Both are random samples from the same population. A fixed ML model supplies Ŷ on both sets.
- Estimand θ\*: any minimiser of a convex objective ("General applicability"; Table 1, last row). Means, quantiles and GLM coefficients are special cases.
- Measure of fit m\_θ, computed on the unlabeled set with predictions; rectifier Δ\_θ, the same quantity on labeled data with predictions minus with true labels. Interval C^PP = {θ : |m\_θ + Δ\_θ| ≤ w\_θ(α)} (Table 1 caption).
- For the mean (Table 1, row 1) the point estimate is the mean of Ŷ′ minus the average error (Ŷ − Y) on the labeled set. For a convex loss L\_θ (row 6), m\_θ = (1/N) Σ ∇L\_θ(X′ᵢ, Ŷ′ᵢ) and Δ\_θ = (1/n) Σ \[∇L\_θ(Xᵢ, Ŷᵢ) − ∇L\_θ(Xᵢ, Yᵢ)\].

**Assumptions doing the heavy lifting.**

- &#91;Paper\] Both datasets are sampled from the same population ("Protocol"), or the shift is a known covariate or label shift handled by reweighting ("Inference under distribution shift").
- &#91;Inference, from paper 5\] The predictor must be independent of the data used for inference — trained elsewhere. The main text implies this rather than stating it; paper 5 (Section 5) states it as the PPI setting. The formal condition sits in PPI's supplementary material, which isn't attached.
- &#91;Paper\] Convexity of the objective for the general case.

**Results.**

- Proved \[Paper, but in the missing supplement\]: validity "for any machine-learning algorithm and any underlying data distribution" ("Properties"). The constant w\_θ(α) is in Theorem S1, which I can't see. \[Inference\] The main text says "guaranteed … with probability at least 1 − α"; if w\_θ(α) is a normal quantile, as is standard, the guarantee is asymptotic. Check Theorem S1 before quoting it as finite-sample.
- Shown empirically \[Paper\]: across seven domains the imputed interval never covers the truth, and PPI intervals are narrower than classical ones (Figure 2). Labels needed to reject a null drop by between about 15% and 60% (Table 2; e.g. 316 versus 799 for AlphaFold).

**Limitations.**

- &#91;Paper\] No improvement when predictions are inaccurate or the unlabeled set is not large enough (Conclusions). General, mixed distribution shifts are left open.
- &#91;Inference\] "No improvement" understates it. For the mean, the PPI variance is about Var(Ŷ − Y)/n + Var(Ŷ)/N. If Ŷ were pure noise of variance σ², that is (Var Y + σ²)/n + σ²/N, which is *worse* than classical Var Y / n. Paper 5 (Section 5, point 2) makes the same point: original PPI is not "safe". PPI++ (cited by paper 5, not attached) adds a tuning weight to fix this.
- &#91;Inference\] The guarantees are for low-dimensional θ (a coefficient vector of fixed size). Nothing here speaks to estimating a billion-parameter policy.

**Role in the brief: the conceptual template and a competing approach.** The rectifier is the same algebraic move as paper 4's loss (Stage 3 shows the match). PPI is also the natural tool if your unlabeled data come with LLM-judge labels. Read the main text in an hour; the substance is in the supplement, which you should get.

### Paper 4 · Ye, Zhou, Zhu, Quinzan & Shi, *Robust RLHF for LLM fine-tuning* (VRPO; arXiv 2504.03784 v6, Feb 2026)

**Problem and contribution \[Paper\].** Reward-based RLHF assumes preferences follow Eq. (1), p\*(x, y⁽¹⁾, y⁽²⁾) = σ(r\*(y⁽²⁾, x) − r\*(y⁽¹⁾, x)), and that r\* lies in the model class {r\_θ}. Either can fail (Section 3, "The model"). VRPO adds a more flexible auxiliary preference model p\_η and fresh responses from π\_ref to the loss, to cut the variance of the estimated reward or policy under misspecification (Section 4, Figure 2). The paper explicitly frames this as semi-supervised learning (Section 2, last paragraph).

**Setup \[Paper\].**

- Data (Section 3): prompt X; Y⁽¹⁾, Y⁽²⁾ ∼ π\_ref(· | X); label Z = 1(Y⁽²⁾ ≻ Y⁽¹⁾). Baseline estimator θ̂ minimises L(θ) = E\_n\[ℓ(X, Y⁽¹⁾, Y⁽²⁾, Z; θ)\], e.g. the cross-entropy of Eq. (2).
- The VRPO loss, Eq. (3), averages three terms over the labeled tuples:

```latex
\tilde L(\theta)=\mathbb E_n\Big[\ell(X,Y^{(1)},Y^{(2)},Z;\theta)-\sum_{u\in\{0,1\}}\ell(X,Y^{(1)},Y^{(2)},u;\theta)\,p_\eta(X,Y^{(1)},Y^{(2)},u)+\sum_{u\in\{0,1\}}\mathbb E_{y^{(1)*},y^{(2)*}\sim\pi_{\mathrm{ref}}(\cdot\mid X)}\,\ell(X,y^{(1)*},y^{(2)*},u;\theta)\,p_\eta(X,y^{(1)*},y^{(2)*},u)\Big]
```

- Two-stage: plug θ̃ into PPO with the KL objective, Eq. (4). One-stage: r\_θ = β log(π\_θ/π\_ref) − C(x), Eq. (5), i.e. a modified DPO.
- In practice the inner expectation is a single Monte Carlo pair per prompt, and p\_η is either a BT model (Section 5.1) or the general preference model of Zhang et al. 2024a (Sections 5.2–5.3; not attached).

**Assumptions doing the heavy lifting.**

- &#91;Paper\] π\_ref is known or "well-specified" (Section 3, footnote 2). This is what makes the second and third terms cancel in expectation, so the correction adds no bias.
- &#91;Paper\] p\_η is close to p\*. In Theorem 6.2 the gain term is (1/n)A⁻¹HA⁻¹, but the remainder O(‖p\_η − p\*‖²\_∞ / (nλ²\_min)) is of the same 1/n order. The gain dominates only if ‖p\_η − p\*‖ → 0, which the authors state as a proviso after Theorem 6.2.
- &#91;Paper\] Fixed-dimension M-estimation regularity, Supplement 8.2 (A1)–(A4): compact Θ with θ̄ interior, bounded first and second derivatives, non-singular Hessian A(θ̄).
- &#91;Inference\] The proof treats p\_η as fixed, but Supplement Section 9 says the preference models are trained on "the same dataset". With no sample splitting, p\_η depends on the labeled data, and the cancellation argument no longer holds exactly. This is the standard case for cross-fitting.
- &#91;Inference\] For a billion-parameter policy, d ≫ n and the Hessian is singular, so the O(d^{3/2}/n^{3/2}) remainder is not small and (A3) fails. The theory applies cleanly to a low-dimensional reward model; for the one-stage LLM experiments it is a heuristic.
- &#91;Inference\] On HH, π\_ref is an SFT model fitted to HH responses (Supplement 9.2), not the unknown model that generated them. Table 2 marks π\_ref as correctly specified there; I'd call that an approximation.

**Results.**

- Proved \[Paper\]:
  - Theorem 6.1 (double robustness): in the correctly specified setting, θ̄ minimises E\[L̃(θ)\] if either π\_ref or p\_η is correct.
  - Theorem 6.2: both estimators have bias O(d/(nλ\_min)); the variance difference is the PSD gain term plus the two remainders above, with H in Supplement 8.2, Step 3, and lower bound (6). The gain is zero if π\_ref is deterministic or the model is correct (text after Theorem 6.2; Table 1).
  - Theorem 6.3: the expected suboptimality gap is R(θ̄) + trace(Var(θ)(−∇²J(θ̄))) + O(n^{−3/2}), so lower variance means a smaller gap. It needs (B2): θ̄ also optimises J. Supplement 8.3 writes "minimizer", which I think should be "maximizer". The authors call (B2) restrictive and give a bias-corrected Theorem 3′.
- Shown empirically \[Paper\]:
  - IMDb with a BT-simulated oracle (Section 5.1, Figure 3): VRPO beats DPO on expected reward and on the reward–KL frontier. Varying which of π\_ref and p\_η is correct reproduces the double-robustness pattern.
  - HH (Section 5.2): win rates of 0.53–0.98 against nine baselines across temperatures (Table 3). AlpacaEval 2.0 win rate 93.79% (LC 92.95%) versus 90.93% for Dr. DPO (Table 4).
  - TL;DR with a deliberately mismatched π\_ref (Section 5.3, Figure 4): smaller gains, VRPO over DPO 0.565.
  - Two-stage VR-PPO and VR-GRPO mostly beat their MLE-reward versions (Supplement Tables 7–8).

**Limitations.**

- &#91;Paper\] Gains depend on a well-specified π\_ref (Section 5.3). No gain under correct specification (Table 1).
- &#91;Inference\] No seeds, error bars or number of evaluation prompts are reported for the win-rate tables, and all in-distribution judging is GPT-4o-mini with no human check. In the examples (Supplement Tables 9–12) the judge often rewards VRPO for "more detail", so length bias is a live alternative explanation. The AlpacaEval length-controlled figure partly answers this.
- &#91;Inference\] The HH SFT model was trained on chosen *and* rejected responses (Supplement 9.2), unlike DPO's setup, which may weaken the SFT and DPO baselines. VRPO's HH variant also uses a hinge loss; the DPO-hinge comparison (Table 3, last row) is the authors' ablation for this.

**Things that look wrong or unclear \[Inference — raise these carefully, it's your supervisor's paper\].**

1. **Section 5.1, Result I.** There, p\_η is DPO's own fitted model. For the cross-entropy loss, E\_{u∼p\_θ̂}\[∇ℓ(u; θ̂)\] = 0, so at θ = θ̂\_DPO both correction terms have zero gradient and θ̂\_DPO is a stationary point of L̃. First-order theory therefore predicts *no* gain in that configuration. The observed gain may come from training differences: DPO ran 3 epochs and VRPO 1 (Supplement 9.1). This depends on implementation details I can't see, so ask rather than assert.
2. **Theorem 6.2, Step 2.** The proof says the last two terms "converge to 0 uniformly" when π\_ref is correct. They cancel in *expectation*, but their O(n^{−1/2}) fluctuation is exactly what reduces variance, and Eq. (12) mixes population and sample quantities. The final H agrees with the general formula in paper 5 (Stage 3), so I think the result is right but the derivation loose. Re-deriving it yourself is an ideal first exercise.
3. **Theorem 6.1 proof.** Case 1 invokes the central limit theorem where a law of large numbers is meant.
4. **Theorem 3′.** It concludes |b(θ̃)| ≤ |b(θ̂)| from Var(θ̃) ⪯ Var(θ̂). That needs the trace map to be monotone with a fixed sign, which isn't argued.
5. **Notation.** π\_ref becomes π\_b in the proofs, ℓ and L are used interchangeably, and Table 8's header reads "GRPO vs. VR-GRPO" although the text describes the numbers as VR-GRPO's win rate.

**Role in the brief: the method to extend.** Whatever you do must be positioned against VRPO. Read all of it, proofs included.

### Paper 5 · Xu, Witten & Shojaie (2025), *A unified framework for semiparametrically efficient semi-supervised learning* (arXiv 2502.17741 v2)

**Problem and contribution \[Paper\].** When, and by how much, can unlabeled X's improve inference on a functional θ(P) relative to labeled data alone? The paper derives semi-supervised efficiency bounds for an *arbitrary* regular functional, gives two generic estimators that wrap any supervised estimator, and shows that PPI and its variants are special cases (Sections 1.2, 5).

**Setup \[Paper\].**

- Z = (X, Y), P\* = P\**X · P\**{Y|X}. The model, Eq. (1), lets the two factors vary independently. Labeled L\_n: n i.i.d. draws of Z. Unlabeled U\_N: N i.i.d. draws of X, independent of L\_n. N/(n + N) → γ.
- Three regimes (Section 1.1): supervised; ordinary semi-supervised (OSS, both samples); ideal semi-supervised (ISS, P\*\_X known).
- φ\* is the supervised efficient influence function. The object that drives everything is its conditional mean ϕ\*(x) = E\[φ\*(Z) | X = x\], Eq. (3).

**Results — all proved, with proofs in Appendix B \[Paper\].**

- Theorem 3.1 (ISS): the efficient influence function is φ\* − ϕ\*, and the bound is Var φ\* − Var ϕ\* (Eq. 5). Gain exists if and only if ϕ\* is not almost surely constant.
- Definition 3.1 and Theorem 3.2: θ is *well-specified* if changing P\_X with P\_{Y|X} fixed leaves θ unchanged. Then ϕ\* = 0, and unlabeled data cannot help (Corollaries 3.3, 4.2).
- Theorem 4.1 (OSS): efficient influence function Eq. (24), bound Var φ\* − γ Var ϕ\* (Eq. 25). It interpolates between supervised (γ = 0) and ISS (γ = 1).
- Theorem 4.3, the "safe" estimator (28): regress the estimated influence function on centred features g(X) and subtract. Its variance is never above the supervised one (Eq. 31), whatever g is.
- Theorem 4.4, the "efficient" estimator (34): the same with a growing sieve basis. It attains the bound under Hölder smoothness (Assumption 3.2) with α > dim(X).
- Section 5 and Appendix C: PPI, PPI++ and two other variants all have influence functions of form (76). Their safe-PPI estimator (41) is optimal within that class (Proposition C.1). None is efficient unless the predictor is a linear transform of E\[Y | X\] (Proposition C.2).
- Remark 5.1: an independently trained predictor, however accurate, cannot improve inference on a well-specified parameter.

**Assumptions doing the heavy lifting.**

- &#91;Paper\] Assumption 3.1: the initial estimator is regular and asymptotically linear; its influence functions form a Donsker class, Lipschitz in a nuisance η that you can estimate consistently. Assumption 3.2 (smoothness) only for the efficient estimator.
- &#91;Paper\] Labeled and unlabeled X come from the same distribution; any predictor is independent of the data.
- &#91;Inference\] Fixed p. Like paper 4, this is low-dimensional theory.

**Results shown empirically \[Paper\].** Simulations only (Section 8; Appendix F): two-dimensional X, n = 1,000, 1,000 replications. Safe and efficient estimators track the bounds, coverage is nominal, and nothing beats the supervised estimator in the well-specified settings.

**Limitations.**

- &#91;Paper\] Section 9: the Donsker condition fails for high- or infinite-dimensional nuisances, where they suggest double/debiased ML; covariate shift is open.
- &#91;Inference\] For RLHF the "covariate" is text. α > dim(X) is hopeless on raw text, so the efficient estimator is out of reach except on learned low-dimensional features. The *safe* estimator is the realistic tool.
- &#91;Inference\] "Safe" is asymptotic. Estimating the regression coefficient with d features costs roughly d/n in finite samples, so it can lose a little in small samples.
- &#91;Inference\] RLHF data have a two-level structure — prompts from an unknown distribution, responses from a known π\_ref — that the paper's single "X" does not cover directly. That is an opening (Stage 4, direction A).

**Things that look wrong \[Inference\].**

- Section 4.1: "When γ = 1, there are many more labeled than unlabeled observations". It should be the reverse — γ = N/(n + N) → 1 means unlabeled data dominate.
- Proof of Theorem 4.4: the last bound is labelled ‖IV‖ but concerns term VI.
- Remark 5.1 makes a claim about the simulations in PPI++ (Angelopoulos, Duchi & Zrnic 2023b), which isn't attached, so I can't check it.

**Role in the brief: the theoretical backbone.** It tells you exactly when semi-supervised RLHF can gain (misspecification), by how much (Var ϕ\*), and how to get a guarantee of no loss (the safe estimator). Read Sections 1–5 and Appendix C closely; Sections 6–7 as examples.
