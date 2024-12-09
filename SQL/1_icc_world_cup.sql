-- create table statement
create table icc_world_cup
(
Team_1 Varchar(20),
Team_2 Varchar(20),
Winner Varchar(20)
);

-- Insert data
INSERT INTO icc_world_cup (team_1,team_2,winner) VALUES
	 ('India','SL','India'),
	 ('SL','Aus','Aus'),
	 ('SA','Eng','Eng'),
	 ('Eng','NZ','NZ'),
	 ('Aus','India','India');

-- Input data
select * from icc_world_cup;
--"team_1","team_2","winner"
--India,SL,India
--SL,Aus,Aus
--SA,Eng,Eng
--Eng,NZ,NZ
--Aus,India,India

-- Required Output
-- Calculate Total match played, win and lose for a team
--"team","match_played","no_of_wins","no_of_losses"
--India,2,2,0
--Eng,2,1,1
--NZ,1,1,0
--Aus,2,1,1
--SA,1,0,1
--SL,2,0,2

--Solution steps 
-- 1. bring team_1 an team_2 in same column by union_all
-- 2. get win_count column by check if team_1 is winning or team_2 is winning
-- 3. COUNT all the row by team will give match played by teams
-- 4. SUM of all the win_count will give no_of_win by team
-- 5. Difference of win and played will give loss

--SQL solution1
select team, count(1) as match_played, sum(winner_count) as no_of_wins, 
(count(1) - sum(winner_count)) as no_of_losses from (
select team_1 as team, case when team_1 = winner then 1 else 0 end as winner_count from icc_world_cup union all
select team_2 as team, case when team_2 = winner then 1 else 0 end as winner_count from icc_world_cup) a 
group by team
order by no_of_wins desc

--SQL solution2
with team_and_results as (
	select team_1 as team,
		case when team_1 = winner then 1 else 0 end as win_flag
	from icc_world_cup iwc
	union all
	select team_2 as team,
		case when team_2 = winner then 1 else 0 end as win_flag
	from icc_world_cup iwc)
select team,
	count(1) as match_played,
	sum(win_flag) as win_count,
	count(1) - sum(win_flag) as matches_lost
	from team_and_results
	group by team
	order by sum(win_flag) desc

-- Additional check with draw case (Common table expression)
with win_draw_flag as(
    select team_1 as team, case when team_1 = winner then 1 else 0 end as win_flag,
        case when Winner = 'Draw' then 1 else 0 end as draw_flag from icc_world_cup1 union all
    select team_2 as team, case when team_2 = winner then 1 else 0 end as win_flag,
        case when Winner = 'Draw' then 1 else 0 end as draw_flag from icc_world_cup1)
select team, count(1) as match_played, sum(win_flag) as no_of_wins, 
    (count(1)- sum(win_flag) -sum(draw_flag)) as no_of_losses,
    sum(draw_flag) as no_of_draw from win_draw_flag group by team order by no_of_wins desc