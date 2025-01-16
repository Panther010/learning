-- question statement
    -- Calculate the median salary of a company

-- create table statement
create table employee
(
emp_id int,
company varchar(10),
salary int
);

-- Insert data
insert into employee values
(1,'A',2341),
(2,'A',341),
(3,'A',15),
(4,'A',15314),
(5,'A',451),
(6,'A',513),
(7,'B',15),
(8,'B',13),
(9,'B',1154),
(10,'B',1345),
(11,'B',1221),
(12,'B',234),
(13,'C',2345),
(14,'C',2645),
(15,'C',2645),
(16,'C',2652),
(17,'C',65);

-- Input data
"emp_id","company","salary"
1,A,2341
2,A,341
3,A,15
4,A,15314
5,A,451
6,A,513
7,B,15
8,B,13
9,B,1154
10,B,1345
11,B,1221
12,B,234
13,C,2345
14,C,2645
15,C,2645
16,C,2652
17,C,65

-- Required Output
"company","avg"
A,482.0000000000000000
B,694.0000000000000000
C,2645.0000000000000000

--Solution steps
-- 1. get the row_number of emp or each company order by salary
-- 2. get the total count of the emp from a company
-- 3. Save this data as temp table
-- 4. get the avg of the records which are having rank between count/2 or count/2 + 1

--SQL solution1
with cte as (
	select
		*,
		row_number() over(partition by company order by salary) as rn,
		(count(emp_id) over(partition by company)) * 1.0 /2 as cnt1,
		(count(emp_id) over(partition by company))* 1.0 /2 + 1 as cnt2
	from employee)
select company, avg(salary)
from cte
where rn between cnt1 and cnt2
group by company

--SQL solution2
with cte as (
	select
		*,
		row_number() over(partition by company order by salary) as rn,
		count(emp_id) over(partition by company) as cnt
	from employee)
select company, avg(salary)
from cte
where rn between (cnt * 1.0)/2 and ((cnt * 1.0)/2 + 1)
group by company