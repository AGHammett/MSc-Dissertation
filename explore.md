# Task: overviews of my MSc dissertation proposals

Each subdirectory of this repo is one dissertation proposal. Each should contain a `brief.txt` (the supervisor's short brief) and the background papers the supervisor gave. I haven't had the proposal meetings yet. I want to understand what each project is about before I go in.

## About the reader (me)
I'm an LSE MSc Statistics student. My BSc was in Economics and Finance. I'm comfortable with probability, statistical inference, regression, MLE and the basics of machine learning and deep learning, and I've done some real analysis. This term I'm taking measure-theoretic probability, stochastic processes (martingales, Itô calculus, SDEs) and statistical inference. Assume nothing beyond that.

## Step 1: Check everything is in order
Go through every subdirectory and produce a table with these columns:
- project
- `brief.txt` present and readable
- number of papers
- unreadable or scanned-only PDFs
- duplicates
- papers mentioned in the brief that aren't in the folder
- files that aren't what their name suggests

If anything is missing or broken, stop and show me the table. Otherwise show the table and carry on.

## Step 2: Two documents per proposal
Use one subagent per proposal, running in parallel. Each subagent reads only its own folder and writes two files into it.

Work only from the brief and the supplied papers. Don't search for other papers.

### `overview.md` (the in-depth one)
1. **The brief.** The brief restated in a paragraph. Say what kind of project it is: theoretical, methodological, computational or applied.
2. **Paper by paper.** For each paper:
   - the problem it tackles;
   - its approach;
   - its main findings and results;
   - its key assumptions;
   - how it relates to the other papers.
   Give page, section or equation references for specific claims.
3. **How the papers fit together.** The shape of the area as these papers present it.
4. **Tie-in to the dissertation.**
   - What the brief's proposed directions would mean in practice.
   - What a dissertation would plausibly involve: proofs, new methods, simulations, real-data experiments.
   - Where the open questions are, using the papers' own limitations and future-work sections.
5. **Background knowledge required.** List the maths, statistics and CS/ML knowledge needed. Mark each item as "covered by my modules", "partly covered" or "new to me", and give a rough sense of how much work the new items would be.
6. **Practicalities.** Whether code is available, whether data is available, and how much compute it would need.
7. **Questions for the proposal meeting.** Points the brief leaves ambiguous, and choices the supervisor would need to make.

### `plain-summary.md` (the short one, about one page)
Write this so I can get a real sense of the project.
- No equations.
- Stats and ML basics are fine. Explain any term from the specific domain the first time it appears.

Sections:
1. **The domain.** What field this is and why it exists.
2. **The problem.** What isn't working, or isn't known.
3. **What's been done.** The supplied papers in a sentence or two each.
4. **What the project would do.** The proposed directions in plain terms.
5. **What working on it would feel like.** Mostly proofs, coding, experiments, or data work.

## Rules
- Don't invent claims about the papers. If something is unclear from the text, say so.
- Keep your own interpretation clearly separate from what the papers say.
- British spelling.