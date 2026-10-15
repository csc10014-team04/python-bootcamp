def binary_search(a: list[int], key: int) -> int:
    """
    python does not require explicit integer casting for division since the // operator performs floor division directly.
    """
    lo, hi = 0, len(a) - 1 # initialize search boundaries
    while lo <= hi:
        mid = lo + (hi - lo) // 2 # calculate middle index
        if a[mid] == key:
            return mid
        if a[mid] < key:
            lo = mid + 1 # shift lower bound
        else:
            hi = mid - 1 # shift upper bound
    return -1 # return -1 if element is not found