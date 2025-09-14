-- question statement
    -- write a query to find all couples of trade for same stock that happened in the range of 10 seconds
    --and having difference by more that 10 %
    --Output result should also list the percentage f price difference between the 2 trade

-- create table statement update
Create Table Trade_tbl(
TRADE_ID varchar(20),
Trade_Timestamp time,
Trade_Stock varchar(20),
Quantity int,
Price Float
)

-- Insert data
Insert into Trade_tbl Values('TRADE1','10:01:05','ITJunction4All',100,20)
Insert into Trade_tbl Values('TRADE2','10:01:06','ITJunction4All',20,15)
Insert into Trade_tbl Values('TRADE3','10:01:08','ITJunction4All',150,30)
Insert into Trade_tbl Values('TRADE4','10:01:09','ITJunction4All',300,32)
Insert into Trade_tbl Values('TRADE5','10:10:00','ITJunction4All',-100,19)
Insert into Trade_tbl Values('TRADE6','10:10:01','ITJunction4All',-300,19)


-- Input data
"userid","productid","purchasedate"
1,1,2012-01-23
1,2,2012-01-23
1,3,2012-01-25
2,1,2012-01-23
2,2,2012-01-23
2,2,2012-01-25
2,4,2012-01-25
3,4,2012-01-23
3,1,2012-01-23
4,1,2012-01-23
4,2,2012-01-25

-- Required Output
"userid"
1
4

--Solution steps
-- 1. self join the table on user id on same userid and differentdate not same
-- 2. productid same or greater than the first to avoid duplicate
-- 3. this join wil give us products pair bought by same user on different date save this data in temp table
-- 4. group by user id conditional sum 1 when product id is same else 0
-- 5. select only records having sum 0 to get the user not bought same product on different date

--SQL solution1

with cte as(
	select
		*,
		rank() over(partition by user_id order by created_at) as rn
	from marketing_campaign),
first_day as (
	select * from cte where rn = 1),
other_day as (
	select * from cte where rn != 1)

select
distinct a.user_id
from other_day	a left join first_day b
on a.user_id = b.user_id and a.product_id = b.product_id
where b.user_id is null
order by user_id
