#!/bin/bash
LOG_FILE=/var/install.log
yum install -y nginx flask python-flask git
echo "1. Yum installs done" >> /var/install.log
service nginx restart
echo "1.1" >> /var/install.log
pip install virtualenv
echo "1.2" >> /var/install.log
mkdir hack
echo "1.3" >> /var/install.log
cd hack/
echo "1.4" >> /var/install.log
virtualenv venv
echo "1.5" >> /var/install.log
. venv/bin/activate
echo "2. VitrtualEnv installed">> /var/install.log
pip install Flask
echo "2.1" >> /var/install.log
git clone https://github.com/wjimenez5271/awsreinvent_t33
echo "2.2" >> /var/install.log
cd awsreinvent_t33/
echo "2.3" >> /var/install.log
pip install boto
echo "2.4" >> /var/install.log
pip install twilio
echo "3. Twilio ready" >> /var/install.log
python sms_receiver.py &
python sms_send.py

echo "End" >> /var/install.log
