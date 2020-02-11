from adb_utility import get_adb_device_id
from Run import get_run_id
from appium import webdriver
from db_interface import init_db, get_xindus_db_conn
from Androbench import run_androbench
from Antutu import run_antutu
from Geekbench import run_geekbench
from threedmark import run_3dmark

def run_all_perf_tools():
    adb_id = get_adb_device_id()
    xindus_db_conn = get_xindus_db_conn()
    run_id = get_run_id(xindus_db_conn)
    print("Device adb_id = ", adb_id, "run_id = ", run_id);
    run_androbench(adb_id, get_xindus_db_conn, run_id)
    run_geekbench(adb_id)
    run_antutu(adb_id)

def one_time_config():
    init_db()

def main():
    #one_time_config()
    #run_all_perf_tools()
    adb_id = get_adb_device_id()
    run_3dmark(adb_id)
main()