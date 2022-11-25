from local import *
from datetime import datetime

import psycopg2

conn = psycopg2.connect(dbname=db_name, user=db_username,
                        password=db_password, host=db_host)
cursor = conn.cursor()

cursor.execute('''
ALTER TABLE tests
  ALTER COLUMN task_1 TYPE varchar(50),
  ALTER COLUMN task_2 TYPE varchar(50),
  ALTER COLUMN task_3 TYPE varchar(50),
  ALTER COLUMN task_4 TYPE varchar(50),
  ALTER COLUMN task_5 TYPE varchar(50),
  ALTER COLUMN task_6 TYPE varchar(50),
  ALTER COLUMN task_7 TYPE varchar(50),
  ALTER COLUMN task_8 TYPE varchar(50),
  ALTER COLUMN task_9 TYPE varchar(50),
  ALTER COLUMN task_10 TYPE varchar(50),
  ALTER COLUMN task_11 TYPE varchar(50),
  ALTER COLUMN task_12 TYPE varchar(50),
  ALTER COLUMN task_13 TYPE varchar(50),
  ALTER COLUMN task_14 TYPE varchar(50),
  ALTER COLUMN task_15 TYPE varchar(50),
  ALTER COLUMN task_16 TYPE varchar(50),
  ALTER COLUMN task_17 TYPE varchar(50),
  ALTER COLUMN task_18 TYPE varchar(50),
  ALTER COLUMN task_19 TYPE varchar(50),
  ALTER COLUMN task_20 TYPE varchar(50),
  ALTER COLUMN task_21 TYPE varchar(50),
  ALTER COLUMN task_22 TYPE varchar(50),
  ALTER COLUMN task_23 TYPE varchar(50),
  ALTER COLUMN task_24 TYPE varchar(50),
  ALTER COLUMN task_25 TYPE varchar(50),
  ALTER COLUMN task_26 TYPE varchar(256),
  ALTER COLUMN task_27 TYPE varchar(50);

ALTER TABLE test_started 
  ALTER COLUMN task_1 TYPE varchar(50),
  ALTER COLUMN task_2 TYPE varchar(50),
  ALTER COLUMN task_3 TYPE varchar(50),
  ALTER COLUMN task_4 TYPE varchar(50),
  ALTER COLUMN task_5 TYPE varchar(50),
  ALTER COLUMN task_6 TYPE varchar(50),
  ALTER COLUMN task_7 TYPE varchar(50),
  ALTER COLUMN task_8 TYPE varchar(50),
  ALTER COLUMN task_9 TYPE varchar(50),
  ALTER COLUMN task_10 TYPE varchar(50),
  ALTER COLUMN task_11 TYPE varchar(50),
  ALTER COLUMN task_12 TYPE varchar(50),
  ALTER COLUMN task_13 TYPE varchar(50),
  ALTER COLUMN task_14 TYPE varchar(50),
  ALTER COLUMN task_15 TYPE varchar(50),
  ALTER COLUMN task_16 TYPE varchar(50),
  ALTER COLUMN task_17 TYPE varchar(50),
  ALTER COLUMN task_18 TYPE varchar(50),
  ALTER COLUMN task_19 TYPE varchar(50),
  ALTER COLUMN task_20 TYPE varchar(50),
  ALTER COLUMN task_21 TYPE varchar(50),
  ALTER COLUMN task_22 TYPE varchar(50),
  ALTER COLUMN task_23 TYPE varchar(50),
  ALTER COLUMN task_24 TYPE varchar(50),
  ALTER COLUMN task_25 TYPE varchar(50),
  ALTER COLUMN task_26 TYPE varchar(256),
  ALTER COLUMN task_27 TYPE varchar(50);''')

conn.commit()



cursor.close()
conn.close()
