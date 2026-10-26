# What past ST499 dissertations tell us about the bar

**Prepared:** 22 October 2026 · **Sources:** the 15 dissertations in this folder (8 Distinction, one of them the 2023–24 Winton Prize winner, and 7 Merit), with one structured profile per dissertation in `Profiles/`.

> **Labels.** **[Observed]** comes from the dissertations or their profiles. **[Interpretation]** is my reading. We see the grades but not the markers' feedback, so every "why" is interpretation.

## How this was done

- Each dissertation was profiled **blind** by a separate reviewer. Each reviewer saw an anonymised PDF, not the filename, read the whole text, rendered a few pages to judge presentation, and scored it on a fixed rubric before guessing the grade.
- I then compared the 15 profiles, and read three dissertations myself: the prize winner (D10), D01 (a Vojnovic-supervised distinction) and D08 (a merit).
- **Caveats.**
  - 15 examples is a small sample, and they cover two cohorts (2023–24 and 2024–25), many supervisors and very different topics.
  - The examples may be self-selected, since students who share their dissertation may differ from those who don't.
  - Some PDFs may not be the exact submitted version.
  - The reviewers are AI models, not LSE markers.

## The headline finding: forensic reading can't tell the bands apart

| | Distinctions (8) | Merits (7) |
|---|---|---|
| Mean blind mark | 62.8 | 61.6 |
| Blind estimate | **all 8 rated Merit** | 6 Merit, 1 Pass |
| Main-body length (mean) | ~11,100 words | ~9,900 words |
| Rigour score (1–5) | 1.9 | 2.0 |
| Writing score | 3.4 | 2.7 |
| Literature review score | 3.1 | 2.7 |
| Originality score | 3.0 | 2.7 |

**[Observed]**
- The blind reviewers marked every distinction as a merit. The prize winner was rated around 60, among the lowest of the 15.
- Every dissertation in both bands contains substantive errors. Examples:
  - a misdefined Sharpe ratio and a literal placeholder citation ("IEEE Transactions on Something") in the prize winner;
  - impossible simulation output (bias of 10⁻¹⁶ alongside 100% coverage) in D14;
  - a wrong acceptance ratio in D15's sampler;
  - tables that contradict each other in D06.
- Distinctions and merits differ most on **writing**, then the **literature review**, then **originality**. Rigour, as a statistician would judge it, barely differs.

**[Interpretation]** Three things follow:
1. **Markers grade more generously, and on different things, than a line-by-line reviewer.** They seem to reward a clear question, a complete piece of work, a coherent story and evident effort. They penalise errors far less than you might fear.
2. **A distinction doesn't require perfection.** This is reassuring.
3. **Rigour is the clearest way to stand out above the field.** Hardly anyone in the sample does it well, so careful work beats all 15 on the dimension the reviewers criticised most. If the prize goes to the top of the cohort, that's a cheap edge.

## What the distinctions seem to share

These are **[Interpretation]** patterns from the 15 profiles, ordered by how consistent they are.

1. **Delivering everything the introduction promises.** Every distinction finishes what it sets out to do. The merits more often promise and don't deliver:
   - D08 proposes three "new tests" but evaluates one;
   - D09 promises six architectures, a baseline and a "corrected proof", none of which appear;
   - D13's simulation can't test its own claim.

   Unmet promises invite the marker to check every other claim. D11, a merit, presents its supervisor's method as its own.
2. **A clear, well-posed question and a coherent narrative.** Writing quality is the biggest score gap. The merit at the bottom of the writing scores (D07) is also the shortest (about 6,500 words) and has weak English.
3. **Substantial working implementation.** Examples:
   - D01 trains a real LLM with RL using an LLM judge, over 5 seeds;
   - D10 builds a replay of real order-book (LOB) data plus a simulated market, and trains 7 agents;
   - D14 runs 27 settings × 5 estimators × 2,000 replications;
   - D05 writes its own EM implementation with a pooled extension.

   **Scale and completeness seem to carry real weight.**
4. **One modest idea of the student's own.** The idea is usually small but clearly stated:
   - MUBPO's marginal-utility advantage (D01);
   - the dynamic-weights schedule (D10);
   - a draws-based variance (D14);
   - a pooled two-list estimator (D05);
   - a volatility-input kernel (D06).

   **None of the 15 proves a new theorem.** Theory is restated from the literature throughout.
5. **Honesty about limitations and negative results.** D02 reports that its baseline beats its Transformer. D04 and D12 have candid limitations sections. Distinctions overclaim too (D01, D04, D10), so honesty isn't decisive on its own, but it appears in most of the stronger work.

## The prize winner (D10)

**[Observed]** The prize winner applies deep RL (DQN and A2C) to market making, adding behaviour cloning from an "oracle" expert and a heuristic weight schedule, tested on real Nasdaq order-book data and a simulated market. It is ambitious, complete and clearly structured, in a topical area.

Read as a statistics paper, it is weak:
- the Sharpe ratio is divided by the variance rather than the standard deviation;
- there are no seeds, confidence intervals or tests, and the differences between models are tiny (1.95 vs 1.97);
- the expert uses future prices, which isn't discussed;
- there's a placeholder reference, a duplicated table header and typos ("INDV" for NVDA);
- it promises code in an appendix that doesn't exist.

**[Interpretation]** I can't tell how the Winton Prize is decided: highest mark, a separate panel, relevance to the sponsor (Winton is a quantitative investment firm), or something else. Ask the department. Don't model your dissertation on this one: it shows that ambition and completeness can be rewarded despite the flaws, not that the flaws don't matter.

## Two examples close to your shortlist

- **D01, *Aggregating Preferences for AI Alignment* (Distinction, supervised by Vojnović, 2024–25).** **[Observed]** It proposes a GRPO variant and runs real fine-tuning on Qwen2-0.5B, with Gemini as the reward judge, using departmental compute and 5 seeds. It reports honestly that its +1% gain isn't statistically significant. **[Interpretation]** Vojnović supervises method-plus-LLM-experiment projects, and a 0.5B model is feasible within an MSc. This is a useful reference point for Shi P2 and for Vojnovic P2.
- **D08, *Multivariate Ranks via Optimal Transport* (Merit, supervised by "Prof. Wang").** **[Observed]** Its acknowledgements say the student is starting a PhD with that supervisor. **[Interpretation]** Most likely this is Tengyao Wang, but the text doesn't confirm it. Either way, it's evidence that a Merit dissertation doesn't block a PhD when grades and references are strong. Its weaknesses are classic merit ones: three tests proposed but one evaluated, average p-values from 10–50 replications, and a placeholder code link.

## What this means for your projects

**[Interpretation]**

| Project | What a distinction looks like, judged against this sample |
|---|---|
| **Wang** | A systematic comparison like D14 or D06, both distinctions: a clear simulation design across the brief's factors (shift severity, n, heteroscedasticity, overlap) plus one or two real datasets, and one small idea of your own, such as a weight-truncation rule. Proper Monte Carlo hygiene would put it above everything here on rigour. |
| **Feng P1** | Compare PPI against PAST or CARE-style estimators on simulations and a real application, such as LLM-generated labels or lending, plus one modification. Same shape as D05 and D14. |
| **Vojnovic P1** | Even the reduced-risk version (a fixed number of groups, a coverage-valid interval, and simulations against simultaneous bounds and sample splitting) involves **more theory than any dissertation in this sample**. The "single theorem or nothing" fear is overstated if Vojnović accepts that version. |
| **Shi P2** | Like D01: a modification to VRPO, with experiments across seeds and confidence intervals on a small model. The rigour points below would set it apart. |

## A checklist from the 15 profiles

These came up again and again as weaknesses, in both bands.

1. **Cross-check every number.** Text against tables, tables against each other, and every value against its definition: a bounded metric stays within its bounds, RMSE² = bias² + variance, and coverage near the nominal level. This was the most common error in the sample.
2. **Run simulations properly.** Use hundreds of replications or more, report Monte Carlo standard errors, include scenarios where your method *should* fail, and use non-null designs that can actually test your claim.
3. **Quantify uncertainty for every comparison.** Use seeds, confidence intervals and paired tests. "Not significant" in the results means you can't say "outperforms" in the abstract.
4. **List only contributions you deliver.** Attribute methods precisely, especially your supervisor's.
5. **Keep textbook exposition short.** Cite it, and spend the words on analysis. Several merits pad with background such as the history of Brownian motion or restated Transformer equations.
6. **Release your code and finish properly.** No placeholders, readable figures, and captions that match their content.

**Still worth getting:** the official ST499 marking criteria and word limit, from the programme handbook or Moodle. With those, this document could be checked against what markers are actually told to reward.
