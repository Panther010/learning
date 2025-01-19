-- question statement
    -- Write an SQL to fill the category column in the given data with last not null value

-- create table statement
create table brands (category varchar(20), brand_name varchar(20));

-- Insert data
insert into brands values
('chocolates','5-star')
,(null,'dairy milk')
,(null,'perk')
,(null,'eclair')
,('Biscuits','britannia')
,(null,'good day')
,(null,'boost');

-- Input data
"category","brand_name"
chocolates,"5-star"
,dairy milk
,perk
,eclair
Biscuits,britannia
,good day
,boost

-- Required Output
"category","brand_name"
chocolates,"5-star"
chocolates,dairy milk
chocolates,perk
chocolates,eclair
Biscuits,britannia
Biscuits,good day
Biscuits,boost


--Solution steps
-- 1. Add the row_number on the table.
-- 2. Save the data in temp table1
-- 3. From this temp table fetch the records not having null in category
-- 4. Using lead function fetch the row number of the next record which is having not null category
-- 5. This new column we can name as next ruw number
-- 6. Save this data in temp table 2
-- 7. join these 2 temp table on rn from first table should be greater or equal to rn of second table
-- 8. it will introduce some extra data
-- have another condition rn from table 1 should be less than next row number from table 2


--SQL solution1
with cte1 as (
	select
		*,
		row_number() over(order by (select null)) as rn
	from brands),
cte2 as (
	select
		*,
		lead(rn,1 ,9999) over(order by rn) as next_rn
	from cte1
	where category is not null)

select
b.category,
a.brand_name
from cte1 a inner join cte2 b on a.rn >= b.rn
and a.rn < b.next_rn