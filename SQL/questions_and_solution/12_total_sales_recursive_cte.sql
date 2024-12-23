-- question statement
    -- write a query to calculate total sales for each year from given average salaries for time period

-- create table statement
create table sales (product_id int, period_start date, period_end date, average_daily_sales int);

-- Insert data
insert into sales values
    (1,'2019-01-25','2019-02-28',100),
    (2,'2018-12-01','2020-01-01',10),
    (3,'2019-12-01','2020-01-31',1);

-- Input data
--table 1 sales:
"product_id","period_start","period_end","average_daily_sales"
1,2019-01-25,2019-02-28,100
2,2018-12-01,2020-01-01,10
3,2019-12-01,2020-01-31,1

-- Required Output
"product_id","year","total_sales"
1,"2019",3500
2,"2018",310
2,"2019",3650
2,"2020",10
3,"2019",31
3,"2020",31

--Solution steps
    --using recursive CTE create all the possible date from min date to max date from table
    --join this date data with sales table to get daily sales from avg sales
    --join wil be on date and between condition
    --calculate the total sales using group by and sum

--SQL solution1
with RECURSIVE cte_dates as (
	select
		min(period_start) as start_date,
		max(period_end) as end_date from sales
	union all
	select
		start_date + 1,
		end_date f
	from cte_dates
	where start_date < end_date),
daily_sales as (
	select
		product_id,
		cast(date_part('year', start_date) as text) as year,
		average_daily_sales as daily_sales,
		period_start,
		period_end
	from sales inner join cte_dates
	on start_date between period_start and period_end)
select
	product_id,
	year,
	sum(daily_sales) as total_sales
from daily_sales
group by product_id, year
order by product_id

--Additional logics Recursive CTE sample
with RECURSIVE cte_num as(
	select 1 as num
	union all
	select num + 1 from cte_num
	where num < 115)

select * from cte_num