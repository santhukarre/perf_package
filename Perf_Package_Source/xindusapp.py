from appium import webdriver
import subprocess
import io
from Run import wait_for_element,pull_screenshots, wait_for_element_quick, wait_for_element_xpath,mergeWithFinalReport
from tabulate import tabulate
import pandas as pd
from vincent.colors import brews
import xlsxwriter

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

def generateXindusAppReport(xindus_db_conn):
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
        'categories': ['Sheet1', 1, 0, 9, 0],
        'values': ['Sheet1', 1, 1, 9, 1],
    })
    chart1.add_series({
        'name': ['Sheet1', 0, 2],
        'categories': ['Sheet1', 1, 0, 9, 0],
        'values': ['Sheet1', 1, 2, 9, 2],
        'y2_axis':    True,
})

    chart1.set_title({'name': 'Two_linecharts'})
    chart1.set_x_axis({'name': 'Buffer_Size'})
    chart1.set_y_axis({'name': 'Throughputs'})
    chart1.set_y2_axis({'name': 'Frequency'})
    chart1.set_style(11)
    worksheet.insert_chart('D2', chart1, {'x_offset': 25, 'y_offset': 10})
    workbook.close()
    mergeWithFinalReport('Xindus_App.xlsx', '.\\Xindus_PerfReport.xlsx', 1)

def generateXindusAppReport_Freq(xindus_db_conn):
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
        'categories': ['Sheet1', 1, 0, 9, 0],
        'values': ['Sheet1', 1, 1, 9, 1],
    })
    chart1.add_series({
        'name': ['Sheet1', 0, 2],
        'categories': ['Sheet1', 1, 0, 9, 0],
        'values': ['Sheet1', 1, 2, 9, 2],
})
    chart1.set_title({'name': 'Frequency_Residency'})
    chart1.set_x_axis({'name': 'Timestamp'})
    chart1.set_y_axis({'name': 'Frequency'})
    chart1.set_style(11)
    worksheet.insert_chart('D2', chart1, {'x_offset': 25, 'y_offset': 10})
    workbook.close()
    mergeWithFinalReport('XindusApp_Freq.xlsx', '.\\Xindus_PerfReport.xlsx', 1)



def run_xindusapp(adb_id, xindus_db_conn, run_id,screenShotsPath):
    print("Running xindusapp on device with adb_id =", adb_id)
    desired_cap = {
        "deviceName": adb_id,
        "platformName": "android",
        "appPackage": "com.example.myapplication",
        "appActivity": "com.example.myapplication.MainActivity",
        "automationName": "UiAutomator2"
    }
    appium_web_driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
    appium_web_driver.implicitly_wait(10)
    appium_web_driver.find_element_by_id('com.android.packageinstaller:id/permission_allow_button').click()
    start_button_element = wait_for_element_quick(appium_web_driver, 50, 'com.example.myapplication:id/button')
    start_button_element.click()
    results_button_element = wait_for_element_quick(appium_web_driver, 200, 'com.example.myapplication:id/results')
    results_button_element.click()
    pull_screenshots(run_id, "Xindus_APP",screenShotsPath)
    populate_xindusapp_result(xindus_db_conn, screenShotsPath)
    populate_xindusapp_config(xindus_db_conn, screenShotsPath)

