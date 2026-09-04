name = "aaaabbbc"
result = {}
for char in name:
    result[char] = result.get(char, 0) + 1

print(result)
max_o_char = ''
max_o = 0
for key in result:
    if result[key] > max_o:
        max_o = result[key]
        max_o_char = key
print(max_o_char)