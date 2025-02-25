-- question statement
--Write a query to find PersonID, name, number of friends, sum of marks
--of a person who have friends with total score greater than 100

-- create table statement
create table person (person_id int, name varchar(100), email varchar(100), score int);

create table friend (person_id int, friend_id int);

-- Insert data
INSERT INTO person (person_id, name, email, score) VALUES
(1,'Alice','alice2018@hotmail.com',88),
(2,'Bob','bob2018@hotmail.com',11),
(3,'Davis','davis2018@hotmail.com',27),
(4,'Tara','tara2018@hotmail.com',45),
(5,'John','john2018@hotmail.com',63);

INSERT INTO friend (person_id, friend_id) VALUES
(1,2), (1,3), (2,1), (2,3), (3,5), (4,2), (4,3), (4,5);

-- Input data
--table 1 person
    person_id,name,email,score
    1,Alice,alice2018@hotmail.com,88
    2,Bob,bob2018@hotmail.com,11
    3,Davis,davis2018@hotmail.com,27
    4,Tara,tara2018@hotmail.com,45
    5,John,john2018@hotmail.com,63

--table 2 friends
    person_id,friend_id
    1,2
    1,3
    2,1
    2,3
    3,5
    4,2
    4,3
    4,5

-- Required Output
"person_id","name","friends_count","sum_of_marks"
2,Bob,2,115
4,Tara,3,101

--Solution steps
-- create a tem table by
    -- joining friends and person table on f.friend_id = p.person_id
    -- make another join with this table to person table to get the name of the person
    -- get person_id, name friend_id, and friends score by above join
    -- aggregate on person_id and name to get the friend count and sum of marks in new temp table
    -- apply total marks filter

--SQL solution1
with friend_make_details as (
	select f.person_id,
		p2.name,
		p.person_id as friend_id,
		p.name as friend_name, p.score as friend_score
	from friend f inner join person p
		on f.friend_id = p.person_id
		inner join person p2
		on f.person_id = p2.person_id),
friend_make_sum as (
	select
		person_id,
		name,
		count(1) as friends_count,
		sum(friend_score) as sum_of_marks
	from friend_make_details
	group by person_id, name)

select * from friend_make_sum
where sum_of_marks > 100

--Additional logics
with friend_mark_details as (
	select
		a.person_id,
		a.name,
		b.friend_id,
		c.name as friend_name,
		c.score as friend_score
	from person a join friend b
		on a.person_id = b.person_id
	join person c on b.friend_id = c.person_id),
marks_total as (
	select
		person_id,
		name,
		count(1) as friend_count,
		sum(friend_score) sum_of_marks
	from friend_mark_details
	group by person_id, name)
select * from marks_total where sum_of_marks > 100

