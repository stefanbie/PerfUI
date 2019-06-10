from selenium import webdriver
import logging
import threading
import time
from selenium_tests import*

options = webdriver.ChromeOptions()
options.binary_location = r'C:\Users\stefanb\AppData\Local\Google\Chrome SxS\Application\chrome.exe'
#options.headless = True
#options.add_argument('window-size=1200x600')


def sundsvall1(name):
    logging.info("Thread %s: starting", name)
    driver = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Python\chromedriver77.exe', options=options)
    sundsvall()
    driver.quit()
#
#    driver.get("https://sundsvall")
#    time.sleep(2)
#    driver.quit()
#    logging.info("Thread %s: finishing", name)


if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S")

    logging.info("Main    : before creating thread")
    x = threading.Thread(target=sundsvall1, args=(1,))
    y = threading.Thread(target=sundsvall1, args=(2,))
    logging.info("Main    : before running thread")
    x.start()
    time.sleep(2)
    y.start()
    logging.info("Main    : wait for the thread to finish")
    # x.join()
    logging.info("Main    : all done")