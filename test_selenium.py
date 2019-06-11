from selenium import webdriver
import time
import pytest

@pytest.fixture(autouse=True, scope='module')
def driver():
    return webdriver.Chrome()

def test_sundsvall(driver):
    driver.get(r'https://sundsvall.se')
    time.sleep(2)
    driver.find_element_by_xpath("//*[@id='menu-huvudmeny']/a[1]").click()
    time.sleep(2)

def test_arboga(driver):
    driver.get(r'https://arboga.se')

def test_falun(driver):
    driver.get(r'https://falun.se')