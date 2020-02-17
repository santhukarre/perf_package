import datetime

START_DATE = ""
START_TIME = ""
END_DATE = ""
END_TIME = ""
run_id = ""
def update_run_start_time():
    global  START_DATE, START_TIME
    START_DATE = datetime.datetime.now().date()
    START_TIME = datetime.datetime.now().time()
    print(START_DATE)
    print(START_TIME)

def update_run_end_time():
    global  END_DATE, END_TIME
    END_DATE = datetime.datetime.now().date()
    END_TIME = datetime.datetime.now().time()
    print(END_DATE)
    print(END_TIME)

def update_run_start_end_time():
    print("START_DATE = ", START_DATE , "END_DATE = ", END_DATE)

def get_run_id(xindus_db_conn):
    xindus_db_cursor = xindus_db_conn.cursor()
    sql_read = "select MAX(RUN_ID) from RUN"
    xindus_db_cursor.execute(sql_read)
    data = xindus_db_cursor.fetchall()
    print("Total number of rows is ", xindus_db_cursor.rowcount)
    for row in data:
        run_id = row[0]
        print("row [0] = ", row[0])
    if(run_id == None):
        run_id = 1
    else:
        print("run_id = ", run_id)
        run_id = run_id + 1
    return run_id

def insert_runid(xindus_db_conn,run_id):
    xindus_db_cursor = xindus_db_conn.cursor()
    run_sql = "INSERT INTO RUN(RUN_ID) VALUES(%s)"
    run_val = [
        (run_id)
    ]
    xindus_db_cursor.execute(run_sql,run_val)
    xindus_db_conn.commit()

def insert_run_data(xindus_db_conn, run_id):
    xindus_db_cursor = xindus_db_conn.cursor()
    global START_DATE,START_TIME,END_DATE,END_TIME,Mode
    Mode='perf';

    run_data_sql = "Update RUN SET START_DATE ='" + str(START_DATE) + "'," +\
                    "START_TIME ='" + str(START_TIME) + "'," +\
                    "END_DATE ='" + str(END_DATE) + "'," + \
                    "END_TIME ='" + str(END_TIME) + "'," +\
                    "MODE ='" + Mode + "'"\
                    "where RUN_ID = '" + str(run_id) +"'"
    print("run_id = ", run_id)
    print("run_data_sql = ", run_data_sql)
    xindus_db_cursor.execute(run_data_sql)
    xindus_db_conn.commit()
