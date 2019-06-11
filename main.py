from selenium import webdriver
import logging
import threading
import time
from test_selenium import *


if __name__ == "__main__":


    options = webdriver.ChromeOptions()
    options.binary_location = r'C:\Users\stefanb\AppData\Local\Google\Chrome SxS\Application\chrome.exe'
    #options.headless = True
    #options.add_argument('window-size=1200x600')
    logging.info("Main    : before creating thread")
    x = threading.Thread(target=test_sundsvall, args=(webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Python\chromedriver77.exe', options=options),))
    y = threading.Thread(target=test_arboga, args=(webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Python\chromedriver77.exe', options=options),))
    logging.info("Main    : before running thread")
    x.start()
    time.sleep(2)
    y.start()
    logging.info("Main    : wait for the thread to finish")
    #x.join()
    logging.info("Main    : all done")