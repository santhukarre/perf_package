import mysql.connector


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
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS DEVICE(DEVICE_ID VARCHAR(255) PRIMARY KEY,NAME VARCHAR(255),CPU VARCHAR(255),CORES INT,DDR_SIZE INT,DDR_VENDOR INT,STORAGE INT,STORAGE_VENDOR INT)")
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS TOOLS(NAME VARCHAR(255),ID INT AUTO_INCREMENT PRIMARY KEY,CATEGORY VARCHAR(255))")
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS SUBSYSTEMS(ID INT, FOREIGN KEY SUBSYSTEMS(ID) REFERENCES TOOLS(ID),SUSSYSTEM VARCHAR(255))")
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS RUN(RUN_ID INT PRIMARY KEY,START_DATE VARCHAR(255),START_TIME VARCHAR(255),END_DATE VARCHAR(255),END_TIME VARCHAR(255),MODE VARCHAR(255))")
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS KPIS(KPI_ID INT AUTO_INCREMENT,NAME VARCHAR(255),UNITS VARCHAR(255),PRIMARY KEY(KPI_ID))")
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS RUN_KPI(RUN_ID INT,CONSTRAINT fk_category_3 FOREIGN KEY (RUN_ID) REFERENCES RUN(RUN_ID),KPI_ID INT NOT NULL,CONSTRAINT fk_category_4 FOREIGN KEY (KPI_ID) REFERENCES KPIS(KPI_ID),END_DATE VARCHAR(255),END_TIME VARCHAR(255))")
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS TESTING_SEQUENCE(RUN_ID INT NOT NULL,CONSTRAINT fk_category_7 FOREIGN KEY (RUN_ID) REFERENCES RUN(RUN_ID),ID INT,CONSTRAINT fk_category_8 FOREIGN KEY (ID) REFERENCES TOOLS(ID),START_TIME VARCHAR(255),END_TIME VARCHAR(255))")
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS BENCHMARK_RESULT(RUN_ID INT,ID INT,CONSTRAINT fk_category_12 FOREIGN KEY (ID) REFERENCES TOOLS(ID),RESULT_ID INT)")
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
  ]
  xindus_db_cursor.executemany(tools_sql, tools_val)
  xindus_db_conn.commit()
def populate_kpi(xindus_db_conn):
  xindus_db_cursor = xindus_db_conn.cursor()
  kpi_sql = "INSERT INTO KPIS(NAME,UNITS) VALUES (%s, %s)"
  kpi_val = [
    ('FLASH_SEQ_READ', 'MBPS'),
    ('FLASH_SEQ_WRITE', 'MBPS'),
    ('FLASH_RAND_READ', 'MBPS'),
    ('FLASH_RAND_WRITE', 'MBPS'),
    ('SQLITE_INSERT', 'QPS'),
    ('SQLITE_UPDATE', 'QPS'),
    ('SQLITE_DELETE', 'QPS'),
  ]
  xindus_db_cursor.executemany(kpi_sql, kpi_val)
  xindus_db_conn.commit()
def populate_tables(xindus_db_conn):
    populate_tools(xindus_db_conn)
    populate_kpi(xindus_db_conn)

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
  populate_tables(xindus_db_conn)

