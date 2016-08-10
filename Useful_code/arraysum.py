def sum(alist):
    """
    Kadane's algorithm implementation, O(n) complexity. Scan through the array values and store current
    subarray sum in <current_maxsum> variable. Answer to this problem is the maximum of the
    <current_maxsum> values.
    :return: maximum sum of the provided subarray
    """
    best_maxsum = 0
    current_maxsum = 0
    for element in alist:
        # If <current_maxsum> lesser than zero, then assign a zero to <current_maxsum>
        current_maxsum = max(current_maxsum + element, 0)
        best_maxsum = max(best_maxsum, current_maxsum)
    return best_maxsum
