# Meeting prep: Oliver Feng (initial meeting, 26 Oct 2026)

Exploratory meeting, held before choosing a project. The question lists in each `overview.md` (§7) are for scoping later. Most of them come down to four things:

1. What does he actually want from each project?
2. How much theory versus empirical work does he expect?
3. What counts as success: a new result, or a careful exposition plus reproduction or comparison?
4. What are the practical constraints: data, compute and timeline?

The meeting has three jobs: find out which project he's most excited about and where he'd steer it, find out what working with him is like, and leave him with a clear picture of me.

## 1. Short intro (about 1 minute)
- My background: BSc in Economics and Finance, and this term measure-theoretic probability, stochastic processes and inference.
- My aims: leaning towards industry, with a PhD kept open.
- One honest sentence per project on what draws me to it. P1 is a problem I've seen in lending. P2 uses the SDE material I'm learning now.

## 2. Questions for both projects (ask these first)
- Which of the two are you most excited about at the moment, and why?
- What would a strong dissertation on each look like? Is a careful exposition plus experiments enough, or do you expect a new result?
- Roughly what split between proofs, coding and data work do you picture?
- Is there a direction within each brief you'd especially like someone to take?

## 3. One or two questions per project
**P1: external predictions**
- Is this mainly about valid inference (confidence intervals) or better prediction? This is the biggest fork in the brief (overview Q1).
- Would an applied angle such as credit scoring be welcome, with an existing scorecard as the external predictor? Or should it stay general or biomedical? This tests whether survival analysis and CARE need to be central.

**P2: diffusion models**
- Of the three directions (application, new domains, convergence theory), which do you favour? Is a non-image application, such as financial time series, welcome? (overview Q1, Q8)
- How deep should the SDE exposition go: derive the reverse-time SDE, or state it and cite it?

## 4. Working with him
- How often would we meet, and how hands-on is he?
- How many MSc students is he taking, and when does he need a decision?
- Is there anything he'd recommend I read or try before committing?

## 5. Leave for later
- Specific datasets and access (UK Biobank, MIMIC), packages (`ppi-py`, `care-survival`) and GPU access. One line at most: "is compute or data access a concern for either?"
- Specific extensions (MAR missingness, VP versions of Dou et al., end-to-end bounds). Mention one only if he asks what interests me.
- Detailed reading lists. These are useful once I've chosen.

## 6. Things to notice (my interpretation)
- Which project he talks about more readily and in more detail.
- Whether a new result sounds required or just welcome. P1 has a safer core. P2 is safe only with an exposition, and the original contribution depends on which extension I pick.
- Whether his preferred direction for P1 involves survival analysis, and whether his preferred direction for P2 involves minimax theory. These are the two big new areas (P1 and P2 overviews, §5).

## After the meeting: his answers
| Question | P1 | P2 |
| --- | --- | --- |
| What he wants / favoured direction | | |
| Theory vs empirics split | | |
| New result required? | | |
| Practical constraints | | |

Other notes:
