from threading import Thread
from test_selenium import *
import time

class thread(Thread):

    def __init__(self, user, scenario):
        Thread.__init__(self)
        self.user = user
        self.scenario = scenario
        self.daemon = True
        self.stop_user = False
        #self.options = webdriver.ChromeOptions()
        #self.options.headless = True
        self.driver = webdriver.Chrome()
        self.start()

    def stop(self):
        self.stop_user = True

    def run(self):
        while(True):
            if(self.stop_user):
                self.driver.quit()
                break
            self.scenario.method(self.driver)
            time.sleep(1)


class User():
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

class Scenario():
    def __init__(self, id, method, probability):
        self.id = id
        self.method = method
        self.probability = probability

scenario_pool = []
user_pool = []

def get_scenario():
    return scenario_pool[0]

def get_user():
    return user_pool[0]

if __name__ == "__main__":
    users = 3
    test_time = 10
    scenario_pool.append(Scenario(id=1, method=test_sundsvall, probability=1))
    scenario_pool.append(Scenario(id=2, method=test_arboga, probability=3))
    user_pool.append(User(id=1, name="gunnar", password="gunnar"))
    user_pool.append(User(id=2, name="arne", password="arne"))
    scenario = get_scenario()
    user = get_user()

    t = thread(user=user, scenario=scenario)

    time.sleep(test_time)
    t.stop()
    t.join()
