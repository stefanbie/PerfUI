from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pytest

host = "https://www.google.com"


@pytest.fixture(autouse=True, scope='module')
def driver():
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('disable-gpu')
    options.add_argument('window-size=1200,1100')
    driver = webdriver.Chrome(options=options)
    return driver


def google_search(driver):
    driver.get(r"{}/".format(host))
    time.sleep(2)
    approve_cookies(driver)
    time.sleep(2)
    driver.find_element(By.NAME, "q").send_keys("camera" + Keys.ENTER)
    time.sleep(2)


def google_browse(driver):
    driver.get(r"{}/".format(host))
    time.sleep(2)
    approve_cookies(driver)
    time.sleep(2)
    driver.find_element(By.XPATH, "//div[3]/center/input[2]").click()
    time.sleep(2)


def approve_cookies(driver):
    try:
        driver.switch_to.frame(0)
        driver.find_element(By.XPATH, "//*[@id='introAgreeButton']").click()
        driver.switch_to.default_content()
    except Exception:
        pass


