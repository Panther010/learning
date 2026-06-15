  Python: fundamentals/python/prep/solutions/
 
  solutions/
  ├── arrays_and_hashing.py      # Problems 1-4, 8-10 (Two Sum, Anagram, Duplicates, etc.)
  ├── two_pointers.py            # Problems 7, 13, 16, 18 (3Sum, Container, Rotate, etc.)
  ├── sliding_window.py          # Problems 12, 25 (Longest Substring, Subarray Sum)
  ├── stacks_and_linked_lists.py # Problems 5, 6, 28 (Valid Parentheses, Merge Lists)
  ├── matrix.py                  # Problems 22-24 (Sudoku, Set Zeroes, Spiral)
  ├── binary_search.py           # Problems 19, 27 (Peak Element, Median of Two)
  ├── dynamic_programming.py     # Problems 4, 15, 26, 30 (Stock, Kadane, Trapping Rain)
  └── graphs_and_bfs.py          # Problem 29 (Word Ladder)
 
  PySpark: fundamentals/spark/prep/solutions/
 
  solutions/
  ├── basic_transformations.py   # Problems 1-4 (filter, withColumn, groupBy, dates)
  ├── joins_and_lookups.py       # Problems 5-8 (joins, broadcast, self-join)
  ├── window_functions.py        # Problems 9-14 (rank, lag, running totals)
  ├── aggregations_advanced.py   # Problems 15-20 (pivot, rollup, complex agg)
  ├── data_quality.py            # Problems 21-25 (nulls, dedup, schema validation)
  └── optimization.py            # Problems 26-30 (partitioning, caching, explain)

# Python Interview Problem Bank

**Total Problems:** 30 (10 Easy, 15 Medium, 5 Hard)
**Suggested pace:** 1-2 per day (complete in 3-4 weeks)

---

## How to Use This

1. Pick one problem per day (start with Easy, move to Medium by Week 2)
2. Create a file: `solutions/problem_XX_name.py`
3. Include: problem statement as docstring, solution with comments, test cases
4. Mark [x] when solved
5. Include time/space complexity analysis

---

## Week 1: Easy Problems (Arrays, Strings, Hash Tables)

### [ ] Problem 1: Two Sum
**Difficulty:** Easy
**Topics:** Arrays, Hash Table
**Time:** 15-20 min

Given an array of integers `nums` and an integer `target`, return indices of the two numbers that add up to `target`. Assume exactly one solution exists, and you cannot use the same element twice.

```python
# Example 1
nums = [2, 7, 11, 15]
target = 9
# Output: [0, 1]  (because nums[0] + nums[1] == 9)

# Example 2
nums = [3, 2, 4]
target = 6
# Output: [1, 2]

# Example 3
nums = [3, 3]
target = 6
# Output: [0, 1]
```

**Constraints:**
- 2 <= len(nums) <= 10^4
- -10^9 <= nums[i] <= 10^9
- Exactly one valid answer exists

**Hints:**
- Brute force is O(n²) with nested loops
- Can you do it in one pass with O(n) using a hash map?

---

### [ ] Problem 2: Valid Anagram
**Difficulty:** Easy
**Topics:** Strings, Hash Table, Sorting
**Time:** 10-15 min

Given two strings `s` and `t`, return `True` if `t` is an anagram of `s`, and `False` otherwise. An anagram is a word formed by rearranging the letters of another word, using all original letters exactly once.

```python
# Example 1
s = "anagram"
t = "nagaram"
# Output: True

# Example 2
s = "rat"
t = "car"
# Output: False

# Example 3
s = "listen"
t = "silent"
# Output: True
```

**Constraints:**
- 1 <= len(s), len(t) <= 50,000
- s and t consist of lowercase English letters

**Follow-up:** What if inputs contain Unicode characters? How would you adapt?

---

### [ ] Problem 3: Contains Duplicate
**Difficulty:** Easy
**Topics:** Arrays, Hash Table, Set
**Time:** 10 min

Given an integer array `nums`, return `True` if any value appears at least twice, and `False` if every element is distinct.

```python
# Example 1
nums = [1, 2, 3, 1]
# Output: True

# Example 2
nums = [1, 2, 3, 4]
# Output: False

# Example 3
nums = [1, 1, 1, 3, 3, 4, 3, 2, 4, 2]
# Output: True
```

---

### [ ] Problem 4: Best Time to Buy and Sell Stock
**Difficulty:** Easy
**Topics:** Arrays, Dynamic Programming
**Time:** 15 min

You are given an array `prices` where `prices[i]` is the price of a stock on the i-th day. You want to maximize profit by choosing a single day to buy and a different day in the future to sell. Return the maximum profit you can achieve. If you cannot achieve any profit, return 0.

```python
# Example 1
prices = [7, 1, 5, 3, 6, 4]
# Output: 5
# Explanation: Buy on day 2 (price=1), sell on day 5 (price=6), profit = 6-1 = 5

# Example 2
prices = [7, 6, 4, 3, 1]
# Output: 0
# Explanation: No profit possible (prices only decrease)
```

**Constraints:**
- Must buy before you sell (can't sell before buying)
- At most one transaction (one buy + one sell)

---

### [ ] Problem 5: Valid Parentheses
**Difficulty:** Easy
**Topics:** String, Stack
**Time:** 15-20 min

Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.

An input string is valid if:
1. Open brackets must be closed by the same type of brackets
2. Open brackets must be closed in the correct order
3. Every close bracket has a corresponding open bracket of the same type

```python
# Example 1
s = "()"
# Output: True

# Example 2
s = "()[]{}"
# Output: True

# Example 3
s = "(]"
# Output: False

# Example 4
s = "([)]"
# Output: False

# Example 5
s = "{[]}"
# Output: True
```

---

### [ ] Problem 6: Merge Two Sorted Lists
**Difficulty:** Easy
**Topics:** Linked List, Recursion
**Time:** 20 min

You are given the heads of two sorted linked lists `list1` and `list2`. Merge the two lists into one sorted list. Return the head of the merged linked list.

```python
# You need this ListNode class
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

# Example 1
list1 = [1, 2, 4]  # represented as: 1 -> 2 -> 4
list2 = [1, 3, 4]  # represented as: 1 -> 3 -> 4
# Output: [1, 1, 2, 3, 4, 4]

# Example 2
list1 = []
list2 = []
# Output: []

# Example 3
list1 = []
list2 = [0]
# Output: [0]
```

**Hint:** Can be solved iteratively or recursively

---

### [ ] Problem 7: Reverse a String
**Difficulty:** Easy
**Topics:** String, Two Pointers
**Time:** 10 min

Write a function that reverses a string. The input string is given as an array of characters. You must do this by modifying the input array in-place with O(1) extra memory.

```python
# Example 1
s = ["h", "e", "l", "l", "o"]
# After running your function, s should be: ["o", "l", "l", "e", "h"]

# Example 2
s = ["H", "a", "n", "n", "a", "h"]
# Output: ["h", "a", "n", "n", "a", "H"]
```

**Constraints:**
- Must be in-place (no creating a new list)
- O(1) extra space

---

### [ ] Problem 8: Find All Duplicates in an Array
**Difficulty:** Easy/Medium
**Topics:** Arrays, Hash Table
**Time:** 15 min

Given an integer array `nums` of length `n` where all integers are in the range `[1, n]` and each integer appears once or twice, return an array of all the integers that appear twice.

```python
# Example 1
nums = [4, 3, 2, 7, 8, 2, 3, 1]
# Output: [2, 3]

# Example 2
nums = [1, 1, 2]
# Output: [1]

# Example 3
nums = [1]
# Output: []
```

**Follow-up:** Can you do it without extra space (O(1)) and in O(n) time?

---

### [ ] Problem 9: Majority Element
**Difficulty:** Easy
**Topics:** Arrays, Hash Table, Divide and Conquer
**Time:** 15 min

Given an array `nums` of size `n`, return the majority element. The majority element is the element that appears more than `⌊n / 2⌋` times. You may assume the majority element always exists.

```python
# Example 1
nums = [3, 2, 3]
# Output: 3

# Example 2
nums = [2, 2, 1, 1, 1, 2, 2]
# Output: 2
```

**Follow-up:** Can you solve it in O(n) time and O(1) space? (Boyer-Moore Voting Algorithm)

---

### [ ] Problem 10: Missing Number
**Difficulty:** Easy
**Topics:** Arrays, Math, Bit Manipulation
**Time:** 10-15 min

Given an array `nums` containing `n` distinct numbers in the range `[0, n]`, return the only number in the range that is missing from the array.

```python
# Example 1
nums = [3, 0, 1]
# Output: 2
# Explanation: n = 3 since there are 3 numbers, so all numbers are in range [0, 3].
# 2 is missing.

# Example 2
nums = [0, 1]
# Output: 2

# Example 3
nums = [9, 6, 4, 2, 3, 5, 7, 0, 1]
# Output: 8
```

**Follow-up:** Can you solve it using only O(1) extra space and O(n) runtime?

---

## Week 2: Medium Problems (Hash Tables, Two Pointers, Sliding Window)

### [ ] Problem 11: Group Anagrams
**Difficulty:** Medium
**Topics:** Hash Table, String, Sorting
**Time:** 20-25 min

Given an array of strings `strs`, group the anagrams together. You can return the answer in any order.

```python
# Example 1
strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
# Output: [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]

# Example 2
strs = [""]
# Output: [[""]]

# Example 3
strs = ["a"]
# Output: [["a"]]
```

**Constraints:**
- 1 <= len(strs) <= 10,000
- 0 <= len(strs[i]) <= 100
- strs[i] consists of lowercase English letters

**Hint:** What's a good key to use for grouping? (Think: sorted letters or character frequency)

---

### [ ] Problem 12: Longest Substring Without Repeating Characters
**Difficulty:** Medium
**Topics:** String, Sliding Window, Hash Table
**Time:** 25-30 min

Given a string `s`, find the length of the longest substring without repeating characters.

```python
# Example 1
s = "abcabcbb"
# Output: 3
# Explanation: The answer is "abc", with length 3

# Example 2
s = "bbbbb"
# Output: 1
# Explanation: The answer is "b", with length 1

# Example 3
s = "pwwkew"
# Output: 3
# Explanation: The answer is "wke", with length 3
# Note that "pwke" is a subsequence, not a substring
```

**Hint:** Use sliding window with two pointers + hash set to track seen characters

---

### [ ] Problem 13: 3Sum
**Difficulty:** Medium
**Topics:** Arrays, Two Pointers, Sorting
**Time:** 30-35 min

Given an integer array `nums`, return all unique triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.

Notice that the solution set must not contain duplicate triplets.

```python
# Example 1
nums = [-1, 0, 1, 2, -1, -4]
# Output: [[-1, -1, 2], [-1, 0, 1]]

# Example 2
nums = [0, 1, 1]
# Output: []

# Example 3
nums = [0, 0, 0]
# Output: [[0, 0, 0]]
```

**Hint:** 
- Sort the array first
- Fix one element, then use two pointers on the rest
- Skip duplicates to avoid duplicate triplets

---

### [ ] Problem 14: Product of Array Except Self
**Difficulty:** Medium
**Topics:** Arrays, Prefix Sum
**Time:** 20-25 min

Given an integer array `nums`, return an array `answer` such that `answer[i]` is equal to the product of all elements of `nums` except `nums[i]`.

```python
# Example 1
nums = [1, 2, 3, 4]
# Output: [24, 12, 8, 6]
# Explanation:
# answer[0] = 2 * 3 * 4 = 24
# answer[1] = 1 * 3 * 4 = 12
# answer[2] = 1 * 2 * 4 = 8
# answer[3] = 1 * 2 * 3 = 6

# Example 2
nums = [-1, 1, 0, -3, 3]
# Output: [0, 0, 9, 0, 0]
```

**Constraints:**
- Must run in O(n) time
- Do NOT use division operator
- Can you do it with O(1) extra space? (output array doesn't count)

**Hint:** Think about left products and right products

---

### [ ] Problem 15: Maximum Subarray (Kadane's Algorithm)
**Difficulty:** Medium
**Topics:** Arrays, Dynamic Programming, Divide and Conquer
**Time:** 20 min

Given an integer array `nums`, find the contiguous subarray (containing at least one number) which has the largest sum and return its sum.

```python
# Example 1
nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
# Output: 6
# Explanation: [4, -1, 2, 1] has the largest sum = 6

# Example 2
nums = [1]
# Output: 1

# Example 3
nums = [5, 4, -1, 7, 8]
# Output: 23
```

**Follow-up:** If you've figured out the O(n) solution (Kadane's Algorithm), try the divide and conquer approach.

---

### [ ] Problem 16: Container With Most Water
**Difficulty:** Medium
**Topics:** Arrays, Two Pointers, Greedy
**Time:** 20-25 min

You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the two endpoints of the i-th line are `(i, 0)` and `(i, height[i])`. Find two lines that together with the x-axis form a container that holds the most water. Return the maximum amount of water a container can store.

```python
# Example 1
height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
# Output: 49
# Explanation: Max area is between index 1 (height=8) and index 8 (height=7)
# Area = min(8, 7) * (8 - 1) = 7 * 7 = 49

# Example 2
height = [1, 1]
# Output: 1
```

**Hint:** Two pointers from both ends. Move the pointer with smaller height inward.

---

### [ ] Problem 17: Merge Intervals
**Difficulty:** Medium
**Topics:** Arrays, Sorting
**Time:** 25 min

Given an array of `intervals` where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals and return an array of the non-overlapping intervals.

```python
# Example 1
intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
# Output: [[1, 6], [8, 10], [15, 18]]
# Explanation: [1,3] and [2,6] overlap, so merge to [1,6]

# Example 2
intervals = [[1, 4], [4, 5]]
# Output: [[1, 5]]
```

**Hint:** Sort intervals by start time first

---

### [ ] Problem 18: Rotate Array
**Difficulty:** Medium
**Topics:** Arrays, Math, Two Pointers
**Time:** 20 min

Given an array, rotate the array to the right by `k` steps, where `k` is non-negative.

```python
# Example 1
nums = [1, 2, 3, 4, 5, 6, 7]
k = 3
# Output: [5, 6, 7, 1, 2, 3, 4]
# Explanation:
# rotate 1 step to the right: [7, 1, 2, 3, 4, 5, 6]
# rotate 2 steps: [6, 7, 1, 2, 3, 4, 5]
# rotate 3 steps: [5, 6, 7, 1, 2, 3, 4]

# Example 2
nums = [-1, -100, 3, 99]
k = 2
# Output: [3, 99, -1, -100]
```

**Constraints:**
- Try to solve it in-place with O(1) extra space
- Think about edge case: what if k > len(nums)?

**Hint:** Reverse the whole array, then reverse first k elements, then reverse rest

---

### [ ] Problem 19: Find Peak Element
**Difficulty:** Medium
**Topics:** Arrays, Binary Search
**Time:** 20 min

A peak element is an element that is strictly greater than its neighbors. Given an integer array `nums`, find a peak element and return its index. If the array contains multiple peaks, return the index to any of the peaks.

```python
# Example 1
nums = [1, 2, 3, 1]
# Output: 2
# Explanation: 3 is a peak element (3 > 2 and 3 > 1)

# Example 2
nums = [1, 2, 1, 3, 5, 6, 4]
# Output: 5
# Explanation: 6 is a peak element (or you could return 1 where 2 is peak)
```

**Constraints:**
- You may assume nums[-1] = nums[n] = -∞
- Must run in O(log n) time (use binary search!)

---

### [ ] Problem 20: Top K Frequent Elements
**Difficulty:** Medium
**Topics:** Arrays, Hash Table, Heap, Bucket Sort
**Time:** 25 min

Given an integer array `nums` and an integer `k`, return the `k` most frequent elements. You may return the answer in any order.

```python
# Example 1
nums = [1, 1, 1, 2, 2, 3]
k = 2
# Output: [1, 2]

# Example 2
nums = [1]
k = 1
# Output: [1]
```

**Follow-up:** Your algorithm's time complexity must be better than O(n log n), where n is array size.

**Hint:** Use bucket sort or heap. Bucket sort achieves O(n) time.

---

### [ ] Problem 21: Longest Consecutive Sequence
**Difficulty:** Medium
**Topics:** Arrays, Hash Table, Union Find
**Time:** 25-30 min

Given an unsorted array of integers `nums`, return the length of the longest consecutive elements sequence. You must write an algorithm that runs in O(n) time.

```python
# Example 1
nums = [100, 4, 200, 1, 3, 2]
# Output: 4
# Explanation: The longest consecutive sequence is [1, 2, 3, 4]. Therefore its length is 4.

# Example 2
nums = [0, 3, 7, 2, 5, 8, 4, 6, 0, 1]
# Output: 9
# Explanation: [0,1,2,3,4,5,6,7,8]
```

**Constraint:** O(n) time complexity required

**Hint:** Use a set. For each number, check if it's the start of a sequence (num-1 not in set)

---

### [ ] Problem 22: Valid Sudoku
**Difficulty:** Medium
**Topics:** Arrays, Hash Table, Matrix
**Time:** 25 min

Determine if a 9x9 Sudoku board is valid. Only the filled cells need to be validated according to:
1. Each row must contain digits 1-9 without repetition
2. Each column must contain digits 1-9 without repetition
3. Each of the nine 3x3 sub-boxes must contain digits 1-9 without repetition

```python
# Example 1
board = [
  ["5","3",".",".","7",".",".",".","."],
  ["6",".",".","1","9","5",".",".","."],
  [".","9","8",".",".",".",".","6","."],
  ["8",".",".",".","6",".",".",".","3"],
  ["4",".",".","8",".","3",".",".","1"],
  ["7",".",".",".","2",".",".",".","6"],
  [".","6",".",".",".",".","2","8","."],
  [".",".",".","4","1","9",".",".","5"],
  [".",".",".",".","8",".",".","7","9"]
]
# Output: True

# Note: A Sudoku board (partially filled) could be valid but not necessarily solvable.
# Only filled cells need to be validated.
```

**Hint:** Use 3 hash sets: rows, columns, boxes. Box index = (row // 3) * 3 + (col // 3)

---

### [ ] Problem 23: Set Matrix Zeroes
**Difficulty:** Medium
**Topics:** Arrays, Matrix
**Time:** 25 min

Given an m x n matrix, if an element is 0, set its entire row and column to 0. Do it in-place.

```python
# Example 1
matrix = [
  [1, 1, 1],
  [1, 0, 1],
  [1, 1, 1]
]
# Output: [
#   [1, 0, 1],
#   [0, 0, 0],
#   [1, 0, 1]
# ]

# Example 2
matrix = [
  [0, 1, 2, 0],
  [3, 4, 5, 2],
  [1, 3, 1, 5]
]
# Output: [
#   [0, 0, 0, 0],
#   [0, 4, 5, 0],
#   [0, 3, 1, 0]
# ]
```

**Follow-up:**
- O(m*n) space is straightforward. Can you do it in O(m + n)?
- Can you do it in O(1) space? (constant space, using matrix itself to store state)

---

### [ ] Problem 24: Spiral Matrix
**Difficulty:** Medium
**Topics:** Arrays, Matrix, Simulation
**Time:** 30 min

Given an m x n matrix, return all elements of the matrix in spiral order (clockwise from top-left).

```python
# Example 1
matrix = [
  [1, 2, 3],
  [4, 5, 6],
  [7, 8, 9]
]
# Output: [1, 2, 3, 6, 9, 8, 7, 4, 5]

# Example 2
matrix = [
  [1,  2,  3,  4],
  [5,  6,  7,  8],
  [9, 10, 11, 12]
]
# Output: [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]
```

**Hint:** Use 4 boundaries: top, bottom, left, right. Shrink them as you traverse each layer.

---

### [ ] Problem 25: Subarray Sum Equals K
**Difficulty:** Medium
**Topics:** Arrays, Hash Table, Prefix Sum
**Time:** 25-30 min

Given an array of integers `nums` and an integer `k`, return the total number of continuous subarrays whose sum equals `k`.

```python
# Example 1
nums = [1, 1, 1]
k = 2
# Output: 2
# Explanation: Subarrays: [1, 1] appears twice

# Example 2
nums = [1, 2, 3]
k = 3
# Output: 2
# Explanation: [1, 2] and [3]
```

**Constraint:** O(n) time required

**Hint:** Use prefix sum + hash map. If prefix_sum - k exists in map, we found a subarray.

---

## Week 3-4: Hard Problems (Advanced DP, Graphs, Trees)

### [ ] Problem 26: Trapping Rain Water
**Difficulty:** Hard
**Topics:** Arrays, Two Pointers, Dynamic Programming, Stack
**Time:** 35-40 min

Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.

```python
# Example 1
height = [0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]
# Output: 6
# Explanation: Water trapped above elevation bars

# Example 2
height = [4, 2, 0, 3, 2, 5]
# Output: 9
```

**Hint:** For each position, water level = min(max_left, max_right) - height[i]
Can be solved with two pointers in O(n) time and O(1) space.

---

### [ ] Problem 27: Median of Two Sorted Arrays
**Difficulty:** Hard
**Topics:** Arrays, Binary Search, Divide and Conquer
**Time:** 40-45 min

Given two sorted arrays `nums1` and `nums2` of size m and n respectively, return the median of the two sorted arrays. The overall run time complexity should be O(log (m+n)).

```python
# Example 1
nums1 = [1, 3]
nums2 = [2]
# Output: 2.0
# Explanation: merged = [1, 2, 3], median = 2

# Example 2
nums1 = [1, 2]
nums2 = [3, 4]
# Output: 2.5
# Explanation: merged = [1, 2, 3, 4], median = (2 + 3) / 2 = 2.5
```

**Constraint:** Must be O(log(m+n)) time

**Hint:** Binary search on the smaller array. Find the correct partition.

---

### [ ] Problem 28: Longest Valid Parentheses
**Difficulty:** Hard
**Topics:** String, Dynamic Programming, Stack
**Time:** 40 min

Given a string containing just `'('` and `')'`, find the length of the longest valid (well-formed) parentheses substring.

```python
# Example 1
s = "(()"
# Output: 2
# Explanation: Longest valid substring is "()"

# Example 2
s = ")()())"
# Output: 4
# Explanation: Longest valid substring is "()()"

# Example 3
s = ""
# Output: 0
```

**Hint:** Can use DP or stack. DP: dp[i] = length of longest valid ending at i

---

### [ ] Problem 29: Word Ladder
**Difficulty:** Hard
**Topics:** Hash Table, String, BFS
**Time:** 40-45 min

Given two words `beginWord` and `endWord`, and a dictionary `wordList`, find the length of shortest transformation sequence from `beginWord` to `endWord`, such that:
1. Only one letter can be changed at a time
2. Each transformed word must exist in the word list

Return 0 if there is no such transformation sequence.

```python
# Example 1
beginWord = "hit"
endWord = "cog"
wordList = ["hot", "dot", "dog", "lot", "log", "cog"]
# Output: 5
# Explanation: One shortest transformation is "hit" -> "hot" -> "dot" -> "dog" -> "cog"

# Example 2
beginWord = "hit"
endWord = "cog"
wordList = ["hot", "dot", "dog", "lot", "log"]
# Output: 0
# Explanation: endWord "cog" is not in wordList, so no transformation

# Example 3
beginWord = "game"
endWord = "thee"
wordList = ["frye", "heat", "tree", "thee", "game", "free", "hell", "fame", "faye"]
# Output: 7
# Explanation: "game" -> "fame" -> "faye" -> "frye" -> "free" -> "tree" -> "thee"
```

**Hint:** Use BFS from beginWord. For each word, try changing each letter to a-z and check if result is in wordList.

---

### [ ] Problem 30: Regular Expression Matching
**Difficulty:** Hard
**Topics:** String, Dynamic Programming, Recursion
**Time:** 45-50 min

Given an input string `s` and a pattern `p`, implement regular expression matching with support for `.` and `*` where:
- `.` Matches any single character
- `*` Matches zero or more of the preceding element

The matching should cover the entire input string (not partial).

```python
# Example 1
s = "aa"
p = "a"
# Output: False
# Explanation: "a" does not match the entire string "aa"

# Example 2
s = "aa"
p = "a*"
# Output: True
# Explanation: '*' means zero or more of preceding element 'a'
# Therefore it can match "aa"

# Example 3
s = "ab"
p = ".*"
# Output: True
# Explanation: ".*" means "zero or more (*) of any character (.)"

# Example 4
s = "mississippi"
p = "mis*is*p*."
# Output: False
```

**Constraint:** This requires advanced DP or recursion with memoization

**Hint:** Use 2D DP where dp[i][j] = whether s[0:i] matches p[0:j]

---

## Solution Template

When solving a problem, use this template:

```python
"""
Problem XX: <Problem Name>
Difficulty: <Easy/Medium/Hard>
Topics: <list topics>
Time Complexity: O(?)
Space Complexity: O(?)

Problem Statement:
<Copy problem statement here>

Examples:
<Copy examples here>

Approach:
1. <Step 1>
2. <Step 2>
...

Edge cases to consider:
- <Edge case 1>
- <Edge case 2>
"""

def solution_name(input_params):
    """
    Args:
        param1: description
        param2: description
    
    Returns:
        description of return value
    """
    # Your solution here
    pass


# Test cases
if __name__ == "__main__":
    # Example 1
    assert solution_name(test_input) == expected_output
    
    # Example 2
    assert solution_name(test_input) == expected_output
    
    # Edge case
    assert solution_name(edge_input) == edge_output
    
    print("All tests passed!")
```

---

## Daily Practice Routine

**Week 1 (Easy Problems):**
- Days 1-2: Problems 1-3 (Arrays, Hash Tables basics)
- Days 3-4: Problems 4-6 (DP intro, Stack, Linked List)
- Days 5-7: Problems 7-10 (Two Pointers, review)

**Week 2 (Medium Problems - Part 1):**
- Days 8-9: Problems 11-13 (Hash Tables, Sliding Window, Two Pointers)
- Days 10-11: Problems 14-16 (Prefix Sum, Kadane, Two Pointers)
- Days 12-14: Problems 17-20 (Sorting, Binary Search, Heap)

**Week 3 (Medium Problems - Part 2):**
- Days 15-16: Problems 21-23 (Hash Set, Matrix)
- Days 17-18: Problems 24-25 (Matrix, Prefix Sum)
- Days 19-21: Review all Medium, redo tough ones

**Week 4 (Hard Problems + Review):**
- Days 22-23: Problems 26-27 (Two Pointers, Binary Search)
- Days 24-25: Problems 28-29 (DP, BFS)
- Day 26: Problem 30 (Advanced DP)
- Days 27-28: Review all Hard, redo from scratch

---

## Tracking Your Progress

Mark problems as you complete them:
- [ ] Problem not attempted
- [x] Problem solved
- [~] Problem attempted but need to revisit

**Difficulty breakdown:**
- Easy (1-10): Build confidence, master fundamentals
- Medium (11-25): Core interview patterns, most important
- Hard (26-30): Stretch problems, impress in final rounds

**Time per problem:**
- Easy: 10-20 min
- Medium: 20-35 min  
- Hard: 35-50 min

If you exceed time, look at hint and try again. If still stuck after 2x time, look at solution but rewrite it yourself without copying.

---

## Notes

- All problems are self-contained (no LeetCode account needed)
- Focus on Medium problems (11-25) for interviews
- Hard problems (26-30) are for senior/staff level depth
- Easy problems (1-10) build foundation fast
- Review SQL problem format in `SQL/questions_and_solution_3/53_Paypal_hard_que.sql` for inspiration on how to document your solutions

Good luck!
