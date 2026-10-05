# Colab notebooks for class

> written primarily by AI agents under human direction.*
> *Agents:*
> *- GPT-6 Sol (gpt-6-sol) via Codex 0.160.0 - drafted (as marimo.md). 2026-10-05*
> *- Claude Opus 5.5 (claude-opus-5-5) via Claude Code - rewrote for Colab. 2026-10-05*

This guide covers notebook mechanics and Google Colab delivery.
Use [demo-design.md](demo-design.md) for the 15-minute teaching sequence,
the exercise budget, and the rule for when a widget earns its place.
The course moved from marimo WebAssembly notebooks to Colab on 2026-10-05;
`design/01-random-sampling.md` records why.

## Code is part of the exercise

Students should write and debug a small, meaningful piece of Python.
Show the surrounding code working before asking them to fill a line.
Keep the target local enough that a syntax error is recoverable in class.
Start with editing a visible literal or call argument.
Keep the code that computes the statistical idea visible.

## Source and pairing

- The source is `notebooks/NN_name.py` in jupytext `py:percent` format,
  paired with `notebooks/NN_name.ipynb`, the file Colab opens.
  Edit the `.py`, sync, and commit both.
  Never hand-edit the `.ipynb` JSON, and never edit both sides before syncing.
- `jupytext.toml` drops the jupytext version stamp so paired files do not churn.
- nbstripout strips outputs on commit through `.gitattributes`.
  The filter itself lives in `.git/config`, which a clone does not copy;
  a clone that skips the install below commits outputs silently.
- The kernel is `python3`, Colab's.

```bash
uv tool install nbstripout && nbstripout --install --attributes .gitattributes  # once per clone
uvx jupytext --set-formats ipynb,py:percent notebooks/NN_name.py              # once per new notebook
uvx jupytext --sync notebooks/NN_name.py                                      # after every edit
```

## Colab is not reactive

- A cell runs only when the student runs it.
  After an edit, every cell that uses the changed value keeps its old output until rerun.
  Keep an editable value in the same cell as the output it changes
  (`N = 60` sits in its plot cell),
  and say in the markdown which other cells to rerun.
- Use the seeded generator described in `demo-design.md`:
  rerunning a draw cell gives a new sample,
  and restarting the runtime and running all from the top reproduces every figure.
  Do not reseed inside a draw cell.
- When a value changes the sample size or another parameter,
  decide whether the sample itself should change.
  To compare sample sizes, draw one long sequence once and compare prefixes of it,
  so only the parameter changes.
- Show values with `print(...)`:
  numpy 2 displays a bare value as `np.int64(2)` or `np.True_`.
- End each plot cell with `plt.show()`.

## Predictions and form fields

- A Colab form field turns a variable into a dropdown menu:
  `prediction = "choose"  # @param ["choose", "0", "1", "2"]`.
  Choosing a value rewrites the line; the student then runs the cell.
  Outside Colab the comment is inert and the line is ordinary Python.
- The menu appears on the right of the cell, while students read the code on the left.
  Put a comment above the `# @param` line pointing to the menu on the right
  and saying not to edit that line by hand,
  and point to "the menu on the right" in the markdown and the gate message too.
- Ask for a prediction about a named event, not a nested condition.
  "How many of 10 runs will be balanced?", with *balanced* defined just above,
  reads at once; "in how many runs would every bar end inside the band?" did not.
- To hold a result back until the prediction is made,
  start the result cell with
  `assert prediction != "choose", "Choose your prediction in the menu above and run that cell first."`.
  Run all then stops at that cell with the message.

## Collapsed answers

Write each answer as an HTML `<details>` block in a markdown cell,
with a blank line after `<summary>Answer</summary>` and before `</details>`,
so the markdown inside still renders:

```markdown
<details>
<summary>Answer</summary>

6. The upper bound is excluded.

</details>
```

Checked in Colab on 2026-10-05 with notebook 1:
the blocks render collapsed, and markdown, code, and math inside them render when opened.
The form field renders as a dropdown,
Run all stops at the `assert` with its message,
and after a prediction is chosen Run all goes through to the last cell.

## Delivery

- Students sign in to Colab with a Google account;
  they used Colab in the Computational Thinking course in late September 2026.
- Colab opens a notebook straight from this public repository:
  `https://colab.research.google.com/github/memming/stats-and-prob-lecture/blob/main/notebooks/NN_name.ipynb`.
  The link shows whatever is on `main`, so push before sharing it.
  Each notebook carries this link as an "Open In Colab" badge under its title,
  and `README.md` links it under the notebook's section.
- Edits to a notebook opened from GitHub are not kept.
  The first markdown cell tells students to use *File > Save a copy in Drive* first;
  their Drive copy is also what they can hand in.
- Colab ships numpy, scipy, pandas, and matplotlib.
  Any other package needs `%pip install` in the notebook,
  which reruns in every new session.
- Colab's AI code completion can fill in an exercise line for the student.
  Ask students to switch AI assistance off in Colab's settings for these exercises.
- An idle Colab session disconnects and loses its variables;
  the student reruns from the top.

## Checks before class

The notebook as shipped should stop only at the prediction gate.
A copy with the exercises solved and a prediction chosen should run clean.
Execute copies outside the repo, and leave `MPLBACKEND` unset,
or the inline plots disappear from the executed notebook.

```bash
uvx --with nbconvert --with nbclient --with ipykernel --with numpy --with matplotlib \
    jupytext --to ipynb --execute <copy>.py -o <copy>.ipynb
```

Before class, open the notebook from its Colab link in a fresh signed-in browser
and check the form field, the collapsed answers, every plot, and the prediction gate.
