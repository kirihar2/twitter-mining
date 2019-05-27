#!/bin/bash
#sudo yum install -y python

pip install -U -r ${PWD}/requirements_pip.txt
mkdir weights
mkdir data

pip install -U ${PWD}/twitters_gen_package

python ${PWD}/web/backend/manage.py makemigrations
python ${PWD}/web/backend/manage.py migrate
