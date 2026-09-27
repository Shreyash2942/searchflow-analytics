# SearchFlow Analytics: run instructions

## Prerequisites

- Python 3.10 or newer.
- PowerShell on Windows, or an equivalent terminal on macOS/Linux.
- No third-party package is required to run the application or tests.

All commands below start in the repository root, the directory containing
`main.py`.

## Create the environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

macOS/Linux:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

The requirements file documents the standard-library runtime policy, so the
install step does not add application dependencies.

## Start the interactive application

Windows:

```powershell
.\.venv\Scripts\python.exe main.py
```

macOS/Linux:

```bash
.venv/bin/python main.py
```

The menu asks for:

1. Dataset size: 100, 1,000, or 10,000.
2. A signed integer target, including `0` and negative values.
3. Linear search, binary search, or both.

Enter `q` at any prompt to quit. The displayed index is zero-based and belongs
to the list that was searched: original-order data for linear search and the
sorted copy for binary search.

## Quick interactive examples

To reproduce a successful 100-element linear search, enter:

```text
Dataset option: 1
Target: 83810
Search mode: 1
```

The included data returns linear index `0`. To compare both algorithms on the
same target, choose mode `3`. To demonstrate a missing value, use a target
such as `-1` with a generated dataset.

## Preview and regenerate data

Validate and preview all included datasets without prompting:

```powershell
.\.venv\Scripts\python.exe main.py --preview
```

Regenerate the three required CSV files with seed `42`:

```powershell
.\.venv\Scripts\python.exe main.py --generate
```

`--generate` replaces the three named CSV files. Use it only when you intend
to recreate the reproducible inputs.

You can generate and then choose a follow-up action:

```powershell
.\.venv\Scripts\python.exe main.py --generate --interactive
.\.venv\Scripts\python.exe main.py --generate --benchmark
```

## Run the complete benchmark

The default benchmark measures 3 dataset sizes, 4 target cases, and 2
algorithms, producing 24 rows:

```powershell
.\.venv\Scripts\python.exe main.py --benchmark
```

The command writes:

- `results/performance_results.csv`
- `results/benchmark_metadata.json`

Default timing settings are seven batches, 100 searches per batch, and three
warm-ups. Customize them only when you want a different experiment:

```powershell
.\.venv\Scripts\python.exe main.py --benchmark --repeats 9 --iterations 200 --warmups 5
```

The saved CSV is search-only timing. Loading, validation, sorting, and output
are excluded; sorting measurements are kept separately in the metadata.

## Run tests

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The final Version 1 suite contains 73 tests. Use the quiet form when only the
pass/fail summary is needed:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -q
```

## Read the evidence

- [Project documentation](project_documentation.md) explains architecture and contracts.
- [Project report](project_report.md) summarizes the problem, method, findings, and limits.
- [Combined development history](combined_days.md) consolidates the seven daily milestones.
- [Big O analysis](big_o_analysis.md) explains complexity and measured trends.
- [Recommendation guide](recommendation_guide.md) explains when each algorithm fits.
- [Day 7 checklist](day_7_checklist.md) records final validation and release evidence.
- [Screenshots](screenshots/) show the completed application and benchmark output.

## Troubleshooting

If a dataset is missing or malformed, run `main.py --generate` to recreate the
three required files. If a benchmark argument is rejected, ensure the timing
options are used with `--benchmark`. If PowerShell blocks activation, call the
environment interpreter directly as shown above; activation is optional.
