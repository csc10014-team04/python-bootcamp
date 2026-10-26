"""W1-4: Translation from C++ to Python."""

from typing import TypeVar

from .W1_4 import transpose_comprehension

T = TypeVar("T")


def binary_search(a: list[int], key: int) -> int:
    """Perform binary search on a sorted list of integers.

    Difference from C++:
        In C++, `lo + (hi - lo) / 2` is needed to prevent 32-bit integer overflow.
        In Python, integers have arbitrary precision and cannot overflow, so
        `(lo + hi) // 2` using floor division is completely safe. Furthermore,
        Python's `len(a)` returns an int without signed/unsigned conversion warnings,
        unlike C++ `static_cast<int>(a.size())`.

    Args:
        a: Sorted list of integers.
        key: Integer value to find.

    Returns:
        Index of the key if found, otherwise -1.
    """
    lo = 0
    hi = len(a) - 1

    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == key:
            return mid
        if a[mid] < key:
            lo = mid + 1
        else:
            hi = mid - 1

    return -1


__all__ = ["binary_search", "transpose_comprehension"]

