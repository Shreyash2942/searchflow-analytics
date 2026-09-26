# Day 7: final validation, screenshots, documentation, and release

Completes the Version 1 portfolio milestone and records the final acceptance
evidence. The release tag is `v1.0.0`.

## Completed quality gate

- [x] Run the full automated test suite: 73 tests pass.
- [x] Run a complete 24-row benchmark in a temporary output directory.
- [x] Verify every fresh row, found/index result, raw measurement set, and CSV hash.
- [x] Review source functions: all `main.py` and `src/` functions have docstrings.
- [x] Capture the required application and benchmark screenshots under this directory.
- [x] Review README setup, examples, architecture, measurements, screenshots, and status.
- [x] Verify every Version 1 requirement against a repository deliverable.
- [x] Commit the final work in focused commits and push `main` to GitHub.
- [x] Create and push the annotated `v1.0.0` release tag.

## Screenshot evidence

| Evidence | File |
| --- | --- |
| Linear search, 100 elements, successful target | [linear_100_success.png](screenshots/linear_100_success.png) |
| Binary search, 1,000 elements, successful target | [binary_1000_success.png](screenshots/binary_1000_success.png) |
| Both algorithms, 10,000 elements, successful target | [both_10000_success.png](screenshots/both_10000_success.png) |
| Missing target in the interactive comparison | [missing_target.png](screenshots/missing_target.png) |
| Application menu and exit path | [main_menu.png](screenshots/main_menu.png) |
| Final saved benchmark results | [final_benchmark_results.png](screenshots/final_benchmark_results.png) |

The images were rendered from actual subprocess output by
[`render_terminal.py`](screenshots/render_terminal.py). Search timings are live
observations and vary by run; the saved CSV and metadata remain the source of
record for the published benchmark evidence.

## Validation record

From the repository root on 2026-09-26:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Result: **73 tests passed**. A fresh run of `run_benchmarks` covered all three
datasets, four target cases, and both algorithms (24 rows) in a temporary
directory. It verified each result against the correct original or sorted
input, checked all 24 raw measurement sets, and matched the generated CSV
SHA-256. Existing published benchmark files were not overwritten, preserving
the dated Day 4 run used by the analysis.

An AST-based review found no missing function docstrings in `main.py` or
`src/`. Requirement coverage is recorded in the
[Version 1 requirements](requirements.md), with analysis and recommendation
evidence linked from the README.

## Release

Focused Day 7 commits cover screenshots, the final README, and validation.
The annotated tag `v1.0.0` points to the validation commit and is pushed to
the configured GitHub remote. Day 7 closes the planned Version 1 scope;
cloud services, databases, APIs, dashboards, and advanced search remain
outside this release.
