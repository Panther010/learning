def anagram1(str1, str2):
    """
    This function take 2 string and check if these are anagram pair or not.
    The check is being done by sort and compare method
    """
    str1 = str1.replace(' ', '').lower()
    str2 = str2.replace(' ', '').lower()

    if sorted(str1) == sorted(str2):
        return True
    else:
        return False

def anagram2(str1, str2):
    """_summary_ : This function checks if 2 string are anagram, or not using disct method 

    Args:
        str1 (String): _description_
        str2 (String): _description_
    """
    str1 = str1.replace(' ', '').lower()
    str2 = str2.replace(' ', '').lower()
    # edge case 
    if len(str1) != len(str2):
        return False
    
    check = {}
    
    for char in str1:
        if char in check:
            check[char] += 1
        else:
            check[char] = 1
           
    for char2 in str2:
        if char2 in check:
            check[char2] -= 1
        else:
            check[char2] = 1
            
    for c in check:
        if check[c] != 0:
            return False
    
    return True

import collections
            
def anagram3(str1, str2):
    """_summary_

    Args:
        str1 (_type_): _description_
        str2 (_type_): _description_

    Returns:
        _type_: _description_
    """
    str1 = str1.replace(' ', '').lower()
    str2 = str2.replace(' ', '').lower()
    
    count = collections.defaultdict(int)
    
    # edge case
    if len(str1) != len(str2):
        return False
    
    for chr in str1:
        count[chr] += 1
        
    for chr in str2:
        count[chr] -= 1
    
    for chr in count:
        if count[chr] != 0:
            return False
        
    return True

def anagram4(str1, str2):
    
    str1 = str1.replace(' ', '').lower()
    str2 = str2.replace(' ', '').lower()
    
    # edge case:
    if len(str1) != len(str2):
        return False
    
    count = collections.defaultdict(int)
    
    for c1, c2 in zip(str1, str2):
        count[c1] += 1
        count[c2] -= 1
        print(count)
        
    for char in count:
        if count[char] != 0:
            return False
        
    return True
        
def anagram5(str1, str2):
    str1 = str1.replace(' ', '').lower()
    str2 = str2.replace(' ', '').lower()
    
    if collections.Counter(str1) == collections.Counter(str2):
        return True
    else:
        return False

print(anagram4('go go go','gggooo'))
print(anagram5('abc','cba'))
print(anagram5('hi man','hi     man'))
print(anagram5('aabbcc','aabbc'))
print(anagram5('123','1 2'))
