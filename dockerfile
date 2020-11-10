FROM ubuntu

RUN apt-get update
RUN apt-get install -y curl gnupg unzip python3-pip

RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add
RUN echo "deb [arch=amd64]  http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get -y update
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get -y install google-chrome-stable

RUN wget https://chromedriver.storage.googleapis.com/86.0.4240.22/chromedriver_linux64.zip

RUN unzip chromedriver_linux64.zip
RUN mv chromedriver /usr/bin/chromedriver
RUN chown root:root /usr/bin/chromedriver
RUN chmod +x /usr/bin/chromedriver

RUN apt-get install -y git

RUN git clone https://github.com/stefanbie/PerfUI.git
RUN pip3 install -r PerfUI/requirements.txt

CMD ["python3", "main.py --conf=./tests/conf.json"]