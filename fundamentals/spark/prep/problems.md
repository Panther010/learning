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


# PySpark Interview Problem Bank

**Total Problems:** 30 (10 Easy, 15 Medium, 5 Hard)
**Suggested pace:** 1-2 per day (complete in 3-4 weeks)

---

## How to Use This

1. Each problem includes complete sample data (copy-paste ready)
2. Create solution files: `solutions/problem_XX_name.py`
3. Include problem statement, solution, and test with sample data
4. Mark [x] when solved
5. Document approach and optimization notes

---

## Week 1: Easy Problems (Basic Transformations, Filters, GroupBy)

### [ ] Problem 1: Filter and Count
**Difficulty:** Easy
**Topics:** DataFrame, filter, count
**Time:** 10-15 min

You have a dataset of customer orders. Filter to show only orders above $100 and count them.

```python
from pyspark.sql import SparkSession
from pyspark.sql.types import *

spark = SparkSession.builder.appName("problem1").master("local[*]").getOrCreate()

data = [
    (1, "Alice",   85.50),
    (2, "Bob",    120.00),
    (3, "Charlie", 95.00),
    (4, "Diana",  210.00),
    (5, "Eve",     45.00),
    (6, "Frank",  150.00),
]

schema = StructType([
    StructField("order_id", IntegerType()),
    StructField("customer", StringType()),
    StructField("amount", DoubleType()),
])

df = spark.createDataFrame(data, schema)
df.show()

# Task: Filter orders where amount > 100, then count
# Expected: 3 orders (Bob, Diana, Frank)
```

---

### [ ] Problem 2: Add Calculated Column
**Difficulty:** Easy
**Topics:** withColumn, expr
**Time:** 10-15 min

Add a new column showing order amount with 8% sales tax applied, rounded to 2 decimals.

```python
data = [
    (1, "Laptop",  1200.00),
    (2, "Mouse",     25.00),
    (3, "Keyboard",  85.00),
    (4, "Monitor",  350.00),
]

schema = StructType([
    StructField("product_id", IntegerType()),
    StructField("product", StringType()),
    StructField("price", DoubleType()),
])

df = spark.createDataFrame(data, schema)

# Task: Add column "price_with_tax" = price * 1.08, rounded to 2 decimals
# Expected output includes:
# Laptop:  1296.00
# Mouse:     27.00
# Keyboard:  91.80
# Monitor:  378.00
```

**Hint:** Use `round()` function or `format_number()`

---

### [ ] Problem 3: GroupBy and Aggregate
**Difficulty:** Easy
**Topics:** groupBy, agg, sum, count
**Time:** 15 min

Group sales by salesperson and calculate total sales and order count for each.

```python
data = [
    (1, "Alice",  500.00),
    (2, "Bob",    300.00),
    (3, "Alice",  700.00),
    (4, "Charlie",450.00),
    (5, "Bob",    250.00),
    (6, "Alice",  600.00),
    (7, "Charlie",800.00),
]

schema = StructType([
    StructField("sale_id", IntegerType()),
    StructField("salesperson", StringType()),
    StructField("amount", DoubleType()),
])

df = spark.createDataFrame(data, schema)

# Task: Group by salesperson, show total_sales and order_count
# Order by total_sales descending
# Expected:
# Alice    1800.00  3
# Charlie  1250.00  2
# Bob       550.00  2
```

---

### [ ] Problem 4: String to Date Conversion
**Difficulty:** Easy
**Topics:** to_date, date functions
**Time:** 15 min

Convert a string date column to proper DateType and extract year, month, day.

```python
data = [
    (1, "2026-01-15", 100.00),
    (2, "2026-02-20", 150.00),
    (3, "2026-03-10", 200.00),
    (4, "2026-01-25", 120.00),
]

schema = StructType([
    StructField("txn_id", IntegerType()),
    StructField("txn_date_str", StringType()),
    StructField("amount", DoubleType()),
])

df = spark.createDataFrame(data, schema)

# Task:
# 1. Convert txn_date_str to DateType (call it txn_date)
# 2. Add columns: year, month, day
# 3. Show txn_id, txn_date, year, month, day, amount
```

**Hint:** Use `to_date()`, `year()`, `month()`, `dayofmonth()`

---

### [ ] Problem 5: Conditional Column (when/otherwise)
**Difficulty:** Easy
**Topics:** when, otherwise
**Time:** 15 min

Categorize products by price range: Budget, Mid-Range, Premium.

```python
data = [
    (1, "Widget A",  15.00),
    (2, "Widget B",  45.00),
    (3, "Widget C", 120.00),
    (4, "Widget D",  30.00),
    (5, "Widget E", 200.00),
    (6, "Widget F",   8.00),
]

schema = StructType([
    StructField("id", IntegerType()),
    StructField("product", StringType()),
    StructField("price", DoubleType()),
])

df = spark.createDataFrame(data, schema)

# Task: Add column "category":
# price < 20    → "Budget"
# price < 100   → "Mid-Range"
# price >= 100  → "Premium"
```

**Hint:** Use `when().when().otherwise()` chaining

---

### [ ] Problem 6: Sort and Limit
**Difficulty:** Easy
**Topics:** orderBy, limit
**Time:** 10 min

Find the top 3 highest-paid employees.

```python
data = [
    (1, "Alice",   75000),
    (2, "Bob",     82000),
    (3, "Charlie", 68000),
    (4, "Diana",   95000),
    (5, "Eve",     71000),
    (6, "Frank",   88000),
]

schema = StructType([
    StructField("emp_id", IntegerType()),
    StructField("name", StringType()),
    StructField("salary", IntegerType()),
])

df = spark.createDataFrame(data, schema)

# Task: Show top 3 employees by salary (highest first)
# Expected:
# Diana   95000
# Frank   88000
# Bob     82000
```

---

### [ ] Problem 7: Remove Duplicates
**Difficulty:** Easy
**Topics:** dropDuplicates, distinct
**Time:** 10-15 min

Remove duplicate customer records based on email address.

```python
data = [
    (1, "Alice", "alice@example.com"),
    (2, "Bob",   "bob@example.com"),
    (3, "Alice", "alice@example.com"),  # duplicate
    (4, "Charlie", "charlie@example.com"),
    (5, "Bob",   "bob@example.com"),    # duplicate
]

schema = StructType([
    StructField("id", IntegerType()),
    StructField("name", StringType()),
    StructField("email", StringType()),
])

df = spark.createDataFrame(data, schema)

# Task: Remove duplicates based on email (keep first occurrence)
# Expected: 3 unique records (Alice, Bob, Charlie)
```

**Hint:** Use `dropDuplicates(["email"])`

---

### [ ] Problem 8: Join Two DataFrames
**Difficulty:** Easy
**Topics:** join, inner join
**Time:** 15-20 min

Join employee data with department data to show employee names with department names.

```python
employees = [
    (1, "Alice",   101),
    (2, "Bob",     102),
    (3, "Charlie", 101),
    (4, "Diana",   103),
]

departments = [
    (101, "Engineering"),
    (102, "Sales"),
    (103, "Marketing"),
]

emp_schema = StructType([
    StructField("emp_id", IntegerType()),
    StructField("name", StringType()),
    StructField("dept_id", IntegerType()),
])

dept_schema = StructType([
    StructField("dept_id", IntegerType()),
    StructField("dept_name", StringType()),
])

emp_df = spark.createDataFrame(employees, emp_schema)
dept_df = spark.createDataFrame(departments, dept_schema)

# Task: Join to show emp_id, name, dept_name
# Expected:
# 1  Alice    Engineering
# 2  Bob      Sales
# 3  Charlie  Engineering
# 4  Diana    Marketing
```

---

### [ ] Problem 9: Null Handling
**Difficulty:** Easy
**Topics:** fillna, na.fill, isNull
**Time:** 15 min

Replace null values in the salary column with the average salary, and filter out rows where department is null.

```python
data = [
    (1, "Alice",   75000, "Engineering"),
    (2, "Bob",     None,  "Sales"),
    (3, "Charlie", 68000, None),
    (4, "Diana",   95000, "Engineering"),
    (5, "Eve",     None,  "Marketing"),
]

schema = StructType([
    StructField("emp_id", IntegerType()),
    StructField("name", StringType()),
    StructField("salary", IntegerType()),
    StructField("department", StringType()),
])

df = spark.createDataFrame(data, schema)

# Task:
# 1. Calculate average salary (from non-null values)
# 2. Fill null salaries with this average
# 3. Remove rows where department is null
# Expected: 4 rows (Charlie removed), Bob and Eve have avg salary
```

---

### [ ] Problem 10: Column Rename and Select
**Difficulty:** Easy
**Topics:** withColumnRenamed, select, alias
**Time:** 10 min

Rename columns to follow snake_case convention and select only relevant columns.

```python
data = [
    (1, "Alice", "Engineering", 75000),
    (2, "Bob", "Sales", 82000),
]

schema = StructType([
    StructField("EmployeeID", IntegerType()),
    StructField("EmployeeName", StringType()),
    StructField("DepartmentName", StringType()),
    StructField("AnnualSalary", IntegerType()),
])

df = spark.createDataFrame(data, schema)

# Task: Rename to: emp_id, emp_name, dept_name, annual_salary
# Select only: emp_id, emp_name, annual_salary
```

---

## Week 2: Medium Problems (Window Functions, Advanced Joins, Aggregations)

### [ ] Problem 11: Rank Within Groups
**Difficulty:** Medium
**Topics:** Window functions, rank, partitionBy
**Time:** 20-25 min

Rank employees by salary within each department. Show rank, employee name, department, salary.

```python
data = [
    (1, "Alice",   "Engineering", 95000),
    (2, "Bob",     "Engineering", 88000),
    (3, "Charlie", "Sales",       75000),
    (4, "Diana",   "Sales",       82000),
    (5, "Eve",     "Engineering", 92000),
    (6, "Frank",   "Sales",       78000),
    (7, "Grace",   "Marketing",   85000),
]

schema = StructType([
    StructField("emp_id", IntegerType()),
    StructField("name", StringType()),
    StructField("department", StringType()),
    StructField("salary", IntegerType()),
])

df = spark.createDataFrame(data, schema)

# Task: Add a "rank" column showing rank by salary within each department
# (highest salary = rank 1)
# Expected:
# Engineering: Alice(1), Eve(2), Bob(3)
# Sales: Diana(1), Frank(2), Charlie(3)
# Marketing: Grace(1)
```

**Hint:** Use `Window.partitionBy("department").orderBy(col("salary").desc())` with `rank()`

---

### [ ] Problem 12: Running Total
**Difficulty:** Medium
**Topics:** Window functions, sum, rowsBetween
**Time:** 20-25 min

Calculate running total of sales for each salesperson ordered by date.

```python
data = [
    ("Alice", "2026-01-10", 500.00),
    ("Alice", "2026-01-15", 300.00),
    ("Alice", "2026-01-20", 450.00),
    ("Bob",   "2026-01-12", 600.00),
    ("Bob",   "2026-01-18", 200.00),
    ("Bob",   "2026-01-22", 350.00),
]

schema = StructType([
    StructField("salesperson", StringType()),
    StructField("sale_date", StringType()),
    StructField("amount", DoubleType()),
])

df = spark.createDataFrame(data, schema)

# Task: Add "running_total" column
# Expected for Alice:
# 2026-01-10  500.00   running_total: 500.00
# 2026-01-15  300.00   running_total: 800.00
# 2026-01-20  450.00   running_total: 1250.00
```

**Hint:** Use `Window.partitionBy("salesperson").orderBy("sale_date").rowsBetween(Window.unboundedPreceding, Window.currentRow)`

---

### [ ] Problem 13: Find Max Per Group (Window)
**Difficulty:** Medium
**Topics:** Window functions, max, filter
**Time:** 20 min

For each department, find the employee with the highest salary (return full row, not just the max value).

```python
data = [
    (1, "Alice",   "Engineering", 95000),
    (2, "Bob",     "Engineering", 88000),
    (3, "Charlie", "Sales",       75000),
    (4, "Diana",   "Sales",       82000),
    (5, "Eve",     "Marketing",   85000),
]

schema = StructType([
    StructField("emp_id", IntegerType()),
    StructField("name", StringType()),
    StructField("department", StringType()),
    StructField("salary", IntegerType()),
])

df = spark.createDataFrame(data, schema)

# Task: Return the highest-paid employee in each department
# Expected:
# Engineering: Alice  95000
# Sales:       Diana  82000
# Marketing:   Eve    85000
```

**Approach 1:** Window function to get max salary per dept, then filter
**Approach 2:** GroupBy + join back to original

---

### [ ] Problem 14: Pivot Table
**Difficulty:** Medium
**Topics:** pivot, groupBy
**Time:** 20-25 min

Pivot sales data so each product category becomes a column showing total sales per region.

```python
data = [
    ("North", "Electronics", 5000),
    ("North", "Clothing",    3000),
    ("South", "Electronics", 7000),
    ("South", "Clothing",    2000),
    ("East",  "Electronics", 6000),
    ("East",  "Clothing",    4000),
    ("North", "Electronics", 3000),
]

schema = StructType([
    StructField("region", StringType()),
    StructField("category", StringType()),
    StructField("sales", IntegerType()),
])

df = spark.createDataFrame(data, schema)

# Task: Pivot to show:
# region  Electronics  Clothing
# North      8000        3000
# South      7000        2000
# East       6000        4000
```

**Hint:** `df.groupBy("region").pivot("category").sum("sales")`

---

### [ ] Problem 15: Explode Array Column
**Difficulty:** Medium
**Topics:** explode, arrays
**Time:** 20 min

You have a column with array values. Explode it so each array element becomes a separate row.

```python
data = [
    (1, "Alice",   ["Python", "SQL", "Spark"]),
    (2, "Bob",     ["Java", "Scala"]),
    (3, "Charlie", ["Python", "Java", "Scala", "SQL"]),
]

schema = StructType([
    StructField("emp_id", IntegerType()),
    StructField("name", StringType()),
    StructField("skills", ArrayType(StringType())),
])

df = spark.createDataFrame(data, schema)

# Task: Explode skills array to create one row per skill
# Expected:
# 1  Alice    Python
# 1  Alice    SQL
# 1  Alice    Spark
# 2  Bob      Java
# 2  Bob      Scala
# ...
```

**Hint:** Use `explode()` function

---

### [ ] Problem 16: Self-Join to Find Pairs
**Difficulty:** Medium
**Topics:** self-join, alias
**Time:** 25 min

Find all pairs of employees who work in the same department (exclude pairing with self, avoid duplicates).

```python
data = [
    (1, "Alice",   "Engineering"),
    (2, "Bob",     "Engineering"),
    (3, "Charlie", "Sales"),
    (4, "Diana",   "Sales"),
    (5, "Eve",     "Engineering"),
]

schema = StructType([
    StructField("emp_id", IntegerType()),
    StructField("name", StringType()),
    StructField("department", StringType()),
])

df = spark.createDataFrame(data, schema)

# Task: Find all unique pairs of employees in the same department
# Expected:
# Alice    Bob      Engineering
# Alice    Eve      Engineering
# Bob      Eve      Engineering
# Charlie  Diana    Sales

# Avoid:
# - Self-pairs (Alice-Alice)
# - Duplicate pairs (Alice-Bob and Bob-Alice counted once)
```

**Hint:** Self-join on department with condition `e1.emp_id < e2.emp_id`

---

### [ ] Problem 17: Lead and Lag
**Difficulty:** Medium
**Topics:** Window, lead, lag
**Time:** 25 min

For each employee's salary history, show previous salary, current salary, and next salary.

```python
data = [
    ("Alice", "2024-01", 70000),
    ("Alice", "2024-07", 75000),
    ("Alice", "2025-01", 80000),
    ("Alice", "2025-07", 85000),
    ("Bob",   "2024-01", 65000),
    ("Bob",   "2024-07", 68000),
    ("Bob",   "2025-01", 72000),
]

schema = StructType([
    StructField("name", StringType()),
    StructField("period", StringType()),
    StructField("salary", IntegerType()),
])

df = spark.createDataFrame(data, schema)

# Task: Add columns "prev_salary" and "next_salary" using lag() and lead()
# Expected for Alice 2025-01:
# prev_salary: 75000
# current:     80000
# next_salary: 85000
```

---

### [ ] Problem 18: Find Duplicates
**Difficulty:** Medium
**Topics:** groupBy, having, count
**Time:** 20 min

Find all customer emails that appear more than once in the dataset.

```python
data = [
    (1, "Alice", "alice@example.com"),
    (2, "Bob",   "bob@example.com"),
    (3, "Alice", "alice@example.com"),
    (4, "Charlie", "charlie@example.com"),
    (5, "Bob",   "bob@example.com"),
    (6, "Diana", "diana@example.com"),
]

schema = StructType([
    StructField("id", IntegerType()),
    StructField("name", StringType()),
    StructField("email", StringType()),
])

df = spark.createDataFrame(data, schema)

# Task: Show emails that appear more than once and their count
# Expected:
# alice@example.com     2
# bob@example.com       2
```

**Hint:** `groupBy("email").count().filter("count > 1")`

---

### [ ] Problem 19: Union and Deduplicate
**Difficulty:** Medium
**Topics:** union, dropDuplicates
**Time:** 20 min

Combine two DataFrames and remove duplicates.

```python
df1_data = [
    (1, "Alice", "Engineering"),
    (2, "Bob",   "Sales"),
    (3, "Charlie", "Marketing"),
]

df2_data = [
    (2, "Bob",   "Sales"),      # duplicate
    (4, "Diana", "Engineering"),
    (5, "Eve",   "Marketing"),
]

schema = StructType([
    StructField("emp_id", IntegerType()),
    StructField("name", StringType()),
    StructField("department", StringType()),
])

df1 = spark.createDataFrame(df1_data, schema)
df2 = spark.createDataFrame(df2_data, schema)

# Task: Union df1 and df2, then remove duplicates
# Expected: 5 unique employees (Bob appears once)
```

---

### [ ] Problem 20: Month-Over-Month Growth
**Difficulty:** Medium
**Topics:** Window, lag, date functions
**Time:** 30 min

Calculate month-over-month sales growth percentage for each product category.

```python
data = [
    ("Electronics", "2026-01", 10000),
    ("Electronics", "2026-02", 12000),
    ("Electronics", "2026-03", 11000),
    ("Clothing",    "2026-01",  5000),
    ("Clothing",    "2026-02",  6000),
    ("Clothing",    "2026-03",  7500),
]

schema = StructType([
    StructField("category", StringType()),
    StructField("month", StringType()),
    StructField("sales", IntegerType()),
])

df = spark.createDataFrame(data, schema)

# Task: Calculate growth % = ((current - previous) / previous) * 100
# Round to 1 decimal. Show null for first month.
# Expected:
# Electronics 2026-01  10000  null
# Electronics 2026-02  12000  20.0%
# Electronics 2026-03  11000  -8.3%
# Clothing    2026-01   5000  null
# Clothing    2026-02   6000  20.0%
# Clothing    2026-03   7500  25.0%
```

**Hint:** Use `lag()` over window partitioned by category, ordered by month

---

### [ ] Problem 21: Complex Filter with Multiple Conditions
**Difficulty:** Medium
**Topics:** filter, and/or logic
**Time:** 20 min

Filter transactions that meet multiple business rules.

```python
data = [
    (1, "Alice",   "2026-01-15", 150.00, "Online"),
    (2, "Bob",     "2026-01-20", 80.00,  "Store"),
    (3, "Charlie", "2026-02-01", 200.00, "Online"),
    (4, "Diana",   "2026-02-10", 50.00,  "Online"),
    (5, "Eve",     "2026-03-05", 120.00, "Store"),
]

schema = StructType([
    StructField("txn_id", IntegerType()),
    StructField("customer", StringType()),
    StructField("date", StringType()),
    StructField("amount", DoubleType()),
    StructField("channel", StringType()),
])

df = spark.createDataFrame(data, schema)

# Task: Filter transactions where:
# (amount > 100 AND channel = "Online") OR (amount > 150 AND channel = "Store")
# Expected: 3 transactions (Alice Online, Charlie Online, Eve Store)
```

---

### [ ] Problem 22: Calculate Percentiles
**Difficulty:** Medium
**Topics:** approx_percentile, aggregate functions
**Time:** 20-25 min

Calculate the 25th, 50th (median), and 75th percentile of salaries.

```python
data = [
    (1, "Alice",   75000),
    (2, "Bob",     82000),
    (3, "Charlie", 68000),
    (4, "Diana",   95000),
    (5, "Eve",     71000),
    (6, "Frank",   88000),
    (7, "Grace",   79000),
    (8, "Henry",   84000),
]

schema = StructType([
    StructField("emp_id", IntegerType()),
    StructField("name", StringType()),
    StructField("salary", IntegerType()),
])

df = spark.createDataFrame(data, schema)

# Task: Calculate 25th, 50th, 75th percentile of salary
# Use approx_percentile or percentile_approx
```

**Hint:** `df.agg(expr("percentile_approx(salary, array(0.25, 0.5, 0.75))"))`

---

### [ ] Problem 23: Broadcast Join Optimization
**Difficulty:** Medium
**Topics:** broadcast join, optimization
**Time:** 25 min

Join a large transactions table with a small lookup table using broadcast join.

```python
# Large table (transactions)
transactions = [
    (1, 101, 150.00),
    (2, 102, 200.00),
    (3, 101, 180.00),
    (4, 103, 220.00),
    (5, 102, 160.00),
] * 1000  # Simulate large dataset

# Small table (products)
products = [
    (101, "Laptop"),
    (102, "Mouse"),
    (103, "Keyboard"),
]

txn_schema = StructType([
    StructField("txn_id", IntegerType()),
    StructField("product_id", IntegerType()),
    StructField("amount", DoubleType()),
])

prod_schema = StructType([
    StructField("product_id", IntegerType()),
    StructField("product_name", StringType()),
])

txn_df = spark.createDataFrame(transactions, txn_schema)
prod_df = spark.createDataFrame(products, prod_schema)

# Task: Join with broadcast hint on products table
# Show txn_id, product_name, amount
```

**Hint:** `from pyspark.sql.functions import broadcast` then `txn_df.join(broadcast(prod_df), "product_id")`

---

### [ ] Problem 24: Aggregate Multiple Columns
**Difficulty:** Medium
**Topics:** agg, multiple aggregations
**Time:** 20 min

For each department, calculate: count of employees, total salary, avg salary, min salary, max salary.

```python
data = [
    (1, "Alice",   "Engineering", 95000),
    (2, "Bob",     "Engineering", 88000),
    (3, "Charlie", "Sales",       75000),
    (4, "Diana",   "Sales",       82000),
    (5, "Eve",     "Engineering", 92000),
    (6, "Frank",   "Sales",       78000),
]

schema = StructType([
    StructField("emp_id", IntegerType()),
    StructField("name", StringType()),
    StructField("department", StringType()),
    StructField("salary", IntegerType()),
])

df = spark.createDataFrame(data, schema)

# Task: Group by department, show:
# - employee_count
# - total_salary
# - avg_salary (rounded to 2 decimals)
# - min_salary
# - max_salary
```

---

### [ ] Problem 25: Cumulative Distribution
**Difficulty:** Medium
**Topics:** Window, cume_dist
**Time:** 25 min

Calculate the cumulative distribution of salaries (what % of employees earn less than or equal to each salary).

```python
data = [
    (1, "Alice",   75000),
    (2, "Bob",     82000),
    (3, "Charlie", 68000),
    (4, "Diana",   95000),
    (5, "Eve",     71000),
    (6, "Frank",   88000),
]

schema = StructType([
    StructField("emp_id", IntegerType()),
    StructField("name", StringType()),
    StructField("salary", IntegerType()),
])

df = spark.createDataFrame(data, schema)

# Task: Add column "percentile_rank" showing cumulative distribution
# Use cume_dist() window function
# Expected: Charlie (68k) at ~0.167, Diana (95k) at 1.0
```

---

## Week 3-4: Hard Problems (Complex Windows, Performance, Advanced Patterns)

### [ ] Problem 26: Session Analysis (Time-Based Grouping)
**Difficulty:** Hard
**Topics:** Window, lag, session detection
**Time:** 35-40 min

Identify user sessions. A new session starts if more than 30 minutes have passed since the last event.

```python
from datetime import datetime

data = [
    ("Alice", "2026-06-08 09:00:00"),
    ("Alice", "2026-06-08 09:10:00"),  # same session
    ("Alice", "2026-06-08 09:15:00"),  # same session
    ("Alice", "2026-06-08 10:00:00"),  # new session (45 min gap)
    ("Alice", "2026-06-08 10:05:00"),  # same session
    ("Bob",   "2026-06-08 09:05:00"),
    ("Bob",   "2026-06-08 09:40:00"),  # new session (35 min gap)
    ("Bob",   "2026-06-08 09:50:00"),  # same session
]

schema = StructType([
    StructField("user", StringType()),
    StructField("event_time", StringType()),
])

df = spark.createDataFrame(data, schema)

# Task:
# 1. Convert event_time to timestamp
# 2. For each user, calculate time difference from previous event
# 3. Mark session boundary when gap > 30 minutes
# 4. Assign session_id (cumulative sum of session boundaries)
# 5. Show user, event_time, session_id

# Expected:
# Alice has 2 sessions: [09:00-09:15], [10:00-10:05]
# Bob has 2 sessions: [09:05], [09:40-09:50]
```

**Hint:** Use `lag()` to get previous timestamp, calculate diff in minutes, use `when()` to flag session start, then `sum()` over window for session_id

---

### [ ] Problem 27: Top N Per Group with Ties
**Difficulty:** Hard
**Topics:** Window, dense_rank, filter
**Time:** 35 min

Find top 2 salaries in each department, but include ties (use dense_rank instead of rank).

```python
data = [
    (1, "Alice",   "Engineering", 95000),
    (2, "Bob",     "Engineering", 95000),  # tie for 1st
    (3, "Charlie", "Engineering", 88000),
    (4, "Diana",   "Sales",       82000),
    (5, "Eve",     "Sales",       82000),  # tie for 1st
    (6, "Frank",   "Sales",       78000),
    (7, "Grace",   "Sales",       75000),
]

schema = StructType([
    StructField("emp_id", IntegerType()),
    StructField("name", StringType()),
    StructField("department", StringType()),
    StructField("salary", IntegerType()),
])

df = spark.createDataFrame(data, schema)

# Task: Show top 2 salaries per department (include ties)
# Expected Engineering: Alice, Bob (both rank 1), Charlie (rank 2) = 3 rows
# Expected Sales: Diana, Eve (both rank 1), Frank (rank 2) = 3 rows
```

**Difference:** `rank()` would give 1, 1, 3 vs `dense_rank()` gives 1, 1, 2

---

### [ ] Problem 28: Skewed Join Optimization
**Difficulty:** Hard
**Topics:** salting, skew handling
**Time:** 40 min

Handle a highly skewed join where one key has disproportionately many records.

```python
# Skewed large table (80% of records have product_id = 101)
large_data = [(i, 101, 100.0) for i in range(1, 801)] + \
             [(i, 102, 150.0) for i in range(801, 901)] + \
             [(i, 103, 200.0) for i in range(901, 1001)]

# Small dimension table
small_data = [
    (101, "Laptop"),
    (102, "Mouse"),
    (103, "Keyboard"),
]

large_schema = StructType([
    StructField("txn_id", IntegerType()),
    StructField("product_id", IntegerType()),
    StructField("amount", DoubleType()),
])

small_schema = StructType([
    StructField("product_id", IntegerType()),
    StructField("product_name", StringType()),
])

large_df = spark.createDataFrame(large_data, large_schema)
small_df = spark.createDataFrame(small_data, small_schema)

# Task: Implement salting to distribute product_id=101 across partitions
# Steps:
# 1. Add salt column (random 0-9) to large_df
# 2. Replicate small_df 10 times with salt values 0-9
# 3. Join on (product_id, salt)
# 4. Remove salt column from result
```

**Hint:** This is an advanced optimization technique for production workloads with skewed keys

---

### [ ] Problem 29: Complex Multi-Level Aggregation
**Difficulty:** Hard
**Topics:** groupBy, rollup, cube
**Time:** 35-40 min

Calculate sales totals at multiple levels: by region, by category, by region+category, and grand total.

```python
data = [
    ("North", "Electronics", 5000),
    ("North", "Clothing",    3000),
    ("South", "Electronics", 7000),
    ("South", "Clothing",    2000),
    ("East",  "Electronics", 6000),
    ("East",  "Clothing",    4000),
]

schema = StructType([
    StructField("region", StringType()),
    StructField("category", StringType()),
    StructField("sales", IntegerType()),
])

df = spark.createDataFrame(data, schema)

# Task: Use rollup or cube to show:
# 1. Total by region and category
# 2. Total by region (all categories)
# 3. Total by category (all regions)
# 4. Grand total (all regions, all categories)

# Expected output includes rows like:
# North  Electronics   5000   (detail)
# North  null          8000   (region total)
# null   Electronics  18000   (category total)
# null   null         27000   (grand total)
```

**Hint:** Use `rollup("region", "category")` or `cube("region", "category")`

---

### [ ] Problem 30: Incremental Processing Pattern
**Difficulty:** Hard
**Topics:** Window, checkpoint, watermark concepts
**Time:** 40-45 min

Process only new records since last run (simulate incremental batch processing).

```python
# Full dataset
full_data = [
    (1, "Alice",  "2026-06-01", 100.0),
    (2, "Bob",    "2026-06-02", 150.0),
    (3, "Charlie","2026-06-03", 200.0),
    (4, "Diana",  "2026-06-04", 120.0),
    (5, "Eve",    "2026-06-05", 180.0),
    (6, "Frank",  "2026-06-06", 210.0),
]

schema = StructType([
    StructField("txn_id", IntegerType()),
    StructField("customer", StringType()),
    StructField("date", StringType()),
    StructField("amount", DoubleType()),
])

df = spark.createDataFrame(full_data, schema)

# Simulate: last processed date was 2026-06-03
last_processed_date = "2026-06-03"

# Task:
# 1. Filter records with date > last_processed_date
# 2. Calculate daily totals for these new records
# 3. Join with historical aggregates to get cumulative totals
# 4. Update checkpoint to new max date

# This simulates an incremental ETL pattern where you only process
# new data and merge with existing aggregates
```

**Pattern:** Common in production for processing only delta/incremental data

---

## Solution Template

```python
"""
Problem XX: <Problem Name>
Difficulty: <Easy/Medium/Hard>
Topics: <list topics>

Problem Statement:
<Copy from above>

Sample Data:
<Include the data from problem>

Expected Output:
<What the result should look like>

Approach:
1. <Step 1>
2. <Step 2>
...

Spark Optimization Notes:
- <Any broadcast hints, partitioning, caching considerations>
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import Window
from pyspark.sql.types import *

spark = SparkSession.builder.appName("problem_XX").master("local[*]").getOrCreate()

# Sample data creation
data = [
    # ... from problem
]

schema = StructType([
    # ... from problem
])

df = spark.createDataFrame(data, schema)

# Solution
result = df.<your transformations>

result.show()

# Cleanup
spark.stop()
```

---

## Daily Practice Routine

**Week 1 (Easy):**
- Days 1-2: Problems 1-3 (Filter, withColumn, GroupBy)
- Days 3-4: Problems 4-6 (Dates, when/otherwise, sorting)
- Days 5-7: Problems 7-10 (Duplicates, joins, nulls, rename)

**Week 2 (Medium - Part 1):**
- Days 8-9: Problems 11-13 (Window basics: rank, running total, max per group)
- Days 10-11: Problems 14-16 (Pivot, explode, self-join)
- Days 12-14: Problems 17-19 (Lead/lag, finding duplicates, union)

**Week 3 (Medium - Part 2):**
- Days 15-16: Problems 20-22 (Growth calcs, complex filters, percentiles)
- Days 17-18: Problems 23-25 (Broadcast joins, multi-agg, cume_dist)
- Days 19-21: Review all Medium, redo challenging ones

**Week 4 (Hard + Review):**
- Days 22-23: Problems 26-27 (Session analysis, dense_rank with ties)
- Days 24-25: Problems 28-29 (Skewed joins, rollup/cube)
- Day 26: Problem 30 (Incremental processing)
- Days 27-28: Review all Hard, practice optimization techniques

---

## Key Concepts Coverage

**Transformations:**
- select, filter, withColumn, withColumnRenamed ✓
- groupBy, agg, pivot ✓
- join (inner, left, broadcast) ✓
- union, dropDuplicates ✓
- explode, arrays ✓

**Functions:**
- Aggregations: sum, count, avg, min, max, percentile ✓
- Date: to_date, year, month, dayofmonth ✓
- Conditional: when, otherwise ✓
- String: concat, split, regex ✓
- Math: round, abs, ceil, floor ✓

**Window Functions:**
- rank, dense_rank, row_number ✓
- lead, lag ✓
- sum (running total), avg ✓
- cume_dist, percent_rank ✓
- rowsBetween, rangeBetween ✓

**Optimization:**
- broadcast joins ✓
- salting for skew ✓
- rollup/cube for multi-level agg ✓
- incremental processing ✓

---

## Notes

- All problems include complete sample data (no external files needed)
- Focus on Medium problems (11-25) for interviews
- Hard problems (26-30) demonstrate senior/staff level depth
- Easy problems (1-10) build foundation quickly
- Review your PySpark problem in `fundamentals/spark/prep/problems.py` for additional practice
- Use existing datasets in `data/raw/` when you want realistic multi-file scenarios

Good luck!
