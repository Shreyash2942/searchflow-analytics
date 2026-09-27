# SearchFlow Analytics: final project report

## Executive summary

SearchFlow Analytics is a local Python implementation of a small search
performance data pipeline. It generates three reproducible integer datasets,
loads and validates CSV input, compares linear search with binary search, and
records measured results. The project demonstrates that algorithm choice is a
workload decision: binary search scales better for repeated lookups on sorted
data, while linear search is attractive for unsorted data, small inputs, or an
early match where sorting would cost more than the lookup saves.

The Version 1 release contains the application, benchmark evidence, automated
tests, analysis, recommendations, screenshots, and an annotated `v1.0.0` tag.

## Problem and motivation

A search algorithm can look better in theory while being a poor choice for a
particular workload. Linear search needs no preparation but may inspect every
value. Binary search reduces the search interval logarithmically, but it needs
ascending data and often requires sorting or maintaining that order first.
This project makes those trade-offs visible using one consistent pipeline and
three dataset sizes rather than presenting complexity as an isolated formula.

## Implementation

The pipeline has four stages:

1. **Generate or load data.** A local seeded random generator creates 100,
   1,000, and 10,000 integers in the inclusive range 0–100,000. The loader
   enforces a strict one-column integer CSV contract.
2. **Validate and prepare.** The processor rejects invalid values and counts,
   preserves the original list, and creates an independent ascending copy.
3. **Search and measure.** Linear search receives original order; binary search
   receives sorted order. The timer performs correctness checks, warm-ups, and
   repeated batches using `time.perf_counter()`.
4. **Display or export.** The CLI displays found status, index, and time. The
   benchmark exports 24 rows plus raw samples, sort timings, environment data,
   and hashes.

## Complexity analysis

| Algorithm | Best | Average | Worst | Search space | Precondition |
| --- | --- | --- | --- | --- | --- |
| Linear | O(1) | O(n) | O(n) | O(1) | None beyond valid sequence |
| Binary | O(1) | O(log n) | O(log n) | O(1) | Ascending sorted sequence |

The average cases assume a uniform successful target position. A missing linear
target scans the full list. Binary search halves the remaining interval after
each midpoint comparison. Preparing a sorted copy adds O(n) space and sorting
costs O(n log n) in the worst case.

## Measured findings

The published benchmark was captured on 2026-09-24 using Python 3.14.4. Each
CSV value is the median of seven batch means, with 100 calls per batch, three
warm-ups, and one untimed correctness call. Values below are microseconds per
search rounded to three decimals; preparation and output are excluded.

| Dataset size | First target: linear | First target: binary | Missing: linear | Missing: binary |
| ---: | ---: | ---: | ---: | ---: |
| 100 | 0.077 | 0.316 | 1.532 | 0.321 |
| 1,000 | 0.115 | 0.674 | 17.587 | 0.512 |
| 10,000 | 0.119 | 0.864 | 179.697 | 0.699 |

The first target is the first value in original order. Linear search returns
immediately at index zero, so it wins that case. For missing targets, linear
time grows sharply as the input grows, while binary time changes much less.
Those observations support the theoretical growth rates but do not prove them
from timings alone. The benchmark uses selected cases and one seeded dataset
family rather than a statistical sample of all possible workloads.

## Recommendations

Use linear search when data is unsorted, the dataset is small, only a few
lookups are needed, or early matches are common. Use binary search when data is
already sorted, the dataset is large, or many queries can reuse one sorted
copy. Include sorting time, update cost, memory, and index requirements in the
decision. The current interactive menu prepares data for each selection, so it
does not implement cross-selection sorted-list reuse.

## Testing and validation

The final suite contains 73 passing tests. It covers:

- generation, reproducibility, CSV round trips, malformed input, and counts;
- linear and binary boundary cases, duplicates, empty input, and immutability;
- logarithmic binary indexed-read bounds;
- timing arithmetic, correctness checks, warm-ups, and invalid settings;
- benchmark row schema, medians, hashes, index correctness, and failure safety;
- interactive choices, invalid input recovery, missing files, repeated searches,
  EOF/Ctrl+C, command routing, and file preservation.

Day 7 also ran a fresh complete 24-row benchmark in temporary output, verified
the rows against the correct original/sorted inputs, checked raw measurement
sets and the generated CSV hash, and preserved the dated published benchmark
files used by the analysis. An AST review found docstrings on every function
in `main.py` and `src/`.

## Requirements and scope outcome

All Version 1 functional requirements are delivered: data generation, both
search algorithms, interactive selection, timing, CSV results, comparisons at
all required sizes, safe loading, validation/sorted preparation, Big O
analysis, and recommendations. The final README, architecture diagram,
screenshots, test suite, report, and release tag satisfy the submission
documentation requirements.

Version 1 remains intentionally local and standard-library based. Cloud
deployment, databases, APIs, web dashboards, authentication, containers,
CI/CD, distributed processing, and advanced search are future scope rather
than unfinished Version 1 requirements.

## Conclusion

The project meets its portfolio objective: it connects implementation,
measurement, theory, and practical recommendation. Its evidence shows why
binary search is valuable for large repeated-query workloads while preserving
the simpler linear approach when ordering and preparation costs dominate.

Supporting files: [benchmark methodology](benchmark_methodology.md),
[Big O analysis](big_o_analysis.md), [recommendation guide](recommendation_guide.md),
[run instructions](run_instructions.md), and
[release notes](release_notes.md).
