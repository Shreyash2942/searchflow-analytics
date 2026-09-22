# Dataset format and reproducibility

The portfolio uses `dataset_100.csv`, `dataset_1000.csv`, and
`dataset_10000.csv`, containing exactly 100, 1,000, and 10,000 values respectively.
The header does not count as a data element.

## File contract

- UTF-8 CSV; a single column headed exactly `value`.
- One signed decimal integer per record. The loader accepts an optional UTF-8
  BOM, quoted integer cells, and surrounding whitespace in integer cells.
- Empty datasets, blank records, extra columns, fractions, and nonnumeric cells
  are rejected. In-memory validation also rejects booleans.
- Negative integers and duplicate values are valid inputs. The supplied
  generator defaults to the inclusive range 0–100,000.

Example of the format, not a benchmark result:

```csv
value
8
3
8
```

## Generation settings

| Setting | Included datasets |
| --- | --- |
| Generator | Python standard-library `random.Random` |
| Seed | 42, restarted independently for each size |
| Minimum / maximum | 0 / 100,000 inclusive |
| Duplicates | Allowed; no deduplication |
| Generation environment | Python 3.14.4 |

The smaller datasets are prefixes of the larger ones because each call restarts
the same seed. This makes the input family reproducible; it is not three
independent random samples. Generation uses a local random-number generator,
so it does not change global random state. The same settings reproduce the
same values in the same Python environment; keep the included CSV files for
comparisons across environments.

From the repository root, regenerate all three files with:

```powershell
.\.venv\Scripts\python.exe main.py --generate
```

This replaces the three named CSVs. Running without `--generate` reads and
validates them without modification.

## Reusable functions

```python
from src.data_generator import generate_dataset, save_dataset
from src.data_loader import load_dataset
from src.data_processor import prepare_search_data

values = generate_dataset(100, seed=42)
save_dataset(values, "data/dataset_100.csv")
loaded = load_dataset("data/dataset_100.csv", expected_size=100)
original, ordered = prepare_search_data(loaded, expected_size=100)
```

`original` preserves input order, while `ordered` is ascending. Both are new
lists, independent of each other and `loaded`; duplicates are retained. Sorted
copies stay in memory for binary search, while the stored CSV retains original
order. Indexes in the two lists may differ for the same value.

Invalid CSV contents or count mismatches raise `ValueError`. A missing file
raises `FileNotFoundError`; other filesystem errors retain their `OSError`
subtype. The entry point catches these expected failures and reports them
without a traceback. `save_dataset` validates values before opening a file.
