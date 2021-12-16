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


def init_plant(num: int, cur_time: int) -> None:
    p = Plant(num)
    p.getReadings(cur_time)
    p.writeLogs()


def main(args): # optional args for configuring email, notification settings

    # ***TO-DO***
    # Add in check for configs

    cur_time = getTime(-6) # Central Time (UTC-06:00)
    init_plant(1, cur_time) # Subject 1


if __name__ == "__main__":
    main(sys.argv)
