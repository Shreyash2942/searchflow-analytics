"""Generate reproducible integer datasets and store them in one-column CSV files."""

import csv
import random
from collections.abc import Sequence
from pathlib import Path

from src.data_processor import validate_dataset

DATASET_SIZES = (100, 1_000, 10_000)
DEFAULT_SEED = 42
DEFAULT_MIN_VALUE = 0
DEFAULT_MAX_VALUE = 100_000
DEFAULT_DATA_DIR = Path(__file__).resolve().parents[1] / "data"


def generate_dataset(
    size: int,
    seed: int = DEFAULT_SEED,
    min_value: int = DEFAULT_MIN_VALUE,
    max_value: int = DEFAULT_MAX_VALUE,
) -> list[int]:
    """Return size random integers in the inclusive range, allowing duplicates.

    The same settings reproduce the same data in the same Python environment.
    A local Random instance leaves the caller's global random state unchanged.
    Raise ValueError for noninteger settings, a nonpositive size, or reversed
    bounds. A fixed seed is deliberate so portfolio datasets are reproducible.
    """
    for name, value in (("size", size), ("seed", seed),
                        ("min_value", min_value), ("max_value", max_value)):
        if type(value) is not int:
            raise ValueError(f"{name} must be an integer.")
    if size <= 0:
        raise ValueError("Dataset size must be positive.")
    if min_value > max_value:
        raise ValueError("Minimum value must not exceed maximum value.")
    rng = random.Random(seed)
    return [rng.randint(min_value, max_value) for _ in range(size)]


def save_dataset(data: Sequence[int], path: str | Path) -> Path:
    """Write UTF-8 CSV with a value header, replacing the destination if present.

    Validate before opening the destination so invalid input cannot truncate an
    existing dataset. Create parent folders as needed; propagate filesystem errors.
    """
    validate_dataset(data)
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(["value"])
        writer.writerows((value,) for value in data)
    return destination


def generate_required_datasets(
    output_dir: str | Path = DEFAULT_DATA_DIR, seed: int = DEFAULT_SEED
) -> list[Path]:
    """Generate and save all three required sizes in ascending size order.

    Each dataset restarts the same seed, so smaller datasets are prefixes of
    larger ones. Existing dataset_*.csv files for these sizes are replaced.
    """
    output_dir = Path(output_dir)
    return [
        save_dataset(generate_dataset(size, seed=seed), output_dir / f"dataset_{size}.csv")
        for size in DATASET_SIZES
    ]
