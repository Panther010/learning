-- question statement
    -- Return the city/cities where not a single order has ever been
    -- returned (i.e. zero rows in namaste_returns for any of that
    -- city's orders).


-- create table statement
create table namaste_orders (
    order_id  int,
    city      varchar(10),
    sales     int
);

create table namaste_returns (
    order_id       int,
    return_reason  varchar(20)
);


-- insert data
insert into namaste_orders values
(1,'Mysore',100), (2,'Mysore',200),
(3,'Bangalore',250), (4,'Bangalore',150),
(5,'Mumbai',300), (6,'Mumbai',500), (7,'Mumbai',800);

insert into namaste_returns values
(3,'wrong item'), (6,'bad quality'), (7,'wrong item');


-- input data
"order_id","city","sales"
1,Mysore,100
2,Mysore,200
3,Bangalore,250
4,Bangalore,150
5,Mumbai,300
6,Mumbai,500
7,Mumbai,800

"order_id","return_reason"
3,wrong item
6,bad quality
7,wrong item


-- required output (verified: executed against sqlite3)
"city"
Mysore


-- solution steps

-- Step 1:
-- Left join orders to returns on order_id, so every order keeps a
-- row even if it was never returned (return columns come back NULL).

-- Step 2:
-- Group by city and count(b.order_id) -- NOT count(*). count() on a
-- specific column ignores NULLs, so this counts only orders that
-- actually matched a return row. count(*) would count every joined
-- row regardless of match and always be >= number of orders, which
-- would break the "= 0" filter entirely.

-- Step 3:
-- HAVING count(b.order_id) = 0 keeps only cities where none of the
-- orders had a matching return.


-- sql solution (your original -- verified correct)
select
    a.city,
    count(b.order_id) as returned_count
from namaste_orders a
left join namaste_returns b
    on a.order_id = b.order_id
group by a.city
having count(b.order_id) = 0;


-- alternative solution (anti-join style, no join fan-out/grouping needed)
select distinct o.city
from namaste_orders o
where not exists (
    select 1
    from namaste_orders o2
    join namaste_returns r
        on o2.order_id = r.order_id
    where o2.city = o.city
);
