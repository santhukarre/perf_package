from appium import webdriver
from Run import insert_runid
import time
def store_antutu_result(xindus_db_conn, result_id_list):
    xindus_db_cursor = xindus_db_conn.cursor()
    sql_read = "select * from ANTUTU_RESULT"
    xindus_db_cursor.execute(sql_read)
    data = xindus_db_cursor.fetchall()
    print("Total number of rows is ", xindus_db_cursor.rowcount)
    file = open("results.csv", "w+")
    file.write("Result id,Antutu_total_score,Antutu_cpu_score,Antutu_memory_score,Antutu_ux_score")
    file.write("\n")
    for row in data:
       file.write(str(row[0]))
       file.write(",")
       file.write(str(row[1]))
       file.write(",")
       file.write(str(row[2]))
       file.write(",")
       file.write(str(row[3]))
       file.write(",")
       file.write(str(row[4]))
       file.write("\n")

def get_antutu_result_id(xindus_db_conn):
    xindus_db_cursor = xindus_db_conn.cursor()
    sql_read = "select MAX(RESULT_ID) from ANTUTU_RESULT"
    xindus_db_cursor.execute(sql_read)
    data = xindus_db_cursor.fetchall()
    print("Total number of rows is ", xindus_db_cursor.rowcount)
    for row in data:
        result_id = row[0]
        print("row [0] = ", row[0])
    if(result_id == None):
        result_id = 1
    else:
        print("result_id = ", result_id)
        result_id = result_id + 1
    return result_id



def insert_antutu_result(xindus_db_conn, run_id):
    global Antutu_total_score,Antutu_cpu_score,Antutu_memory_score, Antutu_ux_score



    xindus_db_cursor = xindus_db_conn.cursor()
    result_id = get_antutu_result_id(xindus_db_conn)

    benchmark_rslt_sql = "INSERT INTO BENCHMARK_RESULT(RUN_ID, ID, RESULT_ID) VALUES (%s,%s,%s)"
    benchmark_rslt_val = [
        (run_id,'3', result_id),     # 3 is the ANDROBENCH_TOOL_ID
    ]
    xindus_db_cursor.executemany(benchmark_rslt_sql, benchmark_rslt_val)
    xindus_db_conn.commit()

    antutu_sql = "INSERT INTO ANTUTU_RESULT(RESULT_ID,ANTUTU_TOTAL_SCORE,ANTUTU_CPU_SCORE,ANTUTU_MEMORY_SCORE,ANTUTU_UX_SCORE) VALUES (%s,%s,%s,%s,%s)"
    antutu_val = [
        (result_id,Antutu_total_score,Antutu_cpu_score,Antutu_memory_score,Antutu_ux_score),
    ]
    xindus_db_cursor.executemany(antutu_sql, antutu_val)
    xindus_db_conn.commit()


def run_antutu(adb_id,xindus_db_conn, run_id):
    print("Running Antutu on device with adb_id =", adb_id)
    desired_cap = {
        "deviceName": adb_id,
        "platformName": "android",
        "appPackage": "com.antutu.ABenchMark",
        "appActivity": "com.antutu.ABenchMark.ABenchMarkStart",
        "noReset": True,
        "automationName": "UiAutomator1"
    }
    appium_web_driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
    print('host successful')
    appium_web_driver.implicitly_wait(30)
    print('wait time')
    appium_web_driver.find_element_by_id('com.antutu.ABenchMark:id/main_test_finish_retest').click()
    print('start')
    #Wait for Test Completion
    appium_web_driver.implicitly_wait(1600)
    antutu_total_score = appium_web_driver.find_element_by_id('com.antutu.ABenchMark:id/main_test_finish_bg').click()
    appium_web_driver.implicitly_wait(10)
    print('Antutu Total Score :', antutu_total_score.text)
    #appium_web_driver.implicitly_wait(10)
    #antutu_cpu_score = appium_web_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[1]/android.view.ViewGroup/android.widget.TextView[1]')
    #antutu_cpu_score.click()
    #print('Antutu CPU Score :', antutu_cpu_score.text)
    #appium_web_driver.implicitly_wait(10)
    #antutu_memory_score = appium_web_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[2]/android.view.ViewGroup/android.widget.TextView[1]')
    #antutu_memory_score.click()
    #print('Antutu Memory Score :', antutu_memory_score.text)
    #appium_web_driver.implicitly_wait(10)
    #antutu_ux_score = appium_web_driver.find_element_by_xpath('	/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[4]/android.view.ViewGroup/android.widget.TextView[1]')
    #antutu_ux_score.click()
    #print('Antutu UX Score :', antutu_ux_score.text)
    # insert_antutu_result(xindus_db_conn, run_id)