# ============================================================
# Problem 5: Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.
# Time: O(n) | Space: O(n)
# ============================================================


def valid_parentheses(s: str) -> bool:

    open_paren = {'(', '[', '{'}
    valid_paren = {('(', ')'), ('[', ']'), ('{', '}')}

    if len(s) % 2 == 1:
        return False

    stack = []

    for paren in s:

        if paren in open_paren:
            stack.append(paren)
        else:
            if len(stack) == 0:
                return False

            last_open = stack.pop()
            if (last_open, paren) not in valid_paren:
                return False


    return len(stack) == 0

# print(valid_parentheses("()"))
# print(valid_parentheses("()[]{}"))
# print(valid_parentheses("(]"))
# print(valid_parentheses("([)]"))
print(valid_parentheses("(()"))

if __name__ == "__main__":
    assert valid_parentheses("()") == True
    assert valid_parentheses("()[]{}") == True
    assert valid_parentheses("(]") == False
    assert valid_parentheses("([)]") == False
    assert valid_parentheses("{[]}") == True
    assert valid_parentheses("") == True  # NEW — empty string edge case
    assert valid_parentheses("(()") == False  # NEW — unclosed bracket, your bug
    assert valid_parentheses("())") == False  # NEW — extra closing bracket
    assert valid_parentheses("(((((((((())))))))))") == True  # NEW — deeply nested
    print("All test cases for stacks and linked list passed")