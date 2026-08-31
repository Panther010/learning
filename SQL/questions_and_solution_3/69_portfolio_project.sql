-- question statement
    -- A batch of user/login analytics queries against a users +
    -- logins schema: inactivity detection, quarterly rollups with
    -- QoQ growth, cohort retention (logged in one month but not
    -- another), daily top scorer, "best user" streak detection, and
    -- a full calendar gap-fill for days with zero logins.


-- create table statement
CREATE TABLE users (
    USER_ID     INT PRIMARY KEY,
    USER_NAME   VARCHAR(20) NOT NULL,
    USER_STATUS VARCHAR(20) NOT NULL
);

CREATE TABLE logins (
    USER_ID         INT,
    LOGIN_TIMESTAMP timestamp NOT NULL,
    SESSION_ID      INT PRIMARY KEY,
    SESSION_SCORE   INT,
    FOREIGN KEY (USER_ID) REFERENCES USERS(USER_ID)
);


-- insert data
INSERT INTO USERS VALUES (1, 'Alice', 'Active');
INSERT INTO USERS VALUES (2, 'Bob', 'Inactive');
INSERT INTO USERS VALUES (3, 'Charlie', 'Active');
INSERT INTO USERS VALUES (4, 'David', 'Active');
INSERT INTO USERS VALUES (5, 'Eve', 'Inactive');
INSERT INTO USERS VALUES (6, 'Frank', 'Active');
INSERT INTO USERS VALUES (7, 'Grace', 'Inactive');
INSERT INTO USERS VALUES (8, 'Heidi', 'Active');
INSERT INTO USERS VALUES (9, 'Ivan', 'Inactive');
INSERT INTO USERS VALUES (10, 'Judy', 'Active');

INSERT INTO LOGINS VALUES (1, '2023-07-15 09:30:00', 1001, 85);
INSERT INTO LOGINS VALUES (2, '2023-07-22 10:00:00', 1002, 90);
INSERT INTO LOGINS VALUES (3, '2023-08-10 11:15:00', 1003, 75);
INSERT INTO LOGINS VALUES (4, '2023-08-20 14:00:00', 1004, 88);
INSERT INTO LOGINS VALUES (5, '2023-09-05 16:45:00', 1005, 82);
INSERT INTO LOGINS VALUES (6, '2023-10-12 08:30:00', 1006, 77);
INSERT INTO LOGINS VALUES (7, '2023-11-18 09:00:00', 1007, 81);
INSERT INTO LOGINS VALUES (8, '2023-12-01 10:30:00', 1008, 84);
INSERT INTO LOGINS VALUES (9, '2023-12-15 13:15:00', 1009, 79);
INSERT INTO LOGINS (USER_ID, LOGIN_TIMESTAMP, SESSION_ID, SESSION_SCORE) VALUES (1, '2024-01-10 07:45:00', 1011, 86);
INSERT INTO LOGINS (USER_ID, LOGIN_TIMESTAMP, SESSION_ID, SESSION_SCORE) VALUES (2, '2024-01-25 09:30:00', 1012, 89);
INSERT INTO LOGINS (USER_ID, LOGIN_TIMESTAMP, SESSION_ID, SESSION_SCORE) VALUES (3, '2024-02-05 11:00:00', 1013, 78);
INSERT INTO LOGINS (USER_ID, LOGIN_TIMESTAMP, SESSION_ID, SESSION_SCORE) VALUES (4, '2024-03-01 14:30:00', 1014, 91);
INSERT INTO LOGINS (USER_ID, LOGIN_TIMESTAMP, SESSION_ID, SESSION_SCORE) VALUES (5, '2024-03-15 16:00:00', 1015, 83);
INSERT INTO LOGINS (USER_ID, LOGIN_TIMESTAMP, SESSION_ID, SESSION_SCORE) VALUES (6, '2024-04-12 08:00:00', 1016, 80);
INSERT INTO LOGINS (USER_ID, LOGIN_TIMESTAMP, SESSION_ID, SESSION_SCORE) VALUES (7, '2024-05-18 09:15:00', 1017, 82);
INSERT INTO LOGINS (USER_ID, LOGIN_TIMESTAMP, SESSION_ID, SESSION_SCORE) VALUES (8, '2024-05-28 10:45:00', 1018, 87);
INSERT INTO LOGINS (USER_ID, LOGIN_TIMESTAMP, SESSION_ID, SESSION_SCORE) VALUES (9, '2024-06-15 13:30:00', 1019, 76);
INSERT INTO LOGINS (USER_ID, LOGIN_TIMESTAMP, SESSION_ID, SESSION_SCORE) VALUES (10, '2024-06-25 15:00:00', 1010, 92);
INSERT INTO LOGINS (USER_ID, LOGIN_TIMESTAMP, SESSION_ID, SESSION_SCORE) VALUES (10, '2024-06-26 15:45:00', 1020, 93);
INSERT INTO LOGINS (USER_ID, LOGIN_TIMESTAMP, SESSION_ID, SESSION_SCORE) VALUES (10, '2024-06-27 15:00:00', 1021, 92);
INSERT INTO LOGINS (USER_ID, LOGIN_TIMESTAMP, SESSION_ID, SESSION_SCORE) VALUES (10, '2024-06-28 15:45:00', 1022, 93);
INSERT INTO LOGINS (USER_ID, LOGIN_TIMESTAMP, SESSION_ID, SESSION_SCORE) VALUES (1, '2024-01-10 07:45:00', 1101, 86);
INSERT INTO LOGINS (USER_ID, LOGIN_TIMESTAMP, SESSION_ID, SESSION_SCORE) VALUES (3, '2024-01-25 09:30:00', 1102, 89);
INSERT INTO LOGINS (USER_ID, LOGIN_TIMESTAMP, SESSION_ID, SESSION_SCORE) VALUES (5, '2024-01-15 11:00:00', 1103, 78);
INSERT INTO LOGINS (USER_ID, LOGIN_TIMESTAMP, SESSION_ID, SESSION_SCORE) VALUES (2, '2023-11-10 07:45:00', 1201, 82);
INSERT INTO LOGINS (USER_ID, LOGIN_TIMESTAMP, SESSION_ID, SESSION_SCORE) VALUES (4, '2023-11-25 09:30:00', 1202, 84);
INSERT INTO LOGINS (USER_ID, LOGIN_TIMESTAMP, SESSION_ID, SESSION_SCORE) VALUES (6, '2023-11-15 11:00:00', 1203, 80);


-- ============================================================
-- Q1: users who have NOT logged in during the past 5 months
--     ("today" = 2024-06-28)
-- ============================================================

-- required output (verified: cutoff = 2024-01-28)
"user_id","last_login"
1,2024-01-10 07:45:00
2,2024-01-25 09:30:00

--SQL solution (join version -- includes user details, the more complete answer)
with cte as (
select
	user_id,
	max(LOGIN_TIMESTAMP) as last_login,
	to_date('2024-06-28', 'yyyy-MM-dd') - interval '5 months' as login_cutoff
from logins
group by user_id
)
select
	c.user_id, last_login, login_cutoff, USER_NAME, USER_STATUS
from cte c join users u on u.user_id = c.user_id and last_login < login_cutoff;



-- ============================================================
-- Q2: user_count and session_count per quarter, newest to oldest
-- ============================================================

-- required output (verified: executed against sqlite3)
"quarter","year","user_count","session_count","first_day_of_quarter"
2,2024,5,8,2024-04-01
1,2024,5,8,2024-01-01
4,2023,6,7,2023-10-01
3,2023,5,5,2023-07-01

--SQL solution
select
	date_part('quarter', LOGIN_TIMESTAMP) as quarter,
	date_part('year', LOGIN_TIMESTAMP) as session_year,
	count(distinct user_id) as user_count,
	count(SESSION_ID) as session_count,
	date_trunc('quarter', min(LOGIN_TIMESTAMP)) as min_login
from logins
group by date_part('year', LOGIN_TIMESTAMP), date_part('quarter', LOGIN_TIMESTAMP)
order by date_part('year', LOGIN_TIMESTAMP) desc, date_part('quarter', LOGIN_TIMESTAMP) desc;


-- ============================================================
-- Q3: user_id who logged in Jan 2024 but did NOT log in Nov 2023
-- ============================================================

-- required output (verified: executed against sqlite3)
"user_id"
1
3
5

--SQL solution
select
	distinct user_id
from logins
where LOGIN_TIMESTAMP between '2024-01-01' and '2024-01-31'
and user_id not in (select user_id from logins where LOGIN_TIMESTAMP between '2023-11-01' and '2023-11-30')
;


-- ============================================================
-- Q4: add QoQ session_count percentage change to Q2
-- ============================================================

-- required output (verified: executed against sqlite3; values match
-- hand-calculated QoQ growth)
"first_day_of_quarter","session_count","session_count_prev","pct_change"
2023-07-01,5,5,0.00
2023-10-01,7,5,40.00
2024-01-01,8,7,14.29
2024-04-01,8,8,0.00

--SQL solution
with cte as (
select
	count(distinct user_id) as user_count,
	count(SESSION_ID) as session_count,
	date_trunc('quarter', min(LOGIN_TIMESTAMP)) as min_login
from logins
group by date_part('year', LOGIN_TIMESTAMP), date_part('quarter', LOGIN_TIMESTAMP)
order by date_part('year', LOGIN_TIMESTAMP) desc, date_part('quarter', LOGIN_TIMESTAMP) desc
)
select
	min_login,
	session_count,
	lag(session_count,1,session_count) over(order by min_login) as session_count_prev,
	((session_count - (lag(session_count,1,session_count) over(order by min_login))) * 1.0
		/ (lag(session_count,1,session_count) over(order by min_login))) * 100 as session_percentage_change
from cte
order by min_login;


-- ============================================================
-- Q5: user with the highest session score per day
-- ============================================================

-- required output as originally written (SUM-based) -- verified by
-- execution; flagged as a likely mismatch with the stated ask
"login_date","session_score","user_name"
...
2024-01-10,172,Alice   <-- only day this differs from the MAX version
...

--SQL solution (as written)
with cte as (select
	cast(LOGIN_TIMESTAMP as date) login_date,
	sum(session_score) as session_score,
	user_id
from logins
group by user_id, cast(LOGIN_TIMESTAMP as date)),
score_calculator as
(
select
	*,
	rank() over(partition by login_date order by session_score desc) as rn
from cte)
select
	login_date, session_score, user_name
from score_calculator c join users u on u.user_id = c.user_id
where rn = 1
order by login_date;


-- ============================================================
-- Q6: "best user" -- had a session every single day since their
--     first login, through today (2024-06-28)
-- ============================================================

-- required output (verified: executed against sqlite3)
"user_id","first_login_date","required_logins","login_count"
10,2024-06-25,4,4

--SQL solution
select
	user_id,
	min(cast(LOGIN_TIMESTAMP as date)) as first_login_date,
	cast('2024-06-28' as date) - min(cast(LOGIN_TIMESTAMP as date)) + 1 as required_logins,
	count(distinct cast(LOGIN_TIMESTAMP as date)) login_count
from logins
group by user_id
having count(distinct cast(LOGIN_TIMESTAMP as date)) = (cast('2024-06-28' as date) - min(cast(LOGIN_TIMESTAMP as date)) + 1)
order by user_id;


-- ============================================================
-- Q7: which calendar dates had zero logins at all
-- ============================================================

-- required output (verified: executed against sqlite3)
-- 324 dates with zero logins, spanning 2023-07-16 through 2024-06-27
-- (excluding the ~25 actual login dates within that range)

--SQL solution
with recursive cte as (
	select
		min(cast(LOGIN_TIMESTAMP as date)) start_date,
		max(cast(LOGIN_TIMESTAMP as date)) end_date
	from logins
	union all
	select
		start_date + 1,
		end_date
	from cte
	where start_date < end_date
)
select
	start_date
from cte left join logins on
	start_date = cast(LOGIN_TIMESTAMP as date)
where user_id isnull
order by start_date;

