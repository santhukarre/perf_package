from appium import webdriver
import subprocess
import io
from Run import wait_for_element,pull_screenshots, wait_for_element_quick, wait_for_element_xpath,mergeWith_FinalReport
from tabulate import tabulate
import pandas as pd
from vincent.colors import brews
import xlsxwriter
import configparser
logsPath = ""

def populate_xindusapp_result(xindus_db_conn,screenShotsPath):
    xindus_db_cursor = xindus_db_conn.cursor()
    cmd = "adb pull /sdcard/max_freq_logging.txt" + " " + screenShotsPath
    print("command = ", cmd)
    print("screenShotsPath = ", screenShotsPath)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    file1 = open(screenShotsPath + "\\max_freq_logging.txt", "r")
    for i, lines in enumerate(file1):
        if i > 0:
             print("Output of Read function is ")
             line = lines.split()
             print(line)
             singleline = line[0]
             str = singleline.split(":")
             print(str)
             Timestamp = str[0]
             print("Timestamp ", str[0])
             Operation = str[1]
             print("Operation ", str[1])
             Bufsize = str[3]
             print("Bufsize ", str[3])
             Freq = str[4]
             print("Freq ", str[4])
             Throughput = str[5]
             print("Throughput ", str[5])
             print("Timestamp = ", Timestamp, "Operation = ", Operation, "Buf_size = ", Bufsize, "DDR_MAX_Freq = ",Freq, "Throughput = ", Throughput)

             xindusapp_sql = "INSERT INTO XINDUSAPP_RESULT(TIMESTAMP,OPERATION,BUF_SIZE,DDR_MAX_FREQ,THROUGHPUT) VALUES(%s,%s,%s,%s,%s)"
             xindusapp_val = [(Timestamp, Operation, Bufsize, Freq, Throughput)]
             xindus_db_cursor.executemany(xindusapp_sql, xindusapp_val)
             xindus_db_conn.commit()

def populate_xindusapp_config(xindus_db_conn,screenShotsPath):
    xindus_db_cursor = xindus_db_conn.cursor()
    cmd = "adb pull /sdcard/config.txt"  + " " + screenShotsPath
    print("command = ", cmd)
    print("screenShotsPath = ", screenShotsPath)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    file1 = open(screenShotsPath + "\\config.txt" , "r")
    for i, line in enumerate(file1):
        if i > 2:
            print("Output of Read function is ")
            lines = line.split()
            print(lines)
            Iteration = lines[0]
            print(Iteration)
            threads = lines[1]
            print(threads)
            Iterations=Iteration.split(":")[1]
            print("Iterations",Iterations)
            Threads = threads.split(":")[1]
            print("Threads",Threads)
            print("Iteration = ", Iterations, "Threads = ", Threads)

            xindusapp_sql = "INSERT INTO XINDUSAPP_CONFIG(ITERATIONS,THREADS) VALUES(%s,%s)"
            xindusapp_val = [
            (Iterations,Threads)
            ]
            xindus_db_cursor.executemany(xindusapp_sql, xindusapp_val)
            xindus_db_conn.commit()

def generate_XindusApp_Report(xindus_db_conn):
    report_file_name = '.\XindusApp.xlsx'
    mycursor = xindus_db_conn.cursor()
   # print(runids)

    #run_ids=convert(runids)
   # print(run_ids)
    statement = "SELECT * FROM XINDUSAPP_RESULT  "
         #       "WHERE RESULT_ID IN ({0})".format(
       # ', '.join(['%s'] * len(run_ids)))
    mycursor.execute(statement)
    data = mycursor.fetchall()
    print(data)

    print(tabulate(data, headers=['TimeStamp','Operation', 'Buf_Size', 'DDR_MAX_FREQ','Throughput'], tablefmt='psql'))
    print("Total number of rows is ", mycursor.rowcount)
    i = 0
    Timestamps = []
    Operations = []
    Buf_Sizes = []
    DDR_MAX_FREQS = []
    Throughputs = []
    for row in data:
        Timestamp=row[0]
        print(Timestamp)
        Operation =row[1]
        print(Operation)
        Buf_Size = row[2]
        print(Buf_Size)
        DDR_MAX_FREQ = row[3]
        print(DDR_MAX_FREQ)
        Throughput = row[4]
        print(Throughput)
        Timestamps.append(Timestamp)
        Operations.append(Operation)
        Buf_Sizes.append(Buf_Size)
        DDR_MAX_FREQS.append(DDR_MAX_FREQ)
        Throughputs.append(Throughput)
    print("Timestamps: ",Timestamps)
    print("Operations: ",Operations)
    print("Buf_Sizes: ",Buf_Sizes)
    print("DDR_MAX_FREQS: ",DDR_MAX_FREQS)
    print("Throughputs: ",Throughputs)

    workbook = xlsxwriter.Workbook('Xindus_App.xlsx')

    worksheet = workbook.add_worksheet()

    bold = workbook.add_format({'bold': True})
    headings = ['Buffer_Size','Throughput','Frequency']
    data= [Buf_Sizes,Throughputs,DDR_MAX_FREQS]

    worksheet.write_row('A1', headings, bold)

    worksheet.write_column('A2', data[0])
    worksheet.write_column('B2', data[1])
    worksheet.write_column('C2', data[2])

    chart1 = workbook.add_chart({'type': 'line'})

    chart1.add_series({
          'name': ['Sheet1', 0, 1],
          'categories': ['Sheet1', 32, 0, 61, 0],
          'values': ['Sheet1', 32, 1, 61, 1],
    })
    chart1.add_series({
          'name': ['Sheet1', 0, 2],
          'categories': ['Sheet1', 32, 0, 61, 0],
          'values': ['Sheet1', 32, 2, 61, 2],
          'y2_axis':    True,
    })

    chart1.set_title({'name': 'Two_linecharts'})
    chart1.set_x_axis({'name': 'Buffer_Size'})
    chart1.set_y_axis({'name': 'Throughputs'})
    chart1.set_y2_axis({'name': 'Frequency'})
    chart1.set_style(11)
    worksheet.insert_chart('D2', chart1, {'x_offset': 25, 'y_offset': 10})
    workbook.close()
    # mergeWith_FinalReport('Xindus_App.xlsx', '.\\Xindus_PerfReport.xlsx', 1)

def generate_XindusApp_Report_Freq(xindus_db_conn):
    report_file_name = '.\XindusApp_Freq.xlsx'
    mycursor = xindus_db_conn.cursor()
   # print(runids)

    #run_ids=convert(runids)
   # print(run_ids)
    statement = "SELECT * FROM XINDUSAPP_RESULT  "
         #       "WHERE RESULT_ID IN ({0})".format(
       # ', '.join(['%s'] * len(run_ids)))
    mycursor.execute(statement)
    data = mycursor.fetchall()
    print(data)

    print(tabulate(data, headers=['TimeStamp','Operation', 'Buf_Size', 'DDR_MAX_FREQ','Throughput'], tablefmt='psql'))
    print("Total number of rows is ", mycursor.rowcount)
    i = 0
    Timestamps = []
    Operations = []
    Buf_Sizes = []
    DDR_MAX_FREQS = []
    Throughputs = []
    for row in data:
        Timestamp=row[0]
        print(Timestamp)
        DDR_MAX_FREQ = row[3]
        print(DDR_MAX_FREQ)
        Timestamps.append(Timestamp)
        DDR_MAX_FREQS.append(DDR_MAX_FREQ)
    print("Timestamps: ",Timestamps)
    print("DDR_MAX_FREQS: ",DDR_MAX_FREQS)
    workbook = xlsxwriter.Workbook('XindusApp_Freq.xlsx')
    worksheet = workbook.add_worksheet()
    bold = workbook.add_format({'bold': True})
    headings = ['Timestamp','Frequency']
    data= [Timestamps,DDR_MAX_FREQS]
    worksheet.write_row('A1', headings, bold)
    worksheet.write_column('A2', data[0])
    worksheet.write_column('B2', data[1])
    chart1 = workbook.add_chart({'type': 'line'})


    chart1.add_series({
            'name': ['Sheet1', 0, 1],
            'categories': ['Sheet1', 32, 0, 61, 0],
            'values': ['Sheet1', 32, 1, 61, 1],
    })
    chart1.add_series({
            'name': ['Sheet1', 0, 2],
            'categories': ['Sheet1', 32, 0, 61, 0],
            'values': ['Sheet1', 32, 2, 61, 2],
            'y2_axis': True,
    })

    chart1.set_title({'name': 'Frequency_Residency'})
    chart1.set_x_axis({'name': 'Timestamp'})
    chart1.set_y_axis({'name': 'Frequency'})
    chart1.set_style(11)
    worksheet.insert_chart('D2', chart1, {'x_offset': 25, 'y_offset': 10})
    workbook.close()
    # mergeWith_FinalReport('XindusApp_Freq.xlsx', '.\\Xindus_PerfReport.xlsx', 1)

def pull_xindus_console_configs():
    pull_xindus_console_config_cmd = "adb shell pull xindus_console_config.ini"
    p = subprocess.Popen(pull_xindus_console_config_cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()

def run_xindusapp(adb_id, xindus_db_conn, run_id,screenShotsPath,xindusAppThreads,xindusAppIterations,xindusAppBuffers,xindusAppDDROnly,xindusAppLogLevel,xindusAppFreeqResidency):
    print("Running xindusapp on device with adb_id =", adb_id)

    desired_cap = {
        "deviceName": "one plus",
        "platformName": "android",
        "appPackage": "com.example.myapplication",
        "appActivity": "com.example.myapplication.MainActivity",
        "udid": adb_id,
        "automationName": "UiAutomator2"
    }
    appium_web_driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
    appium_web_driver.implicitly_wait(10)
    permission_element = wait_for_element_quick(appium_web_driver,20, 'com.android.packageinstaller:id/permission_allow_button')
    if(permission_element != None):
      permission_element.click()
    appium_web_driver.find_element_by_id('com.example.myapplication:id/numOfThreads').clear()
    appium_web_driver.find_element_by_id('com.example.myapplication:id/numOfThreads').set_value(xindusAppThreads)
    appium_web_driver.find_element_by_id('com.example.myapplication:id/numOfIterations').clear()
    appium_web_driver.find_element_by_id('com.example.myapplication:id/numOfIterations').set_value(xindusAppIterations)
    appium_web_driver.find_element_by_id('com.example.myapplication:id/bufSizes').clear()
    appium_web_driver.find_element_by_id('com.example.myapplication:id/bufSizes').set_value(xindusAppBuffers)
    appium_web_driver.find_element_by_id('com.example.myapplication:id/ddrOnly').clear()
    appium_web_driver.find_element_by_id('com.example.myapplication:id/ddrOnly').set_value(xindusAppDDROnly)
    appium_web_driver.find_element_by_id('com.example.myapplication:id/logLevel').clear()
    appium_web_driver.find_element_by_id('com.example.myapplication:id/logLevel').set_value(xindusAppLogLevel)
    appium_web_driver.find_element_by_id('com.example.myapplication:id/freqResidency').clear()
    appium_web_driver.find_element_by_id('com.example.myapplication:id/freqResidency').set_value(xindusAppFreeqResidency)

    start_button_element = wait_for_element_quick(appium_web_driver, 50, 'com.example.myapplication:id/start')
    # start_button_element = wait_for_element_xpath(appium_web_driver, 50, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.widget.RelativeLayout/android.widget.Button[1]')

    if(start_button_element != None):
      start_button_element.click()
    results_button_element = wait_for_element_quick(appium_web_driver, 200, 'com.example.myapplication:id/xindusResults')
    results_button_element.click()
    #results_button_element = wait_for_element_xpath(appium_web_driver, 200, '/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.Button')

    pull_screenshots(run_id, "Xindus_APP",screenShotsPath)
    populate_xindusapp_result(xindus_db_conn, screenShotsPath)
    populate_xindusapp_config(xindus_db_conn, screenShotsPath)

