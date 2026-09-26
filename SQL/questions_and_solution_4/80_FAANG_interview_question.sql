-- question statement
    -- Each pair of consecutive transaction rows (odd id, then even id)
    -- represents one transfer: the odd row is the seller, the even
    -- row is the buyer, sharing the same amount and timestamp. Find
    -- the top 5 seller-buyer pairs by number of transactions between
    -- them -- but disqualify any pair where either party has also
    -- played the OPPOSITE role somewhere else in the data (a seller
    -- who has ever also been a buyer, or a buyer who has ever also
    -- been a seller, is excluded from every pair they appear in).

-- create table statement
CREATE TABLE transactions (
    transaction_id INT PRIMARY KEY,
    customer_id    INT,
    amount         INT,
    tran_Date      timestamp
);


-- Insert data
INSERT INTO transactions VALUES (1, 101, 500, '2025-01-01 10:00:01');
INSERT INTO transactions VALUES (2, 201, 500, '2025-01-01 10:00:01');
INSERT INTO transactions VALUES (3, 102, 300, '2025-01-02 00:50:01');
INSERT INTO transactions VALUES (4, 202, 300, '2025-01-02 00:50:01');
INSERT INTO transactions VALUES (5, 101, 700, '2025-01-03 06:00:01');
INSERT INTO transactions VALUES (6, 202, 700, '2025-01-03 06:00:01');
INSERT INTO transactions VALUES (7, 103, 200, '2025-01-04 03:00:01');
INSERT INTO transactions VALUES (8, 203, 200, '2025-01-04 03:00:01');
INSERT INTO transactions VALUES (9, 101, 400, '2025-01-05 00:10:01');
INSERT INTO transactions VALUES (10, 201, 400, '2025-01-05 00:10:01');
INSERT INTO transactions VALUES (11, 101, 500, '2025-01-07 10:10:01');
INSERT INTO transactions VALUES (12, 201, 500, '2025-01-07 10:10:01');
INSERT INTO transactions VALUES (13, 102, 200, '2025-01-03 10:50:01');
INSERT INTO transactions VALUES (14, 202, 200, '2025-01-03 10:50:01');
INSERT INTO transactions VALUES (15, 103, 500, '2025-01-01 11:00:01');
INSERT INTO transactions VALUES (16, 101, 500, '2025-01-01 11:00:01');
INSERT INTO transactions VALUES (17, 203, 200, '2025-11-01 11:00:01');
INSERT INTO transactions VALUES (18, 201, 200, '2025-11-01 11:00:01');


-- Input data
"transaction_id","customer_id","amount","tran_Date"
1,101,500,2025-01-01 10:00:01
2,201,500,2025-01-01 10:00:01
3,102,300,2025-01-02 00:50:01
4,202,300,2025-01-02 00:50:01
5,101,700,2025-01-03 06:00:01
6,202,700,2025-01-03 06:00:01
7,103,200,2025-01-04 03:00:01
8,203,200,2025-01-04 03:00:01
9,101,400,2025-01-05 00:10:01
10,201,400,2025-01-05 00:10:01
11,101,500,2025-01-07 10:10:01
12,201,500,2025-01-07 10:10:01
13,102,200,2025-01-03 10:50:01
14,202,200,2025-01-03 10:50:01
15,103,500,2025-01-01 11:00:01
16,101,500,2025-01-01 11:00:01
17,203,200,2025-11-01 11:00:01
18,201,200,2025-11-01 11:00:01


-- Required Output (verified: executed against sqlite3)
"seller_id","buyer_id","txn_count"
102,202,2

-- how the other 5 raw pairs get eliminated:
-- (101,201): 3 txns -- 101 also appears as a BUYER (in pair 103->101)
--   -> 101 disqualified -> pair excluded
-- (101,202): 1 txn -- same reason, 101 disqualified
-- (103,101): 1 txn -- 101 is the buyer here, disqualified
-- (103,203): 1 txn -- 203 also appears as a SELLER (in pair 203->201)
--   -> 203 disqualified -> pair excluded
-- (203,201): 1 txn -- 203 is the seller here, disqualified
-- (102,202): 2 txns -- neither 102 nor 202 EVER appears in the
--   opposite role anywhere in the data -> the only pair that survives


--Solution steps
-- 1. Use lead(customer_id) ordered by transaction_id to pull each
--    row's NEXT row's customer_id alongside it -- this pairs every
--    odd-numbered row (seller) with the even-numbered row right
--    after it (buyer), since they were inserted as consecutive pairs.
-- 2. Filter to only the odd rows (transaction_id % 2 = 1) so each
--    real-world transaction is counted exactly once, not twice
--    (once from the odd row's perspective, once redundantly from
--    the even row's).
-- 3. Group by (seller_id, buyer_id) and count transactions between
--    each pair.
-- 4. Disqualification: find every customer_id that shows up in BOTH
--    the seller_id column AND the buyer_id column of the pair-level
--    summary (INTERSECT) -- these are people who have played both
--    roles somewhere in the dataset. Exclude any pair where either
--    the seller or the buyer is in that set.


--SQL solution (as written -- see notes for the missing final step)
with cte as  (
	select
		transaction_id,
		customer_id as seller_id,
		lead(customer_id) over(order by transaction_id) as buyer_id,
		amount,
		tran_Date
	from transactions
	),
seller_buyer_combo as (
	select
		seller_id,
		buyer_id,
		count(transaction_id) as txn_count
	from cte
	where transaction_id % 2 = 1
	group by seller_id, buyer_id
	order by count(transaction_id) desc),
seller_buyer as (
	select seller_id from seller_buyer_combo
	intersect
	select buyer_id from seller_buyer_combo
)
select * from seller_buyer_combo
where seller_id not in (select seller_id from seller_buyer)
	and buyer_id not in (select seller_id from  seller_buyer);


--SQL solution (completed -- actually returns "top 5" as asked)
with cte as (
	select
		transaction_id,
		customer_id as seller_id,
		lead(customer_id) over(order by transaction_id) as buyer_id
	from transactions
),
seller_buyer_combo as (
	select
		seller_id,
		buyer_id,
		count(transaction_id) as txn_count
	from cte
	where transaction_id % 2 = 1
	group by seller_id, buyer_id
),
disqualified as (
	select seller_id from seller_buyer_combo
	intersect
	select buyer_id from seller_buyer_combo
)
select seller_id, buyer_id, txn_count
from seller_buyer_combo
where seller_id not in (select seller_id from disqualified)
  and buyer_id not in (select seller_id from disqualified)
order by txn_count desc
limit 5;
