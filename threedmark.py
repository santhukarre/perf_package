from appium import webdriver

def run_3dmark(adb_device_id):
    desired_cap = {
        "deviceName": adb_device_id,
        "platformName": "android",
        "appPackage": "com.futuremark.dmandroid.application",
        "appActivity": "com.futuremark.flamenco.ui.splash.SplashPageActivity",
        "noReset": True,
        "connectionRetryTimeout": 10000,
        "connectionRetryCount": 3,
        "automationName": "UiAutomator1",
        "newCommandTimeout": 200000
    }
    print("adb_device_id = ", adb_device_id)
    driver = webdriver.Remote("http://localhost:4723/wd/hub", desired_cap)
    driver.implicitly_wait(20)
    continue_btn = driver.find_element_by_id('android:id/button1')
    continue_btn.click()

    driver.implicitly_wait(20)
    warning_btn = driver.find_element_by_id('com.android.packageinstaller:id/permission_allow_button')
    warning_btn.click()

    driver.implicitly_wait(200)
    print("after implicit wait of 100 seconds");

    btn = driver.find_element_by_id('com.futuremark.dmandroid.application:id/flm_fab_benchmark')
    btn.click()


