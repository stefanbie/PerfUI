# UI based performance test tool
The purpose of this tool is to enable the possibility to run UI based performance tests. There are several advantages with UI based performance testing compared to the traditional http based.
* Cheaper maintenance
* Possibility to reuse existing functional UI-based system tests
* Easier implementation
* Out of the box Ajax support

The problem with UI based performance test has traditionally been that it consumes loads of resources which makes it extremely expensive to run. However, with slimmed headless chrome browser running on linux virtual GUI xvfb together with the ability to scale up machines on demand in the cloud, the throughput can be increased significantly in a cost effective way. Add the possibility to monitor all machine metrics and transactions with the an APM tool of you choice and you have all you need to analyze and benchmark the results of your test.

The aim of the project is to create a minimal, robust framework for threading out UI test based on *pytest* together with *Selenium webdriver* and *Chrome*. The combination of the three tools was chosen based on certain criteria; free, increasing trend of interest, well documented. 

##Setup

To setup a the performance environment on a clean Ubuntu:
```
# Set up SSH:
ssh-keygen
# Enter file in which to save the key (/home/ubuntu/.ssh/id_rsa):[Enter]
# Enter passphrase (empty for no passphrase):[Enter]
# Enter same passphrase again:[Enter]
cat /home/ubuntu/.ssh/id_rsa.pub
# Add the key to https://github.com/settings/ssh/new

# Clone project:
git clone git@github.com:system-verification/Performance-test.git

#run setup script
chmod +x ~/Performance-test/env_setup.sh 
sudo su -c ~/Performance-test/env_setup.sh root 
```
To run a test do following:

```
cd ~/Performance-test
python3 main.py --conf="./conf.json
```