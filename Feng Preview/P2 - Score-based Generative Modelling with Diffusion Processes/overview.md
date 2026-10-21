# Score-based Generative Modelling with Diffusion Processes: Overview

**Supervisor:** Dr Oliver Feng · **Prepared:** 21 October 2026 · **Sources:** the brief and the 3 supplied papers only

> **Labels.** **[Paper]** a paper states it (with reference) · **[Brief]** the brief states it · **[Interpretation]** my own reading. Check it before relying on it.

## 1. The brief

**[Brief]** Generative modelling aims to produce artificial samples that resemble, in distribution, a training set of high-dimensional objects such as images. A recent family of methods adds noise to the training data step by step, learns the *score function* (the gradient of the log-density) of the noisy data at each noise level, and then uses the estimated scores to turn pure noise back into a new sample, via Langevin dynamics or, more generally, a diffusion process defined by a stochastic differential equation (SDE). Neural-network versions of these methods have done extremely well empirically, often beating GANs, and statisticians are now working on theoretical guarantees. The student is expected to give a detailed mathematical exposition of score-based generative modelling, including the fundamentals of *score matching*. The brief then offers three possible follow-ups: (i) apply and/or adapt the methodology to a generative modelling task of the student's choice, on simulated or real data; (ii) investigate extensions of score matching to data on different domains; or (iii) survey and perhaps extend recent mathematical results on diffusion processes and their convergence, or on the accuracy of generated samples in a nonparametric setting.

**Project type:** mainly **theoretical** (expository), with an optional **computational** or **methodological** component. The one required element is a "detailed mathematical exposition", and two of the three supplied papers are long theory papers (69 and 71 pages) with no experiments. How much the computational side matters depends on which follow-up direction is chosen. **[Interpretation]**

## 2. Paper by paper

Recommended order: **Song & Ermon (2019)** first, because it is short and introduces the objects everyone else analyses: the score, score matching, noise perturbation and Langevin sampling. Next **Li, Wei, Chen & Chi (2024)**. Its Section 2 is the cleanest statement in the folder of the forward/reverse SDE picture (VP SDE, reverse-time SDE, probability flow ODE), and it treats the *sampling* step on the assumption that the score has already been estimated. Last **Dou, Kotekal, Xu & Zhou (2024)**, which treats the *score estimation* step as a nonparametric statistics problem. It is the most demanding to read, and it closes the loop back to density estimation through Girsanov's theorem.

### 2.1 Generative Modeling by Estimating Gradients of the Data Distribution (Song & Ermon, 2019)

NeurIPS 2019; arXiv:1907.05600v3 [cs.LG], 10 Oct 2020. 23 pages, including appendices.

- **Problem.** **[Paper]** Likelihood-based generative models need special architectures or surrogate losses, and GANs train unstably and have no objective for comparing models (Sec. 1, p. 1). The authors want a model that generates samples using only the score $\nabla_x \log p_{\text{data}}(x)$, learned by score matching and sampled with Langevin dynamics (Sec. 2, pp. 2–3). Applied naively this fails for two reasons (Sec. 3, pp. 3–4). (a) Under the *manifold hypothesis* the score is undefined in the ambient space and score matching is inconsistent. (b) In low-density regions the score is poorly estimated (Fig. 2), and Langevin dynamics mixes slowly between modes. For a mixture with disjoint supports, the score does not depend on the mixing weight $\pi$, so Langevin dynamics cannot recover $\pi$ (Sec. 3.2.2, Fig. 3).
- **Approach.** **[Paper]**
  - *Score matching (Sec. 2.1).* The objective $\tfrac12\mathbb E\|s_\theta(x)-\nabla_x\log p_{\text{data}}(x)\|^2$ equals, up to a constant, $\mathbb E[\operatorname{tr}(\nabla_x s_\theta(x))+\tfrac12\|s_\theta(x)\|^2]$ (Eq. 1). The trace term is too expensive in high dimension, so they review two scalable versions. *Denoising* score matching (Eq. 2) regresses $s_\theta(\tilde x)$ onto $\nabla_{\tilde x}\log q_\sigma(\tilde x\mid x)$ and recovers the score of the *noised* density $q_\sigma$. *Sliced* score matching (Eq. 3) uses random projections $v^\top\nabla_x s_\theta(x) v$.
  - *Langevin dynamics (Eq. 4):* $\tilde x_t=\tilde x_{t-1}+\tfrac{\epsilon}{2}\nabla_x\log p(\tilde x_{t-1})+\sqrt{\epsilon}\,z_t$. This is exact only as $\epsilon\to0$ and $T\to\infty$. They ignore the Metropolis–Hastings correction.
  - *Noise Conditional Score Network (NCSN, Sec. 4.1).* Take a geometric sequence $\sigma_1>\dots>\sigma_L$ and the perturbed densities $q_\sigma=p_{\text{data}}*\mathcal N(0,\sigma^2I)$. A single network $s_\theta(x,\sigma)$ is trained on the weighted sum of denoising objectives $\mathcal L=\frac1L\sum_i\lambda(\sigma_i)\ell(\theta;\sigma_i)$ with $\lambda(\sigma)=\sigma^2$ (Eqs. 5–6, p. 6). The weight is chosen because they observe empirically that $\|s_\theta\|\propto1/\sigma$.
  - *Annealed Langevin dynamics (Alg. 1, p. 6).* Run $T$ Langevin steps at each noise level from largest to smallest, with step size $\alpha_i=\epsilon\,\sigma_i^2/\sigma_L^2$. The motivation is to keep a "signal-to-noise" ratio fixed.
  - Architecture: a RefineNet/U-Net variant with dilated convolutions and a modified conditional instance normalisation, "CondInstanceNorm++" (App. A).
- **Main findings and results.** **[Paper]**
  - No theorems. The consistency claims for score matching are cited from earlier work ([24], [53], [61]).
  - On a 2-D Gaussian mixture, annealed Langevin recovers the mode weights that plain Langevin gets wrong, with exact scores in both cases (Fig. 3).
  - CIFAR-10 unconditional: Inception score 8.87, then a new state of the art, and FID 25.32, comparable to SNGAN (Table 1, p. 7).
  - Uncurated samples on MNIST, CelebA and CIFAR-10 (Fig. 5).
  - Inpainting by clamping the observed pixels inside annealed Langevin (Fig. 6; App. B.3, Alg. 2).
  - A single-noise-level baseline ($\sigma=0.01$) "fails to generate reasonable images" (p. 8; App. C.1).
  - Without any added noise, the sliced score matching loss on CIFAR-10 fluctuates and fails to converge (Fig. 1).
- **Key assumptions.**
  - **[Paper]** The network has enough capacity for the minimiser of Eq. 6 to equal the true noisy scores (p. 6).
  - **[Paper]** The Langevin discretisation error is negligible when $\epsilon$ is small and $T$ large (p. 3).
  - **[Paper]** The design is aimed at images: "we … leave the architecture design for other domains as future work" (Sec. 4.1, p. 5).
  - **[Paper]** The choices of noise schedule and weighting are heuristic and empirical (pp. 6–7).
- **Relation to the other papers.**
  - **[Interpretation]** The paper does not use SDE language. Its perturbed density $q_\sigma=p_{\text{data}}*\mathcal N(0,\sigma^2 I)$ is, however, exactly the time-$t=\sigma^2$ marginal $p(\cdot,t)=\varphi_t*f$ of the variance-exploding forward process $dX_t=dW_t$ that Dou et al. study (their Eq. 16, p. 8). The NCSN loss is the empirical counterpart of the score-matching loss in Dou et al.'s Eq. (4).
  - **[Interpretation]** Annealed Langevin is a different sampler from the DDPM-type and probability-flow-ODE samplers analysed by Li et al. Neither theory paper analyses Algorithm 1 directly.
  - **[Paper]** Li et al. cite this paper as one of the works that popularised diffusion models (p. 2).

### 2.2 Towards Faster Non-Asymptotic Convergence for Diffusion-Based Generative Models (Li, Wei, Chen & Chi, 2024)

arXiv:2306.09251v3 [stat.ML], 7 Mar 2024 (June 2023; revised February 2024). 69 pages: main text pp. 1–25, proofs in Apps. A–E.

- **Problem.** **[Paper]** Given $\ell_2$-accurate score estimates, how many discrete steps $T$ does a sampler need before the generated distribution is $\varepsilon$-close in total variation (TV) to the target? The paper also asks how score errors propagate. Earlier theory for the deterministic (probability flow ODE) sampler was either non-quantitative in $d$ and $1/\varepsilon$, exponential in Lipschitz constants, assumed exact scores, or ignored discretisation (pp. 3, 10).
- **Approach.** **[Paper]**
  - *Forward chain:* $X_t=\sqrt{1-\beta_t}X_{t-1}+\sqrt{\beta_t}W_t$ (Eq. 4), so that $X_t=\sqrt{\bar\alpha_t}X_0+\sqrt{1-\bar\alpha_t}\,\bar W_t$ (Eq. 6). This is the discrete "variance-preserving" chain, whose continuum limit is $dX_t=-\tfrac12\beta(t)X_tdt+\sqrt{\beta(t)}dW_t$ (Eq. 14).
  - Sec. 2.2 (pp. 5–6) gives the continuous-time motivation. It states the probability flow ODE (Eq. 15) and the reverse-time SDE (Eq. 16, attributed to Anderson 1982 and Haussmann–Pardoux 1986). Both have the same marginals as the forward process and depend on the data only through $\nabla\log q_t$.
  - Two discrete samplers are analysed:
    - a deterministic ODE-type sampler, $Y_{t-1}=\frac1{\sqrt{\alpha_t}}\big(Y_t+\frac{1-\alpha_t}{2}s_t(Y_t)\big)$ (Eq. 23);
    - a DDPM-type stochastic sampler, $Y_{t-1}=\frac1{\sqrt{\alpha_t}}\big(Y_t+(1-\alpha_t)s_t(Y_t)\big)+\sigma_tZ_t$ (Eq. 30).
  - Two "accelerated" variants (Eqs. 27, 33) need extra learned quantities, $w_t$ and $v_t$ (Assumptions 3–4), which play the role of higher-order correction terms.
  - The step-size ("learning rate") schedule (Eq. 22, p. 8) starts at $\beta_1=T^{-c_0}$ and grows geometrically at rate $c_1\log T/T$.
  - The key methodological claim is that the analysis works *directly in discrete time with elementary tools*: "No knowledge of SDEs or ODEs is required" (p. 4; also pp. 6, 24).
- **Main findings and results.** **[Paper]** In each theorem, $q_1$ is the law of $X_1$ and $p_1$ the law of $Y_1$.
  - **Theorem 1** (deterministic sampler, p. 8): $\mathrm{TV}(q_1,p_1)\lesssim \frac{d^2\log^4T}{T}+\frac{d^6\log^6T}{T^2}+\sqrt{d\log^3T}\,\varepsilon_{\text{score}}+d\log T\,\varepsilon_{\text{Jacobi}}$. With perfect scores, this gives iteration complexity $\tilde O(d^2/\varepsilon+d^3/\sqrt\varepsilon)$ (Eq. 25). The paper says this is the first result for this sampler with a concrete $1/\varepsilon$ rate that also accounts for score error in discrete time (pp. 3, 10).
  - A counter-example (p. 9) shows that a small $\ell_2$ score error alone cannot control TV for the deterministic sampler, because the output can be made discrete. This is why Assumption 2, on the Jacobian error, is needed.
  - **Theorem 2** (accelerated deterministic, pp. 10–11): with exact scores, $\mathrm{TV}\lesssim d^6\log^6T/T^2$, i.e. $\tilde O(d^3/\sqrt\varepsilon)$ steps (Eq. 29).
  - **Theorem 3** (DDPM-type, p. 11): $\mathrm{TV}\le\sqrt{\tfrac12\mathrm{KL}(q_1\|p_1)}\lesssim\sqrt{d^2\log^3T/T}+\sqrt d\,\varepsilon_{\text{score}}\log^2T$, for $T\gtrsim d^4\log^6T$. That is $1/\varepsilon^2$ steps, the same $\varepsilon$-dependence as prior SDE-based work but with worse $d$-dependence.
  - **Theorem 4** (accelerated stochastic, p. 12): $\mathrm{TV}\lesssim\sqrt{d^3\log^{4.5}T/T}$, i.e. $\tilde O(d^3/\varepsilon)$ steps (Eq. 35).
  - No experiments. **[Interpretation]** I checked the text for experiments and simulations and found none.
- **Key assumptions.** **[Paper]**
  - Assumption 1: average $\ell_2$ score error $\le\varepsilon_{\text{score}}^2$ (Eq. 19).
  - Assumption 2: average Jacobian error $\le\varepsilon_{\text{Jacobi}}$, needed only for the deterministic sampler (Eq. 20).
  - Data: $X_0$ is absolutely continuous with $\|X_0\|_2\le T^{c_R}$ almost surely (Eq. 21). No smoothness is assumed, and this can be relaxed to a bound $B$ at a $\log B$ cost (p. 9).
  - Convergence is to $q_1$, not $q_0$, which is a form of early stopping justified by $\bar\alpha_1\approx1$ (Remark 2, p. 8).
  - The constants $c_0,c_1$ are "large enough" and not specified.
- **Proof techniques.** **[Paper]**
  - For Theorem 1 (Sec. 5.2, pp. 16–20; App. B), the paper tracks the density ratio $p_{Y_t}/p_{X_t}$ step by step. A change-of-variables identity (Eq. 55) splits it into a product of one-step ratios.
  - Each one-step ratio is Taylor-expanded (Lemma 4, Eq. 58) using the representation of the score as a conditional expectation (Tweedie-type, Eq. 36). The expansion is controlled by tail bounds on $X_0\mid X_t$ (Lemma 1: sub-Gaussian-type moments) and by "typical set" arguments (Lemma 2; the set $\mathcal E$ in Eq. 60).
  - For Theorem 3 (Sec. 5.3, pp. 20–24; App. C), Pinsker's inequality reduces TV to KL (Eq. 78). The KL between the two Markov chains is decomposed step by step, which is possible because both one-step kernels are Gaussian (Eq. 76).
  - The initial-distribution error $\mathrm{KL}(q_T\|\mathcal N(0,I))\lesssim T^{-200}$ (Lemma 3, p. 15).
  - **[Interpretation]** The appendices are long because they are full of delicate Taylor expansions with explicit high-probability events. Conceptually they need only multivariate calculus, Gaussian facts and Markov-chain KL decompositions, not Itô calculus.
- **Relation to the other papers.**
  - **[Paper]** The paper studies the *sampling* phase on the assumption that score estimation has been done well ("divide-and-conquer", p. 3). It lists "end-to-end performance guarantees that take into account both the score learning phase and the sampling phase" as open (Sec. 6, p. 25).
  - **[Interpretation]** Dou et al. supply the missing statistical half, but in continuous time and one dimension, whereas Li et al. work in discrete time in $\mathbb R^d$.

### 2.3 From optimal score matching to optimal sampling (Dou, Kotekal, Xu & Zhou, 2024)

arXiv:2409.07032v1 [stat.ML], 11 Sep 2024. 71 pages: main text pp. 1–24, proofs in Apps. A–D.

- **Problem.** **[Paper]** What is the *sharp minimax rate* for estimating the score of the diffused density $p(\cdot,t)=f*\mathcal N(0,t)$ from $n$ i.i.d. samples of $f$, in the score-matching loss $\int|\hat s-s|^2p\,dx$ (Eq. 4)? And does a diffusion model built on the optimal estimator attain the optimal density-estimation rate *without* extra log factors and *without* early stopping? (Abstract; Sec. 1.2, pp. 3–4, criticises early stopping as "ad hoc".)
- **Approach.** **[Paper]**
  - *Setting:* the variance-exploding forward SDE $dX_t=dW_t$ (Sec. 1.3, Eq. 16), in one dimension. The class $\mathcal F_\alpha$ (Eq. 9) contains densities supported on $[-1,1]$ that are $\alpha$-Hölder there and bounded above and below by constants. These densities are therefore discontinuous at $\pm1$.
  - The score is written as $s=\psi/p$ with $\psi=\partial_xp$, and the two parts are estimated separately, with an estimator that depends on the noise regime (Sec. 2):
    - *very high noise* ($t\gtrsim1$): Gaussian-kernel plug-in with an $x$-dependent regulariser $\varepsilon(x,t)$ in the denominator (Eq. 11);
    - *high noise* ($n^{-2/(2\alpha+1)}\lesssim t\lesssim1$): unbiased empirical $\hat\psi,\hat p$ with regularisation (Eq. 12);
    - *low noise*: a boundary-corrected higher-order kernel density estimator $\hat f$ (Eq. 13), plugged in separately on interior, boundary and exterior regions $D_1,D_2,D_3$ (Eqs. 14–15). For $\alpha<1$ they use a trivial data-free estimator.
  - Sampling: plug $\hat s$ into the reverse SDE $d\hat Y_t=\hat s(\hat Y_t,T-t)dt+dW_t$, start from $\mathcal N(0,T)$ with $T=n$, and truncate the output to $[-1,1]$ (Alg. 1, p. 8).
- **Main findings and results.** **[Paper]**
  - **Theorems 1–5** (pp. 9–10), upper bounds: the minimax score risk is at most $\frac1{nt^2}\wedge\frac1{nt^{3/2}}\wedge\big(n^{-2(\alpha-1)/(2\alpha+1)}+t^{\alpha-1}\big)$, for all $\alpha>0$ and $t\ge0$.
  - **Theorems 6–7** (pp. 10–11), matching lower bounds. Together these give the sharp rate (Eq. 10). There are three regimes (Remark 1, p. 5), and the rate improves on Wibisono et al., Zhang et al. and Oko et al.
  - **Theorem 8** (p. 11): $\sup_f\mathbb E\,d_{TV}(X_0,\hat X_0)\lesssim n^{-\alpha/(2\alpha+1)}$, the minimax density-estimation rate, with no log factors and no early stopping (Remark 3, p. 5).
  - **Theorem 9** (p. 12): $\mathbb E\,W_1\lesssim n^{-1/2}$ for $\alpha\ge1$.
  - Sec. 5 (pp. 23–24) states the multivariate analogues. The score rate is $\frac1{nt^2}$ for $t>1$ and $\frac1{nt^{d/2+1}}\wedge(n^{-2(\alpha-1)/(2\alpha+d)}+t^{\alpha-1})$ for $t\le1$. The TV rate is $n^{-\alpha/(2\alpha+d)}$, and $W_1$ is $n^{-(\alpha+1)/(2\alpha+d)}$ for $d>2$ and $\log n\cdot n^{-1/2}$ for $d=2$. The paper says the extension is "straightforward" and only sketches it, in App. D.
  - A notable point is that the boundary discontinuity does not slow the score rate, because the score is "self-normalised" (Remark 4, pp. 5–6).
  - No experiments.
- **Key assumptions.** **[Paper]**
  - One dimension for the main theorems.
  - Compact support $[-1,1]$, with density bounded below on it (Eq. 9).
  - Hölder smoothness $\alpha$ with known constant $L$.
  - The estimator is a hand-crafted kernel method, not a neural network.
  - **[Interpretation]** The smoothness $\alpha$ appears to be assumed known, since the bandwidth $h\asymp n^{-1/(2\alpha+1)}$ depends on it (p. 10). The paper does not discuss adaptivity.
  - **[Interpretation]** Alg. 1 "solves the SDE" exactly in continuous time. Time discretisation, which is Li et al.'s topic, is not analysed.
- **Proof techniques.** **[Paper]**
  - Upper bounds: a decomposition of the score risk into derivative-estimation and density-estimation errors (Lemma 1, p. 14), standard kernel bias–variance bounds (Lemma 4, p. 14), and region-by-region comparisons of exponential tail rates (Sec. 4.1; App. A).
  - Lower bounds: Le Cam's two-point method for $t\gtrsim1$ (Sec. 4.2.1). Fano's method with a Gilbert–Varshamov packing for $t\lesssim1$ (Sec. 4.2.2, pp. 18–20). The new ingredient is a bump width $\rho\asymp\sqrt t\vee\epsilon$ decoupled from the bump height. The $L^2$ separation of the *convolved* derivatives is then lower-bounded using the **heat equation** $\partial_t(\varphi_t*h)=\tfrac12\partial_x^2(\varphi_t*h)$, integration by parts and a first-order Taylor bound (Eq. 28, Prop. 4).
  - Density estimation: a triangle inequality across three processes ($Y,\tilde Y,\hat Y$; Table 1, p. 21), the data-processing inequality, Pinsker's inequality, and **Girsanov's theorem**. The Girsanov step (Lemma 20, p. 52) bounds the KL divergence between path measures by $\tfrac12\int_0^T\!\int p\,\|a-b\|^2$, with equality under Novikov's condition. The $W_1$ result uses a chain of intermediate processes that switch from $s$ to $\hat s$ at dyadic times (Sec. 4.3.2).
- **Relation to the other papers.**
  - **[Interpretation]** This paper bounds exactly the quantity that Li et al. take as given ($\varepsilon_{\text{score}}$), though in a different time parametrisation and dimension.
  - **[Interpretation]** The paper connects the rate of score estimation to classical nonparametric density estimation (Hölder classes, minimax theory). This is the "accuracy of the samples generated in a nonparametric context" that the brief mentions.
  - **[Interpretation]** It also gives a rigorous version of Song & Ermon's empirical observation that large noise makes score estimation easier: the risk falls like $1/(nt^{3/2})$ and then $1/(nt^2)$ as $t$ grows.

## 3. How the papers fit together

**[Interpretation]** The common thread is a two-stage pipeline: (1) estimate the score of the noised data at every noise level; (2) plug it into a sampler that runs from noise back to data. The papers split this pipeline along different axes:

```
                 score estimation (stage 1)             sampling (stage 2)
Song & Ermon     neural net + denoising SM (empirical)  annealed Langevin (heuristic)
Dou et al.       kernel estimator, sharp minimax rate   exact continuous-time reverse SDE,
                 (1-D, Hölder, compact support)         Girsanov  ->  optimal TV / W1 rate
Li et al.        assumed: eps_score, eps_Jacobi given   discrete DDPM / prob.-flow ODE,
                                                        iteration complexity in d and 1/eps
```

| Axis | Song & Ermon | Li et al. | Dou et al. |
|---|---|---|---|
| Nature | methodological / empirical | theory (sampling) | theory (statistics) |
| Forward process | Gaussian perturbation at $L$ levels (≈ VE) | discrete VP chain | continuous VE SDE $dX=dW$ |
| Time | discrete noise levels | discrete, $T$ steps | continuous |
| Dimension | images ($D=3072$ for CIFAR-10) | general $d$, polynomial dependence | $d=1$ (sketch for fixed $d$) |
| Data assumptions | none formal | bounded support, no smoothness | Hölder-$\alpha$, compact support, bounded below |
| Error metric | IS / FID | TV (and KL) | score-matching loss, TV, $W_1$ |
| SDE machinery | none | deliberately avoided | Girsanov, reverse-time SDE |

**What looks settled (within these papers).**
- **[Paper]** Score-based modelling works in practice on images (Song & Ermon, Table 1).
- **[Paper]** With good scores, discrete samplers converge in TV polynomially in $d$ and $1/\varepsilon$: $1/\varepsilon$ for the ODE sampler and $1/\varepsilon^2$ for the DDPM sampler (Li et al., Thms 1, 3).
- **[Paper]** In one dimension under Hölder smoothness, kernel score estimation plus the exact reverse SDE is minimax-optimal for density estimation (Dou et al., Thms 1–9).

**What is unsettled.**
- **[Paper]** The optimal dimension dependence for samplers. Sharp Wasserstein-distance results that might remove the Jacobian assumption. Acceleration using only the score. End-to-end guarantees (all from Li et al., Sec. 6, p. 25).
- **[Interpretation]** Dou et al.'s optimality is for a kernel estimator in low dimension. It does not show that neural score estimators achieve these rates, and the rate $n^{-\alpha/(2\alpha+d)}$ shows the usual curse of dimensionality. This leaves a gap between theory and why the method works so well on images. None of the papers analyses Song & Ermon's annealed Langevin sampler.

## 4. Tie-in to the dissertation

### 4.1 What the proposed directions mean in practice

1. **Mathematical exposition, including score matching (required).** **[Interpretation]** This would involve:
   - deriving Hyvärinen's integration-by-parts identity (Song & Ermon Eq. 1) and the denoising score-matching identity (Eq. 2; Li et al. Eq. 18; Tweedie-type formula Li et al. Eq. 36);
   - setting up the forward SDEs (VP: Li et al. Eq. 14; VE: Dou et al. Eq. 16) and stating the reverse-time SDE and probability flow ODE (Li et al. Eqs. 15–16; Dou et al. Eq. 2). Ideally the exposition would *derive* the probability flow ODE from the Fokker–Planck equation, which the papers do not do; they cite Song et al. 2021b and Anderson 1982;
   - explaining Langevin dynamics and why annealing helps (Song & Ermon Sec. 3);
   - showing how Girsanov's theorem turns score error into a TV bound (Dou et al. Eq. 5 and Lemma 20).

   Much of this is a careful write-up of standard results, at the level of the Itô calculus taught this term.
2. **Apply or adapt the methodology to a generative task (simulated or real data).** **[Interpretation]** Implement denoising score matching and a sampler, either annealed Langevin, Euler–Maruyama on the reverse SDE, or the discrete samplers (Eqs. 23, 30 of Li et al.). Then:
   - *Simulated data:* low-dimensional mixtures (Song & Ermon's 2-D example, App. B.1), where true scores are known and TV or $W_1$ can be computed.
   - *Real data:* MNIST or another small dataset of the student's choice, or perhaps tabular or financial time-series data, given the student's background.
   - A natural empirical study would probe a theoretical claim: for example, compare the deterministic and stochastic samplers' error against $T$ (checking Li et al.'s $1/T$ versus $1/\sqrt T$ rates), or compare a kernel score estimator with a small neural network in 1-D against Dou et al.'s rate.
3. **Extensions of score matching to data on different domains.** **[Interpretation]** The supplied papers barely touch this. Song & Ermon raise the manifold hypothesis (Sec. 3.1) and leave "other domains" to future work (p. 5). Dou et al. handle a compactly supported density with a boundary and note that the boundary does not slow the score rate (Remark 4). Concretely, "different domains" could mean bounded or constrained domains (e.g. $[0,1]^d$ or the positive orthant), manifolds (e.g. spheres), or discrete data. Each would need new forward processes or score-matching objectives that the folder does not contain, so the supervisor would have to point to literature.
4. **Survey and perhaps extend convergence or nonparametric-accuracy results.** **[Interpretation]** Survey: compare the two proof strategies (Li et al.'s discrete density-ratio approach against Girsanov/continuous-time approaches) and the various assumptions in the literature both papers review (Li et al. Sec. 4; Dou et al. Sec. 1.2). Extensions small enough for an MSc might include:
   - redoing Dou et al.'s upper bound for the VP/OU forward process instead of VE;
   - writing out the multivariate case carefully (App. D is only a sketch);
   - combining Dou et al.'s score rate with a discretisation bound in the style of Li et al. Theorem 3 to get an end-to-end rate in 1-D;
   - working through a simpler special case of Li et al.'s argument, e.g. Gaussian data where everything is explicit.

### 4.2 What a dissertation would plausibly involve

**[Interpretation]** Shape A, "theory-leaning":
- Chapters 1–3 (about 50%): exposition of score matching, forward and reverse SDEs, Girsanov, and the TV bound.
- Chapter 4 (about 30%): a detailed walk-through of Dou et al.'s 1-D upper and lower bounds, possibly reproving one regime in full (the very-high-noise regime, Theorem 2, is the most self-contained: Sec. 4.1.1, App. A.3). Or a simplified version of one of Li et al.'s theorems.
- A short simulation chapter (about 20%) checking the predicted rates numerically in 1-D: kernel score estimator, Euler–Maruyama reverse SDE, TV or $W_1$ against $n$.

**[Interpretation]** Shape B, "methodology plus experiments":
- Exposition as above, but shorter (about 35%).
- Implement NCSN-style denoising score matching with a small network, then compare samplers (annealed Langevin, DDPM-type, probability flow ODE) on 2-D mixtures and a small real dataset (about 45%), with an analysis linking the observations to Li et al.'s rates and Song & Ermon's diagnosis of mode-weight failure (about 20%).
- A possible "adapt" twist: a non-image dataset, or a constrained domain.

Neither shape needs a new theorem. A modest extension, such as the VP-SDE version of a Dou et al. bound, would strengthen Shape A.

### 4.3 Open questions

**[Paper]** From Li et al. Sec. 6 (p. 25):
- the dimension dependence of their bounds is sub-optimal (also footnote 3, p. 9, which traces this to Lemma 4);
- can sharp Wasserstein-distance results be obtained, and could they relax the Jacobian Assumption 2?
- how far can sampling be accelerated using *only* score functions, rather than the extra $w_t$ and $v_t$ estimates?
- end-to-end guarantees combining score learning and sampling.

**[Paper]** Li et al. also note a worse $d$-dependence than Chen et al. (2023b) for the ODE sampler (p. 10) and than Chen et al. (2022a) for the DDPM sampler (p. 11).

**[Paper]** Dou et al. do not include a future-work section. Their Sec. 5 states that the multivariate extension is "straightforward" but only sketches it (App. D). They note that for $d=2$ their $W_1$ bound carries a $\log n$ factor that matches the best known result (p. 12, p. 24). Whether that factor is necessary is, in my reading, left open. **[Interpretation]**

**[Paper]** Song & Ermon leave architecture design for non-image domains as future work (p. 5). They also ignore the Metropolis–Hastings correction for finite step sizes (p. 3).

**[Interpretation]** Further questions implied by the papers:
- Can a neural-network (empirical risk minimisation) score estimator achieve Dou et al.'s sharp rates? They contrast with Oko et al.'s neural results, which carry log factors and use early stopping (p. 4).
- What happens when $\alpha$ is unknown (adaptivity)?
- What guarantees exist for annealed Langevin sampling?

## 5. Background knowledge required

| Area | Item | Status | Rough effort if not covered | Where it's needed |
|---|---|---|---|---|
| Maths | Measure-theoretic probability: densities, Radon–Nikodym derivatives, change of measure | covered by my modules | n/a | Girsanov step and TV/KL definitions (Dou et al. Sec. 4.3; Li et al. notation, p. 4) |
| Maths | Brownian motion, Itô integral, Itô's formula, SDE existence/uniqueness | covered by my modules | n/a | Forward SDEs: Li et al. Eqs. 13–14; Dou et al. Eqs. 1, 16 |
| Maths | Explicit solution of linear SDEs (OU / VP process; $X_t=X_0+\sqrt t Z$ for VE) | covered by my modules | a few days if the module skips OU | Li et al. Eq. 6; Dou et al. p. 8 |
| Maths | Fokker–Planck (Kolmogorov forward) equation | partly covered | about 1 week | Deriving the probability flow ODE (Li et al. Eq. 15), which the papers only state; the heat equation is its special case (Dou et al. Eq. 28) |
| Maths | Time reversal of diffusions (Anderson 1982; Haussmann–Pardoux 1986) | new to me | 1–2 weeks to understand and state carefully; a full proof is beyond MSc scope | Reverse-time SDE: Li et al. Eq. 16; Dou et al. Eq. 2 |
| Maths | Girsanov's theorem and Novikov's condition | partly covered (usually stated near the end of an Itô course) | about 1 week to reach the KL-between-path-measures form | Dou et al. Lemma 20 and Thm 8; Eq. 5 |
| Maths | Heat equation, Gaussian convolution, integration by parts, Taylor bounds | partly covered | a few days | Dou et al. lower bound (Prop. 4, Eq. 28) |
| Maths | Langevin diffusion and its discretisation; mixing of MCMC | partly covered | about 1 week | Song & Ermon Eq. 4, Sec. 3.2.2, Alg. 1 |
| Statistics | Score matching (Hyvärinen), denoising score matching, Tweedie's formula | new to me | about 1 week | All three papers: Song & Ermon Eqs. 1–3, 5; Li et al. Eqs. 18, 36; Dou et al. Sec. 1.2 |
| Statistics | TV, KL, Pinsker, data-processing inequality, Wasserstein-1 | partly covered | a few days | Li et al. Thm 3 proof (Eq. 78); Dou et al. Sec. 4.3 |
| Statistics | Nonparametric density estimation: Hölder classes, higher-order and boundary kernels, bias–variance rates | partly covered (KDE basics likely; higher-order theory unlikely) | 2–3 weeks | Dou et al. Sec. 2.3, Eq. 13, Lemma 4 |
| Statistics | Minimax lower bounds: Le Cam two-point, Fano, Gilbert–Varshamov | new to me | substantial: 3–4 weeks to use confidently | Dou et al. Thms 6–7, Sec. 4.2 |
| Statistics | Non-asymptotic probability: sub-Gaussian tails, concentration, high-probability events | partly covered | 1–2 weeks | Li et al. Lemmas 1–2 and the whole appendix |
| CS-ML | Deep learning in PyTorch; autodiff (incl. Jacobian–vector products) | partly covered | 1–2 weeks to train a score network competently | Song & Ermon Sec. 4, App. A; sliced SM (Eq. 3) |
| CS-ML | U-Net/RefineNet architectures, conditional normalisation | new to me | about 1 week (or use an existing implementation) | Song & Ermon App. A |
| CS-ML | Sample-quality metrics (Inception score, FID) | new to me | a few days | Song & Ermon Table 1 |
| CS-ML | Simulating SDEs (Euler–Maruyama) | partly covered | a few days | Implementing reverse SDE / Dou et al. Alg. 1 |

**[Interpretation]** The current modules apply directly to the forward SDEs, Itô's formula, explicit OU/Brownian solutions, change of measure, and the *statement* of Girsanov, which is enough to follow Dou et al.'s route from score error to TV error. What goes beyond them is time reversal of diffusions and the Fokker–Planck derivation of the probability flow ODE, both of which the papers only cite. The biggest gap is **nonparametric minimax theory** (Hölder classes, higher-order kernels, Fano/Le Cam), which is essential for a serious treatment of Dou et al. and which is not in the reader's modules. Li et al.'s proofs avoid SDEs altogether, but they are long, careful non-asymptotic calculations and should be budgeted for accordingly.

## 6. Practicalities

### Code

- **[Paper]** Song & Ermon: "Code and checkpoints are available at https://github.com/ermongroup/ncsn" (App. A, p. 14), implemented in PyTorch. They used the official Inception-score code (https://github.com/openai/improved-gan/tree/master/inception_score) and the TTUR FID code (https://github.com/bioinf-jku/TTUR) (App. B.2, p. 15).
- **[Paper]** Li et al.: no code is mentioned. The paper is purely theoretical.
- **[Paper]** Dou et al.: no code is mentioned. The estimator is fully specified in Sec. 2 and Alg. 1, so it could be implemented from the text. **[Interpretation]**

### Data

- **[Paper]** Song & Ermon use MNIST, CelebA (centre-cropped to 140×140, resized to 32×32) and CIFAR-10 (Sec. 5, p. 7), plus synthetic 2-D Gaussian mixtures (App. B.1). The paper cites the dataset sources but does not explicitly describe them as public. **[Interpretation]** All three are, as far as I know, standard freely downloadable benchmarks, but this is not stated in the paper.
- **[Paper]** Li et al. and Dou et al. use no data.

### Compute

- **[Paper]** Song & Ermon:
  - Toy experiments on a CPU; the appendix says "Intel Core i7 GPU with 2.7GHz", presumably meaning CPU (App. B.1).
  - The Fig. 1 ResNet on one Titan XP.
  - Image models trained with Adam for 200,000 iterations at batch size 128: MNIST on one Titan XP, CelebA and CIFAR-10 on two (App. B.2).
  - Sampling uses $L\times T=10\times100=1000$ network evaluations per sample (Sec. 5). FID and IS were computed on 50,000 samples.
  - No wall-clock times are reported.
- **[Paper]** Li et al. and Dou et al. report no compute.
- **[Interpretation]**
  - 1-D and 2-D experiments (kernel score estimators, small MLP score networks, Euler–Maruyama samplers) run comfortably on a laptop in minutes.
  - An MNIST-scale score network is feasible on a single university-cluster GPU in hours, or possibly a long laptop run with a much smaller network.
  - Reproducing CIFAR-10 at the paper's scale (two GPUs, 200k iterations, 50k samples for FID) is likely several GPU-days and probably not worth it for an MSc. Using the released checkpoints, or a much smaller model, would be the sensible route.

## 7. Questions for the proposal meeting

1. **Which follow-up direction does Dr Feng favour: applied, different domains, or convergence/nonparametric theory?** The brief offers three, and the split between proofs and coding depends entirely on this choice.
2. **How "detailed" should the mathematical exposition be?** Should the reverse-time SDE and the probability flow ODE be derived (via Fokker–Planck), or can they be stated and cited, as the papers do? This decides how much SDE theory beyond the current modules is needed.
3. **Is a new result expected, or is a careful exposition plus reproduction of known results acceptable?** This changes the risk profile considerably.
4. **If theory: which paper should be central?** Dou et al. (nonparametric, statistical) and Li et al. (sampling, non-asymptotic) need quite different toolkits, and Dou et al.'s minimax lower bounds need background (Fano/Le Cam) the reader does not have yet.
5. **Would a 1-D end-to-end result be a reasonable "extension"?** That is, combining Dou et al.'s score rates with a discretisation analysis like Li et al.'s, which both papers leave open (Li et al. Sec. 6). Is this realistic for an MSc, or too ambitious?
6. **Would a VP/OU version of Dou et al.'s results be a sensible smaller extension?** They work only with the VE process $dX=dW$, whereas Li et al. use VP.
7. **What does "different domains" mean in the brief: bounded domains, manifolds, discrete data?** Which references should I read? None of the supplied papers develops this.
8. **For the applied route, what dataset is suitable, and is non-image data (e.g. financial time series) acceptable or encouraged?** Song & Ermon focus on images and leave other domains open (p. 5).
9. **What compute is available: an LSE cluster GPU, or laptop only?** This decides whether anything beyond toy or MNIST-scale experiments is feasible.
10. **Should the experiments test a theoretical prediction?** For example, TV against $T$ for deterministic and stochastic samplers, or score risk against $n$ and $t$. Or is sample quality on a real task the goal? This shapes the evaluation metrics, e.g. exact TV/$W_1$ on toy data versus FID.
11. **Which extra background reading on nonparametric minimax theory and on time reversal of diffusions does Dr Feng recommend?** The folder cites but does not include the standard references (e.g. Tsybakov; Anderson 1982).
12. **What is the timeline: when should the exposition be drafted, and when should coding start?** The theory reading, especially the 69- and 71-page papers, could easily absorb the whole summer if not scoped.
