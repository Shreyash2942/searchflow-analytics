# Choosing linear or binary search

Choose according to data ordering, dataset size, query frequency, and the
cost of preparation. The [Big O analysis](big_o_analysis.md) explains the
bounds; the [benchmark methodology](benchmark_methodology.md) defines what
the measured times include.

## Decision guide

| Situation | Starting choice | Reason or condition |
| --- | --- | --- |
| Unsorted data; one or a few searches | Linear | Search directly without paying for sorting. |
| Small dataset; simplicity matters | Linear may suffice | A short scan is simple; measure total workload before adding preparation. |
| Target often appears near the beginning | Linear may be faster | Early exit can take constant work, even in a large list. |
| Large list already sorted ascending | Binary | O(log n) search work with the ordering cost already paid. |
| Many queries over a stable, unsorted dataset | Sort once, then binary | Reuse the sorted copy so savings can repay preparation. |
| Sorting cost is acceptable and fast repeated lookups matter | Binary after sorting | Include preparation, memory, and update costs in the decision. |
| Data changes frequently | Reassess; linear may suffice | Rebuilding sorted copies can erase lookup savings. |
| First occurrence in original order is required | Linear | Its index preserves original order and its duplicate contract is explicit. |

Binary search must receive sorted input. Its index refers to that sorted
list and may identify any duplicate match. Sorting a copy preserves the
original but adds O(n) memory; an application needing original indexes would
need an additional mapping. Neither algorithm here returns all matches.

## What this project's measurements support

In the captured Day 4 run, a missing target at 10,000 elements took about
179.697 microseconds with linear search and 0.699 microseconds with binary
search, excluding sorting. Yet the original first target took about 0.119
microseconds with linear and 0.864 with binary. Large size alone does not
determine the winner: where queries succeed matters.

The metadata separately records these median sort costs (seven individual
sorts, in microseconds). Adding sort and search medians below is an
illustrative cost estimate, not a measured end-to-end latency.

| n | Sort cost S | Missing linear L | Missing binary B | Estimated S + B |
| ---: | ---: | ---: | ---: | ---: |
| 100 | 1.200 | 1.532 | 0.321 | 1.521 |
| 1,000 | 26.500 | 17.587 | 0.512 | 27.012 |
| 10,000 | 741.000 | 179.697 | 0.699 | 741.699 |

For one missing query at 10,000 elements, this estimate favors a direct
linear scan once sorting is included. At 100 elements the estimates are
too close to justify a confident general recommendation from this run.

For a stable dataset reused across queries, compare `q * L` with
`S + q * B`. If `L > B`, the simplified model favors sorting plus binary
when `q > S / (L - B)`. Substituting the 10,000-element missing-target
measurements gives about 4.14, or five queries under these assumptions.
This is a workload-specific illustration, not a measured universal crossover:
mixed targets, changing data, preparation overhead, and timing variability
change it. If linear is faster for the chosen queries (`L <= B`), this model
offers no positive query count that repays sorting.

The current CLI is a comparison tool: every menu selection reloads the CSV
and prepares original/sorted copies, including in linear-only mode. It then
repeats searches to estimate time per call. Selecting the menu five times
does not reuse a cached sorted list or implement the cost model above.
The benchmark does reuse prepared inputs across its timed calls. Both
interfaces display search-only time, excluding preparation and output.

## Applying the guide

Use linear search for a simple one-off scan of unsorted data, especially
when the list is small or likely matches occur early. Use binary search
when the list is already sorted, or when sorting once is acceptable and
enough later searches can reuse that work. For a real application, measure
representative successful and unsuccessful queries plus loading, sorting,
updates, and memory costs before choosing.

Evidence: [saved CSV](../results/performance_results.csv) and
[raw samples / metadata](../results/benchmark_metadata.json), run completed
`2026-09-24T23:59:43.202789+00:00`. These observations cover the project's
three sizes and selected cases; they do not establish a fixed size threshold
for all machines or workloads.
