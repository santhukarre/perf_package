from adb_utility import get_adb_device_id, launch_xindusapp
from Run import get_run_id
from Run import update_run_start_time, update_run_end_time, insert_run_data

from appium import webdriver
from db_interface import init_db, get_xindus_db_conn
from Androbench import run_androbench,insert_runid,insert_androbench_result, store_androbench_result
from Antutu import run_antutu
from Geekbench import run_geekbench
from threedmark import run_3dmark

def run_all_perf_tools():
    adb_id = get_adb_device_id()

    xindus_db_conn = get_xindus_db_conn()
    run_id = get_run_id(xindus_db_conn)
    print("Device adb_id = ", adb_id, "run_id = ", run_id);

    update_run_start_time()
    insert_runid(xindus_db_conn,run_id)
    run_androbench(adb_id, xindus_db_conn, run_id)
    insert_androbench_result(xindus_db_conn, run_id)
    #run_geekbench(adb_id)
    #run_antutu(adb_id)
    update_run_end_time()
    insert_run_data(xindus_db_conn, run_id)
    store_androbench_result(xindus_db_conn,[1,2])

def one_time_config():
    init_db()

def main():
    #one_time_config()
    run_all_perf_tools()
    launch_xindusapp()
    #run_3dmark(adb_id)
main()