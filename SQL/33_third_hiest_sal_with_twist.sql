-- question statement
    -- Calculate the third highest salary of from each department
    -- in cse total emp cunt is less than 3 return the lowest salary getting emp

-- create table statement
CREATE TABLE emp(
emp_id int NULL,  emp_name varchar(50) NULL,
salary int NULL, manager_id int NULL,
emp_age int NULL, dep_id int NULL,
dep_name varchar(20) NULL, gender varchar(10) NULL) ;

-- Insert data
insert into emp values
(1,'Ankit',14300,4,39,100,'Analytics','Female'),
(2,'Mohit',14000,5,48,200,'IT','Male'),
(3,'Vikas',12100,4,37,100,'Analytics','Female'),
(4,'Rohit',7260,2,16,100,'Analytics','Female'),
(5,'Mudit',15000,6,55,200,'IT','Male'),
(6,'Agam',15600,2,14,200,'IT','Male'),
(7,'Sanjay',12000,2,13,200,'IT','Male'),
(8,'Ashish',7200,2,12,200,'IT','Male'),
(9,'Mukesh',7000,6,51,300,'HR','Male'),
(10,'Rakesh',8000,6,50,300,'HR','Male'),
(11,'Akhil',4000,1,31,500,'Ops','Male');

-- Input data
"emp_id","emp_name","salary","manager_id","emp_age","dep_id","dep_name","gender"
1,Ankit,14300,4,39,100,Analytics,Female
2,Mohit,14000,5,48,200,IT,Male
3,Vikas,12100,4,37,100,Analytics,Female
4,Rohit,7260,2,16,100,Analytics,Female
5,Mudit,15000,6,55,200,IT,Male
6,Agam,15600,2,14,200,IT,Male
7,Sanjay,12000,2,13,200,IT,Male
8,Ashish,7200,2,12,200,IT,Male
9,Mukesh,7000,6,51,300,HR,Male
10,Rakesh,8000,6,50,300,HR,Male
11,Akhil,4000,1,31,500,Ops,Male

-- Required Output
"emp_id","emp_name","salary","dep_id","dep_name"
4,Rohit,7260,100,Analytics
2,Mohit,14000,200,IT
9,Mukesh,7000,300,HR
11,Akhil,4000,500,Ops


--Solution steps
-- 1. Calculate the ranking of the emp from each department highest to lowest
-- 2. Get the total count of the emp in each department
-- 3. Save the data to the temp table
-- 4. Apply filter on rank 3 to get third highest salaried emp
-- 5. Apply another filter where count is = rank of the emp and total count is less than 3
-- 6. This will allow to pass lowest salaried emp from the department where emp count is less than 3

--SQL solution1
with cte as (
	select
		*,
		rank() over(partition by dep_id order by salary desc) sal_rank,
		count(emp_id) over(partition by dep_id) emp_count

	from emp)

select
	emp_id,
	emp_name,
	salary,
	dep_id,
	dep_name
from cte
where sal_rank = 3 or (emp_count < 3 and sal_rank = emp_count)