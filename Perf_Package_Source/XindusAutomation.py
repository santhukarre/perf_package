from appium import webdriver
from db_interface import init_db, get_xindus_db_conn
import time
from adb_utility import get_adb_device_id, launch_xindusapp
from Run import get_run_id,update_run_start_time, update_run_end_time, insert_run_data,insert_runid,pull_screenshots
from Androbench import run_androbench,insert_androbench_result
from LMBench import run_lmbench,insert_lmbench_result,store_lmbench_result
from Geekbench import run_geekbench,insert_geekbench_result,store_geekbench_result
from Antutu import run_antutu,insert_antutu_result,store_antutu_result,generateAntutuReport
from threedmark import run_3dmark,insert_threedmark_result,store_threedmark_result, generateThreeDmarkReport

from Report import sendReportThroughMail
from Androbench import generateAndrobenchReport
from xindusapp import run_xindusapp

import sys
import getpass
import xlsxwriter

mySQLUser = "root"
mySQLPort = "3307"
mySQLPassword = "XINDUS"
emailId = "santhoshkarre956@gmail.com"
password = "Chaankya@gmail.com"
screenShotsPath = ""

def createXindusReport():
    workbook = xlsxwriter.Workbook('.\Xindus_PerfReport.xlsx')
    worksheet = workbook.add_worksheet()

    workbook.close()
	
def run_all_perf_tools():
    global mySQLUser, mySQLPassword, mySQLPort
    adb_id = get_adb_device_id()

    xindus_db_conn = get_xindus_db_conn(mySQLUser, mySQLPort, mySQLPassword)
    run_id = get_run_id(xindus_db_conn)
    print("Device adb_id = ", adb_id, "run_id = ", run_id);
    update_run_start_time()
    insert_runid(xindus_db_conn,run_id)
    createXindusReport()
    run_androbench(adb_id, xindus_db_conn, run_id, screenShotsPath)
    run_antutu(adb_id,xindus_db_conn, run_id, screenShotsPath)
    run_3dmark(adb_id,xindus_db_conn, run_id, screenShotsPath)
    run_geekbench(adb_id,xindus_db_conn, run_id, screenShotsPath)



    #run_lmbench(1024,'rd',xindus_db_conn, run_id, screenShotsPath)
    #run_xindusapp(7, 30, 1, 1, xindus_db_conn, run_id, screenShotsPath)

    update_run_end_time()
    insert_run_data(xindus_db_conn, run_id)
    sendReportThroughMail()

def one_time_config():
    global mySQLUser, mySQLPassword, mySQLPort
    init_db(mySQLUser, mySQLPort, mySQLPassword)

dbOneTimeConfig = '0'
def printDefaultArgs():
    global dbOneTimeConfig, mySQLUser, mySQLPassword, mySQLPort, emailId, password
    print("dbOneTimeConfig =", dbOneTimeConfig)
    print("emailid =", emailId)
    print("password corresponding to emailid = ", emailId, "is =", password)
    print("mySQLUser =", mySQLUser)
    print("mySQLPort =", mySQLPort)
    print("MYSQL password corresponding to mysqluser =", mySQLUser, "is =", mySQLPassword)

def printCmdArgs():
    global dbOneTimeConfig, mySQLUser, mySQLPassword, mySQLPort, emaildId,password, screenShotsPath
    program_name = sys.argv[0]
    argsCount = len(sys.argv)
    if(argsCount < 2):
        print("XindusAutomation.py <onetime db configuration> <testing email id> <mysql username> <mysql port> <screenshots path>")
        printDefaultArgs()
        print("proceed with the default args")
        proceedWithDefaultArgs = input()
        if(proceedWithDefaultArgs == 'y'):
            return;
        else:
            exit()
    dbOneTimeConfig = sys.argv[1]

    emailId = sys.argv[2]
    mySQLUser = sys.argv[3]
    mySQLPort = sys.argv[4]
    screenShotsPath = sys.argv[5]

    print("dbOneTimeConfig = ", dbOneTimeConfig)
    if (dbOneTimeConfig == '1'):
        print("DB Config required")
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
    printCmdArgs()
    if (dbOneTimeConfig == '1'):
        print("DB Config required")
        one_time_config()
    if (dbOneTimeConfig == '0'):
        print("DB Config is NOT required")
    print("password = ", password)
    run_all_perf_tools()
    #launch_xindusapp()

main()