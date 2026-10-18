# Contribution guide

1. Keep book exercise IDs stable within the October 2026 draft.
2. Every newly claimed executable exercise needs an output key `Ecc.ee` in `chapter_demos.py` and an automated assertion or test.
3. Distinguish *proof* from *finite evidence* or *numerical example*. Use `_PARTIAL` keys for demonstrations not sufficient to settle the exercise.
4. Document algebraic conventions: scalar field, characteristic, basis, tensor ordering, and 0/1-based indices.
5. Never change behavior just to match an expected output without checking the theorem and assumptions.
6. Tests: `python -m pytest -q`. Notebook validation can be run with `python scripts/check_notebooks.py` after installing the notebook extra.
7. Add exercises to the map only from a specified manuscript edition; don't invent book exercises.

If adding a new dialect, include at least one counterexample or comparison showing precisely which structural property changes.

To rebuild the exact-text worksheets after revising the manuscript:

```bash
python scripts/sync_exercises.py /path/to/Overleaf-source/chapters
```

This requires the booklet's chapter `.tex` files, **not** a PDF or an internet connection. Review generated diffs and exercise numbering after every resynchronization.
