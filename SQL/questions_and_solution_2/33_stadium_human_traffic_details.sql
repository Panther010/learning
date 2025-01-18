-- question statement
    -- Display records which have 3 or more consecutive rows
    -- with the amount of people more than 100 each day

-- create table statement
create table stadium (id int, visit_date date, no_of_people int);

-- Insert data
insert into stadium values
 (1,'2017-07-01',10)
,(2,'2017-07-02',109)
,(3,'2017-07-03',150)
,(4,'2017-07-04',99)
,(5,'2017-07-05',145)
,(6,'2017-07-06',1455)
,(7,'2017-07-07',199)
,(8,'2017-07-08',188);

-- Input data
"id","visit_date","no_of_people"
1,2017-07-01,10
2,2017-07-02,109
3,2017-07-03,150
4,2017-07-04,99
5,2017-07-05,145
6,2017-07-06,1455
7,2017-07-07,199
8,2017-07-08,188

-- Required Output
"id","visit_date","no_of_people"
5,2017-07-05,145
6,2017-07-06,1455
7,2017-07-07,199
8,2017-07-08,188

--Solution steps
-- 1. Filter the records having more than 100 people
-- 2. row number on these record and subtract from id to get common group of consecutive days
-- 3. save the result in temp table using cte
-- 4. get running count partition by previously added group to get how many consecutive days are there like that
-- 5.save results in tem table
-- 6. apply filter on the recently added count column to get consecutive 3 or more rows

--SQL solution1
with cte as (
	select
		*,
		id - row_number() over(order by visit_date) as rn
	from stadium s
	where no_of_people >= 100),
day_count as (
	select
		*,
		count(id) over(partition by rn) as consecutive_count
	from cte)
select
	id,
	visit_date,
	no_of_people
from day_count
where consecutive_count >= 3