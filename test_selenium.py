from selenium import webdriver
import time
import pytest

host = "http://18.184.252.217"

@pytest.fixture(autouse=True, scope='module')
def driver():
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument('disable-gpu')
    options.add_argument('window-size=1200,1100')
    driver = webdriver.Chrome(options=options)
    return driver

def test_search(driver):
    driver.get(r'{}/nopCommerce/'.format(host))
    time.sleep(20)
    driver.find_element_by_xpath("//*[@id='small-searchterms']").send_keys("camera")
    time.sleep(20)
    driver.find_element_by_xpath("//*[@value='Search']").click()
    time.sleep(20)

def test_browse(driver):
    driver.get(r'{}/nopCommerce/'.format(host))
    time.sleep(20)
    driver.find_element_by_xpath("//*[@href='/nopCommerce/apparel']").click()
    time.sleep(20)
    driver.find_element_by_xpath("//*[@title='Show products in category Shoes']").click()
    time.sleep(20)

def test_add_item_to_cart(driver):
    driver.get(r'{}/nopCommerce/adidas-consortium-campus-80s-running-shoes'.format(host))
    time.sleep(20)
    driver.find_element_by_xpath("//*[@value='Add to cart']").click()
    time.sleep(20)
    driver.find_element_by_xpath("//*[text()='Shopping cart']").click()
    time.sleep(20)
    driver.find_element_by_xpath("//*[@name='removefromcart']").click()
    time.sleep(20)
    driver.find_element_by_xpath("//*[@name='updatecart']").click()
    time.sleep(20)

