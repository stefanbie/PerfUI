#!/bin/bash
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

# Install python libs
sudo -H pip3 install -r ~/PerfUI/requirements.txt
