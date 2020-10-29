import time, sys, traceback, signal, psutil, argparse, logging, json
from threading import Thread
from random import randint
from test_selenium import *


class Scenario:
    def __init__(self, method, probability):
        self.method = method
        self.probability = probability


class Scenario_pool:

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
        self.options.headless = False
        self.options.add_argument('disable-gpu')
        self.options.add_argument('window-size=1200,1100')
        self.options.add_experimental_option('excludeSwitches', ['enable-logging'])
        self.driver = webdriver.Chrome(options=self.options)
        self.start()

    def stop(self):
        self.stop_user = True

    def run(self):
        while True:
            if self.stop_user:
                self.driver.close()
                break
            scenario = sp.get_scenario()
            try:
                scenario.method(self.driver)
            except Exception as err:
                print("olle")
                traceback.print_tb(err.__traceback__)
            time.sleep(1)

    def quit(self):
        self.driver.quit()


class User_pool:
    def __init__(self):
        self.user_pool = []

    def log_user_count(self):
        logging.info("{} users active   ".format(len(self.user_pool)))

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


def signal_handler(sig, frame):
    sys.stdout.write("You pressed Ctrl+C!")
    kill_chromedrivers()
    sys.exit(0)


def setup():
    ### Read arguments ###
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('required arguments')
    required.add_argument("--conf", type=str, required=True, help="Path to configuration file ie 'python3 main.py --conf='./conf.json''")
    optional = parser.add_argument_group('optional arguments')
    optional.add_argument("--log", type=str, help="Output verbosity, [DEBUG, INFO, WARNING]")
    args = parser.parse_args()

    ### Setup for log verbosity ###
    loglevel = args.log
    if loglevel:
        numeric_level = getattr(logging, loglevel.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % loglevel)
    else:
        numeric_level = getattr(logging, "INFO", None)
    logging.basicConfig(format='%(asctime)s\t\t%(message)s', level=numeric_level)

    ### Init interruption handler ###
    signal.signal(signal.SIGINT, signal_handler)

    return args


def kill_chromedrivers():
    logging.debug("Kill Chromedrivers")
    for proc in psutil.process_iter():
        if proc.name().startswith("chromedriver"):
            proc.kill()


def rampup(nbr_of_users, ramp_up_time_in_sec):
    logging.info("Rampup started")
    for i in range(0, nbr_of_users):
        up.add_user(User(sp))
        time.sleep(ramp_up_time_in_sec / nbr_of_users)
    logging.info("Rampup finished")


def wait_test_time(test_time_in_sec):
    logging.info("All resources up. Running test")
    n = 0
    while True:
        if n >= test_time_in_sec:
            break
        n += 10
        time.sleep(10)
        logging.info("Time left: " + str(test_time_in_sec - n) + "s  ")
    logging.info("Test finished")


def tear_down():
    logging.info("Teardown started")
    nbr_of_users = up.size()
    for i in range(0, nbr_of_users):
        up.get_user(i).stop()
    for i in range(0, nbr_of_users):
        user = up.get_user(0)
        user.join()
        up.delete_user(user)
    logging.info("Teardown finished")


if __name__ == "__main__":
    sp = Scenario_pool()
    up = User_pool()

    ### Initial setup
    args = setup()

    ### Specify tests ###
    with open(args.conf, 'r') as _file:
        conf = json.loads(_file.read())
    for testcase in conf["testcases"]:
        logging.debug("Adding testcase {} with prio {}".format(testcase["name"], testcase["prio"]))
        sp.add_scenario(Scenario(method=globals()[testcase["name"]], probability=testcase["prio"]))

    ### Ramp up users ###
    rampup(conf["users"], conf["rampuptime"])

    ### Wait for test_time ###
    wait_test_time(conf["testtime"])

    ### Stop test ###
    tear_down()
    kill_chromedrivers()