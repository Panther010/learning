-- question statement
    -- Two tables: polls (each user's bet on a poll option) and
    -- poll_answers (the correct option per poll). Winners split the
    -- LOSING pool proportionally to their own stake in the winning
    -- pool, and also get their original stake back. Return, per
    -- winning user: their winnings (amount_win) and their total
    -- payout (total_amount_received = winnings + original stake).

-- create table statement
create table polls (
    user_id         varchar(4),
    poll_id         varchar(3),
    poll_option_id  varchar(3),
    amount          int,
    created_date    date
);

create table poll_answers (
    poll_id             varchar(3),
    correct_option_id   varchar(3)
);


-- Insert data
INSERT INTO polls (user_id, poll_id, poll_option_id, amount, created_date) VALUES
('id1', 'p1', 'A', 200, '2021-12-01'),
('id2', 'p1', 'C', 250, '2021-12-01'),
('id3', 'p1', 'A', 200, '2021-12-01'),
('id4', 'p1', 'B', 500, '2021-12-01'),
('id5', 'p1', 'C', 50, '2021-12-01'),
('id6', 'p1', 'D', 500, '2021-12-01'),
('id7', 'p1', 'C', 200, '2021-12-01'),
('id8', 'p1', 'A', 100, '2021-12-01'),
('id9', 'p2', 'A', 300, '2023-01-10'),
('id10', 'p2', 'C', 400, '2023-01-11'),
('id11', 'p2', 'B', 250, '2023-01-12'),
('id12', 'p2', 'D', 600, '2023-01-13'),
('id13', 'p2', 'C', 150, '2023-01-14'),
('id14', 'p2', 'A', 100, '2023-01-15'),
('id15', 'p2', 'C', 200, '2023-01-16');

INSERT INTO poll_answers (poll_id, correct_option_id) VALUES
('p1', 'C'),('p2', 'A');


-- Input data
"user_id","poll_id","poll_option_id","amount","created_date"
id1,p1,A,200,2021-12-01
id2,p1,C,250,2021-12-01
id3,p1,A,200,2021-12-01
id4,p1,B,500,2021-12-01
id5,p1,C,50,2021-12-01
id6,p1,D,500,2021-12-01
id7,p1,C,200,2021-12-01
id8,p1,A,100,2021-12-01
id9,p2,A,300,2023-01-10
id10,p2,C,400,2023-01-11
id11,p2,B,250,2023-01-12
id12,p2,D,600,2023-01-13
id13,p2,C,150,2023-01-14
id14,p2,A,100,2023-01-15
id15,p2,C,200,2023-01-16

"poll_id","correct_option_id"
p1,C
p2,A


-- Required Output (verified: executed against sqlite3; total payout
-- per poll matches total pot exactly -- 2000 for both p1 and p2)
"poll_id","user_id","amount_win","total_amount_received"
p1,id2,750.0,1000.0
p1,id5,150.0,200.0
p1,id7,600.0,800.0
p2,id9,1200.0,1500.0
p2,id14,400.0,500.0

-- math, for reference (p1, correct answer = C):
-- winning pool (option C total): 250+50+200 = 500
-- losing pool (everything else):  200+200+500+500+100 = 1500
-- payout ratio = losing pool / winning pool = 3x each winning dollar
-- id2: 250 * 3 = 750 winnings, +250 stake = 1000 total
-- id5: 50 * 3 = 150 winnings, +50 stake = 200 total
-- id7: 200 * 3 = 600 winnings, +200 stake = 800 total
-- (750+150+600 = 1500 = exactly the losing pool -- fully distributed)


--Solution steps
-- 1. Left join polls to poll_answers on poll_id, so every bet row
--    knows what the correct option for its poll was.
-- 2. Per poll, sum two window totals in parallel: `win` = total
--    amount bet on the CORRECT option (the winning pool), `other` =
--    total amount bet on every OTHER option (the losing pool, which
--    is what gets redistributed).
-- 3. For each winning bet, its share of the losing pool is
--    proportional to its share of the winning pool:
--    (this bet's amount / winning pool total) * losing pool total.
-- 4. total_amount_received adds the original stake back on top of
--    the winnings -- winners don't lose their own bet, they just
--    split everyone else's.
-- 5. Filter to only rows where poll_option_id = correct_option_id --
--    losers get nothing (0), and this WHERE clause drops them from
--    the output entirely.


--SQL solution
with cte as (
select
	p.user_id, p.poll_id, p.poll_option_id, p.amount,
	a.correct_option_id,
	sum(case when p.poll_option_id = a.correct_option_id then amount else 0 end) over(partition by p.poll_id) as win,
	sum(case when p.poll_option_id != a.correct_option_id then amount else 0 end) over(partition by p.poll_id) as other
from polls p left join poll_answers a on p.poll_id = a.poll_id
)
select
	poll_id,
	user_id,
	case when poll_option_id = correct_option_id then (amount * 1.0/win) * other
	else 0 end as amount_win,
	case when poll_option_id = correct_option_id then ((amount * 1.0/win) * other) + amount
	else 0 end as total_amount_received
from cte c
where poll_option_id = correct_option_id;
