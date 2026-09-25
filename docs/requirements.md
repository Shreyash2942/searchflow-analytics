# Version 1 requirements

This repository specification translates the supplied
`README_Search_Performance_Data_Pipeline_V1.md` (especially Day 1 and scope)
and `VERSION_1_REQUIREMENTS.md` into implementation and acceptance criteria.
Those source documents live in the parent portfolio workspace. The planned
release is `v1.0.0`; requirements below describe future acceptance, not current
feature completion. Repository name: `searchflow-analytics`.

Current implementation: Days 1–5 are complete. Data preparation, both searches,
timing (FR-05), benchmark CSV output (FR-07), and measured comparisons at all
required sizes (the measurement portion of FR-08) are implemented and tested.
Interactive search selection (FR-04) and found/index/time display (FR-06) are
also implemented. Final written analysis remains future work.
See [Day 5 evidence](day_5_checklist.md).

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
- Batch commands report expected file/data errors and exit with status 1.
  Interactive searches report errors and return to the menu. Ordinary searches
  only read files; `--generate` explicitly replaces the required CSVs.

Day 3 search contract (implemented):

- Both functions accept integer sequences and integer targets, returning a
  zero-based matching index or `-1`. Empty sequences return `-1` at the
  algorithm level, while the data pipeline still rejects empty CSV datasets.
- Linear search examines elements sequentially and returns the first match.
  Binary search narrows midpoint bounds on ascending input and returns any
  match. Duplicate results need not identify the same occurrence or index.
- Binary search expects already validated, sorted input. Use the sorted copy
  from `prepare_search_data`; an internal sorting/validation pass would add
  work beyond the logarithmic search itself.
- Neither function mutates input, performs file I/O, prints, or measures time.
- Standard Python lists/tuples supply constant-time indexing for the stated
  binary-search complexity. Both implementations use constant auxiliary space.

Day 4 benchmark contract (implemented):

- Use `time.perf_counter()` with defaults of seven batches, 100 calls per batch,
  three untimed warm-ups, and one untimed correctness-check call per case/algorithm.
- Save the median batch average as seconds per search. Timed regions include
  loop/call overhead and exclude validation, sorting, loading, and output.
- Test original first/middle/last values and `max(data) + 1` at each size.
  Alternate algorithm order between cases; the same target is used for both.
- Export 24 rows with the required six columns. Preserve index-zero matches;
  validate found/index consistency and finite nonnegative measured times.
- Store raw per-batch samples, case mapping, timestamps, Python/platform details,
  settings, input/source hashes, and the CSV hash in `benchmark_metadata.json`.
- Measure sorting separately with the median of seven individual sorted-copy
  operations (or the configured repeat count). Do not add sorting to search CSV values.
- `--benchmark` explicitly replaces result files. Invalid settings, missing files,
  or malformed inputs report an error. Keep prior results if computation fails
  before export. Reruns produce new actual timings, not identical timing values.

The complete methodology and interpretation limits are in
[benchmark_methodology.md](benchmark_methodology.md). Day 6 develops the
required analysis and recommendations.

Day 5 interaction contract (implemented):

- No-argument `main.py` or `--interactive` opens the menu. Select one of the
  three dataset sizes, enter an integer target, and select linear/binary/both.
- Invalid options and noninteger targets re-prompt. Zero and negative targets
  are accepted; no Python expression is evaluated as input.
- Each search loads and validates the chosen file, prepares independent
  original/sorted lists, and uses the existing timer defaults. Loading/sorting
  remain outside the displayed search timing.
- Display algorithm, found status, list-relative zero-based index (or `-1`),
  and seconds/search. Identify original-order versus sorted indexes.
- Repeat through the dataset menu; `q` at every prompt, EOF, and Ctrl+C exit
  cleanly with status 0. File/content errors report clearly and allow another choice.
- Interactive searches do not write files. `--preview` preserves the old
  non-interactive preview; `--generate` alone regenerates/previews; explicit
  `--generate --interactive` and `--generate --benchmark` select the follow-up.
- Action flags are mutually exclusive. Benchmark timing options still require
  `--benchmark`, and invalid timing counts are rejected before generation.
