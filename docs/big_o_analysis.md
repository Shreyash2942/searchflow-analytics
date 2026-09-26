# Big O analysis: linear and binary search

SearchFlow Analytics compares two searches over integer lists of size `n`.
The analysis assumes constant-time list indexing and comparisons on the
project's bounded integers. Big O describes growth in work, not an exact
duration or a promise that one implementation always runs faster.

## Algorithm costs

| Algorithm | Best time | Average time* | Worst time | Auxiliary search space |
| --- | --- | --- | --- | --- |
| Linear search | O(1) | O(n) | O(n) | O(1) |
| Binary search | O(1) | O(log n) | O(log n) | O(1) |

*Average case assumes a successful target equally likely to occupy each
position in a list of distinct values. Duplicates and a different query
distribution can change the expected work. Missing targets require a full
linear scan and at most logarithmic binary-search work.

[`linear_search`](../src/linear_search.py) checks elements from left to right.
A match at index zero takes one check, giving O(1) best-case time. A match at
index `k` takes `k + 1` checks. Under the average-case assumption, the mean is
`(n + 1) / 2`, which grows as O(n). A missing target or a first match at the
last position requires `n` checks, giving O(n) worst-case time. No ordering is
needed, so the function works directly on unsorted data. It returns the first
matching index, including when values repeat.

[`binary_search`](../src/binary_search.py) requires ascending sorted data.
It compares the target with the midpoint, then discards the half that cannot
contain it. After `k` unsuccessful midpoint checks, the remaining interval
has at most about `n / 2**k` elements. Thus average and worst-case search work
grow logarithmically; a match at the initial midpoint gives O(1) best time.
For nonempty lists, this implementation uses at most `floor(log2(n)) + 1`
midpoint reads: 7, 10, and 14 at the three required sizes. An empty input
returns `-1` immediately in either algorithm. Binary search returns any
matching index for duplicates and does not sort or validate order itself.

Both functions are iterative and keep only a fixed number of variables, so
their auxiliary space is O(1). This excludes the input lists. Preparing the
pipeline's original-order and sorted copies uses O(n) additional space.

## Measured results and interpretation

The saved [CSV](../results/performance_results.csv) and
[metadata](../results/benchmark_metadata.json) record the run completed at
`2026-09-24T23:59:43.202789+00:00` on Python 3.14.4 / Windows 11. Each value is
the median of seven batch means, with 100 calls per batch, following three
warm-ups and an untimed correctness check. The table converts seconds to
microseconds/search and rounds to three decimals. Loading, validation,
sorting, and output are excluded; Python call/loop overhead remains included.

| n | First target: linear | First target: binary | Missing: linear | Missing: binary |
| ---: | ---: | ---: | ---: | ---: |
| 100 | 0.077 | 0.316 | 1.532 | 0.321 |
| 1,000 | 0.115 | 0.674 | 17.587 | 0.512 |
| 10,000 | 0.119 | 0.864 | 179.697 | 0.699 |

“First” means first in the original list; sorting moves that value, so it is
not the binary-search best case. Linear search immediately returns index
zero and is faster for this case at all three sizes. For missing targets,
each tenfold size increase raises linear time by about 11.5 and 10.2 times,
versus about 1.6 and 1.4 times for binary search. These observations support
the expected linear versus logarithmic growth without proving complexity
from timings alone. The code's iteration bounds provide the theoretical
reason. The original-middle and original-last cases in the CSV also favor
binary search in this run.

The benchmark uses one seeded dataset per size and four selected targets,
not a random sample of query workloads. The sizes share a generated prefix;
they are not independent dataset samples. Duplicates can move a linear
match earlier, and case labels describe original positions, not universal
best/average/worst cases for both algorithms. Scheduling, caching, and clock
resolution affect small measurements. See the
[methodology](benchmark_methodology.md) for raw-sample and reproducibility details.

## Sorting and total work

For an unsorted list, sorting first has O(n log n) worst-case time and needs
O(n) space for the sorted copy. One sort followed by one binary search
therefore has O(n log n) worst-case total work, compared with O(n) for a
single direct linear search. Sorting may be cheaper for already ordered
inputs; the worst-case bound does not predict every dataset.

If a prepared sorted list is reused for `q` queries, the worst-case totals
are O(qn) for linear searches versus O(n log n + q log n) for sorting once
and using binary search. The latter becomes attractive as query count grows.
The current menu reloads and prepares both copies for each selection, even
in linear-only mode; it does not cache the sorted list between selections.
Its displayed search timing is therefore not total menu latency. The
[recommendation guide](recommendation_guide.md) applies these distinctions
to ordering, query frequency, memory, and sorting cost.
