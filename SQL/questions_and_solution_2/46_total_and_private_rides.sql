-- question statement
    -- write a query to print total rides and profit rides for each driver
    -- profit ride is when the end location of current ride is same as start location on next ride

-- create table statement update
create table drivers(id varchar(10), start_time time, end_time time, start_loc varchar(10), end_loc varchar(10));

-- Insert data
insert into drivers values
('dri_1', '09:00', '09:30', 'a','b'),
('dri_1', '09:30', '10:30', 'b','c'),
('dri_1', '11:00', '11:30', 'd','e'),
('dri_1', '12:00', '12:30', 'f','g'),
('dri_1', '13:30', '14:30', 'c','h'),
('dri_2', '12:15', '12:30', 'f','g'),
('dri_2', '13:30', '14:30', 'c','h');

-- Input data
"id","start_time","end_time","start_loc","end_loc"
dri_1,09:00:00,09:30:00,a,b
dri_1,09:30:00,10:30:00,b,c
dri_1,11:00:00,11:30:00,d,e
dri_1,12:00:00,12:30:00,f,g
dri_1,13:30:00,14:30:00,c,h
dri_2,12:15:00,12:30:00,f,g
dri_2,13:30:00,14:30:00,c,h

-- Required Output
"id","total_rides","profit_rides"
dri_1,5,1
dri_2,2,0

--Solution steps
-- 1. using lead calculate the next start location for each ride
-- 2. Save table as CTE and in next step
-- 3. calculate total ride and conditional sum of rides where current end location is same as next start location


--SQL solution1
with drive_cte as (
	select
		*,
		lead(start_loc) over(partition by id order by start_time) as next_start_loc
	from drivers)
select
	id,
	count(start_loc) as total_rides,
	sum(case when end_loc = next_start_loc then 1 else 0 end) as profit_rides
from drive_cte
group by id