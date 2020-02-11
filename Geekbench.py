from appium import webdriver
import time

def run_geekbench(adb_id):
    print("Running Geekbench on device with adb_id =", adb_id)
    geekbench_desired_cap = {
        "deviceName": adb_id,
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
