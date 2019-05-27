#!/bin/bash
#sudo yum install -y python
pip install -y -r ../requirements_pip.txt
mkdir weights
mkdir data
pip install ../twitters_gen_package

python web/backend/manage.py makemigrations
python web/backend/manage.py migrate
