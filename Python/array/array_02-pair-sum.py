from operator import le


def pair_sum(arr, k):
    
    # edgs case:
    if len(arr) < 2:
        return 0
    
    seen = set()
    pair = set()
    
    for num in arr:
        if k-num in seen:
            pair.add((max(num, k-num), min(num, k-num)))
        else:
            seen.add(num)
        
    return len(pair)
        
print(pair_sum([1,3,2,2],4))
print(pair_sum([1,9,2,8,3,7,4,6,5,5,13,14,11,13,-1],10))
print(pair_sum([1,2,3,1],3))