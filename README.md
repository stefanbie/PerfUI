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
# Use root
sudo su

# Install GUI
apt-get update
apt-get install -y unzip xvfb libxi6 libgconf-2-4

# Install Chrome
curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
apt-get -y update
apt-get -y install google-chrome-stable

# Install ChromeDriver
wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
apt-get install unzip
unzip chromedriver_linux64.zip
mv chromedriver /usr/bin/chromedriver
chown root:root /usr/bin/chromedriver
chmod +x /usr/bin/chromedriver

# Install Python3
apt install python3

# Install Pip
apt install -y python3-pip

# Install Selenium
python3 -m pip install -U selenium

# Exit root
exit

```

To run a test do following:

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

# Install requirements
sudo -H pip3 install -r ~/Performance-test/requirements.txt

```