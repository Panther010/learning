-- create table statement
create table entries ( 
name varchar(20),
address varchar(20),
email varchar(20),
floor int,
resources varchar(10));

-- Insert data
INSERT INTO entries ("name",address,email,floor,resources) VALUES
	 ('A','Bangalore','A@gmail.com',1,'CPU'),
	 ('A','Bangalore','A1@gmail.com',1,'CPU'),
	 ('A','Bangalore','A2@gmail.com',2,'DESKTOP'),
	 ('B','Bangalore','B@gmail.com',2,'DESKTOP'),
	 ('B','Bangalore','B1@gmail.com',2,'DESKTOP'),
	 ('B','Bangalore','B2@gmail.com',1,'MONITOR');

-- Input data
"name","address","email","floor","resources"
A,Bangalore,A@gmail.com,1,CPU
A,Bangalore,A1@gmail.com,1,CPU
A,Bangalore,A2@gmail.com,2,DESKTOP
B,Bangalore,B@gmail.com,2,DESKTOP
B,Bangalore,B1@gmail.com,2,DESKTOP
B,Bangalore,B2@gmail.com,1,MONITOR

-- Required Output
name, total_visit, most_visited_floor, resources_used
'A',1,3,"'CPU','DESKTOP'"
'B',2,3,"'DESKTOP', 'MONITOR'"

--Solution steps
-- Calculate total visit for each name
-- Calculate distinct resources used by each name
-- Calculate most visited floor by each name
	-- for this run rank partition by name order by count of floor visit
--Join these results

--SQL solution1 (multiple joins and sub queries)
select a.name, a.floor, b.most_visit, b.no_res
from (
	select e.name, e.floor, count(1), 
rank() over(partition by e.name order by count(1) desc ) as rn from entries e group by name, floor) a
inner join (
	select e2.name, count(1) as most_visit, string_agg(distinct resources, ',') as no_res  from entries e2 group by name) b
	on a.name = b.name
	where rn = 1
	
--SQL solution2
with
	total_visits as (select name, count(1) as total_visit from entries group by name),
	distinct_resources as (select distinct name, resources from entries),
	res_used as (select name, string_agg(resources, ',') as resources_used from distinct_resources group by name),
	most_visit as (select name, floor, count(1),
		rank() over(partition by name order by count(1)) as rn from entries e group by name, floor)

select total_visits.name, total_visit, most_visit.floor as most_visited_floor, resources_used
from total_visits inner join res_used on total_visits.name = res_used.name 
inner join most_visit on total_visits.name = most_visit.name
where rn = 1

