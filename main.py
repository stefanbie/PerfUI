from threading import Thread
from test_selenium import *
import time, sys
from random import randint

users = 5
ramp_up_time = 20
test_time = 60

class Scenario():
    def __init__(self, method, probability):
        self.method = method
        self.probability = probability

class Scenario_pool():

    def __init__(self):
        self.scenario_pool = []

    def get_scenario(self):
        return self.scenario_pool[randint(0,len(self.scenario_pool)-1)]

    def add_scenario(self, scenario):
        for i in range(0, scenario.probability):
            self.scenario_pool.append(scenario)

class User(Thread):

    def __init__(self, sp):
        Thread.__init__(self)
        self.daemon = True
        self.stop_user = False
        self.options = webdriver.ChromeOptions()
        self.options.headless = True
        self.options.add_argument('disable-gpu')
        self.options.add_argument('window-size=1200,1100')
        self.driver = webdriver.Chrome(options=self.options)
        self.start()

    def stop(self):
        self.stop_user = True

    def run(self):
        while(True):
            if(self.stop_user):
                self.driver.close()
                break
            scenario = sp.get_scenario()
            scenario.method(self.driver)
            time.sleep(1)

    def quit(self):
        self.driver.quit()

class User_pool():

    def __init__(self):
        self.user_pool = []

    def log_user_count(self):
        sys.stdout.write("\r{} out of {} users active   ".format(len(self.user_pool), users))

    def add_user(self, user):
        self.user_pool.append(user)
        self.log_user_count()

    def get_user(self, pos):
        return self.user_pool[pos]

    def delete_user(self, user):
        self.user_pool.remove(user)
        self.log_user_count()

    def size(self):
        return len(self.user_pool)

def kill_chromedriver():
    import psutil
    for proc in psutil.process_iter():
        if proc.name().startswith("chromedriver"):
            proc.kill()

if __name__ == "__main__":

    sp = Scenario_pool()
    up = User_pool()

    def wait_test_time():
        n = 0
        while (True):
            time.sleep(1)
            n += 1
            if (n > test_time):
                break
            sys.stdout.write("\rTime left: " + str(test_time - n) + "s  ")

    sp.add_scenario(Scenario(method=test_add_item_to_cart, probability=1))
    sp.add_scenario(Scenario(method=test_search, probability=3))
    sp.add_scenario(Scenario(method=test_browse, probability=2))

    ### Ramp up users ###
    sys.stdout.write("Rampup started\n")
    for i in range(0,users):
        up.add_user(User(sp))
        time.sleep(ramp_up_time/users)
    sys.stdout.write("\nRampup finished\n")

    ### Wait for test_time ###
    sys.stdout.write("\nAll resources up. Running test\n")
    wait_test_time()
    sys.stdout.write("\nTest finished\n")

    ### Stop test ###
    sys.stdout.write("\nTeardown started\n")
    nbr_of_users = up.size()
    for i in range(0, nbr_of_users):
        up.get_user(i).stop()
    for i in range(0, nbr_of_users):
        user = up.get_user(0)
        user.join()
        up.delete_user(user)
    kill_chromedriver()
    sys.stdout.write("\nTeardown finished\n")