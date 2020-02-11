import mysql.connector

def get_xindus_db_conn():
  xindus_db_con = mysql.connector.connect(
    host="localhost",
    user="root",
    port=3307,
    passwd="XINDUS",
    database="Xindus_DB"
  )
  return xindus_db_con

def create_tables():
  xindus_db_con = mysql.connector.connect(
    host="localhost",
    user="root",
    port=3307,
    passwd="XINDUS",
    database="Xindus_DB"
  )
  xindus_db_cursor = xindus_db_con.cursor()
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS DEVICE(DEVICE_ID VARCHAR(255) PRIMARY KEY,NAME VARCHAR(255) NOT NULL,CPU VARCHAR(255)  NOT NULL,CORES INT NOT NULL,DDR_SIZE INT NOT NULL,DDR_VENDOR INT NOT NULL,STORAGE INT NOT NULL,STORAGE_VENDOR INT NOT NULL)")
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS TOOLS(NAME VARCHAR(255) NOT NULL,ID INT AUTO_INCREMENT PRIMARY KEY,CATEGORY VARCHAR(255) NOT NULL)")
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS SUBSYSTEMS(ID INT NOT NULL, FOREIGN KEY SUBSYSTEMS(ID) REFERENCES TOOLS(ID),SUSSYSTEM VARCHAR(255) NOT NULL)")
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS RUN(START_DATE VARCHAR(255) NOT NULL,START_TIME VARCHAR(255) NOT NULL,END_DATE VARCHAR(255) NOT NULL,END_TIME VARCHAR(255) NOT NULL,MODE VARCHAR(255) NOT NULL,Duartion VARCHAR(255) NOT NULL,RUN_ID INT AUTO_INCREMENT PRIMARY KEY)")
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS KPIS(KPI_ID INT NOT NULL AUTO_INCREMENT,NAME VARCHAR(255) NOT NULL,UNITS VARCHAR(255) NOT NULL,PRIMARY KEY(KPI_ID))")
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS DEVICE_THEORITICAL_KPI(DEVICE_ID VARCHAR(255),CONSTRAINT fk_category_1 FOREIGN KEY (DEVICE_ID) REFERENCES DEVICE(DEVICE_ID),KPI_ID INT NOT NULL,CONSTRAINT fk_category_2 FOREIGN KEY (KPI_ID) REFERENCES KPIS(KPI_ID),MIN_VALUE INT NOT NULL,MAX_VALUE INT NOT NULL)")
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS RUN_KPI(RUN_ID INT NOT NULL,CONSTRAINT fk_category_3 FOREIGN KEY (RUN_ID) REFERENCES RUN(RUN_ID),KPI_ID INT NOT NULL,CONSTRAINT fk_category_4 FOREIGN KEY (KPI_ID) REFERENCES KPIS(KPI_ID),END_DATE INT NOT NULL,END_TIME INT NOT NULL,MAX_VALUE INT NOT NULL)")
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS TESTING_SEQUENCE(RUN_ID INT NOT NULL,CONSTRAINT fk_category_7 FOREIGN KEY (RUN_ID) REFERENCES RUN(RUN_ID),ID INT NOT NULL,CONSTRAINT fk_category_8 FOREIGN KEY (ID) REFERENCES TOOLS(ID),START_TIME INT NOT NULL,END_TIME INT NOT NULL,DURATION INT NOT NULL)")
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS BENCHMARK_RESULT(RUN_ID INT,CONSTRAINT fk_category FOREIGN KEY (RUN_ID) REFERENCES RUN(RUN_ID),ID INT,CONSTRAINT fk_category_12 FOREIGN KEY (ID) REFERENCES TOOLS(ID),RESULT_ID INT NOT NULL)")
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS ANDROBENCH_RESULT(RESULT_ID INT,KPI_ID INT NOT NULL,CONSTRAINT fk_category_13 FOREIGN KEY (KPI_ID) REFERENCES KPIS(KPI_ID),Value INT NOT NULL)")
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS ANTUTU_RESULT(RESULT_ID INT,RESULT_SCORES VARCHAR(255))")
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS GEEKBENCH_RESULT(RESULT_ID INT,OPENCL_SCORES VARCHAR(255))")
  xindus_db_cursor.execute("Create Table  IF NOT EXISTS LMBENCH_RESULT(RESULT_ID INT, BYTES_Transferred INT NOT NULL,DDR_BW INT NOT NULL)")
  xindus_db_con.commit()

def init_db():
  connection = mysql.connector.connect(
    host="localhost",
    user="root",
    port=3307,
    passwd="XINDUS"
  )
  xindus_db_cursor = connection.cursor()
  xindus_db_cursor.execute("Create database IF NOT EXISTS Xindus_DB ")
  connection.commit()
  create_tables()
