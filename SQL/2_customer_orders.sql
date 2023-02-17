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

--SQL solution1
select order_date, sum(new_old_flag) as new_vistiors, (count(1) - sum(new_old_flag)) as repeated_visitors
from (
select order_date, coming_date, 
case when coming_date = 1 then 1 else 0 end as new_old_flag from (
select customer_id, order_date,
rank() over(partition by customer_id order by order_date) as coming_date from customer_orders) a) b
group by order_date
order by order_date