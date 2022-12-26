from local import *
from datetime import datetime

import psycopg2

conn = psycopg2.connect(host=db_host, database=db_name, user=db_username, password=db_password)
cursor = conn.cursor()


cursor.execute('''CREATE TABLE IF NOT EXISTS users (
  user_id SERIAL PRIMARY KEY,
  username text NOT NULL,
  email text NOT NULL,
  role int NOT NULL DEFAULT 0,
  
  reg_time timestamp NOT NULL,
  last_visit_time timestamp NOT NULL,
  user_ varchar(64),
  password_hash varchar(128) NOT NULL,
  parent_email varchar(64)
);''')

cursor.execute('''CREATE TABLE IF NOT EXISTS groups (
  group_id SERIAL PRIMARY KEY,
  gr_name varchar(20) NOT NULL,
  group_owner int NOT NULL REFERENCES users (user_id) ON DELETE CASCADE,
  stud_year varchar(20) NOT NULL
);''')

cursor.execute('''ALTER TABLE IF EXISTS users
    ADD COLUMN group_id int DEFAULT 1 REFERENCES groups(group_id) ON DELETE SET DEFAULT''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS tests (
  test_id SERIAL PRIMARY KEY,
  user_id int NOT NULL REFERENCES users (user_id) ON DELETE NO ACTION,
  time_added timestamp NOT NULL,
  path varchar(50) NOT NULL,
  test_name varchar(50) NOT NULL,
  task_1 varchar(256),
  task_2 varchar(256),
  task_3 varchar(256),
  task_4 varchar(256),
  task_5 varchar(256),
  task_6 varchar(256),
  task_7 varchar(256),
  task_8 varchar(256),
  task_9 varchar(256),
  task_10 varchar(256),
  task_11 varchar(256),
  task_12 varchar(256),
  task_13 varchar(256),
  task_14 varchar(256),
  task_15 varchar(256),
  task_16 varchar(256),
  task_17 varchar(256),
  task_18 varchar(256),
  task_19 varchar(256),
  task_20 varchar(256),
  task_21 varchar(256),
  task_22 varchar(256),
  task_23 varchar(256),
  task_24 varchar(256),
  task_25 varchar(256),
  task_26 varchar(256),
  task_27 varchar(256),
  test_hidden BOOLEAN DEFAULT True,
  test_starts_number INT DEFAULT 0,
  test_avg_result INT DEFAULT 0
);''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS test_started (
  try_id SERIAL PRIMARY KEY,
  user_id int NOT NULL REFERENCES users (user_id) ON DELETE CASCADE,
  test_id int NOT NULL REFERENCES tests (test_id) ON DELETE CASCADE,
  time_start timestamp NOT NULL,
  time_left int NOT NULL,
  time_end timestamp,
  ended boolean,
  test_name text NOT NULL,
  path varchar(64),
  task_1 varchar(256),
  task_2 varchar(256),
  task_3 varchar(256),
  task_4 varchar(256),
  task_5 varchar(256),
  task_6 varchar(256),
  task_7 varchar(256),
  task_8 varchar(256),
  task_9 varchar(256),
  task_10 varchar(256),
  task_11 varchar(256),
  task_12 varchar(256),
  task_13 varchar(256),
  task_14 varchar(256),
  task_15 varchar(256),
  task_16 varchar(256),
  task_17 varchar(256),
  task_18 varchar(256),
  task_19 varchar(256),
  task_20 varchar(256),
  task_21 varchar(256),
  task_22 varchar(256),
  task_23 varchar(256),
  task_24 varchar(256),
  task_25 varchar(256),
  task_26 varchar(256),
  task_27 varchar(256),
  primary_mark int,
  final_mark int
);''')


cursor.execute('''CREATE TABLE IF NOT EXISTS videos (
  v_id SERIAL PRIMARY KEY,
  user_id int NOT NULL REFERENCES users (user_id) ON DELETE NO ACTION,
  v_link varchar(64),
  v_name varchar(64),
  v_text varchar(64),
  v_date timestamp
);''')

cursor.execute('''CREATE TABLE IF NOT EXISTS news_all (
  news_id SERIAL PRIMARY KEY,
  news_user_id int NOT NULL REFERENCES users (user_id) ON DELETE CASCADE,
  news_title varchar(64),
  news_text varchar(64),
  new_date timestamp, news_show_group int
);''')

cursor.execute('''CREATE TABLE IF NOT EXISTS restore_pwd (
id SERIAL PRIMARY KEY,
user_id integer NOT NULL REFERENCES users (user_id) ON DELETE NO ACTION,
time_added timestamp,
hash varchar(256));''')

cursor.execute('''CREATE TABLE IF NOT EXISTS hw_tasks (
task_id SERIAL PRIMARY KEY,
task_text varchar(64),
task_user int NOT NULL REFERENCES users (user_id) ON DELETE NO ACTION,
task_answer varchar(64),
task_stat_true int,
task_stat_all int,
task_date timestamp);''')

cursor.execute('''CREATE TABLE IF NOT EXISTS subjects (
    subj_id SERIAL PRIMARY KEY,
    subj_name varchar(64)
);''')

cursor.execute('''CREATE TABLE IF NOT EXISTS themes (
theme_id SERIAL PRIMARY KEY,
theme_number int,
theme_name varchar(64),
theme_subject int NOT NULL REFERENCES subjects (subj_id) ON DELETE CASCADE
);''')

cursor.execute('''CREATE TABLE IF NOT EXISTS homeworks (
hw_id SERIAL PRIMARY KEY,
hw_user_id int NOT NULL REFERENCES users (user_id) ON DELETE NO ACTION,
hw_title varchar(64) NOT NULL,
hw_test_date timestamp NOT NULL,
hw_start_date timestamp,
hw_end_date timestamp,
hw_active BOOLEAN,
hw_task_1 int,
hw_task_2 int,
hw_task_3 int,
hw_task_4 int,
hw_task_5 int,
hw_task_6 int,
hw_task_7 int,
hw_task_8 int,
hw_task_9 int,
hw_task_10 int,
hw_task_11 int,
hw_task_12 int,
hw_task_13 int,
hw_task_14 int,
hw_task_15 int,
hw_task_16 int,
hw_task_17 int,
hw_task_18 int,
hw_task_19 int,
hw_task_20 int,
theme_number int,
theme_name varchar(64),
hw_users_ended int
);''')

cursor.execute('''CREATE TABLE IF NOT EXISTS hw_for_users (
hfu_hw_id int NOT NULL REFERENCES homeworks (hw_id) ON DELETE CASCADE,
hfu_user_id int NOT NULL REFERENCES users (user_id) ON DELETE NO ACTION,
hfu_hw_ended BOOLEAN,
hfu_hw_mark int,
hfu_hw_percentage int
);''')

conn.commit()

pwd = 'aaa'
conn.execute('''
    INSERT INTO users (username, email, role, group_id, reg_time, last_visit_time, user_, password_hash) 
    VALUES ({});''', ('admin', 'sgema@rambler.ru', 2, datetime.now, datetime.now, 'Админ', pwd))

conn.commit()
cursor.close()
conn.close()
