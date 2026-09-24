-- question statement
    -- For each player, how many total matches did they appear in
    -- (as batter or bowler), how many of those they batted in, and
    -- how many of those they bowled in.

-- create table statement
create table cricket_match(
    matchid   integer,
    ballnumber integer,
    inningno  integer,
    overs     float,
    outcome   varchar(100),
    batter    varchar(100),
    bowler    varchar(100),
    score     float
);


-- Insert data (4 matches, ball-by-ball)
INSERT INTO cricket_match VALUES
(1,1,1,0.1,'0','Mohammed Shami','Devon Conway',0),(1,2,1,0.2,'1lb','Mohammed Shami','Devon Conway',1),
(1,3,1,0.3,'0','Mohammed Shami','Ruturaj Gaikwad',0),(1,4,1,0.4,'1','Mohammed Shami','Ruturaj Gaikwad',1),
... (full ball-by-ball data as provided, 4 matches, ~24-25 balls each);


-- Input data
"matchid","ballnumber","inningno","overs","outcome","batter","bowler","score"
1,1,1,0.1,0,Mohammed Shami,Devon Conway,0
1,2,1,0.2,1lb,Mohammed Shami,Devon Conway,1
1,3,1,0.3,0,Mohammed Shami,Ruturaj Gaikwad,0
... (full ball-by-ball data)


-- Required Output (verified: executed against sqlite3)
"player","total_match_played","batting_matches","bowling_matches"
Alzarri Joseph,2,2,1
Ambati Rayudu,2,2,0
Ben S,1,1,1
Brett Lee,2,0,2
Devon Conway,1,1,1
Hardik Pandya,3,1,2
Josh Little,3,1,2
Moeen Ali,2,1,1
Mohammed Shami,2,2,1
Rashid Khan,2,2,1
Ruturaj Gaikwad,4,4,4
Shivam Dube,1,1,1
Yash Dayal,1,0,1

-- a few notable rows: Ruturaj Gaikwad both batted AND bowled in all
-- 4 matches; Brett Lee and Yash Dayal only ever bowled (0 batting
-- matches); Ambati Rayudu only ever batted (0 bowling matches).


--Solution steps
-- 1. The source data is ball-level, with `batter` and `bowler` as
--    two separate columns per row. To count "matches played" per
--    player regardless of role, first UNIONstack both roles into a
--    single (matchid, player, batting-flag) shape -- one row per
--    ball per role, tagged 1 for batting, 0 for bowling.
-- 2. count(distinct matchid) over the combined set gives total
--    matches played in ANY role.
-- 3. count(distinct matchid) filtered to batting=1 (via a CASE
--    inside the count) gives matches where they batted; same
--    pattern with batting=0 for bowling matches.
-- 4. distinct matchid (not just row count) is essential throughout,
--    since a player appears on MANY balls within the same match --
--    without distinct, this would count balls, not matches.


--SQL solution
with cte as (
	select
		matchid,
		batter as player,
		1 as batting
	from cricket_match
	union all
	select
		matchid,
		bowler as player,
		0 as batting
	from cricket_match
)
select
	player,
	count(distinct matchid) as total_match_played,
	count(distinct case when batting = 1 then matchid else null end) as batting_matches,
	count(distinct case when batting = 0 then matchid else null end) as bowling_matches
from cte
group by player
order by player;


-- Approach 2:
with cte as (
	select
		matchid,
		batter as player,
		1 as batting
	from cricket_match
	union
	select
		matchid,
		bowler as player,
		0 as batting
	from cricket_match
)
select
	player,
	count(distinct matchid) as total_match_played,
	count(case when batting = 1 then matchid else null end) as batting_matches,
	count(case when batting = 0 then matchid else null end) as bowling_matches
from cte
group by player
order by player;

-- approach 3:

with total_match as (
select batter as player, matchid from cricket_match
union
select bowler as player, matchid from cricket_match),
batting_match_cnt as (
	select
		batter as player,
		count(distinct matchid) as batting_matches
	from cricket_match
	group by batter
),
bowling_match_cnt as (
	select
		bowler as player,
		count(distinct matchid) as bowling_matches
	from cricket_match
	group by bowler
),
total_match_cnt as (
	select
		player,
		count(distinct matchid) as total_matched_palyed
	from total_match
	group by player)
select
	a.player,
	coalesce(a.total_matched_palyed, 0) as total_matched_palyed,
	coalesce(b.batting_matches, 0) as batting_matches,
	coalesce(c.bowling_matches,0) as bowling_matches
from total_match_cnt a left join batting_match_cnt b
	on a.player = b.player
left join bowling_match_cnt c
	on a.player = c.player
