"""Run the Day 2 data pipeline; interactive search selection follows on Day 5."""

import argparse
import sys

from src.data_generator import DATASET_SIZES, DEFAULT_DATA_DIR, generate_required_datasets
from src.data_loader import load_dataset
from src.data_processor import prepare_search_data


def main() -> int:
    """Optionally regenerate CSV files, then validate and preview both data orders."""
    parser = argparse.ArgumentParser(description="Prepare the SearchFlow Analytics datasets.")
    parser.add_argument(
        "--generate", action="store_true",
        help="regenerate the three required CSV files using seed 42 (replaces existing files)",
    )
    args = parser.parse_args()

    print("SearchFlow Analytics")
    try:
        if args.generate:
            generate_required_datasets(DEFAULT_DATA_DIR)
            print("Generated datasets with seed 42: 100, 1,000, and 10,000 integers.")
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

    print("Data pipeline ready. Search functions are available; timing follows on Day 4.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
