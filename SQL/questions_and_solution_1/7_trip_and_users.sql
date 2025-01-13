-- question statement
    -- Write a SQL query to find the cancellation rate of requests with unbanned users
    --(both client and driver must not be banned) each day between "2013-10-01" and "2013-10-03"
    --Round cancellation rate to two decimal points.

    --The cancellation rate is computed by dividing the number of cancelled (by client or driver)
    --requests with unbanned users by the total number of requests with unbanned users on that day.

-- create table statement
Create table  Trips (id int, client_id int, driver_id int, city_id int, status varchar(50), request_at varchar(50));

Create table Users (users_id int, banned varchar(50), role varchar(50));

-- Insert data
    INSERT INTO Trips (id, client_id, driver_id, city_id, status, request_at)
    VALUES
        ('1', '1', '10', '1', 'completed', '2013-10-01'),
        ('2', '2', '11', '1', 'cancelled_by_driver', '2013-10-01'),
        ('3', '3', '12', '6', 'completed', '2013-10-01'),
        ('4', '4', '13', '6', 'cancelled_by_client', '2013-10-01'),
        ('5', '1', '10', '1', 'completed', '2013-10-02'),
        ('6', '2', '11', '6', 'completed', '2013-10-02'),
        ('7', '3', '12', '6', 'completed', '2013-10-02'),
        ('8', '2', '12', '12', 'completed', '2013-10-03'),
        ('9', '3', '10', '12', 'completed', '2013-10-03'),
        ('10', '4', '13', '12', 'cancelled_by_driver', '2013-10-03');


    INSERT INTO Users (users_id, banned, role)
    VALUES
        ('1', 'No', 'client'),
        ('2', 'Yes', 'client'),
        ('3', 'No', 'client'),
        ('4', 'No', 'client'),
        ('10', 'No', 'driver'),
        ('11', 'No', 'driver'),
        ('12', 'No', 'driver'),
        ('13', 'No', 'driver');

-- Input data
--table 1 trips:
"id","client_id","driver_id","city_id","status","request_at"
1,1,10,1,completed,"2013-10-01"
2,2,11,1,cancelled_by_driver,"2013-10-01"
3,3,12,6,completed,"2013-10-01"
4,4,13,6,cancelled_by_client,"2013-10-01"
5,1,10,1,completed,"2013-10-02"
6,2,11,6,completed,"2013-10-02"
7,3,12,6,completed,"2013-10-02"
8,2,12,12,completed,"2013-10-03"
9,3,10,12,completed,"2013-10-03"
10,4,13,12,cancelled_by_driver,"2013-10-03"

--table 2 users:
"users_id","banned","role"
1,No,client
2,Yes,client
3,No,client
4,No,client
10,No,driver
11,No,driver
12,No,driver
13,No,driver

-- Required Output
"request_at","total_trip_count","cancelled_trip","cancellation_rate"
"2013-10-01",3,1,0.33333333333333333333
"2013-10-02",2,0,0.00000000000000000000
"2013-10-03",2,1,0.50000000000000000000

--Solution steps
    --join the trip table with users table twice and filter out the band user
    --once on the client id with user is
    --second driver id with user id
    -- from this temporary table get the sum of total trips and cancelled trips
    -- divide the cancelled trips with completed trips to get cancellation rate
    -- multiply the answer or one of the column by 1.0 to convert the cancellation rate to decimal


--SQL solution1
with trips_with_user_driver_banned_flag as
	(select id as trip_id,
		client_id,
		driver_id,
		city_id,
		status,
		request_at,
		b.banned as user_banned_flag,
		c.banned as driver_banned_flag
	from trips a
	inner join users b on a.client_id = b.users_id and b.banned = 'No'
	inner join users c on a.driver_id = c.users_id and c.banned = 'No')

select
	request_at,
	count(status) as total_trip_count,
	sum(case when status != 'completed' then 1 else 0 end) as cancelled_trip,
	(sum(case when status != 'completed' then 1 else 0 end) * 1.0/ count(status)) as cancellation_rate
from trips_with_user_driver_banned_flag
group by request_at
order by request_at
--Additional logics

