"""Validate integer datasets and prepare independent search inputs."""

from collections.abc import Sequence


def validate_dataset(data: Sequence[int], expected_size: int | None = None) -> None:
    """Reject empty data, noninteger values, and an incorrect expected count.

    Booleans are rejected even though Python treats them as integer subclasses.
    Raise TypeError for a non-sequence input and ValueError for invalid contents
    or an invalid expected size. Negative integers and duplicates are allowed.
    """
    if isinstance(data, (str, bytes)) or not isinstance(data, Sequence):
        raise TypeError("Dataset must be a sequence of integers.")
    if expected_size is not None:
        if type(expected_size) is not int or expected_size <= 0:
            raise ValueError("Expected size must be a positive integer.")
    if not data:
        raise ValueError("Dataset must not be empty.")
    for index, value in enumerate(data):
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError(f"Dataset value at index {index} must be an integer.")
    if expected_size is not None and len(data) != expected_size:
        raise ValueError(f"Expected {expected_size} values, found {len(data)}.")


def prepare_search_data(
    data: Sequence[int], expected_size: int | None = None
) -> tuple[list[int], list[int]]:
    """Return (original-order copy, ascending sorted copy) without mutating data."""
    validate_dataset(data, expected_size)
    return list(data), sorted(data)
