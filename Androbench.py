from appium import webdriver
from Run import insert_runid
import time
import datetime
seq_read_results=""
seq_write_results=""
rand_read_results=""
rand_write_results=""
sql_insert_results=""
sql_update_results=""
sql_delete_results=""

def wait_for_element(appium_web_driver, secs, element_id):
   each_iteration_sleep = 50
   iteration = (int)(secs/each_iteration_sleep)
   for i in range(1, iteration):
        appium_web_driver.implicitly_wait(secs)
        time.sleep(5)
   # Click on Cancel Button for 'Do you want to send results to server for research purpose'
   appium_web_driver.find_element_by_id(element_id).click()

def store_androbench_result(xindus_db_conn, result_id_list):
    xindus_db_cursor = xindus_db_conn.cursor()
    sql_read = "select * from ANDROBENCH_RESULT"
    xindus_db_cursor.execute(sql_read)
    data = xindus_db_cursor.fetchall()
    print("Total number of rows is ", xindus_db_cursor.rowcount)
    file = open("results.csv", "w+")
    file.write("Result id,Seq Read,Seq Write,Rand Read,Rand Write,SQL Insert,SQL Update,SQL Delete")
    file.write("\n")
    for row in data:
       file.write(str(row[0]))
       file.write(",")
       file.write(str(row[1]))
       file.write(",")
       file.write(str(row[2]))
       file.write(",")
       file.write(str(row[3]))
       file.write(",")
       file.write(str(row[4]))
       file.write(",")
       file.write(str(row[5]))
       file.write(",")
       file.write(str(row[6]))
       file.write(",")
       file.write(str(row[7]))
       file.write("\n")

def get_androbench_result_id(xindus_db_conn):
    xindus_db_cursor = xindus_db_conn.cursor()
    sql_read = "select MAX(RESULT_ID) from ANDROBENCH_RESULT"
    xindus_db_cursor.execute(sql_read)
    data = xindus_db_cursor.fetchall()
    print("Total number of rows is ", xindus_db_cursor.rowcount)
    for row in data:
        result_id = row[0]
        print("row [0] = ", row[0])
    if(result_id == None):
        result_id = 1
    else:
        print("result_id = ", result_id)
        result_id = result_id + 1
    return result_id

def insert_androbench_result(xindus_db_conn, run_id):
    global seq_read_result, seq_write_result, rand_read_result, rand_write_result, sql_insert_result, sql_update_result, sql_delete_result

    seq_read_result = seq_read_result.split(" ")[0]
    seq_write_result = seq_write_result.split(" ")[0]
    rand_read_result = rand_read_result.split(" ")[0]
    rand_write_result = rand_write_result.split(" ")[0]
    sql_insert_result = sql_insert_result.split(" ")[0]
    sql_update_result = sql_update_result.split(" ")[0]
    sql_delete_result = sql_delete_result.split(" ")[0]

    print('seq_read_result = ',seq_read_result)
    print('seq_write_result = ', seq_write_result)
    print('rand_read_result = ', rand_read_result)
    print('rand_write_result = ', rand_write_result)
    print('sql_insert_result = ', sql_insert_result)
    print('sql_update_result = ', sql_update_result)
    print('sql_delete_result = ', sql_delete_result)
	
    xindus_db_cursor = xindus_db_conn.cursor()
    result_id = get_androbench_result_id(xindus_db_conn)

    benchmark_rslt_sql = "INSERT INTO BENCHMARK_RESULT(RUN_ID, ID, RESULT_ID) VALUES (%s,%s,%s)"
    benchmark_rslt_val = [
        (run_id,'3', result_id),     # 3 is the ANDROBENCH_TOOL_ID
    ]
    xindus_db_cursor.executemany(benchmark_rslt_sql, benchmark_rslt_val)
    xindus_db_conn.commit()

    androbench_sql = "INSERT INTO ANDROBENCH_RESULT(RESULT_ID, SEQ_READ, SEQ_WRITE, RAND_READ, RAND_WRITE, SQL_INSERT, SQL_UPDATE, SQL_DELETE) VALUES (%s,%s,%s,%s,%s,%s,%s)"
    androbench_val = [
        (result_id,seq_read_result, seq_write_result, rand_read_result, rand_write_result, sql_insert_result, sql_update_result, sql_delete_result),
    ]
    xindus_db_cursor.executemany(androbench_sql, androbench_val)
    xindus_db_conn.commit()

def get_androdben_results(appium_web_driver, xindus_db_conn, run_id):
    global seq_read_result, seq_write_result, rand_read_result,rand_write_result, sql_insert_result, sql_update_result, sql_delete_result

    # Click on Results Button.
    seq_read_results_element = appium_web_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TabHost/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.ListView/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.TextView[2]')
    seq_write_results_element = appium_web_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TabHost/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.ListView/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.TextView[2]')
    rand_read_results_element = appium_web_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TabHost/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.ListView/android.widget.FrameLayout[3]/android.widget.LinearLayout/android.widget.TextView[2]')
    rand_write_results_element = appium_web_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TabHost/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.ListView/android.widget.FrameLayout[4]/android.widget.LinearLayout/android.widget.TextView[2]')
    sql_insert_results_element = appium_web_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TabHost/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.ListView/android.widget.FrameLayout[5]/android.widget.LinearLayout/android.widget.TextView[2]')
    sql_update_results_element = appium_web_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TabHost/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.ListView/android.widget.FrameLayout[6]/android.widget.LinearLayout/android.widget.TextView[2]')
    sql_delete_results_element = appium_web_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TabHost/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.ListView/android.widget.FrameLayout[7]/android.widget.LinearLayout/android.widget.TextView[2]')


    seq_read_result = seq_read_results_element.text
    seq_write_result = seq_write_results_element.text
    rand_read_result = rand_read_results_element.text
    rand_write_result = rand_write_results_element.text
    sql_insert_result = sql_insert_results_element.text
    sql_update_result = sql_update_results_element.text
    sql_delete_result = sql_delete_results_element.text


    insert_androbench_result(xindus_db_conn, run_id)

def run_androbench(adb_id, xindus_db_conn, run_id):
    print("Running Androbench on device with adb_id =", adb_id)
    desired_cap = {
        "deviceName": adb_id,
        "platformName": "android",
        "appPackage": "com.andromeda.androbench2",
        "appActivity": "main",
        "automationName": "UiAutomator2"
    }
    appium_web_driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
    newVersionDevice = False

    if (newVersionDevice):
        appium_web_driver.implicitly_wait(20)
        continue_btn = appium_web_driver.find_element_by_id('com.android.permissioncontroller:id/continue_button')
        continue_btn.click()
        appium_web_driver.implicitly_wait(20)
        warning_btn = appium_web_driver.find_element_by_id('android:id/button1')
        warning_btn.click()

    appium_web_driver.implicitly_wait(30)
    # on Androbench Run All Benchmarks Button.

    appium_web_driver.find_element_by_id('com.andromeda.androbench2:id/btnStartingBenchmarking').click();

    appium_web_driver.implicitly_wait(30)

    # Click on Yes Button.
    appium_web_driver.find_element_by_id('android:id/button1').click()

    #appium_web_driver.implicitly_wait(140)

    wait_for_element(appium_web_driver, 240, 'android:id/button2')
    # Click on Cancel Button for 'Do you want to send results to server for research purpose'

    # Click on Results Button.
    results_element = appium_web_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TabHost/android.widget.LinearLayout/android.widget.TabWidget/android.widget.LinearLayout[2]')
    results_element.click()
    #Duration = END_TIME - START_TIME
    #print(Duration)
    get_androdben_results(appium_web_driver, xindus_db_conn, run_id)
