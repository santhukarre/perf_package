import subprocess
import io

bytes_transferred = ""
ddr_bw = ""

def run_bw_mem(size, oprtn):
    global bytes_transferred, ddr_bw
    command = 'adb shell /data/x86_64-linux-gnu/bw_mem ' + size + ' ' + oprtn
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
    ddr_bw = lmbench_op.split(" ")

def insert_lmbench_result(xindus_db_conn, run_id):
    global bytes_transferred, ddr_bw
    xindus_db_cursor = xindus_db_conn.cursor()
    sqlbw = "INSERT INTO LMBENCH_RESULT(RESULT_ID, BYTES_Transferred, DDR_BW) VALUES (2,'" +bytes_transferred+ "','" +ddr_bw+ "')"
    xindus_db_cursor.execute(sqlbw)
    print(sqlbw)
    xindus_db_conn.commit()