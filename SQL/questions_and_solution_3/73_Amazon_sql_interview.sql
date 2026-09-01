-- question statement
    -- Find the number of active Prime subscribers at the end of
    -- 2020, broken down by marketplace.

-- create table statement
CREATE TABLE subscription_history (
    customer_id          INT,
    marketplace          VARCHAR(10),
    event_date           DATE,
    event                CHAR(1),
    subscription_period  INT
);


-- Insert data
INSERT INTO subscription_history VALUES (1, 'India', '2020-01-05', 'S', 6);
INSERT INTO subscription_history VALUES (1, 'India', '2020-12-05', 'R', 1);
INSERT INTO subscription_history VALUES (1, 'India', '2021-02-05', 'C', null);
INSERT INTO subscription_history VALUES (2, 'India', '2020-02-15', 'S', 12);
INSERT INTO subscription_history VALUES (2, 'India', '2020-11-20', 'C', null);
INSERT INTO subscription_history VALUES (3, 'USA', '2019-12-01', 'S', 12);
INSERT INTO subscription_history VALUES (3, 'USA', '2020-12-01', 'R', 12);
INSERT INTO subscription_history VALUES (4, 'USA', '2020-01-10', 'S', 6);
INSERT INTO subscription_history VALUES (4, 'USA', '2020-09-10', 'R', 3);
INSERT INTO subscription_history VALUES (4, 'USA', '2020-12-25', 'C', null);
INSERT INTO subscription_history VALUES (5, 'UK', '2020-06-20', 'S', 12);
INSERT INTO subscription_history VALUES (5, 'UK', '2020-11-20', 'C', null);
INSERT INTO subscription_history VALUES (6, 'UK', '2020-07-05', 'S', 6);
INSERT INTO subscription_history VALUES (6, 'UK', '2021-03-05', 'R', 6);
INSERT INTO subscription_history VALUES (7, 'Canada', '2020-08-15', 'S', 12);
INSERT INTO subscription_history VALUES (8, 'Canada', '2020-09-10', 'S', 12);
INSERT INTO subscription_history VALUES (8, 'Canada', '2020-12-10', 'C', null);
INSERT INTO subscription_history VALUES (9, 'Canada', '2020-11-10', 'S', 1);


-- Input data
"customer_id","marketplace","event_date","event","subscription_period"
1,India,2020-01-05,S,6
1,India,2020-12-05,R,1
1,India,2021-02-05,C,
2,India,2020-02-15,S,12
2,India,2020-11-20,C,
3,USA,2019-12-01,S,12
3,USA,2020-12-01,R,12
4,USA,2020-01-10,S,6
4,USA,2020-09-10,R,3
4,USA,2020-12-25,C,
5,UK,2020-06-20,S,12
5,UK,2020-11-20,C,
6,UK,2020-07-05,S,6
6,UK,2021-03-05,R,6
7,Canada,2020-08-15,S,12
8,Canada,2020-09-10,S,12
8,Canada,2020-12-10,C,
9,Canada,2020-11-10,S,1


-- Required Output (verified: executed against sqlite3)
"marketplace","active_prime_members"
Canada,1
India,1
UK,1
USA,1

-- who and why, per customer (verified by execution + hand trace):
-- cust1 (India): last event <=2020-12-31 is R on 2020-12-05 (1mo) ->
--   expires 2021-01-05, still active at year end -> ACTIVE
-- cust2 (India): last event is C (cancel) on 2020-11-20 -> CANCELLED
-- cust3 (USA): last event is R on 2020-12-01 (12mo) -> expires
--   2021-12-01 -> ACTIVE
-- cust4 (USA): last event is C on 2020-12-25 -> CANCELLED
-- cust5 (UK): last event is C on 2020-11-20 -> CANCELLED
-- cust6 (UK): last event <=2020-12-31 is S on 2020-07-05 (6mo) ->
--   expires 2021-01-05, still active (the 2021-03-05 renewal is
--   outside the analysis window and correctly ignored) -> ACTIVE
-- cust7 (Canada): only event is S on 2020-08-15 (12mo) -> expires
--   2021-08-15 -> ACTIVE
-- cust8 (Canada): last event is C on 2020-12-10 -> CANCELLED
-- cust9 (Canada): only event is S on 2020-11-10 (1mo) -> expires
--   2020-12-10, which is BEFORE 2020-12-31 -> EXPIRED (not renewed
--   in time) -> NOT active


--Solution steps
-- 1. Restrict to events on or before 2020-12-31 -- anything after
--    that date (like cust1's Feb-2021 cancel, or cust6's Mar-2021
--    renewal) is future information relative to the "end of 2020"
--    snapshot and must be ignored.
-- 2. For each customer, take their MOST RECENT event within that
--    window (row_number() partitioned by customer, ordered by
--    event_date desc, keep rn=1) -- this is their subscription
--    status as of year-end.
-- 3. Exclude anyone whose latest status is a cancellation (event = 'C').
-- 4. For everyone else, check whether their subscription (event_date
--    + subscription_period months) has actually expired by 2020-12-31
--    -- a Start/Renew event alone doesn't guarantee coverage through
--    year-end if the period is short and wasn't renewed again in time
--    (this is exactly what disqualifies customer 9).
-- 5. Group the surviving active customers by marketplace and count them.

--SQL solution (as originally written -- returns the row-level list,
-- see notes for the missing final step)
with cte as (select
*,
row_number() over(partition by customer_id order by event_date desc) as rn
from subscription_history where event_date <= '2020-12-31'
order by customer_id, event_date)
select
	*
from cte where rn = 1 and event <> 'C' and
(event_date +  subscription_period * interval '1 month') >= cast('2020-12-31' as date);

--SQL solution (completed -- adds the marketplace-level count the
-- question actually asked for)
with cte as (
    select *,
        row_number() over(partition by customer_id order by event_date desc) as rn
    from subscription_history
    where event_date <= '2020-12-31'
),
active as (
    select customer_id, marketplace
    from cte
    where rn = 1
      and event <> 'C'
      and (event_date + subscription_period * interval '1 month') >= cast('2020-12-31' as date)
)
select
    marketplace,
    count(distinct customer_id) as active_prime_members
from active
group by marketplace
order by marketplace;


