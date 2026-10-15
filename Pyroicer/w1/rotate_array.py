def reverse(arr, start, end):
    while start < end:
        arr[start], arr[end] = arr[end], arr[start]
        start += 1
        end -= 1
def left_rotate_reversal(vector, k):
    """
    Main difference is in the helper function (called reverse) instead of having to write (in C++):

    int temp=arr[start]
    arr[start]=arr[end]
    arr[end]=temp

    To swap the value of the variables in Python I can just write:
    arr[start], arr[end] = arr[end], arr[start]
    
    """
    n = len(vector)
    if n == 0:
        return vector
        
    k = k % n

    # reverse first k elements
    reverse(vector, 0, k - 1)
    
    # reverse last n-k elements
    reverse(vector, k, n - 1)
    
    # reverse the entire array
    reverse(vector, 0, n - 1)
    
    return vector