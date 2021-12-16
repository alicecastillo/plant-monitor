# Created by: Alice Castillo

# Description: Generic base class for any sensor.
import json
import os
from datetime import datetime

class Sensor():
    def __init__(self, cur_time: int, sleep_interval: int):
        self.cur_time = cur_time
        self.sleep_interval = sleep_interval

        # non init
        self.logs, self.sensor, self.log_file = None, None, ""

    # Overwritten by children
    def runSensor(self, sec: int):
        pass

    def writeLogFile(self, species_filename: str, subj_num: int):
        pass


    # Generalized methods
    def returnResults(self) -> tuple:
        return self.log_file

    def getSleepInterval(self):
        return self.sleep_interval

    def readyToRead(self, sec):
        return not sec%self.sleep_interval

    def releaseSensor(self):
        if self.sensor:
            self.sensor.exit()

    def getSpeciesFile(self, p: str):
        species_json = self.readJSONFile(f"plant_specs/species/{p}.json")
        return species_json["requirements"]

    def getFileDate(self, subj) -> str:
        d = datetime.fromtimestamp(self.cur_time)
        return "SUBJECT{0}_{1}_logs".format(subj, d.strftime("%b_%d_%Y"))
