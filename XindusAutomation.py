from appium import webdriver
from db_interface import init_db, get_xindus_db_conn
import time
from adb_utility import get_adb_device_id, launch_xindusapp
from Run import get_run_id,update_run_start_time, update_run_end_time, insert_run_data,insert_runid,pull_screenshots
from Androbench import run_androbench
from LMBench import run_lmbench,insert_lmbench_result,store_lmbench_result
from Geekbench import run_geekbench,insert_geekbench_result,store_geekbench_result
from Antutu import run_antutu,insert_antutu_result,store_antutu_result
from threedmark import run_3dmark,insert_threedmark_result,store_threedmark_result
from Report import sendReportThroughMail
from Androbench import generateAndrobenchReport

def run_all_perf_tools():
    adb_id = get_adb_device_id()

    xindus_db_conn = get_xindus_db_conn()
    run_id = get_run_id(xindus_db_conn)
    print("Device adb_id = ", adb_id, "run_id = ", run_id);
    update_run_start_time()
    #insert_runid(xindus_db_conn,run_id)
    #run_androbench(adb_id, xindus_db_conn, run_id)
    #run_geekbench(adb_id,xindus_db_conn, run_id)
    #run_antutu(adb_id,xindus_db_conn, run_id)
    #run_lmbench(1024, 'rd' , xindus_db_conn, run_id)
    #run_3dmark(adb_id,xindus_db_conn, run_id)

    #update_run_end_time()
    #insert_run_data(xindus_db_conn, run_id)
    generateAndrobenchReport(xindus_db_conn)
    sendReportThroughMail()

def one_time_config():
    init_db()

def main():
    #one_time_config()
    run_all_perf_tools()
    #launch_xindusapp()

main()