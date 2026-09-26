# Day 6: validation, Big O analysis, and recommendations

Completes Day 6 of the supplied plan: review the complete application's
tests, explain the measured comparisons (FR-08 / FR-11), and recommend
algorithms according to workload and preparation costs (FR-12).

## Completed quality gate

- [x] Confirm every required search and pipeline case has automated evidence.
- [x] Run the complete suite: all 73 tests pass on Python 3.14.4.
- [x] Explain best, average, and worst search time and auxiliary space.
- [x] Discuss actual measurements at 100, 1,000, and 10,000 elements.
- [x] Account for sorting costs and the limits of search-only timing.
- [x] Recommend choices by ordering, size, query frequency, and sorting cost.
- [x] Verify the saved benchmark's hashes, medians, and result correctness.

## Requirement-to-test audit

The existing suite already implements the required Day 6 cases. No new
runtime behavior or duplicate tests were needed. This is a requirements
audit, not a statement of line or branch coverage.

| Required behavior | Existing automated evidence |
| --- | --- |
| Linear: beginning, middle, end, unsorted input | `test_linear_search.py`: `test_beginning_middle_and_end_of_unsorted_data` |
| Linear: missing and empty input | `test_linear_search.py`: `test_missing_target`, `test_empty_input` |
| Binary: beginning, middle, end of sorted input | `test_binary_search.py`: `test_beginning_middle_and_end` |
| Binary: missing and single-element input | `test_binary_search.py`: `test_missing_below_between_and_above_values`, `test_one_and_two_element_inputs` |
| Generate all sizes and load the saved CSVs | `test_data_pipeline.py`: `test_required_sizes_are_reproducible_and_in_range`, `test_all_required_files_round_trip_and_regenerate_identically` |
| Validate content and expected counts | `test_data_pipeline.py`: `test_invalid_contents`, `test_invalid_csv_content`, `test_loaded_count_must_match` |
| Preserve original data while making a sorted copy | `test_data_pipeline.py`: `test_sorted_copy_preserves_values_duplicates_and_original_order` |
| Search original/sorted inputs at all sizes | `test_data_pipeline.py`: `test_searches_use_original_and_sorted_data_at_all_required_sizes` |
| Benchmark results and output | `test_benchmark.py`: `test_complete_run_records_real_samples_and_correct_results`; `test_results_manager.py`: `test_round_trip_exact_schema_and_timing_precision` |

All test filenames refer to [`tests/`](../tests). Additional cases cover
duplicates, negative/zero values, empty binary input, input preservation,
exhaustive small-input oracles, binary indexed-read bounds, timing arithmetic
and boundaries, file errors, and menu selection/recovery/exit behavior.
Tests assert correctness and operation bounds, not machine-dependent speed
thresholds. Integration tests run actual benchmark calls in temporary folders.

## Validation record

On 2026-09-25, from the repository root:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Result: **73 tests passed**. A separate read-only audit of the captured
Day 4 artifacts verified all 24 CSV rows against their raw-sample medians,
targets, found flags, and original/sorted indexes. All three dataset hashes,
nine recorded source hashes, the result CSV hash, and three sort medians
matched the metadata. The source hash list describes the Day 4 run and
does not claim to include the later CLI module.

The [Big O analysis](big_o_analysis.md) and
[recommendation guide](recommendation_guide.md) use that dated evidence.
No saved benchmark was regenerated for this documentation milestone.
The guide's sorting-plus-search totals and query crossover are explicitly
estimates, and sorted-list reuse is not claimed for successive CLI selections.

Day 7 remains pending: final submission checks, application screenshots,
README review, and the `v1.0.0` release.
