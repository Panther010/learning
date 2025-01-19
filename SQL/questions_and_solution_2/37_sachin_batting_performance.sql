-- question statement
--Write a query to provide various milestone stats and match details like
    --when sachin completed 1000 runs
    -- when completed 5000 runs
    -- when completed 10000 runs

-- create table statement
    --Loaded data from the file "sachin_batting.csv" present in data section

-- Insert data
    --Loaded data from the file "sachin_batting.csv" present in data section

-- Input data

-- Required Output
--Write a query to provide various milestone stats and match details like
    --when sachin completed 1000 runs
    -- when completed 5000 runs
    -- when completed 10000 runs

--Solution steps
    -- create running totals of run scored
    -- save this data to temp table cte
    -- create another temp table cte2 with milestone number and run details
    -- write a query to join these 2 team tables on total_run > milestone run
    -- group by milestone_number and milestone_runs
    -- fetch min match details

--SQL solution1
select *,
sum(runs) over(order by match rows between unbounded preceding and current row) as total_run
from sachin_batting

with cte1 as (
	select
	*,
	sum(runs) over(order by match rows between unbounded preceding and current row) as total_run,
	sum(balls_faced) over(order by match) as total_balls_faced
	from sachin_batting),
cte2 as (
    select 1 as milestone_number, 1000 as milestone_runs
    union all
    select 2 as milestone_number, 5000 as milestone_runs
    union all
    select 3 as milestone_number, 10000 as milestone_runs
    union all
    select 4 as milestone_number, 15000 as milestone_runs
    union all
    select 5 as milestone_number, 20000 as milestone_runs
)

select
    milestone_number,
    milestone_runs,
    min(match),
    min(innings),
    min(total_run),
    min(total_balls_faced)
from
cte2 inner join cte1 on total_run >= milestone_runs
group by milestone_number, milestone_runs
order by milestone_number


