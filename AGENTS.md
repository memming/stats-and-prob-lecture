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
in late September 2026 they implemented a cellular automaton,
so loops, conditionals, and a grid of cells are known ground.
The course description and learning objectives are in `README.md`;
every notebook should serve one of those objectives.
Biological examples come from those two fields:
experiments the students run or will read about, not generic biology.

The current deliverable is a set of teaching widgets:
marimo notebooks exported to WebAssembly,
which students open in a browser and modify with nothing installed.
Topics: random sampling, the law of large numbers, histograms,
sampling distributions, and shuffling (permutation) to generate null distributions.

As of 2026-10-05 the repo has planning documents but no notebook,
`pyproject.toml`, or build script yet;
update this file when the layout lands.

## Notebook guides

Read `demo-design.md` for the teaching sequence and exercise budget.
Read `marimo.md` for marimo authoring, commands, and WebAssembly checks.

## Starting a new notebook: prior art first

Do not design from scratch, and do not inherit a weak design either.
Before drafting the step ladder, search the web for how others teach the same concept,
and open each resource rather than judging it from a search snippet.
Search five places:
established interactive tools,
Python and marimo notebooks (including the links listed under the notebook in `README.md`),
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
`demo-design.md` replaces the global `teaching-materials.md`
and `notebook-craft.md` for this repo.
