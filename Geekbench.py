from appium import webdriver
import time

def store_geekbench_result(xindus_db_conn, result_id_list):
    xindus_db_cursor = xindus_db_conn.cursor()
    sql_read = "select * from GEEKBENCH_RESULT"
    xindus_db_cursor.execute(sql_read)
    data = xindus_db_cursor.fetchall()
    print("Total number of rows is ", xindus_db_cursor.rowcount)
    file = open("results.csv", "w+")
    file.write("Result id,single_core_element,multi_core_element,opencl_score_element")
    file.write("\n")
    for row in data:
       file.write(str(row[0]))
       file.write(",")
       file.write(str(row[1]))
       file.write(",")
       file.write(str(row[2]))
       file.write(",")
       file.write(str(row[3]))
       file.write("\n")


def get_geekbench_result_id(xindus_db_conn):
    xindus_db_cursor = xindus_db_conn.cursor()
    sql_read = "select MAX(RESULT_ID) from GEEKBENCH_RESULT"
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

def insert_geekbench_result(xindus_db_conn, run_id):
    global single_core_element,multi_core_element,opencl_score_element


    xindus_db_cursor = xindus_db_conn.cursor()
    result_id = get_geekbench_result_id(xindus_db_conn)

    benchmark_rslt_sql = "INSERT INTO BENCHMARK_RESULT(RUN_ID, ID, RESULT_ID) VALUES (%s,%s,%s)"
    benchmark_rslt_val = [
        (run_id,'3', result_id),     # 3 is the ANDROBENCH_TOOL_ID
    ]
    xindus_db_cursor.executemany(benchmark_rslt_sql, benchmark_rslt_val)
    xindus_db_conn.commit()

    geekbench_sql = "INSERT INTO GEEKBENCH_RESULT(RESULT_ID,SINGLE_CORE_ELEMENT,MULTI_CORE_ELEMENT,OPENCL_SCORE_ELEMENT) VALUES (%s,%s,%s,%s)"
    geekbench_val = [
        (result_id,single_core_element,multi_core_element,opencl_score_element),
    ]
    xindus_db_cursor.executemany(geekbench_sql,geekbench_val)
    xindus_db_conn.commit()

def run_geekbench(adb_id,xindus_db_conn, run_id):
    print("Running Geekbench on device with adb_id =", adb_id)
    geekbench_desired_cap = {
        "deviceName": adb_id,
        "platformName": "android",
        "appPackage": "com.primatelabs.geekbench5",
        "appActivity": "com.primatelabs.geekbench.HomeActivity",
        "noReset": True,
        #"keep_alive": True,
        "newCommandTimeout": 200,
        "automationName": "UiAutomator1"
    }
    geekbench_driver = webdriver.Remote("http://localhost:4723/wd/hub", geekbench_desired_cap)
    geekbench_driver.implicitly_wait(30)

    # Click the Accept button Button
    #geekbench_driver.find_element_by_id('android:id/button1').click()
    #geekbench_driver.implicitly_wait(30)

    # Click the RUN CPU Benchmark Button
    geekbench_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.support.v4.widget.DrawerLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.support.v4.view.ViewPager/android.widget.ScrollView/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.Button').click()
    geekbench_driver.implicitly_wait(800)
    #time.sleep(120)

    # get the Single core, Multi Core Results
    single_core_element = geekbench_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.support.v7.app.ActionBar.Tab[2]/android.widget.TextView')
    multi_core_element = geekbench_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.support.v4.view.ViewPager/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[2]/android.view.View[3]')
    print('single_core_element= ', single_core_element.text)
    print('multi_core_element= ', multi_core_element.text)

    # Click the Back Button
    geekbench_driver.implicitly_wait(10)
    nav_back_element = geekbench_driver.find_element_by_xpath('//android.widget.ImageButton[@content-desc="Navigate up"]')
    nav_back_element.click()

    # Click the COMPUTE Button
    geekbench_driver.implicitly_wait(10)
    compute_element = geekbench_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.support.v4.widget.DrawerLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.support.v7.app.ActionBar.Tab[2]')
    compute_element.click()

    # Click the RUN COMPUTE Tests Button
    geekbench_driver.find_element_by_id('com.primatelabs.geekbench5:id/runComputeBenchmark').click()
    geekbench_driver.implicitly_wait(1800)
    #time.sleep(1200)

    opencl_score_element = geekbench_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.support.v4.view.ViewPager/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[2]/android.view.View[1]')
    print('opencl_score_element= ', opencl_score_element.text)
    nav_back_element = geekbench_driver.find_element_by_xpath('//android.widget.ImageButton[@content-desc="Navigate up"]')
    nav_back_element.click()
    insert_geekbench_result(xindus_db_conn, run_id)
