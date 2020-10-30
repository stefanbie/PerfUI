import logging, sys, traceback, signal, psutil, argparse, json
from threading import Thread
from random import randint
from test_scenarios import *


class Scenario:
    """Test scenario object.

    Parameters
    ----------
    method : `reference`
       Test scenario definition.
    probability : 'int'
        Probability of this test scenario being executed
    """

    def __init__(self, method, probability):
        self.method = method
        self.probability = probability


class Scenario_pool:
    """An object holding all test scenarios available during execution.

    Parameters
    ----------
    scenario_pool : `Array of Scenarios`
       Pool of test scenarios.
    """

    def __init__(self):
        self.scenario_pool = []

    def get_scenario(self):
        return self.scenario_pool[randint(0, len(self.scenario_pool)-1)]

    def add_scenario(self, scenario):
        for i in range(0, scenario.probability):
            self.scenario_pool.append(scenario)


class User(Thread):
    """Thread object representing a user.
    """

    def __init__(self):
        Thread.__init__(self)
        self.daemon = True
        self.stop_user = False
        self.options = webdriver.ChromeOptions()
        self.options.headless = True
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
            sn = sp.get_scenario()
            try:
                sn.method(self.driver)
            except Exception as err:
                traceback.print_tb(err.__traceback__)
            time.sleep(1)

    def quit(self):
        self.driver.quit()


class User_pool:
    """An object holding all user threads available during execution.

    Parameters
    ----------
    user_pool : `Array of user threads`
       Pool of user threads.
    """

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


def signal_handler():
    """Method used by signal handler, if Ctrl+C is pressed program exit
    """

    sys.stdout.write("You pressed Ctrl+C!")
    kill_chromedrivers()
    sys.exit(0)


def setup():
    """Parse arguments, setup for log verbosity, add scenarios to pool, init interruption handler
    """

    def read_arguments():
        parser = argparse.ArgumentParser()
        required = parser.add_argument_group('required arguments')
        required.add_argument("--conf", type=str, required=True,
                              help="Path to configuration file ie 'python3 main.py --conf='./conf.json''")
        optional = parser.add_argument_group('optional arguments')
        optional.add_argument("--log", type=str, help="Output verbosity, [DEBUG, INFO, WARNING]")
        return parser.parse_args()

    def setup_log_verbosity(log_level):
        if log_level is not None:
            numeric_level = getattr(logging, log_level.upper(), None)
            if not isinstance(numeric_level, int):
                raise ValueError('Invalid log level: %s' % log_level)
        else:
            numeric_level = getattr(logging, "INFO", None)
        logging.basicConfig(format='%(asctime)s\t\t%(message)s', level=numeric_level)

    def add_scenarios_to_pool(con):
        for scenario in con["test_scenarios"]:
            logging.debug("Adding scenario {} with prio {}".format(scenario["method"], scenario["probability"]))
            sp.add_scenario(Scenario(method=globals()[scenario["method"]], probability=scenario["probability"]))

    def add_signal_handler():
        signal.signal(signal.SIGINT, signal_handler)

    args = read_arguments()
    with open(args.conf, 'r') as _file:
        conf = json.loads(_file.read())
    setup_log_verbosity(args.log)
    add_scenarios_to_pool(conf)
    add_signal_handler()

    return conf


def kill_chromedrivers():
    """Kill drivers for all threads
    """

    logging.debug("Kill Chromedrivers")
    for proc in psutil.process_iter():
        if proc.name().startswith("chromedriver"):
            proc.kill()


def rampup(nbr_of_users, ramp_up_time_in_sec):
    """Increase thread count for a specified time period
    :param nbr_of_users: The number threads to be started.
    :param ramp_up_time_in_sec: Time to ramp up the final number of users
    """

    logging.info('Rampup started')
    for i in range(0, nbr_of_users):
        up.add_user(User())
        time.sleep(ramp_up_time_in_sec / nbr_of_users)
    logging.info("Rampup finished")


def wait_test_time(test_time_in_sec):
    """Lets the threads run for the specified test time
    :param test_time_in_sec: The time to run
    """

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
    """Shut down the threads when the scenarios are finished
    """
    logging.info("Teardown started")
    nbr_of_users = up.size()
    for i in range(0, nbr_of_users):
        up.get_user(i).stop()
    for i in range(0, nbr_of_users):
        user = up.get_user(0)
        user.join()
        up.delete_user(user)
    kill_chromedrivers()
    logging.info("Teardown finished")


if __name__ == "__main__":
    sp = Scenario_pool()
    up = User_pool()
    config = setup()
    
    rampup(config["users"], config["rampup_time"])
    wait_test_time(config["test_time"])
    tear_down()
