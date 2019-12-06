from selenium import webdriver
import time
import pytest

@pytest.fixture(autouse=True, scope='module')
def driver():
    return webdriver.Chrome()

def test_search(driver):
    driver.get(r'http://35.158.97.204/nopCommerce/')
    time.sleep(20)
    driver.find_element_by_xpath("//*[@id='small-searchterms']").send_keys("camera")
    time.sleep(20)
    driver.find_element_by_xpath("//*[@value='Search']").click()
    time.sleep(20)

def test_browse(driver):
    driver.get(r'http://35.158.97.204/nopCommerce')
    time.sleep(20)
    driver.find_element_by_xpath("//*[@href='/nopCommerce/apparel']").click()
    time.sleep(20)
    driver.find_element_by_xpath("//*[@href='/nopCommerce/shoes']").click()
    time.sleep(20)

def test_add_item_to_cart(driver):
    driver.get(r'http://35.158.97.204/nopCommerce/adidas-consortium-campus-80s-running-shoes')
    time.sleep(20)
    driver.find_element_by_xpath("//*[@value='Add to cart']").click()
    time.sleep(20)
    driver.find_element_by_xpath("//*[text()='Shopping cart']").click()
    time.sleep(20)
    driver.find_element_by_xpath("//*[@name='removefromcart']").click()
    time.sleep(20)
    driver.find_element_by_xpath("//*[@name='updatecart']").click()
    time.sleep(20)

