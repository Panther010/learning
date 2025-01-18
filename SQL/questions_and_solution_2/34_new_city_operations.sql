-- question statement
    -- Identify year wise count oof new cities where company performed operations

-- create table statement
create table business_city (business_date date, city_id int);

-- Insert data
insert into business_city values
(cast('2020-01-02' as date),3),
(cast('2020-07-01' as date),7),
(cast('2021-01-01' as date),3),
(cast('2021-02-03' as date),19),
(cast('2022-12-01' as date),3),
(cast('2022-12-15' as date),3),
(cast('2022-02-28' as date),12);

-- Input data
"business_date","city_id"
2020-01-02,3
2020-07-01,7
2021-01-01,3
2021-02-03,19
2022-12-01,3
2022-12-15,3
2022-02-28,12

-- Required Output
"ops_year","count"
2020.0,2
2021.0,1
2022.0,1

--Solution steps
-- 1. Get year from the date column
-- 2. add rank column partition by city_id and order by business date
-- 3. filter the data where rank is one to ge new cities only
-- 4. group by year count city to get the results

--SQL solution1 using Rank()
with cte as (
	select
		date_part('year', business_date) ops_year,
		city_id,
		rank() over(partition by city_id order by business_date) as rn
	from business_city)
select
ops_year, count(city_id)
from cte
where rn = 1
group by ops_year

--SQL solution1 using Self join
with cte as (
	select
		date_part('year', a.business_date) as a_year,
		a.city_id as a_city_id,
		date_part('year', b.business_date) as b_year,
		b.city_id as b_city_id

	from business_city a
	left join business_city b on
		a.city_id = b.city_id and
		date_part('year', a.business_date) > date_part('year', b.business_date))
select
	a_year,
	count(a_city_id) as new_city_count
from cte
where b_year is null
group by a_year