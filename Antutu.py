import time
from appium import webdriver

def run_antutu(adb_id):
    print("Running Antutu on device with adb_id =", adb_id)
    antutu_desired_cap = {
        "deviceName": adb_id,
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
    #antutu_driver.implicitly_wait(2400)
    time.sleep(600)
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
