DROP DATABASE IF EXISTS honors;
CREATE DATABASE honors;
USE honors;

CREATE TABLE users
(
  ID INT NOT NULL,
  last_name VARCHAR(20) NOT NULL,
  first_name VARCHAR(20) NOT NULL,
  username VARCHAR(25) NOT NULL,
  admitted VARCHAR(20),
  code INT NOT NULL,
  type VARCHAR(20) DEFAULT 'student',
  password VARCHAR(5000)

);


CREATE TABLE checksheet
(
  ID INT NOT NULL,
  status VARCHAR(10),
  comments text,
  term VARCHAR(20),
  major VARCHAR(20),
  advisor VARCHAR(20),
  initial_essay DATE,
  co_curricular1 text,
  co_curricular1_date DATE,
  co_curricular2 text,
  co_curricular2_date DATE,
  co_curricular3 text,
  co_curricular3_date DATE,
  co_curricular4 text,
  co_curricular4_date DATE,
  co_curricular5 text,
  co_curricular5_date DATE,
  co_curricular6 text,
  co_curricular6_date DATE,
  co_curricular7 text,
  co_curricular7_date DATE,
  co_curricular8 text,
  co_curricular8_date DATE,
  fsem VARCHAR(10),
  fsem_date VARCHAR(20),
  hn_course1 VARCHAR(20),
  hn_course1_date VARCHAR(20),
  hn_course2 VARCHAR(10),
  hn_course2_date DATE,
  hn_course3 VARCHAR(10),
  hn_course3_date DATE,
  research_course VARCHAR(10),
  research_course_date DATE,
  capstone VARCHAR(10),
  capstone_date DATE,
  honr201 VARCHAR(10),
  honr201_date DATE,
  leadership VARCHAR(10),
  mentoring VARCHAR(10),
  honr_port1 VARCHAR(10),
  honr_port2 VARCHAR(10),
  honr_port3 VARCHAR(10),
  honr_port4 VARCHAR(10),
  exit_interview VARCHAR(10),
  PRIMARY KEY (ID)
  );
insert into users values (10, 'Shaikhah', 'sara', 'student', 'yes', 12, 'admin', 'welcome123');
insert into users values (11, 'Shaikhah', 'sara', 'admin', 'yes', 123, 'student', 'welcome123');