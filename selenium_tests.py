from selenium import webdriver
options = webdriver.ChromeOptions()
options.binary_location = r'C:\Users\stefanb\AppData\Local\Google\Chrome SxS\Application\chrome.exe'

def sundsvall():
    driver.get("https://sundsvall.se")

def arboga():
    driver.get("https://arboga.se")

def falun():
    driver.get("https://falun.se")

driver = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Python\chromedriver77.exe', options=options)
sundsvall()
arboga()
falun()