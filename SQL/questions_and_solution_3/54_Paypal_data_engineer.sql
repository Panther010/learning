-- question statement
    -- Find for each employee: employee id, their default phone number,
    -- total check-in entries, total logins, total logouts,
    -- last login time, last logout time.


------------------------------------------------------------
-- Create Table Statement
------------------------------------------------------------
CREATE TABLE "employee_checkin_details" (
    "employeeid"        INT,
    "entry_details"     VARCHAR(512),
    "timestamp_details" TIMESTAMP
);

CREATE TABLE "employee_details" (
    "employeeid"    INT,
    "phone_number"  INT,
    "isdefault"     VARCHAR(512)
);

------------------------------------------------------------
-- Insert Data
------------------------------------------------------------
INSERT INTO "employee_checkin_details" VALUES ('1000', 'login',  '2023-06-16 01:00:15.34');
INSERT INTO "employee_checkin_details" VALUES ('1000', 'login',  '2023-06-16 02:00:15.34');
INSERT INTO "employee_checkin_details" VALUES ('1000', 'login',  '2023-06-16 03:00:15.34');
INSERT INTO "employee_checkin_details" VALUES ('1000', 'logout', '2023-06-16 12:00:15.34');
INSERT INTO "employee_checkin_details" VALUES ('1001', 'login',  '2023-06-16 01:00:15.34');
INSERT INTO "employee_checkin_details" VALUES ('1001', 'login',  '2023-06-16 02:00:15.34');
INSERT INTO "employee_checkin_details" VALUES ('1001', 'login',  '2023-06-16 03:00:15.34');
INSERT INTO "employee_checkin_details" VALUES ('1001', 'logout', '2023-06-16 12:00:15.34');

INSERT INTO "employee_details" VALUES ('1001', '9999', 'false');
INSERT INTO "employee_details" VALUES ('1001', '1111', 'false');
INSERT INTO "employee_details" VALUES ('1001', '2222', 'true');
INSERT INTO "employee_details" VALUES ('1003', '3333', 'false');

------------------------------------------------------------
-- Input Data
------------------------------------------------------------
"employeeid","entry_details","timestamp_details"
1000,login,2023-06-16 01:00:15.34
1000,login,2023-06-16 02:00:15.34
1000,login,2023-06-16 03:00:15.34
1000,logout,2023-06-16 12:00:15.34
1001,login,2023-06-16 01:00:15.34
1001,login,2023-06-16 02:00:15.34
1001,login,2023-06-16 03:00:15.34
1001,logout,2023-06-16 12:00:15.34

"employeeid","phone_number","isdefault"
1001,9999,false
1001,1111,false
1001,2222,true
1003,3333,false


------------------------------------------------------------
-- Required Output
------------------------------------------------------------
"employeeid","phone_number","totalentry","totallogin","totallogout","lastlogin","lastlogout"
1000,,4,3,1,2023-06-16 03:00:15.34,2023-06-16 12:00:15.34
1001,2222,4,3,1,2023-06-16 03:00:15.34,2023-06-16 12:00:15.34


-- solution steps

-- Step 1:
-- Aggregate employee_checkin_details per employeeid to get
-- totalentry, totallogin, totallogout, lastlogin, lastlogout.

-- Step 2:
-- Left join the aggregated result to employee_details,
-- filtered to isdefault = 'true', to attach the default phone number.
-- (Aggregate first, then join -> smaller join, and safe even if
-- isdefault could ever match more than one row per employee.)


------------------------------------------------------------
-- SQL Solution
------------------------------------------------------------
with emp_summary as (
    select
        employeeid,
        count(*) as totalentry,
        sum(case when entry_details = 'login'  then 1 else 0 end) as totallogin,
        sum(case when entry_details = 'logout' then 1 else 0 end) as totallogout,
        max(case when entry_details = 'login'  then timestamp_details else null end) as lastlogin,
        max(case when entry_details = 'logout' then timestamp_details else null end) as lastlogout
    from employee_checkin_details
    group by employeeid
)
select
    a.employeeid,
    b.phone_number,
    a.totalentry,
    a.totallogin,
    a.totallogout,
    a.lastlogin,
    a.lastlogout
from emp_summary a
left join employee_details b
    on a.employeeid = b.employeeid
   and b.isdefault = 'true';


-- alternative solution (join first, then aggregate)
select
    a.employeeid,
    b.phone_number,
    count(*) as totalentry,
    sum(case when a.entry_details = 'login'  then 1 else 0 end) as totallogin,
    sum(case when a.entry_details = 'logout' then 1 else 0 end) as totallogout,
    max(case when a.entry_details = 'login'  then a.timestamp_details else null end) as lastlogin,
    max(case when a.entry_details = 'logout' then a.timestamp_details else null end) as lastlogout
from employee_checkin_details a
left join employee_details b
    on a.employeeid = b.employeeid
   and b.isdefault = 'true'
group by a.employeeid, b.phone_number;
