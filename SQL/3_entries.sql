-- create table statement
create table entries ( 
name varchar(20),
address varchar(20),
email varchar(20),
floor int,
resources varchar(10));

-- Insert data
INSERT INTO entries ("name",address,email,floor,resources) VALUES
	 ('A','Bangalore','A@gmail.com',1,'CPU'),
	 ('A','Bangalore','A1@gmail.com',1,'CPU'),
	 ('A','Bangalore','A2@gmail.com',2,'DESKTOP'),
	 ('B','Bangalore','B@gmail.com',2,'DESKTOP'),
	 ('B','Bangalore','B1@gmail.com',2,'DESKTOP'),
	 ('B','Bangalore','B2@gmail.com',1,'MONITOR');

-- Input data
"name","address","email","floor","resources"
A,Bangalore,A@gmail.com,1,CPU
A,Bangalore,A1@gmail.com,1,CPU
A,Bangalore,A2@gmail.com,2,DESKTOP
B,Bangalore,B@gmail.com,2,DESKTOP
B,Bangalore,B1@gmail.com,2,DESKTOP
B,Bangalore,B2@gmail.com,1,MONITOR

-- Required Output
name, total_visti, most_visited_floor, resources_used
--Solution steps

--SQL solution1

--Aditional logics

