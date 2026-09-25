# Day 4: performance timing and benchmark pipeline

Implements the Day 4 plan: measure both algorithms on all three required
sizes using repeated actual clock measurements, then store results in CSV.

## Completed quality gate

- [x] Use `time.perf_counter()` for high-resolution timing.
- [x] Measure both linear and binary search on their correct input orders.
- [x] Benchmark 100, 1,000, and 10,000 integers.
- [x] Repeat searches and document the summary statistic and time units.
- [x] Record present and missing targets with correct found/index values.
- [x] Save the exact required CSV columns and 24 measured rows.
- [x] Keep sorting outside search timing and record it separately.
- [x] Save raw samples, timing settings, environment, and file hashes.
- [x] Verify output against actual samples and run 56 passing tests.

## Delivered files

- `src/performance_timer.py`: correctness check, warm-ups, timed batches,
  median seconds/search, and raw sample return values.
- `src/results_manager.py`: validated records and required CSV export.
- `src/benchmark.py`: target selection, both searches/all sizes, sort timings,
  run metadata, and output orchestration.
- `main.py`: `--benchmark` and configurable repeats/iterations/warm-ups.
- `tests/test_performance_timer.py`, `test_results_manager.py`,
  `test_benchmark.py`: 17 new tests, in addition to the existing 39.
- `results/performance_results.csv` and `results/benchmark_metadata.json`:
  actual captured output. [Methodology](benchmark_methodology.md) documents
  the experiment, its limitations, and a dated result summary.

## Validation record

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe main.py --benchmark
```

All 56 tests passed on Python 3.14.4. The full default run produced 24 records;
each CSV timing matched the median of its recorded batch samples. Source,
dataset, and CSV hashes were verified. Tests also checked result correctness,
index-zero handling, CSV precision/schema, invalid parameters, and missing files.
Controlled-clock unit tests verify arithmetic; published results use actual clocks.

Day 5 adds the interactive search menu. The final Big O analysis and
recommendation guide remain Day 6 work.
