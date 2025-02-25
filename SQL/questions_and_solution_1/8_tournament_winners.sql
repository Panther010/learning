-- question statement
    -- Write a query to find the winner in each group

    --Winner is a player who scored the maximum total points within the group.
    --In case of tie, the lowest player_id wins

-- create table statement
create table players (player_id int, group_id int);

create table matches (match_id int, first_player int, second_player int, first_score int, second_score int);

-- Insert data
    INSERT INTO players (player_id, group_id)
    VALUES
        (15, 1),
        (25, 1),
        (30, 1),
        (45, 1),
        (10, 2),
        (35, 2),
        (50, 2),
        (20, 3),
        (40, 3);


    INSERT INTO matches (match_id, first_player, second_player, first_score, second_score)
    VALUES
        (1, 15, 45, 3, 0),
        (2, 30, 25, 1, 2),
        (3, 30, 15, 2, 0),
        (4, 40, 20, 5, 2),
        (5, 35, 50, 1, 1);

-- Input data
--table 1 players:
"player_id","group_id"
15,1
25,1
30,1
45,1
10,2
35,2
50,2
20,3
40,3


--table 2 matches:
"match_id","first_player","second_player","first_score","second_score"
1,15,45,3,0
2,30,25,1,2
3,30,15,2,0
4,40,20,5,2
5,35,50,1,1


-- Required Output
"group_id","player","total_score","ranking"
1,15,3,1
2,35,1,1
3,40,5,1

--Solution steps
    --get the all the players and there scores by union 2 tables first and second player data from matches table
    --calculate total score of each player by adding the scores of each player
    --second driver id with user id
    --add the group details to the table by joining with players table
    -- add the players ranking by highest score and the low player_id
    -- filter on rank 1 players to get desired result


--SQL solution1
with players_and_scores as
	(select first_player as player, first_score as score from matches m1
	union all
	select second_player as player, second_score as score from matches m),
players_and_total_score as (
	select player, sum(score) as total_score
	from players_and_scores
	group by player),
player_ranking as (
	select group_id,
		player,
		total_score,
		rank() over(partition by group_id order by total_score desc, player) as ranking
	 from players_and_total_score inner join
	players p on player = player_id)

select * from player_ranking where ranking = 1

--Additional logics
with player_score as (
	select
		first_player as player,
		first_score as score
	from matches
	union all
	select
		second_player as player,
		second_score as score
	from matches),
player_ranking as (
	select
		b.group_id,
		player,
		sum(score) total_score,
		rank() over(partition by b.group_id order by sum(score) desc, player)
	from player_score a join players b on a.player = b.player_id
	group by player, b.group_id)
select * from player_ranking where rank = 1