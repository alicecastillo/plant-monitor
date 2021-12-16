# Created by: Alice Castillo

# Description: Main driver class


# Stlib imports
import sys
from datetime import datetime, timezone, timedelta

# Packages in requirements.txt
import argparse

# Class imports
from plant_specs.Plant import Plant
import environmental_factors


def getTime(offset: int) -> int:
    tz = timezone(timedelta(hours=offset))
    return int(datetime.now(tz).timestamp())

def init_plant(num: int) -> Plant:
    p = Plant(num)
    return p


def main(args): # optional args for configuring email, notification settings

    # ***TO-DO***
    # Add in check for configs

    cur_time = getTime(-6) # Central Time (UTC-06:00)
    print(cur_time)
    p = init_plant(1) # Subject 1
    p.getReadings(cur_time)
    p.writeLogs()


if __name__ == "__main__":
    main(sys.argv)
