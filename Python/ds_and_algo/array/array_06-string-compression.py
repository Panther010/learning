def compress(s):
    compressed = ''
    length = len(s)

    # edge case
    if length == 0:
        return ''

    # edge case
    if length == 1:
        return s + '1'

    i = 1
    count = 1
    while i < length:
        if s[i - 1] == s[i]:
            count += 1
        else:
            compressed += s[i - 1] + str(count)
            count = 1
        i += 1
    compressed += s[i - 1] + str(count)

    return compressed


print(compress('AAAAABBBBCCCCCCCC'))


def compress2(s):
    count = 1
    result = ''

    for i in range(1, len(s)):
        if s[i - 1] == s[i]:
            count += 1
        else:
            result = result + s[i - 1] + str(count)
            count = 1

    result = result + s[i] + str(count)
    return result


print(compress2('AAAAABBBBCCCCCCCC'))
