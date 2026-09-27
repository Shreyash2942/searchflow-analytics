# SearchFlow Analytics: A Measured Comparison of Linear and Binary Search

**Shreyash2942**

CSU Global

CSC506 Design and Analysis of Algorithms

Module 2 Portfolio Milestone
September 27, 2026

## Abstract

SearchFlow Analytics is a local Python data pipeline created to connect search
algorithm theory with measured workload behavior. The project generates
reproducible integer datasets containing 100, 1,000, and 10,000 values; loads
and validates those values as CSV input; prepares original-order and sorted
search views; and compares linear search with binary search. The benchmark
records 24 search results, raw timing samples, sorting measurements, and file
hashes. In the captured run, linear search was fastest when the target appeared
at the first original position, while binary search was substantially faster
for missing targets as the dataset grew. The results support the expected
O(n) average and worst-case behavior of linear search and O(log n) average and
worst-case behavior of binary search. They also show why sorting cost and
query frequency must be included in a practical recommendation. The final
Version 1 release contains the application, 73 passing tests, benchmark
evidence, technical documentation, screenshots, and an annotated `v1.0.0`
tag.

*Keywords:* linear search, binary search, algorithm analysis, benchmarking, Python, data pipeline

## Introduction

Algorithm analysis provides a way to reason about how computational work grows
as input size increases. Asymptotic notation is useful for comparing search
strategies, but a practical decision also depends on data ordering,
preparation, query frequency, memory, and the location of successful targets.
The standard analysis of sequential and divide-and-conquer search provides the
theoretical foundation for this comparison (Cormen et al., 2022). SearchFlow
Analytics was developed to make those trade-offs visible in a small,
reproducible application.

## Project Purpose and Motivation

The purpose of the project was to build a complete search-performance pipeline
for a Design and Analysis of Algorithms portfolio. The project asks when a
simple linear scan is sufficient and when binary search justifies the
preparation required by sorted data. This question matters because a faster
search operation can still produce more total work when a list must first be
sorted and only one lookup is needed.

The project has five goals. First, it creates reproducible datasets at three
required sizes. Second, it implements nonmutating linear and binary search
functions with explicit index contracts. Third, it measures search calls using
a repeatable timing protocol. Fourth, it makes the comparison accessible from
an interactive command-line interface. Fifth, it connects the measured values
to complexity analysis and workload recommendations. The Version 1 boundary
deliberately excludes cloud deployment, databases, web dashboards,
authentication, distributed processing, and advanced search algorithms.

## System Design and Implementation

The application follows four stages. The generator uses a local seeded random
number generator to create integer lists of 100, 1,000, and 10,000 values in
the inclusive range 0 through 100,000. The loader reads a UTF-8 CSV with the
exact `value` header and rejects invalid headers, blank rows, extra columns,
malformed integers, empty data, and count mismatches. The processor validates
the values, preserves the original order, and creates an independent ascending
copy.

The search stage sends original-order data to linear search and the sorted copy
to binary search. Linear search returns the first matching index or `-1` after
checking values from left to right. Binary search compares the target with the
middle value and repeatedly narrows the remaining interval. It requires
ascending input and can return any matching index when duplicates exist. Both
functions are iterative, nonmutating, and use constant auxiliary search space.

The measurement stage performs one untimed correctness check, three warm-up
calls, and seven timed batches of 100 calls. The reported value is the median
of the batch means in seconds per search. The timer includes Python call and
loop overhead but excludes loading, validation, sorting, result checks, CSV
writes, and terminal output. The benchmark records the first, middle, and last
original-order values plus `max(data) + 1` as an absent target for each size.
It alternates algorithm order across cases and stores raw samples and
provenance metadata (Shreyash2942, 2026b).

## Algorithms and Complexity

Linear search has a best-case time of O(1) when the first value matches. Under
the assumption that a successful target is equally likely to occur at any
position, its average time is O(n), and a missing target or final-position
match requires O(n) work. It needs no ordering precondition and uses O(1)
auxiliary search space.

Binary search has a best-case time of O(1) when the initial midpoint matches.
Each unsuccessful comparison removes approximately half of the remaining
range, giving O(log n) average and worst-case time under the usual constant-time
indexing assumption. Its auxiliary search space is O(1), but its input must be
sorted. Sorting a copy adds O(n) space and O(n log n) worst-case preparation
time. Therefore, one sorted binary search has total preparation-and-search
work that can exceed one direct linear scan.

## Benchmark Method

The published benchmark used the three included datasets and was captured on
September 24, 2026, using Python 3.14.4 on Windows 11. It measured 3 dataset
sizes x 4 target cases x 2 algorithms, resulting in 24 CSV rows. The saved
metadata records the timing settings, raw samples, sorting samples, platform,
dataset hashes, source hashes, and CSV hash (Shreyash2942, 2026a).

The benchmark is evidence about the selected cases rather than a statistical
sample of every workload. The three datasets share a seeded prefix, and the
present targets are selected positions rather than random successful queries.
Duplicates can cause linear search to find an earlier occurrence, while sorting
changes the index used by binary search. These limits are why the report uses
the measurements to illustrate the theoretical analysis rather than claiming a
universal timing threshold.

## Results

Table 1 summarizes the saved execution times in microseconds per search. The
values are rounded to three decimals for presentation; the CSV preserves full
floating-point precision. “First target” means the first value in original
order. Preparation and output are excluded from these search-only values.

**Table 1**
*Selected search times by dataset size*

| Dataset size | First target: linear | First target: binary | Missing: linear | Missing: binary |
| ---: | ---: | ---: | ---: | ---: |
| 100 | 0.077 | 0.316 | 1.532 | 0.321 |
| 1,000 | 0.115 | 0.674 | 17.587 | 0.512 |
| 10,000 | 0.119 | 0.864 | 179.697 | 0.699 |

Linear search wins the first-target case because it returns immediately at
original index zero. The result demonstrates the best-case behavior of a
sequential scan even at the largest input size. Binary search is faster for
the missing target at every size. As the data grows from 100 to 10,000 values,
missing-target linear time rises from 1.532 to 179.697 microseconds, while
binary time rises from 0.321 to 0.699 microseconds. The growth pattern is
consistent with O(n) versus O(log n), although hardware timing alone cannot
prove those bounds.

## Recommendations

Linear search is a reasonable choice for unsorted data, small datasets, one or
a few lookups, or workloads where targets commonly occur near the beginning.
It avoids sorting and preserves original-order indexes. Binary search is a
reasonable choice when data is already sorted, the dataset is large, or many
lookups can reuse one sorted copy. A production decision should include
sorting, update, memory, and index-mapping costs.

For a stable dataset reused across queries, the simplified comparison is
`qL` for repeated linear searches versus `S + qB` for one sort followed by
binary searches. Here, `S` is sorting cost, `L` is representative linear time,
and `B` is representative binary time. The current menu prepares data for
each selection and does not cache a sorted copy, so this reuse model is a
recommendation for a possible workload rather than a claim about current menu
behavior.

## Testing and Quality Assurance

The final automated suite contains 73 passing tests. It verifies generation,
reproducibility, CSV loading, validation, sorted-copy independence, search
boundaries, duplicates, empty inputs, binary indexed-read bounds, timing
arithmetic, benchmark schemas, raw-sample medians, hashes, CLI recovery,
repeated searches, and file preservation. A Day 7 temporary benchmark rerun
covered all 24 cases and verified every result against the correct original or
sorted input without replacing the dated published benchmark.

An AST review found docstrings on every function in `main.py` and `src/`. The
final repository includes the source modules, datasets, result files,
architecture diagram, run guide, technical documentation, screenshots, and
release notes. The annotated `v1.0.0` tag marks the Version 1 release
(Shreyash2942, 2026c).

## Limitations and Future Work

The benchmark uses one seeded dataset family and a small set of selected
targets. It does not estimate a universal crossover point across hardware,
languages, data distributions, or query mixes. The timer includes Python call
and loop overhead, and the smallest timings are close to clock-resolution and
scheduling effects. The benchmark also measures search-only time separately
from sorting, so total end-to-end cost must be interpreted using the metadata.

Future work could evaluate independent random datasets, larger query batches,
dynamic updates, index-preserving mappings, or other search structures. Those
ideas are intentionally outside the completed Version 1 scope.

## Conclusion

SearchFlow Analytics met its portfolio objective by connecting implementation,
measurement, theory, and practical recommendation. The measured first-match
case shows why linear search can be the simplest and fastest option for a
one-off early lookup. The missing-target results show why binary search is
valuable as sorted data and repeated query volume grow. The resulting decision
is workload-sensitive: binary search is powerful, but sorting and reuse must be
part of the analysis.

## References

Cormen, T. H., Leiserson, C. E., Rivest, R. L., & Stein, C. (2022). *Introduction to algorithms* (4th ed.). The MIT Press. https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/

Shreyash2942. (2026a). *Benchmark metadata and performance results* [Data set].
GitHub. https://github.com/Shreyash2942/searchflow-analytics

Shreyash2942. (2026b). *Benchmark methodology* [Project documentation]. GitHub. https://github.com/Shreyash2942/searchflow-analytics

Shreyash2942. (2026c). *SearchFlow Analytics* [Computer software]. GitHub. https://github.com/Shreyash2942/searchflow-analytics/tree/v1.0.0

## Appendix A: Version 1 evidence

The release contains the following evidence artifacts:

- `results/performance_results.csv` — 24 measured records.
- `results/benchmark_metadata.json` — raw timing samples, settings, sort
  measurements, environment, and SHA-256 provenance hashes.
- `tests/` — 73 automated tests.
- `docs/screenshots/` — six CLI and benchmark captures.
- `diagrams/pipeline_architecture.png` — pipeline architecture diagram.
- `README.md` — setup, operating commands, and project navigation.

The complete implementation and documentation are available in the
[SearchFlow Analytics GitHub repository](https://github.com/Shreyash2942/searchflow-analytics).
