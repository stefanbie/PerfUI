from threading import Thread
from test_selenium import *
import time
from random import randint

users = 5
ramp_up_time = 20
test_time = 60

scenario_pool = []
user_pool = []

class Scenario():
    def __init__(self, method, probability):
        self.method = method
        self.probability = probability

def get_scenario_from_pool():
    return scenario_pool[randint(0,len(scenario_pool)-1)]

def add_scenario_to_pool(scenario):
    for i in range(0, scenario.probability):
        scenario_pool.append(scenario)

class User(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.stop_user = False
        self.options = webdriver.ChromeOptions()
        #self.options.headless = True
        self.driver = webdriver.Chrome(options=self.options)
        self.start()

    def stop(self):
        self.stop_user = True

    def run(self):
        while(True):
            if(self.stop_user):
                self.driver.quit()
                break
            scenario = get_scenario_from_pool()
            scenario.method(self.driver)
            time.sleep(1)

if __name__ == "__main__":
    add_scenario_to_pool(Scenario(method=test_add_item_to_cart, probability=1))
    add_scenario_to_pool(Scenario(method=test_search, probability=3))
    add_scenario_to_pool(Scenario(method=test_browse, probability=2))

    for i in range(0,users):
        user_pool.append(User())
        time.sleep(ramp_up_time/users)
    time.sleep(test_time)
    for user in user_pool:
        user.stop()
        user.join()