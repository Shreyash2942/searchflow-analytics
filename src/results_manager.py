"""Validate and write the required benchmark CSV schema."""

import csv
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from math import isfinite
from pathlib import Path

RESULT_COLUMNS = ("algorithm", "dataset_size", "target", "found", "index", "execution_time")
DEFAULT_RESULTS_DIR = Path(__file__).resolve().parents[1] / "results"


@dataclass(frozen=True)
class BenchmarkResult:
    """One measured search result; execution_time is seconds per search."""

    algorithm: str
    dataset_size: int
    target: int
    found: bool
    index: int
    execution_time: float

    def __post_init__(self) -> None:
        """Enforce consistent index/found fields and finite nonnegative timing."""
        if self.algorithm not in ("Linear", "Binary"):
            raise ValueError("Algorithm must be Linear or Binary.")
        if type(self.dataset_size) is not int or self.dataset_size <= 0:
            raise ValueError("Dataset size must be a positive integer.")
        if type(self.target) is not int:
            raise ValueError("Target must be an integer.")
        if type(self.index) is not int or not -1 <= self.index < self.dataset_size:
            raise ValueError("Index must be -1 or within the dataset.")
        if type(self.found) is not bool or self.found != (self.index != -1):
            raise ValueError("Found status must agree with the returned index.")
        if (type(self.execution_time) not in (int, float)
                or not isfinite(self.execution_time) or self.execution_time < 0):
            raise ValueError("Execution time must be finite and nonnegative.")


def save_results(records: Iterable[BenchmarkResult], path: str | Path) -> Path:
    """Replace a CSV with validated records and the exact required header.

    Materialize and validate before opening the output; invalid records cannot
    truncate existing results. Filesystem errors propagate to the entry point.
    """
    rows = list(records)
    if not rows:
        raise ValueError("At least one benchmark result is required.")
    if any(not isinstance(row, BenchmarkResult) for row in rows):
        raise TypeError("Results must be BenchmarkResult records.")
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=RESULT_COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(asdict(row) for row in rows)
    return destination
