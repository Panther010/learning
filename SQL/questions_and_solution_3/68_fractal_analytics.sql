-- question statement
    -- For each region, find the house that won the maximum number of
    -- battles. Display region, house, and number of wins.


-- create table statement
CREATE TABLE king (
    k_no  INT PRIMARY KEY,
    king  VARCHAR(50),
    house VARCHAR(50)
);

CREATE TABLE battle (
    battle_number    INT PRIMARY KEY,
    name             VARCHAR(100),
    attacker_king    INT,
    defender_king    INT,
    attacker_outcome INT,
    region           VARCHAR(50),
    FOREIGN KEY (attacker_king) REFERENCES king(k_no),
    FOREIGN KEY (defender_king) REFERENCES king(k_no)
);


-- insert data
INSERT INTO king (k_no, king, house) VALUES
(1, 'Robb Stark', 'House Stark'),
(2, 'Joffrey Baratheon', 'House Lannister'),
(3, 'Stannis Baratheon', 'House Baratheon'),
(4, 'Balon Greyjoy', 'House Greyjoy'),
(5, 'Mace Tyrell', 'House Tyrell'),
(6, 'Doran Martell', 'House Martell');

INSERT INTO battle (battle_number, name, attacker_king, defender_king, attacker_outcome, region) VALUES
(1, 'Battle of Oxcross', 1, 2, 1, 'The North'),
(2, 'Battle of Blackwater', 3, 4, 0, 'The North'),
(3, 'Battle of the Fords', 1, 5, 1, 'The Reach'),
(4, 'Battle of the Green Fork', 2, 6, 0, 'The Reach'),
(5, 'Battle of the Ruby Ford', 1, 3, 1, 'The Riverlands'),
(6, 'Battle of the Golden Tooth', 2, 1, 0, 'The North'),
(7, 'Battle of Riverrun', 3, 4, 1, 'The Riverlands'),
(8, 'Battle of Riverrun', 1, 3, 0, 'The Riverlands');


-- input data
"battle_number","name","attacker_king","defender_king","attacker_outcome","region"
1,Battle of Oxcross,1,2,1,The North
2,Battle of Blackwater,3,4,0,The North
3,Battle of the Fords,1,5,1,The Reach
4,Battle of the Green Fork,2,6,0,The Reach
5,Battle of the Ruby Ford,1,3,1,The Riverlands
6,Battle of the Golden Tooth,2,1,0,The North
7,Battle of Riverrun,3,4,1,The Riverlands
8,Battle of Riverrun,1,3,0,The Riverlands


-- required output (verified: executed against sqlite3)
"region","house","no_of_wins"
The North,House Stark,2
The Reach,House Martell,1
The Reach,House Stark,1
The Riverlands,House Baratheon,2

-- winner per battle, for reference:
-- 1: Stark (attacker won)      -> The North
-- 2: Greyjoy (defender won)    -> The North
-- 3: Stark (attacker won)      -> The Reach
-- 4: Martell (defender won)    -> The Reach
-- 5: Stark (attacker won)      -> The Riverlands
-- 6: Stark (defender won)      -> The North
-- 7: Baratheon (attacker won)  -> The Riverlands
-- 8: Baratheon (defender won)  -> The Riverlands
-- The Reach genuinely ties 1-1 between Stark and Martell -- both
-- correctly appear in the output.


-- solution steps

-- Step 1:
-- attacker_outcome tells you who won each battle (1 = attacker won,
-- 0 = defender won) -- resolve this into a single "winner" king_id
-- per battle with a CASE expression, rather than carrying two
-- separate king columns forward.

-- Step 2:
-- Join the winner's king_id to the king table to get their house,
-- then count wins grouped by (region, house).

-- Step 3:
-- Rank houses within each region by win count descending, and keep
-- rank = 1. Using rank() (not row_number()) is the right call here
-- deliberately -- it correctly surfaces BOTH houses when there's a
-- genuine tie for most wins in a region (The Reach), rather than
-- arbitrarily picking one winner and hiding the tie.


-- sql solution (scratch attempt -- incomplete, not runnable)
select
	bat.*
from battle bat join king as king on bat.attacker_king
-- Cut off mid-ON-clause (missing "= k.k_no"), and reuses "king" as
-- both the table name and its own alias, which is confusing even
-- where it happens to still parse. Not a candidate solution --
-- looks like an abandoned first attempt at exploring the join.


-- sql solution (final -- verified correct, two equivalent versions)

-- version A: rank computed in a separate final CTE step
with cte as (
    select
        battle_number, region,
        case when attacker_outcome = 1 then attacker_king else defender_king end as winner
    from battle
),
win_counter as (
    select
        c.region,
        k.house,
        count(battle_number) as no_of_wins
    from cte c
    join king k on c.winner = k.k_no
    group by c.region, k.house
),
mx_win as (
    select *,
        rank() over (partition by region order by no_of_wins desc) as rn
    from win_counter
)
select region, house, no_of_wins
from mx_win
where rn = 1;

-- version B: rank computed inline in the same aggregation step
-- (functionally identical -- one fewer CTE, count(*) instead of
-- count(battle_number))
with cte as (
    select
        battle_number, region,
        case when attacker_outcome = 1 then attacker_king else defender_king end as winner
    from battle
),
win_counter as (
    select
        c.region,
        k.house,
        count(*) as no_of_wins,
        rank() over (partition by region order by count(*) desc) as rn
    from cte c
    join king k on c.winner = k.k_no
    group by c.region, k.house
)
select region, house, no_of_wins
from win_counter
where rn = 1;

