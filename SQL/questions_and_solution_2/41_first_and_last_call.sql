-- question statement
    -- A company wants to hire new employees. Th budget of the company for salaries is $70000. The company's criteria for hire are:
        -- Keep hiring the senior with smallest salary until you can not hire any more senior.
        -- Use the remaining budget to hire the junior with smallest salary.

-- create table statement update
create table candidates (emp_id int, experience varchar(20), salary int);

-- Insert data
insert into candidates values
    (1,'Junior',10000),(2,'Junior',15000),(3,'Junior',40000),
    (4,'Senior',16000),(5,'Senior',20000),(6,'Senior',50000);

-- Input data
"emp_id","experience","salary"
1,Junior,10000
2,Junior,15000
3,Junior,40000
4,Senior,16000
5,Senior,20000
6,Senior,50000

-- Required Output
"emp_id","experience","salary","salary_total"
1,Junior,10000,10000
2,Junior,15000,25000
4,Senior,16000,16000
5,Senior,20000,36000

--Solution steps
-- 1. Calculate the running salary sum for candidates partition by experience and order by emp_id
-- 2. get the senior emp till the running sum is less than or equal to 70000
-- 3. rest is junior till the running salary is less than or equal to 70000 - sum of senior salary


--SQL solution1
with total_salary as (
    select *,
        sum(salary) over(partition by experience order by emp_id) as salary_total
    from candidates),
senior_emp as
	(select *
	from total_salary
	where experience = 'Senior' and
	salary_total <= 70000)
select *
from total_salary
where experience = 'Junior' and
    salary_total <= 70000 - (select sum(salary) from senior_emp)
union all
select * from senior_emp