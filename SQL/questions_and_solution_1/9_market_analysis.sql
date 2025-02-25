-- question statement
    -- Write a query to find each seller, whether the brand of the second item (by date) they sold is their
    -- favorite brand

    --if seller is selling less than two items, report the answer for seller as no. o/p


-- create table statement
create table market_users (user_id int, join_date date, favorite_brand varchar(50));

create table orders (order_id int, order_date date, item_id int, buyer_id int, seller_id int);

create table items (item_id int, item_brand varchar(50));

-- Insert data
 insert into market_users
 values
    (1,'2019-01-01','Lenovo'),
    (2,'2019-02-09','Samsung'),
    (3,'2019-01-19','LG'),
    (4,'2019-05-21','HP');

 insert into items
 values
    (1,'Samsung'),
    (2,'Lenovo'),
    (3,'LG'),
    (4,'HP');

 insert into orders
 values
    (1,'2019-08-01',4,1,2),
    (2,'2019-08-02',2,1,3),
    (3,'2019-08-03',3,2,3),
    (4,'2019-08-04',1,4,2),
    (5,'2019-08-04',1,3,4),
    (6,'2019-08-05',2,2,4);

-- Input data
--table 1 market_users:
"user_id","join_date","favorite_brand"
1,2019-01-01,Lenovo
2,2019-02-09,Samsung
3,2019-01-19,LG
4,2019-05-21,HP

--table 2 matches:
"order_id","order_date","item_id","buyer_id","seller_id"
1,2019-08-01,4,1,2
2,2019-08-02,2,1,3
3,2019-08-03,3,2,3
4,2019-08-04,1,4,2
5,2019-08-04,1,3,4
6,2019-08-05,2,2,4

-- Required Output
"item_id","item_brand"
1,Samsung
2,Lenovo
3,LG
4,HP

--Solution steps
    --get the ranking of item sold from orders table which sell is no 1 or no 2 and so on and create temp table
    --Join this temp table with items table to get name of sold brand on item id create a temp table
    -- Left Join this temp table with the market_users on m.user_id = d.seller_id
    -- add a filter in join to select only rank 2 sell to get data of second sell
    -- add case statement to check if sold item is favorite item or not to add YES or NO flag

--SQL solution1
   with sell_rank as (
   		select *,
   		    rank() over(partition by seller_id order by order_date) as sell_number
   		from orders),
   sell_rank_and_brand as (
   		select a.*,
   		    b.item_brand as sold_brand
   		from sell_rank a inner join items b
   		    on a.item_id = b.item_id)

   select
        m.user_id,
        m.favorite_brand,
        d.sold_brand,
        case when m.favorite_brand = d.sold_brand
            then 'YES'
            else 'NO' end as result
   from market_users m left outer join sell_rank_and_brand d
        on m.user_id = d.seller_id and sell_number = 2

--Additional logics
with market_analysis as (
	select
		a.seller_id,
		b.item_brand,
		row_number() over(partition by seller_id order by order_date) as rn
	from orders a join items b on a.item_id = b.item_id)
select
	coalesce(seller_id, user_id) as seller_id,
	case when item_brand = favorite_brand then 'YES' else 'NO' end as item_fav_brand
from market_analysis right join market_users
	on seller_id = user_id and rn = 2
order by seller_id