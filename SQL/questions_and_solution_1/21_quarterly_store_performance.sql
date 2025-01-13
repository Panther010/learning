-- question statement
    -- write a sql to find stores and quarter when stores were closed

-- create table statement
CREATE TABLE STORES (store varchar(10), quarter varchar(10), amount int);


-- Insert data
INSERT INTO STORES (Store, Quarter, Amount)
    VALUES ('S1', 'Q1', 200),
    ('S1', 'Q2', 300),
    ('S1', 'Q4', 400),
    ('S2', 'Q1', 500),
    ('S2', 'Q3', 600),
    ('S2', 'Q4', 700),
    ('S3', 'Q1', 800),
    ('S3', 'Q2', 750),
    ('S3', 'Q3', 900);

-- Input data
"store","quarter","amount"
S1,Q1,200
S1,Q2,300
S1,Q4,400
S2,Q1,500
S2,Q3,600
S2,Q4,700
S3,Q1,800
S3,Q2,750
S3,Q3,900


-- Required Output
"store","quarter"
S1,Q3
S2,Q2
S3,Q4

--Solution steps
    -- Try making list of all the possible combination  of stores and quarters
    -- Once the table is reasy anti left join or left join with filter on null

--SQL solution 1 using cross join
with stores_and_quarters as (
	select distinct
        a.store,
        b.quarter
	from stores a, stores b)
select
    a.store,
    a.quarter
from stores_and_quarters a left join stores b
	on a.store = b.store and a.quarter = b.quarter
where b.amount is null


--SQL solution 2 using recursive CTE
with recursive cte as(
	select distinct store, 1 as q_no from stores
	union all
	select store, q_no + 1 from cte where q_no < 4)
select
	a.store,
	'Q' || cast(q_no as char(2)) as quarter
from cte a left join stores b
	on a.store = b.store and 'Q' || cast(q_no as char(2)) = b.quarter
where b.amount is null
order by store, q_no


--SQL solution 3 Tricky method
select
	store,
	'Q' || 10 - sum(cast(right(quarter, 1) as integer)) as q_no
from stores
group by store
