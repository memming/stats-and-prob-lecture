# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

`AGENTS.md` is the tracked file;
`CLAUDE.md` is a gitignored symlink to it.
Edit `AGENTS.md`.

## What this repo is

Teaching materials for Memming's introductory statistics and probability course,
taught to PhD students in cancer immunology and neuroscience programs.
They are smart but have little training in statistics or programming.
Most met statistics in an undergraduate biology course,
so the words (mean, histogram, p-value, t-test) are familiar
but often not tied to any phenomenon they have watched happen;
a notebook earns its place by making that connection.
Their programming comes from the Computational Thinking course:
in late September 2026 they implemented a cellular automaton in Google Colab,
so loops, conditionals, a grid of cells, and Colab itself are known ground.
The course description and learning objectives are in `README.md`;
every notebook should serve one of those objectives.
Biological examples come from those two fields:
experiments the students run or will read about, not generic biology.

The current deliverable is a set of Jupyter notebooks
that students open in Google Colab, edit, and save to their own Drive.
Topics: random sampling, the law of large numbers, histograms,
sampling distributions, and shuffling (permutation) to generate null distributions.
Until 2026-10-05 they were marimo WebAssembly notebooks;
`design/01-random-sampling.md` records why the course moved.

Layout: each notebook is `notebooks/NN_name.py` (jupytext `py:percent`, the source)
paired with `notebooks/NN_name.ipynb` (what Colab opens),
with one design note per notebook in `design/` under the same number.
`diary/YYYY-MM-DD.md` is the teaching diary, one file per class day:
what worked, timing, student questions, follow-ups.
It is public like the rest of the repo, so it names no student and carries no detail that could identify one.
The repo is public at https://github.com/memming/stats-and-prob-lecture,
and students open notebooks from its `main` branch in Colab (`colab.md`, "Delivery").
There is no `pyproject.toml` or build script.

## Notebook guides

Read `demo-design.md` for the teaching sequence and exercise budget.
Read `colab.md` for pairing, Colab mechanics, delivery, and checks.

## Starting a new notebook: prior art first

Do not design from scratch, and do not inherit a weak design either.
Start with `old_ref/`, local and git-ignored:
last year's five-day version of this course (October 2025),
with its Colab activity notebooks, readings, and books.
Never commit or publish anything from it; the books are copyrighted.
Of the books, Julian Simon's *Resampling: The New Statistics*
(`old_ref/books/02_resampling_book/`) fits this course best;
its open Python edition, Simon and Brett's *Resampling with*
(https://github.com/resampling-stats/resampling-with), is the one to cite and link.

Then search the web for how others teach the same concept,
and open each resource rather than judging it from a search snippet.
Search five places:
established interactive tools,
Python notebooks (including the links listed under the notebook in `README.md`),
university courses that post their labs and lecture code,
GitHub, for code that real courses use,
and the education research on the misconceptions the concept runs into.

Judge every candidate feature against `demo-design.md`, one by one.
A resource being widely used does not make each of its features good.
Adopt a move only when it beats what we would have written,
and reject the rest by name with a reason,
so nobody re-imports a rejected feature after finding the same source again.

Record the outcome in `design/<notebook>.md`:
the final observation, the step ladder,
an adopted list (source URL, what we took)
and a rejected list (source URL, what, why).
Cite only sources that were actually opened.
Present that note for approval before writing any cell.

## Authoring rules

Before designing, writing, or reviewing a notebook, read both guides.
Together, `demo-design.md` and `colab.md` replace the global `teaching-materials.md`
and `notebook-craft.md` for this repo.
