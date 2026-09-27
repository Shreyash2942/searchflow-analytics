# SearchFlow Analytics: user and operating guide

This guide explains how to install, run, and review SearchFlow Analytics. The
project is a local Python command-line application; it has no third-party
runtime dependencies. It compares linear search on original-order data with
binary search on an independent ascending copy.

## 1. Prerequisites

Use Python 3.10 or newer. From a terminal, confirm that Python is available:

```powershell
python --version
```

Run commands from the repository root, the directory containing `main.py`,
`data/`, `results/`, and `src/`.

## 2. Create the environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

macOS or Linux:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

`requirements.txt` documents that Version 1 uses only the Python standard
library. Installing it is still useful because it confirms the environment is
ready for the same commands used in the project documentation.

## 3. Confirm or recreate the datasets

The repository includes `data/dataset_100.csv`, `data/dataset_1000.csv`, and
`data/dataset_10000.csv`. Each file has a single `value` column and the
expected number of signed integer rows.

To validate the supplied files and preview their first values without prompts:

```powershell
.\.venv\Scripts\python.exe main.py --preview
```

To recreate all three files with the reproducible seed `42`:

```powershell
.\.venv\Scripts\python.exe main.py --generate
```

The generation command replaces the three required dataset files. It does not
change the saved benchmark files until a benchmark command is run.

## 4. Run an interactive search

Start the menu with either command:

```powershell
.\.venv\Scripts\python.exe main.py
# or
.\.venv\Scripts\python.exe main.py --interactive
```

The application repeats the following workflow:

1. Select `100`, `1,000`, or `10,000` values.
2. Enter a signed whole-number target, such as `83810`, `0`, or `-7`.
3. Select `Linear Search`, `Binary Search`, or `Compare Both`.
4. Review whether the target was found, its zero-based index, and seconds per
   search.
5. Start another search or enter `q` at any prompt to exit.

For a known successful comparison, select dataset `100`, enter `83810`, and
choose `Compare Both`. Linear search reports the index in original order;
binary search reports an index in the sorted copy. These indexes refer to
different list views and should not be compared as positions in the same list.

Interactive searches use the same timing defaults as the benchmark but do not
overwrite the saved CSV or metadata files. Loading, validation, and sorting
are excluded from the displayed search timing.

## 5. Run the complete benchmark

Run the standard benchmark with:

```powershell
.\.venv\Scripts\python.exe main.py --benchmark
```

The command measures four target cases for each dataset size—original first,
original middle, original last, and a missing value above the maximum—for both
algorithms. It writes 24 rows to:

- `results/performance_results.csv`
- `results/benchmark_metadata.json`

The CSV columns are `algorithm`, `dataset_size`, `target`, `found`, `index`,
and `execution_time`. The metadata file preserves raw timing batches, timer
settings, sorting measurements, environment information, source hashes,
dataset hashes, and the exported CSV hash.

The default measurement uses one correctness call, three warm-ups, and seven
batches of 100 searches. Each reported value is the median batch mean in
seconds per search. To run a smaller exploratory benchmark, provide positive
settings explicitly:

```powershell
.\.venv\Scripts\python.exe main.py --benchmark --repeats 3 --iterations 20 --warmups 1
```

Every benchmark run replaces the two files in `results/`. Preserve the
published files before experimenting if the dated portfolio evidence must
remain unchanged.

## 6. Run the tests

Run the complete standard-library test suite:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The suite covers search boundaries and duplicates, dataset generation and
loading, validation, sorted-copy behavior, timing arithmetic, benchmark
export, metadata, CLI recovery, and command routing. The completed Version 1
suite contains 73 passing tests.

## 7. Understand the outputs

### Interactive result

Each result includes:

- `Found`: `Yes` or `No`.
- `Index`: the zero-based index returned by the selected algorithm, or `-1`
  when the target is absent.
- `Execution time`: seconds per search for the search calls only.

Linear search scans the original list and returns the first matching duplicate.
Binary search receives the ascending copy and may return any matching duplicate
index. Binary search does not sort or validate its input internally; the data
pipeline performs that preparation before the call.

### Benchmark files

Use the CSV for a compact comparison table and the JSON metadata for method
details. `execution_time` is a measured seconds-per-search value, not a manual
or estimated number. Sorting time is recorded separately in metadata because
sorting is preparation work rather than search work.

## 8. Troubleshooting

**`python` is not recognized.** Install Python 3.10 or newer and ensure it is
available on `PATH`. Activate or call the virtual-environment interpreter
directly as shown above.

**A dataset file is missing.** Run `main.py --generate` from the repository
root, then run `main.py --preview` to validate the files.

**The menu rejects an entry.** Dataset choices must be one of the listed menu
options. Targets must be whole numbers; zero and negative values are valid.
Enter `q` to exit from any prompt.

**A benchmark output changed unexpectedly.** The `--benchmark` command replaces
the result CSV and metadata. Restore the published files from Git or rerun the
full benchmark with the standard settings.

**The application reports invalid data.** Check that each dataset is UTF-8 CSV
with exactly the header `value` and one integer per row. Regenerating the files
is the fastest way to restore the supplied data contract.

## 9. Related project documents

- [Project documentation](project_documentation.md): architecture, data
  contracts, module responsibilities, and benchmark design.
- [Benchmark methodology](benchmark_methodology.md): timing boundaries and
  interpretation of raw samples.
- [Big O analysis](big_o_analysis.md): complexity and measured trends.
- [Recommendation guide](recommendation_guide.md): when each algorithm fits a
  workload.
- [Final submission checklist](final_submission_checklist.md): requirements
  audit and verification record.
