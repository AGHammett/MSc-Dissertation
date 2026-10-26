> **Actual grade:** Distinction · **Source:** `Past Examples/Application of Transformer Architecture to Signal Generation in the Mid-Frequency FX Spot Market - Distinction.pdf`
> Profile written blind (the reviewer did not know the grade). The blind estimate below is the reviewer's guess, not the real mark.

# D02: Application of Transformer Architecture to Signal Generation in the Mid-Frequency FX Spot Market
**Length:** 51 pages (7 front matter + 42 main body + 2 bibliography; no appendices), ~11,000 words in the main body (excluding references and appendices) · **Area:** Machine learning for financial time series / quantitative trading
**Structure:** Intro 9% · Related work 22% · Data and labelling 13% · Methodology (architecture, XGBoost) 20% · Results 21% · Backtesting 9% · Conclusion 6%

## Research question and project type
Can an encoder-only Transformer, trained on hourly OHLC prices for six major FX pairs (2013–2023), produce useful 12-hour directional trading signals? The study varies context length (24/72/120 h), positional encoding (convolution-smoothed "local" versus fully learnable) and imbalance-aware loss (focal versus weighted cross-entropy). It compares against a class-weighted XGBoost on flattened windows and backtests the chosen model. The project is applied and computational (an empirical ML pipeline). There is no theoretical component.

## Contribution
- **Original:** a three-class labelling scheme based on the signed largest 12-hour forward move, with per-pair 10th/90th percentile thresholds (pp. 10–12); a small grid of seven Transformer configurations; a bespoke "signal accuracy" metric (TP − FP)/N_active plus an activity rate (pp. 31–32); and a Backtesting.py simulation with stop-loss tuning per pair (pp. 35–36).
- **Reproduced/explained:** standard Transformer encoder equations (Vaswani et al.), He initialisation, pre-LayerNorm residual blocks, focal loss and weighted CE (pp. 15–22), all presented as textbook exposition.
- **Label:** novel application/data, plus a modest systematic comparison. The comparison is narrow: it changes one factor at a time around a base model and uses single runs.

## Theory
Depth: **restates known results**. Chapter 4 writes out the Transformer equations (4.1–4.18, pp. 16–22), the attention formula (p. 18), the focal loss (p. 21) and pooling. Nothing is derived or proved. The labelling definitions (p. 11) and metric definitions (pp. 31–32) are the only "own" formalism.

## Empirical and simulation work
- **Data:** real 1-minute HistData quotes resampled to hourly. A chronological 40/20/40 split (p. 13) is sensible, and the scaler is fitted on the training split only.
- **Design concerns:**
  - The models are fed standardised raw price *levels* rather than returns. These are non-stationary across 2013–2023, so a scaler fitted on 2013–17 extrapolates.
  - The labelling percentiles seem to be computed on each pair's full-sample distribution (p. 12), which leaks test-period information into the thresholds and the profit targets (p. 35).
  - The text never says which split Table 4.3 is evaluated on. The focal-loss α and WCE weights appear to have been hand-tuned against these same results, so there is a risk of selection on the test data.
  - Training epochs and early stopping for the Transformer are not reported. The loss curves show overfitting after about 30 epochs (p. 31), and it is unclear whether that was acted on.
- **Baselines:** XGBoost only. There is no buy-and-hold, random-signal, LSTM or logistic baseline, and no majority-class reference.
- **Uncertainty:** none. Every model is a single run, with no seeds, confidence intervals or significance tests. The backtest returns of ±1–2% over three years with near-50% win rates (Table 5.1, p. 36) are very likely indistinguishable from noise, but this is never tested.
- **Robustness:** a 0.002% flat cost is acknowledged as optimistic (p. 42). There is no sensitivity analysis on costs or thresholds. Thresholding on predicted probability was tried but only described in words (p. 31).
- **Reproducibility:** a GitHub repository is linked (abstract), and the hyperparameter tables (4.1, 4.2) are reasonably complete.

## Literature review
About 22% (6 pages, pp. 4–9), with 16 references, several of them arXiv or working papers. It covers ARIMA/GARCH, then XGBoost, LSTMs, Transformers (TFT, Informer, Momentum Transformer, Quantformer, Fischer et al.), and momentum versus mean-reversion strategies. It is mostly descriptive and somewhat generic. Section 2.3 drifts into speculation ("one can imagine…", p. 8). The conclusion does relate the findings back to Bilokon and Qiu and to Fischer et al. (p. 41), which is a good touch. There is some misattribution: Deep Momentum Networks are credited to "Zhang et al. (2023)" (p. 4), but they are due to Lim, Zohren and Roberts.

## Correctness
- **Impossible metric values:** by its definition (p. 32), (TP − FP)/N_active is bounded in [−1, 1]. Yet Table 4.3 reports 1.17 and 3.70. These are presumably percentages, which would mean a tiny net edge, but that reading is never stated. The text treats 1.17 versus 3.70 as large differences in "directional discrimination" (pp. 33–34), which overstates weak signals. This is the most serious error.
- **Contradiction on the chosen model:** p. 34 says Model 2 uses "Learnable Positional Encoding", but Table 4.3 and the abstract say Local.
- **Labelling wording:** "the 10th and 90th percentiles of the absolute return distribution", with values below the 10th labelled "down" (p. 12), mixes up the absolute and signed distributions.
- **Mislabelled figure (probably):** in Figure 5.1 (p. 38), "USD/JPY" shows prices around 1.20–1.40. That is inconsistent with USD/JPY, which trades at about 105–150, and looks like USD/CAD.
- **Overclaims:**
  - "risk remained tightly controlled", and "diversification value", are inferred from low volatility that simply reflects 20% position sizing and tiny returns (pp. 37, 41).
  - "Local encoding lifted every metric" (p. 41) rests on a single comparison of one run each.
  - Win rates below 50% yet "reasonable accuracy" (p. 37).
- **Literature claim:** "Transformers… reduced computational cost" versus LSTMs (p. 2) is stated without qualification.

## Writing and presentation
The prose is fluent and well organised, but verbose. Long generic paragraphs explain why one looks at softmax distributions or loss curves (pp. 24, 27), which pads the word count. The rendered pages show clean LaTeX with a standard book layout, numbered equations and booktabs-style tables (p. 32). The figures are default matplotlib panels with tiny axis labels, three per page (p. 25). The Backtesting.py screenshots (p. 38) are illegible at print size, with unreadable legends. The figure-heavy results (11 figures across pp. 25–30) add little quantitative content. Referencing is consistent author–year. Typos are few, but the British/American spelling is mixed ("focussing", "parallelizable").

## Critical reflection
This is a genuine strength relative to the rest of the dissertation. The conclusion (pp. 41–42) honestly admits that XGBoost beats the Transformer. It offers alternative explanations: OHLC-only inputs, the coarse labelling and the evaluation regime. It lists limitations (flat costs, siloed capital, stop-loss tuning causing mild overfitting) and gives concrete future work. However, it does not see its own biggest problems: the metric scale, the lack of uncertainty, possible look-ahead in the labelling, and the near-noise returns. The results chapters mostly describe plots rather than test hypotheses.

## Strengths
1. A complete end-to-end pipeline, from raw data to labels, models, metric and backtest, with code released and hyperparameters tabulated.
2. Honest reporting of a negative result: the simple baseline wins, and the conclusion places this sensibly in the literature.
3. A thoughtful framing of trading-relevant evaluation: the activity–accuracy trade-off, and a metric that penalises opposite-direction errors.

## Weaknesses
1. Internal inconsistency in the core metric (values outside its [−1, 1] range), contradictions over which model was chosen, and an apparently mislabelled backtest figure. These undermine trust in the results.
2. Weak experimental rigour: single runs, no uncertainty or significance testing, no naive or random baselines, unclear evaluation split, possible look-ahead in thresholds, and price levels rather than returns as inputs.
3. Heavy textbook exposition of standard Transformer material and generic padding, with no theoretical or methodological depth beyond implementation.

## Scores (1–5, 5 = exceptional for an MSc)
| Originality | Technical depth | Rigour | Empirical work | Literature review | Writing | Presentation | Critical reflection |
|---|---|---|---|---|---|---|---|
| 3 | 2 | 2 | 3 | 3 | 3 | 3 | 3 |

## Blind grade estimate
**Estimate:** Merit · **Mark:** ~62 · **Confidence:** medium
The project is competent, complete and clearly written, with a real dataset, a working pipeline, a benchmark and an honest conclusion, so it sits comfortably above a Pass. It falls short of Distinction because the statistical content is thin. The theory is exposition only. The evaluation lacks uncertainty quantification and proper baselines, and there are visible errors (an impossible metric range, the model-description contradiction) that an examiner would catch. A generous marker who values the applied scope and reflection might push it to the mid-to-high 60s. A strict statistician could put it in the high 50s.

## Lessons for a future student
1. Sanity-check every number against its definition. A bounded metric reported outside its bounds, or a figure whose axis contradicts its caption, costs credibility that no amount of fluent prose recovers.
2. In an applied ML dissertation for a *Statistics* MSc, the marks come from rigour rather than architecture diagrams. Use repeated runs or seeds, confidence intervals or tests against a random/naive strategy, a clearly stated evaluation split with no tuning on the test set, and leakage-free preprocessing.
3. Cut generic exposition, such as restating the Transformer equations and explaining why loss curves matter, and spend those words on analysis: ablations, sensitivity to costs and thresholds, and whether the edge is statistically real.
