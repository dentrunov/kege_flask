START TRANSACTION;

CREATE TABLE groups (
  group_id SERIAL PRIMARY KEY,
  gr_name varchar(20) NOT NULL,
  group_owner int NOT NULL REFERENCES users (user_id) ON DELETE CASCADE,
  stud_year varchar(20) NOT NULL
);

CREATE TABLE parents (
  link_id SERIAL PRIMARY KEY,
  parent_id int NOT NULL,
  child_id int NOT NULL
);

CREATE TABLE tests (
  test_id SERIAL PRIMARY KEY,
  user_id int NOT NULL REFERENCES users (user_id) ON DELETE NO ACTION,
  time_added timestamp NOT NULL,
  path varchar(20) NOT NULL,
  test_name varchar(40) NOT NULL,
  task_1 text NOT NULL,
  task_2 varchar NOT NULL,
  task_3 int NOT NULL,
  task_4 text NOT NULL,
  task_5 text NOT NULL,
  task_6 int NOT NULL,
  task_7 int NOT NULL,
  task_8 int NOT NULL,
  task_9 int NOT NULL,
  task_10 int NOT NULL,
  task_11 int NOT NULL,
  task_12 int NOT NULL,
  task_13 int NOT NULL,
  task_14 int NOT NULL,
  task_15 int NOT NULL,
  task_16 text NOT NULL,
  task_17 varchar(11) NOT NULL,
  task_18 varchar(11) NOT NULL,
  task_19 int NOT NULL,
  task_20 varchar(11) NOT NULL,
  task_21 varchar(11) NOT NULL,
  task_22 int NOT NULL,
  task_23 int NOT NULL,
  task_24 int NOT NULL,
  task_25 varchar(50) NOT NULL,
  task_26 varchar(200) NOT NULL,
  task_27 varchar(20) NOT NULL,
  test_hidden BOOLEAN DEFAULT True,
  test_starts_number INT DEFAULT 0,
  test_avg_result INT DEFAULT 0
);

CREATE TABLE test_started (
  try_id SERIAL PRIMARY KEY,
  user_id int NOT NULL REFERENCES users (user_id) ON DELETE CASCADE,
  test_id int NOT NULL REFERENCES test (test_id) ON DELETE CASCADE,
  time_start timestamp NOT NULL,
  time_left int NOT NULL,
  time_end timestamp,
  ended boolean,
  test_name text NOT NULL,
  path varchar(64),
  task_1 varchar(64),
  task_2 varchar(64),
  task_3 int,
  task_4 int,
  task_5 int,
  task_6 int,
  task_7 int,
  task_8 int,
  task_9 int,
  task_10 int,
  task_11 int,
  task_12 int,
  task_13 int,
  task_14 int,
  task_15 int,
  task_16 text,
  task_17 varchar(11),
  task_18 varchar(11),
  task_19 int,
  task_20 varchar(11),
  task_21 varchar(11),
  task_22 int,
  task_23 int,
  task_24 int,
  task_25 varchar(50),
  task_26 varchar(200),
  task_27 varchar(50),
  primary_mark int,
  final_mark int
);

CREATE TABLE users (
  user_id SERIAL PRIMARY KEY,
  username text NOT NULL,
  email text NOT NULL,
  role int NOT NULL,
  group_id int NOT NULL DEFAULT 1 REFERENCES groups ON DELETE SET DEFAULT,
  reg_time timestamp NOT NULL,
  last_visit_time timestamp NOT NULL,
  user_ varchar(64),
  password_hash varchar(128) NOT NULL,
  parent_email text
);

CREATE TABLE videos (
  v_id SERIAL PRIMARY KEY,
  user_id int NOT NULL REFERENCES users (user_id) ON DELETE NO ACTION,
  v_link text,
  v_name text,
  v_text text,
  v_date timestamp
);

CREATE TABLE news_all (
  news_id SERIAL PRIMARY KEY,
  news_user_id int NOT NULL REFERENCES users (user_id) ON DELETE CASCADE,
  news_title text,
  news_text text,
  new_date timestamp, news_show_group int
);

CREATE TABLE restore_pwd (
id SERIAL PRIMARY KEY,
user_id integer NOT NULL REFERENCES users (user_id) ON DELETE NO ACTION,
time_added timestamp,
hash text);


COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
