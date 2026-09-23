"""Sequential search of integer data in its existing order."""

from collections.abc import Sequence


def linear_search(data: Sequence[int], target: int) -> int:
    """Return the first matching zero-based index, or -1 if target is absent.

    Accept validated integer data in any order and an integer target. An empty
    sequence returns -1. Read the input without modifying it; validation and
    file operations belong to the surrounding pipeline, outside search timing.

    Time: O(1) best case, O(n) average/worst case. Auxiliary space: O(1).
    """
    for index, value in enumerate(data):
        if value == target:
            return index
    return -1
