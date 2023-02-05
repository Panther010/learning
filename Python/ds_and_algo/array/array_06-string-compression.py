def compress(s):
    compressed = ''
    length = len(s)
    
    # edge case
    if length == 0:
        return ''
    
    # edge case
    if length == 1:
        return s+'1'
    
    i =1
    count = 0
    while i < length:
        if s[i-1] == s[i]:
            count += 1
        else:
            compressed += s[i-1] + str(count)
            count =0
        i+=1
    compressed += s[i-1] + str(count)
    
    return compressed

print(compress('AAAAABBBBCCCCCCCC'))