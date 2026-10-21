# What Does a Human-Preference Leaderboard Actually Rank?: Plain summary

**Supervisor:** Professor Milan Vojnović

## 1. The domain

This project is about how AI chatbots, or large language models (LLMs), get evaluated and compared. Simple test sets with right answers do not capture what people actually want from a chatbot. Popular "leaderboards" like Chatbot Arena (now LMArena) do something else instead. A user types a question, sees answers from two anonymous models side by side, and votes for the better one, or for a tie. Hundreds of thousands of such votes are combined into one score per model, and the scores give a ranking. Companies and researchers use these rankings to decide which models to build on or adopt. The statistics underneath are old: the Bradley–Terry model, a logistic model for "who beats whom" that is used for sports and chess ratings.

## 2. The problem

The voters are a self-selected crowd, mostly tech enthusiasts according to the Arena authors themselves. They also disagree with each other: one group may prefer short, direct answers on coding questions, another long, careful answers on personal topics. Pooling everyone into one number hides this. The pooled ranking might not match what *any* particular group of users would conclude. It can also depend on which pairs of models happened to be shown to which users. Nobody has worked out clearly what the pooled score is a measure *of* in that situation. It is also unclear which ranking claims ("model A is better than model B") would still hold for a different population of users, say a company's own customers.

## 3. What's been done

- **Chatbot Arena paper.** Describes the platform, the data (about 240,000 votes, over 100 languages) and the statistics: a Bradley–Terry fit with "robust" standard errors, plus confidence intervals for ranks. It admits the user base may be unrepresentative, but treats all voters as one population.
- **Ameli and co-authors.** Improve the statistical model on the same data: better handling of ties, correlations between models, and fixes for estimation problems. They show that the middle of the ranking shifts with modelling choices. Voter differences are still ignored.
- **Distributional Preference Learning paper.** Proves the key theoretical fact for this project. When the people giving preferences differ in ways the model cannot see, a pooled Bradley–Terry fit ranks items by their average chance of beating a randomly chosen rival (a voting rule called the Borda count). This can disagree with what people value on average.
- **PRISM dataset paper.** Collects ratings from 1,500 people in 75 countries whose demographics are recorded. It shows that rankings move by several places depending on who is rating and on what kind of conversation they are having. This is the "known groups" dataset the brief mentions, and it is publicly downloadable.
- **Frauen and co-authors.** A modern framework for defining a ranking score flexibly and getting valid confidence intervals for it, even when machine-learning models are used along the way. They list "bounds" on rankings, for when assumptions are weakened, as future work.

## 4. What the project would do

The brief asks for three things. First, work out mathematically what the pooled leaderboard score actually estimates when users come from several groups with different tastes. Second, find out how far a model's rank could move if the mix of users were different or uncertain, for example if there were more non-English speakers or more coding questions. Third, build confidence statements of the form "A beats B no matter which plausible mix of users you assume". All three would be checked by simulation, then applied to publicly released Arena votes, splitting them by language and type of question. Finally, they would be tested on PRISM, where the real groups are known. I think a central early decision is how to define the set of "plausible mixes", since every result depends on it. Another is whether question type and language should count as user groups, given that they are really properties of the question rather than of the voter.

## 5. What working on it would feel like

I would guess roughly 35–40% theory, 25% simulation coding and 35–40% real-data work. A typical week early on might mean deriving what a mis-specified likelihood converges to and checking it on small examples. Later weeks would go on coding simulations in Python or R, setting up optimisation over user mixes, and wrangling the Arena and PRISM data files. Nothing needs heavy computing: everything should run on a laptop. The mathematics is mostly maximum likelihood, convexity and confidence regions, which builds on familiar material. The newer pieces are some social-choice ideas and optimising over sets of weights.
