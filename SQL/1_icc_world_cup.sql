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
--"team","match_played","no_of_wins","no_of_losses"
--India,2,2,0
--Eng,2,1,1
--NZ,1,1,0
--Aus,2,1,1
--SA,1,0,1
--SL,2,0,2

--SQL solution1
select team, count(1) as match_played, sum(winner_count) as no_of_wins, 
(count(1) - sum(winner_count)) as no_of_losses from (
select team_1 as team, case when team_1 = winner then 1 else 0 end as winner_count from icc_world_cup union all
select team_2 as team, case when team_2 = winner then 1 else 0 end as winner_count from icc_world_cup) a 
group by team
order by no_of_wins desc

