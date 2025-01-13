-- question statement
    -- write a query to calculate products bought together and their frequency

-- create table statement
create table orders (order_id int, customer_id int, product_id int);

create table products (id int, name varchar(10));

-- Insert data
insert into orders VALUES
    (1, 1, 1),
    (1, 1, 2),
    (1, 1, 3),
    (2, 2, 1),
    (2, 2, 2),
    (2, 2, 4),
    (3, 1, 5);

insert into products VALUES
    (1, 'A'),
    (2, 'B'),
    (3, 'C'),
    (4, 'D'),
    (5, 'E');
-- Input data
--table 1 orders:
"order_id","customer_id","product_id"
1,1,1
1,1,2
1,1,3
2,2,1
2,2,2
2,2,4
3,1,5

--table 2 orders:
"id","name"
1,A
2,B
3,C
4,D
5,E

-- Required Output
"pair","purchase_freq"
A B,2
A C,1
A D,1
B C,1
B D,1


--Solution steps
    --Self join the orders table to get all the possible pair sold
    --To remove duplicate and same to product apply filter a.product_id < b.product_id
    --join the results with product table to get the product name save this in temp table
    --group by name1 and name2 get the frequency of products bought together
    -- concat the names to get the pair column

--SQL solution1
with product_pair as (
	select c.name as name_1, d.name as name_2
	from orders a join orders b
		on a.order_id = b.order_id and a.product_id < b.product_id
	join products c on a.product_id = c.id
	join products d on b.product_id = d.id)

select concat(name_1, ' ', name_2) as pair,
count(1) as purchase_freq from product_pair
group by name_1, name_2

--Additional logics Recursive CTE sample
