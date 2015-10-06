#!/bin/bash
yum install -y nginx flask python-flask git
service nginx restart
pip install virtualenv
mkdir hack
cd hack/
virtualenv venv
. venv/bin/activate
pip install Flask
git clone https://github.com/wjimenez5271/awsreinvent_t33
cd awsreinvent_t33/
pip install boto
pip install twilio
python sms_server.py
