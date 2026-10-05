# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

`AGENTS.md` is the tracked file;
`CLAUDE.md` is a gitignored symlink to it.
Edit `AGENTS.md`.

## What this repo is

Teaching materials for Memming's introductory statistics and probability course,
taught to biology students whose only programming prerequisite is basic Python.
The course description and learning objectives are in `README.md`;
every notebook should serve one of those objectives.

The current deliverable is a set of teaching widgets:
marimo notebooks exported to WebAssembly,
which students open in a browser and modify with nothing installed.
Topics: random sampling, the law of large numbers, histograms,
sampling distributions, and shuffling (permutation) to generate null distributions.

As of 2026-10-05 the repo holds only `README.md`.
There is no `pyproject.toml`, notebook, or build script yet;
update this file when the layout lands.

## Commands

marimo is not installed globally.
Each notebook declares its own dependencies in an inline PEP 723 header (`# /// script`),
so `uvx` and `uv run` work without a project environment.

```bash
uvx marimo edit --sandbox nb.py                      # author, in an env built from the inline header
uvx marimo check nb.py                               # lint; --fix rewrites in place; exits 0 on warnings unless --strict
uv run nb.py                                         # headless run of every cell = the restart-and-run-all check
uvx marimo export html-wasm nb.py -o <out> --mode edit   # student build: code visible and editable
python -m http.server --directory <out>              # WASM exports must be served over HTTP
```

`--mode run` gives a read-only app instead.
`--single-file` gives one HTML file that opens from disk but loads its assets from a CDN.
The export directory is regenerable,
and it contains a marimo-generated `CLAUDE.md` -
the prompt for marimo's in-browser AI assistant, not guidance for this repo.

## Authoring rules

Before designing, writing, or reviewing a notebook, read `demo-design.md`:
the step-by-step design for a 15-minute demo aimed at programming novices.
In this repo it replaces the global `teaching-materials.md` and `notebook-craft.md`.

marimo specifics:

- **The `.py` is the notebook.**
  There is no `.ipynb`, no jupytext pairing, and no output stripping.
- **marimo enforces the dependency graph.**
  Each global name is defined in exactly one cell,
  execution follows dependencies rather than file order,
  and `_`-prefixed names are cell-local.
  This removes most hidden-state failures,
  but marimo does not track mutation:
  mutating an object defined in another cell does not re-run its dependents.
  Build new objects instead.
  The one deliberate exception is the shared random generator in `demo-design.md`,
  whose draws advance its state so that rerunning a cell gives a fresh sample.
- **A UI element's `.value` is read in a different cell from the one that defines it.**
  Assign every `mo.ui.*` element to a global name, or it is not reactive.

## WebAssembly constraints

The exported notebook runs in Pyodide in the student's browser.

- Only pure-Python wheels and packages built for Pyodide import;
  numpy, scipy, pandas, and matplotlib are available.
- No threads, multiprocessing, or subprocess.
- No local filesystem: a data file is fetched relative to `mo.notebook_location()`,
  not opened by path.
- Pyodide is single-threaded and slower than native Python.
  Size simulations so that dragging a slider re-runs without a visible pause.
