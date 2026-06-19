# ============================================================
# Problem 1: Two Sum (Easy)
# Time: O(n) | Space: O(n)
# ============================================================

def two_sum(nums: list, target:int) -> list:
    if len(nums) < 2:
        return []

    index_map = {}
    for i in range(len(nums)):
        if target - nums[i] in index_map:
            return [index_map[target - nums[i]], i]
        else:
            index_map[nums[i]] = i
    return []

# print(two_sum([2, 7, 11, 15], 9))
# print(two_sum([3, 2, 4], 6))
# print(two_sum([3, 3], 6))



# ============================================================
# Problem 2: Valid Anagram
# Time: O(n) | Space: O(n)
# ============================================================
def valid_anagram(s: str, t: str) -> bool:
    s = s.lower().strip()
    t = t.lower().strip()

    if len(s) != len(t):
        return False

    fre_counter = {}

    for char in s:
        fre_counter[char] = fre_counter.get(char, 0) + 1

    for char in t:
        fre_counter[char] = fre_counter.get(char, 0) - 1

    for k, v in fre_counter.items():
        if v != 0:
            return False

    return True

# print(valid_anagram("anagram", "nagaram")) # Output: True
# print(valid_anagram("rat", "car")) # Output: False
# print(valid_anagram("listen", "silent"))


# ============================================================
# Problem 3: Contains Duplicate
# Time: O(n) | Space: O(n)
# ============================================================

def duplicate_check1(nums: list) -> bool:
    if nums == list(set(nums)):
        return False
    return True

def duplicate_check2(nums: list) -> bool:
    seen = set()
    for num in nums:
        if num in seen:
            return True
        else:
            seen.add(num)

    return False

# print(duplicate_check2([1, 2, 3, 1]))
# print(duplicate_check2([1, 2, 3, 4]))
# print(duplicate_check2([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]))


# ============================================================
# Problem 4: Best time to buy sell stock
# Time: O(n) | Space: O(n)
# ============================================================

def buy_sell_analysis(prices: list[int]) -> int:
    min_price = float('inf')
    max_profit = 0

    for price in prices:
        if price < min_price:
            min_price = price

        profit = price - min_price
        max_profit = max(profit, max_profit)

    return max_profit

# print(buy_sell_analysis([7, 1, 5, 3, 6, 4]))
# print(buy_sell_analysis([7, 6, 4, 3, 1]))

if __name__ == "__main__":
      assert two_sum([2, 7, 11, 15], 9) == [0, 1]
      assert two_sum([3, 2, 4], 6) == [1, 2]
      assert two_sum([3, 3], 6) == [0, 1]
      assert two_sum([], 5) == []
      print("All two sum tests passed!")

      assert valid_anagram("anagram", "nagaram") == True
      assert valid_anagram("rat", "car") == False
      assert valid_anagram("listen", "silent") == True
      print("All anagram tests passed!")

      assert duplicate_check1([1, 2, 3, 1]) == True
      assert duplicate_check1([1, 2, 3, 4]) == False
      assert duplicate_check1([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]) == True
      print("All duplicate check 1 tests passed!")

      assert duplicate_check2([1, 2, 3, 1]) == True
      assert duplicate_check2([1, 2, 3, 4]) == False
      assert duplicate_check2([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]) == True
      print("All duplicate check 2 tests passed!")

      assert buy_sell_analysis([7, 1, 5, 3, 6, 4]) == 5
      assert buy_sell_analysis( [7, 6, 4, 3, 1]) == 0
      print("All Best Time to Buy and Sell Stock tests passed!")