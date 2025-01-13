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
"order_month","count"
1.0,1
2.0,4

--Solution steps
    --using lead function calculate the next order date
    --calculate the month part from order date
    --get difference between month part or current date and next order date
    --get the sum of orders for each month get repeated customers

--SQL solution1
with previous_sale as (
    select *,
        extract(month from order_date) as order_month,
        lead(order_date) over(partition by cust_id order by order_date) as last_order
    from transactions)
select order_month, count(cust_id) from previous_sale where last_order is null
group by order_month

--Additional logics Recursive CTE sample
