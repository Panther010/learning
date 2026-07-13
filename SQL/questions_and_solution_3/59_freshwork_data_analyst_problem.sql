-- question statement
    -- For each sku, find the price at the start of each calendar month
    -- (i.e. price effective on the 1st), and the difference from the
    -- previous month's starting price.


-- create table statement
create table sku (
    sku_id     int,
    price_date date,
    price      int
);


-- insert data
insert into sku values
(1,'2023-01-01',10),
(1,'2023-02-15',15),
(1,'2023-03-03',18),
(1,'2023-03-27',15),
(1,'2023-04-06',20);


-- input data
"sku_id","price_date","price"
1,2023-01-01,10
1,2023-02-15,15
1,2023-03-03,18
1,2023-03-27,15
1,2023-04-06,20


-- required output (verified: executed, matches manual trace of each month's start price)
"sku_id","price_date","price","diff"
1,2023-01-01,10,0
1,2023-02-01,10,0
1,2023-03-01,15,5
1,2023-04-01,15,0
1,2023-05-01,20,5

-- reasoning per month:
-- Jan 1: opening price = 10 (base row)
-- Feb 1: still 10 -- next change (15) doesn't happen until Feb 15
-- Mar 1: 15 -- Feb 15 change is in effect; Mar 3 change (18) hasn't hit yet
-- Apr 1: 15 -- Mar 27 change (back down to 15) is in effect; Apr 6 (20) hasn't hit yet
-- May 1: 20 -- Apr 6 change in effect, extended forward since it's the last known price


-- solution steps

-- Step 1:
-- For each price row, find how long that price stays valid
-- (price_end_date) using lead(price_date) -- the date of the *next*
-- price change for that sku.

-- Step 2:
-- For the last price change (where lead() has nothing to look
-- ahead to and returns NULL), fall back to the first day of the
-- *month after* that change, plus one extra day. This is the key
-- fix: it guarantees the daily calendar actually reaches and
-- includes the 1st of the following month, so that month's opening
-- price shows up in the final output instead of the calendar
-- simply stopping at the last recorded price_date.

-- Step 3:
-- Recursively expand each price into one row per day it's valid,
-- from price_date up to (but not including) price_end_date -- this
-- avoids duplicate rows on transition days.

-- Step 4:
-- Filter the daily calendar down to just day = 1 of each month, and
-- use lag() ordered by price_date to compute the difference from
-- the previous month's opening price. coalesce to 0 for the very
-- first month (no prior month to diff against).


-- sql solution
with recursive price_details as (
    select
        *,
        coalesce(
            lead(price_date) over (order by price_date),
            (date_trunc('month', price_date) + interval '1 month 1 day')::date
        ) as price_end_date
    from sku
),
price_calendar as (
    select sku_id, price_date, price, price_end_date
    from price_details

    union all

    select sku_id, price_date + 1, price, price_end_date
    from price_calendar
    where price_date + 1 < price_end_date
)
select
    sku_id,
    price_date,
    price,
    coalesce(price - lag(price) over (order by price_date), 0) as diff
from price_calendar
where date_part('day', price_date) = 1
order by price_date;


-- notes

-- Correctness (verified by execution):
-- Ran the full query against the sample data. All 5 monthly-start
-- rows and diffs match the manual month-by-month trace above.

-- Why '1 month 1 day' and not just '1 month':
-- An earlier version of this same query (see prior review in this
-- thread) used just '+1 month' as the fallback, which correctly
-- stopped the calendar at the last day of the last known month but
-- did NOT generate a row for the 1st of the *following* month --
-- so if the last price change was mid-month, that next month's
-- opening price would silently be missing from a "start of month"
-- report. Adding '+1 day' to the fallback pushes the boundary just
-- far enough to include that one extra day (the 1st) while the
-- `price_date + 1 < price_end_date` condition still prevents any
-- duplicate/boundary-day rows elsewhere in the calendar.

-- This is a narrow, deliberate fix for this specific report:
-- If you need the calendar to extend further than "just barely
-- capture next month's 1st" (e.g. all the way to today, or to
-- year-end for a full annual view), replace the fallback expression
-- with a fixed anchor date instead of a relative one, e.g.:
--     coalesce(lead(price_date) over (...), '2023-12-31'::date)
-- or a parameterized "as of" date if this runs on a schedule.

-- Efficiency:
-- Recursion depth here is bounded by days-per-sku (roughly 120 rows
-- for ~4 months), which is trivial. For many skus over long date
-- ranges, this daily-expansion approach can get expensive --
-- consider generating only the 1st-of-month dates directly (e.g.
-- via generate_series(min_date, max_date, interval '1 month')) and
-- joining each to the price row whose [price_date, price_end_date)
-- window contains it, rather than materializing every single day
-- just to filter 96% of them back out at the end.

-- Alternative worth considering (avoids full daily expansion):
with month_starts as (
    select
        sku_id,
        generate_series(
            date_trunc('month', min(price_date)),
            date_trunc('month', max(price_date)) + interval '1 month',
            interval '1 month'
        )::date as month_start
    from sku
    group by sku_id
),
price_ranges as (
    select
        *,
        coalesce(
            lead(price_date) over (partition by sku_id order by price_date),
            'infinity'::date
        ) as price_end_date
    from sku
)
select
    m.sku_id,
    m.month_start,
    r.price,
    coalesce(r.price - lag(r.price) over (partition by m.sku_id order by m.month_start), 0) as diff
from month_starts m
join price_ranges r
    on m.sku_id = r.sku_id
   and m.month_start >= r.price_date
   and m.month_start < r.price_end_date
order by m.month_start;
-- Same result, but only ever materializes one row per sku per
-- month -- no wasted daily rows to filter away.