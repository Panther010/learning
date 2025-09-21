-- question statement
    -- List of students who scored above the average marks in each subject
    -- Percentage of student who score more than 90 in any subject the total students
    -- second highest and second lowest mark of each subject
    -- From first test marks have increased or decreased


-- create table statement
CREATE TABLE  students (
  studentid   int  NULL,
  studentname   varchar (255) NULL,
  subject   varchar (255) NULL,
  marks   int  NULL,
  testid   int  NULL,
  testdate   date  NULL
)

-- Insert data
insert into students values
	(2,'Max Ruin','Subject1',63,1,'2022-01-02'),
	(3,'Arnold','Subject1',95,1,'2022-01-02'),
	(4,'Krish Star','Subject1',61,1,'2022-01-02'),
	(5,'John Mike','Subject1',91,1,'2022-01-02'),
	(4,'Krish Star','Subject2',71,1,'2022-01-02'),
	(3,'Arnold','Subject2',32,1,'2022-01-02'),
	(5,'John Mike','Subject2',61,2,'2022-11-02'),
	(1,'John Deo','Subject2',60,1,'2022-01-02'),
	(2,'Max Ruin','Subject2',84,1,'2022-01-02'),
	(2,'Max Ruin','Subject3',29,3,'2022-01-03'),
	(5,'John Mike','Subject3',98,2,'2022-11-02');

-- Input data
"studentid","studentname","subject","marks","testid","testdate"
2,Max Ruin,Subject1,63,1,2022-01-02
3,Arnold,Subject1,95,1,2022-01-02
4,Krish Star,Subject1,61,1,2022-01-02
5,John Mike,Subject1,91,1,2022-01-02
4,Krish Star,Subject2,71,1,2022-01-02
3,Arnold,Subject2,32,1,2022-01-02
5,John Mike,Subject2,61,2,2022-11-02
1,John Deo,Subject2,60,1,2022-01-02
2,Max Ruin,Subject2,84,1,2022-01-02
2,Max Ruin,Subject3,29,3,2022-01-03
5,John Mike,Subject3,98,2,2022-11-02

-- Required Output
    -- List of students who scored above the average marks in each subject
"studentid","studentname","subject","marks","testid","testdate","avg_marks"
3,Arnold,Subject1,95,1,2022-01-02,77.5000000000000000
5,John Mike,Subject1,91,1,2022-01-02,77.5000000000000000
4,Krish Star,Subject2,71,1,2022-01-02,61.6000000000000000
2,Max Ruin,Subject2,84,1,2022-01-02,61.6000000000000000
5,John Mike,Subject3,98,2,2022-11-02,63.5000000000000000

-- Percentage of student who score more than 90 in any subject the total students
"bright_student"
40.0000000000000000

-- second highest and second lowest mark of each subject
"subject","lowest_2nd","higest_2nd"
Subject1,63,91
Subject2,60,71
Subject3,98,29

-- From previous test marks have increased or decreased
"studentname","subject","marks","previous_marks","marks_update"
Arnold,Subject1,95,,
Arnold,Subject2,32,95,decreased
John Deo,Subject2,60,,
John Mike,Subject1,91,,
John Mike,Subject2,61,91,decreased
John Mike,Subject3,98,61,increased
Krish Star,Subject1,61,,
Krish Star,Subject2,71,61,increased
Max Ruin,Subject1,63,,
Max Ruin,Subject2,84,63,increased
Max Ruin,Subject3,29,84,decreased


--Solution steps

--SQL solution1
-- List of students who scored above the average marks in each subject
with cte as (
	select
		*,
		avg(marks) over(partition by subject) as avg_marks
	from students)

select * from cte
where marks > avg_marks


-- Percentage of student who score more than 90 in any subject the total students
select
(count(distinct case when marks > 90 then studentid else null end) * 100.0/
count(distinct studentid)) as bright_student
from students


-- second highest and second lowest mark of each subject
with cte as (
	select
		subject,
		marks,
		rank() over(partition by subject order by marks) lowest_marks_rank,
		rank() over(partition by subject order by marks desc) higest_marks_rank
	from students)
select
	subject,
	sum(case when lowest_marks_rank = 2 then marks else null end) as lowest_2nd,
	sum(case when higest_marks_rank = 2 then marks else null end) as higest_2nd
from cte
group by subject


-- From previous test marks have increased or decreased
with cte as (
	select
		studentname,
		subject,
		marks,
		lag(marks) over(partition by studentname order by subject) as previous_marks
	from students)
select
	studentname,
	subject,
	marks,
	previous_marks,
	case when marks < previous_marks then 'decreased'
		when marks > previous_marks then 'increased'
	else null end as marks_update
from cte
