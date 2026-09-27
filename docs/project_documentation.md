# SearchFlow Analytics: project documentation

## 1. Project purpose

SearchFlow Analytics is a local Python data pipeline and algorithm comparison
project. It generates reproducible integer datasets, validates them as CSV
input, prepares original and sorted search views, measures linear and binary
search, and presents the results through a command-line interface and a saved
benchmark report.

The project was created for the Design and Analysis of Algorithms portfolio.
Its central question is practical: when does a simple sequential scan make
sense, and when does the cost of sorted data pay off for repeated lookups?
The project answers that question with both theoretical analysis and measured
evidence instead of assuming that binary search is always the best choice.

## 2. Objectives and motivation

The implementation has five connected objectives:

1. Build a reproducible data-processing pipeline for 100, 1,000, and 10,000
   integer records.
2. Implement linear search over original-order data and binary search over an
   independent ascending copy.
3. Measure search work consistently with a high-resolution clock and preserve
   the raw samples behind each reported value.
4. Make the comparison usable through a forgiving interactive CLI as well as
   a repeatable benchmark command.
5. Explain complexity, sorting cost, and workload trade-offs in language a
   portfolio reviewer can verify from the source and results.

This scope keeps the focus on algorithm behavior. Cloud deployment, databases,
web dashboards, authentication, distributed processing, and advanced search
algorithms are deliberately outside Version 1.

## 3. System overview

```text
CLI or benchmark command
          |
Generate or read CSV datasets
          |
Load UTF-8 integer values and validate count/content
          |
Prepare independent original-order and sorted lists
          |                         |
    Linear search             Binary search
    (original order)          (ascending copy)
          \                         /
       Measure search calls and verify result consistency
                          |
       Display results or export CSV + metadata
```

The interactive path displays measurements and writes no files. The benchmark
path measures every required dataset and target case, then writes
`results/performance_results.csv` and `results/benchmark_metadata.json`.
Loading, validation, sorting, and output are outside the displayed search
timing. Sorting cost is recorded separately so it can be discussed in a total
workload recommendation.

## 4. Repository responsibilities

| Area | Responsibility |
| --- | --- |
| `main.py` | Routes interactive, preview, generation, and benchmark commands. |
| `src/data_generator.py` | Generates seeded integer lists and one-column CSV files. |
| `src/data_loader.py` | Reads strict UTF-8 integer CSV input and reports data errors. |
| `src/data_processor.py` | Validates values and creates independent original/sorted lists. |
| `src/linear_search.py` | Sequential search; returns the first matching original-order index. |
| `src/binary_search.py` | Midpoint search on ascending data; returns any matching sorted-list index. |
| `src/performance_timer.py` | Correctness check, warm-ups, timed batches, and median batch means. |
| `src/results_manager.py` | Validates benchmark records and writes the exact CSV schema. |
| `src/benchmark.py` | Runs all cases and records metadata, raw samples, and hashes. |
| `src/cli.py` | Handles menu input, recovery, result display, and repeated searches. |
| `data/` | Reproducible 100-, 1,000-, and 10,000-value CSV inputs. |
| `results/` | Published benchmark CSV and provenance metadata. |
| `tests/` | Standard-library `unittest` coverage for algorithms and pipeline behavior. |
| `docs/` | Requirements, architecture, analysis, operating instructions, report, and evidence. |

## 5. Data contract

The supplied datasets use UTF-8 CSV with the exact header `value` and one signed
integer per row. The generator uses `random.Random(42)`, an inclusive range of
0 through 100,000, and allows duplicates. The seed is restarted for each
required size, so the smaller datasets are reproducible prefixes of the larger
ones. The loader accepts a UTF-8 BOM and surrounding cell whitespace but
rejects empty files, blank rows, extra columns, invalid headers, fractions,
text, and invalid encoding.

The processor preserves the input order and creates a separate ascending list.
This matters because a match's index belongs to the list that was actually
searched. Linear search reports the first duplicate in original order; binary
search may report any matching duplicate in sorted order.

## 6. Algorithm contracts and complexity

### Linear search

Linear search examines values from left to right and returns as soon as it
finds the target. Its best case is O(1), average case is O(n) under a uniform
successful-target position assumption, and worst case is O(n). It accepts
unsorted data and uses O(1) auxiliary search space.

### Binary search

Binary search requires an ascending sequence. It compares the target with the
middle value and discards the half that cannot contain the target. Its best
case is O(1), average and worst cases are O(log n), and auxiliary search space
is O(1). It does not sort or verify ordering inside the search function.

### Preparation cost

Creating the sorted copy takes O(n) additional space and sorting costs
O(n log n) in the worst case. For one search, direct linear search can be less
work than sorting first. For a stable dataset reused across many searches, the
comparison is approximately `q * L` versus `S + q * B`, where `S` is sorting
cost and `L`/`B` are representative linear/binary search costs. The current
interactive menu prepares both copies for each selection; it does not cache a
sorted list between selections.

See [big_o_analysis.md](big_o_analysis.md) and
[recommendation_guide.md](recommendation_guide.md) for the measured evidence
and workload guidance.

## 7. Benchmark design

The benchmark uses four cases for each dataset: the first, middle, and last
values in original order, plus `max(data) + 1` as an absent target. Both
algorithms receive the same target. Linear search receives the original list;
binary search receives the sorted copy. Algorithm order alternates across
cases to reduce a fixed ordering effect.

The default timer performs one untimed correctness call, three warm-ups, and
seven timed batches of 100 calls. Each result is the median of the seven batch
means in seconds per search. Raw batch values, environment details, settings,
case mapping, dataset hashes, source hashes, and the exported CSV hash are
stored in the metadata sidecar.

The saved benchmark contains 24 rows: 3 sizes x 4 cases x 2 algorithms. The
published Day 4 run is retained as dated evidence. Day 7 also ran a complete
24-row benchmark in temporary output and verified each row without replacing
the published evidence.

## 8. User interface behavior

The menu asks for a dataset size, signed integer target, and linear, binary, or
comparison mode. Invalid options and noninteger targets are re-prompted. Zero
and negative targets are valid. Missing or malformed data returns the user to
the dataset menu with a clear message. `q`, EOF, and Ctrl+C exit cleanly.

Each displayed result includes the algorithm, found status, index, index-list
meaning, and seconds per search. An index of zero is a successful result.
Interactive searches do not overwrite datasets or saved benchmark results.

## 9. Quality and evidence

The project has 73 passing tests covering dataset generation/loading,
validation, sorting, search boundaries and duplicates, logarithmic binary
read bounds, timing arithmetic, benchmark export, metadata, menu recovery,
and command routing. The final portfolio also includes application captures,
the architecture diagram, the Big O analysis, the recommendation guide, and
the [Day 7 validation checklist](day_7_checklist.md).

Version 1.0.0 is represented by the annotated `v1.0.0` tag. See
[release_notes.md](release_notes.md) for the release boundary and included
deliverables.
