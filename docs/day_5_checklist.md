# Day 5: interactive CLI and pipeline integration

Implements Day 5 of the supplied portfolio plan, completing FR-04 (user
selections) and FR-06 (found/index/time display).

## Completed quality gate

- [x] Launch the titled menu with `python main.py` or `--interactive`.
- [x] Select 100, 1,000, or 10,000 integers.
- [x] Enter a signed integer target, including zero and negative values.
- [x] Select linear search, binary search, or comparison of both.
- [x] Load/validate the chosen dataset and route original/sorted inputs correctly.
- [x] Display found status, correct input-list index, and measured execution time.
- [x] Re-prompt invalid choices/targets and recover from missing/malformed files.
- [x] Support repeated searches and `q` at any prompt; handle EOF/Ctrl+C cleanly.
- [x] Preserve batch generation and benchmark commands; add explicit `--preview`.
- [x] Keep interactive searches from modifying datasets or saved benchmarks.

## Delivered files

- `src/cli.py`: reusable `search_dataset` function plus input, display, and menu loop.
- `main.py`: default menu and mutually exclusive interactive/preview/benchmark
  actions; generation before the selected action where explicitly requested.
- `tests/test_cli.py`: 17 tests for selections, validation, recovery, repeat/exit
  behavior, correct input ordering, file preservation, and command routing.
- Updated README, requirements, and architecture contracts.

The menu uses the existing timer defaults: seven batches of 100 searches,
three warm-ups, and the median batch mean in seconds/search. Loading, sorting,
validation, and output are excluded from that timing. Results explicitly label
original-order and sorted indexes; an index of zero is a successful match.

## Validation record

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe main.py
.\.venv\Scripts\python.exe main.py --preview
```

All 73 tests pass on Python 3.14.4 (the existing 56 plus 17 CLI tests).
A real subprocess session launched from the parent directory supplied an
invalid option, compared both searches for target `83810` in 100 elements,
searched for missing target `-1` with binary search in 1,000 elements, and quit.
It completed with exit status 0 and no stderr. Dataset and saved benchmark
hashes were unchanged. Unit tests additionally cover all size/mode combinations,
wrong element counts, malformed CSVs, EOF/interrupts at every prompt, and
invalid benchmark settings before generation.

Interactive results are live observations and are not saved over the Day 4
benchmark evidence. Use `--benchmark` for a new saved comparison run. The
captured Day 4 measurements and source hashes remain a dated record of that run.

Day 6 adds the final Big O analysis and recommendation guide, alongside review
of the existing test coverage. Day 7 handles final screenshots and release checks.
