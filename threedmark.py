from appium import webdriver
from Run import pull_screenshots
import time
SlingopenGL_overall=""
SlingopenGL_physics=""
SlingopenGL_graphics=""
Sling_overall=""
Sling_graphics=""
Sling_physics=""
Slingshot_overall=""
Slingshot_graphics=""
Slingshot_physics=""
API_OPENGL=""
API_VULKAN=""

def is_element_found(appium_web_driver, sec, element_id):
    try:
        print("sleeping for ", sec, " seconds to find the element")
        appium_web_driver.implicitly_wait(sec)
        found_element_id = appium_web_driver.find_element_by_xpath(element_id)
        return True
    except:
        print("exception occured")
        return False

found_element_id = ""
def wait_for_element(appium_web_driver, secs, element_id):
   global  found_element_id
   each_iteration_sleep = 50
   iterations = (int)(secs/each_iteration_sleep)
   print("Total iterations  = ", iterations)
   for i in range(1, iterations):
        print("iteration no. = ", i )
        element_found = is_element_found(appium_web_driver, each_iteration_sleep, element_id)
        if(element_found == True):
            global  found_element_id
            found_element_id = appium_web_driver.find_element_by_xpath(element_id)
            break
        if(element_found == False):
            print("Sleeping explicilty for 5 seconds")
            time.sleep(5)
   return found_element_id

def store_threedmark_result(xindus_db_conn, result_id_list):
    xindus_db_cursor = xindus_db_conn.cursor()
    sql_read = "select * from THREEDMARK_RESULT"
    xindus_db_cursor.execute(sql_read)
    data = xindus_db_cursor.fetchall()
    print("Total number of rows is ", xindus_db_cursor.rowcount)
    file = open("results.csv", "w+")
    file.write("Result id,slingopenGL_overall,slingopenGL_physics,slingopenGL_graphics,sling_overall,sling_graphics,sling_physics,slingshot_overall,slingshot_graphics,slingshot_physics,API_OpenGL,API_Vulkan")
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
       file.write(",")
       file.write(str(row[5]))
       file.write(",")
       file.write(str(row[6]))
       file.write(",")
       file.write(str(row[7]))
       file.write(",")
       file.write(str(row[8]))
       file.write(",")
       file.write(str(row[9]))
       file.write(",")
       file.write(str(row[10]))
       file.write(",")
       file.write(str(row[11]))
       file.write("\n")
def get_threedmark_result_id(xindus_db_conn):
    xindus_db_cursor = xindus_db_conn.cursor()
    sql_read = "select MAX(RESULT_ID) from THREEDMARK_RESULT"
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
def insert_threedmark_result(xindus_db_conn, run_id):
    global SlingopenGL_overall, SlingopenGL_physics, SlingopenGL_graphics, Sling_overall, Sling_graphics, Sling_physics, Slingshot_overall, Slingshot_graphics, Slingshot_physics, API_OPENGL, API_VULKAN

    xindus_db_cursor = xindus_db_conn.cursor()
    result_id = get_threedmark_result_id(xindus_db_conn)

    benchmark_rslt_sql = "INSERT INTO BENCHMARK_RESULT(RUN_ID, ID, RESULT_ID) VALUES (%s,%s,%s)"
    benchmark_rslt_val = [
        (run_id,'3',result_id),     # 3 is the ANDROBENCH_TOOL_ID
    ]
    xindus_db_cursor.executemany(benchmark_rslt_sql, benchmark_rslt_val)
    xindus_db_conn.commit()

    threedmark_sql = "INSERT INTO THREEDMARK_RESULT(RESULT_ID,SLINGOPENGL_OVERALL,SLINGOPENGL_PHYSICS,SLINGOPENGL_GRAPHICS,SLING_OVERALL,SLING_GRAPHICS,SLING_PHYSICS,SLINGSHOT_OVERALL,SLINGSHOT_GRAPHICS,SLINGSHOT_PHYSICS,API_OPENGL,API_VULKAN) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    threedmark_val = [
        (result_id,SlingopenGL_overall,SlingopenGL_physics,SlingopenGL_graphics,Sling_overall,Sling_graphics,Sling_physics, Slingshot_overall, Slingshot_graphics, Slingshot_physics, API_OPENGL, API_VULKAN)
    ]
    xindus_db_cursor.executemany(threedmark_sql,threedmark_val)
    xindus_db_conn.commit()
def run_3dmark(adb_id,xindus_db_conn, run_id):
    global SlingopenGL_overall,SlingopenGL_physics,SlingopenGL_graphics,Sling_overall,Sling_graphics,Sling_physics,Slingshot_overall,Slingshot_graphics,Slingshot_physics,API_OPENGL,API_VULKAN
    print("Running Threedmark on device with adb_id =", adb_id)
    desired_cap = {
        "deviceName": adb_id,
        "platformName": "android",
        "appPackage": "com.futuremark.dmandroid.application",
        "appActivity": "com.futuremark.flamenco.ui.splash.SplashPageActivity",
        "noReset": True,
        "connectionRetryTimeout": 10000,
        "connectionRetryCount": 3,
        "automationName": "uiautomator1",
        "newCommandTimeout": 200000
    }
    print("adb_device_id = ", adb_id)
    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
    driver.implicitly_wait(20)
    #continue_btn = driver.find_element_by_id('android:id/button1')
    #continue_btn.click()

    #driver.implicitly_wait(20)
    #warning_btn = driver.find_element_by_id('com.android.packageinstaller:id/permission_allow_button')
    #warning_btn.click()

    #driver.implicitly_wait(200)
    #print("after implicit wait of 100 seconds");

    #btn = driver.find_element_by_id('com.futuremark.dmandroid.application:id/flm_fab_benchmark')
    #btn.click()


    run_sling = driver.find_element_by_id('com.futuremark.dmandroid.application:id/flm_fab_progress_circle')
    run_sling.click()

    slingopenGL_overall=wait_for_element(driver,850,'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.TextView[2]')
    SlingopenGL_overall = slingopenGL_overall.text
    print('sling shot extreme OpenGL overall score :',slingopenGL_overall.text)
    slingopenGL_graphics=driver.find_element_by_xpath(' /hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[2]/android.widget.TextView[2]')
    SlingopenGL_graphics=slingopenGL_graphics.text
    print('sling shot extreme OpenGL graphics score :', slingopenGL_graphics.text)
    slingopenGL_physics=driver.find_element_by_xpath(' /hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[3]/android.widget.TextView[2]')
    SlingopenGL_physics=slingopenGL_physics.text
    print('sling shot extreme OpenGL physics score :', slingopenGL_physics.text)
    sling_overall =driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.TextView[2]')
    Sling_overall=sling_overall.text
    print('sling shot extreme Vulkan overall score :', sling_overall.text)
    sling_graphics=driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[2]/android.widget.TextView[2]')
    Sling_graphics=sling_graphics.text
    print('sling shot extreme Vulkan graphics score :', sling_graphics.text)
    sling_physics=driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[3]/android.widget.TextView[2]')
    Sling_physics=sling_physics.text
    print('sling shot extreme Vulkan physics score :', sling_physics.text)
    pull_screenshots(run_id, "3dmark","C:\KnowledgeCenter\Xindus\Code\Perf_package_final\OnePlusDeviceReports\\apps_data")
    nav_back =driver.find_element_by_xpath('//android.widget.ImageButton[@content-desc="Navigate up"]')
    nav_back.click()
    goto_slingshot = driver.find_element_by_xpath('//android.support.v7.app.ActionBar.Tab[@content-desc="Sling Shot"]/android.widget.TextView')
    goto_slingshot.click()
    driver.implicitly_wait(10)
    run_slingshot = driver.find_element_by_id('com.futuremark.dmandroid.application:id/flm_fab_progress_circle')
    run_slingshot.click()

    slingshot_overall = wait_for_element(driver,850,'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.TextView[2]')
    Slingshot_overall=slingshot_overall.text
    print('sling shot Vulkan overall score :', slingshot_overall.text)
    slingshot_graphics=driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[2]/android.widget.TextView[2]')
    Slingshot_graphics=slingshot_graphics.text
    print('sling shot Vulkan graphics score :', slingshot_graphics.text)
    slingshot_physics=driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[5]/android.widget.TextView[2]')
    Slingshot_physics=slingshot_physics.text
    print('sling shot Vulkan physics score :', slingshot_physics.text)
    pull_screenshots(run_id, "3dmark_SLING","C:\KnowledgeCenter\Xindus\Code\Perf_package_final\OnePlusDeviceReports\\apps_data")
    Back = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.ImageButton')
    Back.click()
    goto_API = driver.find_element_by_xpath('//android.support.v7.app.ActionBar.Tab[@content-desc="API Overhead"]/android.widget.TextView')
    goto_API.click()
    driver.implicitly_wait(10)
    run_API = driver.find_element_by_id('com.futuremark.dmandroid.application:id/flm_fab_progress_circle')
    run_API.click()
    API_OpenGL =wait_for_element(driver,850,'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.TextView[2]')
    API_OPENGL=API_OpenGL.text
    print('API OpenGL Drawcalls/sec score :', API_OpenGL.text)
    API_Vulkan = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[2]/android.widget.TextView[2]')
    API_VULKAN=API_Vulkan.text
    print('API Vulkan Drawcalls/sec score :', API_Vulkan.text)

    insert_threedmark_result(xindus_db_conn, run_id)
    store_threedmark_result(xindus_db_conn, [1, 2])
    pull_screenshots(run_id, "3dmark_API","C:\KnowledgeCenter\Xindus\Code\Perf_package_final\OnePlusDeviceReports\\apps_data")



