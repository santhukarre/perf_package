from appium import webdriver
from Run import pull_screenshots,report_file_name,wait_for_element,wait_for_element_xpath,convert
import time
import pandas as pd
from vincent.colors import brews
from Run import mergeWithFinalReport

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

def remove(string):
    return "".join(string.split())
def generateThreeDmarkReport(xindus_db_conn,runids):
    mycursor = xindus_db_conn.cursor()
    print(runids)
    run_ids = convert(runids)
    print(run_ids)
    statement = "SELECT * FROM THREEDMARK_RESULT WHERE RESULT_ID IN ({0})".format(
        ', '.join(['%s'] * len(run_ids)))
    mycursor.execute(statement, run_ids)
    data = mycursor.fetchall()
    print("Total number of rows is ", mycursor.rowcount)
    i = 0
    iterations = []
    iterations_names = []
    for row in data:
        iteration={'SlingShot_OPENGLoverallScore': row[1], 'SlingShot_OPENGLGraphicsScore': row[2], 'SlingShot_OPENGLPhysicsScore': row[3], 'SlingShot_VulkanoverallScore': row[4], 'SlingShot_VulkanGraphicsScore': row[5],'SlingShot_VulkanPhysicsScore':row[6],'SlingShot_overallScore':row[7],'SlingShot_GraphicsScore':row[8],'SlingShot_PhysicsScore':row[9],'API_OPENGLSCORE':row[10],'API_VULKANSCORE':row[11]}
        iterations.append(iteration)
        iterations_names.append('iteration '+ str(i))
        i = i +1
    data = iterations
    index = iterations_names
    # Create a Pandas dataframe from the data.
    df = pd.DataFrame(data,index=index)
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    sheet_name = 'THREEDMARK'
    report_file_name = '.\THREEDMARK.xlsx'
    writer = pd.ExcelWriter(report_file_name, engine='xlsxwriter')
    df.to_excel(writer, sheet_name=sheet_name)
    # Access the XlsxWriter workbook and worksheet objects from the dataframe.
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]
    # Create a chart object.
    chart = workbook.add_chart({'type': 'column'})
    # Configure the series of the chart from the dataframedata.
    for col_num in range(1, len(row)):
        print("col_num ", col_num)
        chart.add_series({
            'name':       [sheet_name, 0, col_num],
            'categories': [sheet_name, 1, 0, i, 0],
            'values':     [sheet_name, 1, col_num, i, col_num],
            'fill':       {'color': brews['Set1'][col_num - 1]},
            'overlap':-10})
    # Configure the chart axes.
    chart.set_x_axis({'name': 'Iterations'})
    chart.set_y_axis({'name': 'Score', 'major_gridlines': {'visible': False}})
    # Insert the chart into the worksheet.
    worksheet.insert_chart('H2', chart)
    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    mergeWithFinalReport(report_file_name, '.\\Xindus_PerfReport.xlsx', 3)
    time.sleep(5)

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

    benchmark_rslt_sql = "INSERT INTO BENCHMARK_RESULT(RUN_ID,TOOL_NAME, RESULT_ID) VALUES (%s,%s,%s)"
    benchmark_rslt_val = [
        (run_id,'3DMARK',result_id),
    ]
    xindus_db_cursor.executemany(benchmark_rslt_sql, benchmark_rslt_val)
    xindus_db_conn.commit()

    threedmark_sql = "INSERT INTO THREEDMARK_RESULT(RESULT_ID,SLINGOPENGL_OVERALL,SLINGOPENGL_GRAPHICS,SLINGOPENGL_PHYSICS,SLING_OVERALL,SLING_GRAPHICS,SLING_PHYSICS,SLINGSHOT_OVERALL,SLINGSHOT_GRAPHICS,SLINGSHOT_PHYSICS,API_OPENGL,API_VULKAN) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    threedmark_val = [
        (result_id,SlingopenGL_overall,SlingopenGL_graphics,SlingopenGL_physics,Sling_overall,Sling_graphics,Sling_physics,Slingshot_overall,Slingshot_graphics,Slingshot_physics,API_OPENGL,API_VULKAN)
    ]
    xindus_db_cursor.executemany(threedmark_sql,threedmark_val)
    xindus_db_conn.commit()
def run_3dmark(adb_id,xindus_db_conn, run_id, screenShotsPath):
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
    permission_element = wait_for_element(driver, 50,'android:id/button1')
    if (permission_element != None):
        permission_element.click()
        driver.implicitly_wait(20)
        continue_btn = driver.find_element_by_id('com.android.packageinstaller:id/permission_allow_button')
        continue_btn.click()
        driver.implicitly_wait(20)
        warning_btn = driver.find_element_by_id('com.futuremark.dmandroid.application:id/flm_bt_tutorial_skip')
        warning_btn.click()
        driver.implicitly_wait(30)

        btn = driver.find_element_by_id('com.futuremark.dmandroid.application:id/flm_fab_progress_circle')
        print("waiting for 20 seconds before clicking the button")
        time.sleep(20)
        btn.click()
        print("waiting for 60 seconds for downloading files")
        time.sleep(60)
        goto_API = driver.find_element_by_xpath('//android.support.v7.app.ActionBar.Tab[@content-desc="API Overhead"]/android.widget.TextView')
        goto_API.click()
        btn1 = driver.find_element_by_id('com.futuremark.dmandroid.application:id/flm_fab_progress_circle')
        print("waiting for 20 seconds before clicking the button")
        time.sleep(20)
        btn1.click()
        goto_Sling = driver.find_element_by_xpath('//android.support.v7.app.ActionBar.Tab[@content-desc="Sling Shot Extreme"]/android.widget.TextView')
        print("waiting for 20 seconds before clicking the button")
        time.sleep(20)
        goto_Sling.click()
        print("waiting for 60 seconds for downloading files")
        time.sleep(60)
    run_sling = driver.find_element_by_id('com.futuremark.dmandroid.application:id/flm_fab_progress_circle')
    run_sling.click()

    slingopenGL_overall=wait_for_element_xpath(driver,850,'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.TextView[2]')
    SlingopenGL_overall = remove(slingopenGL_overall.text)
    print('sling shot extreme OpenGL overall score :',slingopenGL_overall.text)
    print(SlingopenGL_overall)
    slingopenGL_graphics=driver.find_element_by_xpath(' /hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[2]/android.widget.TextView[2]')
    SlingopenGL_graphics=remove(slingopenGL_graphics.text)
    print('sling shot extreme OpenGL graphics score :', slingopenGL_graphics.text)
    print(SlingopenGL_graphics)
    slingopenGL_physics=driver.find_element_by_xpath(' /hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[3]/android.widget.TextView[2]')
    SlingopenGL_physics=remove(slingopenGL_physics.text)
    print('sling shot extreme OpenGL physics score :', slingopenGL_physics.text)
    print(SlingopenGL_physics)
    sling_overall =driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.TextView[2]')
    Sling_overall=remove(sling_overall.text)
    print('sling shot extreme Vulkan overall score :', sling_overall.text)
    print(Sling_overall)
    sling_graphics=driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[2]/android.widget.TextView[2]')
    Sling_graphics=remove(sling_graphics.text)
    print('sling shot extreme Vulkan graphics score :', sling_graphics.text)
    print(Sling_graphics)
    sling_physics=driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[3]/android.widget.TextView[2]')
    Sling_physics=remove(sling_physics.text)
    print('sling shot extreme Vulkan physics score :', sling_physics.text)
    print(Sling_physics)
    pull_screenshots(run_id, "3dmark","C:\KnowledgeCenter\Xindus\Code\Perf_package_final\OnePlusDeviceReports\\apps_data")
    nav_back =driver.find_element_by_xpath('//android.widget.ImageButton[@content-desc="Navigate up"]')
    nav_back.click()
    goto_slingshot = driver.find_element_by_xpath('//android.support.v7.app.ActionBar.Tab[@content-desc="Sling Shot"]/android.widget.TextView')
    goto_slingshot.click()
    driver.implicitly_wait(10)
    run_slingshot = driver.find_element_by_id('com.futuremark.dmandroid.application:id/flm_fab_progress_circle')
    run_slingshot.click()

    slingshot_overall = wait_for_element_xpath(driver,850,'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.TextView[2]')
    Slingshot_overall=remove(slingshot_overall.text)
    print('sling shot Vulkan overall score :', slingshot_overall.text)
    print(Slingshot_overall)
    slingshot_graphics=driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[2]/android.widget.TextView[2]')
    Slingshot_graphics=remove(slingshot_graphics.text)
    print('sling shot Vulkan graphics score :', slingshot_graphics.text)
    print(Slingshot_graphics)
    slingshot_physics=driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[5]/android.widget.TextView[2]')
    Slingshot_physics=remove(slingshot_physics.text)
    print('sling shot Vulkan physics score :', slingshot_physics.text)
    print(Slingshot_physics)
    pull_screenshots(run_id, "3dmark_SLING","C:\KnowledgeCenter\Xindus\Code\Perf_package_final\OnePlusDeviceReports\\apps_data")
    Back = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.ImageButton')
    Back.click()
    goto_API = driver.find_element_by_xpath('//android.support.v7.app.ActionBar.Tab[@content-desc="API Overhead"]/android.widget.TextView')
    goto_API.click()
    driver.implicitly_wait(10)
    run_API = driver.find_element_by_id('com.futuremark.dmandroid.application:id/flm_fab_progress_circle')
    run_API.click()
    API_OpenGL =wait_for_element_xpath(driver,850,'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[1]/android.widget.TextView[2]')
    API_OPENGL=remove(API_OpenGL.text)
    print('API OpenGL Drawcalls/sec score :', API_OpenGL.text)
    print(API_OPENGL)
    API_Vulkan = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.support.v7.widget.RecyclerView/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.LinearLayout/android.support.v7.widget.RecyclerView/android.view.ViewGroup[2]/android.widget.TextView[2]')
    API_VULKAN=remove(API_Vulkan.text)
    print('API Vulkan Drawcalls/sec score :', API_Vulkan.text)
    print(API_VULKAN)

    insert_threedmark_result(xindus_db_conn, run_id)
    store_threedmark_result(xindus_db_conn, [1, 2])
    pull_screenshots(run_id, "3dmark_API",screenShotsPath)
    #generateThreeDmarkReport(xindus_db_conn)


