> **Actual grade:** Merit · **Source:** `Past Examples/Multiple Mean-shift Interval Detection for Multivariate Time Series with Applications to Stock Returns - Merit.pdf`
> Profile written blind (the reviewer did not know the grade). The blind estimate below is the reviewer's guess, not the real mark.

# D07: Multiple Mean-shift Interval Detection for Multivariate Time Series with Applications to Stock Returns
**Length:** 33 pages (29 numbered plus front matter), ~6,500 words in the main body (excluding references and appendices) · **Area:** Change-point / epidemic change detection, high-dimensional time series, financial application
**Structure:** Intro + lit review 18% · Problem set-up and notation 8% · Scan statistics 9% · Methodology 15% · Simulation study 15% · Extension (single-series clustering) 5% · Real data (NASDAQ stocks) 25% · Conclusion + limitations 6%

## Research question and project type
Can epidemic (raised or dipped interval) mean shifts shared across many series be found by aggregating Walther and Perry's (2022) self-normalised (SN) scan statistic across dimensions (ℓ1, ℓ2 with optional sparsification threshold γ, or ℓ∞), with Rademacher multiplier bootstrap thresholds? And does this reveal trends in five years of daily log-returns for 493 NASDAQ tech stocks? This is a methodological/computational project with a substantial applied part. No theory is developed. The weight is split fairly evenly between a proposed procedure with simulations and the stock-market application.

## Contribution
- **Original:** combining the SN scan with cross-sectional ℓq aggregation and sparsification, which the author says has not been done before (only Fryzlewicz 2024 has used SN in a change-point setting). Also new: a sequential "remove overlapping intervals" search, ad hoc interpretation tools ("contribution", "level", "deviance explained by interval" (DEI), pp. 21–22), a per-series multi-layer detection plus "cluster plot" (Section 6, Algorithm 1), and the application to NASDAQ data.
- **Reproduced or explained:** the SN scan, its cosine interpretation and tail bound (Walther 2022), the unknown-baseline version (Walther and Perry), aggregation and sparsification ideas (Cho and Fryzlewicz 2015, Cai et al. 2012), and the Rademacher bootstrap.
- **Label:** new or modified method (incremental) · novel application/data · some systematic comparison (SN vs non-SN).

## Theory
**Restates known results.** It restates the SN statistic, the √n·cosθ interpretation (p. 6), the sub-Gaussian tail bound quoted without proof (p. 6), the Chan and Walther detection boundary √(2 log T) (p. 8), and the one-factor representation of equicorrelated noise (p. 12). There are no derivations, null distributions or asymptotics for the aggregated statistic. The author admits this (p. 25: "results … are mostly empirical … lack of precise theoretical proof"), and γ is chosen by "guess".

## Empirical and simulation work
- **Simulation design (pp. 11–14):** p = T = 200. It compares SN and non-SN (rolling-window pre-standardised) scans across homoscedastic t/Gaussian noise, cross-sectional heteroscedasticity, temporal heteroscedasticity (Case 3) and equicorrelated noise (Case 4). Metrics are report rate, average intersection over union (IoU), and success rate (significant with IoU ≥ 0.8). The metrics are sensible.
- **Small replication counts:** results move in steps of 0.05 or 0.033, which implies about 20–30 replications. No Monte Carlo standard errors are given.
- **Weak results:** the Case 4 (correlation) results are close to zero for every method (Table 5). The significance results in Table 4 are hard to read: the SN-ℓ1 rejection rate on pure noise is 0.1 at the 90% level, which is fine, but power is very low.
- **Incomplete tables:** Table 3 reports only IoU, so significance is missing for Cases 1–2.
- **Inconsistent design:** Table 2 places signals at t ∈ [201,250] and [301,400], although T = 200 was stated.
- **Real data:** 493 stocks, 1,255 days. The bootstrap and permutation thresholds reject nothing (Figures 2–3). The author attributes this to a strong common factor (first principal component explains 25.5%). They then drop formal testing and simply rank the top-5 intervals from 14 method variants (Table 7), merge them into 11 "worth attention" intervals (Table 8), and match these to market events.
- **Missing comparisons:** the only baseline is the non-SN version of the same procedure. There is no comparison with existing high-dimensional methods such as sparsified binary segmentation (SBS), double CUSUM or MOSUM aggregation.
- **Code:** not provided or linked. Generative AI use for programming is acknowledged.

## Literature review
About 18% of the body (pp. 1–3), plus short reviews inside the bootstrap and methodology sections. It is reasonably broad, covering classical epidemic change, scan statistics, high-dimensional CUSUM/MOSUM aggregation and financial regime models, with about 45 references, mostly good journal papers. It is largely **descriptive** ("X did A, later Y did B"). There is little critical comparison or positioning beyond a gap statement ("no study used a multi-dimensional epidemic mean change model…").

## Correctness
- p. 21: the "contribution" formula divides a non-SN statistic S (with σ̂) by an SN-aggregated denominator. It is internally inconsistent and does not match the text.
- p. 22: as written, the DEI formula uses Σ(X − X̄)², which is the residual (unexplained) deviance rather than deviance explained.
- p. 24: the "worst September in 20 years" Forbes article (Saul, 2022) refers to September 2022, but it is used to support the September 2020 interval. This is a factual mismatch.
- p. 22: "November 2022 to February 2021" is a date typo.
- p. 12: Table 2 time indices fall outside the stated T = 200.
- Sequential testing (p. 9) reuses the same Cα at every step with no multiplicity discussion. The claim on p. 9 that the Rademacher bootstrap "preserves cross-sectional dependence" needs the same ξt across dimensions. This is implied but never stated.
- The simulation conclusion that SN is "more robust" is overstated given about 20 replications and mixed Case 3 results: non-SN with w = 75 beats SN in Case 3-2.
- The real-data conclusion that intervals "are likely to be real shocks" (p. 24) rests on anecdotal matching to Wikipedia and press articles, after the formal test found nothing.

## Writing and presentation
- **Typesetting:** clean LaTeX with a title page carrying the LSE logo, contents, lists of figures and tables, a summary, numbered equations, an algorithm box, and hyperlinked citations.
- **English:** frequent non-native phrasing and grammar errors ("literatures who employed", "their is", "principle components", "stickers" for tickers, "transitional" for traditional). There are dangling references ("see 8 and It is not difficult…", p. 24; "While is can also be note that More results…", p. 8).
- **Flow:** acceptable but somewhat list-like.
- **Rendered pages:**
  - Figure 1 (p. 10): a well-made 4×2 panel of heatmaps that illustrates aggregation and sparsification nicely.
  - Figure 5 (p. 21): NDXT index with labelled intervals, clear and effective.
  - Figure 8 (p. 24): the cluster plot is unreadable at page size, with tiny axis labels and an illegible legend.
  - Maths pages (p. 8): neatly typeset.
- **Tables:** Table 7 is dense but legible. Tables 4 and 5 are labelled "part-2" with no visible part 1.

## Critical reflection
**Moderate.** The author openly reports that the significance procedure failed on real data and gives a plausible explanation (common factor). Section 9 names real limitations: no confidence intervals for locations, fragmentation from discarding overlaps, no theory, and an arbitrary γ. Section 7.3 offers some genuine interpretation, for example that low-variance intervals inflate the SN statistic and so rank "trivial-looking" periods first. But the response to the failed test is to drop inference rather than fix it (for example by factor-adjusting the returns first, which is an obvious step). The event matching is uncritical.

## Strengths
1. A coherent and fairly natural idea: aggregate the heteroscedasticity-robust SN scan across dimensions with tunable sparsity. This is well motivated by the features of financial returns.
2. A good illustrative figure (Figure 1) and a sensible evaluation set-up (IoU, success rate, several heteroscedasticity regimes).
3. An honest report of a negative result on real data, with a reasonable diagnosis through PCA and a substantial, data-rich application section.

## Weaknesses
1. No theoretical development, thin simulations (about 20–30 replications, no standard errors, incomplete metrics, an inconsistent design), and no comparison with existing high-dimensional change-point methods.
2. The real-data analysis abandons formal inference and relies on ad hoc ranking plus anecdotal event matching. It has a factual citation error and inconsistent formulas for the interpretation tools.
3. Weak English and proof-reading, and one unreadable key figure (Figure 8). The main body is short, at about 6,500 words.

## Scores (1–5, 5 = exceptional for an MSc)
| Originality | Technical depth | Rigour | Empirical work | Literature review | Writing | Presentation | Critical reflection |
|---|---|---|---|---|---|---|---|
| 3 | 2 | 2 | 3 | 3 | 2 | 3 | 3 |

## Blind grade estimate
**Estimate:** Merit · **Mark:** ~61 · **Confidence:** medium
The project has a clear, somewhat original methodological idea and a real application, and it reads competently in LaTeX, which lifts it above a Pass. It is held back by:
- no theory;
- small, partly inconsistent simulations with no external baselines;
- a real-data section where the main inferential tool fails and is replaced by informal ranking;
- several formula and citation errors and weak English.

These keep it well short of Distinction. A low-to-mid Merit seems most likely, and a high Pass is possible if the examiners weigh the rigour problems heavily.

## Lessons for a future student
1. When your inference fails on real data, treat that as a problem to solve, not something to route around. Here, removing the common factor (PCA residuals or market-adjusted returns) and re-testing would have turned a negative result into a contribution.
2. Run enough Monte Carlo replications (hundreds, not 20), report standard errors, keep the design internally consistent, and benchmark against at least one established competitor from your literature review.
3. Check every formula against its verbal definition and every citation against the claim it supports. Make sure each figure is readable at printed size. Small slips like these add up and undermine examiners' trust.
