-- question statement
    -- ind student with same marks in Physics and Chemistry

-- create table statement
create table exams (student_id int, subject varchar(20), marks int);

-- Insert data
insert into exams values
    (1,'Chemistry',91)
    ,(1,'Physics',91)
    ,(2,'Chemistry',80)
    ,(2,'Physics',90)
    ,(3,'Chemistry',80)
    ,(4,'Chemistry',71)
    ,(4,'Physics',54);

-- Input data
"student_id","subject","marks"
1,Chemistry,91
1,Physics,91
2,Chemistry,80
2,Physics,90
3,Chemistry,80
4,Chemistry,71
4,Physics,54



-- Required Output
"student_id"
1


--Solution steps
    -- group by student_id
    -- have having filter on subject count > 1
    -- second filter can be on distinct count of marks.
    -- It will ensure getting the records which are having same marks in both the subjects

--SQL solution 1 using special having clause
select student_id
from exams
group by student_id
having count(subject) > 1 and count(distinct marks) = 1


--SQL solution 2 using self join and CTE
with cte as
	(select
		a.student_id,
		a.subject as subject_c,
		b.subject as subject_p,
		a.marks as marks_c,
		b.marks as marks_p
	from exams a inner join exams b on a.student_id=b.student_id
	and a.subject = 'Chemistry' and b.subject = 'Physics')
	select * from cte where marks_c = marks_p
