from appium import webdriver
from Run import wait_for_element,pull_screenshots,mergeWithFinalReport,convert
from tabulate import tabulate
import pandas as pd
from vincent.colors import brews
import time

seq_read_result=""
seq_write_result=""
rand_read_result=""
rand_write_result=""
sql_insert_result=""
sql_update_result=""
sql_delete_result=""

def generateAndrobenchReport(xindus_db_conn,runids):
    report_file_name = '.\Androbench.xlsx'
    mycursor = xindus_db_conn.cursor()
    print(runids)

    run_ids=convert(runids)
    print(run_ids)
    statement = "SELECT * FROM ANDROBENCH_RESULT WHERE RESULT_ID IN ({0})".format(
        ', '.join(['%s'] * len(run_ids)))
    mycursor.execute(statement,run_ids)
    data = mycursor.fetchall()
    print(data)

    print(tabulate(data, headers=['result_id','seq_read', 'seq_write', 'rand_read','rand_write','sql_insert','sql_update','sql_delete'], tablefmt='psql'))
    print("Total number of rows is ", mycursor.rowcount)
    i = 0
    iterations = []
    iterations_names = []
    for row in data:
        iteration={'seq_read': row[1], 'seq_write': row[2], 'rand_read': row[3], 'rand_write': row[4], 'sql_insert': row[5],'sql_update': row[6],'sql_delete': row[7]}
        print(iteration)
        iterations.append(iteration)
        iterations_names.append('iteration '+ str(i))
        i = i +1
    data = iterations
    index = iterations_names
    # Create a Pandas dataframe from the data.
    df = pd.DataFrame(data,index=index)
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    sheet_name = 'Sheet1'
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
            'name':       ['Sheet1', 0, col_num],
            'categories': ['Sheet1', 1, 0, i, 0],
            'values':     ['Sheet1', 1, col_num, i, col_num],
            'fill':       {'color': brews['Set1'][col_num - 1]},
            'overlap':-10,})
    # Configure the chart axes.
    chart.set_x_axis({'name': 'Iterations'})
    chart.set_y_axis({'name': 'Score', 'major_gridlines': {'visible': False}})
    # Insert the chart into the worksheet.
    worksheet.insert_chart('H2', chart)
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    mergeWithFinalReport(report_file_name, '.\\Xindus_PerfReport.xlsx', 1)
    time.sleep(5)


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
    rand_read_result= rand_read_result.split(" ")[0]
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

    benchmark_rslt_sql = "INSERT INTO BENCHMARK_RESULT(RUN_ID,TOOL_NAME, RESULT_ID) VALUES (%s,%s,%s)"
    benchmark_rslt_val = [
        (run_id,'Androbench', result_id),
    ]
    xindus_db_cursor.executemany(benchmark_rslt_sql, benchmark_rslt_val)
    xindus_db_conn.commit()

    androbench_sql = "INSERT INTO ANDROBENCH_RESULT(RESULT_ID, SEQ_READ, SEQ_WRITE, RAND_READ, RAND_WRITE, SQL_INSERT, SQL_UPDATE, SQL_DELETE) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
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


def run_androbench(adb_id, xindus_db_conn, run_id, screenshots_path):
    print("Running Androbench on device with adb_id =", adb_id)
    desired_cap = {
        "deviceName": adb_id,
        "platformName": "android",
        "appPackage": "com.andromeda.androbench2",
        "appActivity": "main",
        "automationName": "uiautomator1"
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

    appium_web_driver.implicitly_wait(10)
    # on Androbench Run All Benchmarks Button.

    appium_web_driver.find_element_by_id('com.andromeda.androbench2:id/btnStartingBenchmarking').click()

    appium_web_driver.implicitly_wait(10)

    # Click on Yes Button.
    appium_web_driver.find_element_by_id('android:id/button1').click()

    # Click on Cancel Button for 'Do you want to send results to server for research purpose'
    send_results_element = wait_for_element(appium_web_driver,150,'android:id/button2')
    send_results_element.click()

    # Click on Results Button.
    #appium_web_driver.implicitly_wait(10)
    #results_element = appium_web_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TabHost/android.widget.LinearLayout/android.widget.TabWidget/android.widget.LinearLayout[2]')
    #results_element.click()
    #Duration = END_TIME - START_TIME
    #print(Duration)

    get_androdben_results(appium_web_driver, xindus_db_conn, run_id)
    insert_androbench_result(xindus_db_conn, run_id)
    store_androbench_result(xindus_db_conn, [1, 2])
    pull_screenshots(run_id, "Androbench", screenshots_path)
    #generateAndrobenchReport(xindus_db_conn)