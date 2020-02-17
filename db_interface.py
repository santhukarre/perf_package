import mysql.connector

def get_xindus_db_conn():
  xindus_db_con = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="XINDUS",
    port = 3307,
    database="Xindus_DB"
  )
  return xindus_db_con

def create_tables():
  xindus_db_con = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="XINDUS",
    port=3307,
    database="Xindus_DB"
  )
  xindus_db_cursor = xindus_db_con.cursor()
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS DEVICE(DEVICE_ID VARCHAR(255) PRIMARY KEY,NAME VARCHAR(255) NOT NULL,CPU VARCHAR(255)  NOT NULL,CORES INT NOT NULL,DDR_SIZE INT NOT NULL,DDR_VENDOR INT NOT NULL,STORAGE INT NOT NULL,STORAGE_VENDOR INT NOT NULL)")
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS TOOLS(NAME VARCHAR(255) NOT NULL,ID INT AUTO_INCREMENT PRIMARY KEY,CATEGORY VARCHAR(255) NOT NULL)")
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS SUBSYSTEMS(ID INT NOT NULL, FOREIGN KEY SUBSYSTEMS(ID) REFERENCES TOOLS(ID),SUSSYSTEM VARCHAR(255) NOT NULL)")
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS RUN(RUN_ID INT PRIMARY KEY,START_DATE VARCHAR(255),START_TIME VARCHAR(255) ,END_DATE VARCHAR(255),END_TIME VARCHAR(255),MODE VARCHAR(255))")
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS KPIS(KPI_ID INT NOT NULL AUTO_INCREMENT,NAME VARCHAR(255) NOT NULL,UNITS VARCHAR(255) NOT NULL,PRIMARY KEY(KPI_ID))")
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS RUN_KPI(RUN_ID INT NOT NULL,CONSTRAINT fk_category_3 FOREIGN KEY (RUN_ID) REFERENCES RUN(RUN_ID),KPI_ID INT NOT NULL,CONSTRAINT fk_category_4 FOREIGN KEY (KPI_ID) REFERENCES KPIS(KPI_ID),END_DATE INT NOT NULL,END_TIME INT NOT NULL,MAX_VALUE INT NOT NULL)")
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS TESTING_SEQUENCE(RUN_ID INT NOT NULL,CONSTRAINT fk_category_7 FOREIGN KEY (RUN_ID) REFERENCES RUN(RUN_ID),ID INT NOT NULL,CONSTRAINT fk_category_8 FOREIGN KEY (ID) REFERENCES TOOLS(ID),START_TIME INT NOT NULL,END_TIME INT NOT NULL,DURATION INT NOT NULL)")
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS BENCHMARK_RESULT(RUN_ID INT,CONSTRAINT fk_category FOREIGN KEY (RUN_ID) REFERENCES RUN(RUN_ID),ID INT,CONSTRAINT fk_category_12 FOREIGN KEY (ID) REFERENCES TOOLS(ID),RESULT_ID INT NOT NULL)")
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS ANDROBENCH_RESULT(RESULT_ID INT, SEQ_READ  VARCHAR(25), SEQ_WRITE VARCHAR(25), RAND_READ VARCHAR(25), RAND_WRITE VARCHAR(25), SQL_INSERT VARCHAR(25), SQL_UPDATE VARCHAR(25), SQL_DELETE VARCHAR(25))")
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS ANTUTU_RESULT(RESULT_ID INT,ANTUTU_TOTAL_SCORE VARCHAR(255),ANTUTU_CPU_SCORE VARCHAR(255),ANTUTU_MEMORY_SCORE VARCHAR(255),ANTUTU_UX_SCORE VARCHAR(255))")
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS GEEKBENCH_RESULT(RESULT_ID INT,SINGLE_CORE_ELEMENT VARCHAR(255),MULTI_CORE_ELEMENT VARCHAR(255),OPENCL_SCORE_ELEMENT VARCHAR(255))")
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS LMBENCH_RESULT(RESULT_ID INT, BYTES_Transferred INT NOT NULL,DDR_BW INT NOT NULL)")
  xindus_db_con.commit()
  return xindus_db_con

def populate_tools(xindus_db_conn):
  xindus_db_cursor = xindus_db_conn.cursor()
  tools_sql = "INSERT INTO TOOLS(NAME, CATEGORY) VALUES (%s, %s)"
  tools_val = [
    ('ANDROBENCH', 'PERF'),
    ('ANTUTU', 'PERF'),
    ('GEEKBENCH', 'PERF'),
    ('3DMARK', 'PERF'),
    ('LMBENCH', 'PERF'),
    ('GFXBENCH', 'PERF'),
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

def init_db():
  connection = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="XINDUS",
    port = 3307,
  )
  xindus_db_cursor = connection.cursor()
  xindus_db_cursor.execute("Create database IF NOT EXISTS Xindus_DB ")
  connection.commit()
  xindus_db_conn = create_tables()
  populate_tables(xindus_db_conn)

