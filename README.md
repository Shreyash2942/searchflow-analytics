# SearchFlow Analytics

A Python portfolio project for comparing linear and binary search in a local
CSV data-processing pipeline. The planned Version 1 release is `v1.0.0`.

## Current status

Days 1 and 2 are complete: project setup, requirements, architecture, reproducible
dataset generation, CSV loading, validation, and independent sorted copies.
`main.py` runs the data pipeline. Search algorithms, performance timing, and the
interactive search menu follow on Days 3–5.

## Objectives

- Generate and validate datasets containing 100, 1,000, and 10,000 integers.
- Compare linear search on unsorted data with binary search on a sorted copy.
- Measure actual execution times and save benchmark results to CSV.
- Explain O(n) versus O(log n), including sorting costs and usage recommendations.

## Setup

Use Python 3.10 or newer. Days 1 and 2 were verified locally with Python 3.14.4.
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
Day 2 data pipeline is ready. Search algorithms and timing follow on Days 3 and 4.
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
|   `-- data_processor.py
|-- data/                   # README and generated 100/1,000/10,000-value CSV files
|-- results/                # Measured benchmark CSV on Day 4
|-- tests/test_data_pipeline.py
|-- docs/
|   |-- requirements.md
|   |-- architecture.md
|   |-- day_1_checklist.md
|   |-- day_2_checklist.md
|   `-- screenshots/         # Working application captures on Day 7
`-- diagrams/
    |-- render_architecture.py
    `-- pipeline_architecture.png
```

Future module names and responsibilities are recorded in the architecture
document. Empty output directories are retained with `.gitkeep` files.

## Validation

Run the Day 2 tests from the repository root:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The 21 tests cover reproducibility, numeric bounds, CSV round trips, missing
and malformed files, count validation, independent sorted copies, and the
data-pipeline entry point. Benchmark measurements and search tests follow when
those features are implemented.

## Delivery plan

| Day | Deliverable |
| --- | --- |
| 1 — complete | Environment, requirements, structure, architecture |
| 2 — complete | Dataset generation, loading, validation, sorted copies |
| 3 | Linear and binary search |
| 4 | Timing and benchmark CSV |
| 5 | Interactive CLI and integration |
| 6 | Complete tests, Big O analysis, recommendation guide |
| 7 | Final validation, screenshots, README, `v1.0.0` release |

See [Version 1 requirements](docs/requirements.md) and the
[Day 2 quality gate](docs/day_2_checklist.md). The
[Day 1 quality gate](docs/day_1_checklist.md) is retained as a historical record.
This version stays local:
cloud deployment, databases, APIs, containers, orchestration, CI/CD,
authentication, web dashboards, distributed processing, and advanced search
algorithms are outside its scope.
