-- question statement
    -- Find supplier_id, product_id, and the date(s) when stock_quantity
    -- stayed below 50 for 2 or more CONSECUTIVE calendar days.


-- create table statement
create table stock (
    supplier_id     int,
    product_id      int,
    stock_quantity  int,
    record_date     date
);


-- insert data
INSERT INTO stock (supplier_id, product_id, stock_quantity, record_date)
VALUES
    (1, 1, 60, '2022-01-01'),
    (1, 1, 40, '2022-01-02'),
    (1, 1, 35, '2022-01-03'),
    (1, 1, 45, '2022-01-04'),
    (1, 1, 51, '2022-01-06'),
    (1, 1, 55, '2022-01-09'),
    (1, 1, 25, '2022-01-10'),
    (1, 1, 48, '2022-01-11'),
    (1, 1, 45, '2022-01-15'),
    (1, 1, 38, '2022-01-16'),
    (1, 2, 45, '2022-01-08'),
    (1, 2, 40, '2022-01-09'),
    (2, 1, 45, '2022-01-06'),
    (2, 1, 55, '2022-01-07'),
    (2, 2, 45, '2022-01-08'),
    (2, 2, 48, '2022-01-09'),
    (2, 2, 35, '2022-01-10'),
    (2, 2, 52, '2022-01-15'),
    (2, 2, 23, '2022-01-16');


-- required output (verified: executed against sqlite3, dates translated via julianday())
"supplier_id","product_id","record_date","no_of_days"
1,1,2022-01-02,3
1,1,2022-01-10,2
1,1,2022-01-15,2
1,2,2022-01-08,2
2,2,2022-01-08,3

-- streak detail, for reference (start -> end):
-- (1,1): 01-02 -> 01-04  (3 consecutive days: 40, 35, 45)
-- (1,1): 01-10 -> 01-11  (2 consecutive days: 25, 48)
-- (1,1): 01-15 -> 01-16  (2 consecutive days: 45, 38)
-- (1,2): 01-08 -> 01-09  (2 consecutive days: 45, 40)
-- (2,2): 01-08 -> 01-10  (3 consecutive days: 45, 48, 35)
-- (2,1) excluded: only 01-06 is below 50; 01-07 is 55, so no
--   2-day streak ever happens for that supplier/product.
-- (2,2)'s 01-16 (23, below 50) excluded: it's isolated -- 01-15
--   (52) was above 50, so 01-16 doesn't extend any streak and is
--   its own group of size 1.


-- solution steps

-- Step 1:
-- Filter to only rows where stock_quantity < 50. This alone loses
-- information about which calendar days were "safe," which is
-- exactly what Step 2 needs to recover.

-- Step 2:
-- For each filtered row, compute the number of calendar days since
-- the PREVIOUS filtered row for that supplier/product (lag ordered
-- by record_date). Using lag(..., 1, record_date) as the default
-- means the very first row per partition diffs against itself,
-- giving diff_in_days = 0 -- a safe sentinel so it always falls into
-- the "same streak" bucket rather than needing special-case NULL
-- handling.

-- Step 3:
-- If diff_in_days <= 1, the current row is truly the next calendar
-- day after the previous low-stock row -> same streak. If it's more
-- than 1 day, a "safe" (>=50) day existed in between (or no record
-- for that day at all) -> the streak breaks. A running sum of these
-- break-flags gives each row a streak/group id (classic
-- gaps-and-islands pattern).

-- Step 4:
-- Group by (supplier_id, product_id, flag) and keep only groups
-- with more than 1 row -- i.e. streaks of 2+ genuinely consecutive
-- low-stock days.


-- sql solution (yours -- verified correct)
with cte as (
    select *,
        lag(record_date, 1, record_date) over (partition by supplier_id, product_id order by record_date) as previous_date,
        (record_date - lag(record_date, 1, record_date) over (partition by supplier_id, product_id order by record_date)) as diff_in_days
    from stock
    where stock_quantity < 50
),
group_flag as (
    select *,
        sum(case when diff_in_days <= 1 then 0 else 1 end) over (partition by supplier_id, product_id order by record_date) as flag
    from cte
)
select
    supplier_id,
    product_id,
    min(record_date) as record_date,
    count(*) as no_of_days
from group_flag
group by supplier_id, product_id, flag
having count(*) > 1
order by supplier_id, product_id, record_date;
