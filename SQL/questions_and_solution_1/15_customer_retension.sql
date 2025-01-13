-- question statement
    -- write a query to calculate conversation rate or the users who
        -- join prime member with in 30 days of joining
        -- and are music users

-- create table statement
create table transactions(order_id int, cust_id int, order_date date, amount int );

-- Insert data
insert into transactions values
    (1,1,'2020-01-15',150)
    ,(2,1,'2020-02-10',150)
    ,(3,2,'2020-01-16',150)
    ,(4,2,'2020-02-25',150)
    ,(5,3,'2020-01-10',150)
    ,(6,3,'2020-02-20',150)
    ,(7,4,'2020-01-20',150)
    ,(8,5,'2020-02-20',150);

-- Input data
--table 1 transactions:
"order_id","cust_id","order_date","amount"
1,1,2020-01-15,150
2,1,2020-02-10,150
3,2,2020-01-16,150
4,2,2020-02-25,150
5,3,2020-01-10,150
6,3,2020-02-20,150
7,4,2020-01-20,150
8,5,2020-02-20,150


-- Required Output
"month_part","retention"
1.0,0
2.0,3

--Solution steps
    --using lag unction calculate the previous order date
    --calculate the month part from order date
    --get difference between month part or current date and previous order date
    --get the sum of orders for each month get repeated customers

--SQL solution1
with repeat_sale as (
	select extract(month from order_date) month_part,
	extract(month from (order_date)) - extract(month from lag(order_date) over(partition by cust_id order by order_date)) as diff_month
from transactions)

select month_part, sum(case when diff_month in (1) then 1 else 0 end) as retention
from repeat_sale
group by month_part

--Additional logics Recursive CTE sample
