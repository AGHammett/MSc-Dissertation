# Variance-reduced Alignment for Large Language Models: Plain summary

**Supervisor:** Dr Chengchun Shi

## 1. The domain

Large language models (LLMs) are first *pre-trained* to predict the next word on huge amounts of text. That makes them fluent, but not necessarily helpful or safe. A second stage, *alignment*, nudges the model towards answers people prefer. The dominant method is **reinforcement learning from human feedback (RLHF)**. People see a prompt and two candidate answers and say which they prefer, and the model is tuned to give more answers like the preferred ones. A penalty stops it drifting too far from its starting model, which is called the *reference policy*. The field sits where statistics (learning from noisy comparisons) meets machine learning (training huge neural networks).

## 2. The problem

Nearly all RLHF methods assume the **Bradley–Terry model**. Each answer has a hidden quality score (a *reward*), and the chance that A beats B depends only on the score difference, much like a logistic regression. Real preferences are messier. They can be non-transitive (A beats B, B beats C, yet C beats A), they depend on context, and they are noisy: in one supplied paper, labellers agree only about 73% of the time. When the assumed model is wrong ("misspecified"), the estimates are noisier and the tuned model ends up worse than it could be. The question is how to get more out of the same data without abandoning the simple, cheap methods everyone uses.

## 3. What's been done

- **InstructGPT (Ouyang et al., 2022).** OpenAI's standard three-step recipe: fine-tune on human-written answers, fit a reward model to human comparisons, then optimise the model against that reward with a reinforcement-learning algorithm (PPO). A small model tuned this way was preferred to one 100 times its size.
- **DPO (Rafailov et al., 2023).** A mathematical shortcut that skips the reward model and the reinforcement learning. The model is trained directly with a classification-style loss. It is much cheaper and at least as good at the sizes tested, but it still assumes Bradley–Terry.
- **VRPO (Ye, Zhou, Zhu, Quinzan and Shi, 2025).** This is the supervisor's paper and the centrepiece. Because the reference policy is usually known, you can generate unlimited extra *unlabelled* answer pairs. VRPO trains a second, more flexible preference model and uses it, with those extra pairs, to add correction terms to the usual loss. The corrections cancel on average but soak up much of the noise. I read it as a "control variate", the same trick used in Monte Carlo simulation. The paper proves this lowers the variance of the estimates, and the gap to the best policy, under misspecification. As judged by GPT, its answers beat nine competing methods 53–98% of the time. The gains were smaller when the reference policy was not known exactly.

## 4. What the project would do

The brief has two goals:
- **Make VRPO cheaper and more statistically efficient.** VRPO costs more than DPO: it needs extra generated answers and a second model. I think natural angles are caching parts of the computation, using a lighter helper model, and measuring the cost-benefit trade-off. Statistically, the paper uses only one extra pair per prompt and a fixed weight on the correction, so using more pairs, choosing the weight from the data, or training the helper model on a separate data split are obvious things to try, and possibly to prove things about.
- **Apply it to UltraFeedback.** The brief describes this dataset as larger and with more complex answers. None of the supplied papers discusses it, so an early task is finding out how its answers were generated. That matters because VRPO relies on knowing the reference policy.

## 5. What working on it would feel like

The brief says outright that the project is coding intensive. My rough guess at the split:
- about 60% coding and GPU experiments;
- about 15% evaluation and data wrangling;
- about 15% statistical theory;
- about 10% writing.

A typical week: adapt the released VRPO code, launch fine-tuning jobs for a model with one to two billion parameters on a university GPU cluster, fix memory errors, generate answers, have an automated judge (an LLM asked which of two answers is better) score them, and check whether the predicted variance reduction appears. Some weeks will feel like MSc statistics: working through estimation arguments or a cheap simulation where the truth is known. Access to GPUs will shape the project more than anything else, so settle it first.
