def balance_check(s):

    opening = {'(', '{', '['}  # All the opening parentheses
    matches = {('(', ')'), ('{', '}'), ('[', ']')}  # Pair of match cases

    stack = []

    # edge case to check is string is odd length or initial character is not opening parentheses
    if len(s) % 2 == 1:
        return False

    for paren in s:

        # If element is first element add it to stack
        if paren in opening:
            stack.append(paren)
        else:
            # Check if stack has element
            if len(stack) == 0:
                return False

            last_open = stack.pop()

            # In case of closing element check if previous was matching open or not
            if (last_open, paren) not in matches:
                return False

    return len(stack) == 0


print(balance_check('[](){([[[]]])}'))
# Testing the function
print(balance_check('[](){([[[]]])}'))  # Should return True
print(balance_check('[(])'))            # Should return False
print(balance_check(''))                # Should return True (empty string is balanced)
print(balance_check('['))               # Should return False (unmatched opening bracket)