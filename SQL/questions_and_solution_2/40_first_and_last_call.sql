-- question statement
    -- Write an SQL to get the quite students in the class. Quite students are:
        -- Who tok at least one exam and did not score high score nor the low score in any on the exam.
        -- Do not return the student who have not given any exam.

-- create table statement
create table phonelog(caller_id int, recipient_id int, date_called timestamp);

-- Insert data
insert into phonelog(caller_id, recipient_id, date_called)
values(1, 2, '2019-01-01 09:00:00.000'),
       (1, 3, '2019-01-01 17:00:00.000'),
       (1, 4, '2019-01-01 23:00:00.000'),
       (2, 5, '2019-07-05 09:00:00.000'),
       (2, 3, '2019-07-05 17:00:00.000'),
       (2, 3, '2019-07-05 17:20:00.000'),
       (2, 5, '2019-07-05 23:00:00.000'),
       (2, 3, '2019-08-01 09:00:00.000'),
       (2, 3, '2019-08-01 17:00:00.000'),
       (2, 5, '2019-08-01 19:30:00.000'),
       (2, 4, '2019-08-02 09:00:00.000'),
       (2, 5, '2019-08-02 10:00:00.000'),
       (2, 5, '2019-08-02 10:45:00.000'),
       (2, 4, '2019-08-02 11:00:00.000');

-- Input data
"caller_id","recipient_id","date_called"
1,2,2019-01-01 09:00:00.000
1,3,2019-01-01 17:00:00.000
1,4,2019-01-01 23:00:00.000
2,5,2019-07-05 09:00:00.000
2,3,2019-07-05 17:00:00.000
2,3,2019-07-05 17:20:00.000
2,5,2019-07-05 23:00:00.000
2,3,2019-08-01 09:00:00.000
2,3,2019-08-01 17:00:00.000
2,5,2019-08-01 19:30:00.000
2,4,2019-08-02 09:00:00.000
2,5,2019-08-02 10:00:00.000
2,5,2019-08-02 10:45:00.000
2,4,2019-08-02 11:00:00.000

-- Required Output
"student_id","student_name"
2,Jade

--Solution steps
-- 1. Find out the rows which are having highest and lowest marks in an subject
-- 2. Using case statement flag 1 can be set for the student who has get highest or lowest mark in subject
-- 3. rest will get 0 in flag. Save this data temp table
-- 4. Group by student_id get the records having sum of flag == 0
-- 5. These are the quite student.
-- 6. To get name join with students table


--SQL solution1
with cte as (
	select
	*,
	case when rank() over(partition by exam_id order by score) = 1 then 1
		when rank() over(partition by exam_id order by score desc) = 1 then 1
		else 0 end as rank_flag
	from exams)
select
a.student_id, b.student_name
from cte a inner join students b
on a.student_id = b.student_id
group by a.student_id, b.student_name
having sum(rank_flag) = 0

--SQL solution2
with cte as (
select
	student_id, exam_id,
	rank() over(partition by exam_id order by score) low_marks_rank,
	rank() over(partition by exam_id order by score desc) high_marks_rank
	from exams),
cte2 as (
	select distinct student_id from exams where student_id not in (
	select distinct student_id from cte
	where low_marks_rank = 1 or high_marks_rank = 1))
select a.* from students a
inner join cte2 b on a.student_id = b.student_id