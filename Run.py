def get_run_id(xindus_db_conn):
    mycursor = xindus_db_conn.cursor()
    sql_read = "select MAX(RUN_ID) from RUN"
    mycursor.execute(sql_read)
    data = mycursor.fetchall()
    print("Total number of rows is ", mycursor.rowcount)
    for row in data:
        run_id = row[0]
        print(row[0])
        print(row[1])
    return run_id

def insert_run_data(xindus_db_conn):
    mycursor = xindus_db_conn.cursor()
    global START_DATE,START_TIME,END_DATE,END_TIME,Mode
    Mode='perf';

    sql4 = "INSERT INTO RUN(START_DATE,START_TIME,END_DATE,END_TIME,MODE) VALUES(%s,%s,%s,%s,%s)"
    val4 = [
        (START_DATE,START_TIME,END_DATE,END_TIME,Mode),
    ]
    mycursor.executemany(sql4,val4)
    xindus_db_conn.commit()
