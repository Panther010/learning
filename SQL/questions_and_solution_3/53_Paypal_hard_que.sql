-- Question Statement
-- List departments whose average salary is lower than the company's average salary,
-- where the company average is calculated excluding the department being compared.

------------------------------------------------------------
-- Create Table Statement
------------------------------------------------------------

create table emp_new(
    emp_id int,
    emp_name varchar(20),
    department_id int,
    salary int,
    manager_id int,
    emp_age int
);

------------------------------------------------------------
-- Insert Data
------------------------------------------------------------

insert into emp_new values (1, 'Ankit', 100, 10000, 4, 39);
insert into emp_new values (2, 'Mohit', 100, 15000, 5, 48);
insert into emp_new values (3, 'Vikas', 100, 10000, 4, 37);
insert into emp_new values (4, 'Rohit', 100, 5000, 2, 16);

insert into emp_new values (5, 'Mudit', 200, 12000, 6, 55);
insert into emp_new values (6, 'Agam', 200, 12000, 2, 14);
insert into emp_new values (7, 'Sanjay', 200, 9000, 2, 13);
insert into emp_new values (8, 'Ashish', 200, 5000, 2, 12);

insert into emp_new values (9, 'Mukesh', 300, 6000, 6, 51);
insert into emp_new values (10, 'Rakesh', 300, 7000, 6, 50);

------------------------------------------------------------
-- Input Data
------------------------------------------------------------

emp_id | emp_name | department_id | salary | manager_id | emp_age
-------|----------|---------------|--------|------------|--------
1      | Ankit    | 100           | 10000  | 4          | 39
2      | Mohit    | 100           | 15000  | 5          | 48
3      | Vikas    | 100           | 10000  | 4          | 37
4      | Rohit    | 100           | 5000   | 2          | 16
5      | Mudit    | 200           | 12000  | 6          | 55
6      | Agam     | 200           | 12000  | 2          | 14
7      | Sanjay   | 200           | 9000   | 2          | 13
8      | Ashish   | 200           | 5000   | 2          | 12
9      | Mukesh   | 300           | 6000   | 6          | 51
10     | Rakesh   | 300           | 7000   | 6          | 50

------------------------------------------------------------
-- Required Output
------------------------------------------------------------

department_id | avg_salary | rest_avg
--------------|------------|---------
300           | 6500.00    | 9750.00

------------------------------------------------------------
-- Solution Steps
------------------------------------------------------------

-- Step 1:
-- Calculate department-wise average salary,
-- employee count, and total salary.

-- Step 2:
-- Join each department with all other departments
-- to calculate salary and employee counts excluding
-- the current department.

-- Step 3:
-- Calculate average salary of the remaining departments.

-- Step 4:
-- Compare department average salary with the average
-- salary of the rest of the company.

------------------------------------------------------------
-- SQL Solution
------------------------------------------------------------

with cte as (
    select
        department_id,
        avg(salary) as avg_salary,
        count(emp_id) as emp_count,
        sum(salary) as total_salary
    from emp_new
    group by department_id
),

rest_department as (
    select
        a.department_id,
        a.avg_salary,
        b.total_salary as rest_salary,
        b.emp_count as rest_count
    from cte a
    inner join cte b
        on a.department_id <> b.department_id
),

rest_dep_avg as (
    select
        department_id,
        avg_salary,
        sum(rest_salary) * 1.0 / sum(rest_count) as rest_avg
    from rest_department
    group by
        department_id,
        avg_salary
)

select *
from rest_dep_avg
where avg_salary < rest_avg;

------------------------------------------------------------
-- Alternative Optimized Solution
------------------------------------------------------------

with dept_salary as (
    select
        department_id,
        avg(salary) as dept_avg_salary,
        sum(salary) as dept_total_salary,
        count(*) as dept_emp_count
    from emp_new
    group by department_id
),
company_stats as (
    select
        sum(salary) as company_total_salary,
        count(*) as company_emp_count
    from emp_new
)

select
    d.department_id,
    d.dept_avg_salary,
    (c.company_total_salary - d.dept_total_salary) * 1.0 /
    (c.company_emp_count - d.dept_emp_count) as rest_avg_salary
from dept_salary d
cross join company_stats c
where d.dept_avg_salary <
      (c.company_total_salary - d.dept_total_salary) * 1.0 /
      (c.company_emp_count - d.dept_emp_count);

------------------------------------------------------------
-- Notes
------------------------------------------------------------

-- Approach 1:
-- Self-join departments with all other departments.
-- Easy to understand but less efficient for many departments.

-- Approach 2:
-- Uses overall company totals and subtracts the current
-- department's totals.
-- More scalable and typically preferred in interviews
-- and production environments.

-- Time Complexity:
-- Approach 1: O(N²) on number of departments
-- Approach 2: O(N)
