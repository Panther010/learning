def reverse_arr(arr):
    rev_arr = []
    length = len(arr)
    for i in range(length, 0, -1):
        rev_arr.append(arr[i - 1])

    return rev_arr


def rev_sen(s):
    spaces = [' ']
    rev = []
    length = len(s)

    i = 0

    while i < length:
        if s[i] not in spaces:
            start = i

            while i < length and s[i] not in spaces:
                i += 1

        rev.append(s[start:i])
        i += 1
    return " ".join(reverse_arr(rev))


print(rev_sen('Bakul Seth is the best'))


def rev_sen1(s):
    return " ".join(reversed(s.split()))


print(rev_sen1('Bakul Seth is the best'))


def rev_sen2(s):
    return " ".join(s.split()[::-1])


print(rev_sen2('Bakul Seth is the best'))


def rev_sen3(s1):
    result = []
    word = ''
    for i in s1:
        if i.isspace():
            result.insert(0, word)
            word = ''
        else:
            word += i
    result.insert(0, word)
    return " ".join(result)


print(rev_sen3('Bakul Seth is the best'))


def rev_sen4(s1):  # this method do not help with leading or trailing or more than one spaces
    result = ''
    word = ''
    for i in s1:
        if i.isspace():
            result = word + ' ' + result
            word = ''
        else:
            word += i
    result = word + ' ' + result
    return result


print(rev_sen4('  Bakul Seth is the best  '))