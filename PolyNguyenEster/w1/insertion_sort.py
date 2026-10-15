def insertion_sort(arr: list[int]) -> list[int]:

    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = key

    return arr

numbers = [5, 2, 4, 1, 3]
result = insertion_sort(numbers)
