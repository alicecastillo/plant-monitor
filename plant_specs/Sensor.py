# Created by: Alice Castillo

# Description: Generic base class for any sensor.
import json
import numpy as np
from datetime import datetime
from openpyxl import Workbook

# Local class imports
from subject_logs.LogFile import LogFile, EvalColor


class Sensor():
    def __init__(self, cur_time: int, sleep_interval: int):
        self.cur_time = cur_time
        self.sleep_interval = sleep_interval

        # non init
        self.logs, self.sensor, self.log_file = None, None, ""

    # Overwritten by children
    def runSensor(self, sec: int):
        pass

    def writeLogFile(self, species_filename: str, log_file: LogFile):
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

    def getMedian(self, log) -> str:
        if not len(log):
            return "Error"
        a = np.array(log)
        return str(np.median(a))

    def getAvg(self, log) -> str:
        if not len(log):
            return "Error"
        a = np.array(log)
        return str(np.mean(a))

    def getLogColors(self, log_data, range) -> []:
        log_colors = []
        for count, ld in enumerate(log_data):
            if str(ld).__contains__("Error"):
                log_colors.append(EvalColor.Error)
            elif ld < range[0]:
                log_colors.append(EvalColor.Lower)
            elif range[0] < ld < range[1]:
                log_colors.append(EvalColor.Equal)
            else:
                log_colors.append(EvalColor.Greater)
        return log_colors
