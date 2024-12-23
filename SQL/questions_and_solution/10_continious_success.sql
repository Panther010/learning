-- question statement
    -- Write a query to find continuous success or failure for date range

-- create table statement
create table tasks (date_value date, state varchar(10));

-- Insert data
insert into tasks  values
    ('2019-01-01','success'),
    ('2019-01-02','success'),
    ('2019-01-03','success'),
    ('2019-01-04','fail'),
    ('2019-01-05','fail'),
    ('2019-01-06','success')

-- Input data
--table 1 tasks:
"date_value","state"
2019-01-01,success
2019-01-02,success
2019-01-03,success
2019-01-04,fail
2019-01-05,fail
2019-01-06,success


-- Required Output
"start_date","end_date","state"
2019-01-01,2019-01-03,success
2019-01-04,2019-01-05,fail
2019-01-06,2019-01-06,success


--Solution steps
    --get the row_number partition by state and order by date_value
    --subtract this rank with the date_value to get common base date for all the continuous records
    --make this as temp table where we have common base_date
    --group by base_date and state and get the min() and max() value for date_value to get stat_date and end_date

--SQL solution1
with common_base_date  as (
	select date_value,
		state,
		row_number() over(partition by state order by date_value) as rn,
		(date_value - cast(row_number() over(partition by state order by date_value) as integer) ) as base_date
	from tasks)
select
	min(date_value) as start_date,
	max(date_value) as end_date,
	state
from common_base_date
group by base_date, state
order by min(date_value)

--Additional logics
