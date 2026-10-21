# Semi-supervised Reinforcement Learning from Human Feedback for LLM Fine-tuning: Plain summary

**Supervisor:** Dr Chengchun Shi

## 1. The domain

Large language models (LLMs) such as ChatGPT are trained in two stages. First they read huge amounts of text and learn to predict the next word ("pre-training"). Then they are adjusted to behave helpfully and safely ("post-training" or "alignment"). The most common alignment method is *reinforcement learning from human feedback* (RLHF). The model writes two answers to a prompt, a person says which one is better, and the model is nudged towards the kind of answer people prefer. Statistically, the core is a logistic-regression-like model (the *Bradley–Terry model*): the chance that one answer beats another depends on the difference in their hidden "reward" scores.

## 2. The problem

Human preference labels are slow and expensive. In the OpenAI paper supplied, most comparisons were judged by a single contractor, and raters agreed with each other only about 73% of the time. So the labelled data are small and noisy, and the fitted reward or policy can have high variance. Meanwhile, *unlabelled* data (extra model-generated answers, or prompts nobody has rated) are cheap. Statisticians have a toolkit for exactly this situation, called *semi-supervised learning*, but the brief says it has rarely been used in RLHF.

## 3. What's been done

- **InstructGPT (OpenAI, 2022)** set out the standard three-step recipe: imitate good human answers, fit a reward model to human rankings, then optimise the model against that reward with an RL algorithm.
- **DPO (Stanford, 2023)** showed that the last two steps can be merged into one loss function that looks like logistic regression, which makes training far simpler. Its authors list using unlabelled prompts as future work.
- **Prediction-powered inference (Science, 2023; the short journal version)** shows how to combine a few true labels with many machine-learning predictions. You use the predictions on the unlabelled data, then use the labelled data to measure and correct their errors, so the conclusions stay valid while confidence intervals shrink.
- **Xu, Witten and Shojaie (2025)** give the general theory of when unlabelled data can help. A key message is that if the statistical model is exactly right, unlabelled data give no gain; the gains come when the model is misspecified. They also build "safe" estimators that never do worse than ignoring the unlabelled data.
- **VRPO (2025, with Dr Shi as corresponding author)** applies these ideas to RLHF. Real human preferences don't follow the Bradley–Terry model exactly, so VRPO adds a correction term built from a more flexible preference model and from freshly generated, unlabelled answers. The paper proves this lowers variance under misspecification. In experiments with small open models (0.5 to 1.5 billion parameters) its answers were preferred over standard DPO's roughly 80% of the time. The paper itself calls this a semi-supervised approach and says no earlier work had done it.

## 4. What the project would do

I think the project is best seen as the next step after VRPO. Concretely, it could:

- **Make VRPO "safe".** VRPO's correction is fixed. Estimating its weight from the data, as in Xu et al., would guarantee it never does worse than the base method, even when the helper model is poor.
- **Use different unlabelled data.** Add many unrated prompts rather than just extra answers to rated prompts, or use a strong AI judge's labels as cheap "predictions", in the style of prediction-powered inference.
- **Show the effect on real models.** Do this both in a controlled set-up where the true reward is known (movie-review sentiment) and on real preference datasets, measuring how many human labels are saved.

The supervisor would need to decide which of these to pursue, and how much theory is expected.

## 5. What working on it would feel like

The brief calls the project coding-intensive and aims at a publishable paper. I would guess the split is about **55% coding and experiments, 25% reading and theory, and 20% writing**. The theory is mostly classical large-sample arguments (Taylor expansions, the central limit theorem, comparing variances), which builds on this term's inference module. The heavy lifting is engineering. You would work in Python with PyTorch and Hugging Face libraries, fine-tune language models on university GPUs, and manage many runs across random seeds and dataset sizes.

A typical week: debug a training script, launch a batch of GPU jobs, check a variance calculation on a small simulated example, read off reward curves or AI-judged win rates, and meet briefly to plan the next experiment. Expect waiting on jobs and early software frustration. The supplied papers report model sizes but not GPU hours, so compute access is something to settle in the first meeting.
