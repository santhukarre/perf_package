from appium import webdriver
import datetime

seq_read_result = ""
seq_write_result = ""
rand_read_result = ""
sql_insert_result = ""
sql_update_result = ""
sql_delete_result = ""

def insert_androbench_result(xindus_db_conn, run_id):
    global seq_read_result, seq_write_result, rand_read_result, sql_insert_result, sql_update_result, sql_delete_result
    xindus_db_cursor = xindus_db_conn.cursor()
    result_id = '1' # It has to be fetched from db, and +1 has to be the result_id

    benchmark_rslt_sql = "INSERT INTO BENCHMARK_RESULT(RUN_ID, ID, RESULT_ID) VALUES (%s,%s,%s)"
    benchmark_rslt_val = [
        (run_id,'3', result_id),     # 3 is the ANDROBENCH_TOOL_ID
    ]
    xindus_db_cursor.executemany(benchmark_rslt_sql, benchmark_rslt_val)
    xindus_db_cursor.commit()

    androbench_sql = "INSERT INTO ANDROBENCH_RESULT(RESULT_ID, KPI_ID,VALUE) VALUES (%s,%s,%s)"
    androbench_val = [
        (result_id,'1', seq_read_result),
        (result_id,'1', seq_write_result),
        (result_id,'1', rand_read_result),
        (result_id,'2', sql_insert_result),
        (result_id,'2', sql_update_result),
        (result_id,'2', sql_delete_result),
    ]
    xindus_db_cursor.executemany(androbench_sql, androbench_val)
    xindus_db_cursor.commit()

def get_androdben_results(appium_web_driver, xindus_db_conn, run_id):
    # Click on Results Button.
    seq_read_results_element = appium_web_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TabHost/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.ListView/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.TextView[2]')
    seq_write_results_element = appium_web_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TabHost/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.ListView/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.TextView[2]')
    rand_read_results_element = appium_web_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TabHost/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.ListView/android.widget.FrameLayout[3]/android.widget.LinearLayout/android.widget.TextView[2]')
    rand_write_results_element = appium_web_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TabHost/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.ListView/android.widget.FrameLayout[4]/android.widget.LinearLayout/android.widget.TextView[2]')
    sql_insert_results_element = appium_web_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TabHost/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.ListView/android.widget.FrameLayout[5]/android.widget.LinearLayout/android.widget.TextView[2]')
    sql_update_results_element = appium_web_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TabHost/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.ListView/android.widget.FrameLayout[6]/android.widget.LinearLayout/android.widget.TextView[2]')
    sql_delete_results_element = appium_web_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TabHost/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.ListView/android.widget.FrameLayout[7]/android.widget.LinearLayout/android.widget.TextView[2]')
    print('seq_read_results_element= ', seq_read_results_element.text)
    print('seq_write_results_element= ', seq_write_results_element.text)
    print('rand_read_results_element= ', rand_read_results_element.text)
    print('sql_insert_results_element= ', sql_insert_results_element.text)
    print('sql_update_results_element= ', sql_update_results_element.text)
    print('sql_delete_results_element= ', sql_delete_results_element.text)
    insert_androbench_result(xindus_db_conn, run_id)

def run_androbench(adb_id, xindus_db_conn, run_id):
    print("Running Androbench on device with adb_id =", adb_id)
    desired_cap = {
        "deviceName": adb_id,
        "platformName": "android",
        "appPackage": "com.andromeda.androbench2",
        "appActivity": "main",
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

    #    appium_web_driver.implicitly_wait(30)
#    appium_web_driver.find_element_by_id('com.android.permissioncontroller:id/continue_button').click();
#    appium_web_driver.implicitly_wait(30)
#    appium_web_driver.find_element_by_id('android:id/button1').click();
    appium_web_driver.implicitly_wait(30)
    # on Androbench Run All Benchmarks Button.

    START_DATE = datetime.datetime.now().date()
    START_TIME = datetime.datetime.now().time()
    print(START_DATE)
    print(START_TIME)

    appium_web_driver.find_element_by_id('com.andromeda.androbench2:id/btnStartingBenchmarking').click();

    appium_web_driver.implicitly_wait(30)

    # Click on Yes Button.
    appium_web_driver.find_element_by_id('android:id/button1').click();

    appium_web_driver.implicitly_wait(120)

    # Click on Cancel Button for 'Do you want to send results to server for research purpose'
    appium_web_driver.find_element_by_id('android:id/button2').click();

    # Click on Results Button.
    results_element = appium_web_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TabHost/android.widget.LinearLayout/android.widget.TabWidget/android.widget.LinearLayout[2]')
    results_element.click()
    END_DATE = datetime.datetime.now().date()
    END_TIME = datetime.datetime.now().time()
    print(END_DATE)
    print(END_TIME)
    Duration = END_TIME - START_TIME
    print(Duration)
    get_androdben_results(appium_web_driver, xindus_db_conn, run_id)
