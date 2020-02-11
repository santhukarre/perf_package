def get_run_id(xindus_db_conn):
  run_id = 2  # it has to be fetched from db, and whatever fetched from db + 1 has to be returned.
  return run_id

def Insert_Run_data():
    mycursor = mydb.cursor()
    global START_DATE,START_TIME,END_DATE,END_TIME,Mode
    Mode='perf';

    sql4 = "INSERT INTO RUN(START_DATE,START_TIME,END_DATE,END_TIME,MODE) VALUES(%s,%s,%s,%s,%s)"
    val4 = [
        (START_DATE,START_TIME,END_DATE,END_TIME,Mode),
    ]
    mycursor.executemany(sql4,val4)
    mydb.commit()
