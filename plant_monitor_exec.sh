#!/bin/sh

# Create virtualenv if none exists
if [ ! -d pm_venv ]
then
  python3 -m venv pm_venv
fi

. pm_venv/bin/activate
pip install --upgrade pip
#sudo apt-get install libatlas-base-dev
pip3 install -r requirements.txt

#python --version

# Run program
python3 main.py

# Deactivate venv
deactivate
