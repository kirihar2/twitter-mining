#!/bin/bash
#sudo yum install -y python

pip3 install -U -r ${PWD}/requirements_pip.txt
mkdir weights
mkdir data

pip3 install -U ${PWD}/twitters_gen_package

python3 ${PWD}/web/backend/manage.py makemigrations
python3 ${PWD}/web/backend/manage.py migrate
