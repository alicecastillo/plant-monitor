# Create virtualenv if none exists
if [ -d plant_monitor_venv ]
then
  #echo "plant_monitor_venv already exists"
  source plant_monitor_venv/bin/activate
else
  python3 -m venv plant_monitor_venv
  source plant_monitor_venv/bin/activate
  pip3 install -r requirements.txt
fi

# Run program
python3 main.py

# Deactivate venv
deactivate
