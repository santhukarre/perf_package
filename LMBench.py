import subprocess
import io

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
        (run_id, '3', result_id),  # 3 is the ANDROBENCH_TOOL_ID
    ]
    xindus_db_cursor.executemany(benchmark_rslt_sql, benchmark_rslt_val)
    xindus_db_conn.commit()

    lmbench_sql = "INSERT INTO LMBENCH_RESULT(RESULT_ID,BYTES_Transferred,DDR_BW) VALUES (2,'" +bytes_transferred+ "','" +ddr_bw+ "')"
    xindus_db_cursor.execute(lmbench_sql)
    print(lmbench_sql)
    xindus_db_conn.commit()


def run_lmbench(size,oprtn,xindus_db_conn, run_id):
    global bytes_transferred, ddr_bw
    command = 'adb shell /data/x86_64-linux-gnu/bw_mem ' + str(size) + ' ' + oprtn
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
