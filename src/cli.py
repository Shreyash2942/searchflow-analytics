"""Interactive dataset selection and timed searches using the existing pipeline."""

import re
import sys
from pathlib import Path

from src.binary_search import binary_search
from src.data_generator import DATASET_SIZES, DEFAULT_DATA_DIR
from src.data_loader import load_dataset
from src.data_processor import prepare_search_data
from src.linear_search import linear_search
from src.performance_timer import DEFAULT_ITERATIONS, DEFAULT_REPEATS, time_search
from src.results_manager import BenchmarkResult


def search_dataset(
    size: int, target: int, mode: str, data_dir: str | Path = DEFAULT_DATA_DIR
) -> list[BenchmarkResult]:
    """Load/prepare one dataset and time linear, binary, or both search methods.

    Return measured records without writing files. Binary search always receives
    the sorted copy; linear search receives original order. Timing uses the
    same defaults and boundaries as the full benchmark command.
    """
    if type(size) is not int or size not in DATASET_SIZES:
        raise ValueError("Dataset size must be 100, 1000, or 10000.")
    if type(target) is not int:
        raise ValueError("Target must be an integer.")
    if mode not in ("linear", "binary", "both"):
        raise ValueError("Search mode must be linear, binary, or both.")
    data = load_dataset(Path(data_dir) / f"dataset_{size}.csv", expected_size=size)
    original, ordered = prepare_search_data(data, expected_size=size)
    algorithms = []
    if mode in ("linear", "both"):
        algorithms.append(("Linear", linear_search, original))
    if mode in ("binary", "both"):
        algorithms.append(("Binary", binary_search, ordered))
    results = []
    for name, search, values in algorithms:
        timing = time_search(search, values, target)
        results.append(BenchmarkResult(name, size, target, timing.index != -1,
                                       timing.index, timing.execution_time))
    return results


def _read_choice(prompt: str, choices: dict[str, object]) -> str | None:
    """Prompt until a listed choice or q is entered; None means quit."""
    while True:
        answer = input(prompt).strip().lower()
        if answer == "q":
            return None
        if answer in choices:
            return answer
        print("Invalid option. Choose " + ", ".join(choices) + ", or q to quit.")


def _read_target() -> int | None:
    """Accept a signed decimal integer (including zero), or q to quit."""
    while True:
        answer = input("Enter value to search (q to quit): ").strip()
        if answer.lower() == "q":
            return None
        if re.fullmatch(r"[+-]?[0-9]+", answer):
            try:
                return int(answer)
            except ValueError:
                pass  # Python may reject integers exceeding its digit limit.
        print("Enter a whole number, such as 42, 0, or -7, or q to quit.")


def _display_results(size: int, target: int, results: list[BenchmarkResult]) -> None:
    """Display list-relative indexes and clearly labeled search-only timings."""
    print(f"\nDataset size: {size:,}\nTarget value: {target}")
    print(f"Timing: median of {DEFAULT_REPEATS} batches of {DEFAULT_ITERATIONS} searches;")
    print("loading and sorting are excluded.")
    for result in results:
        order = "original-order data" if result.algorithm == "Linear" else "sorted data"
        print(f"\n{result.algorithm.upper()} SEARCH")
        print(f"Found: {'Yes' if result.found else 'No'}")
        if result.found:
            print(f"Index: {result.index} ({order}, zero-based)")
        else:
            print("Index: -1 (not found)")
        print(f"Execution time: {result.execution_time:.9g} seconds/search")


def run_interactive(data_dir: str | Path = DEFAULT_DATA_DIR) -> int:
    """Repeat menu-driven searches; recover from invalid input and data errors."""
    sizes = {str(number): size for number, size in enumerate(DATASET_SIZES, 1)}
    modes = {"1": "linear", "2": "binary", "3": "both"}
    print("\n========================================")
    print("        SEARCHFLOW ANALYTICS")
    print("========================================")
    print("Enter q at any prompt to quit.")
    try:
        while True:
            print("\nSelect Dataset Size")
            for option, size in sizes.items():
                print(f"{option}. {size:,}")
            choice = _read_choice("Enter option (q to quit): ", sizes)
            if choice is None:
                break
            target = _read_target()
            if target is None:
                break
            print("\nChoose Search Mode\n1. Linear Search\n2. Binary Search\n3. Compare Both")
            mode = _read_choice("Enter option (q to quit): ", modes)
            if mode is None:
                break
            try:
                results = search_dataset(sizes[choice], target, modes[mode], data_dir)
            except (OSError, ValueError) as exc:
                print(f"Unable to search this dataset: {exc}", file=sys.stderr)
                if isinstance(exc, FileNotFoundError):
                    print("Run main.py --generate to recreate the required datasets.", file=sys.stderr)
                continue
            _display_results(sizes[choice], target, results)
    except (EOFError, KeyboardInterrupt):
        print("\nSearch session ended.")
    print("Goodbye.")
    return 0
