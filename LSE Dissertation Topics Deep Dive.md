# LSE Dissertation Topics: Deep Dive

Oct 13, 2026 · @Alex

## How to read this

Each project gets the same four questions: what it actually asks, the maths you'd use, where the research is heading, and the main risk. Fit is judged against your modules: ST460 (inference), ST409 (stochastic processes), MA411 (probability and measure), and three of ST451, ST455 and ST418.

Projects fall into three kinds, which drives risk more than topic does:

- **Proof-driven** — success means proving something; high upside, uncertain outcome.
- **Method plus experiments** — a guaranteed core with room for an original extension.
- **Engineering-heavy** — most time goes on making code and data work.

Shi's two projects are covered in the chat, not here.

## David Itkin

The simulation project is the better-scoped of Itkin's two; the boundary-attainment project is open-ended theory with an uncertain deliverable.

Itkin works in stochastic portfolio theory (SPT): models for large equity markets over long horizons. His [hybrid Jacobi paper with Larsson](https://ideas.repec.org/p/arx/papers/2110.14046.html) (Annals of Applied Probability, 2024) analyses ergodicity, particle collisions and boundary attainment for market-weight processes. Both projects come out of that toolkit.

### Project 1: Boundary attainment of multivariate Markov processes

**What it asks.** When does a diffusion living in a domain actually hit the edge? In one dimension, Feller's boundary classification gives a complete answer through the scale function and speed measure. In several dimensions, tools for proving a process *never* hits the boundary (Lyapunov-type test functions) are mature; tools for proving that it *does* are not. Recent work builds test functions from the process's candidate invariant measure to show hitting occurs. The project asks how far that method generalises.

**Applications.** A stock's market weight hitting zero (dropping out of the market), a firm hitting bankruptcy, a queue hitting capacity, a population going extinct.

**Maths.** Generators and Itô's formula, Feller tests, Lyapunov and Khasminskii-style stability arguments, invariant measures and the stationary Fokker–Planck equation. The Itkin–Larsson paper also lists [Dirichlet forms among its tools](https://par.nsf.gov/servlets/purl/10525396). ST409 is the core prerequisite; MA411 supplies the measure theory.

**Risk.** Proof-driven. A realistic deliverable is a careful survey, a reproduction of the existing test-function argument, and its application to one new class of examples. Ask Itkin which example class he has in mind.

### Project 2: Simulation schemes for multivariate reflected SDEs

**What it asks.** A reflected diffusion gets pushed back inward whenever it touches the boundary. Simulating this in many dimensions is hard. The standard projected Euler scheme only achieves [weak order 1/2, versus order 1 without reflection](https://researchportal.ip-paris.fr/en/publications/efficient-schemes-for-the-weak-approximation-of-reflected-diffusi/). A [symmetrised Euler scheme](https://www.cambridge.org/core/journals/journal-of-applied-probability/article/symmetrized-euler-scheme-for-an-efficient-approximation-of-reflected-diffusions/6C3ED94163CACEF1566FD96DAF52737C) recovers order 1 on smooth boundaries.

The new ingredient is Itkin and Karatzas's [Folding representations of reflected diffusions](https://arxiv.org/abs/2607.28004) (July 2026). It builds reflected diffusions, including oblique reflection on convex domains, by instantly "folding" an ordinary unconstrained diffusion back into the domain. The natural scheme follows: simulate the easy unconstrained process, then fold. The project develops and tests such schemes.

**Applications.** Rank-based SPT models, queueing networks (reflected Brownian motion in an orthant is the classic heavy-traffic limit), and constrained sampling in ML, where reflected Langevin dynamics keep samples inside a bounded domain.

**Maths.** The Skorokhod problem and local time; Itô and Tanaka formulas; strong versus weak error for SDE schemes; convex geometry (projections and reflections across faces). Empirical work means convergence-rate studies on log–log plots, possibly with multilevel Monte Carlo.

**Risk.** Turning a new representation into a working scheme may only be tractable on simple domains first, such as an orthant or simplex. That still makes a complete dissertation.

**Fit.** Strong. It uses ST409 directly, has a guaranteed computational deliverable, and Monte Carlo simulation is core quant work that matches your NPL background. Being among the first to build on a July 2026 preprint gives you a ready-made niche.

## Giulia Livieri

The RL portfolio project fits you best of Livieri's three; it's also the vaguest, so its value depends on how you frame it.

Livieri works on high-frequency financial econometrics, ML for time series, and mean field games. Her three projects span three different toolkits.

### Project 1: Mean field games and mean field control for green finance

**What it asks.** A review of SDE models, mean field games (MFG) and mean field control (MFC), applied to green finance, with an optional policy simulation. The anchor paper is [Carmona, Dayanıklı and Laurière](https://arxiv.org/abs/2102.09434). Electricity producers trade off profitable but polluting fossil generation against uncertain wind and solar under a carbon tax. They compare competitive producers (Nash equilibrium, an MFG) with cooperating producers (social optimum, MFC), then add a regulator who sets the tax (a Stackelberg equilibrium).

**Maths.** Stochastic control, Hamilton–Jacobi–Bellman equations, the stochastic maximum principle, McKean–Vlasov dynamics, and forward–backward SDEs. The anchor paper proves [existence and uniqueness via FBSDE systems](https://www.biosino.org/nafldkb/article_details?id=28742). Numerics would use fictitious play or deep-learning solvers. ST409 is the stated prerequisite; the reference text (Carmona and Delarue) runs to two volumes.

**Risk.** As written it's mostly review plus simulation. Originality would come from a new policy scenario or regulator design. The theory ramp is steep for a summer.

### Project 2: Variable selection via variational Bayes

**What it asks.** Variational Bayes (VB) replaces an intractable posterior with the closest member of a simple family, measured by KL divergence. Its objective, the evidence lower bound (ELBO), approximates the log marginal likelihood, so it can rank models. The project reviews VB variable selection, possibly extends it, and implements it.

The main reference, [Ormerod, You and Müller (2017)](https://doi.org/10.1214%2F17-EJS1332), uses mean-field VB with a spike-and-slab prior. They show it selects the true model at an exponential rate in the sample size, faster than MCMC.

**Maths.** KL divergence and the ELBO, coordinate-ascent updates, spike-and-slab priors, consistency arguments for selection. ST451 covers the core.

**A natural research angle.** The ELBO sits below the log-evidence by exactly the KL gap. If that gap differs across candidate models, ranking by ELBO can be biased. Quantifying when this matters is a clean question.

**Risk.** Lowest of the three. Also the least distinctive: VB variable selection is an established literature.

### Project 3: RL-based parametric portfolio policies

**What it asks.** Parametric portfolio policies (Brandt, Santa-Clara and Valkanov, 2009) skip forecasting returns. They write portfolio weights directly as a function of stock characteristics and maximise investor utility. [Simon, Weibels and Zimmermann](https://pubsonline.informs.org/doi/10.1287/mnsc.2025.00721) (Management Science, 2026) replace the linear function with a neural network. They report 43–102 basis points higher monthly certainty-equivalent returns than linear policies. The project asks whether RL can solve the same problem.

**The framing that makes it work.** In the single-period version, the policy is already optimised directly, so RL adds little. RL earns its place with transaction costs, where today's weights shape tomorrow's turnover and the problem becomes genuinely sequential. Pitch it that way.

**Maths.** Policy-gradient methods and MDPs (ST455), expected utility and certainty equivalents, portfolio constraints. Mostly empirical, with some theory on when the RL and direct-optimisation solutions coincide.

**Data.** Characteristic-based equity data. The [Open Source Asset Pricing](https://pubsonline.informs.org/doi/references/10.1287/mnsc.2025.00721) signals (Chen and Zimmermann) are cited by the paper and freely available. Check with Livieri whether LSE gives you WRDS/CRSP access.

**Risk.** Backtests are noisy, and showing that RL genuinely beats the deep-policy benchmark out of sample is hard. Define success as a careful comparison, not as beating the benchmark.

**Fit.** The best of Livieri's three for you. It uses ST455, connects to quant hiring, and builds on your finance degree.

## Tengyao Wang

The conformal project is the safest strong option on the whole list; the high-dimensional nuisance project overlaps with econometrics you've already done.

Wang works on high-dimensional statistics, change-point detection and robust procedures, and is the MSc Financial Statistics programme director.

### Project 1: Conformal prediction under distribution shift

**What it asks.** Conformal prediction wraps any ML model in prediction intervals with exact finite-sample coverage, but only if the data are exchangeable. Deployment usually breaks that. The project reviews the fixes and compares them in simulation and on real data.

The two anchor papers:

- [Tibshirani et al. (NeurIPS 2019)](https://papers.nips.cc/paper/8522-conformal-prediction-under-covariate-shift) handle covariate shift by weighting calibration points by the likelihood ratio between test and training covariates. That ratio must be known or estimated, typically from unlabelled test covariates.
- [Barber, Candès, Ramdas and Tibshirani (Annals of Statistics, 2023)](https://projecteuclid.org/journals/annals-of-statistics/volume-51/issue-2/Conformal-prediction-beyond-exchangeability/10.1214/23-AOS2276.pdf) use weighted quantiles against drift and bound the coverage gap. Their methods recover the usual guarantees when data are exchangeable.

The brief also names doubly robust calibration and distributionally robust methods, and suggests extensions such as weight truncation.

**Maths.** The coverage proof is a short, elegant rank argument from exchangeability. Beyond that: weighted exchangeability, total variation distance, density-ratio estimation (often via a classifier), and semiparametric ideas for the doubly robust version. ST460 covers most of it; MA411 helps with the distances.

**Where to take it.** The base comparison is well-trodden, so the extension is where you'd be original. Two angles suit you. Drift over time connects to ST418 and to Barber et al.'s decaying weights. Abrupt shifts connect to Wang's own change-point expertise: should you re-weight smoothly, or detect the break and recalibrate?

**Applications.** Any deployed model facing a changing population, such as credit scoring as the applicant mix shifts, medical models moved between hospitals, or demand forecasts after a shock.

**Fit.** Very good. It matches the conformal and time series direction you started with, has a guaranteed core, and uncertainty under drift is directly valued in industry.

### Project 2: Estimating a target coefficient with high-dimensional nuisance

**What it asks.** In y = αz + βᵀx + ε with many controls x, you want inference on the single coefficient α. The Lasso biases it. The project compares three fixes in simulation (p < n, p ≫ n, correlated designs, heteroscedasticity): Robinson's partialling-out, the debiased Lasso of Zhang and Zhang, and [double/debiased machine learning](https://cemmap.ac.uk/publication/double-debiased-machine-learning-for-treatment-and-structural-parameters/). DML's two ingredients are Neyman-orthogonal scores, which make the estimate insensitive to errors in the nuisance fit, and cross-fitting.

**Maths.** Lasso theory (restricted eigenvalue conditions, oracle inequalities), asymptotic normality of debiased estimators, sample splitting. Solid graduate high-dimensional statistics.

**Risk.** A review-and-simulation project on well-established methods; originality is limited. You also said the causal-inference modules repeated your BSc econometrics, and DML sits close to that material.

**Fit.** Weaker for you. Choose it only if you want a structured route into high-dimensional theory.

## Andreas Søjmark

The unit-roots project is the hardest and most distinctive fit on the list; the epidemic project is a more balanced theory-plus-data option outside finance.

Søjmark works where stochastic analysis meets finance: systemic risk, mean-field limits and weak convergence. He is also your ST409 lecturer, so you'll see how he teaches before committing.

### Project 1: Unit roots and functional convergence of stochastic integrals

**What it asks.** The starting point is [Davis and Song (Annals of Statistics, 2011)](https://www.projecteuclid.org/euclid.aos/1327413778) on unit roots in moving-average models. A unit root in the MA polynomial is the signature of over-differencing, so testing for one is a test of invertibility. Their trick is to treat the initial value as an extra parameter, then integrate it out to recover the exact likelihood. That avoids diagonalising the covariance matrix and extends beyond MA(1). Their likelihood-ratio test is competitive with Tanaka's locally best test for some alternatives and dominates it for the rest.

The existing theory assumes finite variance, so the limits are driven by Brownian motion. The project asks what happens with heavy-tailed innovations, where the variance is infinite.

**Why it's hard, and why it's his.** With heavy tails, partial sums of moving averages converge only in Skorokhod's weaker M1 topology, not the usual J1. Søjmark and Wunderlich's [2024 paper on moving averages](https://arxiv.org/abs/2401.13543v2) shows that convergence of stochastic integrals can fail badly for strictly M1-convergent moving averages. They also identify natural integrand classes for which it still holds. The project would push that machinery into the likelihood asymptotics, jointly in time and in the parameters.

**Maths.** Weak convergence on metric spaces (tightness, continuous mapping, argmax theorems), Skorokhod space with its J1 and M1 topologies, stochastic integration, and stable laws and Lévy processes. MA411 gives the weak convergence, ST409 the stochastic integrals, ST460 the likelihood asymptotics and ST418 the unit-root setting. The function-space topology is exactly where your point-set topology self-study pays off.

**Risk.** Research-level and proof-driven; the heavy-tailed result may not close by August. A good fallback is a rigorous exposition of Davis and Song, simulations showing the non-standard heavy-tailed limits, and a partial result. Agree that fallback with him up front.

**Fit.** The strongest PhD signal on the list, and the only project that uses every one of your core modules. Industry value is indirect: rigorous econometrics, but a niche topic.

### Project 2: Epidemic models with diffusive heterogeneity

**What it asks.** Classical SIR models give everyone the same contact rate. [Berestycki, Desjardins, Weitz and Oury (2023)](https://centreborelli.ens-paris-saclay.fr/en/node/2968) instead let individual exposure risk vary and change over time. The result is a reaction–diffusion system, with a Fokker–Planck-type equation describing how behaviour changes during and between epidemics. Such models reproduce [plateaus, shoulders and rebounds](https://ias.hkust.edu.hk/events/modelling-the-propagation-of-epidemics-with-diffusion) like those seen in Covid-19 data.

The project first lays out the theory at two levels: individuals as interacting SDEs, and the PDEs that arise as large-population limits. It then calibrates the models to past epidemic data and compares them. Optional extensions are modelling interventions or asking whether parameters are identifiable from aggregate infection counts.

**Maths.** SDEs and Fokker–Planck equations, reaction–diffusion PDEs, mean-field limits, numerical PDE schemes, and likelihood-based or simulation-based calibration. ST409 is ideal; some ODE/PDE background helps; Python is required.

**Risk.** Moderate. Calibration to noisy aggregate data can be fiddly, but there is always a deliverable.

**Fit.** Good balance of theory and data, and the identifiability question is genuinely statistical. It's further from finance and your stated interests than the other projects.

## Zoltán Szabó

Spectral distribution regression is the more tractable of Szabó's two; the minimax project is pure theory built on functional analysis that none of your modules teach.

Szabó works on kernel methods, information-theoretic estimators and learning theory, and directs the MSc Data Science. Both projects rest on one idea: embed a probability distribution as a single point (its *mean embedding*) in a reproducing kernel Hilbert space (RKHS), then do geometry there.

### Project 1: Minimax estimation of kernel information-theoretic measures

**What it asks.** Kernel measures compare distributions: MMD for two-sample testing, HSIC for independence, KSD for goodness of fit. The question is the fastest rate at which any estimator can recover them. [Kalinke and Szabó (NeurIPS 2024)](https://proceedings.neurips.cc/paper_files/paper/2024/hash/c43bade4b146231b0149da3b9e7e286e-Abstract.html) settled HSIC on ℝ^d: the minimax rate is n^(−1/2) for continuous, bounded, translation-invariant characteristic kernels. That makes the standard U-statistic, V-statistic and Nyström estimators optimal. Their slides list [lower bounds beyond ℝ^d as open](https://neurips.cc/media/neurips-2024/Slides/95630_sxHxZ71.pdf).

The project asks you to relax the translation-invariance assumption, or extend the results to newer measures: kernel Lancaster and Streitberg interactions, and kernel cumulants.

**Maths.** RKHS theory and characteristic kernels; Bochner's theorem (the Fourier description of translation-invariant kernels); Hilbert–Schmidt operators and tensor products; and minimax lower bounds via Le Cam's two-point method and divergences between Gaussians (Tsybakov, chapter 2). MA411 helps; the functional analysis is self-study.

**Risk.** High. Relaxing translation invariance removes the Fourier tool the existing proof relies on. A more realistic MSc target is reusing the existing proof template for a new measure, such as the Lancaster interaction under the same assumptions. Ask Szabó which he'd accept.

### Project 2: Spectral distribution regression

**What it asks.** In distribution regression the inputs are distributions, observed only as bags of samples. Szabó and coauthors' [JMLR paper (2016)](https://www.jmlr.org/papers/v17/14-510.html) showed that a simple pipeline works: embed each bag, then run ridge regression. It is consistent in this two-stage sampled setting, matches the one-stage minimax rate, and settled a 17-year-old open question about set kernels. Applications include multi-instance learning, entropy estimation and [aerosol prediction from multispectral satellite images](https://discovery.ucl.ac.uk/id/eprint/1469659/).

The bottleneck is cost: these methods scale cubically in the number of bags. Spectral algorithms generalise ridge regression to a family that includes gradient descent and spectral cut-off. They often adapt better and use less memory. The project studies their computational and statistical properties for distribution regression.

**Maths.** Kernel ridge regression theory, integral operators and spectral calculus, source and capacity conditions, and learning-rate proofs. A natural structure: implement several spectral methods, map the compute–accuracy trade-off, then prove a rate for one method by adapting existing analyses to two-stage sampling.

**A finance angle (my suggestion).** Each trading day is a bag of intraday returns, and the target is next-day realised volatility. That gives a real-data application close to your interests.

**Risk.** Moderate. There's a guaranteed computational deliverable, and the theory can be scoped to one algorithm.

**Fit.** Good if you want ML theory with a computational safety net. Industry relevance is modest, since kernel methods are less common in industry than deep learning, but it's strong PhD preparation.

## Milan Vojnović

The leaderboard project is the better fit for you: AI evaluation, accessible data, moderate theory and no GPUs. The multicalibration project is more proof-heavy, but it connects most directly to his current Meta collaborators.

**Who he is.** Vojnović is Professor and Head of Department. He spent 13 years at Microsoft Research and has held a [visiting scientist position at Meta](https://www.lse.ac.uk/statistics/research/data-science). His work spans multi-armed bandits, multi-agent systems, algorithms under uncertainty and game theory, and he wrote *Contest Theory* (Cambridge, 2016).

Two recent papers show where his head is:

- He co-authored [MCGrad: Multicalibration at Web Scale](https://arxiv.org/abs/2509.19884) with Meta's London team. MCGrad has been in production at Meta and is now part of hundreds of production models. That is the industrial version of his multicalibration project.
- With Se-Young Yun he wrote [What is the Alignment Objective of GRPO?](https://arxiv.org/pdf/2502.18548). It shows that GRPO aggregates preferences differently from the logarithmic pooling implemented by RLHF. That is the theoretical root of his leaderboard project.

### Project 1: What does a human-preference leaderboard actually rank?

**What it asks.** Chatbot Arena (now LMArena) pools pairwise votes from a self-selected crowd into one Bradley–Terry score per model. If voters disagree, that ranking may match no actual group of users, and it may depend on which pairs happened to be shown. The project has four parts:

1. Characterise what the pooled ranking estimates under voter heterogeneity.
2. Bound how a model's rank could change under different or uncertain user mixes.
3. Build confidence statements of the form "A ranks above B for every plausible user mix".
4. Check the methods by simulation, on public leaderboard votes segmented by language and prompt type, and on a dataset where voter groups are known (such as PRISM).

**The research frontier.** The field is moving fast, and the evidence that something is wrong is striking:

- [Huang, Shen, Wei and Broderick](https://arxiv.org/abs/2508.11847v2) found that dropping just 0.003% of human preferences can change the top-ranked model on Chatbot Arena.
- [Haghtalab, Procaccia and coauthors (ICML 2026)](https://icml.cc/virtual/2026/poster/62053) argue that a single Bradley–Terry score is incompatible with heterogeneous preferences. They propose a social-choice fix and show standard aggregation violates stability on LMArena data.
- A 2026 study found individual users' [Bradley–Terry rankings had a mean Spearman correlation of 0.043](https://arxiv.org/pdf/2604.18943) with the global ranking, statistically indistinguishable from random.
- [DMLRank (ICML 2026)](https://mcml.ai/publications/fds+26/) offers nonparametric, debiased-ML estimates of ranking scores.

Vojnović's angle is distinct from all of these. Rather than a new mechanism or a more efficient estimator, he asks which ranking claims are *identified* and robust across populations: a partial-identification question.

**Maths.** Likelihood theory under misspecification: the fitted Bradley–Terry parameter is the KL projection of the true preference mixture, the same idea underlying VRPO. Mixture models, bounds optimised over sets of user mixes (often linear programmes), simultaneous confidence statements, and a little social choice theory (Condorcet cycles). ST460 is the core. Coding is moderate, on public vote data, with no GPUs.

**Risk.** Moderate. The field is crowded, so keep the identification framing central to stay distinct. There's always a deliverable: the characterisation, simulations and an empirical analysis stand even if the sharpest bounds don't.

**Fit.** Excellent. It sits in the same Bradley–Terry family as Shi's projects and the department's wider preference-data cluster. It speaks directly to your interest in evaluating AI systems, and "how do you rank models you can't fully trust users to agree on?" is a live question at every AI lab.

### Project 2: Valid confidence intervals for multicalibration error

**What it asks.** A model is multicalibrated if its probabilities are accurate within every subgroup in a large, overlapping collection: among cases given 70%, about 70% should occur, in each group. The summary statistic is the worst calibration gap across groups and probability bands, restricted to groups above a minimum size. Because the worst group is chosen with the same data that measure it, the estimate is biased upwards, and a naive interval undercovers.

Two existing tools bracket the problem. [Cherian and Candès (JMLR 2024)](https://www.jmlr.org/papers/v25/23-0739.html) use the bootstrap to bound performance over all groups simultaneously, which is valid but conservative. Econometric "intersection bounds" give inference on the maximum of many estimated quantities. The project asks how much shorter than the all-groups interval you can go by exploiting the max structure and the nesting and overlap of groups, while keeping coverage. The outcome is a single result either way: a shorter interval with a coverage proof, or a proof that no valid interval is substantially shorter.

**Maths.** Gaussian approximation and the multiplier bootstrap for maxima of many statistics, selective inference (the winner's curse), multiple testing, and moment-inequality inference. For an impossibility result, lower-bound arguments. Meta's calibration work uses metrics built on the classical [Kuiper statistic](https://papers.cool/arxiv/2506.11251), weighted by each subgroup's signal-to-noise ratio. ST460 is essential; MA411's weak convergence helps.

**Risk.** Higher. It's proof-driven, and the outcome depends on whether the max structure buys real width. The "either a better interval or an impossibility proof" framing is well designed, though: both outcomes count.

**Fit.** Strong on rigour, and the most direct line to Meta's London team, whose multicalibration work is on the reading list. It also maps onto lending: credit models must be calibrated within customer segments, not just overall.

### On the tech connection

The link is real. His Meta collaborators are London-based, and MCGrad shows they turn research into production. Still, treat it as a possible upside, not a reason to choose. Pitch him on the research. A strong dissertation is what makes an introduction plausible. As Head of Department he will also have limited time, so ask early how many students he's taking and whether a PhD student or postdoc helps supervise.

## Oliver Feng

Both of Feng's projects suit you. The external-predictions project is the industry-friendly one, with low compute and the same statistical idea as Shi's semi-supervised work. The diffusion project is the best bridge on the list between ST409 and generative AI.

**Who he is.** Feng is an Assistant Professor, previously a lecturer at Bath, with a PhD and postdoc at Cambridge. His work [has a nonparametric flavour](https://www.lse.ac.uk/statistics/research/time-series-and-statistical-learning), with emphasis on robustness to outliers and model misspecification, and he is exploring score matching and its links to convex optimisation. His paper with Kao, Xu and Samworth, [Optimal convex M-estimation via score matching](https://arxiv.org/abs/2403.16688), builds a data-driven convex loss for regression via a log-concave projection in Fisher divergence. For Cauchy errors it reaches over 87% of the efficiency of the oracle MLE. That paper is the thread connecting his two projects: one is about making estimators efficient, the other about score matching.

As a recent arrival he may have more supervision capacity than established staff, but ask.

### Project 1: Improving statistical inference using external predictions

**What it asks.** Labels are expensive, but a black-box model can predict them cheaply on a much larger unlabelled set. How do you combine a small labelled set with those predictions to sharpen estimation and inference, even when the predictions are poor and can't simply be plugged in? Starting from a literature review, you compare or modify existing methods theoretically or empirically, or refine them for a specific application area.

**The landscape.** Three strands are on his reading list:

- **Prediction-powered inference** (Angelopoulos et al., *Science* 2023) uses the labelled set to debias the predictions.
- **[Prediction aided by surrogate training](https://www.arxiv.org/abs/2412.09364)** (Xia and Wainwright) uses helper covariates available only at training time. It fits a response estimator on the labelled data, then trains the final predictor on pseudo-responses for the full dataset.
- **[CARE](https://talks.cam.ac.uk/talk/index/235123)** upgrades existing clinical survival models with new data by taking a convex combination of a new kernel estimator and the external models. It achieves a rate at least as good as both the best kernel estimator and the best external model.

The unifying theory is the semiparametric framework covered in the Shi discussion: unlabelled data or external predictions can only help when the target parameter isn't well specified.

**Maths.** M- and Z-estimation, influence functions, control variates and semiparametric efficiency for the PPI strand. RKHS estimators and oracle inequalities for aggregation in the CARE strand. ST460 is the core.

**A natural application for you.** CARE's setting is a lender's everyday problem. A bank has an existing scorecard or bureau score (the external predictor) and a small labelled dataset for a new product or segment (the new data). "Upgrading a credit model without discarding the old one" is a well-posed project on public data, and it sits close to what you saw at iwoca.

**Risk.** Low to moderate. The PPI area is busy, but this brief is deliberately open, and a careful comparison plus one modification makes a solid dissertation. No GPUs needed.

**Fit.** Very good. It's the statistical core of Shi's semi-supervised project, without the LLM training burden.

### Project 2: Score-based generative modelling with diffusion processes

**What it asks.** Diffusion models add noise to data step by step, learn the *score* (the gradient of the log-density) of the noisy data, then run a reverse-time SDE to turn pure noise into new samples. The project starts with a detailed mathematical exposition, including score matching. You then choose a direction:

- apply or adapt the method to a generative task of your choice;
- extend score matching to other data domains;
- survey and extend recent results on convergence and sample accuracy.

**The research frontier.** Two results anchor the theory:

- [Chen, Chewi and coauthors](https://arxiv.org/abs/2209.11215v3) showed that with an L²-accurate score estimate, diffusion models can sample efficiently from essentially any realistic distribution, with polynomial dependence on all problem parameters. The proof is a [clever application of Girsanov's theorem](https://web.tcs.tifr.res.in/web/events/1544).
- [Dou, Kotekal, Xu and Zhou](https://arxiv.org/abs/2409.07032v1) pinned down the sharp minimax rate of score estimation for Hölder densities. They showed the resulting diffusion sampler is minimax-optimal in total variation, without the extra log factors or early stopping that earlier work needed.

**Maths.** Itô calculus, Fokker–Planck equations, time reversal of diffusions, Girsanov's theorem, score matching and nonparametric rates. ST409 covers the stochastic calculus, and Girsanov is in the ST409 notes you already have. An applied direction adds PyTorch, but small-scale experiments (2-D data, tabular data, time series) run on a single GPU or a laptop.

**A finance angle (my suggestion).** Generating realistic synthetic return paths for stress testing and scenario analysis. Fat tails and volatility clustering are a demanding test of whether a diffusion model has really learned the distribution.

**Risk.** Moderate. An exposition-only dissertation is safe but unremarkable. Agree early on which extension (an application, a new domain or a convergence result) carries the original contribution.

**Fit.** Strong. It's the only listed project that uses ST409's stochastic calculus to explain a central tool of modern AI, which reads well to both ML employers and PhD committees.

## Comparison and shortlist

Given an industry lean with a PhD kept open, email three people this week: Shi (VRPO), Itkin (reflected SDE simulation) and Wang (conformal under shift). Keep Søjmark's unit-roots project as the stretch option if ST409 hooks you.

The three cover one engineering-heavy ML project, one stochastic-analysis-with-computation project and one statistical-methods project. Each has a guaranteed core.

| Project | Supervisor | Kind | Modules it uses | Risk | Industry value | PhD signal |
| --- | --- | --- | --- | --- | --- | --- |
| Variance-reduced alignment (VRPO) | Shi | Engineering-heavy | ST455, ST460 | Medium | High | High |
| What a preference leaderboard ranks | Vojnović | Theory + data | ST460 | Medium | High | High |
| Inference with external predictions | Feng | Method + experiments | ST460 | Low–medium | High | Medium–high |
| Score-based diffusion models | Feng | Theory + experiments | ST409, ST460 | Medium | Medium–high | High |
| Reflected SDE simulation | Itkin | Method + experiments | ST409 | Medium | High | Medium–high |
| Conformal under distribution shift | Wang | Method + experiments | ST460, ST418 | Low | High | Medium |
| Multicalibration confidence intervals | Vojnović | Proof-driven | ST460, MA411 | Medium–high | Medium–high | High |
| Unit roots and functional convergence | Søjmark | Proof-driven | MA411, ST409, ST460, ST418 | High | Low–medium | Very high |
| RL parametric portfolio policies | Livieri | Method + experiments | ST455 | Medium | High | Medium |
| Semi-supervised RLHF | Shi | Engineering + theory | ST455, ST460 | High (crowded field) | High | High |
| Spectral distribution regression | Szabó | Method + theory | ST460, MA411 | Medium | Low–medium | High |
| Boundary attainment | Itkin | Proof-driven | ST409, MA411 | High | Low | High |
| Epidemics with diffusive heterogeneity | Søjmark | Theory + data | ST409 | Medium | Low | Medium |
| Minimax kernel measures | Szabó | Proof-driven | MA411 | High | Low | High |
| Mean field games for green finance | Livieri | Review + simulation | ST409 | Medium | Low–medium | Medium |
| VB variable selection | Livieri | Review + method | ST451 | Low | Medium | Low |
| High-dimensional nuisance | Wang | Review + simulation | ST460 | Low | Medium | Low |

### Questions to bring to each meeting

- **Shi:** GPU access for MSc students; which project he'd prioritise given ABC-Align; whether a combined "safe VRPO" project is acceptable; whether a PhD student would co-supervise.
- **Itkin:** which domains the folding scheme is tractable on; whether any code exists; what counts as success if only simple domains work.
- **Wang:** whether a time-series or change-point extension is welcome; how many students he's taking.
- **Søjmark:** the agreed fallback if the heavy-tailed result doesn't close; how much functional analysis to learn first.
- **Livieri:** data access (WRDS/CRSP); whether the multi-period, transaction-cost framing fits her intent.
- **Szabó:** which extension he'd accept as an MSc target; essential prior reading.
