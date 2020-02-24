from appium import webdriver
import time
from Run import pull_screenshots,report_file_name
import pandas as pd
from vincent.colors import brews
Single_core_element = ""
Multi_core_element= ""
Opencl_score_element= ""

report_file_name = "Xindus_PerfReport_Geekbench.xlsx"
def generateGeekbenchReport(xindus_db_conn):
    mycursor = xindus_db_conn.cursor()
    sql_read = "select * from GEEKBENCH_RESULT"
    mycursor.execute(sql_read)
    data = mycursor.fetchall()
    print("Total number of rows is ", mycursor.rowcount)
    i = 0
    iterations = []
    iterations_names = []
    for row in data:
        iteration={'Single_Core_element': row[1], 'Multi_Core_element': row[2], 'OpenGL_Score_element': row[3]}
        iterations.append(iteration)
        iterations_names.append('iteration '+ str(i))
        i = i +1
    data = iterations
    index = iterations_names
    # Create a Pandas dataframe from the data.
    df = pd.DataFrame(data,index=index)
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    sheet_name = 'Sheet4'
    writer = pd.ExcelWriter(report_file_name, engine='xlsxwriter')
    df.to_excel(writer, sheet_name=sheet_name)
    # Access the XlsxWriter workbook and worksheet objects from the dataframe.
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]
    # Create a chart object.
    chart = workbook.add_chart({'type': 'column'})
    # Configure the series of the chart from the dataframedata.
    for col_num in range(1, len(row)):
        print("col_num ", col_num)
        chart.add_series({
            'name':       ['Sheet4', 0, col_num],
            'categories': ['Sheet4', 1, 0, 1, 0],
            'values':     ['Sheet4', 1, col_num, 1, col_num],
            'fill':       {'color': brews['Set1'][col_num - 1]},
            'overlap':-10,})
    # Configure the chart axes.
    chart.set_x_axis({'name': 'Iterations'})
    chart.set_y_axis({'name': 'Score', 'major_gridlines': {'visible': False}})
    # Insert the chart into the worksheet.
    worksheet.insert_chart('H2', chart)
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
def is_element_found(appium_web_driver, sec, element_id):
    try:
        print("sleeping for ", sec, " seconds to find the element")
        appium_web_driver.implicitly_wait(sec)
        found_element_id = appium_web_driver.find_element_by_xpath(element_id)
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
            found_element_id = appium_web_driver.find_element_by_xpath(element_id)
            break
        if(element_found == False):
            print("Sleeping explicilty for 5 seconds")
            time.sleep(5)
   return found_element_id


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
    global Single_core_element,Multi_core_element,Opencl_score_element


    xindus_db_cursor = xindus_db_conn.cursor()
    result_id = get_geekbench_result_id(xindus_db_conn)

    benchmark_rslt_sql = "INSERT INTO BENCHMARK_RESULT(RUN_ID, ID, RESULT_ID) VALUES (%s,%s,%s)"
    benchmark_rslt_val = [
        (run_id,'4', result_id),     # 3 is the ANDROBENCH_TOOL_ID
    ]
    xindus_db_cursor.executemany(benchmark_rslt_sql, benchmark_rslt_val)
    xindus_db_conn.commit()

    geekbench_sql = "INSERT INTO GEEKBENCH_RESULT(RESULT_ID,SINGLE_CORE_ELEMENT,MULTI_CORE_ELEMENT,OPENCL_SCORE_ELEMENT) VALUES (%s,%s,%s,%s)"
    geekbench_val = [
        (result_id,Single_core_element,Multi_core_element,Opencl_score_element),
    ]
    xindus_db_cursor.executemany(geekbench_sql,geekbench_val)
    xindus_db_conn.commit()

def run_geekbench(adb_id,xindus_db_conn, run_id):
    global Single_core_element,Multi_core_element,Opencl_score_element
    print("Running Geekbench on device with adb_id =", adb_id)
    geekbench_desired_cap = {
        "deviceName": adb_id,
        "platformName": "android",
        "appPackage": "com.primatelabs.geekbench5",
        "appActivity": "com.primatelabs.geekbench.HomeActivity",
        "noReset": True,
        "newCommandTimeout": 200,
        "automationName": "uiautomator1"
    }
    geekbench_driver = webdriver.Remote("http://localhost:4723/wd/hub", geekbench_desired_cap)
    geekbench_driver.implicitly_wait(30)

    # Click the Accept button Button
    #geekbench_driver.find_element_by_id('android:id/button1').click()
    #geekbench_driver.implicitly_wait(30)

    # Click the RUN CPU Benchmark Button
    geekbench_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.support.v4.widget.DrawerLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.support.v4.view.ViewPager/android.widget.ScrollView/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.Button').click()

    #time.sleep(120)

    # get the Single core, Multi Core Results
    single_core_element = wait_for_element(geekbench_driver,850,'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.support.v4.view.ViewPager/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[2]/android.view.View[1]')
    Single_core_element = single_core_element.text
    multi_core_element = geekbench_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.support.v4.view.ViewPager/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[2]/android.view.View[3]')
    Multi_core_element= multi_core_element.text
    print('single_core_element= ', single_core_element.text)
    print('multi_core_element= ', multi_core_element.text)
    pull_screenshots(run_id, "Geekbench_CPU","C:\KnowledgeCenter\Xindus\Code\Perf_package_final\OnePlusDeviceReports\\apps_data")
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

    #time.sleep(1200)

    opencl_score_element =wait_for_element(geekbench_driver,850, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.support.v4.view.ViewPager/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[2]/android.view.View[1]')
    Opencl_score_element=opencl_score_element.text
    print('opencl_score_element= ', opencl_score_element.text)
    #nav_back_element = geekbench_driver.find_element_by_xpath('//android.widget.ImageButton[@content-desc="Navigate up"]')
    #nav_back_element.click()
    insert_geekbench_result(xindus_db_conn, run_id)
    store_geekbench_result(xindus_db_conn, [1, 2])
    pull_screenshots(run_id, "Geekbench_COMPUTE","C:\KnowledgeCenter\Xindus\Code\Perf_package_final\OnePlusDeviceReports\\apps_data")
