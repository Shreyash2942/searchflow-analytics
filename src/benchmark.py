"""Benchmark both searches on every required dataset and record run provenance."""

import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from math import isfinite
from pathlib import Path
from statistics import median
from time import get_clock_info, perf_counter

from src.binary_search import binary_search
from src.data_generator import DATASET_SIZES, DEFAULT_DATA_DIR
from src.data_loader import load_dataset
from src.data_processor import prepare_search_data
from src.linear_search import linear_search
from src.performance_timer import (
    DEFAULT_ITERATIONS, DEFAULT_REPEATS, DEFAULT_WARMUPS,
    time_search, validate_timing_settings,
)
from src.results_manager import BenchmarkResult, DEFAULT_RESULTS_DIR, save_results


def run_benchmarks(
    data_dir: str | Path = DEFAULT_DATA_DIR,
    output_dir: str | Path = DEFAULT_RESULTS_DIR,
    *,
    repeats: int = DEFAULT_REPEATS,
    iterations: int = DEFAULT_ITERATIONS,
    warmups: int = DEFAULT_WARMUPS,
) -> list[BenchmarkResult]:
    """Measure 3 sizes x 4 target cases x 2 algorithms and save 24 CSV rows.

    Cases use the first/middle/last ORIGINAL values and max(data)+1 (missing).
    They are input positions, not guaranteed algorithm best/average/worst cases.
    Alternate which algorithm is measured first between cases. Keep original
    and sorted input separate; metadata maps CSV rows to cases and raw samples.
    Existing output is replaced only after all datasets have been benchmarked.
    """
    validate_timing_settings(repeats, iterations, warmups)
    clock = get_clock_info("perf_counter")
    metadata = {
        "started_at_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version, "platform": platform.platform(),
        "timer": "time.perf_counter", "units": "seconds per search",
        "statistic": "median of batch means", "repeats": repeats,
        "iterations_per_batch": iterations, "warmup_calls": warmups,
        "untimed_correctness_calls": 1,
        "clock_resolution_seconds": clock.resolution,
        "clock_implementation": clock.implementation,
        "timing_scope": "search calls plus Python loop/call overhead; excludes preprocessing and output",
        "algorithm_order": "alternates by dataset index plus case index",
        "datasets": [], "measurements": [],
    }
    records = []
    for dataset_index, size in enumerate(DATASET_SIZES):
        path = Path(data_dir) / f"dataset_{size}.csv"
        before_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        data = load_dataset(path, expected_size=size)
        if hashlib.sha256(path.read_bytes()).hexdigest() != before_hash:
            raise ValueError(f"Dataset changed while being loaded: {path.name}")
        original, ordered = prepare_search_data(data, expected_size=size)
        sort_samples = []
        for _ in range(repeats):
            start = perf_counter()
            sorted_copy = sorted(original)
            elapsed = perf_counter() - start
            if not isfinite(elapsed) or elapsed < 0:
                raise ValueError("Clock produced an invalid sort time.")
            sort_samples.append(elapsed)
            del sorted_copy  # Deallocation is outside the timed region.
        metadata["datasets"].append({
            "file": path.name, "size": size, "sha256": before_hash,
            "sort_seconds": median(sort_samples), "sort_samples_seconds": sort_samples,
        })
        cases = (("original_first", original[0]),
                 ("original_middle", original[size // 2]),
                 ("original_last", original[-1]), ("missing_above_max", ordered[-1] + 1))
        for case_index, (case, target) in enumerate(cases):
            algorithms = [("Linear", linear_search, original), ("Binary", binary_search, ordered)]
            if (dataset_index + case_index) % 2:
                algorithms.reverse()
            for name, search, values in algorithms:
                timing = time_search(search, values, target, repeats=repeats,
                                     iterations=iterations, warmups=warmups)
                records.append(BenchmarkResult(name, size, target, timing.index != -1,
                                               timing.index, timing.execution_time))
                metadata["measurements"].append({
                    "csv_row": len(records), "case": case, "algorithm": name,
                    "dataset_size": size, "target": target,
                    "batch_seconds_per_search": timing.samples,
                })
    source_dir = Path(__file__).resolve().parent
    metadata["source_sha256"] = {
        path.name: hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(source_dir.glob("*.py"))
    }
    metadata["completed_at_utc"] = datetime.now(timezone.utc).isoformat()
    csv_path = save_results(records, Path(output_dir) / "performance_results.csv")
    metadata["csv_sha256"] = hashlib.sha256(csv_path.read_bytes()).hexdigest()
    (Path(output_dir) / "benchmark_metadata.json").write_text(
        json.dumps(metadata, indent=2, allow_nan=False) + "\n", encoding="utf-8"
    )
    return records
