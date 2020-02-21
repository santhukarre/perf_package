import subprocess
import datetime
import time

START_DATE = ""
START_TIME = ""
END_DATE = ""
END_TIME = ""
run_id = ""
report_file_name = "Xindus_PerfReport.xlsx"

def is_element_found(appium_web_driver, sec, element_id):
    try:
        print("sleeping for ", sec, " seconds to find the element")
        appium_web_driver.implicitly_wait(sec)
        found_element_id = appium_web_driver.find_element_by_id(element_id)
        return True
    except:
        print("exception occured")
        return False

found_element_id = ""
def wait_for_element(appium_web_driver, secs, element_id):
   global  found_element_id
   each_iteration_sleep = 50
   iterations = (int)(secs/each_iteration_sleep)
   print("Total iterations  = ", iterations)
   for i in range(1, iterations):
        print("iteration no. = ", i )
        element_found = is_element_found(appium_web_driver, each_iteration_sleep, element_id)
        if(element_found == True):
            global  found_element_id
            found_element_id = appium_web_driver.find_element_by_id(element_id)
            break
        if(element_found == False):
            print("Sleeping explicilty for 5 seconds")
            time.sleep(5)
   return found_element_id

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

def pull_screenshots(run_id, fileName, dest):
    screenshot_cmd = "adb shell screencap -p /sdcard/" + fileName + "_" + str(run_id) + ".png"
    p = subprocess.Popen(screenshot_cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    dest = dest.replace("\\", "\\\\")
    pull_cmd = "adb pull -p -a  /sdcard/" + fileName + "_" + str(run_id) + ".png " + dest
    p = subprocess.Popen(pull_cmd,stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()