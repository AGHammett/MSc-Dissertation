# ST499 — MSc dissertation proposal research

This is a reading repo for choosing an LSE MSc Statistics dissertation (ST499), 2026–27. It's mostly PDFs and notes. There is almost no code.

## Layout
- `<Supervisor> Preview/P<n> - <project title>/` is one proposal per leaf folder. Each holds a brief (`Brief - <title>.txt`, not `brief.txt`), the background papers the supervisor supplied, and the generated `overview.md` and `plain-summary.md`:
  - `Feng Preview/P1 - Improving Statistical Inference Using External Predictions/`
  - `Feng Preview/P2 - Score-based Generative Modelling with Diffusion Processes/`
  - `Shi Preview/P1 - Semi-supervised RLHF for LLM Fine-tuning/`
  - `Shi Preview/P2 - Variance-reduced Alignment for Large Language Models/`: VRPO (the brief has no title or supervisor line)
  - `Vojnovic Preview/P1 - Valid Confidence Intervals for the Multicalibration Error/`
  - `Vojnovic Preview/P2 - What Does a Human-Preference Leaderboard Actually Rank/`
  - `Wang Preview/P1 - Conformal Prediction under Distribution Shift/`
- Shared papers: the Shi P1 and P2 folders both contain the same DPO, InstructGPT and VRPO PDFs. Shi P1's PPI is the *Science* version, while Feng P1's is the arXiv version.
- `Past Examples/` holds 15 past ST499 dissertations (grade in the filename), `expectations.md` (synthesis of what separates the bands) and `Profiles/` (one blind rubric profile per dissertation).
- `MSc Dissertation Topics List for Students 2026-27.pdf` is the department's full topic list.
- `LSE Dissertation Topics Deep Dive.md` holds earlier notes covering other supervisors (Itkin, Livieri, …).
- The `.md` reviews in the `Shi Preview/P*/` folders are earlier AI-written reviews. They are not supervisor material.
- `explore.md` is the current task spec: an overview and plain summary per proposal.
- `sync.py` makes filenames Windows-safe, then commits, pulls and pushes. The user syncs between Linux and Windows, so keep new filenames free of `: " < > | ? *`.
- `pyproject.toml` and `src/st499/` are an empty uv skeleton (Python 3.14).

## The user
LSE MSc Statistics student with a BSc in Economics and Finance. Comfortable with probability, inference, regression, MLE, basic ML/DL and some real analysis. This term: measure-theoretic probability, stochastic processes (martingales, Itô, SDEs), statistical inference.

## Conventions for written output
- Use British spelling.
- Never invent claims about papers. Cite page, section or equation, and flag anything unclear in the source.
- Keep the papers' claims separate from your own interpretation, and label which is which.
- Unless asked otherwise, work only from the supplied brief and papers, with no outside literature.
- Tools: `pdftotext` / `pdfinfo` are installed. `pypdf` is not.
