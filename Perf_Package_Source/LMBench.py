import subprocess
import io
from Run import pull_screenshots,report_file_name
import pandas as pd
from vincent.colors import brews

def store_lmbench_result(xindus_db_conn, result_id_list):
    xindus_db_cursor = xindus_db_conn.cursor()
    sql_read = "select * from LMBENCH_RESULT"
    xindus_db_cursor.execute(sql_read)
    data = xindus_db_cursor.fetchall()
    print("Total number of rows is ", xindus_db_cursor.rowcount)
    file = open("results.csv", "w+")
    file.write("Result id,BYTES_Transferred,DDR_BW")
    file.write("\n")
    for row in data:
       file.write(str(row[0]))
       file.write(",")
       file.write(str(row[1]))
       file.write(",")
       file.write(str(row[2]))
       file.write("\n")

def get_lmbench_result_id(xindus_db_conn):
    xindus_db_cursor = xindus_db_conn.cursor()
    sql_read = "select MAX(RESULT_ID) from LMBENCH_RESULT"
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

def insert_lmbench_result(xindus_db_conn, run_id):
    global bytes_transferred, ddr_bw
    xindus_db_cursor = xindus_db_conn.cursor()

    result_id = get_lmbench_result_id(xindus_db_conn)

    benchmark_rslt_sql = "INSERT INTO BENCHMARK_RESULT(RUN_ID, ID, RESULT_ID) VALUES (%s,%s,%s)"
    benchmark_rslt_val = [
        (run_id, '5', result_id),
    ]
    xindus_db_cursor.executemany(benchmark_rslt_sql, benchmark_rslt_val)
    xindus_db_conn.commit()

    lmbench_sql = "INSERT INTO LMBENCH_RESULT(RESULT_ID,BYTES_Transferred,DDR_BW) VALUES (2,'" +bytes_transferred+ "','" +ddr_bw+ "')"
    xindus_db_cursor.execute(lmbench_sql)
    print(lmbench_sql)
    xindus_db_conn.commit()

def generateGeekbenchReport(xindus_db_conn):
    mycursor = xindus_db_conn.cursor()
    sql_read = "select * from LMBENCH_RESULT"
    mycursor.execute(sql_read)
    data = mycursor.fetchall()
    print("Total number of rows is ", mycursor.rowcount)
    i = 0
    iterations = []
    iterations_names = []
    for row in data:
        iteration={'bytes_taransferred': row[1], 'ddr_bw': row[2]}
        iterations_names.append('iteration '+ str(i))
        i = i +1
    data = iterations
    index = iterations_names
    # Create a Pandas dataframe from the data.
    df = pd.DataFrame(data,index=index)
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    sheet_name = 'Sheet5'
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
            'name':       ['Sheet5', 0, col_num],
            'categories': ['Sheet5', 1, 0, i, 0],
            'values':     ['Sheet5', 1, col_num, i, col_num],
            'fill':       {'color': brews['Set1'][col_num - 1]},
            'overlap':-10,})
    # Configure the chart axes.
    chart.set_x_axis({'name': 'Iterations'})
    chart.set_y_axis({'name': 'Score', 'major_gridlines': {'visible': False}})
    # Insert the chart into the worksheet.
    worksheet.insert_chart('H2', chart)
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()

def run_lmbench(size,oprtn,xindus_db_conn, run_id, screenShotsPath):
    global bytes_transferred, ddr_bw
    command = 'adb shell /data/bw_mem ' + str(size) + ' ' + oprtn
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdout, stderr) = p.communicate()
    print("standard output :", stderr)
    str_output = str(stderr, 'utf-8')
    print("str_output :", str_output)
    buf = io.StringIO(str_output)
    lmbench_op = buf.readline()
    print("bandwidth and memory values: ", lmbench_op)
    print("bytes_mem:", lmbench_op.split(" ")[0])
    print("bandwidth:", lmbench_op.split(" ")[1])
    bytes_transferred = lmbench_op.split(" ")[0]
    ddr_bw = lmbench_op.split(" ")[1]
    insert_lmbench_result(xindus_db_conn, run_id)
    #pull_screenshots(run_id, "LMBENCH",screenShotsPath)