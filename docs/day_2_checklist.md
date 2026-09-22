# Day 2: dataset generation and data processing

Implements Day 2 of the supplied portfolio plan and FR-01, FR-09, and FR-10
in [the repository requirements](requirements.md).

## Completed quality gate

- [x] Generate reproducible random integer datasets with a local seeded generator.
- [x] Store all three required CSV datasets: 100, 1,000, and 10,000 values.
- [x] Load CSV files as integers and validate exact expected counts.
- [x] Reject empty/invalid data, incorrect headers, blank rows, and extra columns.
- [x] Handle missing files and malformed data clearly at the entry point.
- [x] Preserve original data order and create an independent ascending sorted copy.
- [x] Document format, seed, range, duplicates, and error behavior.
- [x] Verify the data pipeline with 21 automated tests.

## Delivered files

- `src/data_generator.py`: random generation, validated CSV writing, and generation of all required sizes.
- `src/data_loader.py`: strict CSV loading, integer conversion, validation, and count checking.
- `src/data_processor.py`: validation and independent original/sorted lists.
- `data/dataset_100.csv`, `data/dataset_1000.csv`, `data/dataset_10000.csv`.
- `tests/test_data_pipeline.py`: generation, CSV, preprocessing, and entry-point tests.
- `main.py`: run the data pipeline, or regenerate and run it with `--generate`.
- [Dataset documentation](../data/README.md) and updated README/architecture/contracts.

## Validation record

Verified with Python 3.14.4 on Windows, using the existing `.venv`:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe main.py --generate
.\.venv\Scripts\python.exe main.py
```

All 21 tests passed. All three generated files loaded with the exact expected
counts. Regeneration with the same settings produced identical bytes in the
temporary test directory. The application also ran from the parent directory,
confirming resource paths do not depend on the terminal's working directory.

These are data-pipeline checks, not algorithm-performance measurements. Search
algorithms are the next increment (Day 3); timing and result CSVs follow on Day 4.
