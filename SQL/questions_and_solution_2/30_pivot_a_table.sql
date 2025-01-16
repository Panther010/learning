-- question statement
    -- From given table create data for city as columns and players as row for the cities

-- create table statement
create table players_location (name varchar(20), city varchar(20));

-- Insert data
insert into players_location values
('Sachin','Mumbai'),
('Virat','Delhi') ,
('Rahul','Bangalore'),
('Rohit','Mumbai'),
('Mayank','Bangalore');



-- Input data
"name","city"
Sachin,Mumbai
Virat,Delhi
Rahul,Bangalore
Rohit,Mumbai
Mayank,Bangalore

-- Required Output
"bangalore","mumbai","delhi"
Rahul,Sachin,[NULL]
Mayank,Rohit,Virat

--Solution steps
-- 1. get the row_number of players partition by the city and order by name
-- 2. Save as temp table
-- 3. write case statement for each city
-- 4. Apply max or min function to get the specific result
-- 5. Group by row_number

--SQL solution1
with cte as (
	select
		*,
		row_number() over(partition by city order by name) as rn
	from players_location)
select
max(case when city = 'Bangalore' then name else null end) as bangalore,
max(case when city = 'Mumbai' then name else null end) as mumbai,
max(case when city = 'Delhi' then name else null end) as delhi
from cte
group by rn

--SQL solution2
with cte as (
    select
        name,
        city,
        row_number() over (partition by city order by name) as rn
    from players_location
)
select
    coalesce(max(case when city = 'Bangalore' then name end), null) as bangalore,
    coalesce(max(case when city = 'Mumbai' then name end), null) as mumbai,
    coalesce(max(case when city = 'Delhi' then name end), null) as delhi
from cte
group by rn
order by rn;