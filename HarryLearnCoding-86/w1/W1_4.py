"""Week 1 Task 4: Matrix transpose using list comprehension."""

from typing import TypeVar

T = TypeVar("T")


def transpose_comprehension(matrix: list[list[T]]) -> list[list[T]]:
    """Transpose a 2D matrix using nested list comprehension.

    Args:
        matrix: 2D rectangular list of elements.

    Returns:
        Transposed 2D matrix where rows and columns are swapped.
    """
    if not matrix or not matrix[0]:
        return []

    rows = len(matrix)
    cols = len(matrix[0])

    return [[matrix[j][i] for j in range(rows)] for i in range(cols)]
