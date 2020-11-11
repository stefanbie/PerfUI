# UI based performance test tool
The purpose of this tool is to enable the possibility to run UI based performance tests. There are several advantages with UI based performance testing compared to the traditional http based.
* Cheaper maintenance
* Possibility to reuse existing functional UI-based system tests
* Easier implementation
* Out of the box Ajax support

The problem with UI based performance test has traditionally been that it consumes loads of resources which makes it extremely expensive to run. However, with slimmed headless chrome browser running on linux virtual GUI xvfb together with the ability to scale up machines on demand in the cloud, the throughput can be increased significantly in a cost effective way. Add the possibility to monitor all machine metrics and transactions with the an APM tool of you choice and you have all you need to analyze and benchmark the results of your test.

The aim of the project is to create a minimal, robust framework for threading out UI test based on *pytest* together with *Selenium webdriver* and *Chrome*. The combination of the three tools was chosen based on certain criteria; free, increasing trend of interest, well documented. 

## Test setup
Place a perf_conf.json file in the root of your project. In the conf file you specify the relative path to the test case files, the name of the test methods and the probability of the test cases to be executed. You also specify the number of users to be simulated, the rampup time and the time for the test to run (in seconds). Below is an example. Probability 2 means that it will be executed two times more than the testcase with probability 1.
```
{
  "users": 3,
  "rampup_time": 10,
  "test_time": 60,
  "test_scenarios":
  [
    {
      "relative_path": "tests/test_scenarios.py",
      "method": "google_search",
      "probability": 1
    },
    {
      "relative_path": "tests/test_scenarios.py",
      "method": "google_browse",
      "probability": 2
    }
  ]
}
```
## Run test
To setup and run using Docker:
```
docker run -it --mount type=bind,source=[path to root of your project],target=/PerfUI/mnt sbie/perfui
```
