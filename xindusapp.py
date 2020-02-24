import subprocess
import io
from Run import wait_for_element,pull_screenshots, report_file_name
import pandas as pd
from vincent.colors import brews

def run_xindusapp(threads,iterations,cache,loglevel,xindus_db_conn, run_id):
    global bytes_transferred, ddr_bw
    command = 'adb shell /data/xindus_app ' + str(threads) + str(iterations) + str(cache) + str(loglevel)
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = p.communicate()
    print("standard output :", stderr)
    str_output = str(stderr, 'utf-8')
    print("str_output :", str_output)
    buf = io.StringIO(str_output)
    xindus_op = buf.readline()
    print("bandwidth and memory values: ", xindus_op)
    pull_screenshots(run_id, "Xindus_APP","C:\KnowledgeCenter\Xindus\Code\Perf_package_final\OnePlusDeviceReports\\apps_data")
def generateXindusAppReport(xindus_db_conn):
    mycursor = xindus_db_conn.cursor()
    sql_read = "select * from XindusApp_RESULT"
    mycursor.execute(sql_read)
    data = mycursor.fetchall()
    print("Total number of rows is ", mycursor.rowcount)
    i = 0
    iterations = []
    iterations_names = []
    for row in data:
        iteration={'Threads': row[1], 'Iterations': row[2], 'Cache': row[3], 'LogLevel': row[4]}
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
    for col_num in range(1, len(iterations) + 1):
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