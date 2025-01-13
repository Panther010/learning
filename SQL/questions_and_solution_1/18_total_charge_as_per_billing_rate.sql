-- question statement
    -- write a sql to find total amount earned by user using billing rate and total hours worked

-- create table statement
create table billings(emp_name varchar(10), bill_date date, bill_rate int);

create table hours_worked  (emp_name varchar(20), work_date date, bill_hrs int);



-- Insert data
insert into billings values
    ('Sachin','01-JAN-1990',25)
    ,('Sehwag' ,'01-JAN-1989', 15)
    ,('Dhoni' ,'01-JAN-1989', 20)
    ,('Sachin' ,'05-Feb-1991', 30);

insert into HoursWorked values
('Sachin', '01-JUL-1990' ,3)
,('Sachin', '01-AUG-1990', 5)
,('Sehwag','01-JUL-1990', 2)
,('Sachin','01-JUL-1991', 4)

-- Input data
--table 1 billings:
"emp_name","bill_date","bill_rate"
Sachin,1990-01-01,25
Sehwag,1989-01-01,15
Dhoni,1989-01-01,20
Sachin,1991-02-05,30

--table 2 HoursWorked:
"emp_name","work_date","bill_hrs"
Sachin,1990-07-01,3
Sachin,1990-08-01,5
Sehwag,1990-07-01,2
Sachin,1991-07-01,4

-- Required Output
"emp_name","paise_mila"
Sachin,320
Sehwag,30


--Solution steps
    --calculate start and end_date for the billing rate in billings table
    -- join billings and HoursWorked table to calculate money eared by user hours worked * billing rate at that time
    -- join should be on user and date rate
    -- calculate the sum of money earned

--SQL solution1
with billing_start_end as (
    select
        *,
        coalesce ((lead(bill_date) over(partition by emp_name order by bill_date) - 1), '9999-12-31') as bill_date_end
    from billings)
select
    a.emp_name,
    sum(bill_hrs * bill_rate) as money_earned
from hoursworked a
    join billing_start_end b
        on a.emp_name = b.emp_name and
        a.work_date between bill_date and bill_date_end
group by a.emp_name

--Additional logics Recursive CTE sample
