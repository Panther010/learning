def unique_char(s):
    """
    check if all the character in the string are unique or not
    """
    seen = set()
    
    for char in s:
        if char in seen:
            return False
        else:
            seen.add(char)
            
    return True


def unique_char1(s):
    """
    check if all the character in the string are unique or not
    """
    if len(s) == len(set(s)):
        return True

    return False


print(unique_char1(''))
print(unique_char1('goo'))
print(unique_char1('abcdefg'))
