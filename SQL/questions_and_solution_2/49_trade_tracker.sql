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
"trade_id","trade_timestamp","trade_stock","quantity","price"
TRADE1,10:01:05,ITJunction4All,100,20.0
TRADE2,10:01:06,ITJunction4All,20,15.0
TRADE3,10:01:08,ITJunction4All,150,30.0
TRADE4,10:01:09,ITJunction4All,300,32.0
TRADE5,10:10:00,ITJunction4All,-100,19.0
TRADE6,10:10:01,ITJunction4All,-300,19.0

-- Required Output
"first_trade","second_trade","first_trade_price","second_trade_price","percentage_diff"
TRADE1,TRADE2,20.0,15.0,25.0
TRADE1,TRADE3,20.0,30.0,50.0
TRADE1,TRADE4,20.0,32.0,60.0
TRADE2,TRADE3,15.0,30.0,100.0
TRADE2,TRADE4,15.0,32.0,113.33333333333333

--Solution steps
-- 1. Self join on trade company.
-- 2. to avoid duplicate use time stamp column in join filter t1 < t2
-- 3. calculate required column -> first_trade, second_trade, first_trade_price, second_trade_price, percentage_diff, time_difference
-- 4. use abs to get positive results
-- 5. apply filters --> percentage_diff > 10 and time_difference < 10

--SQL solution1

with trade_compare_tbl as (
	select
		t1.trade_id as first_trade,
		t2.trade_id as second_trade,
		t1.price as first_trade_price,
		t2.price as second_trade_price,
		date_part('second', t2.trade_timestamp - t1.trade_timestamp) as time_difference,
		t1.trade_stock,
		abs(t1.price - t2.price) as price_difference,
		(abs(t2.price - t1.price) / t1.price) * 100 as percentage_diff
	from trade_tbl as t1 inner join trade_tbl t2
		on t1.trade_stock = t2.trade_stock and t1.trade_timestamp < t2.trade_timestamp)
select
	first_trade,
	second_trade,
	first_trade_price,
	second_trade_price,
	percentage_diff
from trade_compare_tbl
where percentage_diff > 10 and time_difference < 10
order by first_trade, second_trade
