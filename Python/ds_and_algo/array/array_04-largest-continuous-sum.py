def largest_sum(arr):
    """_summary_

    Args:
        arr (_type_): array of negative and positive integers

    Returns:
        _type_: largest continuous sum of integers.
    """
    
    # edge case
    if len(arr) == 0:
        return 0
    
    current_sum = sum = arr[0]
    
    for num in arr[1:]:
        current_sum = max(current_sum+num, num)
        sum = max(sum, current_sum)
    
    return sum


print(largest_sum([1,2,-1,3,4,-1]))
print(largest_sum([1,2,-1,3,4,10,10,-10,-1]))
print(largest_sum([-1,1]))