# Day 3: linear search and binary search

Implements Day 3 of the supplied portfolio plan and FR-02/FR-03 in
[the repository requirements](requirements.md).

## Completed quality gate

- [x] Linear search accepts a sequence and target and examines values sequentially.
- [x] Linear search finds existing values in unsorted data.
- [x] Linear search returns `-1` when a target is absent.
- [x] Binary search accepts ascending sorted data and a target.
- [x] Binary search calculates a midpoint and narrows the lower/upper bounds.
- [x] Binary search finds existing values and returns `-1` for missing values.
- [x] Pipeline tests pass sorted copies to binary search at all three sizes.
- [x] Document duplicate handling, index meaning, empty input, and complexity.

## Delivered files and contracts

- `src/linear_search.py`: `linear_search(data, target)` returns the first
  matching index. Best time O(1), average/worst O(n), auxiliary space O(1).
- `src/binary_search.py`: `binary_search(data, target)` returns any matching
  index. For lists/tuples with constant-time indexing, best time O(1),
  average/worst O(log n), auxiliary space O(1).
- Both functions return `-1` for missing values and empty sequences. They
  accept validated integer inputs and never change the input sequence.
- Binary search requires ascending (nondecreasing) data; it does not sort or
  scan to validate ordering. Pass the sorted copy from `prepare_search_data`.
- Duplicate handling follows ordinary early-return algorithms: linear search
  finds the first occurrence, while binary search can find another occurrence.
  Requiring the first duplicate from binary search would change its early-return
  behavior. Found status uses `index != -1`; index zero is a valid match.

The plan's examples now return the required results:

```python
linear_search([7, 2, 9, 4], 9)       # 2
binary_search([1, 3, 5, 7, 9], 7)    # 3
```

## Validation record

Verified on Python 3.14.4 with:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

All 39 tests pass: the prior 21 tests, eight linear-search tests, nine
binary-search tests, and one additional pipeline integration test. Subtests
exercise multiple inputs within these tests.

The search tests cover beginning/middle/end, absence, empty input, one/two
elements, duplicates, negatives, zero, tuples, and input preservation. Small
integer sequences are checked against independent membership/index oracles.
Binary-search indexed reads are bounded by `n.bit_length()` for tested sizes
up to 10,000; a midpoint match uses one read. These checks assess work performed,
not wall-clock performance.

The pipeline integration test generates, saves, reloads, and prepares all three
required sizes. It searches present and missing targets through both functions
using the correct input order and verifies the source data remains unchanged.

`main.py` continues to run data preparation. The README provides direct search
examples; timing/results arrive on Day 4, followed by interactive search
selection on Day 5.
