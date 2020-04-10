import mysql.connector
import subprocess
import io
from adb_utility import adb_id

def get_xindus_db_conn(mySQLUser, mySQLPort, mySQLPassword):
    print("mySQLPort = ", mySQLPort)
    xindus_db_con = mysql.connector.connect(
    host="localhost",
    user=mySQLUser,
    port=int(mySQLPort),
    passwd=mySQLPassword,
    database="Xindus_DB"
    )
    return xindus_db_con

def create_tables(mySQLUser, mySQLPort, mySQLPassword):
    xindus_db_con = mysql.connector.connect(
    host="localhost",
    user=mySQLUser,
    port=int(mySQLPort),
    passwd=mySQLPassword,
    database="Xindus_DB"
    )
    xindus_db_cursor = xindus_db_con.cursor()
    xindus_db_cursor.execute("Create Table  IF NOT EXISTS DEVICE(DEVICE_ID VARCHAR(255),NAME VARCHAR(255),CPU_HARDWARE VARCHAR(255),CPU_CORES INT,DDR_SIZE FLOAT,STORAGE VARCHAR(255),DDR_VENDOR INT,STORAGE_VENDOR INT)")
    xindus_db_cursor.execute("Create Table  IF NOT EXISTS TOOLS(NAME VARCHAR(255),ID INT AUTO_INCREMENT PRIMARY KEY,CATEGORY VARCHAR(255))")
    xindus_db_cursor.execute("Create Table  IF NOT EXISTS SUBSYSTEMS(ID INT, FOREIGN KEY SUBSYSTEMS(ID) REFERENCES TOOLS(ID),SUBSYSTEM VARCHAR(255))")
    xindus_db_cursor.execute("Create Table  IF NOT EXISTS RUN(RUN_ID INT PRIMARY KEY,RUN_COMMENTS VARCHAR(255),DEVICE_ID VARCHAR(255),NAME VARCHAR(255),START_DATE VARCHAR(255),START_TIME VARCHAR(255),END_DATE VARCHAR(255),END_TIME VARCHAR(255),MODE VARCHAR(255))")
    xindus_db_cursor.execute("Create Table  IF NOT EXISTS TESTING_SEQUENCE(RUN_ID INT NOT NULL,CONSTRAINT fk_category_7 FOREIGN KEY (RUN_ID) REFERENCES RUN(RUN_ID),ID INT,CONSTRAINT fk_category_8 FOREIGN KEY (ID) REFERENCES TOOLS(ID),START_TIME VARCHAR(255),END_TIME VARCHAR(255))")
    xindus_db_cursor.execute("Create Table  IF NOT EXISTS BENCHMARK_RESULT(RUN_ID INT,TOOL_NAME VARCHAR(255),RESULT_ID INT)")
    xindus_db_cursor.execute("Create Table  IF NOT EXISTS ANDROBENCH_RESULT(RESULT_ID INT,SEQ_READ INT,SEQ_WRITE INT,RAND_READ INT,RAND_WRITE INT,SQL_INSERT INT,SQL_UPDATE INT,SQL_DELETE INT)")
    xindus_db_cursor.execute("Create Table  IF NOT EXISTS ANTUTU_RESULT(RESULT_ID INT,ANTUTU_TOTAL_SCORE INT,ANTUTU_CPU_SCORE INT,ANTUTU_GPU_SCORE INT,ANTUTU_MEMORY_SCORE INT,ANTUTU_UX_SCORE INT)")
    xindus_db_cursor.execute("Create Table  IF NOT EXISTS GEEKBENCH_RESULT(RESULT_ID INT,SINGLE_CORE_ELEMENT INT,MULTI_CORE_ELEMENT INT,OPENCL_SCORE_ELEMENT INT)")
    xindus_db_cursor.execute("Create Table  IF NOT EXISTS LMBENCH_RESULT(RESULT_ID INT, BYTES_Transferred FLOAT,DDR_BW INT)")
    xindus_db_cursor.execute("Create Table  IF NOT EXISTS THREEDMARK_RESULT(RESULT_ID INT,SLINGOPENGL_OVERALL INT, SLINGOPENGL_GRAPHICS INT, SLINGOPENGL_PHYSICS INT, SLING_OVERALL INT, SLING_GRAPHICS INT, SLING_PHYSICS INT,SLINGSHOT_OVERALL INT,SLINGSHOT_GRAPHICS INT,SLINGSHOT_PHYSICS INT,API_OPENGL INT,API_VULKAN INT)")
    xindus_db_cursor.execute("Create Table  IF NOT EXISTS XINDUSAPP_RESULT(RESULT_ID INT,THREADS INT,ITERATIONS INT,CACHE INT,LOGLEVEL INT)")
    xindus_db_con.commit()
    return xindus_db_con

def populate_tools(xindus_db_conn):
    xindus_db_cursor = xindus_db_conn.cursor()
    tools_sql = "INSERT INTO TOOLS(NAME, CATEGORY) VALUES (%s, %s)"
    tools_val = [
    ('ANDROBENCH', 'PERF'),
    ('ANTUTU', 'PERF'),
    ('3DMARK', 'PERF'),
    ('GEEKBENCH', 'PERF'),
    ('LMBENCH', 'PERF'),
    ('XINDUS_APP', 'PERF'),
    ]
    xindus_db_cursor.executemany(tools_sql, tools_val)
    xindus_db_conn.commit()
def populate_Subsystems(xindus_db_conn):
    xindus_db_cursor = xindus_db_conn.cursor()
    subsystem_sql = "INSERT INTO SUBSYSTEMS(ID,SUBSYSTEM) VALUES (%s, %s)"
    subsystem_val = [
    ('1', 'PERF'),
    ('2', 'PERF'),
    ('3', 'PERF'),
    ('4', 'PERF'),
    ('5', 'PERF'),
    ('6', 'PERF'),
    ]
    xindus_db_cursor.executemany(subsystem_sql, subsystem_val)
    xindus_db_conn.commit()
def insert_runid_testingseq(xindus_db_conn,run_id):
    xindus_db_cursor = xindus_db_conn.cursor()
    data_sql = "INSERT INTO TESTING_SEQUENCE(RUN_ID,ID) VALUES(%s,%s)"
    data_val = [
        (run_id)
    ]
    xindus_db_cursor.executemany(data_sql,data_val)
    xindus_db_conn.commit()

def insert_Tetsingseq_data(xindus_db_conn, run_id):
    xindus_db_cursor = xindus_db_conn.cursor()
    global START_TIME,END_TIME

    testseq_data_sql = "Update TESTING_SEQUENCE SET START_TIME ='" + str(START_TIME) + "'," +\
                    "END_TIME ='" + str(END_TIME) + "'," +\
                    "where RUN_ID = '" + str(run_id) +"'"
    print("run_id = ", run_id)
    print("testseq_data_sql = ", testseq_data_sql)
    xindus_db_cursor.execute(testseq_data_sql)
    xindus_db_conn.commit()

def getDeviceName():
    p = subprocess.Popen("adb shell getprop | findstr product.name", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    str_output = str(output, 'utf-8')
    buf = io.StringIO(str_output)
    device_name = buf.readline()
    dev=device_name.split(" ")[1].strip()
    device=dev.strip("[]")
    print("Inside getDeviceName device= ", device)
    return device

def getDDRSize():
    p = subprocess.Popen("adb shell cat /proc/meminfo | findstr MemTotal", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    str_output = str(output, 'utf-8')
    buf = io.StringIO(str_output)
    DDR_SIZE = buf.readline()
    size = int(DDR_SIZE.split(" ")[8])/(1024*1024)
    print("DDR Size = %.2f " % round(size,2))
    return round(size,2)

def getCPUCores():
     p = subprocess.Popen('adb shell "cat /proc/cpuinfo | grep -i 7"', stdout=subprocess.PIPE, shell=True)
     (output, err) = p.communicate()
     p_status = p.wait()
     str_output = str(output, 'utf-8')
     buf = io.StringIO(str_output)
     CPU_CORES = buf.readline()
     cpu = CPU_CORES.split(" ")[1]
     cpucores=int(cpu)+1
     print("No. of CPU Cores = ", cpucores)
     return cpucores

def getCPU():
     p = subprocess.Popen('adb shell "cat /proc/cpuinfo | grep -i qualcomm', stdout=subprocess.PIPE, shell=True)
     (output, err) = p.communicate()
     p_status = p.wait()
     str_output = str(output, 'utf-8')
     buf = io.StringIO(str_output)
     CPU = buf.readline()
     print("CPU = ", CPU.split(" ")[1])
     return CPU.split(" ")[1]

def getStorage():
    p = subprocess.Popen('adb shell "df -h | grep -i storage', stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    str_output = str(output, 'utf-8')
    buf = io.StringIO(str_output)
    Storage = buf.readline()
    print("Storage = ", Storage.split(" ")[6])
    return Storage.split(" ")[6]

def populate_device(xindus_db_conn, adb_id):
    print("Inside populate_device function")
    xindus_db_cursor = xindus_db_conn.cursor()
    name = getDeviceName()
    CPU = getCPU()
    Cores = getCPUCores()
    DDR_SIZE = getDDRSize()
    Storage = getStorage()
    print("adb_id = ", adb_id, "name = ", name , "CPU = ", CPU, "Cores = ", Cores, "DDR_SIZE = ", DDR_SIZE, "Storage = ", Storage)

    device_sql = "INSERT INTO DEVICE(DEVICE_ID,NAME,CPU_HARDWARE,CPU_CORES,DDR_SIZE,STORAGE) VALUES(%s,%s,%s,%s,%s,%s)"
    device_val = [
    (adb_id,name,CPU,Cores,DDR_SIZE,Storage)
    ]
    xindus_db_cursor.executemany(device_sql,device_val)
    xindus_db_conn.commit()
def populate_tables(xindus_db_conn,adb_id):
    print("Inside populate_tables")
    populate_tools(xindus_db_conn)
    populate_device(xindus_db_conn,adb_id)
    #populate_Subsystems(xindus_db_conn)
    #insert_runid_testingseq(xindus_db_conn,run_id)
    #insert_Tetsingseq_data(xindus_db_conn,run_id)


def init_db(mySQLUser, mySQLPort, mySQLPassword):
  print("mySQLPort = ", mySQLPort)
  connection = mysql.connector.connect(
    host="localhost",
    user=mySQLUser,
    port=int(mySQLPort),
    passwd=mySQLPassword,
  )
  xindus_db_cursor = connection.cursor()
  xindus_db_cursor.execute("Create database IF NOT EXISTS Xindus_DB ")
  connection.commit()
  xindus_db_conn = create_tables(mySQLUser, mySQLPort, mySQLPassword)

