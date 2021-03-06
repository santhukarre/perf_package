from appium import webdriver
import pandas as pd
from vincent.colors import brews
from Run import wait_for_element, wait_for_element_quick, pull_screenshots,mergeWith_FinalReport,convert
import openpyxl
import time
import sys

Antutu_total_score = ""
Antutu_cpu_score = ""
Antutu_mem_score = ""
Antutu_gpu_score = ""
Antutu_ux_score = ""

def generate_Antutu_Report(xindus_db_conn,runids):
    mycursor = xindus_db_conn.cursor()
    print(runids)
    run_ids = convert(runids)
    print(run_ids)
    statement = "SELECT * FROM ANTUTU_RESULT WHERE RESULT_ID IN ({0})".format(
        ', '.join(['%s'] * len(run_ids)))
    mycursor.execute(statement, run_ids)
    data = mycursor.fetchall()
    print("Total number of rows is ", mycursor.rowcount)
    i = 0
    iterations = []
    iterations_names = []
    for row in data:
        iteration={'Antutu_totalScore': row[1], 'Antutu_cpu_score': row[2], 'Antutu_mem_score': row[3], 'Antutu_gpu_score': row[4], 'Antutu_ux_score': row[5]}
        iterations.append(iteration)
        iterations_names.append('iteration '+ str(i))
        i = i +1
    data = iterations
    index = iterations_names
    # Create a Pandas dataframe from the data.
    df = pd.DataFrame(data, index=index)
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    sheet_name = 'Antutu'
    report_file_name = '.\Antutu.xlsx'
    writer = pd.ExcelWriter(report_file_name, engine='xlsxwriter')
    df.to_excel(writer, sheet_name=sheet_name)
    # Access the XlsxWriter workbook and worksheet objects from the dataframe.
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]
    # Create a chart object.
    chart = workbook.add_chart({'type': 'column'})
    # Configure the series of the chart from the dataframedata.
    for col_num in range(1,len(row)):
        print("col_num ", col_num)
        chart.add_series({
            'name':       [sheet_name, 0,col_num],
            'categories': [sheet_name, 1, 0, i, 0],
            'values':     [sheet_name, 1, col_num, i, col_num],
            'fill':       {'color': brews['Set1'][col_num - 1]},
            'overlap':-10,})
    # Configure the chart axes.
    chart.set_x_axis({'name': 'Iterations'})
    chart.set_y_axis({'name': 'Score', 'major_gridlines': {'visible': False}})
    # Insert the chart into the worksheet.
    worksheet.insert_chart('H2', chart)
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    # mergeWith_FinalReport(report_file_name, '.\\Xindus_PerfReport.xlsx', 2)
    time.sleep(5)

def store_antutu_result(xindus_db_conn, result_id_list):
    xindus_db_cursor = xindus_db_conn.cursor()
    sql_read = "select * from ANTUTU_RESULT"
    xindus_db_cursor.execute(sql_read)
    data = xindus_db_cursor.fetchall()
    print("Total number of rows is ", xindus_db_cursor.rowcount)
    file = open("results.csv", "w+")
    file.write("Result id,Antutu_total_score,Antutu_cpu_score,Antutu_memory_score,Antutu_ux_score")
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
       file.write("\n")

def get_antutu_result_id(xindus_db_conn):
    xindus_db_cursor = xindus_db_conn.cursor(  )
    sql_read = "select MAX(RESULT_ID) from ANTUTU_RESULT"
    xindus_db_cursor.execute(sql_read)
    data = xindus_db_cursor.fetchall( )
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



def insert_antutu_result(xindus_db_conn, run_id):
    global Antutu_total_score,Antutu_cpu_score, Antutu_gpu_score,Antutu_memory_score, Antutu_ux_score

    xindus_db_cursor = xindus_db_conn.cursor()
    result_id = get_antutu_result_id(xindus_db_conn)

    benchmark_rslt_sql = "INSERT INTO BENCHMARK_RESULT(RUN_ID,TOOL_NAME, RESULT_ID) VALUES (%s,%s,%s)"
    benchmark_rslt_val = [
        (run_id,'Antutu', result_id),
    ]
    xindus_db_cursor.executemany(benchmark_rslt_sql,benchmark_rslt_val)
    xindus_db_conn.commit()

    antutu_sql = "INSERT INTO ANTUTU_RESULT(RESULT_ID,ANTUTU_TOTAL_SCORE,ANTUTU_CPU_SCORE,ANTUTU_GPU_SCORE,ANTUTU_MEMORY_SCORE,ANTUTU_UX_SCORE) VALUES (%s,%s,%s,%s,%s,%s)"
    antutu_val = [
        (result_id,Antutu_total_score,Antutu_cpu_score,Antutu_gpu_score,Antutu_memory_score,Antutu_ux_score),
    ]
    xindus_db_cursor.executemany(antutu_sql, antutu_val)
    xindus_db_conn.commit()


def run_antutu(adb_id,xindus_db_conn, run_id, screenShotsPath):
    global Antutu_total_score,Antutu_cpu_score, Antutu_gpu_score,Antutu_memory_score, Antutu_ux_score
    print("Running Antutu on device with adb_id =", adb_id)
    desired_cap = {
        "deviceName": "oneplus",
        "platformName": "android",
        "appPackage": "com.antutu.ABenchMark",
        "appActivity": "com.antutu.ABenchMark.ABenchMarkStart",
        "udid" : adb_id,
        "noReset": True,
        "newCommandTimeout":800000,
        "automationName": "UiAutomator1"
    }
    appium_web_driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
    permission_element = wait_for_element_quick(appium_web_driver, 30, 'com.android.packageinstaller:id/permission_allow_button')

    if(permission_element != None):
        print("it means it is appium web element")
        sys.stdout.flush()
        permission_element.click()
        appium_web_driver.implicitly_wait(10)
        appium_web_driver.find_element_by_id('com.android.packageinstaller:id/permission_allow_button').click()
        appium_web_driver.implicitly_wait(10)
        appium_web_driver.find_element_by_id('com.android.packageinstaller:id/permission_allow_button').click()
    print("Finding start element")
    main_test_start_element = wait_for_element_quick(appium_web_driver, 30,'com.antutu.ABenchMark:id/main_test_start_title')

    if(main_test_start_element != None):
        print("Found start element")
        main_test_start_element.click()
    else:
        main_test_start_element = wait_for_element_quick(appium_web_driver, 20,
                                                         'com.antutu.ABenchMark:id/main_test_finish_retest')
        if (main_test_start_element != None):
            print("Found start element")
            main_test_start_element.click()

    antutu_total_score_element=wait_for_element(appium_web_driver,1600,'com.antutu.ABenchMark:id/textViewTotalScore')
    #antutu_total_score_element=appium_web_driver.find_element_by_id('com.antutu.ABenchMark:id/textViewTotalScore')
    Antutu_total_score = antutu_total_score_element.text
    print('Antutu Total Score :', Antutu_total_score)
    appium_web_driver.implicitly_wait(10)

    antutu_cpu_score_element = appium_web_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[1]/android.view.ViewGroup/android.widget.TextView[1]')
    #antutu_cpu_score.click()
    Antutu_cpu_score = antutu_cpu_score_element.text
    print('Antutu CPU Score :', Antutu_cpu_score)
    appium_web_driver.implicitly_wait(10)

    antutu_gpu_score_element = appium_web_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[2]/android.view.ViewGroup/android.widget.TextView[1]')
    Antutu_gpu_score = antutu_gpu_score_element.text
    #antutu_gpu_score.click()
    print('Antutu GPU Score :', Antutu_gpu_score)

    appium_web_driver.implicitly_wait(10)
    antutu_memory_score_element = appium_web_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[3]/android.view.ViewGroup/android.widget.TextView[1]')
    #antutu_memory_score.click()
    Antutu_memory_score = antutu_memory_score_element.text
    print('Antutu Memory Score :', Antutu_memory_score)

    appium_web_driver.implicitly_wait(10)
    antutu_ux_score_element = appium_web_driver.find_element_by_xpath('	/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[4]/android.view.ViewGroup/android.widget.TextView[1]')
    #antutu_ux_score.click()
    Antutu_ux_score = antutu_ux_score_element.text
    print('Antutu UX Score :', Antutu_ux_score)
    insert_antutu_result(xindus_db_conn, run_id)
    store_antutu_result(xindus_db_conn, [1, 2])
    pull_screenshots(run_id, "Antutu",screenShotsPath)
    #generate_Antutu_Report(xindus_db_conn)