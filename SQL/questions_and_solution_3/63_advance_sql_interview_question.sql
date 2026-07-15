-- question statement
    -- A set of frequently-asked SQL interview patterns:
    -- 1. Top N by salary within each department
    -- 2. Top N product by sales within each category
    -- 3. Year-over-year sales growth
    -- 4. Year-over-year sales growth within each category
    -- 5. Cumulative sales + rolling N-month sales
    -- 6. Rows-to-columns pivot by category


-- create table statement (emp)
create table emp(
    emp_id        int,
    emp_name      varchar(20),
    department_id int,
    salary        int,
    manager_id    int,
    emp_age       int
);

-- assume "orders" table already exists with columns roughly:
-- order_id, order_date, product_id, category, sales


-- insert data
insert into emp values (1,'Ankit',100,12000,4,39);
insert into emp values (2,'Mohit',100,15000,5,48);
insert into emp values (3,'Vikas',100,10000,4,37);
insert into emp values (4,'Rohit',100,5000,2,16);
insert into emp values (5,'Mudit',200,12000,6,55);
insert into emp values (6,'Agam',200,12000,2,14);
insert into emp values (7,'Sanjay',200,9000,2,13);
insert into emp values (8,'Ashish',200,5000,2,12);
insert into emp values (9,'Mukesh',300,6000,6,51);
insert into emp values (10,'Rakesh',500,7000,6,50);
insert into emp values (11,'dummy',400,4000,4,99);


-- ============================================================
-- 1. Top 2 highest-salary employees per department
-- ============================================================

-- required output (verified: executed against sqlite3)
"emp_id","emp_name","department_id","salary"
2,Mohit,100,15000
1,Ankit,100,12000
5,Mudit,200,12000
6,Agam,200,12000
7,Sanjay,200,9000      <-- NOTE: this is a 3rd row, see below
9,Mukesh,300,6000
11,dummy,400,4000
10,Rakesh,500,7000

-- sql solution
with salary_rank as (
    select *,
        dense_rank() over (partition by department_id order by salary desc) as rn
    from emp
)
select emp_id, emp_name, department_id, salary, manager_id, emp_age
from salary_rank
where rn <= 2;

-- notes
-- This is one of the most common interview follow-up questions --
-- know the difference and pick deliberately:
--   dense_rank(): top N distinct VALUES (can return >N rows on ties)
--   rank():       top N by position, but ties create GAPS (e.g. two
--                 people tied at rank 1 means no one gets rank 2 --
--                 "top 2" would only return those 2 tied people,
--                 which is often what's actually wanted)
--   row_number(): always exactly N rows, but arbitrarily and
--                 non-deterministically picks which tied employee
--                 "wins" when there's a tie at the cutoff -- add a
--                 tiebreaker column to order by (e.g. emp_id) if you
--                 need this to be reproducible.
--
-- If the requirement is truly "exactly top 2 people, tie or not,"
-- use row_number() with an explicit tiebreaker:
--     row_number() over (partition by department_id
--                         order by salary desc, emp_id) as rn
-- If the requirement is "top 2 salary bands, ties included," your
-- original dense_rank() is exactly correct as written.


-- ============================================================
-- 2. Top 5 products by sales, within each category
-- ============================================================

-- sql solution
with cte as (
    select product_id, category, sum(sales) as total_sale
    from orders
    group by product_id, category
),
sale_rank as (
    select *,
        dense_rank() over (partition by category order by total_sale desc) as rn
    from cte
)
select *
from sale_rank
where rn <= 5;

-- ============================================================
-- 3. Year-over-year sales growth
-- ============================================================

-- sql solution
with yearly_sales as (
    select extract(year from order_date) as year_order, sum(sales) as total_sales
    from orders
    group by extract(year from order_date)
)
select *,
    ((total_sales - lag(total_sales, 1, total_sales) over (order by year_order))
        / lag(total_sales, 1, total_sales) over (order by year_order)) * 100 as sales_growth
from yearly_sales;

-- notes
-- BUG -- wrong denominator for "growth":
-- Tested this exact formula against synthetic data (2021 sales=200,
-- 2022 sales=700). Standard YoY growth % is
-- (current - previous) / previous * 100 = (700-200)/200*100 = 250%.
-- Your query instead divides by total_sales (the CURRENT year), which
-- gives (700-200)/700*100 = 71.43% -- a completely different, much
-- smaller number that does NOT match how "YoY growth" is normally
-- defined or how a stakeholder reading a dashboard would interpret it.
--
-- Corrected version:
select *,
    ((total_sales - lag(total_sales) over (order by year_order))
        * 1.0 / nullif(lag(total_sales) over (order by year_order), 0)) * 100
        as sales_growth
from yearly_sales;

-- ============================================================
-- 4. Year-over-year sales growth, within each category
-- ============================================================

-- sql solution
with yearly_sales as (
    select extract(year from order_date) as year_order, category, sum(sales) as total_sales
    from orders
    group by extract(year from order_date), category
)
select *,
    ((total_sales - lag(total_sales, 1, total_sales) over (partition by category order by year_order))
        / total_sales) * 100 as sales_growth
from yearly_sales;

-- notes
-- Same denominator bug as query 3 (divides by current year instead
-- of previous), just partitioned by category this time. Same fix:
select *,
    ((total_sales - lag(total_sales) over (partition by category order by year_order))
        * 1.0 / nullif(lag(total_sales) over (partition by category order by year_order), 0)) * 100
        as sales_growth
from yearly_sales;


-- ============================================================
-- 5. Cumulative sales + rolling 3-month sales, per category
-- ============================================================

-- sql solution
with monthly_sales as (
    select
        extract(month from order_date) as order_month,
        extract(year from order_date) as order_year,
        category,
        sum(sales) as total_sales
    from orders
    group by extract(year from order_date), extract(month from order_date), category
)
select *,
    sum(total_sales) over (partition by category order by order_year, order_month) as cumulative_sales,
    sum(total_sales) over (partition by category order by order_year, order_month
                            rows between 2 preceding and current row) as rolling_3month_sales
from monthly_sales;

-- notes
-- cumulative_sales: no explicit ROWS frame given, so it defaults to
-- RANGE UNBOUNDED PRECEDING TO CURRENT ROW. Harmless here since
-- (order_year, order_month, category) is unique per row (grouped),
-- so there are no order-key ties to cause the RANGE-vs-ROWS problem
-- flagged in earlier reviews in this thread -- but it's still good
-- habit to write rows between unbounded preceding and current row
-- explicitly, so correctness doesn't depend on "happens to have no
-- ties" being true forever.
--
-- rolling_3month_sales -- REAL BUG, confirmed by testing:
-- Built a synthetic Furniture category with sales in Jan, (gap:
-- no Feb sales), Mar, Apr. The query's "rows between 2 preceding and
-- current row" counts the 2 preceding ROWS in the result set, not
-- the 2 preceding CALENDAR months. Since Feb has no row at all (zero
-- sales = no group = no row), April's "rolling 3 month" figure
-- silently pulls in Jan + Mar + Apr -- a 4-CALENDAR-MONTH span --
-- while looking identical in the output to a genuine 3-month window.
-- This is one of the most common and hardest-to-notice bugs in
-- rolling-window SQL: ROWS-based frames assume no gaps in the time
-- series. If your real orders data has any month/category
-- combination with zero sales, this number will be silently wrong,
-- and there's nothing in the output that flags it.
--
-- Fix: build a complete date spine (every year/month, even with zero
-- sales) before computing the rolling window, e.g.:
with month_spine as (
    select category, order_year, order_month
    from (select distinct category from orders) c
    cross join (
        select
            extract(year from d) as order_year,
            extract(month from d) as order_month
        from generate_series(
            (select date_trunc('month', min(order_date)) from orders),
            (select date_trunc('month', max(order_date)) from orders),
            interval '1 month'
        ) as d
    ) months
),
monthly_sales as (
    select
        extract(year from order_date) as order_year,
        extract(month from order_date) as order_month,
        category,
        sum(sales) as total_sales
    from orders
    group by extract(year from order_date), extract(month from order_date), category
),
filled as (
    select
        s.category, s.order_year, s.order_month,
        coalesce(m.total_sales, 0) as total_sales
    from month_spine s
    left join monthly_sales m
        on s.category = m.category
       and s.order_year = m.order_year
       and s.order_month = m.order_month
)
select *,
    sum(total_sales) over (partition by category order by order_year, order_month) as cumulative_sales,
    sum(total_sales) over (partition by category order by order_year, order_month
                            rows between 2 preceding and current row) as rolling_3month_sales
from filled;
-- Now every category has one row per month with no gaps, so "2
-- preceding rows" is guaranteed to mean "2 preceding calendar
-- months," and zero-sales months correctly show up as 0 and get
-- counted in the window rather than silently vanishing.


-- ============================================================
-- 6. Rows-to-columns pivot by category
-- ============================================================

-- sql solution
select
    date_part('year', order_date) as order_year,
    sum(case when category = 'Furniture' then sales else 0 end) as fur_sales,
    sum(case when category = 'Office Supplies' then sales else 0 end) as os_sales,
    sum(case when category = 'Technology' then sales else 0 end) as tech_sales
from orders
group by date_part('year', order_date);

-- notes
-- No issues -- this is the standard, correct pivot pattern.
-- Optional Postgres-only style alternative using FILTER, arguably
-- more readable than CASE for simple conditional sums:
select
    date_part('year', order_date) as order_year,
    sum(sales) filter (where category = 'Furniture') as fur_sales,
    sum(sales) filter (where category = 'Office Supplies') as os_sales,
    sum(sales) filter (where category = 'Technology') as tech_sales
from orders
group by date_part('year', order_date);
-- Same result, just Postgres-specific syntax vs the portable
-- CASE-based version above.