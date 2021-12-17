# Created by: Alice Castillo

# Description: Generic base class for any plant.
import json
import time
import os
from datetime import datetime
import xlsxwriter
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, Fill, PatternFill

# Import sensor classes
from plant_specs.VEML6070 import VEML6070
from plant_specs.DHT11 import DHT11
from plant_specs.subject_logs.LogFile import  LogFile



class Plant():
    def __init__(self, num: int, reqs: list = []):
        self.species_filepath, self.species_filename = "", ""
        self.loadData(num)
        self.num = num
        self.last_ht_check, self.last_uv_check, self.last_water = 0, 0, 0

    def loadData(self, num: int):
        # get subject file
        sub_json = self.readJSONFile("plant_specs/current_subjects/subject_{0}.json".format(num))
        self.last_ht_check = sub_json["last_ht_check"]
        self.last_uv_check = sub_json["last_uv_check"]
        self.last_water = sub_json["last_water"]

        # move this to outside method if possible later
        #self.species_filepath = "plant_specs/species/{0}.json".format(sub_json["species_filename"])
        self.species_filename = sub_json["species_filename"]

    def readJSONFile(self, path):
        f = open(os.path.join(os.getcwd(), path), "r")
        return json.load(f)

    def getReadings(self, cur_time: int) -> None:
        sensors = [VEML6070(cur_time)]
        cur_min = int(datetime.fromtimestamp(cur_time).strftime("%M"))
        if cur_min % 30:
            sensors.append(DHT11(cur_time))

        #if int(datetime.fromtimestamp(cur_time).strftime("%H")) cur_min == 0:
        #     # create Excel file
        log_file = LogFile(
            "SUBJECT{0}_{1}_logs".format(self.num, datetime.fromtimestamp(cur_time).strftime("%b_%d_%Y")),
            cur_time
        )

        for i in range(60):
            for sensor in sensors:
                sensor.runSensor(i)
            time.sleep(1)
        for sensor in sensors:
            sensor.writeLogFile(self.species_filename, log_file)
        log_file.applyHeaderStyling()
