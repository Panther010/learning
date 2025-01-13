-- question statement
    -- Find largest order by each salesperson and display order details
    -- get result without using cte window function or temp table


-- create table statement
CREATE TABLE int_orders(
 order_number int NOT NULL,
 order_date date NOT NULL,
 cust_id int NOT NULL,
 salesperson_id int NOT NULL,
 amount float NOT NULL
);


-- Insert data
INSERT INTO int_orders VALUES
(30, CAST('1995-07-14' AS Date), 9, 1, 460),
(10, CAST('1996-08-02' AS Date), 4, 2, 540),
(40, CAST('1998-01-29' AS Date), 7, 2, 2400),
(50, CAST('1998-02-03' AS Date), 6, 7, 600),
(60, CAST('1998-03-02' AS Date), 6, 7, 720),
(70, CAST('1998-05-06' AS Date), 9, 7, 150),
(20, CAST('1999-01-30' AS Date), 4, 8, 1800);


-- Input data
"order_number","order_date","cust_id","salesperson_id","amount"
30,1995-07-14,9,1,460.0
10,1996-08-02,4,2,540.0
40,1998-01-29,7,2,2400.0
50,1998-02-03,6,7,600.0
60,1998-03-02,6,7,720.0
70,1998-05-06,9,7,150.0
20,1999-01-30,4,8,1800.0


-- Required Output
"order_number","order_date","cust_id","salesperson_id","amount"
20,1999-01-30,4,8,1800.0
30,1995-07-14,9,1,460.0
40,1998-01-29,7,2,2400.0
60,1998-03-02,6,7,720.0


--Solution steps
-- 1. left join to create all possible combination
-- 2. having clause to filter unwanted record a.amount >= max(b.amount)
-- 3. group by all the columns from first table to support having clause

--SQL solution1
select a.*
from int_orders a left join int_orders b on
a.salesperson_id = b.salesperson_id
group by a.order_number, a.order_date, a.cust_id, a.salesperson_id, a.amount
having a.amount >= max(b.amount)
order by a.order_number


--SQL solution2
with max_sale_by_seller as (
	select salesperson_id, max(amount) as amount from int_orders
	group by salesperson_id)

select a.* from int_orders a inner join
select salesperson_id, max(amount) as amount from int_orders
	group by salesperson_id
	max_sale_by_seller b on a.salesperson_id = b.salesperson_id and a.amount = b.amount
order by order_number