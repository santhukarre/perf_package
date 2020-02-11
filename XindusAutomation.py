import time
from appium import webdriver


def get_androdben_results(driver):
    # Click on Results Button.
    seq_read_results_element = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TabHost/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.ListView/android.widget.FrameLayout[1]/android.widget.LinearLayout/android.widget.TextView[2]')
    seq_write_results_element = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TabHost/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.ListView/android.widget.FrameLayout[2]/android.widget.LinearLayout/android.widget.TextView[2]')
    rand_read_results_element = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TabHost/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.ListView/android.widget.FrameLayout[3]/android.widget.LinearLayout/android.widget.TextView[2]')
    rand_write_results_element = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TabHost/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.ListView/android.widget.FrameLayout[4]/android.widget.LinearLayout/android.widget.TextView[2]')
    sql_insert_results_element = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TabHost/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.ListView/android.widget.FrameLayout[5]/android.widget.LinearLayout/android.widget.TextView[2]')
    sql_update_results_element = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TabHost/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.ListView/android.widget.FrameLayout[6]/android.widget.LinearLayout/android.widget.TextView[2]')
    sql_delete_results_element = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TabHost/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.LinearLayout[2]/android.widget.ListView/android.widget.FrameLayout[7]/android.widget.LinearLayout/android.widget.TextView[2]')
    print('seq_read_results_element= ', seq_read_results_element.text)
    print('seq_write_results_element= ', seq_write_results_element.text)
    print('rand_read_results_element= ', rand_read_results_element.text)
    print('sql_insert_results_element= ', sql_insert_results_element.text)
    print('sql_update_results_element= ', sql_update_results_element.text)
    print('sql_delete_results_element= ', sql_delete_results_element.text)

def run_androbench():
    desired_cap = {
        "deviceName": "bab0d1770403",
        "platformName": "android",
        "appPackage": "com.andromeda.androbench2",
        "appActivity": "main",
    }
    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)


    driver.implicitly_wait(30)
    # on Androbench Run All Benchmarks Button.
    driver.find_element_by_id('com.andromeda.androbench2:id/btnStartingBenchmarking').click();

    driver.implicitly_wait(30)

    # Click on Yes Button.
    driver.find_element_by_id('android:id/button1').click();

    driver.implicitly_wait(200)

    # Click on Cancel Button for 'Do you want to send results to server for research purpose'
    driver.find_element_by_id('android:id/button2').click();

    # Click on Results Button.
    results_element = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.TabHost/android.widget.LinearLayout/android.widget.TabWidget/android.widget.LinearLayout[2]')
    results_element.click()
    get_androdben_results(driver)

def run_antutu():
    antutu_desired_cap = {
        "deviceName": "bab0d1770403",
        "platformName": "android",
        "appPackage": "com.antutu.ABenchMark",
        "appActivity": ".ABenchMarkStart",
        "noReset": True,
    }
    antutu_driver = webdriver.Remote("http://localhost:4723/wd/hub", antutu_desired_cap)
    #antutu_driver.implicitly_wait(30)
    #antutu_driver.find_element_by_id('com.android.packageinstaller:id/permission_allow_button').click()
    #antutu_driver.implicitly_wait(30)
    #antutu_driver.find_element_by_id('com.android.packageinstaller:id/permission_allow_button').click()
    #antutu_driver.implicitly_wait(30)
    #antutu_driver.find_element_by_id('com.android.packageinstaller:id/permission_allow_button').click()
    #antutu_driver.implicitly_wait(30)
    #antutu_driver.find_element_by_id('com.android.packageinstaller:id/permission_allow_button').click()

    # Starting the tests, by clicking the Test Button.
    antutu_driver.implicitly_wait(30)
    antutu_driver.find_element_by_id('com.antutu.ABenchMark:id/main_test_start_title').click()

    # Wait for Test Completion
    antutu_driver.implicitly_wait(2400)
    antutu_total_score = antutu_driver.find_element_by_id('com.antutu.ABenchMark:id/textViewTotalScore')

    antutu_driver.implicitly_wait(10)
    print('Antutu Total Score :', antutu_total_score.text)
    antutu_driver.implicitly_wait(10)
    antutu_cpu_score = antutu_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[1]/android.view.ViewGroup/android.widget.TextView[1]')
    print('Antutu CPU Score :', antutu_cpu_score.text)
    antutu_driver.implicitly_wait(10)
    antutu_memory_score = antutu_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[2]/android.view.ViewGroup/android.widget.TextView[1]')
    print('Antutu Memory Score :', antutu_memory_score.text)
    antutu_driver.implicitly_wait(10)
    antutu_ux_score = antutu_driver.find_element_by_xpath('	/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.FrameLayout[4]/android.view.ViewGroup/android.widget.TextView[1]')
    print('Antutu UX Score :', antutu_ux_score.text)

def run_geekbench():
    geekbench_desired_cap = {
        "deviceName": "bab0d1770403",
        "platformName": "android",
        "appPackage": "com.primatelabs.geekbench5",
        "appActivity": "com.primatelabs.geekbench.HomeActivity",
        "keep_alive": True,
        "newCommandTimeout": 1800000
    }
    geekbench_driver = webdriver.Remote("http://localhost:4723/wd/hub", geekbench_desired_cap)
    geekbench_driver.implicitly_wait(30)

    # Click the Accept button Button
    geekbench_driver.find_element_by_id('android:id/button1').click()
    geekbench_driver.implicitly_wait(30)

    # Click the RUN CPU Benchmark Button
    geekbench_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.support.v4.widget.DrawerLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.support.v4.view.ViewPager/android.widget.ScrollView/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.Button').click()
    #geekbench_driver.implicitly_wait(800)
    time.sleep(800)

    # get the Single core, Multi Core Results
    single_core_element = geekbench_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.support.v4.view.ViewPager/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[2]/android.view.View[1]')
    multi_core_element = geekbench_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.support.v4.view.ViewPager/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[2]/android.view.View[3]')
    print('single_core_element= ', single_core_element.text)
    print('multi_core_element= ', multi_core_element.text)

    # Click the Back Button
    geekbench_driver.implicitly_wait(10)
    nav_back_element = geekbench_driver.find_element_by_xpath('//android.widget.ImageButton[@content-desc="Navigate up"]')
    nav_back_element.click()

    # Click the COMPUTE Button
    geekbench_driver.implicitly_wait(10)
    compute_element = geekbench_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.support.v4.widget.DrawerLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.HorizontalScrollView/android.widget.LinearLayout/android.support.v7.app.ActionBar.Tab[2]')
    compute_element.click()

    # Click the RUN COMPUTE Tests Button
    geekbench_driver.find_element_by_id('com.primatelabs.geekbench5:id/runComputeBenchmark').click()
    #geekbench_driver.implicitly_wait(1800)
    time.sleep(1200)

    opencl_score_element = geekbench_driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.support.v4.view.ViewPager/android.webkit.WebView/android.webkit.WebView/android.view.View/android.view.View[2]/android.view.View[1]')
    print('opencl_score_element= ', opencl_score_element.text)
    nav_back_element = geekbench_driver.find_element_by_xpath('//android.widget.ImageButton[@content-desc="Navigate up"]')
    nav_back_element.click()

def main():
    run_androbench()
    run_geekbench()
    #run_antutu()
main()