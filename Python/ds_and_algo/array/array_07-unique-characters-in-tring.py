def unique_char(s):
    seen = set()
    
    for char in s:
        if char in seen:
            return False
        else:
            seen.add(char)
            
    return True


print(unique_char(''))
print(unique_char('goo'))
print(unique_char('abcdefg'))