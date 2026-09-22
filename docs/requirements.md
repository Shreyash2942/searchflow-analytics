# Version 1 requirements

This repository specification translates the supplied
`README_Search_Performance_Data_Pipeline_V1.md` (especially Day 1 and scope)
and `VERSION_1_REQUIREMENTS.md` into implementation and acceptance criteria.
Those source documents live in the parent portfolio workspace. The planned
release is `v1.0.0`; requirements below describe future acceptance, not current
feature completion. Repository name: `searchflow-analytics`.

Current implementation: Days 1–2 are complete. FR-01, FR-09 (including friendly
entry-point error reporting), and FR-10 are implemented and tested. Search,
timing, benchmark output, interactive search selection, and written analysis
remain future work. See [Day 2 evidence](day_2_checklist.md).

## Functional requirements

| ID | Requirement | Acceptance evidence / planned day |
| --- | --- | --- |
| FR-01 | Generate and store 100, 1,000, and 10,000 integers. | `data/dataset_100.csv`, `dataset_1000.csv`, `dataset_10000.csv`; verify counts. Day 2. |
| FR-02 | Search unsorted data sequentially using linear search. | `src/linear_search.py`; return a matching zero-based index or `-1`. Day 3. |
| FR-03 | Search sorted data by repeatedly narrowing the range around its midpoint. | `src/binary_search.py`; return a matching zero-based index or `-1`; document sorted input. Day 3. |
| FR-04 | Accept dataset size, integer target, and linear/binary/both selection. | `main.py` menu; invalid input is handled without crashing. Day 5. |
| FR-05 | Measure actual search execution time using a high-resolution clock. | `src/performance_timer.py`, using `time.perf_counter()`; repeated searches across every required size. Day 4. |
| FR-06 | Display found/missing status, matching index where appropriate, and elapsed time. | CLI output for successful and missing targets. Day 5. |
| FR-07 | Save benchmark results with headers. | `src/results_manager.py` writes `results/performance_results.csv`. Day 4. |
| FR-08 | Compare both algorithms at all three dataset sizes. | Actual recorded measurements and explanations; no fabricated timing values. Days 4 and 6. |
| FR-09 | Load numeric CSV data and report missing or malformed files safely. | `src/data_loader.py`; conversion and failure cases verified. Day 2; CLI handling Day 5. |
| FR-10 | Reject empty/invalid datasets, verify counts, preserve unsorted values, and produce a sorted copy. | `src/data_processor.py`; original list remains unchanged. Day 2. |
| FR-11 | Explain search complexity using the measurements. | Approximately 1–2 pages in `docs/big_o_analysis.md`; all three sizes discussed. Day 6. |
| FR-12 | Recommend algorithms according to data ordering, size, search frequency, and sorting cost. | `docs/recommendation_guide.md`; avoid claiming binary search is always best. Day 6. |

The result CSV must contain these columns in this order:

```csv
algorithm,dataset_size,target,found,index,execution_time
```

Linear search: best O(1), average/worst O(n). Binary search: best O(1),
average/worst O(log n). Binary search requires sorted data; preprocessing cost
must be discussed separately from its search complexity.

## Nonfunctional requirements

| ID | Requirement | Acceptance evidence |
| --- | --- | --- |
| NFR-01 | Keep code modular and readable. | Focused modules/functions, meaningful names, docstrings, no unused code or debug output. |
| NFR-02 | Support reproducible experiments where practical. | Document dataset seed/range, target selection, repetition count, timing units and statistic before benchmarking. |
| NFR-03 | Handle expected failures predictably. | Invalid menu input, missing files and invalid datasets produce clear messages; no ordinary input error crashes the CLI. |
| NFR-04 | Run locally with portable paths. | Repository-relative resources, documented environment setup, successful package imports; no hardcoded user paths. |
| NFR-05 | Present honest, understandable results. | Actual measurements, clearly labeled time units and index interpretation; planned features distinguished from delivered ones. |
| NFR-06 | Validate important behavior. | Search boundary cases, dataset generation/loading/validation/sorting, and result-file generation covered by automated tests. |
| NFR-07 | Maintain reviewable development history and documentation. | Meaningful Git increments, final clean repository, runnable README and tagged release after final review. |

## Validation and submission evidence

- Linear search tests: beginning, middle, end, missing target, empty list, unsorted input.
- Binary search tests: beginning, middle, end, missing target, one-element list, sorted input.
- Pipeline tests: generation, CSV loading, data validation, sorting and benchmark output.
- Architecture: `diagrams/pipeline_architecture.png` and documented stage responsibilities.
- Screenshots in `docs/screenshots/`: linear/100, binary/1,000, both/10,000,
  found target, missing target, benchmark results, and main menu.
- Final README: title, description, objectives, features, architecture, technologies,
  structure, setup, run instructions, examples, dataset sizes, algorithms, tests,
  performance summary, screenshots, status, author, and version.
- Release: complete all acceptance checks before preparing `v1.0.0` on Day 7.
- Plan follow-through: document the retrospective and future ideas after release.

## Scope and design decisions

Version 1 uses Python, CSV, a CLI, tests, and written analysis. Cloud deployment,
databases, APIs, Docker, Airflow, CI/CD, authentication, a web dashboard,
distributed processing and advanced search algorithms are excluded. Expansion
waits until Version 1 is complete and reviewed.

Day 1 design decisions: use standard-library runtime modules and `unittest`;
keep the existing repository name; preserve the input data; treat indexes as
positions in the list actually searched; time search execution separately from
loading, sorting, and output. These are implementation choices consistent with
the supplied requirements.

Day 2 data contract (implemented):

- UTF-8 CSV with the exact header `value` and one integer per row. Loading also
  accepts a UTF-8 BOM and surrounding whitespace in integer cells.
- Generate with local `random.Random(42)`, inclusive range 0–100,000; allow
  duplicates. Each required size restarts the seed, making smaller datasets
  prefixes of larger ones. The included CSV files preserve the experiment inputs.
- Loader rejects empty data, bad headers, blank rows, extra columns, invalid
  encoding/CSV, and noninteger values with `ValueError`. Filesystem failures
  retain their `OSError` subtype, including `FileNotFoundError`.
- Validator rejects booleans, fractions, strings, empty data, and incorrect
  expected counts. Original-order and sorted outputs are separate copies.
- `main.py` reports expected file/data errors and exits with status 1. Normal
  execution only reads files; `--generate` explicitly replaces the required CSVs.

Resolve before the remaining features are built:

- Day 3: whether duplicates return any matching index or the first match.
- Day 4: target cases, repetition count, timing units, summary statistic,
  and how separately measured sorting costs will be reported.
