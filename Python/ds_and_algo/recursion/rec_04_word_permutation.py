def permute(s):

    # base case
    if len(s) == 0:
        return ['']

    first_char = s[0]
    rest_perm = permute(s[1:])

    result = []

    for perm in rest_perm:
        for i in range(len(perm) + 1):
            new_permute = perm[:i] + first_char + perm[i:]
            result.append(new_permute)

    return result


def perm2(s):

    result = ['']

    for char in s:

        new_permute = []

        for perm in result:
            for i in range(len(perm)+1):
                new = perm[i:] + char + perm[:i]
                new_permute.append(new)

        result = new_permute

    return result


print(perm2('abcd'))
