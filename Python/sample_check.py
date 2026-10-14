a = {"apple": 2, "banana": 3}
b = {"apple": 4, "orange": 5}

def merge_count(a: dict, b: dict) -> dict:
    result = a
    for key, value in b.items():
        result[key] = result.get(key, 0) + value
    return result

print(merge_count(a, b))