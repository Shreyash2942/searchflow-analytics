# SearchFlow Analytics

SearchFlow Analytics is a Python portfolio project that explains when linear
search or binary search is the better practical choice. It generates
reproducible integer data, validates CSV input, searches original and sorted
views, measures real execution time, and presents the results through a local
command-line application.

Version 1.0.0 is complete and released for the Design and Analysis of
Algorithms portfolio.

**Author:** Shreyash2942

**Release:** [`v1.0.0`](https://github.com/Shreyash2942/searchflow-analytics/tree/v1.0.0)

**Runtime:** Python 3.10+ standard library

**Repository:** [Shreyash2942/searchflow-analytics](https://github.com/Shreyash2942/searchflow-analytics)

## Why this project exists

Algorithm complexity is useful only when it is connected to a workload.
Linear search can be the right answer for unsorted data, small inputs, or an
early match because it needs no preparation. Binary search can be the right
answer for large sorted data and repeated lookups because it narrows the
search interval logarithmically. SearchFlow Analytics makes that trade-off
concrete by measuring both algorithms at 100, 1,000, and 10,000 values while
recording sorting costs separately.

## What the application does

- Generates deterministic CSV datasets with 100, 1,000, and 10,000 integers.
- Loads, validates, and preserves original-order data.
- Creates an independent sorted copy for binary search.
- Runs linear search, binary search, or both from an interactive menu.
- Reports found status, zero-based index, and seconds per search.
- Benchmarks four target cases across all sizes and writes 24 result rows.
- Stores raw timing samples, sorting measurements, environment details, and
  SHA-256 provenance hashes in `benchmark_metadata.json`.
- Provides 73 automated tests, complexity analysis, recommendations, and
  portfolio screenshots.

## Quick start

From the repository root in Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

The menu asks for a dataset size, a signed integer target, and a search mode:

```text
1. 100
2. 1,000
3. 10,000

1. Linear Search
2. Binary Search
3. Compare Both
```

Enter `q` at any prompt to quit. For a quick successful comparison, choose
dataset `1`, target `83810`, and mode `3`. The linear result uses original-order
index `0`; the binary result uses an index in the sorted copy.

For macOS/Linux, replace `.\.venv\Scripts\python.exe` with `.venv/bin/python`.
The full architecture and operating context is in
[project documentation](docs/project_documentation.md).

## Benchmark and tests

Run the complete benchmark:

```powershell
.\.venv\Scripts\python.exe main.py --benchmark
```

This measures 3 sizes x 4 target cases x 2 algorithms and writes:

- [results/performance_results.csv](results/performance_results.csv)
- [results/benchmark_metadata.json](results/benchmark_metadata.json)

Run the full test suite:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

The final suite contains 73 passing tests. The timer uses seven batches of 100
searches, three warm-ups, and the median batch mean by default. Loading,
validation, sorting, and output are excluded from search-only timing.

## Complexity and findings

| Algorithm | Input | Best | Average / worst | Extra search space |
| --- | --- | --- | --- | --- |
| Linear search | Any valid order | O(1) | O(n) / O(n) | O(1) |
| Binary search | Ascending sorted data | O(1) | O(log n) / O(log n) | O(1) |

The saved benchmark shows linear search winning an immediate first-element
match, while binary search is much faster for missing targets as the dataset
grows. Sorting costs O(n log n) worst-case and uses O(n) space for a copy, so
binary search is not automatically best for one lookup. Read the full
[Big O analysis](docs/big_o_analysis.md) and
[recommendation guide](docs/recommendation_guide.md).

## Screenshots

The final evidence captures are in [docs/screenshots](docs/screenshots/):

| Capture | File |
| --- | --- |
| Linear search on 100 values | [linear_100_success.png](docs/screenshots/linear_100_success.png) |
| Binary search on 1,000 values | [binary_1000_success.png](docs/screenshots/binary_1000_success.png) |
| Both algorithms on 10,000 values | [both_10000_success.png](docs/screenshots/both_10000_success.png) |
| Missing target and main menu | [missing_target.png](docs/screenshots/missing_target.png), [main_menu.png](docs/screenshots/main_menu.png) |
| Final benchmark table | [final_benchmark_results.png](docs/screenshots/final_benchmark_results.png) |

## Documentation map

Start with the document that matches your purpose:

- [Project documentation](docs/project_documentation.md) — detailed purpose,
  architecture, data contracts, module responsibilities, algorithm contracts,
  benchmark design, and quality evidence.
- [Final project report](docs/project_report.md) — portfolio-ready summary of
  the problem, implementation, findings, recommendations, and limitations.
- [APA 7 project report](docs/APA_SearchFlow_Analytics_Report.docx) — formatted
  Word report with title page, abstract, citations, references, tables, and appendix.
- [Combined seven-day history](docs/combined_days.md) — one readable record of
  the complete Day 1–7 implementation journey.
- [Requirements](docs/requirements.md) — functional and nonfunctional scope.
- [Architecture](docs/architecture.md) — pipeline diagram and module contracts.
- [Benchmark methodology](docs/benchmark_methodology.md) — timing boundaries,
  target cases, raw-sample interpretation, and reproducibility.
- [Day 7 checklist](docs/day_7_checklist.md) — final validation, screenshots,
  and release evidence.
- [Release notes](docs/release_notes.md) — Version 1 included scope and limits.

The original [Day 1](docs/day_1_checklist.md), [Day 2](docs/day_2_checklist.md),
[Day 3](docs/day_3_checklist.md), [Day 4](docs/day_4_checklist.md),
[Day 5](docs/day_5_checklist.md), and [Day 6](docs/day_6_checklist.md)
checklists remain available as detailed historical records.

## Repository structure

```text
searchflow-analytics/
|-- main.py
|-- src/                    # Pipeline, algorithms, timing, benchmark, CLI
|-- data/                   # Reproducible input CSV files
|-- results/                # Benchmark CSV and metadata
|-- tests/                  # 73 unittest cases
|-- docs/                   # Guides, report, history, analysis, screenshots
`-- diagrams/               # Pipeline architecture image and source
```

## Scope

Version 1 is intentionally local and standard-library based. Cloud deployment,
databases, APIs, dashboards, authentication, containers, CI/CD, distributed
processing, and advanced search algorithms are outside this release.
