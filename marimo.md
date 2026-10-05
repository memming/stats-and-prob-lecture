# marimo notebooks for class

> written primarily by AI agents under human direction.*
> *Agents:*
> *- GPT-6 Sol (gpt-6-sol) via Codex 0.160.0 - drafted. 2026-10-05*

This guide covers marimo mechanics and WebAssembly delivery.
Use [demo-design.md](demo-design.md) for the 15-minute teaching sequence,
the exercise budget, and the rule for when a widget earns its place.

## Code is part of the exercise

Students should write and debug a small, meaningful piece of Python.
Show the surrounding code working before asking them to fill a line.
Keep the target local enough that a syntax error is recoverable in class.
Start with editing a visible literal or call argument.
Add a widget when the idea needs many repetitions or a sweep.
Keep the code that computes the statistical idea visible in edit mode.

## Reactive cells and controls

- The notebook source is a `.py` file with an inline PEP 723 dependency block.
  There is no `.ipynb` or jupytext pairing.
- Put `import marimo as mo` in its own cell for faster markdown rendering
  in WASM.
- Give each global name one defining cell.
  Execution follows references between cells, rather than page order.
  Prefix temporary, cell-local names with `_`.
- marimo does not track mutation across cells.
  Make a new object or mutate it in the cell that defines it.
- Assign a `mo.ui.*` element to a global name in one cell.
  Read its `.value` in another cell so the dependent cell reruns.
  Keep the control next to the output it changes.
- Prefer normal reactive references to `on_change` callbacks or `mo.state`.
  If defining a control reruns, its value resets to the initial value.
- Label a slider and show its current value.
  For a costly calculation, use `debounce=True` so a drag runs on release,
  or gate the calculation with a run button or form.

## Randomness and fair comparisons

Use the seeded generator described in [demo-design.md](demo-design.md)
when rerunning a draw cell is meant to produce a new sample.
Do not reseed inside that draw cell.

When a control changes sample size, effect size, or another parameter,
decide whether the sample itself should change.
For a visual comparison of sample sizes, reuse one sequence of draws
and compare prefixes of that sequence.
Otherwise each slider move changes both the parameter and the random sample,
making the cause of a change in the plot unclear.

## WebAssembly delivery

- `--mode edit` opens the editor so students can change code.
  `--mode run` keeps controls live but locks code.
- Pyodide runs Python in each student's browser.
  NumPy, SciPy, pandas, and matplotlib are supported,
  but other dependencies need a compatible wheel.
  WASM has no true CPU parallelism and a documented 2 GB memory limit.
  Keep simulations small enough for a modest student laptop.
- Normal directory exports fetch the Python runtime and packages online.
  `--offline` can bundle them at build time, but still needs an HTTP server.
  It also requires Playwright and Chromium in the author's environment.
- `--single-file` opens from disk but still fetches assets from a CDN.
  It does not bundle `public/` data, local modules, or execution caches.
- Put bundled data in `public/` beside the notebook.
  In WASM, `mo.notebook_location()` points to a URL;
  load that URL with a reader that can fetch it, not built-in `open()`.
  Remote data must also permit browser cross-origin requests.
- A static host has no submission endpoint for student edits.
  If the code matters after class, give students an explicit
  download and submission path and test it after a page refresh.

## Authoring and pre-class check

marimo is not installed globally.
Each notebook declares dependencies in its PEP 723 header,
so these commands work without a project environment:

```bash
uvx marimo edit --sandbox nb.py
uvx marimo check nb.py --strict
uvx marimo check nb.py --select MW
uv run nb.py
uvx marimo export html-wasm nb.py -o <out> --mode edit
uv run --no-project python -m http.server --directory <out>
```

`marimo check --select MW` catches known WASM import, system-call,
and package incompatibilities.
`uv run nb.py` checks a fresh headless run of the notebook.
The export directory is regenerable;
its generated `CLAUDE.md` is for marimo's in-browser assistant,
not guidance for this repo.

Open the exported page in a fresh browser profile before class.
Check the first load on classroom Wi-Fi, all controls and code edits,
the slowest simulation, any bundled data, and the student hand-in route.
Test on a typical student laptop or tablet, not only the author's machine.

## marimo references

- [Best practices](https://docs.marimo.io/guides/best_practices/)
- [Interactive elements](https://docs.marimo.io/guides/interactivity/)
- [Running cells](https://docs.marimo.io/guides/reactivity/)
- [WASM notebooks](https://docs.marimo.io/guides/wasm/)
- [WASM export](https://docs.marimo.io/guides/exporting/webassembly_html/)
- [Offline export](https://docs.marimo.io/guides/publishing/self_host_wasm/)
- [Bundled data URL behavior](https://github.com/marimo-team/marimo/issues/6719)
