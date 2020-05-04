from appium import webdriver
from db_interface import init_db, get_xindus_db_conn
import time
from adb_utility import get_adb_device_id, launch_xindusapp, adb_id
from Run import get_run_id,update_run_start_time, update_run_end_time, insert_run_data,insert_runid,pull_screenshots,generaterun_Report
from Androbench import run_androbench,insert_androbench_result,generate_Androbench_Report
from LMBench import run_lmbench,insert_lmbench_result,store_lmbench_result
from Geekbench import run_geekbench,insert_geekbench_result,store_geekbench_result,generate_Geekbench_Report
from Antutu import run_antutu,insert_antutu_result,store_antutu_result,generate_Antutu_Report
from threedmark import run_3dmark,insert_threedmark_result,store_threedmark_result, generate_ThreeDmark_Report
from db_interface import populate_tables
from Report import sendReport_ThroughMail
from xindusapp import run_xindusapp,generate_XindusApp_Report,generate_XindusApp_Report_Freq
from xindus_console_app import run_xindus_console_app
import configparser

import sys
import getpass
import xlsxwriter

mySQLUser = "root"
mySQLPort = "3306"
mySQLPassword = ""
emailId = "santhoshkarre956@gmail.com"
password = ""
logsPath = ""
runids = ""

xindus_app = False
androbench = False
lmbench = False
geekbench = False
threedmark = False
gfx = False
antutu = False

def parseConfigFile():
    global xindus_app, androbench, lmbench, geekbench, threedmark, gfx, antutu
    global dbOneTimeConfig, mySQLUser, mySQLPort, emailId, logsPath
    global xindusAppThreads, xindusAppIterations, xindusAppDDROnly, xindusAppFreeqResidency, xindusAppLogLevel,xindusAndroidApp,xindusAppBuffers

    parser = configparser.ConfigParser()
    parser.read('.\Release\\Perf_Package\\xindusconfig.ini')

    print("Sections : ", parser.sections())
    print("Xindus_Performance Package configuration")
    dbOneTimeConfig = parser.getint('Xindus_Performance_Package', 'OneTimeConfig')
    mySQLUser = parser.get('Xindus_Performance_Package', 'MySQLUserName')
    mySQLPort = parser.get('Xindus_Performance_Package', 'MySQLPort')
    emailId = parser.get('Xindus_Performance_Package', 'Email')
    logsPath = parser.get('Xindus_Performance_Package', 'LogFile')

    xindus_app = parser.getboolean('BenchMarks', 'Xindus_App')
    androbench = parser.getboolean('BenchMarks', 'Androbench')
    lmbench = parser.getboolean('BenchMarks', 'Lmbench')
    geekbench = parser.getboolean('BenchMarks', 'Geekbench')
    threedmark = parser.getboolean('BenchMarks', '3DMark')
    gfx = parser.getboolean('BenchMarks', 'Gfx')
    antutu = parser.getboolean('BenchMarks', 'Antutu')

    xindus_app = parser.getboolean('BenchMarks', 'Xindus_App')
    androbench = parser.getboolean('BenchMarks', 'Androbench')
    lmbench = parser.getboolean('BenchMarks', 'Lmbench')
    geekbench = parser.getboolean('BenchMarks', 'Geekbench')
    threedmark = parser.getboolean('BenchMarks', '3DMark')
    gfx = parser.getboolean('BenchMarks', 'Gfx')
    antutu = parser.getboolean('BenchMarks', 'Antutu')

    print("Xindus_App :", xindus_app)
    print("androbench :", androbench)
    print("lmbench :", lmbench)
    print("geekbench :", geekbench)
    print("threedmark :", threedmark)
    print("gfx :", gfx)
    print("antutu :", antutu)
    print("\n")
    print("Xindus_App configuration:")
    xindusAppThreads = parser.get('Xindus_App', 'Threads')
    xindusAppIterations = parser.get('Xindus_App', 'Iterations')
    xindusAppDDROnly = parser.get('Xindus_App', 'Optimized')
    xindusAppFreeqResidency = parser.get('Xindus_App', 'Frequency')
    xindusAppLogLevel = parser.get('Xindus_App', 'LogLevel')
    xindusAndroidApp = parser.getboolean('Xindus_App', 'AndroidApp')
    xindusAppBuffers = parser.get('Xindus_App', 'Buffers')
    print("Threads : ", xindusAppThreads)
    print("Iterations : ", xindusAppIterations)
    print("Frequency : ", xindusAppFreeqResidency)
    print("Optimized : ", xindusAppDDROnly)
    print("LogLevel : ", xindusAppLogLevel)
    print("XindusAndroidApp : ", xindusAndroidApp)
    print("XindusBuffers : ", xindusAppBuffers)

    if (xindus_app == True):
        print("xindus_app configured")
    else:
        print("xindsu_app not configured")

    if (threedmark == True):
        print("threedmark configured")
    else:
        print("threedmark not configured")

def createXindusReport():
    workbook = xlsxwriter.Workbook('.\Xindus_PerfReport.xlsx')
    worksheet = workbook.add_worksheet()

    workbook.close()


def generateReportWithRunIds(xindus_db_conn,runids):
    mycursor = xindus_db_conn.cursor()
    print("select no of inputs to compare results")
    n=int(input())
    print(n)
    print("select run_ids to compare")
    runids = []
    for row in range(n):
        runid=int(input())
        runids.append(runid)
        print(runids)
        sql_select = "select * from run where run_id = %s"
        mycursor.execute(sql_select,(runid,))
        data = mycursor.fetchall()
        print(data)
    print(runids)
    Tools = []
    for i in runids:
         sql_read="select * from benchmark_result where run_id = %s"
         mycursor.execute(sql_read,(i,))
         data = mycursor.fetchall()
         print(data)
         Tools.append(data)
    print("select no of benchmarks inputs to generate graphs")
    a = int(input())
    print(a)
    print("select benchmarks to Compare results with graph")
    for row in range(a):
        name = input()
        if(name=='Androbench'):
            generate_Androbench_Report(xindus_db_conn,runids)
        elif(name=='Antutu'):
            generate_Antutu_Report(xindus_db_conn,runids)
        elif(name=='3DMARK'):
            generate_ThreeDmark_Report(xindus_db_conn)
        elif(name=='GEEKBENCH'):
           generate_Geekbench_Report(xindus_db_conn)
        elif(name=='XINDUSAPP'):
            generate_XindusApp_Report(xindus_db_conn)
            generate_XindusApp_Report_Freq(xindus_db_conn)
        else:
            print('select any benchmarks')

def run_all_perf_tools(adb_id):
    global mySQLUser, mySQLPassword, mySQLPort, logsPath
    global xindus_app, androbench, lmbench, geekbench, threedmark, gfx, antutu

    xindus_db_conn = get_xindus_db_conn(mySQLUser, mySQLPort, mySQLPassword)
    run_id = get_run_id(xindus_db_conn)

    update_run_start_time()
    insert_runid(xindus_db_conn,run_id, adb_id)
    createXindusReport()
    if (xindus_app == True):
        if(xindusAndroidApp == True):
            run_xindusapp(adb_id, xindus_db_conn, run_id, logsPath, xindusAppThreads, xindusAppIterations, xindusAppDDROnly,xindusAppFreeqResidency,xindusAppLogLevel,xindusAppBuffers)
        else:
            run_xindus_console_app(xindus_db_conn, run_id, logsPath, xindusAppThreads, xindusAppIterations, xindusAppDDROnly,xindusAppFreeqResidency,xindusAppLogLevel,xindusAppBuffers)
    if(androbench == True):
         run_androbench(adb_id, xindus_db_conn, run_id, logsPath)
    if(antutu == True):
         run_antutu(adb_id, xindus_db_conn, run_id, logsPath)
    if(threedmark == True):
         run_3dmark(adb_id, xindus_db_conn, run_id, logsPath)
    if(geekbench == True):
         run_geekbench(adb_id, xindus_db_conn, run_id, logsPath)
    if(lmbench == True):
         run_lmbench(1024,'rd', xindus_db_conn, run_id, logsPath)
    populate_tables(xindus_db_conn, adb_id)
    update_run_end_time()
    insert_run_data(xindus_db_conn, run_id)
    generateReportWithRunIds(xindus_db_conn, runids)
    generaterun_Report(xindus_db_conn)
    # sendReport_ThroughMail()

def one_time_config():
    global mySQLUs,er, mySQLPassword, mySQLPort
    init_db(mySQLUser, mySQLPort, mySQLPassword)

dbOneTimeConfig = '0'
def printDefaultArgs():
    global dbOneTimeConfig, mySQLUser, mySQLPassword, mySQLPort, emailId, password
    print("dbOneTimeConfig =", dbOneTimeConfig)
    print("emailid =", emailId)
    print("Enter email password")
    password=input()
    print("password corresponding to emailid = ", emailId, "is =", password)
    print("mySQLUser =", mySQLUser)
    print("mySQLPort =", mySQLPort)
    print("Enter mySQLPassword")
    mySQLPassword=input()
    print("MYSQL password corresponding to mysqluser =", mySQLUser, "is =", mySQLPassword)

def printCmdArgs():
    global dbOneTimeConfig, mySQLUser, mySQLPassword, mySQLPort, emaildId,password, logsPath
    program_name = sys.argv[0]
    argsCount = len(sys.argv)
    if(argsCount < 2):
        print("XindusAutomation.py <onetime db configuration> <testing email id> <mysql username> <mysql port> <screenshots path>")
        printDefaultArgs()
        print("proceed with the default args")
        proceedWithDefaultArgs = 'y' #input()
        if(proceedWithDefaultArgs == 'y'):
            return;
        else:
            exit()
    dbOneTimeConfig = sys.argv[1]

    emailId = sys.argv[2]
    mySQLUser = sys.argv[3]
    mySQLPort = sys.argv[4]
    logsPath = sys.argv[5]

    print("dbOneTimeConfig = ", dbOneTimeConfig)
    if (dbOneTimeConfig == '1'):
        print("DB Config required")
        one_time_config()
    if (dbOneTimeConfig == '0'):
        print("DB Config is NOT required")
    print("emailID = ", emailId)
    print("password corresponding to emailid = ", emailId)
    try:
        password = getpass.getpass()
    except Exception as error:
        print('ERROR', error)
    else:
        print('Password entered:', password)

    print("mySQLUser = ", mySQLUser)
    print("mySQLPort = ", mySQLPort)
    print("MYSQL password corresponding to mysqluser = ", mySQLUser)
    try:
        mySQLPassword = getpass.getpass()
    except Exception as error:
        print('ERROR', error)
    else:
        print('MYSQL Password entered:', mySQLPassword)

def main():
    global dbOneTimeConfig
    parseConfigFile()
    printCmdArgs()
    if (dbOneTimeConfig == 1):
        print("DB Config required")
        one_time_config()
        print("one time done")
    if (dbOneTimeConfig == 0):
        print("DB Config is NOT required")
    print("password = ", password)
    adb_id = "7a9d2cc6"
    print("inside main adb_id = ", adb_id)
    run_all_perf_tools(adb_id)

    print("")

main()