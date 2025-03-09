-- question statement
    -- write a query to users who bought different products on different dates
    -- products purchased on any given date are not repeated on any other day by same user

-- create table statement update
create table purchase_history (userid int, productid int, purchasedate date);

-- Insert data
insert into purchase_history values
(1,1,'2012-01-23')
,(1,2,'2012-01-23')
,(1,3,'2012-01-25')
,(2,1,'2012-01-23')
,(2,2,'2012-01-23')
,(2,2,'2012-01-25')
,(2,4,'2012-01-25')
,(3,4,'2012-01-23')
,(3,1,'2012-01-23')
,(4,1,'2012-01-23')
,(4,2,'2012-01-25');

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
with cte as (
	select
		a.*,
		b.productid as b_productid,
		b.purchasedate
	from purchase_history a join purchase_history b on
		a.userid = b.userid and
		a.purchasedate != b.purchasedate and
		a.productid <= b.productid)
select
	userid
from cte
group by userid
having sum(case when productid = b_productid then 1 else 0 end) = 0

-- SQL solution to by checking if there are different purchase date and
-- distinct product count and total product count is same
select
	userid
from purchase_history
group by userid
having count(distinct purchasedate) > 1 and count(productid) = count(distinct productid)