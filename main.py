"""Prepare datasets or run benchmarks; interactive search follows on Day 5."""

import argparse
import sys

from src.data_generator import DATASET_SIZES, DEFAULT_DATA_DIR, generate_required_datasets
from src.data_loader import load_dataset
from src.data_processor import prepare_search_data
from src.benchmark import run_benchmarks
from src.performance_timer import DEFAULT_REPEATS, DEFAULT_ITERATIONS, DEFAULT_WARMUPS
from src.results_manager import DEFAULT_RESULTS_DIR


def main() -> int:
    """Prepare data or measure both searches, reporting expected input/file errors."""
    parser = argparse.ArgumentParser(description="Prepare the SearchFlow Analytics datasets.")
    parser.add_argument(
        "--generate", action="store_true",
        help="regenerate the three required CSV files using seed 42 (replaces existing files)",
    )
    parser.add_argument("--benchmark", action="store_true", help="measure both searches and replace result files")
    parser.add_argument("--repeats", type=int, help="benchmark batches (default: 7)")
    parser.add_argument("--iterations", type=int, help="searches per batch (default: 100)")
    parser.add_argument("--warmups", type=int, help="untimed warm-up calls (default: 3)")
    args = parser.parse_args()
    if not args.benchmark and any(value is not None for value in
                                  (args.repeats, args.iterations, args.warmups)):
        parser.error("--repeats, --iterations and --warmups require --benchmark")

    print("SearchFlow Analytics")
    try:
        if args.generate:
            generate_required_datasets(DEFAULT_DATA_DIR)
            print("Generated datasets with seed 42: 100, 1,000, and 10,000 integers.")
        if args.benchmark:
            records = run_benchmarks(
                DEFAULT_DATA_DIR, DEFAULT_RESULTS_DIR,
                repeats=args.repeats if args.repeats is not None else DEFAULT_REPEATS,
                iterations=args.iterations if args.iterations is not None else DEFAULT_ITERATIONS,
                warmups=args.warmups if args.warmups is not None else DEFAULT_WARMUPS,
            )
            print("Algorithm  Size   Target  Found  Index  Seconds/search (median batch mean)")
            for row in records:
                print(f"{row.algorithm:9} {row.dataset_size:5} {row.target:7} "
                      f"{str(row.found):5} {row.index:6} {row.execution_time:.9g}")
            print(f"Saved {len(records)} measurements to {DEFAULT_RESULTS_DIR / 'performance_results.csv'}")
            print("Settings, raw samples, and separate sorting times: benchmark_metadata.json")
            return 0
        for size in DATASET_SIZES:
            path = DEFAULT_DATA_DIR / f"dataset_{size}.csv"
            loaded = load_dataset(path, expected_size=size)
            original, ordered = prepare_search_data(loaded, expected_size=size)
            print(f"{path.name}: {len(original):,} integers validated; sorted copy ready.")
            print(f"  Original first 5: {original[:5]}")
            print(f"  Sorted first 5:   {ordered[:5]}")
    except (OSError, ValueError) as exc:
        print(f"Data pipeline error: {exc}", file=sys.stderr)
        if isinstance(exc, FileNotFoundError):
            print("Run with --generate to create the required datasets.", file=sys.stderr)
        return 1

    print("Data pipeline ready. Use --benchmark to measure both search algorithms.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
