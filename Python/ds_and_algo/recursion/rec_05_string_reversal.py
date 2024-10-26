def rev(s):

    if len(s) == 1:
        return s

    return rev(s[1:]) + s[0]


print(rev('Bakul Seth'))
