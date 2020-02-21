import subprocess
import io
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

