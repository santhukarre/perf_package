from appium import webdriver
import time
slingopenGL_overall=""
slingopenGL_physics=""
slingopenGL_graphics=""
sling_overall=""
sling_graphics=""
sling_physics=""
slingshot_overall=""
slingshot_graphics=""
slingshot_physics=""
API_OpenGL=""
API_Vulkan=""


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
    global slingopenGL_overall,slingopenGL_physics,slingopenGL_graphics,sling_overall,sling_graphics,sling_physics,slingshot_overall,slingshot_graphics,slingshot_physics,API_OpenGL,API_Vulkan

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
        (result_id,slingopenGL_overall,slingopenGL_physics,slingopenGL_graphics,sling_overall,sling_graphics,sling_physics,slingshot_overall,slingshot_graphics,slingshot_physics,API_OpenGL,API_Vulkan),
    ]
    xindus_db_cursor.executemany(threedmark_sql,threedmark_val)
    xindus_db_conn.commit()
def run_3dmark(adb_id,xindus_db_conn, run_id):
    print("Running Threedmark on device with adb_id =", adb_id)
    desired_cap = {
        "deviceName": adb_id,
        "platformName": "android",
        "appPackage": "com.futuremark.dmandroid.application",
        "appActivity": "com.futuremark.flamenco.ui.splash.SplashPageActivity",
        "noReset": True,
        "connectionRetryTimeout": 10000,
        "connectionRetryCount": 3,
        "automationName": "UiAutomator1",
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
    time.sleep(600)
    slingopenGL_overall=driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.TextView[2]')
    slingopenGL_overall.click()
    print('sling shot extreme OpenGL overall score :',slingopenGL_overall.text)
    slingopenGL_graphics=driver.find_element_by_xpath(' /hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[2]/android.widget.TextView[2]')
    slingopenGL_graphics.click()
    print('sling shot extreme OpenGL graphics score :', slingopenGL_graphics.text)
    slingopenGL_physics=driver.find_element_by_xpath(' /hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[3]/android.widget.TextView[2]')
    slingopenGL_physics.click()
    print('sling shot extreme OpenGL physics score :', slingopenGL_physics.text)
    sling_overall =driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.TextView[2]')
    sling_overall.click()
    print('sling shot extreme Vulkan overall score :', sling_overall.text)
    sling_graphics=driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[2]/android.widget.TextView[2]')
    sling_graphics.click()
    print('sling shot extreme Vulkan overall score :', sling_graphics.text)
    sling_physics=driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[3]/android.widget.TextView[2]')
    sling_physics.click()
    print('sling shot extreme Vulkan overall score :', sling_physics.text)
    nav_back =driver.find_element_by_xpath('//android.widget.ImageButton[@content-desc="Navigate up"]')
    nav_back.click()
    goto_slingshot = driver.find_element_by_xpath('//android.support.v7.app.ActionBar.Tab[@content-desc="Sling Shot"]/android.widget.TextView')
    goto_slingshot.click()
    #driver.implicitly_wait(10)
    run_slingshot = driver.find_element_by_id('com.futuremark.dmandroid.application:id/flm_fab_progress_circle')
    run_slingshot.click()
    driver.implicitly_wait(600)
    slingshot_overall = driver.find_element_by_id('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.TextView[2]')
    slingshot_overall.click()
    print('sling shot Vulkan overall score :', slingshot_overall.text)
    slingshot_graphics=driver.find_element_by_id('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[2]/android.widget.TextView[2]')
    slingshot_graphics.click()
    print('sling shot Vulkan graphics score :', slingshot_graphics.text)
    slingshot_physics=driver.find_element_by_id('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[5]/android.widget.TextView[2]')
    slingshot_physics.click()
    print('sling shot Vulkan physics score :', slingshot_physics.text)
    Back = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.ImageButton')
    Back.click()
    goto_API = driver.find_element_by_xpath('//android.support.v7.app.ActionBar.Tab[@content-desc="API Overhead"]/android.widget.TextView')
    goto_API.click()
    #driver.implicitly_wait(10)
    run_API = driver.find_element_by_id('com.futuremark.dmandroid.application:id/flm_fab_progress_circle')
    run_API.click()
    driver.implicitly_wait(50)
    API_OpenGL = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.TextView[2]')
    API_OpenGL.click()
    print('API OpenGL Drawcalls/sec score :', API_OpenGL.text)
    API_Vulkan = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[2]/android.widget.TextView[2]')
    API_Vulkan.click()
    print('API Vulkan Drawcalls/sec score :', API_Vulkan.text)
    Back.click()
    insert_threedmark_result(xindus_db_conn, run_id)


