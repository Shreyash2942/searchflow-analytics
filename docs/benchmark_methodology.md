# Day 4 benchmark methodology

The benchmark compares the two implemented search algorithms using the same
target values and the stored 100, 1,000, and 10,000-integer datasets. Run:

```powershell
.\.venv\Scripts\python.exe main.py --benchmark
```

## Search measurements

Defaults: `repeats=7`, `iterations=100`, `warmups=3`.

1. Load and validate the dataset and preserve original order plus a sorted copy.
2. Select the original first, middle (`n // 2`), and last values, plus
   `max(data) + 1`, which is guaranteed absent.
3. For each algorithm/case, run one untimed correctness check and three warm-up calls.
4. For each of seven batches, read `time.perf_counter()`, perform 100 calls,
   then read the clock again. Divide elapsed seconds by 100.
5. Save the median of those seven batch means as `execution_time`.

The timer wraps the search loop. It includes Python call/loop overhead but
excludes file operations, dataset validation, sorting, result checks, CSV
writing, and terminal output. No overhead is subtracted or estimated. Keep
timer results in full floating-point precision in the CSV; the terminal rounds
only its display.

Both algorithms receive the same target; linear search uses original-order
data and binary search uses the sorted copy. The algorithm measured first
alternates with dataset index plus case index. Each algorithm remains a
deterministic, nonmutating callable; correctness and last-result consistency
checks occur outside timed batches.

## Cases and interpretation

The original-position cases are not guaranteed best/average/worst cases for
both algorithms. Duplicates can make linear search find an earlier occurrence;
sorting changes positions; binary search returns any matching duplicate.
The missing target exercises a full unsuccessful linear scan and an unsuccessful
binary narrowing sequence. Three chosen present targets do not estimate the
statistical average over all possible targets.

Batching reduces the relative cost of reading the clock, and the median limits
the effect of unusually slow batches. Timings still depend on Python version,
CPU scheduling, background work, memory/cache state, and repeated-call warming.
No speed threshold is used as a unit-test assertion. The included data files
and their generation settings are reproducible; timing values vary between runs.

## Sorting measurements

Sorting is measured separately by calling `sorted(original)` seven times (or
the configured repeat count), always starting from the same unsorted input.
Each sort has its own start/end clock readings; the median and all sort samples
are recorded in metadata as seconds per sort. Copy deallocation happens after
the timed region. Input preparation has already created a sorted copy before
these measurements; these are warmed measurements, not cold-start timings.

The search CSV does not include sorting costs. A one-time binary-search choice
must account for preprocessing; repeated searches can reuse the sorted copy.
Use these measurements as context for Day 6's analysis, not as a universal
break-even estimate or a claim that binary search is always preferable.

## Output and provenance

- `results/performance_results.csv`: 24 records with
  `algorithm,dataset_size,target,found,index,execution_time`.
- `results/benchmark_metadata.json`: timestamps in UTC, Python/platform,
  clock resolution/implementation, timing settings, source and dataset SHA-256
  hashes, per-case raw samples, separate sort times, and the result CSV hash.
- `measurements[].csv_row` is the one-based data-record number, excluding the
  CSV header. It ties each CSV row to its target case and batch samples.
- Hashes identify the literal file bytes used for the captured run; the CSV hash
  checks that the CSV and metadata belong together.
- CSV writers use LF newlines, and `.gitattributes` preserves LF for Python,
  CSV, and JSON files across platforms so Git checkout does not invalidate hashes.

Rerunning replaces both result files after measurements complete. A computation
error leaves prior output intact. An I/O error during export is reported; if
export is interrupted, verify the CSV hash before treating the files as a pair.
Never substitute the illustrative values used in unit tests for measured output.

## Captured Day 4 run

The snapshot below comes from the run completed at
`2026-09-24T23:59:43.202789+00:00` with the default settings on Python 3.14.4.
Values are converted from the saved CSV seconds to microseconds and rounded
for readability. This dated snapshot is historical if result files are regenerated.

| Dataset size | Missing target: linear (microseconds/search) | Missing target: binary (microseconds/search) |
| --- | ---: | ---: |
| 100 | 1.532 | 0.321 |
| 1,000 | 17.587 | 0.512 |
| 10,000 | 179.697 | 0.699 |

In this run, missing-target linear time increased much more with input size.
Linear search was faster for the original first value, where it immediately
returned index zero. Both observations are consistent with the algorithms'
different work patterns. The completed [Big O analysis](big_o_analysis.md)
explains the theoretical bounds and sample limitations; the
[recommendation guide](recommendation_guide.md) accounts for sorting costs.
