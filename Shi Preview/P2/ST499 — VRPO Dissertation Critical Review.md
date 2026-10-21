# ST499 — VRPO Dissertation: Critical Review

Oct 15, 2026 · @Alex

## How to read this review

The open problem, in one line: VRPO's variance-reduction guarantee covers an idealised estimator that is never actually run. Making the real estimator efficient and cheap, then using it where the response-generating policy is unknown (UltraFeedback), is the dissertation.

Every claim carries a label:

- **\[Paper\]**: what a paper states, with its section, equation or theorem number.
- **\[Inference\]**: my own reasoning or reading. Check it before relying on it.
- **\[Outside\]**: from the wider literature, not the attached papers. Sources are linked where I opened them; otherwise the claim comes from my own knowledge, so treat it as approximate.

You left some placeholders blank, so I assumed the following. Correct me where wrong, because the Stage 4 feasibility verdicts depend on them:

- **Supervisor:** Chengchun Shi, VRPO's corresponding author.
- **Deadline:** late summer 2027, the usual MSc timetable.
- **Time:** about 10 hours a week in term, near full-time over the summer.
- **Winter Term:** ST451 (Bayesian ML), ST455 (Reinforcement Learning) and ST418 (your time-series option).

**References the brief relies on but you didn't attach.** I haven't guessed at what they contain beyond what the attached papers say. Anything I add about them is labelled \[Outside\].

| Reference | Why you need it |
| --- | --- |
| Cui et al. (2023), UltraFeedback | The brief's target dataset. How its responses were generated decides whether VRPO applies as written (Stage 4). |
| Zhang et al. (2024a), general preference models (GPM) | VRPO's auxiliary model p\_η on HH and TL;DR (VRPO §5, Supp. §9). |
| Angelopoulos et al. (2023), prediction-powered inference; Zhang, Brown & Cai (2019) | The semi-supervised template that VRPO's loss, eq. (3), adapts (VRPO §2). |
| Azar et al. (2024), IPO | The standard critique of DPO under the Bradley–Terry (BT) model. |
| Xu et al. (2025), Doubly Robust Alignment | Same group, the closest neighbouring work. Check how much it overlaps with your project. |

## Stage 1 — The brief

The brief asks for three things: make VRPO cheaper, make it statistically sharper, and show it working on UltraFeedback. Success is a method plus evidence strong enough to grow into a conference or journal paper.

**The question, in my words.** Most RLHF methods fit a Bradley–Terry (BT) reward model, which is probably misspecified. VRPO (Ye et al.) keeps that BT-based primary model. It adds two things: an auxiliary preference model p\_η, and extra responses sampled from the reference policy π\_ref. Together these reduce the variance of the fitted parameter without moving its target. The brief wants VRPO improved computationally and statistically, then scaled to UltraFeedback, which is a larger and harder dataset. It calls the project coding-intensive and aims for a paper.

**What a successful dissertation delivers** \[Inference\]:

1. **A modified VRPO estimator with one clear claim:** lower variance at the same compute, or the same variance at lower compute.
2. **Theory for that claim** at the level of VRPO §6, covering asymptotic variance and suboptimality. It should be honest about the regime it covers.
3. **Controlled experiments where the truth is known**, such as IMDb with synthetic BT labels. These should measure variance directly, not only win rates.
4. **An UltraFeedback experiment** against DPO and VRPO, on the benchmarks that literature uses: AlpacaEval 2, Arena-Hard and MT-Bench \[Outside, [SimPO](https://arxiv.org/html/2405.14734v2)\].
5. **Reproducible code** built on VRPO's TRL-based repository ([VRPO/VRPO](https://github.com/VRPO/VRPO)).

**Ambiguities to settle with your supervisor**

| # | What's unclear | Why it matters |
| --- | --- | --- |
| 1 | "Computational efficiency" of which cost? VRPO pays to train p\_η, to generate extra response pairs, and to run extra forward and backward passes per step. | Each cost has a different fix. Some fixes are engineering, others are research. |
| 2 | "Statistical efficiency" against which benchmark: DPO, current VRPO, or a semiparametric efficiency bound? | This decides whether the theory compares variances or proves optimality. Optimality is much harder. |
| 3 | Which version of UltraFeedback? The original draws 4 responses per prompt from 4 of 17 models, rated by GPT-4 ([OpenBMB](https://github.com/OpenBMB/UltraFeedback)). Binarised versions keep the top-rated response. On-policy versions regenerate responses from the SFT model and label them with a reward model ([SimPO](https://arxiv.org/html/2405.14734v2)). | VRPO needs the response-generating policy to be known. Only the on-policy version makes it known. Even that version picks pairs using their labels, which breaks VRPO's unbiasedness (Stage 4). |
| 4 | Model scale and compute. The UltraFeedback literature uses 7–8B models \[Outside\]. | Is a 0.5–1.5B model with LoRA acceptable? Which GPUs can you use, and for how long? |
| 5 | Evaluation budget. AlpacaEval 2 and Arena-Hard use paid GPT-4-class judges. | Who pays, and how many evaluation runs are affordable? |
| 6 | What "the paper" means. Is your work a section of a group paper or standalone? How much does it overlap with Xu et al. (2025) and the group's ongoing work? | It sets what novelty you need and what you can claim as your own. |
| 7 | The topic you picked from Shi's list was "Semi-supervised RLHF for LLM fine-tuning". The list had it as a separate project from VRPO. | Confirm which brief is yours, or whether he has merged the two. |

## Stage 2a — InstructGPT (Ouyang et al., 2022)

InstructGPT is foundational: it defines the two-stage RLHF pipeline that both DPO and VRPO formalise. It proves nothing. Its value to you is the pipeline, the reward-model loss, and evidence that real preference labels are noisy.

**Problem and contribution** \[Paper\]. Next-token prediction is "misaligned" with following user instructions (§1). The paper scales a three-step pipeline to GPT-3: supervised fine-tuning (SFT), then a reward model (RM), then PPO (§3.1, Fig. 2). Its 1.3B InstructGPT is preferred to the 175B GPT-3 (Fig. 1, §4.1). PPO-ptx mixes pretraining gradients into PPO to cut the "alignment tax" on public NLP benchmarks (eq. 2, §4.2).

**Setup** \[Paper\]

- **Data:** about 13k SFT prompts, 33k RM prompts and 31k PPO prompts (Table 6), from about 40 contractors (§3.4). RM labellers rank K = 4–9 responses per prompt.
- **RM loss, eq. (1):** loss(θ) = −(1/C(K,2)) E log σ(r\_θ(x, y\_w) − r\_θ(x, y\_l)). All C(K,2) pairs from one prompt form a single batch element, to avoid overfitting (§3.5, footnote 5). Rewards are shifted so that demonstrations average 0.
- **RL objective, eq. (2):** E\[r\_θ(x, y) − β log(π^RL(y|x) / π^SFT(y|x))\] + γ E\_pretrain\[log π^RL(x)\], with β = 0.02 and γ = 27.8 (App. C.4). One 6B RM serves policies of every size (App. C.2).

**Assumptions doing the heavy lifting** \[Inference about which ones matter\]

1. **Pairwise logistic (BT) form of eq. (1).** Preference depends only on a reward difference. It is never tested; it simply defines the RM. This is the assumption VRPO later treats as possibly misspecified.
2. **The RM is only trusted near π^SFT.** That is why the KL penalty β exists. Over-optimisation still shows: Likert scores peak at β ≈ 0.01–0.02 and fall on either side (Fig. 36).
3. **Responses come from a mixture of policies.** "Most" comparison data comes from SFT policies and "some" from PPO policies (§3.1). No single known π\_ref generates the RM data, which is exactly what VRPO needs.
4. **The labellers' preferences are the target** (§5.2).

**Results: proved vs shown** \[Paper\]. Nothing is proved; every result is empirical:

- Human preference win rates (Figs. 1, 3) and quality metadata (Fig. 4).
- TruthfulQA (Fig. 6), toxicity (Fig. 7) and bias (Fig. 32).
- Regressions on public NLP datasets (Figs. 28–29).
- Inter-annotator agreement of 72.6 ± 1.5% for training labellers and 77.3 ± 1.3% for held-out ones (§3.4).
- RM accuracy on held-out labellers of 69.6%, against 72.4% on training labellers (§4.1).

**Limitations the authors state** \[Paper\]

- Labellers are unrepresentative, and most comparisons have a single labeller (§5.3).
- The alignment tax is reduced but not removed (§4.2, App. E.6).
- The model follows harmful instructions (Fig. 44), over-hedges and accepts false premises (Fig. 9).

**Limitations I see** \[Inference\]

- **Systematic disagreement, not just noise.** About 73% agreement means roughly a quarter of comparisons split two trained raters. A single-reward BT model can absorb random noise but not systematic disagreement between labellers. That is direct evidence for VRPO's misspecification premise.
- **Training variance is never measured.** Error bars come from resampling evaluation prompts, not from retraining. The variance of the trained policy, which is what VRPO targets, goes unmeasured.
- **No diagnostic for misspecification.** RM accuracy tops out near 70%, and nothing separates label noise from model misspecification.

**Things that look wrong** \[Inference; check against the PDF\]

- **App. E.2 swaps inter and intra.** It calls 72.4% the "inter-group" accuracy and 69.6% the "intra-group" one. §4.1 says the reverse, and §4.1's reading is the coherent one.
- **Table 14 has a copy error.** The CNN/DM and TL;DR ROUGE-L rows match to every digit.
- **Training and evaluation targets differ by design.** Training labels put helpfulness first; final evaluations put truthfulness and harmlessness first (§3.4, App. B.2).

**Role in the brief: foundational.** Read §3.1, §3.5, eqs. (1)–(2) and §5.2–5.3 closely, and skim the rest.

## Stage 2b — DPO (Rafailov et al., 2023)

DPO is the algorithm VRPO wraps in its one-stage mode; VRPO's code "parallels the training pipeline of DPO" (VRPO §5). Its key result is algebra, a closed-form optimal policy, and it says nothing about variance. That gap is VRPO's entry point.

**Problem and contribution** \[Paper\]. RLHF with PPO is complex, expensive and unstable (§1). DPO solves the KL-regularised objective, eq. (3), in closed form, eq. (4). Inverting that gives the reward in terms of the policy, eq. (5). Substituting into BT cancels the partition function Z(x), eq. (6). The result is a binary classification loss on the policy, eq. (7), with no reward model and no RL loop.

**Setup** \[Paper\]. The data are D = {(x, y\_w, y\_l)}. The model is BT, eq. (1): p\*(y₁ ≻ y₂ | x) = σ(r\*(x, y₁) − r\*(x, y₂)). The chain is:

```latex
\pi_r(y\mid x)=\frac{1}{Z(x)}\,\pi_{\mathrm{ref}}(y\mid x)\exp\!\Big(\tfrac{1}{\beta}r(x,y)\Big)\quad\text{(4)}\qquad r(x,y)=\beta\log\frac{\pi_r(y\mid x)}{\pi_{\mathrm{ref}}(y\mid x)}+\beta\log Z(x)\quad\text{(5)}
```

```latex
\mathcal{L}_{\mathrm{DPO}}(\pi_\theta;\pi_{\mathrm{ref}})=-\,\mathbb{E}_{(x,y_w,y_l)\sim\mathcal{D}}\Big[\log\sigma\Big(\beta\log\frac{\pi_\theta(y_w\mid x)}{\pi_{\mathrm{ref}}(y_w\mid x)}-\beta\log\frac{\pi_\theta(y_l\mid x)}{\pi_{\mathrm{ref}}(y_l\mid x)}\Big)\Big]\quad\text{(7)}
```

**Assumptions doing the heavy lifting**

1. **BT (or Plackett–Luce) is the true preference model** (eq. 1). Z(x) cancels only because BT depends on reward differences (eq. 6, App. A.2). Under non-BT preferences DPO still runs, but it targets a different object. VRPO starts from exactly this point. \[Paper + Inference\]
2. **The policy class is nonparametric.** Eq. (4) is derived over "a general non-parametric policy class" (App. A.1), and Theorem 1 needs π to range over every distribution (App. A.6). With a finite network the DPO minimiser need not equal the PPO solution, so "same objective" holds only in that limit. \[Inference\]
3. **π\_ref(y | x) > 0 for every y** (Theorem 1 restated, App. A.6). \[Paper\]
4. **Pairs are drawn from π\_ref.** Step 1 of the DPO outline says so (§4). When no SFT model exists, π\_ref is fitted by maximising the likelihood of the chosen responses, "to mitigate the distribution shift" (§4). In other words, π\_ref doubles as an estimated behaviour policy, which is the object VRPO needs to know. \[Paper + Inference\]

**Results: proved vs shown**

- **Proved** \[Paper\]: the optimum, eq. (4) (App. A.1, via Gibbs' inequality); Lemmas 1–2 (§5.1, App. A.5); Theorem 1 and Proposition 1, on representability and uniqueness (App. A.6); the gradient (§4, App. A.4); the Plackett–Luce extension (App. A.3).
- **Argued, not proved** \[Inference\]: the PPO instability story in §5.2 is a heuristic based on control-as-inference, with no theorem. The paper proves no consistency, rates or variance results of its own; it cites Bong & Rinaldo for consistency (§4).
- **Shown empirically** \[Paper\]:
  - On the IMDb reward–KL frontier, DPO dominates PPO, even PPO with the true reward (Fig. 2 left, §6.1).
  - On TL;DR, DPO wins about 61% against reference summaries, versus 57% for PPO (Fig. 2 right).
  - On HH, DPO is the only method that beats the chosen responses (Fig. 3).
  - Out of distribution on CNN/DM, DPO scores 36% versus 26% for PPO (Table 1).
  - Humans agree with the GPT-4 judge about as often as with each other (Table 2, §6.4).

**Limitations the authors state** \[Paper\]. Models go up to 6B. Out-of-distribution generalisation and over-optimisation are open. GPT-4 win rates depend on the judge prompt (§7).

**Limitations I see**

- **Deterministic preferences break the KL constraint** \[Outside: Azar et al. 2024, cited in VRPO §2\]. If one response always wins, the BT maximum-likelihood estimate wants an infinite reward gap. DPO then pushes the log-ratio gap to infinity and the KL term stops binding. This matters for you because labels built from score comparisons, as in UltraFeedback, are deterministic.
- **Weak baselines on HH.** PPO on HH could not beat the base Pythia-2.8B, so Best-of-128 stands in as a "rough proxy" for PPO (§6.2). β is barely tuned: 0.1, or 0.5 on TL;DR (App. B). \[Paper\]
- **No training-seed variability.** The plots don't say whether they average over training seeds. The error bars look like evaluation resampling. \[Inference; check the PDF\]

**Things that look wrong** \[Inference\]

- **Wrong equation reference.** §5.2 says "π\* is the optimal policy from Eq. 7"; it should be Eq. 4.
- **Swapped order in App. A.4.** Eq. (21) puts y\_l before y\_w inside log σ, the reverse of eq. (7). The final gradient comes out right only with eq. (7)'s order, so this is a typo.
- **A label error in the HH test set.** In Table 10 the "ground truth" answer to "what is 7 plus 2" is "11", and GPT-4 sided with it. This is concrete HH label noise, which VRPO's misspecification argument relies on (VRPO §5.2).
- **Different label designs on IMDb.** DPO labels IMDb pairs deterministically by classifier score (§6, App. C.1). VRPO deliberately samples them from BT instead (VRPO Supp. §9.1). Keep this in mind when comparing the two papers' IMDb numbers.

**Role in the brief: the method VRPO extends** (one-stage variant). Read §3–5 and App. A.1, A.2, A.4 and A.5–A.6 closely, then skim §6.

## Stage 2c — VRPO (Ye, Zhou, Zhu, Quinzan & Shi, arXiv 2504.03784v6)

VRPO is the method you will extend. Its theory proves a variance reduction for an idealised estimator, one with infinitely many extra response pairs per prompt. **\[Inference\]** The implementation appears to use one pair per prompt. In that case, with a good auxiliary model, the theory predicts no reduction at all. That gap is the most useful thing in this review for you.

### Problem and contribution \[Paper\]

BT-based RLHF can be misspecified in two ways (§3):

- **The preference model is wrong.** p\* is not σ of a reward difference, for example because preferences are intransitive or context-dependent (§1).
- **The reward model is wrong.** r\* lies outside the parametric family r\_θ.

VRPO keeps the simple primary model p\_θ and adds two ingredients:

- **An auxiliary, more flexible preference model p\_η**, trained beforehand. This is a GPM on HH and TL;DR, and BT on IMDb (§4–5).
- **Fresh response pairs from π\_ref.** They enter a corrected loss, eq. (3), that keeps the target and cuts variance (§4, Fig. 2).

The recipe plugs into two-stage RLHF (fit a reward, then PPO or GRPO via eq. 4) or one-stage DPO-style training (eq. 5).

### Setup \[Paper\]

- **Data:** n tuples (X, Y⁽¹⁾, Y⁽²⁾, Z), with Y⁽¹⁾, Y⁽²⁾ \~ π\_ref(· | X) and Z = 𝕀(Y⁽²⁾ ≻ Y⁽¹⁾) (§3).
- **Preference function:** p\*(x, y⁽¹⁾, y⁽²⁾) = P(Y⁽²⁾ ≻ Y⁽¹⁾ | X).
- **Reward-based condition, eq. (1):** p\* = σ(r\*(y⁽²⁾, x) − r\*(y⁽¹⁾, x)).
- **Baseline loss:** the cross-entropy ℓ of eq. (2), minimised as L(θ) = E\_n ℓ.
- **VRPO loss**, with u ranging over {0, 1}:

```latex
\tilde{\mathcal L}(\theta)=\mathbb E_n\Big[\ell(X,Y^{(1)},Y^{(2)},Z;\theta)-\sum_{u}\ell(X,Y^{(1)},Y^{(2)},u;\theta)\,p_\eta(X,Y^{(1)},Y^{(2)},u)+\sum_{u}\mathbb E_{y^{*}\sim\pi_{\mathrm{ref}}(\cdot\mid X)}\,\ell(X,y^{(1)*},y^{(2)*},u;\theta)\,p_\eta(X,y^{(1)*},y^{(2)*},u)\Big]\quad(3)
```

- **Targets:** in the misspecified case the target is θ̄ = argmin\_θ E\[L(θ)\] (§6). Under misspecification θ̄ depends on the distribution of the pairs. That is why the extra pairs must come from the same π\_ref. \[Inference\]
- **Stated regularity conditions:**
  - (A1) θ̄ is an interior point of a compact Θ ⊂ ℝ^d.
  - (A2) First and second derivatives are bounded by M.
  - (A3) A(θ̄) is non-singular, with eigenvalues λ\_min and λ\_max.
  - (A4) Derivatives and expectations commute.
  - (B1)–(B2) for Theorem 6.3 (Supp. §8.2–8.3).

**Assumptions doing the heavy lifting** \[Inference about which ones matter\]

1. **π\_ref is known and generated the observed pairs.** This is the only reason the second and third terms of eq. (3) cancel in expectation, whatever p\_η is. Theorems 6.2–6.3 assume it outright ("we focus on settings with a known π\_ref", §6.1).
2. **The expectation over y* is exact.*\* The proof of Theorem 6.2 writes it as E\_{z,y} in eq. (12) (Supp. §8.2). That is, it assumes infinitely many fresh pairs. Practice uses Monte Carlo (§5, "sampling a pair of responses").
3. **p\_η is fixed and close to p*.*\* The proofs treat p\_η as non-random. In fact it is trained on the same dataset (Supp. §9). The variance reduction dominates only if ‖p\_η − p\*‖\_∞ → 0 (discussion after Theorem 6.2).
4. **Fixed dimension d.** The bounds scale as d/(nλ\_min) and d^{3/2}/(n^{3/2}λ\_min²). With d ≈ 1.5×10⁹ parameters and n ≈ 1.6×10⁵ HH pairs, they say nothing quantitative about the experiments. This is standard for the genre, but you should say it.

### Results: proved vs shown

**Proved** \[Paper\]

- **Theorem 6.1 (double robustness).** In the *correctly specified* setting, θ̄ minimises E\[L̃\] when either π\_ref or p\_η is correct.
- **Theorem 6.2 (variance and MSE).** Both estimators have bias of order d/(nλ\_min). Var(θ̂) − Var(θ̃) = (1/n)A⁻¹HA⁻¹ + O(d^{3/2}/(n^{3/2}λ\_min²)) + O(‖p\_η − p\*‖\_∞²/(nλ\_min²)). H is positive semi-definite, and eq. (6) gives a lower bound on its smallest eigenvalue.
- **Theorem 6.3 (suboptimality).** E R(θ) = R(θ̄) + tr(Var(θ)(−∇²J(θ̄))) + O(n^{−3/2}). So lower variance means a smaller suboptimality gap.
- **Where the reduction vanishes** (stated after Theorem 6.2 and in Table 1). Under correct specification E\_z∇L = 0 pair by pair, so H = 0 and there is no reduction.

**Shown empirically** \[Paper\]

- **IMDb (Qwen2-0.5B, BT labels sampled from a sentiment classifier):** a better reward–KL frontier than DPO, and an empirical double-robustness pattern (Fig. 3, Supp. §9.1).
- **HH (Qwen2.5-1.5B):**
  - VRPO beats 9 baselines with win rates of 0.53–0.98, and beats DPO with 0.78–0.81 (Table 3).
  - It is best on AlpacaEval 2: 93.79% win rate (92.95% length-controlled) against Dr. DPO's 90.93% (92.16%) (Table 4).
- **TL;DR (Pythia-1B, misspecified π\_ref):** VRPO beats DPO with 0.565 (Fig. 4).
- **Two-stage variants:** VR-PPO and VR-GRPO mostly beat PPO and GRPO (Tables 7–8).

### The main gap: one Monte Carlo pair gives no reduction \[Inference\]

Write g = ∇\_θℓ at θ̄. Let m\*(x, y) = E\[g | x, y\] = Σ\_u g(u) p\*(u), and let m\_η be the same sum with p\_η. With M fresh pairs per prompt, the per-example VRPO gradient is ψ = g − m\_η(Y) + M⁻¹ Σ\_j m\_η(Y\*\_j). The fresh pairs are independent of (Y, Z) given X, so:

```latex
\operatorname{Var}(\psi\mid X)=\mathbb E[\operatorname{Var}(g\mid X,Y)]+\operatorname{Var}_Y(m^*-m_\eta)+\tfrac{1}{M}\operatorname{Var}_Y(m_\eta)\quad\text{vs. baseline}\quad \operatorname{Var}(g\mid X)=\mathbb E[\operatorname{Var}(g\mid X,Y)]+\operatorname{Var}_Y(m^*)
```

- **With a perfect auxiliary model (p\_η = p*),*\* the reduction is Var\_Y(m\*)(1 − 1/M). With M = 1 it is exactly zero. Theorem 6.2's H equals E\[Var\_Y(m\*)\], which corresponds to M = ∞.
- **With an imperfect p\_η and M = 1,** VRPO beats the baseline only if Var(m\_η) < Cov(m\*, m\_η). In words, p\_η must be *shrunk* relative to the truth, so its calibration matters.
- **This is the PPI picture with N = n.** In prediction-powered inference, the gain comes from having many more unlabelled than labelled points ([PPI++](https://arxiv.org/abs/2311.01453v2)). \[Outside\]
- **The implementation appears to use M = 1.** The repository's data format stores one extra pair (`a_1`, `a_2`) per example, with precomputed preference scores ([VRPO/VRPO README](https://github.com/VRPO/VRPO)). That looks like M = 1, generated offline. I couldn't open `trainer/` (GitHub blocks automated fetching), so confirm this in the code.

If M = 1, the 0.78–0.81 wins over DPO (Table 3) need another explanation. The third term on its own is DPO with GPM soft labels on fresh SFT samples. That is *distillation of a stronger preference model*, which adds information rather than reducing variance. Testing this comes first (Stage 4, direction B). Raise it carefully: the authors may well know and handle this, and I may be misreading the setup.

### Other limitations \[Inference unless marked\]

- **Robustness only covers the primary model.** The specification-error term in Theorem 6.2 has the same 1/n order as the gain. It is negligible only if p\_η is asymptotically correct, so "regardless of whether the model is correctly specified" means the *primary* model. The auxiliary model must still be right.
- **The two theorems live in different regimes.** Double robustness (Theorem 6.1) is proved under correct specification, where H = 0 and there is no gain. Under misspecification, where the gain lives, only the "π\_ref correct" arm survives.
- **The data reuse goes unanalysed.** p\_η is trained on the same D with no cross-fitting (Supp. §9). The resulting dependence is not covered.
- **π\_ref plays two roles.** In the main text π\_ref is both the KL anchor and the data generator. The proofs switch to π\_b (Supp. §8.1). On HH, π\_ref is an SFT model *fitted* to responses from Anthropic's models, so it is an estimated behaviour policy. Table 2 still marks it ✓, but the theory assumes it is known.
- **The experiments aren't matched.**
  - VRPO gets an extra GPM and extra samples; the baselines don't.
  - No method was hyperparameter-tuned (Supp. §9).
  - On IMDb, DPO trains for 3 epochs and VRPO for 1, with different β (Supp. §9.1).
  - There are no training-seed replicates or confidence intervals in Tables 3–4.
  - The "misspecified p\_η" is adversarial, 1 − p\_true (Supp. §9.1), not a realistic imperfect model.

### Things that look wrong or unclear \[Inference; check each against the PDF\]

- **The sign of A is inconsistent.** A(θ̄) := −E∇²L is defined for a *loss*, so it is negative semi-definite. Yet (A3) treats its eigenvalues as positive. The convention looks borrowed from likelihood maximisation (A3, eq. 10).
- **Argmax and argmin are swapped twice.** Eq. (9) writes argmax where it should be argmin. (B2) calls θ̄ the *minimiser* of J, while the proof treats it as the maximiser.
- **(B2) is very strong.** Under misspecification the loss minimiser need not maximise J, and the authors concede this.
- **Theorem 3′ looks garbled.** Var(θ̃) ≼ Var(θ̂) does not by itself give |b(θ̃)| ≤ |b(θ̂)|. That needs sign conditions on the multiplying matrices. Also, the second-order bias should involve third derivatives, but here a matrix inverse multiplies a scalar trace. Don't rely on Theorem 3′.
- **CLT where LLN is meant.** The proof of Theorem 6.1 cites the central limit theorem where it needs the law of large numbers.
- **Table 8's row label is ambiguous.** It reads "GRPO vs. VR-GRPO", but the text reports these numbers as VR-GRPO's win rate.

### Role in the brief: the method to extend

Read all of it, including the Supplement's proofs, with a pencil.

## Stage 3 — The literature as a whole

The three papers are a single line of descent:

- **InstructGPT** defines the KL-regularised objective.
- **DPO** solves it in closed form.
- **VRPO** makes the resulting estimator robust and lower-variance.

All three use BT and a KL anchor π\_ref. Their real disagreement is whether BT is the truth or an approximation.

|  | InstructGPT | DPO | VRPO |
| --- | --- | --- | --- |
| Status of BT | The RM's definition (eq. 1) | Assumed true; it makes Z(x) cancel (eq. 6) | Possibly wrong; the target is the best approximation θ̄ (§6) |
| Objective | Eq. 2: reward − β·per-token KL + γ·pretraining | Eq. 3: reward − β·KL | Two-stage, eq. 4; one-stage, eq. 5 inside eq. 3 |
| What π\_ref does | KL anchor (the SFT model). The data come from a mix of SFT and PPO policies (§3.1) | KL anchor and assumed data generator (§4) | KL anchor and the *known* data generator the correction needs |
| Statistical results | None | None; consistency is cited, not proved | Variance, MSE and suboptimality (Theorems 6.1–6.3) |
| Evaluation | Human labellers | GPT-4 judge, validated by a human study | GPT-4o-mini judge and AlpacaEval 2 |

**Who builds on whom** \[Paper\]. DPO's eq. (3) is InstructGPT's eq. (2) with γ = 0 and the KL taken over the whole sequence. VRPO's one-stage variant reuses DPO's reparameterisation (VRPO eq. 5). Its two-stage variant is InstructGPT-style RLHF (VRPO eq. 4).

**Where they disagree** \[Paper + Inference\]

- **Are DPO and PPO the same thing?** DPO says they optimise "the same objective" (§1, §6.1). VRPO §5.1 argues that DPO's implicit reward is *itself* misspecified once the policy class is finite. That is consistent with the nonparametric caveat I flagged in Stage 2b.
- **Is PPO usable?** DPO presents PPO as unstable (§5.2). VRPO uses PPO and GRPO happily in its two-stage variant (Supp. §10.2).

**Notation traps** \[Inference\]

- **Direction of preference.** DPO writes p\*(y₁ ≻ y₂) = σ(r(y₁) − r(y₂)). VRPO writes Z = 𝕀(Y⁽²⁾ ≻ Y⁽¹⁾) with σ(r(y⁽²⁾) − r(y⁽¹⁾)).
- **Argument order.** VRPO writes r(y, x) in eq. (1) but r(x, y) in eqs. (4)–(5).
- **β is not comparable across papers.** InstructGPT uses a per-token β = 0.02; DPO uses a sequence-level β = 0.1.
- **The policy symbols differ.** π^SFT, π\_ref and π\_b all appear. Keep the KL anchor and the behaviour (data-generating) policy as separate symbols in your own write-up, because UltraFeedback forces them apart.

### Reading order

The wall is VRPO's Supplement §8. Get there with M-estimation and control variates already in hand.

1. **M-estimation under misspecification.** Pseudo-true value θ̄, sandwich variance A⁻¹BA⁻¹ (White, 1982). You know this from econometrics and ST460 covers it \[Outside\]. Half a day.
2. **InstructGPT** §1, §3.1, §3.5 and §5.2–5.3. Two hours.
3. **DPO** §3–4. Then derive eq. (4) yourself before reading App. A.1. Then App. A.2, A.4 and §5.1, and skim §6.
4. **Control variates and prediction-powered inference.** [PPI++](https://arxiv.org/abs/2311.01453v2) §2, plus Angelopoulos et al. (2023) \[Outside\]. Work the mean-estimation case by hand; it is VRPO's eq. (3) in one dimension.
5. **VRPO §3–4** with eq. (3) beside you. Re-derive the Stage 2c variance decomposition yourself, then read §6.
6. **VRPO Supp. §8.** Rewrite the proofs in your own notation, fixing the sign of A and settling π\_b against π\_ref.
7. **VRPO §5 and Supp. §9–10** alongside the [repository](https://github.com/VRPO/VRPO). Find exactly how many extra pairs are used.
8. **Zhang et al. (2024a), GPM.** The auxiliary model.
9. **UltraFeedback** ([OpenBMB](https://github.com/OpenBMB/UltraFeedback)) and **SimPO's experimental setup** ([SimPO](https://arxiv.org/html/2405.14734v2)). The dataset and the on-policy protocol.
10. **Azar et al. (2024), IPO.** DPO under deterministic preferences.
11. **Optional:** Tsiatis (2006) on semiparametric efficiency and augmented inverse-probability weighting (AIPW), only if you choose direction E. Also Xu et al. (2025), to check for overlap.

## Stage 4 — Gaps and candidate research questions

My recommendation: build the dissertation on direction A, an optimally weighted, multi-sample VRPO with a "never worse than DPO" guarantee. Start with the cheap mechanism test B, and finish with UltraFeedback (D). Together they cover all three asks in the brief. Every direction below is my own proposal \[Inference\]; check its novelty against Xu et al. (2025) and the group's current work.

| Rank | Direction | Type | What's new | Feasibility in your time |
| --- | --- | --- | --- | --- |
| 1 | A. Weighted, multi-sample VRPO | Theory and method | VRPO implicitly uses λ = 1 and M = 1; optimising both gives a guaranteed gain | High. This is the core chapter. |
| 2 | D. UltraFeedback with an exchangeable-pair design | Method and empirics | Applies VRPO without knowing the behaviour policy | Moderate. Compute is the risk. |
| 3 | B. Variance reduction or distillation? | Empirics | Establishes what actually drives VRPO's gains | High. A few weeks. |
| 4 | C. Compute-aware VRPO | Method | Measures variance reduction per unit of compute | High, best folded into A |
| 5 | E. Estimated behaviour policy | Theory | Shows how the target shifts when π\_ref is estimated | Low as a full theory; one lemma is feasible |

### A. Optimally weighted, multi-sample VRPO — rank 1

**The question.** VRPO's correction carries an implicit weight λ = 1 and uses one fresh pair, M = 1. What λ and M minimise variance, and can a data-driven λ̂ guarantee you never do worse than DPO?

**The idea.** Put λ on both correction terms of eq. (3) and average over M fresh pairs. Unbiasedness holds for any λ and M while π\_ref is correct. From the Stage 2c decomposition:

- **The variance:** Var(ψ | X) = E\[Var(g | X, Y)\] + Var(m\* − λm\_η) + λ² Var(m\_η)/M.
- **With p\_η = p*,*\* the optimal weight is λ\* = M/(M+1). That shrinks the reducible part H to H/(M+1). For M = 1 this halves H, where VRPO as run gets nothing.
- **With an imperfect p\_η,** a plug-in λ̂ in the style of PPI++ adapts automatically. Because λ = 0 (plain DPO) is always available, the result is asymptotically never worse than DPO.

**What's new.** PPI++ tunes λ for M-estimation ([PPI++](https://arxiv.org/abs/2311.01453v2)) \[Outside\]. It has not been used for RLHF or analysed with M as a cost. You would extend Theorem 6.2 to finite M and estimated λ̂, with cross-fitting so that p\_η and the data are independent.

**The practical snag.** Estimating λ needs gradient covariances in about 10⁹ dimensions. You can work with LoRA parameters, use a scalar λ chosen on validation data, or use a loss-level proxy.

**What it needs.**

- **Maths:** M-estimation asymptotics, Slutsky's theorem and the delta method (ST460); conditional variance decompositions and conditional independence (MA411).
- **Tools:** PyTorch, TRL and LoRA, on IMDb with synthetic BT labels so that p\* is known and variance can be measured.

**Verdict:** a dissertation's worth, and well within reach.

### D. UltraFeedback with an exchangeable-pair design — rank 2

**The problem.** UltraFeedback breaks VRPO's key assumption. Its responses come from 4 of 17 models per prompt, including GPT-4, GPT-3.5 Turbo and Bard ([OpenBMB](https://github.com/OpenBMB/UltraFeedback)). That behaviour policy is a mixture you cannot sample from or evaluate. Standard binarisation then picks pairs by their labels: the top-rated response is chosen. On-policy protocols pick the best and worst of five ([SimPO](https://arxiv.org/html/2405.14734v2)). Either way the observed pair is not drawn from π\_b ⊗ π\_b, so the second and third terms of eq. (3) no longer cancel. \[Inference\]

**The fix: exchangeability, not knowledge.** Within a prompt, the 4 UltraFeedback completions come from randomly drawn models, so they are exchangeable. Take the labelled pair as a *uniformly random* 2 of the 4, and use the other completions as the y\* pool. Their marginal distribution then matches the labelled pair's, so the correction stays unbiased without knowing π\_b. \[Inference; prove it and check it hasn't been done\]

**An on-policy variant.** Generate K responses per prompt from the SFT model, label one random pair, and use the rest as y\*. With K = 5 you get C(3,2) = 3 extra pairs at no extra generation cost, which ties directly into A's M.

**Bonus experiment.** All 4 completions are rated, so you can hide labels to trace a label-efficiency curve. This is the semi-supervised story your other topic was about.

**What it needs.**

- **Tools:** vLLM generation, TRL, LoRA or QLoRA, a judge or reward model (ArmoRM or GPM), and AlpacaEval 2, Arena-Hard and MT-Bench \[Outside\].
- **Courses:** ST455 if you also run the two-stage PPO/GRPO variant.

**Verdict.** Feasible at 0.5–1.5B parameters with LoRA on one large GPU per run. Results at 7–8B, the scale reviewers expect for UltraFeedback, need a multi-GPU node. Settle compute first.

### B. Variance reduction or distillation? — rank 3, but do it first

**The question.** Do VRPO's gains come from variance reduction, as in Theorem 6.2? Or from distilling the GPM through soft labels on fresh SFT samples?

**The design.** Use IMDb, where the truth is known, then HH. Run six arms:

1. DPO.
2. DPO plus the third term alone, a biased soft-label augmentation.
3. VRPO with M = 1.
4. VRPO with M = 4.
5. VRPO with λ̂.
6. VRPO with a deliberately degraded p\_η.

**What to measure.**

- The spread of final reward across 5–10 training seeds.
- Per-example gradient variance on a LoRA subspace.
- The reward–KL frontier.

**What's new.** A diagnostic the VRPO paper lacks (Stage 2c). If the gain survives at M = 1, its mechanism is not the one proved.

**Verdict.** Small models and a few weeks. Agree the framing with your supervisor first, because it tests his paper's mechanism.

### C. Compute-aware VRPO — rank 4

**Where the cost goes.** Per step, the cost is about (1 + M) times DPO's policy forward-backward. Reference log-probabilities and p\_η scores can be cached offline; the repository already stores the preference scores ([VRPO/VRPO](https://github.com/VRPO/VRPO)).

**The levers.** \[Inference\]

- **Correct only a random fraction q of examples per batch.** The correction has mean zero, so this stays unbiased.
- **Choose (λ, M, q) jointly** to minimise variance multiplied by FLOPs.
- **Replace the separate GPM** with a cheaper p\_η, such as a distilled small model or the primary model's own estimate, as in VRPO Fig. 3.

**What it needs.** The same maths as A, plus careful profiling.

**Verdict.** Low risk. Present it as part of A's "efficiency frontier" rather than as a standalone contribution.

### E. Estimated behaviour policy — rank 5

**The problem.** On HH and TL;DR, π\_ref is fitted to, or differs from, the real response generator. With an estimate π̂, the expected VRPO gradient becomes E\_{π\_b}\[m\*\] + (E\_{π̂} − E\_{π\_b})\[m\_η\]. \[Inference\]

- **Under correct specification** m\* ≡ 0, so this is harmless. That is Theorem 6.1.
- **Under misspecification** the target itself moves, and the error is first-order in π̂ − π\_b. It is not the product of two errors, as it would be in augmented inverse-probability weighting (AIPW).
- **So VRPO's HH results estimate a slightly different target from DPO's.** That target shift is another possible source of the gains.

**What's new.** This is the first characterisation of that shift. A full semiparametric treatment, with an efficient influence function and product-rate double robustness, is a PhD's worth of work.

**What it needs.** Semiparametric theory (Tsiatis) \[Outside\], beyond your taught courses, plus ST460.

**Verdict.** Prove one lemma that characterises the bias, and put it in your discussion section. Don't make it the dissertation.

**Course coverage, candidly.** ST460 and MA411 carry the theory. ST455 helps with the two-stage variants. ST451 is tangential, though calibrating p\_η, which matters for A, is a Bayesian-flavoured question. ST409 and ST418 don't bear on this project.

## Stage 5 — Questions for the first supervisor meeting

Lead with scope and with the Monte Carlo question. The answers decide whether A is the core contribution or something he has already solved.

**Scope**

1. Is this the VRPO brief or the semi-supervised RLHF brief, or have the two merged?
2. Of the three asks (compute, statistics, UltraFeedback), which is essential and which is a stretch goal?
3. Does "statistical efficiency" mean beating VRPO's variance, or deriving an efficiency bound?

**How VRPO works in practice**

4. How many fresh pairs per prompt does the released code use? Ask whether he agrees that Theorem 6.2's gain needs M → ∞, and what he thinks drives the HH gains at M = 1. Phrase this as a question, not a claim.
5. Was p\_η trained on the full training set, or cross-fitted?
6. On HH, π\_ref is an SFT model fitted to Anthropic's responses. How does he reconcile that with the theory's "known π\_ref"?

**UltraFeedback**

7. Which version should you use? Is a random-pair design acceptable, even though it makes your numbers harder to compare with published binarised results?
8. What model scale, and which judge or reward model for on-policy labels?

**Resources and outputs**

9. Which GPUs can you use, for how many hours, and is there an API budget for judges?
10. Is there an internal version of the code newer than the public repository?
11. Which venue and deadline does he have in mind? How does your work relate to ongoing group projects such as Xu et al. (2025)?
12. How often will you meet, what should be ready by the end of Autumn Term, and what are the ST499 deadline and length limits?

**Before the meeting**

- [ ] Clone the repository and find the extra-pair sampling in `trainer/`.
- [ ] Write the Stage 2c variance decomposition on one page, in your own notation.
- [ ] Rerun VRPO's IMDb experiment at Qwen2-0.5B scale, if you have a GPU.

## Sources

Pages opened while writing this. The three papers themselves are your attachments.

- [VRPO/VRPO repository and README](https://github.com/VRPO/VRPO): data format with one extra pair per example.
- [UltraFeedback, OpenBMB](https://github.com/OpenBMB/UltraFeedback): construction, model pool and annotation.
- [PPI++, arXiv 2311.01453](https://arxiv.org/abs/2311.01453v2): power-tuned prediction-powered inference.
- [SimPO, arXiv 2405.14734](https://arxiv.org/html/2405.14734v2): the on-policy UltraFeedback protocol and benchmarks.
