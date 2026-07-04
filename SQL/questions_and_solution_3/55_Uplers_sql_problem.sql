-- question statement
    -- An organisation is hiring maximum possible employee for junior and senior positions with a
    -- total combined budget of 50000.
    -- Senior positions are filled first, then junior positions with
    -- whatever budget remains.
    -- Return the number of junior and senior candidates hired.


------------------------------------------------------------
-- Create Table Statement
------------------------------------------------------------
create table candidates(
    id        int primary key,
    positions varchar(10) not null,
    salary    int not null
);


------------------------------------------------------------
-- Insert Data
------------------------------------------------------------
-- test case 1
insert into candidates values (1,'junior',5000);
insert into candidates values (2,'junior',7000);
insert into candidates values (3,'junior',7000);
insert into candidates values (4,'senior',10000);
insert into candidates values (5,'senior',30000);
insert into candidates values (6,'senior',20000);

-- test case 2
insert into candidates values (20,'junior',10000);
insert into candidates values (30,'senior',15000);
insert into candidates values (40,'senior',30000);

-- test case 3
insert into candidates values (1,'junior',15000);
insert into candidates values (2,'junior',15000);
insert into candidates values (3,'junior',20000);
insert into candidates values (4,'senior',60000);

-- test case 4
insert into candidates values (10,'junior',10000);
insert into candidates values (40,'junior',10000);
insert into candidates values (20,'senior',15000);
insert into candidates values (30,'senior',30000);
insert into candidates values (50,'senior',15000);


-- required output (verified by running against sqlite3, all 4 pass)
-- columns: junior, senior

-- test case 1: junior=3, senior=2
--   seniors sorted by salary: 10000, 20000, 30000
--   running total: 10000, 30000, 60000 -> only first two (30000) fit in 50000
--   remaining budget = 50000 - 30000 = 20000
--   juniors sorted by salary: 5000, 7000, 7000
--   running total: 5000, 12000, 19000 -> all fit in 20000

-- test case 2: junior=0, senior=2
--   seniors: 15000, 30000 -> running total 15000, 45000, both fit
--   remaining budget = 5000, cheapest junior is 10000 -> none fit

-- test case 3: junior=3, senior=0
--   only senior costs 60000 -> exceeds 50000 alone, senior=0
--   remaining budget = 50000, juniors: 15000,15000,20000 -> running total
--   15000,30000,50000 -> all fit

-- test case 4: junior=2, senior=2
--   seniors sorted by (salary, id): 15000(id20), 15000(id50), 30000(id30)
--   running total: 15000, 30000, 60000 -> only first two fit
--   remaining budget = 50000 - 30000 = 20000
--   juniors: 10000, 10000 -> running total 10000, 20000 -> both fit


-- solution steps

-- Step 1:
-- Sort senior candidates by salary ascending (cheapest first) so that,
-- for a fixed budget, we maximise the number of seniors hired.
-- Tie-break on id for a deterministic order when salaries are equal.

-- Step 2:
-- Compute a running total of salary over that order and keep only the
-- rows whose running total is still <= 50000. Since salaries are
-- positive, the running total is strictly increasing, so this always
-- yields a clean prefix (never "skips" a cheaper candidate after a
-- more expensive one was rejected).

-- Step 3:
-- Count how many seniors were hired and sum their salary
-- (salary_consumed). This is the amount taken out of the 50000 budget
-- before junior hiring starts.

-- Step 4:
-- Repeat the same "cheapest-first, running total" logic for juniors,
-- but against the leftover budget (50000 - salary_consumed) instead
-- of the full 50000.

-- Step 5:
-- Cross join the two single-row summary CTEs to return junior and
-- senior counts together.


------------------------------------------------------------
-- SQL Solution
------------------------------------------------------------
with senior_cte as (
    select
        *,
        sum(salary) over (order by salary, id) as total_salary
    from candidates
    where positions = 'senior'
),
hired_senior as (
    select
        count(*) as senior,
        coalesce(sum(salary), 0) as salary_consumed
    from senior_cte
    where total_salary <= 50000
),
junior_cte as (
    select
        *,
        sum(salary) over (order by salary, id) as total_salary
    from candidates
    where positions = 'junior'
),
hired_junior as (
    select count(*) as junior
    from junior_cte
    where total_salary <= 50000 - (select salary_consumed from hired_senior)
)
select junior, senior
from hired_senior, hired_junior;
