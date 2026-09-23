# SearchFlow Analytics

A Python portfolio project for comparing linear and binary search in a local
CSV data-processing pipeline. The planned Version 1 release is `v1.0.0`.

## Current status

Days 1–3 are complete: project setup, reproducible datasets, CSV loading,
validation, independent sorted copies, and linear/binary search functions.
`main.py` runs the data preparation pipeline; the search functions can be used
directly as shown below. Timing and the interactive search menu follow on Days 4–5.

## Objectives

- Generate and validate datasets containing 100, 1,000, and 10,000 integers.
- Compare linear search on unsorted data with binary search on a sorted copy.
- Measure actual execution times and save benchmark results to CSV.
- Explain O(n) versus O(log n), including sorting costs and usage recommendations.

## Setup

Use Python 3.10 or newer. Days 1–3 were verified locally with Python 3.14.4.
Run these commands from the repository root in PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

Calling the environment's interpreter directly does not require activation or
changes to PowerShell's execution policy. On macOS/Linux, use
`.venv/bin/python` after creating the environment with `python3 -m venv .venv`.

The three datasets are already included. Running `main.py` loads and validates
them without changing the files, then previews original and sorted values.
It works from another working directory as well because the data directory is
resolved relative to the project source.

Example output (previews omitted here):

```text
SearchFlow Analytics
dataset_100.csv: 100 integers validated; sorted copy ready.
dataset_1000.csv: 1,000 integers validated; sorted copy ready.
dataset_10000.csv: 10,000 integers validated; sorted copy ready.
Data pipeline ready. Search functions are available; timing follows on Day 4.
```

To regenerate all three CSV files with seed `42`, replacing their current contents:

```powershell
.\.venv\Scripts\python.exe main.py --generate
```

Missing files and invalid data produce an error message and a nonzero exit code.
See [dataset format and reproducibility](data/README.md) for the data contract.

The application and tests use the Python standard library (`csv`,
`random`, `pathlib`, `time`, `statistics`, and `unittest`); no third-party runtime
packages are currently required.

## Search examples

From the repository root, start Python with `.\.venv\Scripts\python.exe`, then:

```python
from src.linear_search import linear_search
from src.binary_search import binary_search
from src.data_processor import prepare_search_data

original, ordered = prepare_search_data([7, 2, 9, 4])
print(linear_search(original, 9))  # 2, in original order
print(binary_search(ordered, 9))  # 3, in [2, 4, 7, 9]
print(linear_search(original, 99))  # -1
print(binary_search(ordered, 99))  # -1
```

Both functions return a zero-based matching index or `-1`, leave inputs
unchanged, and return `-1` for empty sequences. Test `index != -1` for a match;
index `0` is a valid result.

| Algorithm | Input | Duplicates | Time / extra space |
| --- | --- | --- | --- |
| Linear search | Validated integers in any order | First matching index | Best O(1), average/worst O(n); O(1) space |
| Binary search | Validated integers sorted ascending | Any matching index | Best O(1), average/worst O(log n); O(1) space |

Binary search assumes a list or tuple with constant-time indexing. It does not
sort or scan to check ordering inside the search. Use the sorted output of
`prepare_search_data` and validate at the pipeline boundary before searching.
The two algorithms may return different indexes for the same value. Sorting
cost is separate from the search complexities above.

## Architecture

![Planned pipeline architecture](diagrams/pipeline_architecture.png)

The CLI will coordinate generation/loading, validation, an unsorted and sorted
branch, timed searches, CSV results, and user display. Written analysis will use
the measured results. See [architecture and contracts](docs/architecture.md).

## Repository structure

```text
searchflow-analytics/
|-- main.py                  # Day 2 data pipeline; interactive search on Day 5
|-- requirements.txt         # Runtime dependencies
|-- .gitignore
|-- src/
|   |-- __init__.py
|   |-- data_generator.py
|   |-- data_loader.py
|   |-- data_processor.py
|   |-- linear_search.py
|   `-- binary_search.py
|-- data/                   # README and generated 100/1,000/10,000-value CSV files
|-- results/                # Measured benchmark CSV on Day 4
|-- tests/
|   |-- test_data_pipeline.py
|   |-- test_linear_search.py
|   `-- test_binary_search.py
|-- docs/
|   |-- requirements.md
|   |-- architecture.md
|   |-- day_1_checklist.md
|   |-- day_2_checklist.md
|   |-- day_3_checklist.md
|   `-- screenshots/         # Working application captures on Day 7
`-- diagrams/
    |-- render_architecture.py
    `-- pipeline_architecture.png
```

Future module names and responsibilities are recorded in the architecture
document. Empty output directories are retained with `.gitkeep` files.

## Validation

Run the data pipeline and search tests from the repository root:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

All 39 tests pass. Coverage includes dataset/CSV validation, reproducibility,
copy independence, entry-point behavior, search boundary cases, duplicates,
small-input oracle comparisons, and searching all three required sizes.
Indexed-read checks verify binary search's logarithmic work bound and one-read
midpoint match. Actual timing and benchmark measurements follow on Day 4.

## Delivery plan

| Day | Deliverable |
| --- | --- |
| 1 — complete | Environment, requirements, structure, architecture |
| 2 — complete | Dataset generation, loading, validation, sorted copies |
| 3 — complete | Linear and binary search |
| 4 | Timing and benchmark CSV |
| 5 | Interactive CLI and integration |
| 6 | Complete tests, Big O analysis, recommendation guide |
| 7 | Final validation, screenshots, README, `v1.0.0` release |

See [Version 1 requirements](docs/requirements.md) and the
[Day 3 quality gate](docs/day_3_checklist.md). The
[Day 1](docs/day_1_checklist.md) and [Day 2](docs/day_2_checklist.md) quality gates
are retained as historical records.
This version stays local:
cloud deployment, databases, APIs, containers, orchestration, CI/CD,
authentication, web dashboards, distributed processing, and advanced search
algorithms are outside its scope.
