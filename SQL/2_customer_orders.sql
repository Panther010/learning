-- create table statement
create table customer_orders (
order_id integer,
customer_id integer,
order_date date,
order_amount integer
);

-- Insert data
insert into customer_orders values
(1,100,cast('2022-01-01' as date),2000),
(2,200,cast('2022-01-01' as date),2500),
(3,300,cast('2022-01-01' as date),2100),
(4,100,cast('2022-01-02' as date),2000),
(5,400,cast('2022-01-02' as date),2200),
(6,500,cast('2022-01-02' as date),2700),
(7,100,cast('2022-01-03' as date),3000),
(8,400,cast('2022-01-03' as date),1000),
(9,600,cast('2022-01-03' as date),3000);

-- Input data
select * from customer_orders
"order_id","customer_id","order_date","order_amount"
1,100,2022-01-01,2000
2,200,2022-01-01,2500
3,300,2022-01-01,2100
4,100,2022-01-02,2000
5,400,2022-01-02,2200
6,500,2022-01-02,2700
7,100,2022-01-03,3000
8,400,2022-01-03,1000
9,600,2022-01-03,3000

-- Required Output
-- get the new and repeated customers daily from customer_orders table
"order_date","new_vistiors","repeated_visitors"
2022-01-01,3,0
2022-01-02,2,1
2022-01-03,1,2

--Solution steps
-- check if the customer is visting the first time or not by using rank function partition by ID and order by date
-- case statement to make it flag in case first visit make it 1 else 0
-- get customer ID, order date and first visit flag by above queries
-- group by date and add the first visit flag to get date wise 1st visit and total minus first visit will be the repeated customers

--SQL solution1
select order_date, sum(new_old_flag) as new_vistiors, (count(1) - sum(new_old_flag)) as repeated_visitors
from (
select order_date, coming_date, 
case when coming_date = 1 then 1 else 0 end as new_old_flag from (
select customer_id, order_date,
rank() over(partition by customer_id order by order_date) as coming_date from customer_orders) a) b
group by order_date
order by order_date

--SQL solution2
select order_date, sum(new_old_flag) as new_vistiors, (count(1) - sum(new_old_flag)) as repeated_visitors
from (
select customer_id, order_date,
case when rank() over(partition by customer_id order by order_date) = 1 then 1 else 0 end as new_old_flag from customer_orders) b
group by order_date
order by order_date

--SQL solution3
with first_visit as (
select customer_id, min(order_date) as min_order_date from customer_orders group by customer_id),
visit_flag as 
(select order_id, a.customer_id, order_date, order_amount, min_order_date,
case when order_date = min_order_date then 1 else 0 end as first_visit_flag
from customer_orders a
inner join first_visit b on a.customer_id = b.customer_id)
select order_date, sum(first_visit_flag) as new_vistiors, (count(1) - sum(first_visit_flag)) as repeated_visitors
from visit_flag
group by order_date

-- Additional check to get order amount by repeated and new customers
with first_visit_order as (
select order_date, order_amount,
case when rank() over(partition by customer_id order by order_date) = 1 then 1 else 0 end as fisrt_visit_flag,
case when rank() over(partition by customer_id order by order_date) = 1 then 0 else 1 end as repeated_visit_flag
from customer_orders)

select order_date, 
sum(fisrt_visit_flag) as new_vistiors,
sum(repeated_visit_flag) as repeated_visitors,
sum(case when fisrt_visit_flag = 1 then order_amount else 0 end) as new_vistiors_order,
sum(case when repeated_visit_flag = 1 then order_amount else 0 end) as repeated_vistiors_order
from first_visit_order
group by order_date
order by order_date