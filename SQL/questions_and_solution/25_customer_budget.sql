-- question statement
    -- Find how many products fall into customer budget along with list of products
    -- in case of clash chose less costly product

-- create table statement
create table products (product_id varchar(20) ,cost int);

create table customer_budget (customer_id int, budget int);

-- Insert data
INSERT INTO subscriber VALUES
	('2020-4-1', 'Avinash', 'Vibhor',10),
	('2020-4-1', 'Vibhor', 'Avinash',20),
	('2020-4-1', 'Avinash', 'Pawan',30),
	('2020-4-1', 'Pawan', 'Avinash',20),
	('2020-4-1', 'Vibhor', 'Pawan',5),
	('2020-4-1', 'Pawan', 'Vibhor',8),
	('2020-4-1', 'Vibhor', 'Deepak',50);

-- Input data
    --table 1 products
"product_id","cost"
P1,200
P2,300
P3,500
P4,800

    --table 2 customer_budget
"customer_id","budget"
100,400
200,800
300,1500

-- Required Output
"customer_id","budget","no_of_products","list_of_products"
100,400,1,P1
200,800,2,"P1,P2"
300,1500,3,"P1,P2,P3"


--Solution steps
    -- calculate the running total of the cost and create temp table
    -- left join budget and tem table on budget > running_cost
    -- to get all the product falling in budget
    -- group by customer id and budget
    -- get the count of the product
    -- for list of the product string aggregate product_id

--SQL solution 1
with cte as(
	select
	    *,
	    sum(cost) over(order by cost) as running_cost
	from products p )
select
	customer_id,
	budget,
	count(1) as no_of_products,
	string_agg(product_id, ',') as list_of_products

from customer_budget left join cte on
    budget > running_cost
group by customer_id, budget
order by customer_id

--SQL solution 2
with cte as(
	select *,
	    sum(cost) over(order by cost) as running_cost,
	    string_agg(product_id, ',') over(order by cost) as list_of_products
	from products p )

select
	customer_id,
	budget,
	count(1) as no_of_products,
	max(list_of_products) as list_of_products
from customer_budget left join cte on
    budget > running_cost
group by customer_id, budget
order by customer_id