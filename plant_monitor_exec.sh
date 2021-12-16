# Create virtualenv if none exists
if [ -d pm_venv ]
then
  . pm_venv/bin/activate
else
  python3 -m venv pm_venv
  . pm_venv/bin/activate
  pip install --upgrade pip
  pip3 install -r requirements.txt
fi

#python --version

# Run program
python3 main.py

# Deactivate venv
deactivate
