"""Iterative binary search of ascending integer data."""

from collections.abc import Sequence


def binary_search(data: Sequence[int], target: int) -> int:
    """Return a matching zero-based index, or -1 if target is absent.

    Precondition: data contains validated integers in ascending (nondecreasing)
    order, such as the sorted copy from prepare_search_data. The target is an
    integer. This function does not sort or check ordering: an O(n) validation
    pass would obscure the O(log n) search cost. Unsorted input is unsupported.

    Duplicates may return any matching index, not necessarily the first.
    An empty sequence returns -1. The input is never modified.

    For a list or tuple with O(1) indexing: time is O(1) best case and O(log n)
    average/worst case; auxiliary space is O(1).
    """
    low = 0
    high = len(data) - 1
    while low <= high:
        middle = (low + high) // 2
        value = data[middle]
        if value == target:
            return middle
        if value < target:
            low = middle + 1
        else:
            high = middle - 1
    return -1
