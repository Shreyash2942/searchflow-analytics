"""Measure repeated search calls with a high-resolution monotonic clock."""

from collections.abc import Callable, Sequence
from dataclasses import dataclass
from math import isfinite
from statistics import median
from time import perf_counter

DEFAULT_REPEATS = 7
DEFAULT_ITERATIONS = 100
DEFAULT_WARMUPS = 3


@dataclass(frozen=True)
class SearchTiming:
    """Search index, median seconds per call, and per-batch seconds per call."""

    index: int
    execution_time: float
    samples: tuple[float, ...]


def validate_timing_settings(repeats: int, iterations: int, warmups: int) -> None:
    """Reject invalid counts, including booleans, before performing any work."""
    for name, value, minimum in (("repeats", repeats, 1),
                                 ("iterations", iterations, 1), ("warmups", warmups, 0)):
        if type(value) is not int or value < minimum:
            raise ValueError(f"{name} must be an integer >= {minimum}.")


def time_search(
    search: Callable[[Sequence[int], int], int],
    data: Sequence[int],
    target: int,
    *,
    repeats: int = DEFAULT_REPEATS,
    iterations: int = DEFAULT_ITERATIONS,
    warmups: int = DEFAULT_WARMUPS,
) -> SearchTiming:
    """Time deterministic, nonmutating searches on already prepared input.

    Check correctness once and warm up before timing. Each sample times a batch
    of calls and divides elapsed seconds by iterations; return the median sample.
    Timed regions include Python loop/call overhead, but no validation, sorting,
    loading or output. Do not interpret these samples as end-to-end pipeline time.
    """
    validate_timing_settings(repeats, iterations, warmups)
    expected = search(data, target)
    if type(expected) is not int or not -1 <= expected < len(data):
        raise ValueError("Search returned an invalid index.")
    if (expected == -1 and target in data) or (expected != -1 and data[expected] != target):
        raise ValueError("Search returned an incorrect result.")
    for _ in range(warmups):
        if search(data, target) != expected:
            raise ValueError("Search returned inconsistent results during warm-up.")
    samples = []
    for _ in range(repeats):
        start = perf_counter()
        for _ in range(iterations):
            index = search(data, target)
        elapsed = perf_counter() - start
        if index != expected:
            raise ValueError("Search returned inconsistent results between batches.")
        if not isfinite(elapsed) or elapsed < 0:
            raise ValueError("Clock produced an invalid elapsed time.")
        samples.append(elapsed / iterations)
    return SearchTiming(expected, median(samples), tuple(samples))
