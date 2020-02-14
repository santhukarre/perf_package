from adb_utility import get_adb_device_id, launch_xindusapp
from Run import get_run_id
from Run import update_run_start_time, update_run_end_time, insert_run_data
from LMBench import run_lmbench,insert_lmbench_result,store_lmbench_result
from Geekbench import insert_geekbench_result,store_geekbench_result
from Antutu import insert_antutu_result,store_antutu_result

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
    #run_androbench(adb_id, xindus_db_conn, run_id)
   # insert_androbench_result(xindus_db_conn, run_id)
    #run_geekbench(adb_id,xindus_db_conn, run_id)
    run_antutu(adb_id,xindus_db_conn, run_id)
    #run_lmbench(1024, 'rd' , xindus_db_conn, run_id)
    # run_3dmark(adb_id)
    #insert_lmbench_result(xindus_db_conn, run_id)
    #insert_geekbench_result(xindus_db_conn, run_id)
    #insert_antutu_result(xindus_db_conn, run_id)
    update_run_end_time()
    insert_run_data(xindus_db_conn, run_id)
    #store_androbench_result(xindus_db_conn,[1,2])
    #store_lmbench_result(xindus_db_conn,run_id)
    #store_geekbench_result(xindus_db_conn, run_id)
    #store_antutu_result(xindus_db_conn, run_id)

def one_time_config():
    init_db()

def main():
    #one_time_config()
    run_all_perf_tools()
    #launch_xindusapp()

main()