from selenium import webdriver
import time
import pytest

@pytest.fixture(autouse=True, scope='module')
def driver():
    return webdriver.Chrome()

def test_sundsvall(driver):
    driver.get(r'https://sundsvall.se')
    time.sleep(20)
    driver.find_element_by_xpath("//*[@id='menu-huvudmeny']/a[1]").click()
    time.sleep(20)


def test_arboga(driver):
    driver.get(r'https://arboga.se')
    time.sleep(20)
    driver.find_element_by_xpath("//*[@id='svid12_76ff47581558962a24fea64d']/ul/li[1]/a").click()
    time.sleep(20)
    driver.find_element_by_xpath("//*[@id='site-nav']/ul/li[1]/ul/li[3]/a").click()
    time.sleep(20)

def test_falun(driver):
    driver.get(r'https://falun.se')
    time.sleep(20)
    driver.find_element_by_xpath("//*[@id='svid12_5ba8daa915dc81f8f1c8f8cb']/ul/li[1]/a").click()
    time.sleep(20)
    driver.find_element_by_xpath("//*[@id='svid12_647f51061499f55d0b1ca752'']/nav/ul/li[4]/ul/li[1]/ul/li[10]/a").click()
    time.sleep(20)
